"""Optional adapter contracts, using synthetic subprocess output."""

from pathlib import Path
from subprocess import CompletedProcess, TimeoutExpired
import unittest
from unittest.mock import patch

from subterfuge.analysis import AnalysisError
from subterfuge.environment import capture, discover, doctor, interfaces

XML = (Path(__file__).parent / "fixtures/nmap_inventory.xml").read_bytes()


class DiscoveryTests(unittest.TestCase):
    def test_explicit_bounded_targets_only(self):
        for target in ["example.invalid", "192.0.2.0/16", "192.0.2.1;echo test"]:
            with self.subTest(target=target), self.assertRaises(AnalysisError):
                discover(target)

    def test_invalid_timeouts(self):
        for timeout in [0, -1, 301, float("nan")]:
            with self.subTest(timeout=timeout), self.assertRaises(AnalysisError):
                discover("192.0.2.10", timeout)

    def test_optional_nmap_unavailable(self):
        with patch("subterfuge.environment.shutil.which", return_value=None), self.assertRaises(AnalysisError):
            discover("192.0.2.10")

    def test_ipv4_discovery_parses_standard_output(self):
        with patch("subterfuge.environment.shutil.which", return_value="/synthetic/nmap"), patch("subterfuge.environment.subprocess.run", return_value=CompletedProcess([], 0, XML, b"")) as run:
            report = discover("192.0.2.10")
            self.assertEqual(report["kind"], "discovery")
            self.assertEqual(report["stats"]["hosts"], 2)
            self.assertEqual(run.call_args.args[0], ["/synthetic/nmap", "-sn", "-oX", "-", "192.0.2.10/32"])
            self.assertNotIn("shell", run.call_args.kwargs)

    def test_ipv6_adapter(self):
        with patch("subterfuge.environment.shutil.which", return_value="/synthetic/nmap"), patch("subterfuge.environment.subprocess.run", return_value=CompletedProcess([], 0, XML, b"")) as run:
            discover("2001:db8::10")
            self.assertIn("-6", run.call_args.args[0])

    def test_nmap_failures_are_reported(self):
        with patch("subterfuge.environment.shutil.which", return_value="/synthetic/nmap"):
            with patch("subterfuge.environment.subprocess.run", return_value=CompletedProcess([], 1, b"", b"synthetic failure")), self.assertRaisesRegex(AnalysisError, "synthetic failure"):
                discover("192.0.2.10")
            with patch("subterfuge.environment.subprocess.run", side_effect=TimeoutExpired("nmap", 1)), self.assertRaisesRegex(AnalysisError, "timed out"):
                discover("192.0.2.10")


class CaptureBoundaryTests(unittest.TestCase):
    def test_duration_and_packet_bounds(self):
        for duration, limit in [(0, 10), (float("nan"), 10), (601, 10), (1, 0), (1, 250001)]:
            with self.subTest(duration=duration, limit=limit), self.assertRaises(AnalysisError):
                capture("synthetic", duration, limit)

    def test_unknown_interface(self):
        with patch("subterfuge.environment.interfaces", return_value=[]), self.assertRaisesRegex(AnalysisError, "Unknown network interface"):
            capture("synthetic")

    def test_restricted_interface_enumeration_keeps_offline_runtime_usable(self):
        with patch("subterfuge.environment.socket.if_nameindex", side_effect=PermissionError), patch("subterfuge.environment.Path.iterdir", return_value=[]), patch("subterfuge.environment.shutil.which", return_value=None):
            self.assertEqual(interfaces(), [])
            self.assertTrue(doctor()["offline_analysis"])


if __name__ == "__main__":
    unittest.main()
