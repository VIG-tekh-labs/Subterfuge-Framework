"""Synthetic PCAPNG import regressions without network activity."""
import struct
import unittest
from subterfuge.analysis import AnalysisError, analyze_pcap
from subterfuge.demo import sample_capture


def block(kind, body, endian="<"):
    size = len(body) + 12
    return struct.pack(endian + "II", kind, size) + body + struct.pack(endian + "I", size)


def capture(endian="<", frame=None):
    if frame is None:
        frame = sample_capture()[40:82]
    section = block(0x0A0D0D0A, struct.pack(endian + "IHHq", 0x1A2B3C4D, 1, 0, -1), endian)
    interface = block(1, struct.pack(endian + "HHI", 1, 0, 65535), endian)
    padded = frame + b"\x00" * (-len(frame) % 4)
    packet = block(6, struct.pack(endian + "IIIII", 0, 0, 1700000000, len(frame), len(frame)) + padded, endian)
    return section + interface + packet


class PcapngTests(unittest.TestCase):
    def test_little_and_big_endian(self):
        for endian in ("<", ">"):
            with self.subTest(endian=endian):
                result = analyze_pcap(capture(endian))
                self.assertEqual(result["stats"]["arp_packets"], 1)
                self.assertEqual(result["kind"], "pcapng")

    def test_multiple_sections_with_different_byte_orders(self):
        report = analyze_pcap(capture("<") + capture(">"))
        self.assertEqual(report["stats"]["packets"], 2)
        self.assertEqual(report["stats"]["arp_packets"], 2)
        self.assertEqual(report["capture"]["sections"], 2)

    def test_timestamp_resolution_option(self):
        original = capture()
        section = original[:28]
        frame = sample_capture()[40:82]
        option = struct.pack("<HH", 9, 1) + bytes([9, 0, 0, 0])
        interface = block(1, struct.pack("<HHI", 1, 0, 65535) + option)
        packet = block(6, struct.pack("<IIIII", 0, 0, 1700000000, len(frame), len(frame)) + frame + bytes((-len(frame)) % 4))
        report = analyze_pcap(section + interface + packet)
        self.assertEqual(report["stats"]["arp_packets"], 1)

    def test_invalid_interface_option_and_packet_limits(self):
        data = capture()
        section = data[:28]
        invalid_option = block(1, struct.pack("<HHI", 1, 0, 65535) + struct.pack("<HH", 9, 2) + bytes(4))
        with self.assertRaises(AnalysisError):
            analyze_pcap(section + invalid_option)
        from unittest.mock import patch
        with patch("subterfuge.analysis.MAX_PACKETS", 0), self.assertRaises(AnalysisError):
            analyze_pcap(data)

    def test_truncation_and_bad_trailer(self):
        valid = capture()
        for data in (valid[:-1], valid[:20], valid[:28] + b"\x00", valid[:-4] + b"\x00" * 4):
            with self.subTest(length=len(data)), self.assertRaises(AnalysisError):
                analyze_pcap(data)

    def test_missing_interface(self):
        data = capture()
        section_length = struct.unpack_from("<I", data, 4)[0]
        interface_length = struct.unpack_from("<I", data, section_length + 4)[0]
        with self.assertRaises(AnalysisError):
            analyze_pcap(data[:section_length] + data[section_length + interface_length:])

    def test_non_arp_ignored(self):
        frame = sample_capture()[40:82]
        report = analyze_pcap(capture(frame=frame[:12] + b"\x08\x00" + frame[14:]))
        self.assertEqual(report["stats"]["ignored_packets"], 1)
        self.assertEqual(report["stats"]["hosts"], 0)


if __name__ == "__main__":
    unittest.main()