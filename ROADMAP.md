# Maintenance roadmap

## Verified default-branch cleanup — October 9, 2026

- **Final active code commit:** 9a986a148eb34cf74596df8b6d2adbfa34714ad8. The owner explicitly approved fast-forwarding modernization into master; the 79 earlier commits were applied without a force push.
- **Removed from the active GitHub tree:** 193 historical files in legacy (Django, Twisted/SSLStrip, UI assets, old setup/updater). A fresh clone of master confirms **63 tracked files and zero legacy paths**.
- **Preservation:** The original source and authorship are on the separate archive-legacy-original-2026-10-09 branch and in Git history. No history rewriting or relicensing occurred; 2015 code was not made functional.
- **Fresh checkout tests:** 108 Python cases discovered; 106 passed, 2 expected skips for absent historical source. Node saved-report validation accepted 5 valid and rejected 10 malformed fixtures.
- **Distribution:** wheel has 18 members, sdist has 67 members; both exclude the old legacy tree. The original GPLv3 license hash remains 8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903.
- **GitHub Actions:** [run 37858737482](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37858737482) passed all six jobs on Linux (Python 3.11–3.14), Windows and macOS (Python 3.12).
- **Still incomplete:** Version 2.0.0a2 alpha; old interception functionality remains unported. Further real-device capture, diverse PCAPNG, keyboard accessibility and provenance/legal review are needed.
- **Continuation:** Work from master; the separate modernization branch is synchronized to the same latest revision. Read ROADMAP and HANDOFF before new changes. No pull request needed for this cleanup.


## FINAL MAIN-BRANCH CLEANUP — October 9, 2026

- The owner explicitly authorized applying modernization to the default branch master. Master fast-forwarded without force from 4bc3c2e to f50bd4a (79 commits).
- To remove the 10–11-year-old files from the active GitHub tree, all 193 tracked files in the legacy directory were deleted from the maintained branch (190 older framework files, archive README, original update.py and setup.py).
- The separate branch archive-legacy-original-2026-10-09 preserves the old source, history and copyright attribution. No history rewrite, force push, archival branch deletion or relicensing was performed.
- The active Python 3 runtime remains under src/subterfuge; it is version 2.0.0a2 alpha and does not restore unported historical interception features.
- The original complete GPLv3 text remains byte-for-byte unchanged in LICENSE, with COPYING as a pointer. Historical relocation maps remain documentation, not active source paths.
- Verify Python/Node regression tests, wheel and source archive hygiene, and six-platform CI after this cleanup. Synchronize both modernization and master through non-forced fast-forward, then verify the GitHub default root has no legacy folder.
- Remaining modernization: diverse actual authorized PCAP/PCAPNG captures, safe Scapy passive lab testing, browser accessibility/keyboard checks, provenance and module-by-module feature migration decisions.



## POST-PUBLICATION VERIFIED CHECKPOINT — October 9, 2026

- Latest published archive/reorganization code commit: `1f21f9bc8cfafd4689eb781e6f83f7f335fcf8f5`, derived from baseline `8c8f7f3`. Complete historical tree remains preserved as branch `archive-legacy-original-2026-10-09`.
- **At 2026-10-09 01:03 Europe/Brussels, independently checked all 255 tracked files on the published modernization branch:** exactly **zero** have a last path-commit older than 24 hours; no path lacked commit information. This is a genuine relocation timestamp, **not** proof the archived 2015 code has been made compatible.
- A total of **190 historical framework files** moved byte-for-byte into `legacy/historical-framework-2015-2016/`; the separate GPLv3 COPYING text moved verbatim into root `LICENSE` with a new compatibility pointer at COPYING. The original GPL text SHA-256 remains `8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903`.
- Fetched that precise **published Git tree** SHA `36793967e59cc7e2f153c20fc1f89d4b8c8695fd` into a fresh archive and ran 105 unittest cases (**103 passed, 2 skipped** without Git metadata); Node report-schema checks accepted 5 valid and rejected 10 malformed reports. In the development Git worktree, 105 unittest cases discovered (**104 passed, 1 expected skip**). 
- Verified wheel and source distribution builds and packaging: 18 wheel entries, 66 sdist members; wheel contains byte-verified original GPLv3 license; archived historical directory excluded from both artifacts.
- GitHub Actions [run 37857219307](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37857219307) for `1f21f9b` completed **all six matrix jobs successfully**: Linux/Python 3.11–3.14, Windows/Python 3.12 and macOS/Python 3.12.
- **Default branch `master` is unchanged** at `4bc3c2ec439d6c978d5b51a3c9d310c39aed590e`. A user looking at GitHub's default master will still see old file history until they explicitly approve merging or changing the default branch. No public history rewriting or relicensing occurred.
- Next development priority is **real modernization**, not artificial timestamp editing: reproduce genuine authorized PCAP/PCAPNG captures; test optional local Scapy interfaces in a permitted isolated network; strengthen browser keyboard accessibility and saved report validation; classify historical modules for safe replacement or retirement; continue GDPR/privacy and third-party license provenance review. Do not claim interception feature parity while the package remains alpha `2.0.0a2`.

## CURRENT VERIFIED HANDOFF — October 9, 2026

- **Start with HANDOFF.md and MODERNIZATION_STATUS.md** for the exact branch, proven feature state, outstanding tasks and licensing/security caveats.
- Last fully verified functional commit: d8bb5b836b20046e13712beced1e03c7b5ee36c5, version 2.0.0a2 alpha.
- Cross-platform GitHub Actions run 37840748127: six Linux/Windows/macOS jobs successful.
- Latest clean feature archive: 100 unittest cases discovered, 99 passed and 1 Git-dependent test skipped; in a Git checkout all 100 passed. Browser schema, Chromium QA and distribution audit passed in the recorded checkpoints.
- The default GitHub master points to 4bc3c2e (earlier alpha), while the working modernization branch has progressed ahead of master. Do not confuse an old master commit date with an unpublished feature branch.
- FILE_AGE_INVENTORY_2026-10-08.csv lists **252** tracked paths at audit baseline ea23621; LEGACY_AGE_REVIEW_2026-10-08.md records 169 historic code/assets, 55 old Python references and 24 legacy syntax failures.
- **No full historical interception feature parity is claimed. Do not merge master, force-push or rewrite history without owner approval.**

