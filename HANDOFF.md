# Subterfuge Framework — verified continuation handoff

## FINAL MAIN-BRANCH CLEANUP — exact continuation

- The owner explicitly authorized applying modernization to the default branch master. Master fast-forwarded without force from 4bc3c2e to f50bd4a (79 commits).
- To remove the 10–11-year-old files from the active GitHub tree, all 193 tracked files in the legacy directory were deleted from the maintained branch (190 older framework files, archive README, original update.py and setup.py).
- The separate branch archive-legacy-original-2026-10-09 preserves the old source, history and copyright attribution. No history rewrite, force push, archival branch deletion or relicensing was performed.
- The active Python 3 runtime remains under src/subterfuge; it is version 2.0.0a2 alpha and does not restore unported historical interception features.
- The original complete GPLv3 text remains byte-for-byte unchanged in LICENSE, with COPYING as a pointer. Historical relocation maps remain documentation, not active source paths.
- Verify Python/Node regression tests, wheel and source archive hygiene, and six-platform CI after this cleanup. Synchronize both modernization and master through non-forced fast-forward, then verify the GitHub default root has no legacy folder.
- Remaining modernization: diverse actual authorized PCAP/PCAPNG captures, safe Scapy passive lab testing, browser accessibility/keyboard checks, provenance and module-by-module feature migration decisions.
The default GitHub view is now on modern master; old historical files are accessible via archive-legacy-original-2026-10-09 only. Do not reintroduce or re-import them.


## Definitive current state — October 9, 2026

- **Published modern branch last validated code commit:** `1f21f9bc8cfafd4689eb781e6f83f7f335fcf8f5` (archive structural cleanup). Previous last substantive runtime feature commit remains `d8bb5b8`; version `2.0.0a2` alpha, not historical parity.
- Preservation: `archive-legacy-original-2026-10-09` points at the exact pre-move snapshot `8c8f7f3`; 190 historical source files have been moved intact under `legacy/historical-framework-2015-2016/`; original full GPLv3 text from COPYING is unchanged at LICENSE (SHA-256 `8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903`). Full mapping is in `LEGACY_ARCHIVE_FILE_MAP_2026-10-09.csv`.
- Fresh Git archive of code commit `1f21f9b`: **105 Python tests, 103 passed + 2 skipped** due to absent Git metadata; Node report QA passed (5 valid, 10 invalid fixtures); wheel/sdist hygiene passed (18 and 66 archive entries). Git checkout before publishing passed 104 tests with one expected skip.
- GitHub Actions [run 37857219307](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37857219307) completed **six out of six jobs successfully**.
- Timestamp verification: **255 current tracked paths, zero last-touched Git commit dates older than 24h** at the check on 2026-10-09 01:03 Brussels. This DOES NOT erase old Git commits or upgrade archived Python 2 functionality.
- Master baseline remains `4bc3c2e`; keep `master` untouched until explicitly authorized. Do not force-push, delete provenance or change license terms. Current source branch is `modernization-2026-10-08-continuation`. The specific clean development worktree was `~/projects/Subterfuge-Framework-stale-complete-20261009`; older worktrees may contain uncommitted work and must not be reset.
- Next: read ROADMAP and MODERNIZATION_STATUS before starting; prioritize module-by-module functional compatibility, real permitted capture tests, build/CI stability, security and licensing rather than further cosmetic timestamp changes.

**Date:** 2026-10-09 (Europe/Brussels)  
**Repository:** https://github.com/VIG-tekh-labs/Subterfuge-Framework  
**Working branch:** `modernization-2026-10-08-continuation`  
**Last fully validated feature commit:** `d8bb5b836b20046e13712beced1e03c7b5ee36c5`  
**Development version:** `2.0.0a2` (alpha; NOT full historical restoration)

## Verified results at this checkpoint

