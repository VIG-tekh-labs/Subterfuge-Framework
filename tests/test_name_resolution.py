"""Offline NBNS query decoding and invalid-input checks."""
import struct
import unittest

from subterfuge.analysis import AnalysisError
from subterfuge.name_resolution import analyze_nbns_query


def query(name="WPAD"):
    raw = name.ljust(15).encode("ascii") + bytes([0])
    encoded = bytes(value for octet in raw for value in (65 + (octet >> 4), 65 + (octet & 15)))
    return struct.pack("!HHHHHH", 1234, 0, 1, 0, 0, 0) + bytes([32]) + encoded + bytes([0]) + struct.pack("!HH", 32, 1)


class NameResolutionTests(unittest.TestCase):
    def test_wpad_observation_without_active_response(self):
        report = analyze_nbns_query(query())
        self.assertEqual(report["stats"]["wpad_queries"], 1)
        self.assertEqual(report["queries"][0]["name"], "WPAD")
        self.assertEqual(report["findings"][0]["code"], "wpad_query_observed")

    def test_other_name_has_no_finding(self):
        report = analyze_nbns_query(query("PRINTER"))
        self.assertEqual(report["findings"], [])

    def test_malformed_and_response_rejected(self):
        packet = query()
        for data in (b"", packet[:-1], packet[:12] + bytes([31]) + packet[13:],
                     packet[:2] + bytes([128, 0]) + packet[4:],
                     packet[:13] + bytes([0]) + packet[14:]):
            with self.subTest(length=len(data)), self.assertRaises(AnalysisError):
                analyze_nbns_query(data)