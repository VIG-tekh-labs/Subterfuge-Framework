# Subterfuge modernization: verified status and remaining work

**Reviewed:** October 8, 2026, Europe/Brussels.
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
