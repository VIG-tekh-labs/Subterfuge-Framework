"""Bounded, passive DHCP and NBNS evidence from captured IPv4 UDP frames.

Only metadata needed for review is retained. No packet is transmitted.
"""
from __future__ import annotations

from collections import Counter
import struct

from .analysis import AnalysisError
from .dhcp import analyze_dhcp
from .name_resolution import analyze_nbns_query

MAX_EVIDENCE_GROUPS = 1024


def inspect_udp_frame(frame: bytes, linktype: int = 1) -> dict | None:
    """Inspect unfragmented IPv4 UDP carried over Ethernet or Linux cooked captures."""
    if linktype == 1:
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
    elif linktype == 113:
        if len(frame) < 16:
            return None
        protocol = struct.unpack_from("!H", frame, 14)[0]
        offset = 16
    elif linktype == 276:
        if len(frame) < 20:
            return None
        protocol = struct.unpack_from("!H", frame, 0)[0]
        offset = 20
    else:
        return None

    if protocol != 0x0800 or len(frame) < offset + 20:
        return None
    first = frame[offset]
    ihl = (first & 15) * 4
    if first >> 4 != 4 or ihl < 20 or len(frame) < offset + ihl:
        return None
    total = struct.unpack_from("!H", frame, offset + 2)[0]
    fragment = struct.unpack_from("!H", frame, offset + 6)[0]
    if fragment & 0x3FFF or frame[offset + 9] != 17 or total < ihl + 8:
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


def inspect_ethernet_udp(frame: bytes) -> dict | None:
    """Keep the original standalone API for compatibility."""
    return inspect_udp_frame(frame, linktype=1)


class EvidenceAccumulator:
    """Deduplicate bounded passive observations across a capture."""

    def __init__(self) -> None:
        self.groups: dict[tuple, dict] = {}
        self.counts: Counter[str] = Counter()

    def observe(self, frame: bytes, linktype: int) -> bool:
        result = inspect_udp_frame(frame, linktype)
        if result is None:
            return False
        kind = result["kind"]
        if kind == "dhcp":
            details = result["observations"][0]
            key = (
                kind, details["message_type"], details["server_identifier"],
                details["wpad_option_present"],
            )
            group = {
                "protocol": "dhcp", "message_type": details["message_type"],
                "server_identifier": details["server_identifier"],
                "wpad_option_present": details["wpad_option_present"],
            }
            self.counts["dhcp_messages"] += 1
            if details["wpad_option_present"]:
                self.counts["wpad_dhcp_options"] += 1
        else:
            details = result["queries"][0]
            key = (kind, details["name"], details["suffix"], details["query_type"])
            group = {
                "protocol": "nbns", "name": details["name"],
                "suffix": details["suffix"], "query_type": details["query_type"],
            }
            self.counts["nbns_queries"] += 1
            if details["name"].upper() == "WPAD":
                self.counts["wpad_nbns_queries"] += 1
        if key not in self.groups:
            if len(self.groups) >= MAX_EVIDENCE_GROUPS:
                raise AnalysisError("Distinct passive evidence group limit exceeded.")
            self.groups[key] = {**group, "observations": 0}
        self.groups[key]["observations"] += 1
        return True

    def extend(self, report: dict) -> dict:
        report["network_evidence"] = list(self.groups.values())
        report["stats"].update({
            "dhcp_messages": self.counts["dhcp_messages"],
            "nbns_queries": self.counts["nbns_queries"],
            "wpad_dhcp_options": self.counts["wpad_dhcp_options"],
            "wpad_nbns_queries": self.counts["wpad_nbns_queries"],
        })
        for name, count, message in (
            ("wpad_dhcp_options", self.counts["wpad_dhcp_options"], "WPAD DHCP option 252 was observed."),
            ("wpad_nbns_queries", self.counts["wpad_nbns_queries"], "WPAD NetBIOS name queries were observed."),
        ):
            if count:
                if len(report["findings"]) >= 10_000:
                    raise AnalysisError("Finding limit exceeded.")
                report["findings"].append({
                    "code": name, "severity": "info", "count": count,
                    "message": message,
                    "interpretation": "Observation does not establish interception, exploitation or malicious activity.",
                })
        report["stats"]["findings"] = len(report["findings"])
        return report