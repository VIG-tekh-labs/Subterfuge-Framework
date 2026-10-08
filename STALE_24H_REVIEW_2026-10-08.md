# Files older than 24 hours — inspection and conservative update

## Superseded path inventory; original files preserved on archive branch

- The owner explicitly authorized applying modernization to the default branch master. Master fast-forwarded without force from 4bc3c2e to f50bd4a (79 commits).
- To remove the 10–11-year-old files from the active GitHub tree, all 193 tracked files in the legacy directory were deleted from the maintained branch (190 older framework files, archive README, original update.py and setup.py).
- The separate branch archive-legacy-original-2026-10-09 preserves the old source, history and copyright attribution. No history rewrite, force push, archival branch deletion or relicensing was performed.
- The active Python 3 runtime remains under src/subterfuge; it is version 2.0.0a2 alpha and does not restore unported historical interception features.
- The original complete GPLv3 text remains byte-for-byte unchanged in LICENSE, with COPYING as a pointer. Historical relocation maps remain documentation, not active source paths.
- Verify Python/Node regression tests, wheel and source archive hygiene, and six-platform CI after this cleanup. Synchronize both modernization and master through non-forced fast-forward, then verify the GitHub default root has no legacy folder.
- Remaining modernization: diverse actual authorized PCAP/PCAPNG captures, safe Scapy passive lab testing, browser accessibility/keyboard checks, provenance and module-by-module feature migration decisions.



Audit date: 2026-10-08T21:43:21.074329+00:00
Git cutoff: 2026-10-07T21:43:21.074329+00:00
Baseline branch: `modernization-2026-10-08-continuation`
Baseline SHA: `060ae24e46b1d70307d26aa9bc98a0666cdc7483`

## Actual changes

- Inspected all 104 tracked paths with a last commit older than 24 hours, including binary identification and content review.
- Annotated **37** first-party editable historical files: 33 Django-style templates and 4 old configurations/launchers.
- Preserved 59 paths without editing them; removed 8 unreferenced AppleDouble macOS resource-fork sidecars after validating magic bytes, sizes and absence of code references. All removals remain recoverable from Git history.
- The COPYING GPL licence, jQuery UI and third-party SSLStrip source are preserved.
- The 37 new lines are explicitly NON-FUNCTIONAL documentation comments. The eight AppleDouble removals are repository hygiene, not a new runtime capability; none of these operations ports Python 2/Django plugins to Python 3.
- No secret values, historical payloads or third-party copyright notices were reissued or modified.

## File disposition summary

| Disposition | Count |
|---|---:|
| `annotated_legacy_config_or_launcher` | 4 |
| `annotated_legacy_template` | 33 |
| `preserved_active_legacy_payload` | 4 |
| `preserved_backup_snapshot` | 1 |
| `preserved_binary` | 45 |
| `preserved_empty_placeholder` | 3 |
| `preserved_license` | 1 |
| `preserved_raw_lookup_data` | 2 |
| `preserved_third_party_source` | 3 |
| `removed_obsolete_appledouble` | 8 |

## Open issues

- The modern package uses src/subterfuge and does not load the historical Django templates. Their 2026 comments are not evidence of runtime migration.
- Retired configs still contain historical hard-coded network settings. Never deploy those old files to a production network.
- Historical active payloads, the 45 intact original images/icons, and raw lookup datasets were intentionally not rewritten. All 45 images/icons passed a local ImageMagick decode; duplicate image variants were retained because legacy references may depend on their filenames.
- Third-party legal notices need separate provenance assessment before new builds or relicensing.
- Eight retired AppleDouble sidecars (not actual PNG/HTML/CSS resources) were removed from the working branch. They were binary metadata with AppleDouble signature 00051607 and no references; Git history preserves them.
- One-by-one functional migration and real authorized network fixture testing are still required.

## Verification and continuity

- `FILE_REVIEW_OLDER_24H_2026-10-08.csv` records all qualifying paths, previous Git date, pre/post SHA-256 checksums, preservation/annotation status and explanation.
- `FILE_AGE_INVENTORY_2026-10-08.csv` preserves the earlier long-term 252-file historic classification.
- Modern Python regression tests, Node report schema checks, wheel/sdist hygiene checks and CI must pass after publishing.
- Do not merge master, rewrite Git history or change licence terms without explicit owner approval.

## Published GitHub verification

- Published exact audited snapshot: `b6864e3376c5eb59329e0120b8de0704d9cfd434` on the modernization branch, not master. Git tree matches local staged tree (`d3eb27b0c0938dd52cef2e7be30238942601677a`).
- Independent Git archive: 103 unittest cases discovered (102 passed; one skipped without Git metadata), Node report QA passed, wheel and source archives built, and distribution contents passed hygiene inspection (18 wheel members / 63 source members).
- [GitHub Actions run 37850134395](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37850134395) verified all six Linux/Windows/macOS configurations successfully.
- Source-code functional restoration is still pending for historical Python 2/Django/Twisted and interception modules. The 37 template/config comments are non-executing status markers only.

## Structural follow-up on October 9, 2026

- The earlier 104-row original-path review remains a valid historical snapshot, not a live directory listing. In a separate follow-up, the complete old source/UI directory structure was moved under `legacy/historical-framework-2015-2016/`, and the full GPLv3 text formerly in COPYING was relocated unchanged to LICENSE.
- See `LEGACY_ARCHIVE_FILE_MAP_2026-10-09.csv` and `LEGACY_REORGANIZATION_2026-10-09.md` for all 191 immutable byte-content mappings and rationale. Archived original source ages and the Git history are not erased. The modern runtime remains alpha.
