"""Guard against reintroducing historic generated or sensitive artifacts."""
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RepositoryHygieneTests(unittest.TestCase):
    def test_no_tracked_secret_or_generated_artifacts(self):
        if not (ROOT / ".git").exists():
            self.skipTest("Git metadata is unavailable in an installed source package.")
        files = subprocess.check_output(["git", "-C", str(ROOT), "ls-files", "-z"]).decode().split("\0")
        tracked = set(filter(None, files))
        protected = {"cert.pem", "credentials.txt", "db", "base_db"}
        prohibited = [
            name for name in tracked
            if name in protected or name.lower().endswith((".pyc", ".log", ".pem", ".key", ".sqlite", ".sqlite3"))
        ]
        self.assertEqual(prohibited, [], f"Unexpected generated/sensitive tracked artifacts: {prohibited}")

    def test_legacy_django_secret_is_not_embedded_as_literal(self):
        settings = (ROOT / "settings.py")
        if not settings.exists():
            self.skipTest("Legacy Django settings excluded from the installed package.")
        text = settings.read_text()
        self.assertNotRegex(text, r"(?m)^SECRET_KEY\s*=\s*['\"]")


if __name__ == "__main__":
    unittest.main()