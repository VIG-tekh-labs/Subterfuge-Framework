"""Bounded, passive DHCPv4 evidence decoder; no network operations."""
from __future__ import annotations

from ipaddress import IPv4Address
import struct

from .analysis import AnalysisError, base_report

DHCP_MAGIC = bytes.fromhex("63825363")
MESSAGE_TYPES = {1: "discover", 2: "offer", 3: "request", 4: "decline",
                 5: "ack", 6: "nak", 7: "release", 8: "inform"}


def analyze_dhcp(payload: bytes, source: str = "DHCP UDP payload") -> dict:
    """Inspect one BOOTP/DHCPv4 payload without sending traffic or retaining secrets."""
    if not 240 <= len(payload) <= 65535:
        raise AnalysisError("Invalid DHCPv4 payload length.")
    operation, hardware, hardware_length, hops = struct.unpack_from("!BBBB", payload)
    if operation not in (1, 2) or hardware != 1 or hardware_length != 6:
        raise AnalysisError("Unsupported BOOTP hardware or operation.")
    if payload[236:240] != DHCP_MAGIC:
        raise AnalysisError("Missing DHCP magic cookie.")
    options = {}
    offset = 240
    while offset < len(payload):
        code = payload[offset]
        offset += 1
        if code == 255:
            break
        if code == 0:
            continue
        if offset >= len(payload):
            raise AnalysisError("Truncated DHCP option header.")
        size = payload[offset]
        offset += 1
        if size > len(payload) - offset:
            raise AnalysisError("Truncated DHCP option data.")
        value = payload[offset:offset + size]
        offset += size
        if code in (53, 54, 252) and code not in options:
            options[code] = value
    message = options.get(53, b"")
    if len(message) != 1 or message[0] not in MESSAGE_TYPES:
        raise AnalysisError("Missing or unsupported DHCP message type.")
    server = options.get(54)
    if server is not None and len(server) != 4:
        raise AnalysisError("Invalid DHCP server identifier.")
    report = base_report("dhcp", source)
    report["observations"] = [{
        "message_type": MESSAGE_TYPES[message[0]],
        "transaction_id": struct.unpack_from("!I", payload, 4)[0],
        "server_identifier": str(IPv4Address(server)) if server else None,
        "wpad_option_present": 252 in options,
    }]
    report["stats"] = {"messages": 1, "wpad_options": int(252 in options)}
    if 252 in options:
        report["findings"].append({
            "code": "dhcp_wpad_option_observed", "severity": "info",
            "message": "DHCP option 252 was present.",
            "interpretation": "Presence alone does not establish proxy abuse or interception; option contents are not retained.",
        })
    return report