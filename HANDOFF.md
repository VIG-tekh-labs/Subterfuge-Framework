# Subterfuge Framework — verified continuation handoff

**Date:** 2026-10-08 (Europe/Brussels)  
**Repository:** https://github.com/VIG-tekh-labs/Subterfuge-Framework  
**Working branch:** `modernization-2026-10-08-continuation`  
**Last fully validated feature commit:** `cf49be2d85d3764649677cc5dbe738aa68832374`  
**Development version:** `2.0.0a2` (alpha; NOT full historical restoration)

## Verified results at this checkpoint

- The published feature branch was fetched into a fresh archive and passed **89** Python unit tests, with **one test skipped** in the archive because Git metadata is absent. All 89 passed in a Git checkout with editcap installed.
- Wheel build passed in the fresh archive; previously examined wheel and source archives exclude historical interception source, private PEM, secrets, logs and SQLite databases.
- **GitHub Actions run 37830132711 passed all six jobs:** Linux/Python 3.11–3.14, Windows/Python 3.12 and macOS/Python 3.12.
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
