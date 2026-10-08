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
RELOCATION = ROOT / "LEGACY_ARCHIVE_FILE_MAP_2026-10-09.csv"
ARCHIVE = ROOT / "legacy/historical-framework-2015-2016"
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
        if not ARCHIVE.exists():
            self.skipTest("Historical sources are deliberately excluded from source distributions.")
        with CSV.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        with RELOCATION.open(newline="", encoding="utf-8") as handle:
            relocation = {item["original_path"]: item["current_path"]
                          for item in csv.DictReader(handle)}
        for row in rows:
            original = row["path"]
            path = ROOT / relocation.get(original, original)
            with self.subTest(path=original):
                if row["status"] == "removed_obsolete_appledouble":
                    self.assertFalse(path.exists())
                    self.assertEqual(row["sha256_after"], "")
                    continue
                self.assertTrue(path.is_file())
                content = path.read_bytes()
                expected = row["sha256_after"]
                digest = sha256(content).hexdigest()
                if digest != expected:
                    # A Windows checkout may convert newline bytes. Git objects
                    # retain the original audited content.
                    git_object = subprocess.run(
                        ["git", "show", "HEAD:" + path.relative_to(ROOT).as_posix()],
                        cwd=ROOT, capture_output=True, check=False,
                    )
                    if git_object.returncode == 0:
                        digest = sha256(git_object.stdout).hexdigest()
                self.assertEqual(digest, expected)
                if row["status"] == "annotated_legacy_template":
                    self.assertIn(MARKER, content)
                if row["changes_content"] == "no":
                    self.assertEqual(row["sha256_before"], row["sha256_after"])
                else:
                    self.assertNotEqual(row["sha256_before"], row["sha256_after"])

    def test_relocation_map_complete_and_license_verbatim(self):
        with RELOCATION.open(newline="", encoding="utf-8") as handle:
            mapping = list(csv.DictReader(handle))
        self.assertEqual(len(mapping), 191)
        self.assertEqual(len({entry["original_path"] for entry in mapping}), 191)
        self.assertEqual(len({entry["current_path"] for entry in mapping}), 191)
        license_entries = [entry for entry in mapping if entry["original_path"] == "COPYING"]
        self.assertEqual(len(license_entries), 1)
        self.assertEqual(license_entries[0]["current_path"], "LICENSE")
        self.assertEqual(
            sha256((ROOT / "LICENSE").read_bytes()).hexdigest(),
            license_entries[0]["sha256_original"],
        )
        self.assertIn("LICENSE", (ROOT / "COPYING").read_text(encoding="utf-8"))
        if not ARCHIVE.exists():
            return
        for entry in mapping:
            with self.subTest(original=entry["original_path"]):
                new_path = ROOT / entry["current_path"]
                self.assertTrue(new_path.is_file())
                content = new_path.read_bytes()
                digest = sha256(content).hexdigest()
                if digest != entry["sha256_original"]:
                    git_object = subprocess.run(
                        ["git", "show", "HEAD:" + entry["current_path"]],
                        cwd=ROOT, capture_output=True, check=False,
                    )
                    if git_object.returncode == 0:
                        digest = sha256(git_object.stdout).hexdigest()
                self.assertEqual(digest, entry["sha256_original"])
                if entry["original_path"] != "COPYING":
                    self.assertFalse((ROOT / entry["original_path"]).exists())


if __name__ == "__main__":
    unittest.main()
