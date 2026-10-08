"""Live adapter contracts are tested using synthetic packets, without sniffing."""
import contextlib
import io
import json
import sys
import types
import unittest
from unittest.mock import patch

from subterfuge.analysis import AnalysisError
from subterfuge.cli import main
from subterfuge.environment import capture_protocols
from test_dhcp import packet as dhcp_packet
from test_name_resolution import query


class LiveCaptureTests(unittest.TestCase):
    def test_invalid_duration_limit_interface(self):
        with patch("subterfuge.environment.interfaces", return_value=[]):
            for duration, limit in ((0, 10), (601, 10), (1, 0), (1, 250001)):
                with self.assertRaises(AnalysisError):
                    capture_protocols("test0", duration, limit)
            with self.assertRaisesRegex(AnalysisError, "Unknown network interface"):
                capture_protocols("test0", 1, 10)

    def test_synthetic_arp_dhcp_nbns_in_one_passive_capture(self):
        class ARP: pass
        class IP: pass
        class UDP: pass

        def fake_packet(layers):
            class Fake:
                time = 1700000000.0
                def haslayer(self, kind): return kind in layers
                def __getitem__(self, kind): return layers[kind]
            return Fake()

        arp = fake_packet({ARP: types.SimpleNamespace(psrc="192.0.2.1", hwsrc="02:00:00:00:00:01", op=2)})
        ip = types.SimpleNamespace(frag=0, flags=0)
        dhcp = fake_packet({IP: ip, UDP: types.SimpleNamespace(sport=67,dport=68,payload=dhcp_packet())})
        nbns = fake_packet({IP: ip, UDP: types.SimpleNamespace(sport=137,dport=137,payload=query())})
        packets = [arp, dhcp, nbns]

        module = types.ModuleType("scapy.all")
        module.ARP, module.IP, module.UDP = ARP, IP, UDP

        def sniff(**kwargs):
            self.assertEqual(kwargs["iface"], "test0")
            self.assertFalse(kwargs["store"])
            for item in packets:
                if kwargs["lfilter"](item):
                    kwargs["prn"](item)

        module.sniff = sniff
        package = types.ModuleType("scapy")
        package.all = module

        with patch("subterfuge.environment.interfaces", return_value=[{"name":"test0"}]), patch.dict(
            sys.modules, {"scapy": package, "scapy.all": module}
        ):
            report = capture_protocols("test0", duration=1, limit=3)
        self.assertEqual(report["kind"], "live_passive")
        self.assertEqual(report["stats"]["arp_packets"], 1)
        self.assertEqual(report["stats"]["dhcp_messages"], 1)
        self.assertEqual(report["stats"]["nbns_queries"], 1)
        self.assertEqual(report["stats"]["wpad_nbns_queries"], 1)
        self.assertTrue(report["capture"]["passive_only"])

    def test_cli_dispatch_is_explicit(self):
        output=io.StringIO()
        with patch("subterfuge.cli.capture_protocols",return_value={"kind":"live_passive"}) as capture:
            with contextlib.redirect_stdout(output):
                self.assertEqual(main(["capture-protocols","--interface","test0"]),0)
            capture.assert_called_once_with("test0",30,10_000)
        self.assertEqual(json.loads(output.getvalue())["kind"], "live_passive")


if __name__=="__main__":
    unittest.main()