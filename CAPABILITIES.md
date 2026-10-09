# Capability migration

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


## 2026-10-09 — Actual modern TLS / Browser Lab additions

### New optional TLS / Browser Lab capabilities — 2026-10-09 (2.0.0a3)

- Added a TShark-backed offline tls-decrypt command for PCAP/PCAPNG plus a user-supplied SSLKEYLOGFILE, with strict key-log input permissions (0600 on Unix), limits, metadata-only default, opt-in URI inclusion and private atomic decrypted JSON export.
- Proved a real loopback-only TLS/HTTPS test: a locally generated server certificate, a controlled client producing five TLS secrets, an actual PCAPNG capture on lo and TShark reporting two decrypted HTTP messages, including the expected synthetic test URI.
- Added a mitmproxy-based proxy-lab command for visible local test clients. Only explicit regular proxy mode on 127.0.0.1/loopback is allowed; LAN binding, stealth interception, unauthorized client redirection and automatic CA trust changes are excluded.
- Added a Chromium Manifest V3 Browser Lab companion shipped with the Python wheel and sdist. It has a simple enable/disable toggle, persisted local setting and read-only inspect action. It operates ONLY on 127.0.0.1 with a recognized local Subterfuge dashboard; it does not read cookies or credentials, inject into arbitrary sites, or run background remote commands.
- Added a read-only Bettercap JSON event importer accepting only network discovery tags and discarding packet contents, handshake keys and attack-related events.
- Added agent-capabilities and an independent optional agent-compatible Python policy bridge: standalone operation requires no external agent; a calling agent must supply exact allowed_actions, allowed_files and allowed_targets with additional affirmative gates for sensitive TLS/network operations. Those caller-defined rules can further restrict but never bypass OS controls.
- These modules are optional components. Python 3.11+ modern offline analysis remains zero mandatory external runtime dependencies; TShark and mitmdump are optional installed system tools.
- For installation, examples, scope, privacy and security rules, consult TLS_BROWSER_LAB_2026-10-09.md. Current release remains alpha (2.0.0a3), not a recreation of historical SSLStrip, BeEF, Bettercap spoofing or user-session hooks.


## Active modern package only; old source in archival branch

- The owner explicitly authorized applying modernization to the default branch master. Master fast-forwarded without force from 4bc3c2e to f50bd4a (79 commits).
- To remove the 10–11-year-old files from the active GitHub tree, all 193 tracked files in the legacy directory were deleted from the maintained branch (190 older framework files, archive README, original update.py and setup.py).
- The separate branch archive-legacy-original-2026-10-09 preserves the old source, history and copyright attribution. No history rewrite, force push, archival branch deletion or relicensing was performed.
- The active Python 3 runtime remains under src/subterfuge; it is version 2.0.0a2 alpha and does not restore unported historical interception features.
- The original complete GPLv3 text remains byte-for-byte unchanged in LICENSE, with COPYING as a pointer. Historical relocation maps remain documentation, not active source paths.
- Verify Python/Node regression tests, wheel and source archive hygiene, and six-platform CI after this cleanup. Synchronize both modernization and master through non-forced fast-forward, then verify the GitHub default root has no legacy folder.
- Remaining modernization: diverse actual authorized PCAP/PCAPNG captures, safe Scapy passive lab testing, browser accessibility/keyboard checks, provenance and module-by-module feature migration decisions.



This is an alpha modernization, not historical feature parity. Source paths below refer to historical files retained in the repository; presence is not proof of current compatibility.