- The published feature branch was fetched into a clean archive and discovered **100** Python test cases: **99 passed and 1 was skipped** because Git metadata is absent from archives. In a Git checkout, all 100 passed.
- Wheel build passed in the fresh archive; previously examined wheel and source archives exclude historical interception source, private PEM, secrets, logs and SQLite databases.
- **GitHub Actions run 37840748127 for the latest verified feature commit passed all six jobs:** Linux/Python 3.11–3.14, Windows/Python 3.12 and macOS/Python 3.12.
- Chromium/Puppeteer interactive QA passed: demo loading, upload/report display and JSON export, TLS form invalid-input handling, local reopening of saved JSON reports and malformed-report rejection. No JavaScript page exceptions observed in these checks.
- Wireshark `editcap` conversion to PCAPNG was successfully decoded, matching classic PCAP ARP observations.
- Explicit Nmap service inventory passed against a temporary **127.0.0.1** listener only. No LAN or Internet target was scanned.
- Optional Scapy **2.8.0** installed and detected in an isolated environment. **Real-interface live capture was not verified**; Scapy adapter tests were mocked.

## Functional modern core

- Python 3.11+ package, pip/venv install, modern CLI, stdlib local dashboard with authenticated same-origin requests.
- Classic PCAP and experimental PCAPNG ARP and passive DHCP/NBNS/WPAD metadata aggregation (bounded input, no retention of DHCP option data).
- Import Nmap XML, optional host discovery, and opt-in bounded TCP service scan of one authorized IP; real adapter smoke tested on loopback.
- Certificate-verified TLS endpoint review in CLI and dashboard, no SSLStrip or downgrade proxy.
- Private atomic CLI JSON report exports, browser JSON download and local browser reopening of saved reports.

## Do not misrepresent status

- The modern package does NOT restore historical rogue-DHCP, ARP interception, SSLStrip, session interception, credential harvesters, response injection, denial of service or wireless AP creation. Those historical sources remain reference material and were not executed.
- 26 of 82 original Python files failed Python 3 AST parsing in the original audit; these are mostly Python 2 historical sources **outside** the active package. Syntax compatibility of every historical file is not required for the modern installed package, but full historical feature parity is not achieved.
- Current active dependencies: Python standard library; optional Scapy and Nmap. Django, Twisted and jQuery are not required by the active runtime.
- The project still carries GPL obligations for retained licensed material. See `LICENSING.md` regarding a historical GPLv2-only file and GPLv3 material; no automatic relicensing from rewriting code.
- Historical public `master` and old Git commits still contain sensitive artifacts despite cleanup on the feature branch. Secrets used in real deployments should be rotated; history rewriting needs deliberate owner approval.
- **Never merge into `master`, force-push or rewrite history without explicit owner approval.**

## Exact next actions

1. Verify current branch head and GitHub CI before changing files. Read `ROADMAP.md`, `MIGRATION_MATRIX.md`, `AUDIT.md`, `SECURITY.md`, `LICENSING.md` and this handoff.
2. Expand PCAPNG and DHCP/NBNS real capture test corpus, including malformed-input limits; test live Scapy capture only against a specifically authorized isolated interface.
3. Review historical module implementations and bring forward legitimate capabilities selectively, preserving authorship and documenting why obsolete mechanisms are retired.
4. Improve UI accessibility and state handling, and assess optional secure local persistence and import of prior case data without relying on legacy Django.
5. Coordinate old-commit secret remediation and third-party licensing review with the owner before any license change or public release.
6. Update `ROADMAP.md` **after every verified code change, test, publication, blocker and before interruption**, recording exact commits, branch, test results and the next actionable step.

## Local development

Use a **fresh checkout/worktree** for each new checkpoint rather than overwriting older working directories with unpublished changes. On Linux, create an isolated `python3 -m venv .venv`, activate it, install with `python -m pip install .` and run `python -m unittest discover -s tests -v`. For additional lab-only checks see `qa/loopback_nmap_smoke.py`.

**Documentation and commit messages are in English, per the owner's project requirements.**

## October 8 continuation — PCAPNG extended formats (latest verified)

