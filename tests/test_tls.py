"""TLS verification, evidence and CLI regressions without external traffic."""

import contextlib
import io
import json
import ssl
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

from subterfuge.analysis import AnalysisError, analyze_nmap
from subterfuge.cli import main
from subterfuge.tls import inspect_tls


class TLSTests(unittest.TestCase):
    def test_invalid_parameters_before_connect(self):
        for host, port, timeout in [("https://example.test", 443, 10), ("", 443, 10), ("x", 0, 10), ("x", 443, float("nan"))]:
            with patch("subterfuge.tls.socket.create_connection") as connect:
                with self.assertRaises(AnalysisError):
                    inspect_tls(host, port, timeout)
                connect.assert_not_called()

    def test_validated_negotiation_and_expiring_certificate(self):
        secured = MagicMock()
        secured.getpeercert.return_value = {"notAfter": (datetime.now(timezone.utc) + timedelta(days=5)).strftime("%b %d %H:%M:%S %Y GMT")}
        secured.version.return_value = "TLSv1.3"
        secured.cipher.return_value = ("TLS_AES_256_GCM_SHA384", "TLSv1.3", 256)
        context = ssl.create_default_context()
        self.assertTrue(context.check_hostname)
        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
        with patch("subterfuge.tls.ssl.create_default_context", return_value=context), patch.object(context, "wrap_socket") as wrap, patch("subterfuge.tls.socket.create_connection"):
            wrap.return_value.__enter__.return_value = secured
            report = inspect_tls("example.test")
            self.assertEqual(context.minimum_version, ssl.TLSVersion.TLSv1_2)
            self.assertEqual(wrap.call_args.kwargs["server_hostname"], "example.test")
        self.assertTrue(report["tls"]["certificate_verified"])
        self.assertEqual(report["tls"]["negotiated_version"], "TLSv1.3")
        self.assertEqual(report["findings"][0]["code"], "tls_certificate_expiring")

    def test_invalid_certificate_reported_without_unverified_retry(self):
        error = ssl.SSLCertVerificationError("invalid certificate")
        error.verify_message = "hostname mismatch"
        with patch("subterfuge.tls.socket.create_connection", side_effect=error) as connect:
            report = inspect_tls("example.test")
            self.assertEqual(connect.call_count, 1)
        self.assertFalse(report["tls"]["certificate_verified"])
        self.assertEqual(report["findings"][0]["interpretation"], "hostname mismatch")

    def test_connection_errors_become_cli_errors(self):
        with patch("subterfuge.tls.socket.create_connection", side_effect=TimeoutError("timed out")), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["inspect-tls", "--host", "example.test"]), 2)

    def test_cli_json(self):
        output = io.StringIO()
        with patch("subterfuge.tls.inspect_tls", return_value={"kind": "tls"}) as inspect, contextlib.redirect_stdout(output):
            self.assertEqual(main(["inspect-tls", "--host", "example.test", "--port", "8443"]), 0)
        inspect.assert_called_once_with("example.test", 8443, 10)
        self.assertEqual(json.loads(output.getvalue())["kind"], "tls")


class ServiceEvidenceTests(unittest.TestCase):
    def test_inventory_metadata_and_transport_review(self):
        xml = b'<nmaprun><host><address addr="2001:db8::1" addrtype="ipv6"/><ports><port portid="80" protocol="tcp"><state state="open"/><service name="http" product="Example" version="1.0"/></port><port portid="443" protocol="tcp"><state state="open"/><service name="http" tunnel="ssl"/></port><port portid="21" protocol="tcp"><state state="closed"/><service name="ftp"/></port></ports><os><osmatch name="Example OS" accuracy="95"/></os></host></nmaprun>'
        report = analyze_nmap(xml)
        self.assertEqual(report["stats"]["findings"], 1)
        self.assertEqual(report["findings"][0]["address"], "2001:db8::1")
        self.assertEqual(report["hosts"][0]["ports"][0]["version"], "1.0")
        self.assertEqual(report["hosts"][0]["operating_systems"][0]["name"], "Example OS")

