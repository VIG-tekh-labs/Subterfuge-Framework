"""The optional Chromium companion must remain visible, local and opt-in."""
from importlib.resources import files
from pathlib import Path
import json
import unittest


class BrowserLabTests(unittest.TestCase):
    def test_manifest_has_only_local_host_permissions(self):
        ext = files("subterfuge").joinpath("browser_lab")
        manifest = json.loads(ext.joinpath("manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["manifest_version"], 3)
        self.assertEqual(manifest["content_scripts"][0]["matches"], ["http://127.0.0.1/*"])
        self.assertEqual(manifest["permissions"], ["storage", "activeTab"])
        self.assertNotIn("webRequest", manifest["permissions"])
        self.assertNotIn("debugger", manifest["permissions"])
        self.assertNotIn("background", manifest)

    def test_local_inspection_excludes_sensitive_browser_state(self):
        ext = files("subterfuge").joinpath("browser_lab")
        content = ext.joinpath("content.js").read_text(encoding="utf-8")
        popup = ext.joinpath("popup.js").read_text(encoding="utf-8")
        self.assertIn("isSubterfugeDashboard()", content)
        self.assertIn("labEnabled", content)
        self.assertIn("chrome.storage.local.set", popup)
        self.assertIn("SUBTERFUGE_LAB_INSPECT", content)
        for forbidden in ("document.cookie", "webRequest", "chrome.cookies", "chrome.history", "eval("):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, content + popup)


if __name__ == "__main__":
    unittest.main()