Last checkpoint: 2026-10-08, Europe/Brussels.
Repository: https://github.com/VIG-tekh-labs/Subterfuge-Framework
Working reference branch: modernization-2026-10-08-continuation; master is the older baseline.
Publication parent: 634979fdb8cc71f309bb168706906be7a6817e61.

## Start here

The modern assessment runtime is 2.0.0a2 (alpha). It is an installable alpha, not complete historical feature parity. Use README.md for installation and CAPABILITIES.md for the migration matrix. Historical source remains in the repository and is not imported by the modern package. No replacement repository was created.

## Owner requirements

- Restore usability on current machines and review every historical capability, not ARP alone.
- Keep documentation, instructions, comments and commit messages in English.
- Preserve authorship and license; add no generated branding or signatures.
- Automatically update this roadmap after development steps, checks, publication, failures and before interruption.
- Keep checkpoint bookkeeping in the background. Report newly updated directories once.
- Count functional modernization separately from cosmetic maintenance.
- Do not claim full compatibility, released status or feature parity without checks.

## Functional changes in this checkpoint

- Publish src/subterfuge, CLI and a loopback-only dashboard.
- Add pyproject.toml packaging for Python 3.11+, without core runtime dependencies.
- Replace the root privileged Python 2 installer with a setuptools shim; preserve the previous installer in legacy/setup.py.
- Import classic PCAP with Ethernet, VLAN and Linux cooked headers; consolidate ARP conflicts and bound input/resource sizes.
- Import standard Nmap XML including the normal plain DOCTYPE; reject XML entities, external DTDs and excessive nesting.
- Retain IPv4/IPv6 inventory, ports, service products/versions and OS evidence.
- Add service transport review items with explicit uncertainty about STARTTLS, redirects and policy.
- Add inspect-tls: normal certificate-verified TLS connection, negotiated cipher/protocol and expiry review.
- Bound dashboard uploads; validate Host, Origin and session token; use CSP and local assets.
- Add atomic private JSON exports, optional passive Scapy capture and explicit bounded Nmap host discovery.
- Add 50 regression tests and a CI matrix requesting Linux/Python 3.11–3.14 plus Windows/macOS/Python 3.12.

## Actual validation

- Linux, Python 3.12.14: all 50 tests passed from source and against an installed wheel.
- Wheel built using setuptools 84.0.0 and installed into a fresh venv without package-index access.
- Installed doctor and synthetic demo passed outside the source directory.
- Local TLSv1.3 handshake passed using a temporary trusted localhost certificate; expiry finding observed.
- The first additional TLS fixture encountered a server-side broken pipe from TLS session ticket timing. Disabling tickets in the fixture resolved the race; certificate verification was not disabled.
- No external scan, live capture or historical interception script was executed.
- Dashboard HTTP boundary tests passed; visual browser validation is still pending.
- CI results, Windows/macOS behavior and Python versions other than 3.12 remain unverified.

## Historical capabilities

CAPABILITIES.md identifies ARP interception, DHCP race, WPAD/NetBIOS, wireless AP, SSLStrip/proxy, credential/session handling, HTTP injection and other plugins. These historical implementations are retained, not restored. POODLE, Heartbleed and SSLv3 downgrade were advertised as future roadmap items; dedicated modules were not found in inspected paths. New TLS inspection is a separate assessment function, not a replacement claiming interception parity.

## Exact next actions

1. Verify published paths, branch head and CI results. If workflow publication is rejected, retain the prepared workflow and record the exact error.
2. Perform dashboard browser QA and fix any usability problems.
3. Add PCAPNG import with malformed-input and resource-limit regressions.
4. Add passive DHCP and name-resolution evidence analysis with isolated fixtures.
5. Review historical proxy/plugin contracts against modern TLS and browser protections before porting them.
6. Validate Scapy/Nmap adapters in an isolated test network; they remain optional and unverified here.

## Previous checkpoints

Commit d917e53bfe46647495794c2c8897789c61c2e94e published the initial documentation.
Commit 634979fdb8cc71f309bb168706906be7a6817e61 added 71 comment-only markers and 26 directory notes; no functional fixes or dependency upgrades were included. Filesystem touch is not tracked by Git.
Earlier GitHub writes returned 403 Resource not accessible by integration; installation/reconnection subsequently restored publishing.

## Continuation discipline

Read the current remote head before writes. Preserve unrelated work and use an expected-head lease. Keep separately prepared working copies intact; one older draft exists at /workspace/scratch/977d15b140db/Subterfuge-Framework and may contain unpublished changes. The source used for this checkpoint was validated independently. Never overwrite another working copy as part of reconciliation. Record actual checks and remaining gaps; maintain an explicit alpha status.

## Continuation checkpoint — 2026-10-08 (new session)

- Verified the connected GitHub integration can read this repository, its README, ROADMAP, CAPABILITIES, MAINTENANCE, packaging metadata and source.
- Verified master HEAD at the start of this session: `4bc3c2ec439d6c978d5b51a3c9d310c39aed590e`.
- Created dedicated continuation branch `modernization-2026-10-08-continuation` from that exact commit; master was not modified.
- Remote Desktop Commander device `eden` was offline when checked. No dependencies were installed and no runtime tests were executed in this session; previous 50-test checkpoint remains historical evidence only.
- Confirmed PCAPNG import remains absent; `src/subterfuge/analysis.py` explicitly rejects PCAPNG. Preserve input limits, parsing safety and synthetic test coverage during implementation.
- Immediate next action: obtain an available isolated execution environment, implement and test bounded PCAPNG parsing with malformed-input fixtures, run the complete regression suite, inspect GitHub CI, and record the results before publication or feature claims.
- Documentation rule: update this roadmap after every verified checkpoint; only claim tests that were actually executed. Do not merge continuation into master without owner authorization.

## PCAPNG implementation checkpoint — 2026-10-08

- Commit `cc247f214b0a43fba41b50b24d79f800bf3fe400` adds an initial PCAPNG section/interface/enhanced-packet reader to `src/subterfuge/analysis.py` on the continuation branch.
- Status: **UNTESTED DRAFT**. Desktop Commander `eden` remains offline and direct Git clone was blocked by DNS in the fallback environment. Do not advertise PCAPNG support as validated or merge this branch.
- Next action is mandatory: review the parser, simplify packet-ignore accounting, add PCAPNG fixtures and malformed-input tests, execute the full regression suite, and correct any defects before release.

## Continued parser review — 2026-10-08

