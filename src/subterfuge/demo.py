"""Synthetic documentation-range capture for offline demonstrations."""

from ipaddress import ip_address
import struct

from .analysis import analyze_pcap


def sample_capture() -> bytes:
    header = struct.pack("<IHHiiII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1)
    records = []
    for offset, mac in enumerate([bytes.fromhex("020000000010"), bytes.fromhex("020000000020")]):
        frame = b"\xff" * 6 + mac + b"\x08\x06"
        frame += struct.pack("!HHBBH", 1, 0x0800, 6, 4, 2)
        frame += mac + ip_address("192.0.2.10").packed
        frame += b"\x00" * 6 + ip_address("192.0.2.1").packed
        records.append(struct.pack("<IIII", 1_700_000_000 + offset, 0, len(frame), len(frame)) + frame)
    return header + b"".join(records)


def demo_report() -> dict:
    report = analyze_pcap(sample_capture(), "synthetic demonstration")
    report["kind"] = "demo"
    report["warnings"].insert(0, "Synthetic data only. No traffic was sent or captured.")
    return report

