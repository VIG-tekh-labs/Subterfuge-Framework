# Maintenance roadmap

Last checkpoint: 2026-10-08, Europe/Brussels.
Repository: https://github.com/VIG-tekh-labs/Subterfuge-Framework
Reference branch: master.
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