- Commit `3e3abb5933b50099614b7bee9cd8686b4e3c7c1d`: simplified PCAPNG ignored-packet accounting.
- Commit `1f76782f1729807cda69fafd9701e0442b109c54`: added `tests/test_pcapng.py` with synthetic endian, malformed-length, missing-interface and non-ARP cases.
- **Not validated**: no Python execution environment was available through Desktop Commander. Test files were committed but have not run; all PCAPNG work remains draft. Do not merge or release.
- Next: run `python -m unittest discover -s tests -v` in a Python 3.11+ venv; correct failing fixtures/parser; verify dashboard PCAPNG import and CI; inspect historical modules one at a time. Keep `master` unchanged.

## Verified Python 3 modernization checkpoint — 2026-10-08

- Reconnected Remote Desktop Commander device `eden`; cloned the continuation branch to an isolated directory under `~/projects/Subterfuge-Framework-modernization`. No historical system installer was executed.
- Python 3.14.7, pip 26.1.2 and Git 2.53.0 confirmed on the device.
- Corrected malformed escaped-byte literals in `tests/test_pcapng.py`; all PCAPNG tests now pass on the local machine.
- Retired the Python 2/SVN-based root `update.py` (which used a legacy network version socket and system-wide configuration). Preserved its original source in `legacy/update.py`; the replacement Python 3 entry point is informational and performs no network calls or privileged modifications.
- Added `tests/test_updater.py` to verify the replacement updater remains read-only.
- **Executed checks:** 56/56 unittest cases passed; Python compileall passed; isolated `pip install .` built and installed wheel `subterfuge_framework-2.0.0a1`; installed CLI version and synthetic demo smoke checks passed.
- **Remaining limitations:** historical interception/proxy/plugins remain unported; PCAPNG has only synthetic test coverage, not comprehensive real-capture validation; no network interception or active attack modules tested; Windows/macOS and CI results not verified.
- Next: test real PCAPNG fixtures and multiple sections/interfaces, perform browser QA, inspect historical passive DHCP/name-resolution logic for safe Python 3 replacements, and verify CI before proposing a merge. Keep master untouched pending owner approval.

## Passive name-resolution and PCAPNG UI checkpoint — 2026-10-08

- Examined historical `utilities/dhcptools.py` and `utilities/nbtools.py`: both depend on Python 2 syntax, old Scapy behavior, hard-coded addresses and active packet transmission. These are not compatible or safe to run unchanged. Original sources remain preserved for review.
- Added `src/subterfuge/name_resolution.py`: dependency-free, offline-only NBNS query datagram decoding, including WPAD observation without spoofing or packet transmission. Added `tests/test_name_resolution.py`. This is a library parser, not yet integrated with full PCAP capture workflows.
- Expanded PCAPNG regressions for multiple sections of differing byte order, timestamp resolution options and malformed option/packet limits. Updated dashboard input and text to accept experimental PCAPNG uploads, and added an HTTP import test.
- Verification on Desktop Commander `eden`, Linux Python 3.14.7: 63 tests passed in local worktree; 63 tests passed again from a fresh archive of the published branch commit `14b97dd`. No external network testing or active interception occurred.
- Files updated: `src/subterfuge/static/index.html`, `tests/test_pcapng.py`, `tests/test_web.py`, `src/subterfuge/name_resolution.py`, `tests/test_name_resolution.py`.
- Remaining: integrate passive name-resolution observations into bounded PCAP processing, add passive DHCP parsing with fixtures, browser visual QA, actual capture validation, review historical plugin contracts, inspect CI results. Do not claim historical parity or merge into master.
- Existing working directories contain uncommitted changes; keep them intact and use fresh archives/worktrees for remote-branch verification.

## DHCPv4 passive analysis checkpoint — 2026-10-08

- Added `src/subterfuge/dhcp.py`: offline-only bounded DHCPv4/BOOTP payload inspection, DHCP message-type and server-ID metadata, and presence-only WPAD option 252 review. No DHCP response generation, transmission, privileged network operation or option-252 contents retention.
- Added `tests/test_dhcp.py` for synthetic offer, server identifier, WPAD indicator, and malformed input.
- Local verification: 66 unittest tests passed on Linux/Python 3.14.7 using Desktop Commander device `eden` before publication. Full legacy module parity remains incomplete.
- Publication: new DHCP module and tests committed to the continuation branch; `master` unchanged.
- Next exact actions: verify fresh archive of published branch passes 66 tests; integrate passive DHCP/NBNS evidence into PCAP/PCAPNG packet processing with strict bounds and no payload retention; run browser QA and CI. Never run legacy active DHCP spoofing scripts as a routine test.

## Offline UDP evidence dispatch checkpoint — 2026-10-08

- Added `src/subterfuge/udp_evidence.py` with bounded Ethernet/VLAN/IPv4 UDP frame recognition. It delegates eligible UDP payloads to the passive DHCPv4 and NBNS decoders; non-UDP and fragmented IPv4 are ignored. No packet transmission or persistent payload storage.
- Added `tests/test_udp_evidence.py` with synthetic DHCP, WPAD NBNS, truncated frame, non-UDP and fragmentation cases.
- Local Linux/Python 3.14.7 regression suite: **69 tests passed** before publication.
- This dispatcher is an **independent library helper**. It is not yet wired into the `analyze_pcap` or PCAPNG aggregate reports; do not claim integrated capture-level DHCP/NBNS support.
- Next: implement bounded aggregation into capture reports without changing existing ARP evidence semantics; validate fresh published checkout and dashboard UI; review protocol edge cases and CI.

## Repository-wide modernization and licensing audit — 2026-10-08

- Inventory of all 293 baseline tracked files created in `FILE_AUDIT.md` (automated category-level triage, not manual proof of each module).
- Python 3.14 syntax sweep: 82 tracked Python sources; 56 AST-parse; 26 fail due to legacy Python 2 syntax/indentation.
- Identified legacy Django, Twisted, Scapy and jQuery; the active Python 3 package remains Django/Twisted-free.
- Preliminary license review in `LICENSING.md`: GPLv3 root and GPL-3.0-or-later active-package metadata; explicit historical GPLv2-only notice in `modules/harvester/ftp_password_sniffer.py`; historical SSLStrip modules have GPLv3-or-later notices. **Do not assume blanket relicensing eligibility.**
- Historical public repository carries a private-key PEM, Django SECRET_KEY, credential file and databases. Current branch cleanup prepared (58 tracked artifacts); original Git history remains exposed. See `SECURITY.md` for rotation and remediation.
- Implemented bounded passive DHCP and NetBIOS aggregation in classic PCAP and PCAPNG reports, with Ethernet/VLAN and Linux cooked capture support; dashboard displays observation groups.
- Last local source regression: 76 tests passed on Linux/Python 3.14, prior to packaging/browser validation of this checkpoint.
- Next: validate installed wheel, source distribution, Chromium dashboard rendering, CI, and complete publication of cleanup and tests. Retain alpha status. Continue historical module-by-module modernization without claiming full parity.


