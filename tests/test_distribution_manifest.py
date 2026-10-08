"""Prevent source archive regression in required QA and license manifests."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DistributionManifestTests(unittest.TestCase):
    def test_source_manifest_includes_audit_and_excludes_legacy(self):
        text = (ROOT / "MANIFEST.in").read_text(encoding="utf-8")
        self.assertIn("recursive-include qa *.py *.mjs *.cjs", text)
        self.assertIn("prune legacy", text)
        self.assertIn("recursive-include src/subterfuge/browser_lab *.json *.html *.js *.css", text)
        self.assertIn("LEGACY_ARCHIVE_FILE_MAP_2026-10-09.csv", text)
        self.assertIn("LEGACY_REORGANIZATION_2026-10-09.md", text)
        self.assertIn("include COPYING LICENSE", text)


    def test_full_gpl_is_preserved_in_root_license(self):
        from hashlib import sha256
        text=(ROOT / "LICENSE").read_bytes()
        self.assertTrue(text.startswith(b"                    GNU GENERAL PUBLIC LICENSE"))
        self.assertEqual(
            sha256(text).hexdigest(),
            "8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903",
        )
        self.assertIn("LICENSE", (ROOT / "COPYING").read_text(encoding="utf-8"))

    def test_historical_age_audit_is_packaged_with_handoff(self):
        manifest = (ROOT / "MANIFEST.in").read_text(encoding="utf-8")
        for document in (
            "MODERNIZATION_STATUS.md",
            "LEGACY_AGE_REVIEW_2026-10-08.md",
            "FILE_AGE_INVENTORY_2026-10-08.csv",
        ):
            with self.subTest(document=document):
                self.assertIn(document, manifest)
                self.assertTrue((ROOT / document).is_file())


if __name__ == "__main__":
    unittest.main()
