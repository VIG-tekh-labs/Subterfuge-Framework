# Historical-to-modern capability migration matrix

## Historical paths refer to an external archive branch

- The owner explicitly authorized applying modernization to the default branch master. Master fast-forwarded without force from 4bc3c2e to f50bd4a (79 commits).
- To remove the 10–11-year-old files from the active GitHub tree, all 193 tracked files in the legacy directory were deleted from the maintained branch (190 older framework files, archive README, original update.py and setup.py).
- The separate branch archive-legacy-original-2026-10-09 preserves the old source, history and copyright attribution. No history rewrite, force push, archival branch deletion or relicensing was performed.
- The active Python 3 runtime remains under src/subterfuge; it is version 2.0.0a2 alpha and does not restore unported historical interception features.
- The original complete GPLv3 text remains byte-for-byte unchanged in LICENSE, with COPYING as a pointer. Historical relocation maps remain documentation, not active source paths.
- Verify Python/Node regression tests, wheel and source archive hygiene, and six-platform CI after this cleanup. Synchronize both modernization and master through non-forced fast-forward, then verify the GitHub default root has no legacy folder.
- Remaining modernization: diverse actual authorized PCAP/PCAPNG captures, safe Scapy passive lab testing, browser accessibility/keyboard checks, provenance and module-by-module feature migration decisions.
The maintained default branch no longer includes the old legacy folder; for any old module path below, select the separate archival branch before looking it up.


This is a **feature-gap and acceptance plan**, not a claim that unported historical
modules work. Original code, attribution and Git history must be preserved. The
modern installed package contains only `src/subterfuge/`; legacy source files
outside that path are reference material and must not be imported as plugins.

| Legacy location | Historical responsibility | Modern replacement/status | Next acceptance requirement |
| --- | --- | --- | --- |
| `setup.py`, `configure.py`, `legacy/setup.py`, `uninstall.py` | Privileged Python 2 / OS installer | `pyproject.toml`, pip + venv; privileged installer archived | Fresh install on Linux, Windows and macOS; uninstall from venv |
| `update.py` and `legacy/update.py` | SVN/socket-based auto-updates | Read-only Python 3 migration notice plus reviewed Git/pip updates | Signed releases and integrity checks before any automatic updater |
| `main/views.py`, `urls.py`, `settings.py`, `manage.py` | Django 1.x dashboard and routes | stdlib loopback HTTP server `src/subterfuge/web.py` | Accessible UI, token/origin checks, safe report workflows |
| `main/models.py`, `modules/models.py`, `db` | Django persistence and application state | JSON report schema and private atomic export; no persistent server DB | Define secure local project storage and migration without historic secrets |
| `templates/` / jQuery UI assets | Original Django templates | Dependency-free local `static/index.html` | Visual/responsive/browser QA and accessibility review |
| `utilities/arpwatch.py`, `utilities/scan.py` | ARP monitoring and network inventory | PCAP/PCAPNG ARP observation, optional live passive ARP/DHCP/NBNS capture, Nmap XML import and bounded discovery | Real capture and authorized isolated network regression |
| `utilities/arpmitm.py`, `utilities/rearp.py` | ARP interception/recovery | No active replacement; passive address-conflict evidence | Deliberate safety/authorization decision and separately scoped tests |
| `utilities/dhcptools.py`, `utilities/dhcprace.py` | Rogue DHCP/race logic | Passive DHCP metadata and option-252 presence inspection (offline and optional live adapter) | Real-world DHCP packet coverage, no active spoofing by default |
| `utilities/nbtools.py`, `utilities/wpadhijack.py` | WPAD/NetBIOS response and manipulation | Passive NBNS name-query observations, including WPAD (offline and optional live adapter) | Additional name-resolution formats and capture tests |
| `utilities/apgen.py` | Wireless AP generation | No replacement included | Review current OS drivers/capabilities and need for isolated AP lab |
| `sslstrip/`, `sslstrip.py`, `attackctrl.py` | Historical HTTP/TLS interception/downgrade proxy | Certificate-verified TLS endpoint inspection (CLI and dashboard) | Modern TLS/HSTS model review; do not claim downgrade/proxy parity |
| `modules/harvester/` | FTP/HTTP credentials | No credential capture in modern package | Decide if a privacy-safe protocol configuration audit meets the legitimate need |
| `modules/sessionhijacking/` | Session capture/management | No modern active implementation | Review lawful web session tests and browser security protections |
| `modules/httpcodeinjection/` | HTTP response manipulation | No modern active implementation | Assess legitimate isolated test fixtures instead of live injection |
| `modules/TunnelBlock/`, `modules/dos/` | Traffic disruption | Not active and not shipped | Avoid reactivating destructive functions as routine diagnostics |
| `scan.py`, legacy Nmap wiring | Scan control / reporting | `discover`, `import-nmap`, new bounded `scan-services` for one explicit IP | Verify Nmap adapter in authorized lab; cap targets/ports/timing |
| Legacy reports / databases | Historical logs and export | JSON report download, client-side saved-report reopening and atomic CLI export | Local secure report import/history, schema compatibility and data minimization |

## Technology decisions

- **Keep:** Python 3.11+ and its standard library for offline parsing and local
  dashboard; optional modern Scapy for passive capture; optional current Nmap
  for explicit inventory/discovery; GitHub Actions matrix across current OSes.
- **Do not install merely for compatibility:** Django 1.x, Python 2, Twisted's
  old SSLStrip integration, legacy jQuery UI or system-wide Python packages.
- **Do not silently discard:** attribution, historical source, GPL notices and
  scope gaps between the old and the new runtime.
- **Licensing:** see `LICENSING.md` for the GPLv3/GPLv2-only notice conflict
  and the conditions that would be needed to consider different licensing.
- **Security:** no live network action during offline unit tests. Nmap service
  inventory is explicitly invoked, limited to one IP and at most 32 TCP ports;
  it can create traffic and requires target-owner permission.

## Recommended order of work

1. Expand real PCAPNG and DHCP/NBNS capture regression coverage, including
   malformed packets, link types, repeated records and memory limits.
2. Validate optional Nmap and Scapy adapters on a private authorized lab,
   without touching external networks or production systems.
3. Improve report storage/import/history and browser accessibility.
4. Review each historical plugin's function, current protocol assumptions,
   legal provenance and safe replacement before assigning it a migrated status.
5. Plan security history cleanup and third-party license review with owner
   authorization; keep published packages free of historical keys/databases.
6. Reassess alpha readiness and cut a documented release only when its
   advertised features are independently verified.

## Location of historical paths, 2026-10-09

Historical paths in the migration table are *original path labels*, not current active files. Prefix each such path with `legacy/historical-framework-2015-2016/` to access its unchanged archival reference. For example, modules/views.py is now `legacy/historical-framework-2015-2016/modules/views.py`. This is a relocation, not a verified Python 3 port.