## Installation, browser and packaging validation — 2026-10-08

- Python 3.14.7, isolated pip wheel creation **passed**. The wheel contains
  only the modern package and packaging metadata (18 entries), with no
  historical Django/Twisted modules or sensitive artifacts.
- Isolated source distribution **built** and inspected (46 entries before the
  manifest documentation expansion); no legacy module tree, compiled `.pyc`,
  PEM, credential file or database was found in the archive.
- Optional Scapy 2.8.0 was installed in the virtual environment; 76 offline
  regressions still passed. Live Scapy packet capture was **not** executed.
- A real Chromium headless process loaded the loopback dashboard (HTTP 200),
  returned a DOM containing the passive-evidence panel and generated a
  screenshot. Manual visual/accessibility QA remains to be completed.
- Preliminary technical security and provenance notes recorded in
  `AUDIT.md`, `SECURITY.md`, `LICENSING.md` and `FILE_AUDIT.md`.
- Next: rerun builds/tests after expanded source manifest, publish the branch
  atomically, verify the published content, investigate GitHub CI status,
  then extend PCAPNG fixtures and the Nmap/TLS report experience.
## Published commit and cross-platform CI verification — 2026-10-08

- **Published commit:** `b0027fb39b7cbd2877a798fcc2004d311deef5c6` on continuation branch; 58 generated/sensitive legacy artifacts removed from this branch without rewriting historical commits. `master` remains unchanged.
- A fresh archive of the remote published commit passed **76/76** Python regression tests on Linux/Python 3.14.7.
- The published commit built both a wheel and a source distribution; inspected archives held 18 and 52 entries respectively, with **no** historical module trees, tracked private PEM, credentials, SQLite databases, logs or compiled Python 2 cache artifacts.
- The installed published wheel passed CLI `--version`, `doctor` and `demo` checks outside the source checkout in a fresh virtual environment.
- **GitHub Actions run [37826972168](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37826972168) completed successfully.** Six jobs passed: Linux/Python 3.11, 3.12, 3.13 and 3.14; Windows/Python 3.12; macOS/Python 3.12. Live adapters and full historical plugin functionality were not part of these CI checks.
- Security caveat: older public commits and the unchanged `master` still contain historical artifacts. Owners must rotate any real exposed secrets; coordinate explicitly before a disruptive history rewrite.
- Next: perform interactive browser QA of import/export and report rendering, inspect historical modules and third-party assets, add isolated QA tests for report evidence, document and validate each further checkpoint, and keep alpha status until feature readiness is supported.


## TLS dashboard integration and alpha-2 version — 2026-10-08

- Converted the existing CLI-only TLS endpoint inspection into an explicit
  same-origin, token-authenticated dashboard form and bounded JSON API.
  The operation still makes only one certificate-verified TLS connection.
- Added `test_tls_endpoint_post_and_report`,
  `test_tls_post_rejects_bad_requests` and HTML assertions.
- Linux/Python 3.14 local source regression: **78/78 tests passed**.
- Chromium/Puppeteer clicked the new form with an invalid URL-form hostname;
  it displayed the expected validation error with **no browser JS errors**.
  No external TLS endpoint was contacted in this interactive test.
- Version bumped to `2.0.0a2` in packaging and runtime metadata, still alpha.
- Before release: publish this feature commit, build/test the published wheel
  and source distribution, verify GitHub Actions on all six configured runners,
  and update this file with the results.
- Historical interception modules remain unported. Never infer that
  upgrading Django/Twisted would make deprecated downgrade mechanisms safe
  or reliable on contemporary browsers.
## Alpha 2 published and validated — 2026-10-08

- Feature commit `9862b19640e797c6f8d3548f0f90227db2dd8e39` published on the continuation branch. Runtime and package version: `2.0.0a2` (alpha).
- Published-branch archive passed **78/78** regression tests on Linux/Python 3.14.7. Built wheel (18 entries) and source distribution (52 entries); checked no tracked private PEM, compiled `.pyc`, logs, historic `sslstrip/`/`modules/` trees or credential files.
- Browser interaction validated via Chromium/Puppeteer: the new TLS form rejected an invalid URL-form host with the expected error; **no JavaScript exceptions** occurred. No external endpoint was contacted.
- **GitHub Actions run [37828069880](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37828069880) completed successfully** across all six jobs (Linux/Python 3.11, 3.12, 3.13, 3.14; Windows and macOS/Python 3.12).
- Historical feature parity remains incomplete; no root-only attack scripts or live network adapters were validated. `master` is unchanged. Further work: module-by-module migration plan, real-capture PCAPNG validation, optional adapters in authorized lab, UI accessibility review, and security/license remediation.


## Optional Nmap service inventory and historical migration matrix — 2026-10-08

- Added CLI `scan-services` to complement host discovery and Nmap XML import.
  It requires an explicit single IPv4/IPv6 address, accepts at most 32 unique
  TCP ports, a bounded timeout and optional JSON report output.
- It invokes modern Nmap with TCP connect (`-sT`), no ping (`-Pn`), light
  version detection (`-sV --version-light`) and one retry cap. No external
  scans were performed during this checkpoint; all adapter tests mock Nmap.
- Added `tests/test_services.py` with validation, IPv4/IPv6, error paths
  and CLI dispatch coverage. **83/83** tests pass locally on Linux/Python 3.14.
- Added `MIGRATION_MATRIX.md` describing each historical module category,
  active status, modern equivalent (where one exists), remaining gaps and
  acceptance criteria.
- Updated readme, capability matrix and security notes. Current development
  version remains `2.0.0a2`; still an alpha without historical parity.
- Next: publish, verify clean checkout/wheel/sdist, inspect all six GitHub
  Actions matrix results, then validate optional adapters in a private
  authorized test network. Keep `master` unchanged.

## Optional live passive ARP/DHCP/NBNS capture — 2026-10-08

- Added `capture-protocols` CLI command for one explicitly selected network
  interface, bounded duration and packet count, with private JSON export.
