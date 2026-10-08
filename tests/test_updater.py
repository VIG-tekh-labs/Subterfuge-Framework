"""Legacy update entry-point must be safe on modern Python."""
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class UpdaterTests(unittest.TestCase):
    def test_help_is_read_only(self):
        result = subprocess.run([sys.executable, str(ROOT / "update.py"), "--help"],
                                capture_output=True, text=True, check=True, timeout=10)
        self.assertIn("--version", result.stdout)

    def test_update_notice_does_not_execute_legacy_commands(self):
        result = subprocess.run([sys.executable, str(ROOT / "update.py")],
                                capture_output=True, text=True, check=True, timeout=10)
        self.assertIn("SVN auto-updater is retired", result.stdout)
        self.assertIn("python -m pip install --upgrade .", result.stdout)
