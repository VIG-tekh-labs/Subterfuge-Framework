"""Web UI remote origin support without weakening the loopback binding."""
from http.client import HTTPConnection
import re
import threading
import unittest

from subterfuge.analysis import AnalysisError
from subterfuge.demo import sample_capture
from subterfuge.web import make_server, validate_public_origin


class ServerAccessTests(unittest.TestCase):
    def test_origin_validation_requires_explicit_https_address_and_port(self):
        self.assertEqual(
            validate_public_origin("https://192.0.2.10:8443"),
            "https://192.0.2.10:8443",
        )
        self.assertEqual(
            validate_public_origin("https://Audit.Example.Net:8443/"),
            "https://audit.example.net:8443",
        )
        self.assertIsNone(validate_public_origin(None))
        for candidate in (
            "", "http://192.0.2.10:8443", "https://example.net",
            "https://example.net:0", "https://example.net:65536",
            "https://user:secret@example.net:8443",
            "https://example.net:8443/unsafe", "https://example.net:8443?x=1",
            "https://example.net:8443#fragment",
            "https://example.net:8443\n",
        ):
            with self.subTest(origin=candidate), self.assertRaises(AnalysisError):
                validate_public_origin(candidate)

    @staticmethod
    def _request(server, path: str, *, method="GET", headers=None, body=None):
        connection = HTTPConnection("127.0.0.1", server.server_port, timeout=6)
        try:
            connection.request(method, path, body=body, headers=headers or {})
            response = connection.getresponse()
            return response.status, response.read()
        finally:
            connection.close()

    def test_remote_https_origin_only_through_trusted_proxy_host(self):
        public = "https://192.0.2.10:8443"
        server = make_server(0, public_origin=public)
        self.assertEqual(server.server_address[0], "127.0.0.1")
        self.assertEqual(
            server.allowed_origins,
            {"http://127.0.0.1:" + str(server.server_port), public},
        )
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            valid = {"Origin": public}
            status, page = self._request(server, "/", headers=valid)
            self.assertEqual(status, 200)
            token = re.search(rb"const token='([^']+)'", page).group(1).decode()
            self.assertTrue(token)
            self.assertEqual(
                self._request(server, "/api/report", headers={"Origin": "https://evil.invalid"})[0], 403
            )
            self.assertEqual(
                self._request(server, "/api/report", headers={"Host": "192.0.2.10:8443"})[0], 403
            )
            good = {"Origin": public, "X-Subterfuge-Token": token}
            status, contents = self._request(
                server, "/api/analyze-pcap", method="POST", headers=good, body=sample_capture(),
            )
            self.assertEqual(status, 200)
            self.assertIn(b"arp_address_conflict", contents)
            self.assertEqual(
                self._request(
                    server, "/api/analyze-pcap", method="POST",
                    headers={"Origin": public, "X-Subterfuge-Token": "invalid"},
                    body=sample_capture()
                )[0], 403
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=6)

    def test_local_mode_rejects_remote_origin(self):
        server = make_server(0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            self.assertEqual(server.allowed_origins, {server.expected_origin})
            self.assertEqual(
                self._request(
                    server, "/api/report", headers={"Origin": "https://192.0.2.10:8443"}
                )[0], 403
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=6)


if __name__ == "__main__":
    unittest.main()
