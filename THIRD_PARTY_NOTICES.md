# Third-party runtime components

Subterfuge Framework's own source code and corresponding source availability
remain governed by the original GPL-3.0-or-later license in LICENSE.

Official desktop installers bundle Python, Qt for Python (PySide6),
and Scapy dependencies as permitted by their respective licenses.
Build dependencies include PyInstaller and Pillow. The exact frozen build
manifest and release source are available at the release's corresponding
Git commit, and no vendor binaries are added to the public source tree.

Qt / PySide6 have open-source license obligations (LGPL/GPL; see the official
Qt for Python license information and any notices shipped with the wheels).
Packaging must preserve required Qt/PySide6 license notices and allow the
legally required notices and corresponding source access.

The Linux .deb declares system dependencies on Nmap, Wireshark/TShark and
mitmproxy. Those programs are installed separately by the system package
manager from repositories trusted/configured by the user, not silently
redistributed inside the .deb.

The Windows installer includes a separate, user-selectable task to obtain
Nmap, Wireshark/TShark and mitmproxy through Windows Package Manager.
They are not bundled in Subterfuge's EXE. Internet access, WinGet,
permissions, package agreements and possibly a packet-capture driver
may be necessary. Installation or functionality is not guaranteed on
locked-down or offline machines.

The project makes no assertion that it owns any third-party trademark.
