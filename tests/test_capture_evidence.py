"""PCAP/PCAPNG end-to-end passive DHCP and NBNS capture regressions."""
import json
import struct
import unittest
from unittest.mock import patch

from subterfuge.analysis import AnalysisError, analyze_pcap
from subterfuge.demo import sample_capture
from test_dhcp import packet
from test_name_resolution import query
from test_pcapng import capture as pcapng
from test_udp_evidence import frame


def pcap(*frames, linktype=1):
    header = struct.pack("<IHHiiII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, linktype)
    return header + b"".join(
        struct.pack("<IIII", 1700000000 + i, 0, len(payload), len(payload)) + payload
        for i, payload in enumerate(frames)
    )


class PassiveCaptureTests(unittest.TestCase):
    def test_combined_classic_pcap_evidence(self):
        dhcp = frame(packet(bytes([252, 4]) + b"test"), 67, 68)
        nbns = frame(query("WPAD"), 137, 137)
        non_arp = frame(b"unrelated", 8000, 8001)
        report = analyze_pcap(pcap(dhcp, nbns, dhcp, non_arp), "synthetic.pcap")
        self.assertEqual(report["stats"]["packets"], 4)
        self.assertEqual(report["stats"]["arp_packets"], 0)
        self.assertEqual(report["stats"]["dhcp_messages"], 2)
        self.assertEqual(report["stats"]["nbns_queries"], 1)
        self.assertEqual(report["stats"]["ignored_packets"], 1)
        self.assertEqual(report["stats"]["wpad_dhcp_options"], 2)
        self.assertEqual(report["stats"]["wpad_nbns_queries"], 1)
        self.assertEqual(len(report["network_evidence"]), 2)
        self.assertEqual(len(report["findings"]), 2)
        self.assertNotIn("test", json.dumps(report))  # DHCP option bytes must be discarded

    def test_mixed_arp_and_name_query(self):
        raw_arp = sample_capture()[40:82]
        report = analyze_pcap(pcap(raw_arp, frame(query("PRINTER"), 137, 137)))
        self.assertEqual(report["stats"]["arp_packets"], 1)
        self.assertEqual(report["stats"]["nbns_queries"], 1)
        self.assertEqual(report["stats"]["findings"], 0)

    def test_pcapng_evidence(self):
        result = analyze_pcap(pcapng(frame=frame(packet(), 67, 68)))
        self.assertEqual(result["kind"], "pcapng")
        self.assertEqual(result["stats"]["dhcp_messages"], 1)

    def test_linux_cooked_v1_v2(self):
        ethernet = frame(packet(), 67, 68)
        for linktype, cooked in (
            (113, bytes(14) + bytes.fromhex("0800") + ethernet[14:]),
            (276, bytes.fromhex("0800") + bytes(18) + ethernet[14:]),
        ):
            with self.subTest(linktype=linktype):
                self.assertEqual(
                    analyze_pcap(pcap(cooked, linktype=linktype))["stats"]["dhcp_messages"],
                    1,
                )

    def test_vlan_evidence(self):
        ethernet = frame(query(), 137, 137)
        vlan = ethernet[:12] + bytes.fromhex("810000010800") + ethernet[14:]
        self.assertEqual(analyze_pcap(pcap(vlan))["stats"]["wpad_nbns_queries"], 1)

    def test_bounded_distinct_groups(self):
        with patch("subterfuge.udp_evidence.MAX_EVIDENCE_GROUPS", 1):
            with self.assertRaises(AnalysisError):
                analyze_pcap(pcap(frame(query("ALPHA"), 137, 137), frame(query("BETA"), 137, 137)))


if __name__ == "__main__":
    unittest.main()