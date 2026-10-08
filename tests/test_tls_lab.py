"""Authorized TLS key-log inspection and opt-in local proxy validation."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from subterfuge.analysis import AnalysisError
from subterfuge.tls_lab import decrypt_https, proxy_command

VALID_PCAP = bytes.fromhex("d4c3b2a102000400") + bytes(16)
VALID_KEYLOG = "CLIENT_RANDOM " + "ab" * 32 + " " + "cd" * 48 + "\n"
COLUMNS = [
    "1", "4", "127.0.0.1", "", "127.0.0.1", "",
    "GET", "localhost", "/private/demo", "", "", "", "", "",
]


class TlsDecryptionTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.root = Path(self.dir.name)
        self.capture = self.root / "demo.pcap"
        self.capture.write_bytes(VALID_PCAP)
        self.keylog = self.root / "sslkeys.txt"
        self.keylog.write_text(VALID_KEYLOG)
        self.keylog.chmod(0o600)

    @staticmethod
    def fake_tshark(command, *, timeout=120, stdout=None):
        assert any(item.startswith("tls.keylog_file:") for item in command)
        if "-T" in command and command[command.index("-T") + 1] == "json":
            assert stdout is not None
            stdout.write(b'[{"_source":{"layers":{"http":{"http.request.method":"GET"}}}}]')
            return subprocess.CompletedProcess(command, 0, None, b"")
        return subprocess.CompletedProcess(
            command, 0, ("\t".join(COLUMNS) + "\n").encode(), b"",
        )

    def test_metadata_only_by_default(self):
        with patch("subterfuge.tls_lab.shutil.which", return_value="/usr/bin/tshark"), patch(
            "subterfuge.tls_lab._run_tshark", side_effect=self.fake_tshark
        ):
            result = decrypt_https(self.capture, self.keylog)
        self.assertEqual(result["kind"], "tls_decryption")
        self.assertEqual(result["stats"]["http_messages"], 1)
        self.assertEqual(result["http"][0]["method"], "GET")
        self.assertNotIn("uri", result["http"][0])
        self.assertEqual(result["tls"]["raw_http_content_exported"], False)
        self.assertNotIn("cd" * 48, json.dumps(result))

    def test_explicit_uri_and_decrypted_export_is_private(self):
        path = self.root / "exported.json"
        with patch("subterfuge.tls_lab.shutil.which", return_value="/usr/bin/tshark"), patch(
            "subterfuge.tls_lab._run_tshark", side_effect=self.fake_tshark
        ):
            result = decrypt_https(
                self.capture, self.keylog, include_uris=True, export_json=path,
            )
        self.assertEqual(result["http"][0]["uri"], "/private/demo")
        self.assertTrue(path.is_file())
        if os.name == "posix":
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(result["tls"]["decrypted_json_saved_to"], str(path))

    def test_missing_matching_secrets_is_not_claimed_as_decryption(self):
        with patch("subterfuge.tls_lab.shutil.which", return_value="/usr/bin/tshark"), patch(
            "subterfuge.tls_lab._run_tshark",
            return_value=subprocess.CompletedProcess([], 0, b"", b""),
        ):
            result = decrypt_https(self.capture, self.keylog)
        self.assertEqual(result["tls"]["decrypted_http_messages"], 0)
        self.assertTrue(result["warnings"])

    def test_world_readable_keylog_rejected(self):
        if os.name != "posix":
            self.skipTest("Unix permissions required.")
        self.keylog.chmod(0o644)
        with self.assertRaisesRegex(AnalysisError, "private"):
            decrypt_https(self.capture, self.keylog)

    def test_symlink_secrets_rejected_where_supported(self):
        link = self.root / "keylink"
        try:
            link.symlink_to(self.keylog)
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks may require elevated Windows privileges.")
        with self.assertRaises(AnalysisError):
            decrypt_https(self.capture, link)

    def test_malformed_keylog_rejected(self):
        self.keylog.write_text("CLIENT_RANDOM invalid secret\n")
        with self.assertRaisesRegex(AnalysisError, "SSLKEYLOGFILE"):
            decrypt_https(self.capture, self.keylog)

    def test_invalid_capture_and_invalid_limits_rejected(self):
        self.capture.write_bytes(b"bad file contents")
        with self.assertRaises(AnalysisError):
            decrypt_https(self.capture, self.keylog)
        self.capture.write_bytes(VALID_PCAP)
        for params in ({"maximum_frames": 0}, {"timeout": 900}):
            with self.subTest(params=params):
                with self.assertRaises(AnalysisError):
                    decrypt_https(self.capture, self.keylog, **params)

    def test_existing_output_cannot_be_replaced(self):
        destination = self.root / "existing.json"
        destination.write_text("important content")
        with self.assertRaises(AnalysisError):
            decrypt_https(self.capture, self.keylog, export_json=destination)
        self.assertEqual(destination.read_text(), "important content")


class ProxySafetyTests(unittest.TestCase):
    def test_no_start_without_explicit_opt_in(self):
        with self.assertRaisesRegex(AnalysisError, "authorized"):
            proxy_command("127.0.0.1", 8081, authorized_clients=False)

    def test_loopback_regular_proxy(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch("subterfuge.tls_lab.shutil.which", return_value="/usr/bin/mitmdump"):
                args = proxy_command(
                    "127.0.0.1", 8081, authorized_clients=True, confdir=Path(folder)/"config",
                )
            self.assertIn("regular", args)
            self.assertIn("--listen-host", args)
            self.assertNotIn("transparent", args)
            self.assertTrue((Path(folder)/"config").is_dir())

    def test_remote_or_wildcard_proxy_not_implicitly_enabled(self):
        for host in ("0.0.0.0", "8.8.8.8", "192.168.1.10"):
            with self.subTest(host=host):
                with self.assertRaises(AnalysisError):
                    proxy_command(host, 8081, authorized_clients=True)

    def test_lan_option_does_not_create_open_proxy(self):
        with self.assertRaisesRegex(AnalysisError, "loopback-only"):
            proxy_command("127.0.0.1", 8081, authorized_clients=True, allow_lan=True)

    def test_privileged_ports_rejected(self):
        with self.assertRaises(AnalysisError):
            proxy_command("127.0.0.1", 443, authorized_clients=True)


if __name__ == "__main__":
    unittest.main()
