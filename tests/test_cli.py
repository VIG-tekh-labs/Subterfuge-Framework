"""Exercise user commands from a separate working directory."""

from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile
import unittest

from subterfuge import __version__
from subterfuge.demo import sample_capture

ROOT = Path(__file__).resolve().parents[1]


class CommandTests(unittest.TestCase):
    def run_cli(self, *arguments, cwd):
        environment = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
        return subprocess.run([sys.executable, "-m", "subterfuge", *map(str, arguments)], cwd=cwd, env=environment, text=True, capture_output=True, timeout=15)

    def test_version_and_help(self):
        with tempfile.TemporaryDirectory() as folder:
            result = self.run_cli("--version", cwd=folder)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), __version__)
            self.assertEqual(self.run_cli("--help", cwd=folder).returncode, 0)

    def test_demo_and_json_export(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "report.json"
            result = self.run_cli("demo", "--output", output, cwd=folder)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["stats"]["findings"], 1)
            self.assertEqual(json.loads(output.read_text()), report)

    def test_pcap_file_import(self):
        with tempfile.TemporaryDirectory() as folder:
            capture = Path(folder) / "sample.pcap"
            capture.write_bytes(sample_capture())
            result = self.run_cli("analyze-pcap", capture, cwd=folder)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["stats"]["arp_packets"], 2)

    def test_standard_nmap_file_import(self):
        with tempfile.TemporaryDirectory() as folder:
            result = self.run_cli("import-nmap", ROOT / "tests/fixtures/nmap_inventory.xml", cwd=folder)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["stats"]["open_ports"], 2)

    def test_missing_and_invalid_input_errors(self):
        with tempfile.TemporaryDirectory() as folder:
            invalid = Path(folder) / "invalid.xml"
            invalid.write_text("invalid")
            for arguments in [("import-nmap", invalid), ("analyze-pcap", Path(folder) / "missing.pcap")]:
                with self.subTest(arguments=arguments):
                    result = self.run_cli(*arguments, cwd=folder)
                    self.assertEqual(result.returncode, 2)
                    self.assertIn("Error:", result.stderr)
                    self.assertNotIn("Traceback", result.stderr)

    def test_optional_tls_browser_and_bettercap_commands(self):
        with tempfile.TemporaryDirectory() as folder:
            metadata = self.run_cli("agent-capabilities", cwd=folder)
            self.assertEqual(metadata.returncode, 0, metadata.stderr)
            self.assertIn("tls_decrypt", json.loads(metadata.stdout)["action_schema"])
            extension = self.run_cli("browser-lab", cwd=folder)
            self.assertEqual(extension.returncode, 0, extension.stderr)
            self.assertTrue(
                Path(json.loads(extension.stdout)["installed_extension_directory"])
                .joinpath("manifest.json").is_file()
            )
            events = Path(folder)/"events.json"
            events.write_text('[]', encoding="utf-8")
            bettercap = self.run_cli("import-bettercap", events, cwd=folder)
            self.assertEqual(bettercap.returncode, 0, bettercap.stderr)
            self.assertEqual(json.loads(bettercap.stdout)["stats"]["total_events"], 0)
            proxy = self.run_cli("proxy-lab", cwd=folder)
            self.assertEqual(proxy.returncode, 2)
            self.assertIn("authorized", proxy.stderr)

    def test_doctor_requires_no_optional_packages(self):
        with tempfile.TemporaryDirectory() as folder:
            result = self.run_cli("doctor", cwd=folder)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json.loads(result.stdout)["offline_analysis"])


if __name__ == "__main__":
    unittest.main()
