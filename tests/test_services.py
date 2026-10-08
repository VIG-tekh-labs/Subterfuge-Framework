"""Explicit bounded Nmap service inventory with synthetic subprocesses only."""
import io
import json
from pathlib import Path
from subprocess import CompletedProcess, TimeoutExpired
from unittest.mock import patch
import contextlib
import unittest

from subterfuge.analysis import AnalysisError
from subterfuge.cli import main
from subterfuge.environment import scan_services

XML = (Path(__file__).parent / "fixtures/nmap_inventory.xml").read_bytes()


class ServiceScanTests(unittest.TestCase):
    def test_invalid_targets_ports_and_timeouts_do_not_start_process(self):
        invalid = [
            ("example.invalid", "22", 60), ("192.0.2.0/24", "22", 60),
            ("192.0.2.1;echo", "22", 60), ("192.0.2.1", "0", 60),
            ("192.0.2.1", "65536", 60), ("192.0.2.1", "22,22", 60),
            ("192.0.2.1", "22,-1", 60),
            ("192.0.2.1", ",".join(str(i) for i in range(1, 34)), 60),
            ("192.0.2.1", "22", float("nan")),
            ("192.0.2.1", "22", 301),
        ]
        with patch("subterfuge.environment.subprocess.run") as run:
            for target, ports, timeout in invalid:
                with self.subTest(target=target, ports=ports, timeout=timeout), self.assertRaises(AnalysisError):
                    scan_services(target, ports, timeout)
            run.assert_not_called()

    def test_missing_optional_nmap(self):
        with patch("subterfuge.environment.shutil.which", return_value=None), self.assertRaisesRegex(AnalysisError, "Nmap is not installed"):
            scan_services("192.0.2.10")

    def test_explicit_ipv4_scan_safely_parses_xml(self):
        with patch("subterfuge.environment.shutil.which", return_value="/synthetic/nmap"), patch(
            "subterfuge.environment.subprocess.run",
            return_value=CompletedProcess([], 0, XML, b""),
        ) as run:
            report = scan_services("192.0.2.10", "22,80,443", 30)
            self.assertEqual(report["kind"], "service_scan")
            self.assertEqual(report["scan"]["ports"], [22, 80, 443])
            self.assertEqual(report["stats"]["hosts"], 2)
            command = run.call_args.args[0]
            self.assertEqual(command[-1], "192.0.2.10")
            self.assertIn("-sT", command)
            self.assertIn("-Pn", command)
            self.assertNotIn("-sS", command)
            self.assertEqual(run.call_args.kwargs["timeout"], 30)

    def test_ipv6_uses_explicit_ipv6_mode(self):
        with patch("subterfuge.environment.shutil.which", return_value="/synthetic/nmap"), patch(
            "subterfuge.environment.subprocess.run",
            return_value=CompletedProcess([], 0, XML, b""),
        ) as run:
            scan_services("2001:db8::20")
            self.assertIn("-6", run.call_args.args[0])

    def test_cli_dispatch_and_failure_paths(self):
        with patch("subterfuge.cli.scan_services", return_value={"kind":"service_scan"}) as scan:
            out=io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(main(["scan-services","--target","192.0.2.10","--ports","443"]), 0)
            self.assertEqual(json.loads(out.getvalue())["kind"], "service_scan")
            scan.assert_called_once_with("192.0.2.10","443",120)
        with patch("subterfuge.environment.shutil.which", return_value="/synthetic/nmap"):
            with patch("subterfuge.environment.subprocess.run", return_value=CompletedProcess([], 1, b"", b"synthetic failure")), self.assertRaisesRegex(AnalysisError,"synthetic failure"):
                scan_services("192.0.2.10")
            with patch("subterfuge.environment.subprocess.run", side_effect=TimeoutExpired("nmap", 1)), self.assertRaisesRegex(AnalysisError,"timed out"):
                scan_services("192.0.2.10")


if __name__=="__main__":
    unittest.main()