- Its Scapy adapter passively analyzes ARP and selected UDP DHCP/NetBIOS
  metadata without packet injection, firewall changes or raw UDP payload
  retention. Existing ARP-only `capture` remains available.
- Added `EvidenceAccumulator.observe_datagram` for bounded Scapy
  datagrams and `tests/test_live_protocols.py` exercising synthetic
  ARP/DHCPv4/NBNS packet callbacks and explicit CLI dispatch.
- Local source test suite: **86/86 tests passed** on Linux/Python 3.14.
- IMPORTANT: real live interface capture has NOT been verified in this
  checkpoint; do not claim it is operational across operating systems.
- Next: verify Scapy optional installation, publish this commit, rebuild
  clean wheel/sdist, check all six GitHub CI runners and test real capture
  only on an explicitly authorized isolated interface.

## Artifact hygiene, editcap interoperability and loopback QA — 2026-10-08

- Added `tests/test_repository_hygiene.py` to prevent re-introduction
  of tracked private PEM/keys, logs, compiled Python bytecode, legacy DB/
  credential artifacts or hard-coded legacy Django secrets.
- Added `tests/test_external_capture_writer.py`: optional format test
  produces a PCAPNG with Wireshark `editcap` and verifies that our decoder
  reproduces the classic-PCAP ARP evidence. The test skips when `editcap`
  is missing.
- Added reproducible `qa/loopback_nmap_smoke.py`, which launches one
  ephemeral server on `127.0.0.1`, scans that loopback port only and
  shuts down. It passed locally with installed Nmap. No LAN/Internet scan.
- Local regression suite: **89 tests passed** on Python 3.14/Linux, including
  optional editcap interoperability. Source tests from the prior checkpoint
  on `c99bbe4`: 86/86 passed; its six GitHub Actions jobs all completed
  successfully at [run 37829286881](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37829286881).
- Next: publish these QA artifacts, validate published wheel and all six CI
  jobs, then plan real captures on authorized test interfaces and migration
  of remaining non-privileged historical functions.

## Browser-only saved-report import — 2026-10-08

- Added dashboard ability to reopen version-1 JSON reports from a local file,
  validating top-level schema, arrays, object shapes and 16 MiB file-size
  limit. Existing report export remains unchanged.
- No JSON import endpoint or server persistence was added: saved report data
  stays in the browser until the user exports or reloads; the historical
  Django database is not required.
- Chromium/Puppeteer end-to-end QA: loaded synthetic demo, downloaded JSON,
  reloaded JSON from local file, confirmed host inventory was restored,
  then rejected a malformed host record without JS exceptions.
- Python source regressions: **89 tests passed** on Linux/Python 3.14.
- Previous artifact-hygiene commit `16ae612` passed all six GitHub CI jobs
  at [run 37829668360](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37829668360).
- Next: publish/report branch checks, verify all six new CI jobs; continue
  accessibility/usability review and real-capture validation before release.

## Full-modernization and licensing review checkpoint — 2026-10-08

- Re-read current `HANDOFF.md`, `AUDIT.md`, `MIGRATION_MATRIX.md`, `LICENSING.md` and roadmap. Found **alpha 2.0.0a2** and a more recent verified checkpoint than the older 69-test record. Handoff records 89 passing tests plus one skipped in source archive, six cross-platform CI jobs, browser QA, `editcap` interoperability, and a loopback-only Nmap smoke check. These are recorded previous validation outcomes, not newly rerun in this checkpoint.
- Historical audit lists 26 Python 2 syntax failures among 82 original Python files and obsolete Django 1.x / Twisted / jQuery entry points. Those files are outside the active `src/subterfuge` runtime and should not be globally rewritten without feature-by-feature acceptance criteria.
- Desktop Commander `eden` connected. A separately cloned worktree unexpectedly contained extensive modified/deleted files while other modernization activity had progressed; treat it as potentially concurrent work. **Do not reset, clean, force-push, or overwrite**. A test invocation in that worktree reported 76 passed, but its checkout was not clean and is **not** accepted as a reliable replacement for the more recent 89-test handoff.
- Updated `LICENSING.md` at commit `1773c391` with a rights-holder/provenance decision gate. GPL declarations remain; GPLv2-only legacy material needs separate distribution review. Source reference: https://www.gnu.org/licenses/gpl-faq.en.html.
- Next: obtain a stable clean snapshot of the latest published branch; compare exact SHA and handoff; run reproducible tests/wheel/sdist checks; inspect secrets in historical Git history, dependency SBOM, accessibility, passive capture edge cases, and feature-by-feature legacy migration; publish only verified changes with this roadmap updated. Keep `master` unchanged.

## Fresh archive validation after licensing review — 2026-10-08

- Fetched published continuation commit `ce92dfb`, exported an isolated Git archive to `/tmp/subterfuge-verify-fQ1u9i`, and ran independent Linux/Python 3.14 tests.
- **89 tests passed; one Git-metadata-dependent test skipped** in the archive. `python3 -m compileall -q src/subterfuge` exited successfully. Both commands returned exit code 0.
- This independently confirms the published code in this snapshot; it does not validate historical interception, real live interfaces, external networks, or comprehensive feature parity.
- Next: new changes must use a new clean checkout or archive, add targeted tests, and preserve concurrently modified worktrees. Prioritize provenance/security compliance, passive capture interoperability, and accessibility before any release.

## PCAPNG block compatibility and truthful timestamps — 2026-10-08

