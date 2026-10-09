# Subterfuge modernization: verified status and remaining work

## October 9, 2026 — Self-contained Windows EXE and Linux DEB

- Windows setup built natively on a Windows GitHub runner with PyInstaller
  and Inno Setup. The application bundles Python, Qt/PySide6 and Scapy.
  A user-selectable task, checked by default, installs Nmap, Wireshark/TShark
  and mitmproxy through WinGet when Windows allows it.
- Linux .deb built natively on an Ubuntu 22.04 runner with a bundled Python
  and Qt GUI. Debian package dependencies install Nmap, TShark, mitmproxy
  and required system Qt libraries from trusted APT repositories.
- Both artifacts are independently smoke-tested. Only after their two build
  jobs succeed does the GitHub release job publish EXE, DEB and SHA256SUMS.
- Source and installer documentation: DOWNLOADS.md and
  THIRD_PARTY_NOTICES.md. macOS native packaging is postponed.
- OS admin prompts, restricted repositories, missing WinGet or Npcap drivers
  remain environment-specific prerequisites. No private app is required.


## Native Desktop GUI + secure Web server access — 2.0.0a4 alpha

- Added a **real PySide6/Qt Widgets desktop application**, without Chromium,
  HTTP server or WebView. Five sections: Overview, Files & Reports, Network,
  TLS / HTTPS and Settings. A visual overview shows the same categories of
  inventory, findings and passive evidence as the existing Web dashboard.
- The native desktop uses the same Python assessment engine as the CLI / Web
  interface. Analyses run on worker threads. Raw JSON import is bounded and
  validated; report strings render as plain text. Passive network capture,
  active host/service discovery, TLS inspection and loopback proxy operation
  require explicit GUI actions and confirmations.
- Desktop installation is optional: python -m pip install ".[desktop]";
  launch with subterfuge gui or subterfuge-desktop. A local per-user Linux
  applications-menu shortcut (no root) can be installed explicitly with
  subterfuge desktop-shortcut; both shortcut and SVG logo are packaged.
  No additional dependencies are imposed on core CLI/Web users.
- **The Web interface remains available.** Locally, run subterfuge serve
  --port 8080 and visit http://127.0.0.1:8080/ (port configurable).
  The GUI Settings page can separately start/stop this local Web server on
  demand, without automatically opening a browser.
- **Servers without GUI are supported.** The recommended secure remote
  method is SSH port forwarding to the server's loopback dashboard:
  ssh -N -L 127.0.0.1:8080:127.0.0.1:8080 -p 22 user@SERVER_IP,
  followed by http://127.0.0.1:8080/ locally. For a direct
  https://SERVER_IP:8443/ URL, an externally configured **authenticated
  HTTPS reverse proxy** must forward traffic to the local HTTP backend.
  The new --public-origin https://SERVER_IP:8443 option allows exactly
  that validated HTTPS Origin, while the app **still binds exclusively to
  127.0.0.1**. The reverse proxy must perform TLS and authentication and
  rewrite upstream Host to the local backend, preserving Origin.
- No automatic public binding, open proxy, silent certificate installation,
  network scans or telemetry. Native desktop and Web are separate launch
  modes; they do not currently synchronize in-memory reports. Future mobile
  work may reuse the Web interface with an authenticated transport.
- Documentation: [DESKTOP_GUI.md](DESKTOP_GUI.md) and
  [SERVER_ACCESS.md](SERVER_ACCESS.md).


## VERIFIED RELEASE — October 9, 2026: Subterfuge 2.0.0a3

