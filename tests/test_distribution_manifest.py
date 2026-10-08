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


if __name__ == "__main__":
    unittest.main()