"""Packaging contracts: self-contained native binaries, .deb apt deps, installer tasks.

Tests use only Python source inspection and never install software or contact
external systems; production build scripts run only in the OS-specific CI.
"""
from pathlib import Path
import ast
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReleasePackagingTests(unittest.TestCase):
    def test_cli_launcher_defaults_to_gui_and_supports_server_mode(self):
        code = (ROOT / "packaging/desktop_launcher.py").read_text(encoding="utf-8")
        self.assertIn('sys.argv[1:] or ["gui"]', code)
        self.assertIn("cli_main(arguments)", code)
        self.assertNotIn("subprocess.run", code)

    def test_linux_deb_declares_network_package_dependencies(self):
        code = (ROOT / "packaging/build_deb.py").read_text(encoding="utf-8")
        tree = ast.parse(code)
        declarations = [
            n for n in tree.body if isinstance(n, ast.Assign)
            for target in n.targets if isinstance(target, ast.Name)
            and target.id == "DEB_DEPENDENCIES"
        ]
        self.assertEqual(len(declarations), 1)
        packages = ast.literal_eval(declarations[0].value)
        for required in ("nmap", "tshark", "mitmproxy", "libegl1", "libopengl0"):
            self.assertIn(required, packages)
        self.assertIn("usr/share/applications/", code)
        self.assertIn("opt/subterfuge-framework", code)
        self.assertNotIn("sudo", code)

    def test_windows_inno_setup_installer_contains_dependencies_task(self):
        install = (ROOT / "packaging/Subterfuge.iss").read_text(encoding="utf-8")
        self.assertIn("[Setup]", install)
        self.assertIn("[Tasks]", install)
        self.assertIn("[Run]", install)
        self.assertIn("recursesubdirs createallsubdirs", install)
        self.assertIn("networktools", install)
        self.assertIn("WindowsPowerShell", install)
        self.assertIn("AppExe", install)
        self.assertIn("LicenseFile", install)

    def test_windows_optional_dependency_script_uses_exact_winget_ids(self):
        setup = (ROOT / "packaging/install-optional-network-tools.ps1").read_text(encoding="utf-8")
        for package in (
            "Insecure.Nmap", "WiresharkFoundation.Wireshark", "mitmproxy.mitmproxy"
        ):
            self.assertIn(package, setup)
        self.assertIn("--exact", setup)
        self.assertIn("--accept-package-agreements", setup)
        self.assertIn("WinGet is unavailable", setup)
        self.assertNotIn("Invoke-Expression", setup)
        self.assertNotIn("DownloadString", setup)

    def test_frozen_shortcut_and_web_server_are_supported(self):
        shortcut = (ROOT / "src/subterfuge/desktop_shortcut.py").read_text(encoding="utf-8")
        desktop = (ROOT / "src/subterfuge/desktop.py").read_text(encoding="utf-8")
        self.assertIn('getattr(sys, "frozen", False)', shortcut)
        self.assertIn('getattr(sys, "frozen", False)', desktop)
        self.assertIn('["serve", "--port",', desktop)

    def test_bundle_contains_python_qt_and_scapy(self):
        code = (ROOT / "packaging/build_freeze.py").read_text(encoding="utf-8")
        self.assertIn("--onedir", code)
        self.assertIn("--collect-data", code)
        self.assertIn("PySide6", code)
        self.assertIn("scapy", code)
        self.assertIn("PyInstaller", code)

    def test_optional_release_confidentiality_check(self):
        import os
        private_token = os.environ.get("SUBTERFUGE_PRIVATE_PUBLISH_DENY_TERM", "").strip()
        if not private_token:
            self.skipTest("No private, external publication denylist configured.")
        for file in (ROOT / "packaging").rglob("*"):
            if file.is_file() and file.suffix.lower() in (".py", ".iss", ".ps1"):
                self.assertNotIn(private_token.lower(), file.read_text(encoding="utf-8").lower(), str(file))


if __name__ == "__main__":
    unittest.main()
