"""Passive, offline NetBIOS name-service query decoder.

Historical NBNS/WPAD spoofing scripts are deliberately not executed. This
decoder accepts captured UDP payloads and never sends or constructs responses.
"""
from __future__ import annotations

import struct

from .analysis import AnalysisError, base_report


def analyze_nbns_query(payload: bytes, source: str = "NBNS UDP payload") -> dict:
    """Decode a single NBNS query without resolving names or sending traffic."""
    if len(payload) > 65535 or len(payload) < 12:
        raise AnalysisError("Invalid NBNS datagram length.")
    transaction, flags, questions, answers, authority, additional = struct.unpack_from("!HHHHHH", payload)
    if flags & 0x8000:
        raise AnalysisError("Expected an NBNS query, not a response.")
    if questions != 1 or answers or authority or additional:
        raise AnalysisError("Only a single standard NBNS question is supported.")
    offset = 12
    if offset >= len(payload):
        raise AnalysisError("Missing NBNS name.")
    encoded_length = payload[offset]
    offset += 1
    if encoded_length != 32 or offset + encoded_length + 5 > len(payload):
        raise AnalysisError("Invalid or truncated NBNS first-level name.")
    encoded = payload[offset:offset + encoded_length]
    if any(value < 65 or value > 80 for value in encoded):
        raise AnalysisError("Invalid NBNS first-level encoding.")
    decoded = bytes(((encoded[i] - 65) << 4) | (encoded[i + 1] - 65) for i in range(0, 32, 2))
    offset += 32
    if payload[offset] != 0:
        raise AnalysisError("Compressed or scoped NBNS names are not supported.")
    offset += 1
    query_type, query_class = struct.unpack_from("!HH", payload, offset)
    if query_class != 1:
        raise AnalysisError("Unsupported NBNS query class.")
    report = base_report("nbns_query", source)
    name = decoded[:15].decode("ascii", errors="replace").rstrip()
    report["queries"] = [{
        "transaction_id": transaction, "name": name,
        "suffix": decoded[15], "query_type": query_type,
    }]
    report["stats"] = {"queries": 1, "wpad_queries": int(name.upper() == "WPAD")}
    if name.upper() == "WPAD":
        report["findings"].append({
            "code": "wpad_query_observed", "severity": "info",
            "message": "WPAD name resolution was requested.",
            "interpretation": "A WPAD query alone does not establish interception or exploitation.",
        })
    return report