- Branch: `modernization-2026-10-08-continuation`. New development snapshot: `1581fefff359bcf6eca7b7727005848293944b9a`; documentation checkpoint: `c24f4537ee87079255504be7ce586a584e6eee3f`.
- Production code: `src/subterfuge/analysis.py` now accepts PCAPNG Enhanced Packet Blocks (6), legacy Packet Blocks (2), Simple Packet Blocks (3), and interface timestamp offsets. For Simple Packet Blocks, no time is invented; JSON host times are null if no timestamped evidence exists. The dashboard and README disclose experimental capture compatibility.
- Regression coverage: `tests/test_pcapng_packet_blocks.py` and `tests/test_web.py` cover synthetic endian variants, malformed blocks, passive DHCP passthrough, time-offset handling and loopback HTTP import.
- **Re-verified from published Git archive:** Linux/Python 3.14.7 reports `Ran 97 tests ... OK (skipped=1)`; compileall and wheel creation passed. Wheel checked for historical/secret/credential paths and none were present among 18 archived members. The skipped test needs a Git checkout and does not imply a failure.
- Previously recorded six-platform CI success applies to an **earlier commit**; a new CI verification for `1581fef` is still required. Broader real capture interoperability and real hardware passive capture remain unverified.
- Keep old working folders intact: `~/projects/Subterfuge-Framework-phase2` and others may contain unpublished changes. Fresh development folder `~/projects/Subterfuge-Framework-hardening-20261008` has local modifications already published through the GitHub connector, but is not yet reset to remote HEAD.
- **Next exact steps:** check GitHub Actions status for latest remote HEAD; add diverse externally generated PCAPNG fixtures including simple packet and corrupt options; perform accessibility/browser checks and review UI report validation; update ROADMAP.md following each verified step. Do not merge into master, change license metadata or rewrite public history without owner authorization.

## Latest validation after PCAPNG metadata-bound hardening

- Verified published code commit: `cf49be2d85d3764649677cc5dbe738aa68832374`; roadmap checkpoint: `f4c705ee22823a13fedc5eda65c4bdc17e52eda6`.
- PCAPNG now explicitly limits **all parsed blocks**, including unrecognized metadata blocks, with a bounded count. This prevents large inputs full of tiny metadata blocks from evading the existing packet cap. Tests include a configured low limit to verify rejection.
- Git archive fresh-checkout Linux/Python 3.14.7 results: **98 tests passed, one conditional Git-check test skipped**, compileall succeeded. The previous wheel build and path hygiene checks passed at feature commit `1581fef`; the new bound change has not yet had independent wheel reinspection.
- GitHub Actions run [37838822992](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37838822992) **passed six jobs** for `1581fef` across supported matrix runners. CI for the new `cf49be2` commit was in progress at the last query and must be rechecked.
- Do not overwrite the older dirty local checkouts; the isolated development checkout for these code changes is `~/projects/Subterfuge-Framework-hardening-20261008`. GitHub connector published the content, so local HEAD can lag behind the published branch.
- Next exact actions: verify CI head for `cf49be2`, review saved-report browser import validation and accessibility, add malformed/real PCAPNG interoperability fixtures, then record an updated roadmap checkpoint before any interruption. Keep GPL obligations, alpha caveats and no-master-merge rules unchanged.

## Saved-report browser validation checkpoint — current

- Published source feature HEAD `ac3b754b926d682c6514a45aeff014f4226804e1`, followed by ROADMAP.md checkpoint `968fd5294e66ef64fe0b221f085b245ceb70e945`.
- The browser-side importer now rejects malformed nested host, ports, MACs, timestamps and DHCP/NBNS observation records before replacing the displayed report. Existing valid reports and JSON null timestamps are preserved.
- Added `qa/browser_report_validation.mjs` (no npm dependencies), invoked by the GitHub Actions workflow, and optional `qa/browser_report_smoke.cjs` (Puppeteer externally installed, sandboxed Chromium loopback QA). Updated README.md and SECURITY.md.
- **Fresh published archive validation:** 98 discovered Python unit tests: 97 passed and 1 Git-metadata-dependent case skipped; Node validation accepted 5 genuine/synthetic records and rejected 10 malformed ones; sandboxed Chromium imported a valid report, rejected malformed data without losing the previous report and had zero uncaught page exceptions; compileall passed.
- **CI:** the earlier `cf49be2` PCAPNG hardening run `37839129084` completed successfully. The revised CI workflow commit `ac3b754` was **queued** on run `37839864418` when last checked. Re-check before claiming matrix-wide success for the browser validator.
- Next steps: verify six current CI jobs; rebuild and audit wheel/sdist from latest branch; expand PCAPNG external capture coverage; improve UI accessibility and focus behavior; continue historical migration/licensing provenance audit, without merging into master or rewriting history.

