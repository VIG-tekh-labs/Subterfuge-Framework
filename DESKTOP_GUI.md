# Subterfuge Desktop — native Qt application (2.0.0a4 alpha)

The native desktop application is an optional alternative to Subterfuge's
existing Web dashboard. It uses PySide6/Qt Widgets, not Chromium, an embedded
browser, an HTTP server or a WebView. It runs independently on the computer.

## Installation

Python 3.11+ is required. In a fresh virtual environment:

    git clone https://github.com/VIG-tekh-labs/Subterfuge-Framework.git
    cd Subterfuge-Framework
    python3 -m venv .venv
    . .venv/bin/activate
    python -m pip install ".[desktop]"
    subterfuge gui

The independent GUI executable is also available:

    subterfuge-desktop

The core CLI and the Web dashboard remain installable with pip install .
without any Qt dependency. To install a native application-menu launcher
on a compatible Linux/XDG desktop:

    subterfuge desktop-shortcut

This creates a per-user desktop file and a local SVG icon under XDG_DATA_HOME
(or ~/.local/share), without root privileges. It refuses to replace an
unexpected existing launcher. The shortcut invokes the Python interpreter
associated with the installation; retain that virtual environment.
On Windows and macOS, use subterfuge-desktop for now. Native OS installers
are not yet provided.

## Native application screens

1. Vue d'ensemble — the selected report: host/IP/MAC inventory, activity,
   findings, interpretations, DHCP/NetBIOS evidence, warnings, synthetic demo,
   capture import and JSON export.
2. Fichiers & rapports — import PCAP/PCAPNG, Nmap XML, offline Bettercap
   discovery events, and saved Subterfuge JSON. A capped read-only JSON
   preview and export function are available.
3. Réseau — list interfaces, explicitly requested Nmap host discovery or
   light TCP service inventory, optional passive ARP or ARP/DHCP/NBNS capture,
   duration selection and network activity confirmation.
4. TLS / HTTPS — TLS endpoint check; PCAP and matching authorized SSLKEYLOGFILE
   for offline TShark-assisted inspection; opt-in URI and decrypted detail
   export. A loopback-only regular mitmproxy test proxy is started/stopped
   explicitly and requires manual client configuration.
5. Paramètres — runtime diagnostics, Linux user-menu shortcut, about text,
   and an explicit start/stop control for the optional localhost Web server.
   The native GUI does not open a browser automatically.

Analysis and capture operations execute in Qt worker threads to keep the
interface responsive. Reports are read with bounded JSON validation.
Untrusted report strings display as plain text, never HTML or JavaScript.

## Offline and security behavior

- No Web server is started when launching the native desktop GUI.
- No automatic network discovery, TLS scanning or packet capture on startup.
- No telemetry or remote login.
- Active operations require an explicitly specified target/interface and
  confirmation. Host OS permissions and external tool availability apply.
- The native GUI and the Web dashboard are deliberately separate commands.
- TLS decryption still needs matching session secrets; a handshake alone
  and temporary device disconnection do not reveal TLS secrets.
- The proxy uses explicit loopback clients; it does not alter routes,
  install certificates or hook third-party browser sessions.

## Browser and future phone support

The existing loopback browser dashboard is retained, not replaced. It can
be evolved toward mobile-friendly use independently of this Qt desktop app.
There is no Android APK or native iOS application in this release. The phone
cannot automatically access a PC's localhost; future remote/mobile access
will require its own authenticated secure transport.

## Quality checks

- Pure Python unit tests validate report schema/limits, table summarization
  and per-user desktop shortcut behavior without requiring Qt.
- Optional Qt tests create the five-screen application, render demo and
  untrusted text, check background operation and lack of automatic network
  calls, and produce an offscreen screenshot.
- Linux Qt CI uses QT_QPA_PLATFORM=offscreen, QT_QPA_PLATFORMTHEME empty and
  QT_STYLE_OVERRIDE=Fusion.
- Windows/macOS live desktop integration needs further manual QA. The core
  cross-platform tests continue to run without Qt.

## Server mode and address/port access

The existing Web interface remains available with subterfuge serve --port 8080.
For a headless server, keep the internal HTTP listener on 127.0.0.1 and
either forward it through an SSH tunnel to your computer or place it behind
a trusted HTTPS reverse proxy with mandatory authentication.

Secure remote URL example: https://192.0.2.10:8443/ behind an explicitly
configured HTTPS reverse proxy. The remote HTTPS browser Origin can be
declared with subterfuge serve --port 8080 --public-origin
https://192.0.2.10:8443. The HTTP backend itself always stays on loopback.
Detailed setup steps are in SERVER_ACCESS.md.

The native desktop GUI remains an entirely separate launch mode, and is
never required on a server.
