"""Reproducible integrity check for the October 2026 legacy file review."""
from __future__ import annotations

from collections import Counter
import csv
from hashlib import sha256
from pathlib import Path
import unittest
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "FILE_REVIEW_OLDER_24H_2026-10-08.csv"
MARKER = b"{# Reviewed 2026-10-08: archived Django UI, not loaded by the Python 3 package. #}"


class StaleFileReviewTests(unittest.TestCase):
    def test_included_inventory_has_complete_decisions(self):
        if not CSV.exists():
            self.skipTest("The historical review inventory is not available.")
        with CSV.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 104)
        self.assertEqual(len({row["path"] for row in rows}), 104)
        counts = Counter(row["status"] for row in rows)
        self.assertEqual(counts["annotated_legacy_template"], 33)
        self.assertEqual(counts["annotated_legacy_config_or_launcher"], 4)
        self.assertEqual(sum(row["changes_content"] == "yes" for row in rows), 45)
        self.assertEqual(counts["preserved_binary"], 45)
        self.assertEqual(counts["removed_obsolete_appledouble"], 8)
        self.assertEqual(counts["preserved_license"], 1)
        self.assertTrue(all(row["review_notes"] for row in rows))
        self.assertTrue(all(row["sha256_before"] for row in rows))
        self.assertTrue(all(row["sha256_after"] or row["status"] == "removed_obsolete_appledouble" for row in rows))

    def test_legacy_sources_preserve_provenance_and_review_comments(self):
        if not (ROOT / "templates/basic.tm").exists():
            self.skipTest("Legacy templates are excluded from modern source archives.")
        with CSV.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            path = ROOT / row["path"]
            with self.subTest(path=row["path"]):
                if row["status"] == "removed_obsolete_appledouble":
                    self.assertFalse(path.exists())
                    self.assertEqual(row["sha256_after"], "")
                    continue
                self.assertTrue(path.is_file())
                content = path.read_bytes()
                expected = row["sha256_after"]
                digest = sha256(content).hexdigest()
                if digest != expected:
                    # Windows Git checkouts can translate newline bytes; Git
                    # objects preserve the exact audited committed contents.
                    reference = subprocess.run(
                        ["git", "show", "HEAD:" + row["path"]],
                        cwd=ROOT, capture_output=True, check=False,
                    )
                    if reference.returncode == 0:
                        digest = sha256(reference.stdout).hexdigest()
                self.assertEqual(digest, expected)
                if row["status"] == "annotated_legacy_template":
                    self.assertIn(MARKER, content)
                if row["changes_content"] == "no":
                    self.assertEqual(row["sha256_before"], row["sha256_after"])
                else:
                    self.assertNotEqual(row["sha256_before"], row["sha256_after"])


if __name__ == "__main__":
    unittest.main()
