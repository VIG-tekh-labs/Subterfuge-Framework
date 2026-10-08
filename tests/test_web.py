"""Real loopback HTTP checks; no external network traffic."""

from http.client import HTTPConnection
from pathlib import Path
import json
import re
import threading
import unittest

from subterfuge.demo import sample_capture
from subterfuge.web import MAX_UPLOAD, make_server


class DashboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = make_server(0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        status, _, page = cls.request("GET", "/")
        if status != 200:
            raise AssertionError("Dashboard did not start")
        cls.token = re.search(r"const token='([^']+)'", page.decode()).group(1)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    @classmethod
    def request(cls, method, path, body=None, headers=None):
        connection = HTTPConnection("127.0.0.1", cls.server.server_port, timeout=5)
        try:
            connection.request(method, path, body=body, headers=headers or {})
            response = connection.getresponse()
            return response.status, dict(response.getheaders()), response.read()
        finally:
            connection.close()

    def test_page_and_security_headers(self):
        status, headers, body = self.request("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn(b"Subterfuge", body)
        self.assertNotIn(b"__TOKEN__", body)
        self.assertEqual(headers["Cache-Control"], "no-store")
        self.assertIn(b"Inspect a TLS endpoint", body)
        self.assertIn(b'id="tls-inspect"', body)
        self.assertIn(b'id="load-report"', body)
        self.assertIn(b'validateImportedReport', body)
        self.assertIn("frame-ancestors 'none'", headers["Content-Security-Policy"])
        self.assertEqual(self.server.server_address[0], "127.0.0.1")

    def test_accessible_table_and_result_regions(self):
        status, _, page = self.request("GET", "/")
        self.assertEqual(status, 200)
        for label in (
            b'aria-label="Observed host inventory"',
            b'aria-label="Passive protocol observations"',
            b'aria-label="Audit findings"',
            b'aria-label="Import warnings"',
        ):
            with self.subTest(label=label):
                self.assertIn(label, page)

    def test_demo_and_doctor(self):
        status, _, body = self.request("GET", "/api/demo")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["stats"]["findings"], 1)
        self.assertEqual(self.request("GET", "/api/doctor")[0], 200)

    def test_unexpected_host_and_origin(self):
        for headers in [{"Host": "example.invalid"}, {"Origin": "https://example.invalid"}]:
            with self.subTest(headers=headers):
                self.assertEqual(self.request("GET", "/api/report", headers=headers)[0], 403)

    def test_missing_wrong_and_non_ascii_tokens(self):
        for token in [None, "incorrect", "é"]:
            headers = {} if token is None else {"X-Subterfuge-Token": token}
            with self.subTest(token=token):
                self.assertEqual(self.request("POST", "/api/analyze-pcap", sample_capture(), headers)[0], 403)

    def test_capture_upload_and_report(self):
        headers = {"X-Subterfuge-Token": self.token, "Origin": self.server.expected_origin}
        status, _, body = self.request("POST", "/api/analyze-pcap", sample_capture(), headers)
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["stats"]["findings"], 1)
        self.assertEqual(json.loads(self.request("GET", "/api/report")[2]), json.loads(body))

    def test_tls_endpoint_post_and_report(self):
        from unittest.mock import patch
        report = {"kind": "tls", "hosts": [], "findings": [], "warnings": [],
                  "source": "example.test", "stats": {"findings": 0},
                  "tls": {"host": "example.test", "port": 443,
                          "certificate_verified": True,
                          "negotiated_version": "TLSv1.3"}}
        headers = {"X-Subterfuge-Token": self.token, "Content-Type": "application/json"}
        with patch("subterfuge.tls.inspect_tls", return_value=report) as inspect:
            status, _, body = self.request(
                "POST", "/api/inspect-tls",
                json.dumps({"host": "example.test", "port": 443, "timeout": 10}).encode(), headers,
            )
        self.assertEqual(status, 200)
        inspect.assert_called_once_with("example.test", 443, 10)
        self.assertEqual(json.loads(body)["kind"], "tls")
        self.assertEqual(json.loads(self.request("GET", "/api/report")[2])["kind"], "tls")

    def test_tls_post_rejects_bad_requests(self):
        from unittest.mock import patch
        headers = {"X-Subterfuge-Token": self.token, "Content-Type": "application/json"}
        for data in (b"{bad", b"null", b"[]", b'{"host":123}', b'{"host":"example.test","timeout":"slow"}', b'{"host":"example.test","port":true}'):
            with self.subTest(data=data):
                self.assertEqual(self.request("POST", "/api/inspect-tls", data, headers)[0], 400)
        self.assertEqual(self.request("POST", "/api/inspect-tls", b"{}", {"X-Subterfuge-Token": self.token})[0], 415)
        self.assertEqual(self.request("POST", "/api/inspect-tls", b"x" * 4097, headers)[0], 413)
        self.assertEqual(
            self.request("POST", "/api/inspect-tls", b'{"host":"https://example.test"}', headers)[0],
            400,
        )
        from subterfuge.web import _tls_request
        from subterfuge.analysis import AnalysisError
        with patch("subterfuge.tls.socket.create_connection") as connection, self.assertRaises(AnalysisError):
            _tls_request(b'{"host":"https://example.test"}')
        connection.assert_not_called()

    def test_pcapng_upload_and_ui_copy(self):
        from test_pcapng import capture
        status, _, body = self.request("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn(b".pcapng", body)
        status, _, body = self.request(
            "POST", "/api/analyze-pcap", capture(),
            {"X-Subterfuge-Token": self.token},
        )
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["kind"], "pcapng")

    def test_pcapng_simple_packet_api_preserves_unknown_timestamps(self):
        from test_pcapng_packet_blocks import section_and_interface, simple_packet
        from subterfuge.demo import sample_capture
        payload = section_and_interface() + simple_packet(sample_capture()[40:82])
        status, _, body = self.request(
            "POST", "/api/analyze-pcap", payload,
            {"X-Subterfuge-Token": self.token},
        )
        self.assertEqual(status, 200)
        report = json.loads(body)
        self.assertEqual(report["stats"]["arp_packets"], 1)
        self.assertIsNone(report["hosts"][0]["first_seen"])
        self.assertIsNone(report["hosts"][0]["last_seen"])
        self.assertTrue(any("lack timestamps" in item for item in report["warnings"]))

    def test_dhcp_pcap_report_and_passive_panel(self):
        from test_capture_evidence import pcap
        from test_udp_evidence import frame
        from test_dhcp import packet
        status, _, page = self.request("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn(b"Passive DHCP &amp; NetBIOS evidence", page)
        payload = pcap(frame(packet(), 67, 68))
        status, _, body = self.request("POST", "/api/analyze-pcap", payload,
                                      {"X-Subterfuge-Token": self.token})
        self.assertEqual(status, 200)
        report = json.loads(body)
        self.assertEqual(report["stats"]["dhcp_messages"], 1)
        self.assertEqual(report["network_evidence"][0]["protocol"], "dhcp")

    def test_standard_xml_upload(self):
        data = (Path(__file__).parent / "fixtures/nmap_inventory.xml").read_bytes()
        status, _, body = self.request("POST", "/api/import-nmap", data, {"X-Subterfuge-Token": self.token})
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["stats"]["open_ports"], 2)

    def test_invalid_upload_and_length(self):
        headers = {"X-Subterfuge-Token": self.token}
        self.assertEqual(self.request("POST", "/api/import-nmap", b"invalid", headers)[0], 400)
        for length, expected in [("invalid", 411), ("0", 413), (str(MAX_UPLOAD + 1), 413)]:
            with self.subTest(length=length):
                self.assertEqual(self.request("POST", "/api/import-nmap", b"", {**headers, "Content-Length": length})[0], expected)

    def test_chunked_upload_rejected(self):
        self.assertEqual(self.request("POST", "/api/import-nmap", b"", {"X-Subterfuge-Token": self.token, "Transfer-Encoding": "chunked"})[0], 400)

    def test_unknown_endpoint(self):
        self.assertEqual(self.request("GET", "/unknown")[0], 404)


if __name__ == "__main__":
    unittest.main()