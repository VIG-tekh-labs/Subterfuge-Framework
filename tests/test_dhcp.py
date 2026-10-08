"""Synthetic passive DHCPv4 evidence checks."""
import struct
import unittest

from subterfuge.analysis import AnalysisError
from subterfuge.dhcp import analyze_dhcp


def packet(options=b""):
    data = bytearray(240)
    data[0:4] = bytes([2, 1, 6, 0])
    struct.pack_into("!I", data, 4, 42)
    data[236:240] = bytes.fromhex("63825363")
    return bytes(data) + bytes([53, 1, 2]) + options + bytes([255])


class DhcpTests(unittest.TestCase):
    def test_offer_with_server_and_wpad_indicator(self):
        report = analyze_dhcp(packet(bytes([54, 4, 192, 0, 2, 1, 252, 3, 65, 66, 67])))
        self.assertEqual(report["observations"][0]["message_type"], "offer")
        self.assertEqual(report["observations"][0]["server_identifier"], "192.0.2.1")
        self.assertTrue(report["observations"][0]["wpad_option_present"])
        self.assertNotIn("ABC", str(report))

    def test_no_wpad(self):
        report = analyze_dhcp(packet())
        self.assertEqual(report["stats"]["wpad_options"], 0)

    def test_invalid_datagrams(self):
        valid = packet()
        for value in (b"", valid[:239], valid[:236] + bytes(4) + valid[240:],
                      valid[:-1] + bytes([54, 4, 1]),
                      bytes([9]) + valid[1:]):
            with self.subTest(length=len(value)), self.assertRaises(AnalysisError):
                analyze_dhcp(value)