- Source features commit: `6d5329320e9669a54217ac996731447479a59440`; cross-platform portability fix: `02aaa76d3529b599e445b24d6377a3bea076c2c8`. Both are on default `master` and the modernization continuation branch, without a forced update.
- The real 127.0.0.1 TLS/HTTPS integration test produced an actual PCAPNG and five SSLKEYLOGFILE entries; TShark 4.6.6 recovered two HTTP messages including the synthetic request path.
- The real loopback mitmdump 12.2.3 proxy test returned HTTP 200 from an explicitly configured local temporary HTTP server. The proxy uses regular opt-in mode, does not redirect other clients, refuses LAN/untrusted interfaces and disables optional external update checks.
- The standalone package built and installed in a fresh virtualenv as `2.0.0a3`. The wheel has **26** entries; the source archive has **81**. They contain the Chrome/Chromium MV3 Browser Lab, TLS module, Bettercap offline-event adapter and generic agent tool contract, with the old framework excluded.
- Published code checkout: **134 Python test cases**, 132 passed and two expected historical-source skips; Node Browser Lab preference/indicator/scope tests passed, as did saved-report schema validation (five valid accepted, ten invalid rejected).
- Six-platform GitHub Actions check [run 37862358235](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37862358235) passed on Linux (Python 3.11, 3.12, 3.13 and 3.14), Windows 3.12 and macOS 3.12. The earlier first attempt exposed only path alias differences for decrypted export file tests on Windows/macOS; `os.path.samefile` fixed that regression.
- The Chromium companion retains its visible user preference across browser restarts, but only injects a read-only inspector into the recognized local 127.0.0.1 Subterfuge dashboard. No persistence on third-party websites, cookies, hidden hooks, administrative elevation or remote commands. MV3 persistence has been simulated in QA, not manually tested after a browser restart.
- The optional agent API `subterfuge.agent_integration.run_authorized` is a **ready-to-integrate adapter**, not proof of live registration in a local agent. A caller must provide mission-scoped `allowed_actions`, `allowed_files` and/or `allowed_targets`; sensitive TLS and active network operations need separate affirmative gates. Standalone users need no external agent services or rules.
- Bettercap integration currently **imports user-exported, discovery-only JSON events**; it does not execute Bettercap or impersonate third-party browsers. Old interception features remain unported and are preserved in the historical archive branch only.
- **Next work:** connect the optional adapter to the calling agent's actual tool registry under explicit owner policy after a separate compatibility test; manually smoke-test Chromium extension after a real browser restart; expand permitted live capture / PCAPNG compatibility, and continue license and privacy QA.


## 2026-10-09 — TLS authorized diagnostic expansion

### New optional TLS / Browser Lab capabilities — 2026-10-09 (2.0.0a3)

- Added a TShark-backed offline tls-decrypt command for PCAP/PCAPNG plus a user-supplied SSLKEYLOGFILE, with strict key-log input permissions (0600 on Unix), limits, metadata-only default, opt-in URI inclusion and private atomic decrypted JSON export.
- Proved a real loopback-only TLS/HTTPS test: a locally generated server certificate, a controlled client producing five TLS secrets, an actual PCAPNG capture on lo and TShark reporting two decrypted HTTP messages, including the expected synthetic test URI.
- Added a mitmproxy-based proxy-lab command for visible local test clients. Only explicit regular proxy mode on 127.0.0.1/loopback is allowed; LAN binding, stealth interception, unauthorized client redirection and automatic CA trust changes are excluded.
- Added a Chromium Manifest V3 Browser Lab companion shipped with the Python wheel and sdist. It has a simple enable/disable toggle, persisted local setting and read-only inspect action. It operates ONLY on 127.0.0.1 with a recognized local Subterfuge dashboard; it does not read cookies or credentials, inject into arbitrary sites, or run background remote commands.
- Added a read-only Bettercap JSON event importer accepting only network discovery tags and discarding packet contents, handshake keys and attack-related events.
- Added agent-capabilities and an independent optional agent-compatible Python policy bridge: standalone operation requires no external agent; a calling agent must supply exact allowed_actions, allowed_files and allowed_targets with additional affirmative gates for sensitive TLS/network operations. Those caller-defined rules can further restrict but never bypass OS controls.
- These modules are optional components. Python 3.11+ modern offline analysis remains zero mandatory external runtime dependencies; TShark and mitmdump are optional installed system tools.
- For installation, examples, scope, privacy and security rules, consult TLS_BROWSER_LAB_2026-10-09.md. Current release remains alpha (2.0.0a3), not a recreation of historical SSLStrip, BeEF, Bettercap spoofing or user-session hooks.


## Verified default-branch cleanup — October 9, 2026

- **Final active code commit:** 9a986a148eb34cf74596df8b6d2adbfa34714ad8. The owner explicitly approved fast-forwarding modernization into master; the 79 earlier commits were applied without a force push.
- **Removed from the active GitHub tree:** 193 historical files in legacy (Django, Twisted/SSLStrip, UI assets, old setup/updater). A fresh clone of master confirms **63 tracked files and zero legacy paths**.
- **Preservation:** The original source and authorship are on the separate archive-legacy-original-2026-10-09 branch and in Git history. No history rewriting or relicensing occurred; 2015 code was not made functional.
- **Fresh checkout tests:** 108 Python cases discovered; 106 passed, 2 expected skips for absent historical source. Node saved-report validation accepted 5 valid and rejected 10 malformed fixtures.
- **Distribution:** wheel has 18 members, sdist has 67 members; both exclude the old legacy tree. The original GPLv3 license hash remains 8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903.
- **GitHub Actions:** [run 37858737482](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37858737482) passed all six jobs on Linux (Python 3.11–3.14), Windows and macOS (Python 3.12).
- **Still incomplete:** Version 2.0.0a2 alpha; old interception functionality remains unported. Further real-device capture, diverse PCAPNG, keyboard accessibility and provenance/legal review are needed.
- **Continuation:** Work from master; the separate modernization branch is synchronized to the same latest revision. Read ROADMAP and HANDOFF before new changes. No pull request needed for this cleanup.


