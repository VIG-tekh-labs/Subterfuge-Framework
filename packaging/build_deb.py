"""Build an amd64 Debian package from a Linux PyInstaller onedir bundle.

Required network tools are declared as Debian dependencies. apt install
./file.deb resolves them from the operator's configured, trusted repositories.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.0.0~a5-1"
FILENAME = "Subterfuge-2.0.0a5-Linux-amd64.deb"
DEB_DEPENDENCIES = [
    "nmap", "tshark", "mitmproxy",
    "libegl1", "libopengl0", "libxkbcommon0",
    "libxkbcommon-x11-0", "libxcb-cursor0",
]


def build(bundle: Path, output: Path) -> Path:
    if not sys.platform.startswith("linux") or sys.maxsize <= 2**32:
        raise RuntimeError("Debian builds require a 64-bit Linux runner.")
    executable = bundle / "Subterfuge"
    if not executable.is_file():
        raise RuntimeError(f"Missing frozen executable: {executable}")
    output.mkdir(parents=True, exist_ok=True)
    destination = output / FILENAME
    with tempfile.TemporaryDirectory(prefix="subterfuge-deb-") as temporary:
        stage = Path(temporary) / "pkg"
        app = stage / "opt/subterfuge-framework"
        app.parent.mkdir(parents=True)
        shutil.copytree(bundle, app, symlinks=False)
        # Executables in frozen app remain executable after packaging.
        (app / "Subterfuge").chmod(0o755)
        launch = stage / "usr/bin/subterfuge"
        launch.parent.mkdir(parents=True, exist_ok=True)
        launch.write_text(
            "#!/bin/sh\n"
            'exec /opt/subterfuge-framework/Subterfuge "$@"\n',
            encoding="utf-8",
        )
        launch.chmod(0o755)
        gui_launch = stage / "usr/bin/subterfuge-desktop"
        gui_launch.write_text(
            "#!/bin/sh\n"
            'exec /opt/subterfuge-framework/Subterfuge gui "$@"\n',
            encoding="utf-8",
        )
        gui_launch.chmod(0o755)
        desktop = stage / "usr/share/applications/subterfuge-framework.desktop"
        desktop.parent.mkdir(parents=True, exist_ok=True)
        desktop.write_text(
            "[Desktop Entry]\n"
            "Version=1.0\n"
            "Type=Application\n"
            "Name=Subterfuge Framework\n"
            "Comment=Native network assessment workspace\n"
            "Exec=/usr/bin/subterfuge-desktop\n"
            "TryExec=/usr/bin/subterfuge-desktop\n"
            "Icon=subterfuge-framework\n"
            "Terminal=false\n"
            "Categories=Network;Utility;\n"
            "StartupNotify=true\n", encoding="utf-8",
        )
        icon = stage / "usr/share/icons/hicolor/scalable/apps/subterfuge-framework.svg"
        icon.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / "src/subterfuge/assets/subterfuge.svg", icon)
        docs = stage / "usr/share/doc/subterfuge-framework"
        docs.mkdir(parents=True)
        for name in (
            "LICENSE", "COPYING", "PUBLICATION_POLICY.md",
            "DESKTOP_GUI.md", "SERVER_ACCESS.md", "THIRD_PARTY_NOTICES.md",
        ):
            shutil.copy2(ROOT / name, docs / name)
        control = stage / "DEBIAN/control"
        control.parent.mkdir(parents=True)
        control.write_text(
            "Package: subterfuge-framework\n"
            f"Version: {VERSION}\n"
            "Section: net\n"
            "Priority: optional\n"
            "Architecture: amd64\n"
            "Maintainer: Subterfuge contributors <noreply@github.com>\n"
            "Depends: " + ", ".join(DEB_DEPENDENCIES) + "\n"
            "Description: Native graphical network assessment workspace\n"
            " Subterfuge ships a self-contained Python and Qt GUI, offline\n"
            " capture analysis, TLS assessment and a loopback Web dashboard.\n"
            " Nmap, TShark and mitmproxy are installed by apt as package\n"
            " dependencies from the system's configured repositories.\n",
            encoding="utf-8",
        )
        subprocess.run(
            ["dpkg-deb", "--build", "--root-owner-group", str(stage), str(destination)],
            check=True,
        )
    if not destination.is_file() or destination.stat().st_size < 1_000_000:
        raise RuntimeError("Debian artifact missing or unexpectedly small.")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "release-assets")
    args = parser.parse_args()
    result = build(args.bundle.resolve(), args.output.resolve())
    print("DEBIAN_ARTIFACT", result, result.stat().st_size, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
