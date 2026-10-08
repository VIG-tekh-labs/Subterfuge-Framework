"""Offline format, input-boundary and report-export regressions."""

from pathlib import Path
import json
import os
import struct
import tempfile
import unittest
from unittest.mock import patch

from subterfuge.analysis import AnalysisError, ArpTracker, analyze_nmap, analyze_pcap, write_report
from subterfuge.demo import sample_capture

FIXTURE = Path(__file__).parent / "fixtures/nmap_inventory.xml"


class NmapTests(unittest.TestCase):
    def test_standard_doctype_inventory(self):
        report = analyze_nmap(FIXTURE.read_bytes())
        self.assertEqual(report["stats"]["hosts"], 2)
        self.assertEqual(report["stats"]["open_ports"], 2)
        self.assertEqual(report["hosts"][0]["addresses"], ["192.0.2.10"])
        self.assertEqual(report["hosts"][1]["addresses"], ["2001:db8::20"])
        self.assertEqual(report["hosts"][0]["hostnames"], ["café.example"])

    def test_utf8_bom(self):
        self.assertEqual(analyze_nmap(b"\xef\xbb\xbf" + FIXTURE.read_bytes())["stats"]["hosts"], 2)

    def test_document_without_doctype(self):
        self.assertEqual(analyze_nmap(b"<nmaprun/>")["hosts"], [])

    def test_dtd_resources_and_entities_rejected(self):
        for declaration in [
            '<!DOCTYPE nmaprun SYSTEM "file:///unused">',
            '<!DOCTYPE nmaprun PUBLIC "unused" "https://example.invalid/dtd">',
            '<!DOCTYPE nmaprun [<!ENTITY value "example">]>',
            '<!DOCTYPE nmaprun [<!ENTITY % external SYSTEM "file:///unused">%external;]>',
            '<!DOCTYPE another>',
        ]:
            with self.subTest(declaration=declaration), self.assertRaises(AnalysisError):
                analyze_nmap((declaration + "<nmaprun/>").encode())

    def test_unsupported_encodings(self):
        for data in ["<nmaprun/>".encode("utf-16"), b'<?xml version="1.0" encoding="ISO-8859-1"?><nmaprun/>', b"<nmaprun>\xff</nmaprun>"]:
            with self.subTest(data=data), self.assertRaises(AnalysisError):
                analyze_nmap(data)

    def test_invalid_xml_and_wrong_root(self):
        for data in [b"", b"<nmaprun>", b"<other/>", b'<?xml version="1.1"?><nmaprun/>']:
            with self.subTest(data=data), self.assertRaises(AnalysisError):
                analyze_nmap(data)

    def test_invalid_address(self):
        with self.assertRaises(AnalysisError):
            analyze_nmap(b'<nmaprun><host><address addr="invalid" addrtype="ipv4"/></host></nmaprun>')

    def test_invalid_ports(self):
        for port in ["invalid", "-1", "65536"]:
            with self.subTest(port=port), self.assertRaises(AnalysisError):
                analyze_nmap(f'<nmaprun><host><ports><port portid="{port}"/></ports></host></nmaprun>'.encode())

    def test_nested_xml_limit(self):
        with self.assertRaises(AnalysisError):
            analyze_nmap(b"<nmaprun>" + b"<x>" * 64 + b"</x>" * 64 + b"</nmaprun>")

    def test_element_and_host_limits(self):
        with patch("subterfuge.analysis.MAX_XML_ELEMENTS", 1), self.assertRaises(AnalysisError):
            analyze_nmap(FIXTURE.read_bytes())
        with patch("subterfuge.analysis.MAX_HOSTS", 1), self.assertRaises(AnalysisError):
            analyze_nmap(FIXTURE.read_bytes())


