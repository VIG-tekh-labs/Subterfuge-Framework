"""Offline extraction of bounded UDP evidence from Ethernet/IPv4 frames."""
from __future__ import annotations

import struct

from .analysis import AnalysisError
from .dhcp import analyze_dhcp
from .name_resolution import analyze_nbns_query


def inspect_ethernet_udp(frame: bytes) -> dict | None:
    """Inspect only unfragmented IPv4 UDP. Never retain raw payloads."""
    if len(frame) < 14:
        return None
    offset = 14
    protocol = struct.unpack_from("!H", frame, 12)[0]
    tags = 0
    while protocol in (0x8100, 0x88A8, 0x9100):
        if len(frame) < offset + 4 or tags >= 4:
            return None
        protocol = struct.unpack_from("!H", frame, offset + 2)[0]
        offset += 4
        tags += 1
    if protocol != 0x0800 or len(frame) < offset + 20:
        return None
    first = frame[offset]
    ihl = (first & 15) * 4
    if first >> 4 != 4 or ihl < 20 or len(frame) < offset + ihl:
        return None
    total = struct.unpack_from("!H", frame, offset + 2)[0]
    fragment = struct.unpack_from("!H", frame, offset + 6)[0]
    if fragment & 0x3fff or frame[offset + 9] != 17 or total < ihl + 8:
        return None
    if len(frame) < offset + total:
        return None
    udp_offset = offset + ihl
    sport, dport, udp_length = struct.unpack_from("!HHH", frame, udp_offset)
    if udp_length < 8 or udp_length > total - ihl:
        return None
    payload = frame[udp_offset + 8:udp_offset + udp_length]
    try:
        if {sport, dport} & {67, 68}:
            return analyze_dhcp(payload)
        if sport == 137 or dport == 137:
            return analyze_nbns_query(payload)
    except AnalysisError:
        return None
    return None