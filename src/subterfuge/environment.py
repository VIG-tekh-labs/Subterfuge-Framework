"""Local runtime checks and bounded, explicit network inventory."""

from __future__ import annotations

from importlib import metadata
from ipaddress import ip_address, ip_network
from pathlib import Path
import json
import math
import os
import platform
import shutil
import socket
import subprocess
import sys

from .analysis import AnalysisError, ArpTracker, MAX_PACKETS, analyze_nmap
from . import __version__


def interfaces() -> list[dict]:
    try:
        records = [{"index": index, "name": name} for index, name in socket.if_nameindex()]
    except OSError:
        records = []
        try:
            for path in sorted(Path("/sys/class/net").iterdir()):
                try:
                    records.append({"index": int((path / "ifindex").read_text()), "name": path.name})
                except (OSError, ValueError):
                    continue
        except OSError:
            pass
    for item in records:
        path = Path("/sys/class/net") / item["name"]
        for field, filename in [("mac_address", "address"), ("state", "operstate")]:
            try:
                item[field] = (path / filename).read_text().strip()
            except OSError:
                pass
    executable = shutil.which("ip")
    if executable:
        try:
            result = subprocess.run([executable, "-j", "address", "show"], capture_output=True, text=True, timeout=5, check=True)
            addresses = {item["ifname"]: item.get("addr_info", []) for item in json.loads(result.stdout)}
            for record in records:
                record["addresses"] = [
                    {"address": item["local"], "prefix_length": item["prefixlen"], "family": item["family"]}
                    for item in addresses.get(record["name"], [])
                ]
        except (OSError, subprocess.SubprocessError, ValueError, KeyError, TypeError):
            pass
    return records


def doctor() -> dict:
    try:
        scapy_version = metadata.version("scapy")
    except metadata.PackageNotFoundError:
        scapy_version = None
    return {
        "version": __version__, "python": platform.python_version(),
        "platform": platform.system(), "python_supported": sys.version_info >= (3, 11),
        "offline_analysis": True, "nmap": shutil.which("nmap"),
        "scapy": scapy_version, "interfaces": interfaces(),
        "capture_note": "Live capture requires the capture extra and operating-system packet-capture permissions.",
    }


def discover(target: str, timeout: float = 60) -> dict:
    if not math.isfinite(timeout) or not 0 < timeout <= 300:
        raise AnalysisError("Discovery timeout must be greater than zero and at most 300 seconds.")
    try:
        network = ip_network(target, strict=False)
    except ValueError as exc:
        raise AnalysisError("Use an explicit IP address or CIDR network.") from exc
    if network.num_addresses > 256:
        raise AnalysisError("Discovery is limited to 256 addresses per invocation.")
    executable = shutil.which("nmap")
    if not executable:
        raise AnalysisError("Nmap is not installed. Offline Nmap XML import remains available.")
    command = [executable, "-sn", "-oX", "-"]
    if network.version == 6:
        command.append("-6")
    command.append(str(network))
    try:
        result = subprocess.run(command, capture_output=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise AnalysisError("Network discovery timed out.") from exc
    if result.returncode:
        error = result.stderr.decode("utf-8", errors="replace").strip()[:300]
        raise AnalysisError("Nmap discovery failed: " + (error or str(result.returncode)))
    report = analyze_nmap(result.stdout, str(network))
    report["kind"] = "discovery"
    return report


def scan_services(target: str, ports: str = "22,80,443", timeout: float = 120) -> dict:
    """Optional, explicit low-volume TCP connect inventory for one authorized IP.

    Uses Nmap's user-space TCP connect mode (no raw-socket/root requirement).
    The only network traffic occurs when a user explicitly invokes this API.
    """
    try:
        address = ip_address(target)
    except ValueError as exc:
        raise AnalysisError("Use one explicit IPv4 or IPv6 address (not a hostname or CIDR).") from exc
    if not math.isfinite(timeout) or not 0 < timeout <= 300:
        raise AnalysisError("Scan timeout must be greater than zero and at most 300 seconds.")
    if not isinstance(ports, str):
        raise AnalysisError("Ports must be a comma-separated string.")
    tokens = [value.strip() for value in ports.split(",")]
    if not 1 <= len(tokens) <= 32 or any(not token or not token.isascii() or not token.isdecimal() for token in tokens):
        raise AnalysisError("Specify 1 to 32 explicit TCP port numbers.")
    numbers = [int(value) for value in tokens]
    if len(set(numbers)) != len(numbers) or any(not 1 <= value <= 65535 for value in numbers):
        raise AnalysisError("TCP ports must be unique numbers between 1 and 65535.")
    executable = shutil.which("nmap")
    if not executable:
        raise AnalysisError("Nmap is not installed. Offline Nmap XML import remains available.")
    command = [
        executable, "-sT", "-Pn", "-sV", "--version-light",
        "--max-retries", "1", "-p", ",".join(str(value) for value in numbers),
        "-oX", "-",
    ]
    if address.version == 6:
        command.append("-6")
    command.append(str(address))
    try:
        result = subprocess.run(command, capture_output=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise AnalysisError("Service inventory timed out.") from exc
    if result.returncode:
        error = result.stderr.decode("utf-8", errors="replace").strip()[:300]
        raise AnalysisError("Nmap service inventory failed: " + (error or str(result.returncode)))
    report = analyze_nmap(result.stdout, str(address))
    report["kind"] = "service_scan"
    report["scan"] = {
        "target": str(address), "ports": numbers,
        "method": "explicit TCP connect, light service detection",
        "active_connections": True,
    }
    report["warnings"].append("An active service inventory was requested. Verify authorization before scanning third-party networks.")
    return report


def capture(interface: str, duration: float = 30, limit: int = 10_000) -> dict:
    if not math.isfinite(duration) or not 0 < duration <= 600:
        raise AnalysisError("Capture duration must be greater than zero and at most 600 seconds.")
    if not 1 <= limit <= MAX_PACKETS:
        raise AnalysisError(f"Packet limit must be between 1 and {MAX_PACKETS}.")
    if interface not in {item["name"] for item in interfaces()}:
        raise AnalysisError("Unknown network interface. Run 'subterfuge interfaces' to list interfaces.")
    try:
        from scapy.all import ARP, sniff
    except ImportError as exc:
        raise AnalysisError("Live capture is optional. Install with: python -m pip install 'subterfuge-framework[capture]'") from exc
    tracker = ArpTracker(interface, kind="live_arp")
    errors: list[str] = []
    packets = 0

    def observe(packet) -> None:
        nonlocal packets
        packets += 1
        try:
            arp = packet[ARP]
            tracker.observe(str(arp.psrc), str(arp.hwsrc), int(arp.op), float(packet.time))
        except (ValueError, TypeError, KeyError) as exc:
            if not errors:
                errors.append(str(exc))

    try:
        sniff(iface=interface, timeout=duration, count=limit, store=False,
              lfilter=lambda packet: packet.haslayer(ARP), prn=observe,
              stop_filter=lambda packet: bool(errors))
    except PermissionError as exc:
        raise AnalysisError("Packet-capture permission denied by the operating system.") from exc
    except OSError as exc:
        raise AnalysisError("Could not capture on the selected interface: " + str(exc)) from exc
    if errors:
        raise AnalysisError("Capture could not be fully analyzed: " + errors[0])
    tracker.report["capture"] = {"interface": interface, "requested_duration_seconds": duration, "packet_limit": limit}
    return tracker.finish(packets)