| Historical capability | Evidence | Modern runtime status |
| --- | --- | --- |
| ARP observation and address inventory | utilities/arpwatch.py, utilities/scan.py | Classic PCAP/experimental PCAPNG analysis, VLAN and Linux cooked captures; optional passive Scapy adapter |
| ARP interception | utilities/arpmitm.py, utilities/rearp.py | Historical active implementation retained for reference, not ported; safe offline evidence analysis added where noted |
| DHCP race / rogue DHCP | utilities/dhcprace.py, utilities/dhcptools.py | Historical active implementation retained for reference, not ported; safe offline evidence analysis added where noted |
| WPAD / NetBIOS | utilities/wpadhijack.py, utilities/nbtools.py | Historical source retained; not ported |
| Wireless access point | utilities/apgen.py | Historical source retained; not ported |
| SSLStrip / interception proxy | sslstrip/, sslstrip.py, attackctrl.py | Historical source retained; not ported. New verified TLS endpoint inspection is a separate assessment function |
| HTTP / FTP credential handling | modules/harvester/ | Historical source retained; not ported |
| Session cookies | modules/sessionhijacking/ | Historical source retained; not ported |
| HTTP code injection | modules/httpcodeinjection/ | Historical source retained; not ported |
| Tunnel blocking and denial-of-service modules | modules/TunnelBlock/, modules/dos/ | Historical source retained; not ported |
| Django dashboard / plugins | main/, modules/, templates/ | New loopback dashboard supports evidence imports; historical plugin contracts not restored |
| Installation / updates | setup.py, update.py | Isolated pip installation replaces privileged installer; old installer retained in legacy/setup.py |
| POODLE / Heartbleed / SSLv3 downgrade | Historical README upcoming-content list | Announced in historical roadmap; no dedicated implementation found in inspected paths |

## Passive capture modernization

- DHCPv4: static UDP metadata decoder; reports message type, server identifier
  and presence of WPAD option 252, without retaining option contents.
  Historical DHCP race/rogue reply code is not part of the modern runtime.
- NetBIOS name service: offline first-level name-query decoder with WPAD
  observation; historical response/spoofing code is not part of the runtime.
- A bounded, deduplicated `network_evidence` summary is integrated into classic
  PCAP and experimental PCAPNG analysis and shown in the local dashboard.
  Ethernet/VLAN and Linux cooked v1/v2 IPv4 UDP are supported.
- These are passive parsers for unfragmented IPv4 UDP only. No DHCP/NBNS
  packet transmission, IPv4 reassembly, full DNS parser or live capture
  integration is claimed.

## New supported assessment paths

- Nmap XML imports include IPv4/IPv6 hosts, open ports, service names, product/version evidence and OS guesses.
- Optional `scan-services` performs a bounded, explicitly requested Nmap TCP-connect inventory for one IP and at most 32 TCP ports; it does not run during offline analysis.
- Transport review items identify service records lacking a recorded SSL tunnel. These are not confirmed vulnerabilities: STARTTLS, redirects and policy require separate verification.
- `inspect-tls` (CLI and loopback dashboard) verifies certificate trust and hostname, records the negotiated TLS version/cipher and checks imminent expiry. It does not perform interception, downgrade tests or exhaustive protocol enumeration.

## Compatibility and validation

The offline core has no runtime dependencies and targets Python 3.11+. Linux/Python 3.12 was exercised locally. The CI matrix requests Linux/Python 3.11–3.14 plus Windows/macOS/Python 3.12; results must be checked before expanding verified support claims. Live Scapy capture requires OS capture permissions and appropriate platform drivers. Nmap discovery requires Nmap installed separately. Neither live adapter was validated against a real network in this checkpoint. Experimental PCAPNG parsing covers enhanced packet (type 6), obsolete packet (type 2), and simple packet (type 3) blocks, plus timestamp offset options; only synthetic fixtures for these extensions have been validated on Linux/Python 3.14. Untimed simple packet host observations contain null first/last-seen fields when no timed evidence exists. Broader real capture compatibility is not yet validated.

## Next migration work

1. Expand PCAPNG regression coverage with real captures and additional malformed-input/resource-limit cases.
2. Expand real-capture interoperability checks and standalone DHCP/NBNS safety/regression tests; passive parsers already exist.
3. Review historical proxy and plugin contracts against modern TLS and browser protections, documenting protocol and environment constraints before implementation.
4. Verify live adapters in an isolated test network and reconcile historical functionality one module at a time.

The detailed legacy-to-modern mapping and acceptance conditions are in
[MIGRATION_MATRIX.md](MIGRATION_MATRIX.md).

## Optional live passive adapter (not yet validated on real interfaces)

`capture-protocols` supplements the ARP-only `capture` command with passive
DHCPv4 and NBNS observations on an explicitly selected interface. The Scapy
adapter uses packet filters, enforces time/packet limits and outputs only
bounded metadata. Tests use synthetic Scapy packet objects; driver and
privilege behavior in real environments remains unverified.

## Archived historical source paths

Original source names in the capability matrix are historical identifiers. They are now found beneath `legacy/historical-framework-2015-2016/`. Only the separately tested Python 3 package in src/subterfuge/ is an installed runtime.