## Latest checkpoint — distribution audit and source QA reproducibility

- Latest fully validated published feature commit: `d18dd998dc28d89d460271d2fe3945ad7a46966b`. Roadmap checkpoint: `a633810716ad2e532052f24af0e28fbb947c6572`.
- Packaging: `MANIFEST.in` includes source-only QA scripts. New `qa/audit_distributions.py` checks the wheel and sdist for expected runtime/docs/QA files and rejects legacy interception trees, credentials, private keys, databases and runtime logs. `tests/test_distribution_manifest.py` prevents regression.
- CI now builds an isolated source distribution and runs artifact checks alongside Python, Node browser-schema and installed CLI tests. `build` is a **development-only frontend**, not a runtime dependency. The direct `--no-isolation` build initially failed because setuptools was absent in the development venv; normal isolated build succeeded, as intended.
- Independent Git archive of published `d18dd99` passed **99 Python test cases: 98 passed, 1 Git-metadata test skipped**; Node report-schema QA passed (5 valid, 10 malformed); wheel and source archives built; archive audit found **18 wheel members and 57 source members with no prohibited files**.
- **CI caveat:** prior browser-validator run [37839864418](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37839864418) passed all six matrix jobs. New source-distribution run [37840372524](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37840372524) was **in progress** at last check. Confirm all six results before expanding validated cross-platform claims.
- Next: verify six newest CI jobs and inspect failures if any; extend safe real-capture corpus, UI keyboard/a11y tests, and historical module audit. Legacy Django/Twisted/jQuery are unnecessary for modern runtime; GPL and historical-license obligations remain. Never force-push, merge master or rewrite history without owner approval.

## Current handoff — accessibility and release hygiene

- Latest verified feature commit: `d8bb5b836b20046e13712beced1e03c7b5ee36c5`. Updated roadmap checkpoint: `c60fb6c070cbebdd8f8353500343e323364cac0a`.
- Dashboard now gives explicit accessible semantics to the host inventory and dynamically rendered passive evidence/findings/warnings. A Python HTTP boundary test and sandboxed Chromium QA exercise these attributes with valid PCAPNG saved-report imports.
- Fresh Git archive of `d8bb5b8`: 100 test cases discovered, **99 passed, 1 skipped** (Git metadata absent); Node browser validator (5 valid, 10 malformed) and sandboxed Chromium QA succeeded, with zero uncaught browser exceptions. Local Git worktree ran all 100 tests successfully.
- Artifact-build and archive-hygiene workflow run [37840372524](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37840372524) **passed all six** Linux/Windows/macOS jobs. The newer accessibility workflow run [37840748127](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37840748127) was in progress at last check.
- Remember: current alpha supports passive capture/inventory/TLS review but does NOT have historical active-interception feature parity. GPL obligations remain, historical public secrets need owner-coordinated remediation, and there is no permission to merge master, force-push or rewrite history.
- Next: verify newest six CI jobs; expand authentic sample capture and malformed-input test corpus; test keyboard accessibility in a real browser, and continue safe module-by-module migration. Keep ROADMAP.md updated after each verified change.

## CI status confirmation after accessibility delivery