## Default master now modern; historical source no longer on main

- The owner explicitly authorized applying modernization to the default branch master. Master fast-forwarded without force from 4bc3c2e to f50bd4a (79 commits).
- To remove the 10–11-year-old files from the active GitHub tree, all 193 tracked files in the legacy directory were deleted from the maintained branch (190 older framework files, archive README, original update.py and setup.py).
- The separate branch archive-legacy-original-2026-10-09 preserves the old source, history and copyright attribution. No history rewrite, force push, archival branch deletion or relicensing was performed.
- The active Python 3 runtime remains under src/subterfuge; it is version 2.0.0a2 alpha and does not restore unported historical interception features.
- The original complete GPLv3 text remains byte-for-byte unchanged in LICENSE, with COPYING as a pointer. Historical relocation maps remain documentation, not active source paths.
- Verify Python/Node regression tests, wheel and source archive hygiene, and six-platform CI after this cleanup. Synchronize both modernization and master through non-forced fast-forward, then verify the GitHub default root has no legacy folder.
- Remaining modernization: diverse actual authorized PCAP/PCAPNG captures, safe Scapy passive lab testing, browser accessibility/keyboard checks, provenance and module-by-module feature migration decisions.
Historical path and commit dates elsewhere in the document are prior audit snapshots, not current active paths.


## Published validation of archival restructuring — October 9, 2026

Commit `1f21f9bc8cfafd4689eb781e6f83f7f335fcf8f5` reorganized the inactive source into a preserved historical tree without rewriting legacy contents. All 190 historical source files remain accessible in a named archive directory; one more exact-byte relocation moved complete GPLv3 text to LICENSE. The separate archive branch retains the pre-move complete repository snapshot.

The active modernization branch's **255 tracked paths now have zero last-path-commit dates older than 24 hours** at the 01:03 Brussels verification. That Git metadata result reflects real relocation operations, not evidence of an operational upgrade of the 2015 content; history, copyright and the default master branch remain unchanged.

Re-fetched published Git tree tests: 105 Python test cases (103 success, 2 expected skips without Git metadata), Node saved-report tests (5 valid, 10 malformed), 18-entry wheel and 66-entry source archive; full original GPL text hash verified. Six cross-platform GitHub Actions checks all succeeded in [run 37857219307](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37857219307).

**Reviewed:** October 9, 2026, Europe/Brussels.
**Repository:** https://github.com/VIG-tekh-labs/Subterfuge-Framework
**Current work branch:** `modernization-2026-10-08-continuation`
**Last fully verified functional commit:** `d8bb5b836b20046e13712beced1e03c7b5ee36c5`
**Repository main/master baseline:** `4bc3c2ec439d6c978d5b51a3c9d310c39aed590e` (earlier alpha)
**Alpha version:** `2.0.0a2` — not a full historical framework restoration.

## Why GitHub seems unchanged

The default GitHub view opens master; the modernization is **already published**
on a separate branch. At the initial audit, this branch was **73 commits ahead**
of master, which still pointed to the earlier 17:39 Brussels commit.
This is deliberate: no merge to master was authorized. The read-only
compare URL is:
https://github.com/VIG-tekh-labs/Subterfuge-Framework/compare/master...modernization-2026-10-08-continuation

The older local checkouts contain snapshots with dirty file status, but an
explicit comparison against the latest remote branch found no unique missing
local source paths. Content differences represented **older edits already
superseded on the branch**; other mismatches were only trailing newlines.
Do not run reset/clean on those worktrees without owner review.

## Completed and verified modern components