- Starting remote branch HEAD: `2add3c2861dc14a8aa4148f3da8fd186a7544037`. Used a **new clean checkout** on Desktop Commander device `eden` at `~/projects/Subterfuge-Framework-hardening-20261008`, preserving other possibly concurrent worktrees.
- Modern parser `src/subterfuge/analysis.py` now recognizes PCAPNG Enhanced Packet Blocks (type 6), obsolete Packet Blocks (type 2), Simple Packet Blocks (type 3), and interface timestamp offset (`if_tsoffset`, option 14). It retains previous ARP and passive DHCP/NBNS evidence bounds.
- Simple Packet Blocks contain no capture timestamp: host `first_seen`/`last_seen` are represented as JSON null when no timed evidence exists; when timed and untimed observations are mixed, the known timestamps remain and a partial-timing warning is included. Never synthesize epoch times.
- Added `tests/test_pcapng_packet_blocks.py` (endian, simple/obsolete blocks, DHCP passthrough, timestamp offset, invalid/missing interface/malformed options), dashboard integration regression in `tests/test_web.py`, updated local UI copy, README and CAPABILITIES.
- **Verification in the development checkout:** 97/97 tests passed under Linux/Python 3.14.7, `git diff --check` and `compileall` passed, wheel build passed.
- **Independent published-branch verification:** fetched exact commit `1581fefff359bcf6eca7b7727005848293944b9a`, exported fresh Git archive to `/tmp/subterfuge-pcapng-published-dQMYAc`, executed 97 tests (all passed; one Git-dependent case skipped without repository metadata), compiled the package, built a wheel, and inspected 18 wheel members with no historical/secret/credential paths detected.
- Status: modern PCAPNG paths have expanded **synthetic** and package coverage; diverse real-device PCAPNG corpus and refreshed cross-platform CI for this feature commit are still **pending**. Historical active interception modules remain unported and unvalidated. Version remains `2.0.0a2` alpha; do not merge master.
- **Next exact actions:** verify current GitHub Actions run against new commit, expand real `editcap` corpus and PCAPNG malformed-input fuzz boundaries, improve local dashboard accessibility and invalid report handling, then reassess capture feature support and release readiness. Keep this roadmap and HANDOFF.md current before interruption.

## PCAPNG metadata-flood hardening — 2026-10-08

- Review found the original `MAX_PACKETS` guard did not count unknown/miscellaneous PCAPNG blocks. A 64-MiB crafted file could require millions of metadata-only block iterations without producing packets.
- Introduced `MAX_PCAPNG_BLOCKS = MAX_PACKETS + 50_000` and enforce the total block count, including unknown block types; added `test_excessive_unknown_blocks_are_bounded` in `tests/test_pcapng_packet_blocks.py`.
- Published code commits: `e55d60f7f710f2d6ffad8154e70ac96d4c3d889d` (implementation), `cf49be2d85d3764649677cc5dbe738aa68832374` (regression). Linux/Python 3.14.7 local test suite: **98/98 passed**.
- Fetched published head `cf49be2d85d3764649677cc5dbe738aa68832374`, exported a clean Git archive and independently verified **98 tests passed (one Git-metadata-dependent test skipped)**, plus Python `compileall`; both exited 0.
- GitHub Actions run [37838822992](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37838822992) for earlier feature commit `1581fef` was explicitly checked: **all six** Linux/Windows/macOS jobs completed successfully. Runs for newest metadata-limit commits were still **in progress** when last checked; do not inherit previous results as proof of those commits.
- Next: verify latest GitHub Actions run for the metadata-bound change; expand malformed-input differential corpus and fuzz case coverage, test downstream UI with untimed PCAPNG; review strict import validation and full legacy migration decisions. Maintain alpha status and keep master unchanged.

## Browser saved-report validation and accessibility hardening — 2026-10-08

- Issue: the existing client-side `validateImportedReport()` only checked outer array/object shapes. Malformed nested ports, MAC arrays, timestamp types and passive evidence could pass validation and then throw during `render()`.
- Implemented bounded, type-safe nested validation for report metadata, statistics, hosts/addresses/MACs/ports, optional numeric-or-null times, findings, warnings and DHCP/NBNS observation records. Invalid imports are rejected *before* replacing the currently displayed valid report; report contents continue to render via safe text nodes.
- Added `qa/browser_report_validation.mjs` (dependency-free Node.js): **five valid fixtures accepted**, including genuine CLI demo and Nmap XML exports; **ten malformed fixtures rejected**. Integrated the Node harness into the six-platform GitHub Actions workflow. Added optional `qa/browser_report_smoke.cjs` using **sandboxed** Chromium/Puppeteer solely for local QA; no Puppeteer production dependency.
- Interactive Chromium QA: reopened valid PCAPNG JSON with missing timestamps, retained the saved warning, rejected malformed MAC array import, preserved prior valid report and observed zero uncaught JavaScript page errors. Documentation updated in `README.md` and `SECURITY.md`.
- Verified published feature commit `ac3b754b926d682c6514a45aeff014f4226804e1` from fresh Git archive `/tmp/subterfuge-json-qa-Aj6RIz`: unittest discovered **98 tests, 97 passed and 1 Git-metadata-dependent test skipped**, Node harness passed, sandboxed Chromium QA passed and compileall exited 0.
- GitHub Actions [run 37839129084](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37839129084) for earlier PCAPNG metadata-bound commit `cf49be2` completed **success**; newly modified workflow run [37839864418](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37839864418) for `ac3b754` was **queued** at last inspection and needs a separate matrix-results check.
- No old dependencies (Python 2, Django 1.x, Twisted interception proxy or jQuery) were reintroduced. The modern runtime remains `2.0.0a2` alpha without full historical parity. `master` is unchanged.
- **Next exact steps:** verify six GitHub Actions jobs after workflow change; re-check wheel and source artifact hygiene; test additional malformed PCAPNG and real-device captures; review local dashboard accessibility and keyboard interaction; keep the migration/licensing inventories accurate without reactivating historical active interception modules as routine tests.

## Source-distribution and CI hygiene checkpoint — 2026-10-08

- Artifact review discovered the modern wheel and source archive excluded historical interception directories and known sensitive artifacts, but the source archive **omitted the QA scripts mentioned in README.md**. This made documented source-only validation unreproducible from an sdist.
- Updated `MANIFEST.in` to include `qa/*.py`, `qa/*.mjs` and `qa/*.cjs` in the sdist only. Added dependency-free `qa/audit_distributions.py` to inspect archive members, reject legacy/credential/key/database/log content, and assert expected runtime/license/handoff/QA files. Added `tests/test_distribution_manifest.py` to guard the policy.
- Expanded `.github/workflows/modern-runtime.yml` to build a source distribution with the isolated setuptools backend and audit **both** wheel and sdist across the existing six-platform CI matrix. Updated README.md with source-only audit instructions.
- First local attempt using `python -m build --sdist --no-isolation` failed because the development venv did not contain setuptools. This is an environment/build-mode mismatch, **not a source distribution test success**. Retried with normal isolated `python -m build --sdist`, which built correctly. The `build` frontend was installed **inside the dedicated development venv only**, not system Python or production dependencies.
- **Verification in developer checkout:** 99 Python unit tests passed under Linux/Python 3.14.7, `git diff --check` passed. New wheel and sdist built and passed the archive inspector.
- **Independent published branch verification:** fetched exact commit `d18dd998dc28d89d460271d2fe3945ad7a46966b`, exported a fresh Git archive, executed 99 unittest cases (**98 passed, 1 skipped** due to missing Git metadata), Node browser-schema QA accepted 5 valid cases and rejected 10 malformed ones, rebuilt wheel/sdist, and passed member inspection (**18 wheel members, 57 source members; zero forbidden paths**).
- GitHub Actions run [37839864418](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37839864418) for previous browser-validation feature `ac3b754` is confirmed **all six jobs successful**. New distribution-audit workflow [37840372524](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37840372524) for `d18dd99` was **still in progress** at last check; verify results before claiming cross-platform distribution-audit success.
- **Next exact actions:** check all six `d18dd99` jobs and fix any platform-specific archive issues; expand captured protocol fixture coverage and accessibility QA; reconcile outstanding unported historical features module by module; audit third-party notices and historical secret exposure with owner approval before any license change, history rewrite or release. Keep `master` unchanged and label the runtime `2.0.0a2` alpha until feature validation is sufficient.

