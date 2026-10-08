"""Offline frame evidence integration tests."""
import struct
import unittest

from subterfuge.udp_evidence import inspect_ethernet_udp
from test_dhcp import packet
from test_name_resolution import query


def frame(payload, sport, dport):
    udp = struct.pack("!HHHH", sport, dport, len(payload) + 8, 0) + payload
    ip = bytearray(20)
    ip[0] = 0x45
    ip[9] = 17
    struct.pack_into("!H", ip, 2, len(ip) + len(udp))
    return bytes(12) + bytes.fromhex("0800") + bytes(ip) + udp


class UdpEvidenceTests(unittest.TestCase):
    def test_dhcp_frame(self):
        result = inspect_ethernet_udp(frame(packet(), 67, 68))
        self.assertEqual(result["kind"], "dhcp")

    def test_nbns_frame(self):
        result = inspect_ethernet_udp(frame(query(), 137, 137))
        self.assertEqual(result["stats"]["wpad_queries"], 1)

    def test_non_udp_and_fragment_rejected(self):
        data = bytearray(frame(packet(), 67, 68))
        self.assertIsNone(inspect_ethernet_udp(bytes(data[:15])))
        data[14 + 9] = 6
        self.assertIsNone(inspect_ethernet_udp(bytes(data)))
        data[14 + 9] = 17
        data[14 + 6] = 0x20
        self.assertIsNone(inspect_ethernet_udp(bytes(data)))