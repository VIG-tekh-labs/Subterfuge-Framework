"""Explicit per-user Linux menu shortcut does not overwrite unknown files."""
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from subterfuge.analysis import AnalysisError
from subterfuge.desktop_shortcut import _safe_quote, install_shortcut


class NativeShortcutTests(unittest.TestCase):
    def test_quotes_paths_without_shell(self):
        self.assertEqual(_safe_quote('/tmp/a b'), '"/tmp/a b"')
        self.assertIn('\\\\',_safe_quote('/tmp/a\\b'))
        with self.assertRaises(AnalysisError):
            _safe_quote("bad\nname")

    @unittest.skipUnless(os.name=="posix", "Linux XDG test")
    def test_install_is_opt_in_idempotent_and_local(self):
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ,{"XDG_DATA_HOME":temp}):
            if not os.sys.platform.startswith("linux"):
                self.skipTest("Linux only.")
            shortcut=install_shortcut()
            self.assertTrue(shortcut.is_file())
            data=shortcut.read_text()
            self.assertIn("Terminal=false",data)
            self.assertIn("-m subterfuge gui",data)
            self.assertNotIn("serve --open",data)
            icon=Path(temp)/"icons/hicolor/scalable/apps/subterfuge-framework.svg"
            self.assertTrue(icon.is_file())
            self.assertEqual(install_shortcut(),shortcut)
            shortcut.write_text("[Desktop Entry]\nName=User customization\n")
            with self.assertRaisesRegex(AnalysisError,"existing"):
                install_shortcut()
            self.assertIn("User customization",shortcut.read_text())

    def test_relative_data_home_rejected(self):
        with patch.dict(os.environ,{"XDG_DATA_HOME":"./relative"},clear=False):
            if os.sys.platform.startswith("linux"):
                with self.assertRaises(AnalysisError):
                    install_shortcut()


if __name__=="__main__":
    unittest.main()
