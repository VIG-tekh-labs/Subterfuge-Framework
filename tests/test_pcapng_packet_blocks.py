"""Regression tests for PCAPNG simple/obsolete blocks and interface clocks."""
import struct
import unittest

from subterfuge.analysis import AnalysisError, analyze_pcap
from subterfuge.demo import sample_capture
from test_dhcp import packet as dhcp_payload
from test_pcapng import block, capture
from test_udp_evidence import frame as udp_frame


def section_and_interface(endian="<", options=b""):
    section = capture(endian)[:28]
    interface = block(1, struct.pack(endian + "HHI", 1, 0, 65535) + options, endian)
    return section + interface


def simple_packet(frame, endian="<"):
    return block(3, struct.pack(endian + "I", len(frame)) + frame + bytes(-len(frame) % 4), endian)


def obsolete_packet(frame, endian="<"):
    header = struct.pack(endian + "HHIIII", 0, 0, 0, 1_700_000_000, len(frame), len(frame))
    return block(2, header + frame + bytes(-len(frame) % 4), endian)


class PcapngPacketBlockTests(unittest.TestCase):
    def test_simple_packet_records_arp_without_inventing_timestamp(self):
        frame = sample_capture()[40:82]
        for endian in ("<", ">"):
            with self.subTest(endian=endian):
                report = analyze_pcap(section_and_interface(endian) + simple_packet(frame, endian))
                self.assertEqual(report["stats"]["arp_packets"], 1)
                self.assertEqual(report["stats"]["packets"], 1)
                self.assertEqual(report["hosts"][0]["first_seen"], None)
                self.assertEqual(report["hosts"][0]["last_seen"], None)
                self.assertEqual(report["capture"]["untimed_packets"], 1)
                self.assertTrue(any("lack timestamps" in item for item in report["warnings"]))

    def test_mixed_timed_and_untimed_host_keeps_known_time(self):
        frame = sample_capture()[40:82]
        report = analyze_pcap(capture() + simple_packet(frame))
        self.assertEqual(report["stats"]["packets"], 2)
        self.assertEqual(report["stats"]["arp_packets"], 2)
        self.assertEqual(report["hosts"][0]["observations"], 2)
        self.assertIsNotNone(report["hosts"][0]["first_seen"])
        self.assertEqual(report["hosts"][0]["first_seen"], report["hosts"][0]["last_seen"])

    def test_simple_packet_passive_dhcp(self):
        frame = udp_frame(dhcp_payload(), 67, 68)
        report = analyze_pcap(section_and_interface() + simple_packet(frame))
        self.assertEqual(report["stats"]["dhcp_messages"], 1)
        self.assertEqual(report["stats"]["ignored_packets"], 0)

    def test_obsolete_packet_blocks_compatible(self):
        frame = sample_capture()[40:82]
        for endian in ("<", ">"):
            with self.subTest(endian=endian):
                report = analyze_pcap(section_and_interface(endian) + obsolete_packet(frame, endian))
                self.assertEqual(report["stats"]["arp_packets"], 1)
                self.assertEqual(report["capture"]["untimed_packets"], 0)
                self.assertIsNotNone(report["hosts"][0]["first_seen"])

    def test_tsoffset_adjusts_packet_timestamp(self):
        frame = sample_capture()[40:82]
        for endian in ("<", ">"):
            with self.subTest(endian=endian):
                offset_option = struct.pack(endian + "HHq", 14, 8, -100)
                epb = block(
                    6, struct.pack(endian + "IIIII", 0, 0, 1_700_000_000, len(frame), len(frame))
                    + frame + bytes(-len(frame) % 4), endian,
                )
                report = analyze_pcap(section_and_interface(endian, offset_option) + epb)
                self.assertAlmostEqual(report["hosts"][0]["first_seen"], 1600.0)

    def test_excessive_unknown_blocks_are_bounded(self):
        from unittest.mock import patch
        unknown_metadata = block(0x12345678, b"")
        with patch("subterfuge.analysis.MAX_PCAPNG_BLOCKS", 3):
            with self.assertRaisesRegex(AnalysisError, "block limit exceeded"):
                analyze_pcap(capture() + unknown_metadata)

    def test_invalid_tsoffset_option_and_missing_interface(self):
        bad_option = struct.pack("<HHI", 14, 4, 42)
        with self.assertRaises(AnalysisError):
            analyze_pcap(section_and_interface(options=bad_option))
        section_only = capture()[:28]
        with self.assertRaises(AnalysisError):
            analyze_pcap(section_only + simple_packet(sample_capture()[40:82]))

    def test_simple_packet_invalid_size(self):
        frame = sample_capture()[40:82]
        valid = section_and_interface() + simple_packet(frame)
        with self.assertRaises(AnalysisError):
            analyze_pcap(valid[:-4] + bytes(4) + valid[-4:])


if __name__ == "__main__":
    unittest.main()