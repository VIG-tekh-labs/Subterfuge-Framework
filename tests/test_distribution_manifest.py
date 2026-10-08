"""Prevent source archive regression in required QA and license manifests."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DistributionManifestTests(unittest.TestCase):
    def test_source_manifest_includes_audit_and_excludes_legacy(self):
        text = (ROOT / "MANIFEST.in").read_text(encoding="utf-8")
        self.assertIn("recursive-include qa *.py *.mjs *.cjs", text)
        self.assertIn("prune legacy", text)
        self.assertIn("include COPYING", text)


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