| Area | Current modern state | Verified evidence or limitation |
|---|---|---|
| Install and packages | Python 3.11+, venv/pip, setuptools; no core Django/Twisted dependency | Wheel and source archive build; prior six-platform CI |
| Capture import | Bounded classic PCAP and experimental PCAPNG, incl. classic/obsolete/simple packet blocks and untimed hosts | Synthetic regression tests, editcap sample conversion; diverse real captures pending |
| Passive network evidence | ARP, DHCPv4, NBNS/WPAD metadata; no payload retention in reports | Python regressions; live drivers/interface tests pending |
| Discovery | Nmap XML import, bounded optional discovery and one explicit-IP service scan | Loopback-only integration check; never claim broad authorized live coverage |
| TLS | Certificate-verified TLS endpoint inspection in CLI/dashboard | Local TLS fixtures and CLI/dashboard tests; not a TLS interception proxy |
| Dashboard | Local loopback only, same-origin token protection, JSON report reopening and export | Chromium UI QA; more keyboard/accessibility work pending |
| Security and archives | No known legacy interception paths, keys, logs or credential artifacts in modern wheel/sdist | 18 wheel/57 source members audited, six-platform CI |
| Tests | Modern Python 3 code and browser schema checks | 100 Python cases in checkout; fresh archive 99 passed and one Git-metadata skip; 5 good/10 malformed JSON fixtures and Chromium QA |
| Legacy active plugins | Python 2/Django/Twisted/old jQuery historical sources retained as references, not imported | **Not functionally restored or claimed compatible** |

Six-platform GitHub Actions success for the last functional commit:
https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37840748127

## Audit of old material (older than a year)

At the start of this review, `ea23621`, the branch tracked
**252 files**. **169 historical code/assets** have pre-October-8-2025
commit history; this includes 55 old Python paths and 97 UI assets.
24 of the reviewed legacy Python reference files fail Python 3 syntax parsing.
Changes made in 2026 solely to add maintenance markers **must not be counted**
as functionality migrated. See:
- FILE_AGE_INVENTORY_2026-10-08.csv (every tracked path and timestamp)
- LEGACY_AGE_REVIEW_2026-10-08.md (audit, categories and module decisions)
- MIGRATION_MATRIX.md and FILE_AUDIT.md (functional inventory and earlier security audit)

## Not complete or not validated

1. Legacy ARP interception, rogue DHCP, SSLStrip, credential/session
   interception, injection, denial-of-service, and wireless AP creation are
   **not enabled in the new package**. Their old protocol assumptions and
   safety implications require separate decisions; presence in GitHub is not
   proof of modern compatibility.
2. Real-world PCAPNG diversity, packet malformed-input corpus and actual
   Scapy capture on an authorized lab interface need further test coverage.
3. Cross-platform browser keyboard/accessibility and real-world report
   imports still need additional QA.
4. Old Git history and master may contain archived secret material, even
   though current modern distributions pass hygiene tests; rotation/history
   remediation requires owner involvement and explicit approval.
5. GPL and per-file copyright obligations remain; a GPLv2-only legacy file
   needs specific legal/provenance review before combination/distribution.
6. Alpha compatibility is **not** a released/full feature-parity claim.

## Required next actions (ordered)

1. Confirm CI for the current feature SHA, then verify fresh branch wheel,
   source archive and suite before any new feature change.
2. Build and validate a diverse, permission-cleared PCAP/PCAPNG/DHCP/NBNS
   corpus; add malformed/memory/time-bound tests.
3. Validate optional Scapy live passive capture on one specifically
   authorized isolated interface only. No default network injection.
4. Audit saved report keyboard navigation/focus, file parsing bounds,
   meaningful error feedback and secure local persistence alternatives.
5. Review each 2015–2016 historical component against the migration matrix
   and choose: modern safe replacement, separate explicitly authorized lab
   function, reference-only retirement, or blocked by obsolete protocols.
6. Complete third-party asset/IP provenance; decide whether historical
   source needs to remain in a separate archive. Do not change licenses
   or erase attribution solely because most new code differs.
7. Coordinate any exposed historical secrets and history rewrite with
   the owner. Never rewrite public history or force push silently.
8. Update ROADMAP.md and HANDOFF.md after each verified step. Never merge
   master without explicit approval.

## Commands for a clean validation

On a fresh worktree of the modernization branch:

    python3 -m venv .venv
    .venv/bin/python -m pip install .
    PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
    SUBTERFUGE_PYTHON=.venv/bin/python node qa/browser_report_validation.mjs

For source-distribution validation, install build in that venv, build wheel
and sdist, then run:

    .venv/bin/python qa/audit_distributions.py dist

Avoid running historical privileged setup.py, active interception scripts,
untrusted payloads or production-network scans as basic health checks.

