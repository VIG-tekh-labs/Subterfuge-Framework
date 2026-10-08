"""Bounded, payload-free packet and network-inventory analysis."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from ipaddress import ip_address
from pathlib import Path
import io
import json
import math
import os
import struct
import tempfile
import xml.etree.ElementTree as ET
from xml.parsers import expat

from . import __version__

MAX_INPUT_BYTES = 64 * 1024 * 1024
MAX_PACKET_BYTES = 1024 * 1024
MAX_PACKETS = 250_000
MAX_HOSTS = 10_000
MAX_FINDINGS = 10_000
MAX_MACS_PER_HOST = 256
MAX_XML_ELEMENTS = 250_000
MAX_XML_DEPTH = 64


class AnalysisError(ValueError):
    """An input cannot be safely or reliably interpreted."""


def base_report(kind: str, source: str) -> dict:
    return {
        "schema_version": 1,
        "tool_version": __version__,
        "kind": kind,
        "source": source,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "hosts": [],
        "findings": [],
        "warnings": [],
        "stats": {},
    }


class ArpTracker:
    """Record address claims and possible conflicts, without packet payloads."""

    def __init__(self, source: str, kind: str = "pcap") -> None:
        self.report = base_report(kind, source)
        self.hosts: dict[str, dict] = {}
        self.conflicts: dict[str, dict] = {}
        self.arp_packets = 0
        self.operations: Counter[int] = Counter()

    def observe(self, ip: str, mac: str, operation: int, timestamp: float | None) -> None:
        if operation not in (1, 2):
            return
        self.arp_packets += 1
        self.operations[operation] += 1
        address = ip_address(ip)
        if address.version != 4 or (timestamp is not None and not math.isfinite(timestamp)):
            raise AnalysisError("ARP observations require IPv4 and a finite timestamp when known.")
        raw_mac = bytes.fromhex(mac.replace(":", ""))
        if len(raw_mac) != 6:
            raise AnalysisError("Invalid Ethernet address.")
        if address.is_unspecified or address.is_multicast or ip == "255.255.255.255":
            return
        if not any(raw_mac) or raw_mac[0] & 1:
            return
        if ip not in self.hosts:
            if len(self.hosts) >= MAX_HOSTS:
                raise AnalysisError("Host limit exceeded.")
            self.hosts[ip] = {
                "address": ip, "mac_addresses": set(), "observations": 0,
                "first_seen": timestamp, "last_seen": timestamp,
            }
        host = self.hosts[ip]
        if mac.lower() not in host["mac_addresses"] and len(host["mac_addresses"]) >= MAX_MACS_PER_HOST:
            raise AnalysisError("MAC address limit exceeded for one host.")
        host["mac_addresses"].add(mac.lower())
        host["observations"] += 1
        if timestamp is not None:
            host["first_seen"] = timestamp if host["first_seen"] is None else min(host["first_seen"], timestamp)
            host["last_seen"] = timestamp if host["last_seen"] is None else max(host["last_seen"], timestamp)
        if len(host["mac_addresses"]) > 1:
            if ip not in self.conflicts:
                if len(self.conflicts) >= MAX_FINDINGS:
                    raise AnalysisError("Finding limit exceeded.")
                finding = {
                    "code": "arp_address_conflict", "severity": "warning",
                    "address": ip, "mac_addresses": [],
                    "message": "Multiple MAC addresses claimed one IPv4 address.",
                    "interpretation": "Possible ARP spoofing, address reuse or legitimate failover; investigate before drawing a conclusion.",
                }
                self.conflicts[ip] = finding
                self.report["findings"].append(finding)
            self.conflicts[ip]["mac_addresses"] = sorted(host["mac_addresses"])

    def finish(self, packets: int, ignored: int = 0) -> dict:
        self.report["hosts"] = [
            {**host, "mac_addresses": sorted(host["mac_addresses"])}
            for _, host in sorted(self.hosts.items(), key=lambda item: int(ip_address(item[0])))
        ]
        self.report["stats"] = {
            "packets": packets, "arp_packets": self.arp_packets,
            "ignored_packets": ignored, "hosts": len(self.hosts),
            "arp_requests": self.operations[1], "arp_replies": self.operations[2],
            "findings": len(self.report["findings"]),
        }
        return self.report


def _arp_frame(frame: bytes, linktype: int) -> tuple[str, str, int] | None:
    if linktype == 1:
        if len(frame) < 14:
            raise AnalysisError("Truncated Ethernet header.")
        protocol = struct.unpack_from("!H", frame, 12)[0]
        offset = 14
        tags = 0
        while protocol in (0x8100, 0x88A8, 0x9100):
            if len(frame) < offset + 4 or tags >= 4:
                raise AnalysisError("Invalid or excessive VLAN headers.")
            protocol = struct.unpack_from("!H", frame, offset + 2)[0]
            offset += 4
            tags += 1
    elif linktype == 113:
        if len(frame) < 16:
            raise AnalysisError("Truncated Linux cooked-capture header.")
        protocol = struct.unpack_from("!H", frame, 14)[0]
        offset = 16
    elif linktype == 276:
        if len(frame) < 20:
            raise AnalysisError("Truncated Linux cooked-capture v2 header.")
        protocol = struct.unpack_from("!H", frame, 0)[0]
        offset = 20
    else:
        raise AnalysisError(f"Unsupported capture link type: {linktype}.")
    if protocol != 0x0806:
        return None
    if len(frame) < offset + 8:
        raise AnalysisError("Truncated ARP header.")
    hardware, protocol, hardware_len, protocol_len, operation = struct.unpack_from("!HHBBH", frame, offset)
    if (hardware, protocol, hardware_len, protocol_len) != (1, 0x0800, 6, 4):
        return None
    if len(frame) < offset + 28:
        raise AnalysisError("Truncated ARP address data.")
    mac = frame[offset + 8:offset + 14].hex(":")
    ip = str(ip_address(frame[offset + 14:offset + 18]))
    return ip, mac, operation



def _analyze_pcapng(data: bytes, source: str) -> dict:
    """Decode bounded PCAPNG, retaining only ARP and passive protocol evidence.

    Supports enhanced packet blocks, obsolete packet blocks and simple packet
    blocks. Simple packet blocks have no timestamp; unknown time is represented
    as None rather than an invented epoch.
    """
    if len(data) > MAX_INPUT_BYTES:
        raise AnalysisError("Capture exceeds the 64 MiB input limit.")
    if len(data) < 28:
        raise AnalysisError("Truncated PCAPNG section header.")
    from .udp_evidence import EvidenceAccumulator
    tracker = ArpTracker(source, kind="pcapng")
    passive = EvidenceAccumulator()
    position = 0
    endian = None
    interfaces: list[tuple[int, int, float, int]] = []
    packets = ignored = sections = untimed = 0

    def observe_frame(frame: bytes, linktype: int, timestamp: float | None) -> None:
        nonlocal packets, ignored
        packets += 1
        if packets > MAX_PACKETS:
            raise AnalysisError("Packet limit exceeded.")
        try:
            event = _arp_frame(frame, linktype)
        except AnalysisError:
            event = None
        if event is not None:
            tracker.observe(*event, timestamp)
        elif not passive.observe(frame, linktype):
            ignored += 1

    while position < len(data):
        if len(data) - position < 12:
            raise AnalysisError("Truncated PCAPNG block header.")
        if data[position:position + 4] == b"\x0a\x0d\x0d\x0a":
            if len(data) - position < 28:
                raise AnalysisError("Truncated PCAPNG section header.")
            marker = data[position + 8:position + 12]
            if marker == b"\x4d\x3c\x2b\x1a":
                endian = "<"
            elif marker == b"\x1a\x2b\x3c\x4d":
                endian = ">"
            else:
                raise AnalysisError("Invalid PCAPNG byte-order marker.")
            block_type = 0x0A0D0D0A
        else:
            if endian is None:
                raise AnalysisError("PCAPNG requires a section header.")
            block_type = struct.unpack_from(endian + "I", data, position)[0]
        length = struct.unpack_from(endian + "I", data, position + 4)[0]
        if length < 12 or length % 4 or length > len(data) - position:
            raise AnalysisError("Invalid or truncated PCAPNG block length.")
        if struct.unpack_from(endian + "I", data, position + length - 4)[0] != length:
            raise AnalysisError("PCAPNG block length trailer mismatch.")
        body = position + 8
        body_end = position + length - 4

        if block_type == 0x0A0D0D0A:
            if length < 28 or struct.unpack_from(endian + "HH", data, body + 4) != (1, 0):
                raise AnalysisError("Unsupported PCAPNG section version.")
            sections += 1
            interfaces = []
        elif block_type == 1:
            if body_end - body < 8:
                raise AnalysisError("Truncated PCAPNG interface block.")
            linktype, _, snaplen = struct.unpack_from(endian + "HHI", data, body)
            if len(interfaces) >= 256 or not 0 < snaplen <= MAX_PACKET_BYTES:
                raise AnalysisError("Invalid PCAPNG interface count or snapshot length.")
            if linktype not in (1, 113, 276):
                raise AnalysisError(f"Unsupported capture link type: {linktype}.")
            resolution = 1e-6
            offset_seconds = 0
            option = body + 8
            while option < body_end:
                if body_end - option < 4:
                    raise AnalysisError("Truncated PCAPNG interface option.")
                code, size = struct.unpack_from(endian + "HH", data, option)
                option += 4
                padded = (size + 3) & ~3
                if padded > body_end - option:
                    raise AnalysisError("Invalid PCAPNG option length.")
                if code == 0:
                    if size != 0:
                        raise AnalysisError("Invalid PCAPNG end-of-options.")
                    break
                if code == 9:
                    if size != 1:
                        raise AnalysisError("Invalid PCAPNG timestamp resolution.")
                    value = data[option]
                    resolution = (2.0 ** -(value & 127)) if value & 128 else (10.0 ** -value)
                    if resolution == 0 or not math.isfinite(resolution):
                        raise AnalysisError("Invalid PCAPNG timestamp resolution.")
                elif code == 14:
                    if size != 8:
                        raise AnalysisError("Invalid PCAPNG timestamp offset.")
                    offset_seconds = struct.unpack_from(endian + "q", data, option)[0]
                option += padded
            interfaces.append((linktype, snaplen, resolution, offset_seconds))
        elif block_type in (2, 6):
            if body_end - body < 20:
                raise AnalysisError("Truncated PCAPNG packet block.")
            if block_type == 2:
                interface_id, _drop_count, ts_hi, ts_lo, captured, original = struct.unpack_from(
                    endian + "HHIIII", data, body
                )
            else:
                interface_id, ts_hi, ts_lo, captured, original = struct.unpack_from(
                    endian + "IIIII", data, body
                )
            if interface_id >= len(interfaces):
                raise AnalysisError("PCAPNG packet refers to missing interface.")
            linktype, snaplen, resolution, offset_seconds = interfaces[interface_id]
            if (captured > snaplen or captured > MAX_PACKET_BYTES
                    or captured > original
                    or ((captured + 3) & ~3) > body_end - (body + 20)):
                raise AnalysisError("Invalid PCAPNG packet length.")
            timestamp = ((ts_hi << 32) | ts_lo) * resolution + offset_seconds
            if not math.isfinite(timestamp):
                raise AnalysisError("Invalid PCAPNG timestamp.")
            observe_frame(data[body + 20:body + 20 + captured], linktype, timestamp)
        elif block_type == 3:
            if body_end - body < 4:
                raise AnalysisError("Truncated PCAPNG simple packet.")
            if not interfaces:
                raise AnalysisError("PCAPNG simple packet requires interface zero.")
            linktype, snaplen, _, _ = interfaces[0]
            original = struct.unpack_from(endian + "I", data, body)[0]
            captured = min(original, snaplen)
            if (captured > MAX_PACKET_BYTES
                    or body_end - (body + 4) != ((captured + 3) & ~3)):
                raise AnalysisError("Invalid PCAPNG simple packet length.")
            observe_frame(data[body + 4:body + 4 + captured], linktype, None)
            untimed += 1
        position += length

    if not sections:
        raise AnalysisError("PCAPNG has no section header.")
    if ignored:
        tracker.report["warnings"].append(
            "Non-ARP, non-DHCP/NBNS or incomplete frames were ignored."
        )
    if untimed:
        tracker.report["warnings"].append(
            "Simple PCAPNG packets lack timestamps; host times may be unknown or partial."
        )
    tracker.report["capture"] = {
        "format": "pcapng", "sections": sections,
        "interfaces_last_section": len(interfaces),
        "untimed_packets": untimed,
    }
    return passive.extend(tracker.finish(packets, ignored))


def analyze_pcap(data: bytes, source: str = "capture") -> dict:
    """Analyze classic PCAP or bounded PCAPNG enhanced packets."""
    if len(data) > MAX_INPUT_BYTES:
        raise AnalysisError("Capture exceeds the 64 MiB input limit.")
    if len(data) < 24:
        raise AnalysisError("Truncated PCAP header.")
    formats = {
        b"\xd4\xc3\xb2\xa1": ("<", 1_000_000),
        b"\xa1\xb2\xc3\xd4": (">", 1_000_000),
        b"\x4d\x3c\xb2\xa1": ("<", 1_000_000_000),
        b"\xa1\xb2\x3c\x4d": (">", 1_000_000_000),
    }
    if data[:4] == b"\x0a\x0d\x0d\x0a":
        return _analyze_pcapng(data, source)
    if data[:4] not in formats:
        raise AnalysisError("Unrecognized PCAP format.")
    endian, resolution = formats[data[:4]]
    major, minor, _, _, snaplen, network = struct.unpack_from(endian + "HHiiII", data, 4)
    linktype = network & 0xFFFF
    if (major, minor) != (2, 4) or not 0 < snaplen <= MAX_PACKET_BYTES:
        raise AnalysisError("Unsupported PCAP version or snapshot length.")
    if linktype not in (1, 113, 276):
        raise AnalysisError(f"Unsupported capture link type: {linktype}.")
    from .udp_evidence import EvidenceAccumulator
    tracker = ArpTracker(source)
    passive = EvidenceAccumulator()
    tracker.report["capture"] = {"link_type": linktype, "snapshot_length": snaplen}
    stream = io.BytesIO(data[24:])
    packets = ignored = 0
    while header := stream.read(16):
        if len(header) != 16:
            raise AnalysisError("Truncated PCAP packet header.")
        seconds, fraction, length, original_length = struct.unpack(endian + "IIII", header)
        if fraction >= resolution or length > snaplen or length > original_length or length > MAX_PACKET_BYTES:
            raise AnalysisError("Invalid PCAP packet length or timestamp.")
        frame = stream.read(length)
        if len(frame) != length:
            raise AnalysisError("Truncated PCAP packet data.")
        packets += 1
        if packets > MAX_PACKETS:
            raise AnalysisError("Packet limit exceeded.")
        try:
            event = _arp_frame(frame, linktype)
        except AnalysisError:
            ignored += 1
            continue
        if event is None:
            if not passive.observe(frame, linktype):
                ignored += 1
            continue
        tracker.observe(*event, seconds + fraction / resolution)
    if ignored:
        tracker.report["warnings"].append("Non-ARP, non-DHCP/NBNS or incomplete frames were ignored.")
    return passive.extend(tracker.finish(packets, ignored))


def _nmap_xml(data: bytes) -> ET.Element:
    """Build XML while rejecting DTD resources, entities and excessive trees."""
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise AnalysisError("Nmap XML must use UTF-8 or ASCII encoding.") from exc
    if "\x00" in text:
        raise AnalysisError("Nmap XML must use UTF-8 or ASCII encoding.")
    parser = expat.ParserCreate()
    builder = ET.TreeBuilder()
    elements = depth = 0

    def declaration(version, encoding, standalone):
        if version != "1.0" or encoding and encoding.lower() not in {"utf-8", "utf8", "ascii", "us-ascii"}:
            raise AnalysisError("Nmap XML requires XML 1.0 with UTF-8 or ASCII encoding.")

    def doctype(name, system_id, public_id, internal_subset):
        if name != "nmaprun" or system_id is not None or public_id is not None or internal_subset:
            raise AnalysisError("Only the plain Nmap DOCTYPE is accepted; external and internal DTDs are disabled.")

    def entity(*args):
        raise AnalysisError("XML entity declarations and external resources are disabled.")

    def start(name, attributes):
        nonlocal elements, depth
        elements += 1
        depth += 1
        if elements > MAX_XML_ELEMENTS or depth > MAX_XML_DEPTH:
            raise AnalysisError("XML element or nesting limit exceeded.")
        builder.start(name, attributes)

    def end(name):
        nonlocal depth
        builder.end(name)
        depth -= 1

    parser.XmlDeclHandler = declaration
    parser.StartDoctypeDeclHandler = doctype
    parser.EntityDeclHandler = entity
    parser.ExternalEntityRefHandler = entity
    parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_NEVER)
    parser.StartElementHandler = start
    parser.EndElementHandler = end
    parser.CharacterDataHandler = builder.data
    try:
        parser.Parse(text, True)
        return builder.close()
    except (expat.ExpatError, ET.ParseError) as exc:
        raise AnalysisError("Invalid Nmap XML.") from exc


def analyze_nmap(data: bytes, source: str = "inventory") -> dict:
    if len(data) > MAX_INPUT_BYTES:
        raise AnalysisError("Inventory exceeds the 64 MiB input limit.")
    root = _nmap_xml(data)
    if root.tag != "nmaprun":
        raise AnalysisError("Expected an Nmap XML document.")
    report = base_report("nmap", source)
    for node in root.findall("host"):
        if len(report["hosts"]) >= MAX_HOSTS:
            raise AnalysisError("Host limit exceeded.")
        addresses = []
        macs = []
        for entry in node.findall("address"):
            value = entry.get("addr", "")
            if entry.get("addrtype") in ("ipv4", "ipv6"):
                try:
                    addresses.append(str(ip_address(value)))
                except ValueError as exc:
                    raise AnalysisError("Invalid IP address in inventory.") from exc
            elif entry.get("addrtype") == "mac":
                macs.append(value.lower())
        status = node.find("status")
        ports = []
        for port in node.findall("ports/port"):
            try:
                number = int(port.get("portid", ""))
            except ValueError as exc:
                raise AnalysisError("Invalid port in inventory.") from exc
            if not 1 <= number <= 65535:
                raise AnalysisError("Port outside valid range.")
            state, service = port.find("state"), port.find("service")
            ports.append({
                "port": number, "protocol": port.get("protocol", "unknown"),
                "state": state.get("state", "unknown") if state is not None else "unknown",
                "service": service.get("name", "unknown") if service is not None else "unknown",
                "product": service.get("product", "")[:256] if service is not None else "",
                "version": service.get("version", "")[:256] if service is not None else "",
                "tunnel": service.get("tunnel", "")[:64] if service is not None else "",
            })
            record = ports[-1]
            cleartext = {"ftp", "telnet", "http", "pop3", "imap", "smtp"}
            if record["state"] == "open" and record["service"] in cleartext and record["tunnel"] != "ssl":
                if len(report["findings"]) >= MAX_FINDINGS:
                    raise AnalysisError("Finding limit exceeded.")
                report["findings"].append({
                    "code": "service_transport_review", "severity": "info",
                    "address": addresses[0] if addresses else "unknown",
                    "port": number, "protocol": record["protocol"],
                    "message": f"Review transport protection for {record['service']} on port {number}.",
                    "interpretation": "The inventory does not record an SSL tunnel. STARTTLS, redirects and access controls may still protect this service; this is not a confirmed vulnerability.",
                })
        report["hosts"].append({
            "addresses": addresses, "mac_addresses": sorted(set(macs)),
            "status": status.get("state", "unknown") if status is not None else "unknown",
            "hostnames": [h.get("name", "")[:256] for h in node.findall("hostnames/hostname")],
            "ports": ports,
            "operating_systems": [
                {"name": match.get("name", "")[:256], "accuracy": match.get("accuracy", "")[:8]}
                for match in node.findall("os/osmatch")[:16]
            ],
        })
    report["stats"] = {
        "hosts": len(report["hosts"]),
        "open_ports": sum(p["state"] == "open" for h in report["hosts"] for p in h["ports"]),
        "findings": len(report["findings"]),
    }
    return report


def read_input(path: str | Path) -> bytes:
    with Path(path).open("rb") as handle:
        data = handle.read(MAX_INPUT_BYTES + 1)
    if len(data) > MAX_INPUT_BYTES:
        raise AnalysisError("Input exceeds the 64 MiB limit.")
    return data


def write_report(report: dict, path: str | Path) -> None:
    """Write a private report atomically, keeping a previous report on failure."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=destination.parent, prefix=".subterfuge-", delete=False) as handle:
            temporary = Path(handle.name)
            os.chmod(temporary, 0o600)
            json.dump(report, handle, indent=2, ensure_ascii=False, allow_nan=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)