class CaptureTests(unittest.TestCase):
    @staticmethod
    def capture(frame, endian="<", nano=False, linktype=1):
        magic = 0xA1B23C4D if nano else 0xA1B2C3D4
        return struct.pack(endian + "IHHiiII", magic, 2, 4, 0, 0, 65535, linktype) + struct.pack(endian + "IIII", 1700000000, 1, len(frame), len(frame)) + frame

    def test_synthetic_conflict(self):
        report = analyze_pcap(sample_capture())
        self.assertEqual(report["stats"]["arp_packets"], 2)
        self.assertEqual(report["stats"]["findings"], 1)
        self.assertEqual(report["findings"][0]["address"], "192.0.2.10")

    def test_all_classic_pcap_byte_orders_and_resolutions(self):
        frame = sample_capture()[40:82]
        for endian in ["<", ">"]:
            for nano in [False, True]:
                with self.subTest(endian=endian, nano=nano):
                    self.assertEqual(analyze_pcap(self.capture(frame, endian, nano))["stats"]["arp_packets"], 1)

    def test_vlan_and_linux_cooked_link_types(self):
        frame = sample_capture()[40:82]
        variants = [(1, frame[:12] + b"\x81\x00\x00\x01" + frame[12:]), (113, b"\x00" * 14 + b"\x08\x06" + frame[14:]), (276, b"\x08\x06" + b"\x00" * 18 + frame[14:])]
        for linktype, packet in variants:
            with self.subTest(linktype=linktype):
                self.assertEqual(analyze_pcap(self.capture(packet, linktype=linktype))["stats"]["arp_packets"], 1)

    def test_truncated_and_unknown_captures(self):
        for data in [b"", sample_capture()[:30], sample_capture()[:-1], b"\x0a\x0d\x0d\x0a" + b"\x00" * 24]:
            with self.subTest(length=len(data)), self.assertRaises(AnalysisError):
                analyze_pcap(data)

    def test_invalid_packet_timestamp(self):
        data = bytearray(sample_capture())
        struct.pack_into("<I", data, 28, 1_000_000)
        with self.assertRaises(AnalysisError):
            analyze_pcap(bytes(data))

    def test_non_arp_frames_are_not_hosts(self):
        frame = sample_capture()[40:82]
        report = analyze_pcap(self.capture(frame[:12] + b"\x08\x00" + frame[14:]))
        self.assertEqual(report["stats"]["hosts"], 0)
        self.assertEqual(report["stats"]["ignored_packets"], 1)

    def test_one_conflict_per_address_with_all_claims(self):
        tracker = ArpTracker("synthetic")
        for last in range(1, 4):
            tracker.observe("192.0.2.10", f"02:00:00:00:00:{last:02x}", 2, float(last))
        report = tracker.finish(3)
        self.assertEqual(len(report["findings"]), 1)
        self.assertEqual(len(report["findings"][0]["mac_addresses"]), 3)

    def test_claim_limits_and_non_finite_timestamps(self):
        tracker = ArpTracker("synthetic")
        with patch("subterfuge.analysis.MAX_MACS_PER_HOST", 1):
            tracker.observe("192.0.2.10", "02:00:00:00:00:01", 2, 1.0)
            with self.assertRaises(AnalysisError):
                tracker.observe("192.0.2.10", "02:00:00:00:00:02", 2, 2.0)
        with self.assertRaises(AnalysisError):
            tracker.observe("192.0.2.10", "02:00:00:00:00:01", 2, float("nan"))


class ExportTests(unittest.TestCase):
    def test_private_report_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "report.json"
            report = analyze_pcap(sample_capture())
            write_report(report, path)
            self.assertEqual(json.loads(path.read_text()), report)
            if os.name == "posix":
                self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_failed_export_keeps_previous_report(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "report.json"
            path.write_text("previous")
            with self.assertRaises(ValueError):
                write_report({"invalid": float("nan")}, path)
            self.assertEqual(path.read_text(), "previous")
            self.assertEqual(list(Path(folder).iterdir()), [path])


if __name__ == "__main__":
    unittest.main()
