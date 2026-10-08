# Archival reorganization of Subterfuge — 2026-10-09

## Reason and intent

The owner requested that the maintained repository branch no longer display
2015-era files as though they were the active Python 3 framework. The operation
is a real Git path relocation, **not a manipulation of commit dates**.

- Base: 8c8f7f347b4651d064516758ef4c9abf9495cacf
- Active work branch: modernization-2026-10-08-continuation
- Immutable pre-change snapshot branch: archive-legacy-original-2026-10-09
- Archive folder: legacy/historical-framework-2015-2016/
- Full per-file original-to-current path and SHA-256: LEGACY_ARCHIVE_FILE_MAP_2026-10-09.csv

## Implementation

- All historical Python 2/Django/Twisted source, legacy templates and image
  assets, old executables/configs and security-related reference modules
  were moved with Git rename operations into one self-contained legacy tree.
  Original contents, executable flags, copyright notices and per-file license
  conditions were preserved. The archive is excluded from wheel/sdist.
- Exact verbatim GNU GPLv3 license bytes were moved from root COPYING to
  root LICENSE, preserving SHA-256: 8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903. A short root COPYING pointer was
  added. The packaging license-files field now refers to root LICENSE;
  the declared GPL-3.0-or-later license has NOT changed.
- Tests and modern documentation were updated for the new historical paths.

## Key cautions

- This changes the most recent Git path history through legitimate relocation,
  but the actual 2015 source is STILL OLD and NOT certified as functional.
- The original Git commit history and pre-change archival branch remain visible.
  Rewriting history just to hide dates would be misleading.
- No offensive historical modules were executed. The current Python 3 tool
  remains version 2.0.0a2 alpha and is NOT equivalent to the old MITM framework.
- The default master branch is still the older baseline; no merge can be made
  without explicit approval.
- Proprietary third-party or GPLv2-only historical notices remain independently
  applicable to the archived materials. Any sensitive data in old commits still
  requires coordinated review, not merely a directory rename.

## Required release checks

1. Every file in the relocation CSV exists at its new path with exact original
   SHA-256 bytes, including the full original GPL license.
2. Run the modern Python regression suite and Node browser-schema QA in a clean checkout.
3. Build modern wheel/sdist, verify inclusion of complete LICENSE and exclusion
   of legacy directory; inspect Windows/macOS/Linux CI.
4. Check the current branch again for any remaining last-commit dates older than
   24 hours, and do not conflate archival moves with real functionality updates.
5. Record exact commit SHA and CI result in ROADMAP.md and HANDOFF.md.

## Actual published verification

- The complete archive and packaging tree was committed as `1f21f9bc8cfafd4689eb781e6f83f7f335fcf8f5`, tree `36793967e59cc7e2f153c20fc1f89d4b8c8695fd`, to the modernization branch only.
- Zero of 255 current paths on that published branch had last-commit timestamps older than 24h at 2026-10-09 01:03 Brussels; original 2015 commit history remains intact and separately browsable.
- A fresh export of the exact published tree passed 105 tests (103 successes and two expected skips because Git metadata is not included in archives), Node report validation (five valid, ten malformed), and wheel/sdist packaging audits (18/66 entries with byte-identical GPL).
- [GitHub Actions run 37857219307](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37857219307) completed six successful jobs across Linux, Windows and macOS.
- The default master and GPL terms are untouched. Historical code remains archived, not newly functional or secure.