## Accessible dashboard results and six-platform artifact CI checkpoint — 2026-10-08

- Updated modern dashboard `src/subterfuge/static/index.html`: added an accessible name to the host inventory table, explicit list semantics for passive DHCP/NBNS observations, audit findings and warnings, and matching list-item roles for dynamically created results.
- Added `tests/test_web.py::test_accessible_table_and_result_regions` and augmented the optional sandboxed Chromium smoke script to check the host inventory name and dynamically generated warning list semantics. No new production dependencies.
- Published code on the continuation branch through `d8bb5b836b20046e13712beced1e03c7b5ee36c5`. Linux/Python 3.14.7 development worktree: **100/100 tests succeeded**; sandboxed Chromium and Node saved-report checks passed.
- Independently fetched `d8bb5b8` into a fresh Git archive: unittest discovered **100 tests (99 passed, 1 skipped because Git metadata was absent)**; Node saved-report QA accepted 5 valid and rejected 10 malformed fixtures; Chromium opened an untimed PCAPNG JSON, preserved previous valid report on rejected malformed import, verified inventory/warning accessibility roles, and had zero uncaught JS page errors.
- Verified GitHub Actions run [37840372524](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37840372524) for distribution/audit feature commit `d18dd99`: **all six jobs** (Linux Python 3.11–3.14; Windows/macOS Python 3.12) completed successfully, including new wheel/sdist inspections. Latest UI accessibility run [37840748127](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37840748127) was **in progress** at last inspection; do not claim full matrix validation for `d8bb5b8` until checked.
- Historical Python 2/Django/Twisted sources remain reference-only, modern runtime is `2.0.0a2` alpha, licensing review is still provisional, and master has not been modified.
- **Next exact actions:** confirm latest `d8bb5b8` CI result, extend real-world PCAPNG/DHCP/NBNS sample corpus and malformed-input fuzzing, inspect accessibility with keyboard/screen-reader tooling, validate optional live passive capture only in an expressly authorized isolated environment, and progress migration-matrix entries with accurate verified/unsupported labels.

## Six-platform accessibility CI follow-up — 2026-10-08

- Verified GitHub Actions run [37840748127](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37840748127) for accessibility feature commit `d8bb5b836b20046e13712beced1e03c7b5ee36c5`: **all six jobs completed successfully** (Ubuntu/Python 3.11, 3.12, 3.13 and 3.14; Windows and macOS/Python 3.12).
- All modern features published up to this feature commit have now passed the GitHub Actions matrix. Documentation-only commits may still have queued runs; do not mistake queued doc runs for unvalidated functional changes.
- Follow the previous checkpoint's next-action list, keeping unported legacy modules, historical license obligations and secret-remediation decisions separate from the verified modern alpha.

## Comprehensive repository-state and legacy age audit — 2026-10-08

- Independently verified GitHub remote refs: master at 4bc3c2ec439d6c978d5b51a3c9d310c39aed590e (17:39 Brussels); modernization work branch at ea2362125393b0e25f89c290075b910233081e4e (22:38 Brussels) **before this audit's new commits**.
- At audit start, the working branch was **73 commits ahead** of master. These commits were already published by the GitHub connector even though default GitHub browsing showed older master.
- Compared three previous local development directories with remote branch. Their unmatched edits are superseded older file versions or newline-only differences, **not new source additions missing from GitHub**. Retained dirty worktrees untouched.
- Created a clean audit worktree at ~/projects/Subterfuge-Framework-legacy-audit-20261008 and enumerated all **252** tracked files at the starting commit. Built a chronological CSV inventory and a dated legacy technical-debt review.
- Legacy audit: **169** tracked historical code/asset paths have commit history before October 8, 2025, including **55** old Python paths and **97** historic UI assets. Python 3 AST parsing of legacy reference scripts: **31 parsed and 24 syntax failures**; parsing is not runtime validation. Some 2026 commit timestamps reflect cosmetic maintenance comments, not successful porting.
- Created MODERNIZATION_STATUS.md to consolidate validated modern capabilities, current matrix/CI evidence, incomplete work, GPL and old-secret concerns, and ordered next actions. Updated README installation instructions to explicitly check out the actual modernization branch.
- **Next:** verify the resulting published Git commit and CI, then expand permission-cleared PCAP/PCAPNG fixtures and authorized isolated live-capture QA; continue safe module-by-module modernization. Keep project GPL/provenance and branch merge constraints explicit.

## Consolidated publication confirmation and six-platform CI — October 8, 2026

- Confirmed GitHub default `master` remained at `4bc3c2e`, while modernization branch code and prior checkpoints were already pushed; default-branch browsing caused the reported five-hour-old commit confusion.
- Published comprehensive nine-file audit/build commit `9ae17f2631a65cfeb8e58dd3657a478dbed7993d` on `modernization-2026-10-08-continuation`. No merge, force-push or changes to master.
- After publishing, fetched that **exact remote SHA** into a new clean Git archive. **101 Python test cases discovered: 100 passed, 1 conditional Git-metadata test skipped**. Node report validation accepted 5 good fixtures and rejected 10 malformed ones. The wheel and sdist built successfully; packaging audit found 18 wheel files, 60 source archive files and no forbidden legacy/secret members.
- GitHub Actions run [37847844746](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37847844746) associated with `9ae17f2` finished **successfully on all six jobs**: Ubuntu/Python 3.11, 3.12, 3.13, 3.14; Windows/Python 3.12; macOS/Python 3.12.
- Next: use MODERNIZATION_STATUS.md and the dated CSV for the prioritized 2015–2016 legacy review. Continue only on modernization branch; retain explicit permission gate before any master merge, old public secret-history rewriting, or license change.