- GitHub Actions run [37840748127](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37840748127) for latest fully verified **feature** commit `d8bb5b8` has now completed with **six out of six jobs successful** (Linux Python 3.11–3.14, macOS/Windows Python 3.12).
- Earlier "pending" notes above are retained as chronological history and are superseded by this confirmation. The code feature branch remains alpha `2.0.0a2`; current GitHub documentation-only head can be newer than the last tested feature commit.
- Next session must read current branch HEAD, `ROADMAP.md`, and this `HANDOFF.md`; resume focused real-capture interoperability, authorized lab-only passive adapter QA, accessibility keyboard checks, and source/license/secret provenance review, without merging master or rewriting history.

## Current master/branch status and file-age audit — 2026-10-08

- The earlier report that GitHub had no recent commits was explained by branch selection. Direct git ls-remote confirmed master at 4bc3c2e (17:39 Brussels) and modernization at ea23621 (22:38 Brussels) **before this audit's new documentation commit**.
- The modernization branch had **73 commits beyond master** at the audit start, all published, and three older local worktrees contained only superseded versions or whitespace-only mismatches against current remote source. They were not reset or overwritten.
- Full date inventory created in FILE_AGE_INVENTORY_2026-10-08.csv (252 tracked paths at ea23621 baseline) and LEGACY_AGE_REVIEW_2026-10-08.md. Last Git commit date alone is not evidence that old functionality was modernized.
- MODERNIZATION_STATUS.md is the concise authoritative functional/risks/TODO summary, and README explicitly clones the modernization branch for the current alpha.
- **Current confirmed feature validation** remains d8bb5b8: all six CI jobs successful, 100 Python cases in a Git checkout; clean archive 99 passes + 1 Git-metadata skip. No newer active-code change is represented by this audit. Version 2.0.0a2 alpha.
- Next: confirm new HEAD and CI after audit docs are committed; proceed with historical module-by-module classifications and real authorized capture test corpus. No master merge, history rewrite or license change without owner approval.

## Published audit and definitive cross-platform CI result — October 8, 2026

- The 252-file history inventory and complete next-actions summary were **actually published** in one commit `9ae17f2631a65cfeb8e58dd3657a478dbed7993d`, not merely saved locally. The default master remains at `4bc3c2e`; view the `modernization-2026-10-08-continuation` branch to see current work.
- New files: MODERNIZATION_STATUS.md, LEGACY_AGE_REVIEW_2026-10-08.md, FILE_AGE_INVENTORY_2026-10-08.csv. Updated README branch-clone instructions, ROADMAP, this HANDOFF, MANIFEST.in, distribution audit and its regression test.
- Fresh Git archive verified `9ae17f2`: **101 discovered tests; 100 passed and one Git-metadata-dependent test skipped**, Node browser QA 5 valid/10 invalid cases passed, wheel and sdist audits passed (18/60 members; zero prohibited entries).
- **CI 37847844746: all six Linux/Windows/macOS jobs completed successfully** for `9ae17f2`. Earlier run-status notes above are historical and superseded by this confirmed outcome.
- The audited 2015–2016 historical source has not magically become Python 3-compatible from 2026 maintenance comments. 169 tracked historic code/assets predate the one-year cutoff; 55 older Python paths are identified and 24 legacy-reference Python scripts fail syntax parsing. See the CSV and LEGACY_AGE_REVIEW documentation.
- Next agent: read current remote HEAD, ROADMAP.md, MODERNIZATION_STATUS.md and LICENSING.md first. Preserve dirty older local checkouts. Review age-prioritized legacy modules individually, expand genuine authorized capture tests, maintain cross-platform CI and update handoff after each verified checkpoint.

## Older-than-one-day file review continuation — 2026-10-08

- Worktree: ~/projects/Subterfuge-Framework-one-day-audit-20261008 (isolated clone, baseline 060ae24). Old dirty checkouts retained untouched.
- Examined 104 tracked files with last commit >24 hours before review. 37 first-party templates/configs annotated without executable changes; 8 unreferenced AppleDouble sidecars removed, 59 resources intentionally preserved. See STALE_24H_REVIEW_2026-10-08.md and FILE_REVIEW_OLDER_24H_2026-10-08.csv for every path, checksum and rationale.
- Added tests/test_stale_file_review.py and included both review documents in the sdist manifest and archive auditor. **Do not claim these comments restored old functionality.**
- Before continuing, verify the latest published feature SHA, run fresh checkout unit tests, Node report QA, wheel/sdist content audit and six-platform GitHub Actions. No master merge, force-push, license change or history rewrite without owner approval.

