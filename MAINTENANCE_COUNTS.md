# Maintenance change counts

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
