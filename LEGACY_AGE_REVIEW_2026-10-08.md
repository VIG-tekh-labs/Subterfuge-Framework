# Historical file-age and modernization audit — 2026-10-08

Repository: https://github.com/VIG-tekh-labs/Subterfuge-Framework
Working branch: `modernization-2026-10-08-continuation`
Historical inventory baseline commit: `ea2362125393b0e25f89c290075b910233081e4e`

## Interpretation and scope

- Commit timestamps are not proof of functional modernization. A 2026 maintenance comment or security cleanup can alter an old file without porting it to Python 3.
- The historical column records the most recent Git commit BEFORE October 8, 2025 for paths that existed then; a file may have newer work too.
- Classify obsolete legacy code separately from the installed modern package under src/subterfuge; no old code is executed during this audit.

## Inventory results

- **252 tracked files** evaluated, all with Git commit history.
- **169 currently tracked legacy code/asset files** have historical commits before the one-year cutoff.
- **55 historical Python scripts** and **97 old UI/asset paths** fall in that cohort.
- **31 legacy-reference Python scripts parse under current Python 3; 24 fail syntax parsing.** Syntactic success is not operational compatibility.
- All paths, classes, recent commit dates and historical commit dates are in `FILE_AGE_INVENTORY_2026-10-08.csv`.

| Category | Tracked files | Historic code/assets before cutoff |
|---|---:|---:|
| `archived_legacy` | 2 | 0 |
| `automation` | 1 | 0 |
| `documentation_and_build` | 16 | 0 |
| `historical_ui_assets` | 97 | 97 |
| `legacy_reference` | 72 | 72 |
| `maintenance_note` | 26 | 0 |
| `miscellaneous` | 4 | 0 |
| `modern_qa` | 4 | 0 |
| `modern_runtime` | 12 | 0 |
| `modern_tests` | 18 | 0 |

## Legacy decisions

| Area | Representative paths | Current decision |
|---|---|---|
| Old Django app | `manage.py`, `settings.py`, `urls.py`, `main/views.py` | Modern runtime uses a loopback stdlib dashboard; no Django 1.x install needed. |
| Old Twisted/SSLStrip proxy | `sslstrip/ServerConnection.py`, `sslstrip/StrippingProxy.py`, `attackctrl.py` | Archive interception assumptions incompatible with modern TLS/HSTS; no active proxy shipped. |
| DHCP and NBNS active legacy | `utilities/dhcprace.py`, `utilities/dhcptools.py`, `utilities/nbtools.py` | Modern passive readers exist; spoofing scripts are preserved reference-only. |
| ARP and wireless | `utilities/arpmitm.py`, `utilities/apgen.py`, `utilities/rearp.py` | Modern ARP evidence analysis exists; active interception/AP generation remains unported. |
| Session/credential/injection modules | `modules/sessionhijacking/cookiestealer.py`, `modules/harvester/ftp_password_sniffer.py`, `modules/httpcodeinjection/httpcodeinjection.py` | Keep out of modern builds; security and GPLv2-only provenance require review. |
| Old UI dependencies | `templates/js/`, `templates/css/` | No old jQuery UI runtime dependencies in modern local dashboard. |

## Actions remaining

1. Verify only current branch code in fresh worktrees; the old working directories can have local changes from earlier snapshots. Do not overwrite them.
2. Preserve the modern Python 3.11+ standard-library core and optional current Scapy/Nmap; do not install Python 2, Django 1.x, obsolete jQuery, or historic SSLStrip merely for compatibility.
3. Expand genuine authorized PCAP/PCAPNG fixtures, packet format limits, DHCP/NBNS compatibility and real-interface passive capture in an explicitly isolated lab.
4. Add keyboard/focus and browser accessibility regressions, local report persistence planning and input-fuzzing cases.
5. Inspect every historical module's design and provenance before replacing it; report separate status: migrated, safe replacement, deliberately archived, or unresolved.
6. Review GPLv2-only historical FTP module and copyrighted third-party assets separately before distributing any combined source. Retain GPL notices absent explicit relicensing rights.
7. Review old public commits for sensitive artifacts and coordinate rotations. Never rewrite Git history, force-push, merge master or delete historical records without explicit owner approval.
8. Confirm six-platform GitHub Actions and wheel/sdist archive hygiene after every functional change. Preserve handoff and roadmap updates.

## Limitations and related documents

- This is a static full tracked-file timestamp/classification pass, with Python AST parsing of old reference scripts. It is not a claim every old feature was tested or ported.
- Current functionality: see `MIGRATION_MATRIX.md` and `CAPABILITIES.md`.
- Security and provenance: see `SECURITY.md` and `LICENSING.md`.
- Latest verified source SHA and resumed actions: see `HANDOFF.md` and `ROADMAP.md`.