## Definitive validation of the 24-hour legacy audit

- Published branch commit `b6864e3376c5eb59329e0120b8de0704d9cfd434` is the verified historical-maintenance checkpoint; it does **not** supersede the previously recorded last functional-feature commit `d8bb5b8`.
- Reviewed 104 paths: 37 safe first-party legacy status annotations, eight obsolete AppleDouble files removed (history preserved), 59 excluded from automatic changes, including GPL and third-party source, historical payloads and 45 intact decodable images/icons.
- `FILE_REVIEW_OLDER_24H_2026-10-08.csv` contains one record per file and SHA-256 before/after; `STALE_24H_REVIEW_2026-10-08.md` contains the decision matrix. `tests/test_stale_file_review.py` checks the recorded disposition and snapshot integrity.
- Direct independent Git archive validation of the published commit: 103 unittest cases discovered (102 successful, 1 conditional Git-metadata skip); Node browser-report validator passed; wheel and sdist built and artifact audit passed (18 / 63 archive members).
- GitHub Actions [run 37850134395](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37850134395) passed six out of six platform jobs. Do not confuse these documentation-only old-file annotations with fully ported legacy functionality.
- Next agent: read current remote HEAD, ROADMAP.md, MODERNIZATION_STATUS.md, MIGRATION_MATRIX.md and LICENSING.md; prioritize actually supported current code and safe historical replacements, preserve GPL/attribution, and avoid touching master unless owner explicitly authorizes.

## 2026-10-09 archival reorganization continuation

- Before-change work branch head: `8c8f7f347b4651d064516758ef4c9abf9495cacf`. Pre-change preserved on branch `archive-legacy-original-2026-10-09`. A dedicated clean worktree was created at `~/projects/Subterfuge-Framework-stale-complete-20261009`; other prior worktrees remain untouched.
- Local organization: moved 190 complete old framework files beneath `legacy/historical-framework-2015-2016/` with exact content hashes preserved, and moved complete root GPLv3 COPYING text to root LICENSE, leaving a new pointer at COPYING. Root LICENSE is protected by .gitattributes, retains SHA-256 8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903 and remains GPL-3.0-or-later in package metadata.
- Source docs and tests now use a 191-row relocation map and preserve prior 24-hour old-file review records as *historical snapshots*, not new path assertions. Modern packaged wheels/sdists exclude the historical subtree.
- Validation before publication: 105 Python unit tests discovered (104 successes, 1 expected skip), Node offline report QA passed; wheel/sdist audit passed (18/66 file entries). The modern runtime is still 2.0.0a2 alpha. Renames are not functional Python 3 ports.
- Next agent MUST publish staged modifications via connector atomic tree, then re-fetch the published branch and verify tests, package integrity and per-file last-touch dates. Check six-platform CI. Preserve archive branch, license, Git history and original copyright notices; do not merge master without owner approval.

### Local verification of the owner-requested master cleanup

- Started from the published modernization checkpoint f50bd4a, already fast-forwarded into master by explicit owner authorization (79 commits).
- Removed 193 legacy files from the maintained tree while leaving the original archive branch archive-legacy-original-2026-10-09 unchanged.
- Regression suite on Kali/Linux Python 3.14 discovered 108 tests: 106 passed, two skipped by design (historical source no longer present). The Node saved-report validator accepted five valid and rejected ten malformed fixtures.
- Wheel and source distribution built successfully; the artifact checker found 18 wheel and 67 source members, **no old framework files**, and the byte-identical original GPL-3.0 text in wheel metadata.
- Maintained current project sources under src/subterfuge/ and the root Python3 CLI; no old privileged Django/SSLStrip modules restored.
- Publication and CI confirmation will be recorded in a follow-up checkpoint after the exact new Git SHA exists on GitHub.
