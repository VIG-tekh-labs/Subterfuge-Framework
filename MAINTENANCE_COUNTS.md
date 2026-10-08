# Maintenance change counts

## Client-only saved report reopening checkpoint — 2026-10-08

- Added an explicit JSON report file picker to the loopback dashboard.
- Saved reports are parsed and validated entirely client-side (size and
  schema bounds); no backend upload or new database dependency.
- Chromium/Puppeteer successfully exported the demo, reloaded its JSON
  report and rejected a malformed report with no JavaScript exception.
- The 89 Python regression tests continued to pass.

## Repository hygiene and independent format QA checkpoint — 2026-10-08

- Added regression checks for tracked historical artifacts and a literal
  Django secret; optional independent Wireshark editcap format conversion.
- Added `qa/loopback_nmap_smoke.py` so active inventory may be checked
  against an ephemeral loopback service without probing other hosts.
- Local tests: **89 tests passed**, including editcap interoperability when
  installed. GitHub CI may skip the editcap test when unavailable.

## Passive live protocol observation checkpoint — 2026-10-08

- Added an opt-in Scapy adapter, `capture-protocols`, for passive ARP,
  DHCPv4 and NBNS observation, retaining only bounded metadata.
- Added mocked capture tests; 86 total unit tests passed on Linux/Python
  3.14. This does **not** validate real capture permissions or drivers.
- Maintained the ARP-only `capture` command for compatibility.

## TLS dashboard alpha-2 checkpoint — 2026-10-08

- Added authenticated, bounded JSON `/api/inspect-tls` endpoint to the
  existing loopback server, reusing TLS certificate-verification logic.
- Added a TLS inspection form and report rendering; no Django, Twisted
  or external frontend dependency.
- Added HTTP boundary tests and manual Chromium/Puppeteer validation.
- Bumped the development version to `2.0.0a2` (alpha), **not** a stable
  release or a claim of historical feature parity.

## Repository-wide audit and capture evidence checkpoint — 2026-10-08

- Baseline classification: 293 tracked paths inventoried in `FILE_AUDIT.md`.
- Python 3 AST audit: 82 Python files; 26 legacy syntax/indentation failures.
- Historical cleanup proposed: 58 Git-tracked generated or sensitive paths
  removed from the continuation branch. **Removal is not Git history erasure.**
- Functional changes: aggregate passive DHCP/NBNS observations for classic PCAP
  and PCAPNG (Ethernet/VLAN and Linux cooked), add bounded evidence groups,
  render passive evidence in the dashboard and add end-to-end tests.
- Validation at local checkpoint: 76 Python unit tests passed, wheel and source
  distribution built without legacy scripts or sensitive files, Scapy 2.8.0
  installed in the isolated environment, Chromium headless HTTP/dashboard
  smoke test passed. This does not imply historical functional parity or
  cross-platform validation.
- Documentation additions: AUDIT.md, FILE_AUDIT.md, SECURITY.md, LICENSING.md.

## Functional checkpoint — 2026-10-08

This checkpoint changes 25 paths: 9 modern runtime files, 6 test/fixture files, 3 packaging files, README.md, ROADMAP.md, CAPABILITIES.md, this report, .gitignore, one CI workflow and the preserved historical installer.

These are real implementation, installation, validation and documentation changes. No optional live adapter has been verified against a real network. No complete historical feature parity is claimed.

- Core dependencies: none; Django 1.7 and Twisted are not required by the modern package.
- Build backend: setuptools >=77.0.3, locally tested with 84.0.0.
- Optional capture dependency: Scapy >=2.6.1,<3; installation and live operation remain unverified.
- Validation: 50 tests passed on Linux/Python 3.12; fresh wheel installation and a trusted localhost TLS handshake passed.
- CI matrix added; results are pending.

## Earlier cosmetic checkpoint

Commit 634979fdb8cc71f309bb168706906be7a6817e61 modified 71 source files with comments, added notes in 26 directories, updated 2 root documents and added the count report. It contained 0 functional fixes and 0 dependency upgrades. 163 existing files were unchanged at that point.

Directory activity does not mean every contained file has changed. Filesystem touch operations do not update GitHub commit dates.