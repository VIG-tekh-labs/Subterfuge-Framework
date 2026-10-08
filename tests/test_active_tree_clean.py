"""Keep the maintained default branch free of archived 2015-era source."""
from pathlib import Path
from hashlib import sha256
import subprocess
import unittest

ROOT=Path(__file__).resolve().parents[1]
OLD_COMPONENTS=(
    "legacy",
    "modules", "sslstrip", "cease", "templates", "utilities", "main",
    "manage.py", "settings.py", "sslstrip.py", "xsubterfuge",
    "configure.py", "lock.ico",
)
GPL_SHA="8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903"


class ActiveTreeCleanupTests(unittest.TestCase):
    def test_obsolete_framework_is_not_in_active_checkout(self):
        for name in OLD_COMPONENTS:
            with self.subTest(name=name):
                self.assertFalse((ROOT/name).exists(),name)
        self.assertTrue((ROOT/"src/subterfuge/cli.py").is_file())

    def test_old_code_is_not_tracked(self):
        if not (ROOT/".git").exists():
            self.skipTest("No Git metadata inside source distribution.")
        names=subprocess.check_output(
            ["git","ls-files","-z"],cwd=ROOT
        ).decode("utf-8").split("\0")
        self.assertFalse(any(name.startswith("legacy/") for name in names))
        self.assertTrue(any(name.startswith("src/subterfuge/") for name in names))

    def test_full_gpl_remains_unchanged(self):
        self.assertEqual(
            sha256((ROOT/"LICENSE").read_bytes()).hexdigest(), GPL_SHA
        )
        self.assertIn("LICENSE",(ROOT/"COPYING").read_text(encoding="utf-8"))