## Verification of the published consolidation

The consolidated documentation/build change was published at GitHub commit
`9ae17f2631a65cfeb8e58dd3657a478dbed7993d`, without merging master.

Independent fetch-and-test from that remote commit: 101 Python test cases
were discovered (100 passed and one Git-metadata-dependent test skipped);
Node report-schema checks and modern wheel/sdist inclusion/hygiene audits
passed (18 wheel members, 60 source archive members).

GitHub Actions [run 37847844746](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37847844746)
also passed all six platform jobs. The software still remains an alpha without
full historical feature parity or cleared relicensing of derivative material.

## Review of files older than 24 hours — October 8, 2026

- At baseline 060ae24, 104 tracked paths had last Git commits more than 24 hours earlier. All were opened and classified, with documented pre/post SHA-256 hashes.
- 33 historical first-party Django template fragments and 4 obsolete configuration/launcher samples received non-executable status comments; 8 unreferenced AppleDouble macOS binary sidecars were removed, while 59 originals (including 45 valid images/icons, GPL license, vendor code, payloads and raw data) were intentionally preserved.
- The 37 annotations change Git content and update file history but DO NOT make any historical Django/SSLStrip/DHCP hijacking modules functional under Python 3. The modern active distribution remains separate.
- See STALE_24H_REVIEW_2026-10-08.md and FILE_REVIEW_OLDER_24H_2026-10-08.csv for every path, previous commit date, checksum and decision.

### October 8 older-file audit: published and verified

Commit `b6864e3376c5eb59329e0120b8de0704d9cfd434` reviewed 104 files more than 24 hours old (Git last-commit measure): 37 status comments, eight unused AppleDouble sidecars removed, 59 original files preserved. The 45 remaining images/icons decode correctly. It was independently verified from a fresh Git archive (103 test cases, 102 successes plus one Git-metadata skip; Node QA and wheel/sdist hygiene passed) and on all six GitHub Actions runners ([run 37850134395](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37850134395)). This maintenance checkpoint does not establish restored historical attack functionality; the modern package remains an alpha.

## Historical code/archive separation — 2026-10-09

- The old Django/Twisted-era root and templates were structurally reorganized under `legacy/historical-framework-2015-2016/`. **190 original files** were moved with unchanged bytes, retaining source and license notices; all previous file names have a traceable mapping in `LEGACY_ARCHIVE_FILE_MAP_2026-10-09.csv`. The complete pre-move tree remains available on GitHub branch `archive-legacy-original-2026-10-09`.
- The complete original GPLv3 text was moved unchanged into root `LICENSE`, with a new compatibility pointer `COPYING`. No relicensing occurred; this preserves byte-level legal text and updates packaging to include it.
- The active Python 3 core is not affected. The reorganization changes the last Git path-commit timestamps because the paths are genuinely new, but does not improve compatibility of historical interception code. Real functionality remains defined by the separate modern capability tests and documented gaps.
- Pre-publication tests: 105 Python unittest cases (104 success, one expected skip), offline Node report schema validation, wheel/sdist and license-byte hygiene passed. Publish and independently confirm this exact change before declaring branch-wide completion.

## 2026-10-09 — Prepublication functional validation of 2.0.0a3

- A real 127.0.0.1-only SSL/TLS test produced a PCAPNG capture and
  SSLKEYLOGFILE with five entries; the new offline TShark module decrypted
  two HTTP messages and recognized the synthetic local request path.
- A real locally bound mitmdump proxy completed an explicit HTTP request
  to an operator-controlled temporary HTTP listener with status 200.
- Browser Lab Manifest V3 behavioral simulation passed, including local
  preference persistence and refusal to inject on unrelated websites.
- 134 Python tests discovered (132 passed, two expected history-related
  skips), Node Browser Lab and existing report JSON validators passed.
- Standalone wheel 2.0.0a3 installed into an isolated venv and located its
  packaged browser extension and generic agent tool manifest; archive QA confirmed
  26 wheel and 81 source archive members before the last adjustments.
- Built-in proxy remains loopback-only to avoid becoming a shared, open
  interception proxy; Bettercap integration is offline event import only.
- caller-defined rules can be enforced through the explicit allowed_actions,
  allowed_files, allowed_targets mission bridge. No automatic calling agent
  patch, credential extraction or silent persistence is claimed.
- Publish to GitHub only after final regressions, then check Linux/
  Windows/macOS GitHub Actions and preserve the existing archival branch.