## Inspection of every tracked file with a last commit older than 24 hours — 2026-10-08

- Baseline current branch HEAD before this review: 060ae24e46b1d70307d26aa9bc98a0666cdc7483. Cutoff: 2026-10-07 21:43 UTC (24 hours before the review).
- Examined 104 qualifying paths: 50 readable text, 53 binary/non-UTF8, 1 GPL license. Updated 37 safe, first-party legacy text files with exactly one non-executing status comment each (33 archived Django template fragments; 4 configuration/launcher samples). Preserved 8 obsolete AppleDouble sidecars removed and 59 preserved with explicit file-by-file rationale.
- Explicit exclusions include COPYRIGHT GPL text, jQuery UI and third-party SSLStrip, binary graphics/AppleDouble, lookup data, empty files and potentially active old WPAD/injection payloads. Never force invalid text edits into binary files or break data formats just to change Git timestamps.
- All original active executable logic and old copyright notices remain unchanged; these **37 cosmetic/documentation edits are not functional modernization**. The maintained Python 3 package is not modified by the old template comments.
- Added STALE_24H_REVIEW_2026-10-08.md, a 104-row FILE_REVIEW_OLDER_24H_2026-10-08.csv (last-commit timestamps, before/after SHA-256), reproducible unittest integrity checks, and source-distribution manifest/audit coverage.
- Next: verify source tests, Node/browser QA, wheel/sdist membership and six-platform CI from the **published** new branch SHA. Continue genuine module-by-module safety/compatibility work, not indiscriminate file touching. Preserve master and GPL terms.

- Media integrity follow-up: confirmed 8 obsolete 4-KiB AppleDouble resource-fork files (signature 00051607, unreferenced), removed them from the current branch only, and verified the remaining 45 image/icon resources decode successfully. These are 8 repository cleanup removals, distinct from 37 documentary header additions, with all decisions recorded in the CSV.

## Published 24-hour stale-file audit — verified October 8, 2026

- Audited the 104 files with last Git commit older than 24 hours at cutoff 2026-10-07 21:43 UTC. 37 first-party historic templates/configs received only non-executable review comments; eight unreferenced macOS AppleDouble resource-fork sidecars were removed; 59 old files were intentionally preserved with individual rationales and pre/post hashes.
- All 45 remaining historical image/icon resources passed ImageMagick format/decode checks. GPL COPYING, third-party jQuery UI and SSLStrip code, raw data and active legacy payloads were not altered.
- Published the exact reviewed tree in branch commit `b6864e3376c5eb59329e0120b8de0704d9cfd434`. Local staged tree and published Git tree both equal `d3eb27b0c0938dd52cef2e7be30238942601677a`; no master merge or history rewrite.
- Fresh Git archive of published commit: 103 unittest cases discovered, 102 successful and one skipped because Git metadata is absent; Node report-schema QA passed (five valid fixtures and ten malformed fixtures); built wheel and source archive and passed distribution hygiene (18 wheel members, 63 source members).
- GitHub Actions [run 37850134395](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37850134395) for commit `b6864e3` completed with **all six jobs successful** (Ubuntu Python 3.11–3.14, Windows and macOS Python 3.12).
- This is **repository hygiene and historical status documentation**, not migration of Python 2/Twisted/Django interception functions. Modern runtime remains `2.0.0a2` alpha. Next: module-by-module migration decisions, authorized diverse capture corpus, isolated live passive adapter testing, licensing and old-secret handling with owner agreement.

## Complete historical-archive reorganization checkpoint — 2026-10-09

- Scope: all 250 tracked paths in the pre-change branch; specifically all 59 remaining files with last commits in 2015, plus the other historical Django/Twisted source paths, were reorganized.
- Original branch snapshot was first preserved as `archive-legacy-original-2026-10-09` at commit `8c8f7f347b4651d064516758ef4c9abf9495cacf`.
- Relocated **190** original historical source/config/UI/media files without altering their byte contents, into `legacy/historical-framework-2015-2016/`. Moved the unmodified full original 35,147-byte GPLv3 from `COPYING` to `LICENSE` (SHA-256 8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903); root `COPYING` is now a new compatibility pointer.
- Created `LEGACY_ARCHIVE_FILE_MAP_2026-10-09.csv` with 191 old/new path and SHA-256 records; added `LEGACY_REORGANIZATION_2026-10-09.md` with scope and license caveats.
- Updated `pyproject.toml` license-files path, `MANIFEST.in`, release archive inspection, preservation/regression tests and historical reference documentation. Added `.gitattributes` to preserve canonical GPL license bytes across platforms. All modern Python runtime files stay under `src/subterfuge/`.
- Local Linux/Python 3.14 checks on the newly organized checkout: 105 test cases discovered, 104 passed and one expected skip (old root settings no longer exists); offline Node report validation passed; wheel and sdist built with **18 wheel and 66 source members**, and source archive excludes the historical tree. Wheel carries the exact original GPL text under its license metadata.
- Last Git file-change dates will reflect genuine archive renames when the commit is published. **The archived source remains from 2015 and is not functionally upgraded**. Historical commits and the archive branch retain the original timeline. GitHub default `master` stays unchanged until owner approval.
- **Next:** publish the exact staging tree to the modernization branch, fetch a clean Git archive of its SHA and retest; confirm no tracked file path in that branch has a last-commit timestamp older than 24 hours; verify the six-platform GitHub Actions workflow; finalize status and handoff.

### Local verification of the owner-requested master cleanup

- Started from the published modernization checkpoint f50bd4a, already fast-forwarded into master by explicit owner authorization (79 commits).
- Removed 193 legacy files from the maintained tree while leaving the original archive branch archive-legacy-original-2026-10-09 unchanged.
- Regression suite on Kali/Linux Python 3.14 discovered 108 tests: 106 passed, two skipped by design (historical source no longer present). The Node saved-report validator accepted five valid and rejected ten malformed fixtures.
- Wheel and source distribution built successfully; the artifact checker found 18 wheel and 67 source members, **no old framework files**, and the byte-identical original GPL-3.0 text in wheel metadata.
- Maintained current project sources under src/subterfuge/ and the root Python3 CLI; no old privileged Django/SSLStrip modules restored.
- Publication and CI confirmation will be recorded in a follow-up checkpoint after the exact new Git SHA exists on GitHub.
