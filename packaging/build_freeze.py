"""Build a self-contained GUI executable using PyInstaller.

Build on each TARGET OS; cross-compiling Windows .exe from Linux is not
supported. This script creates no networking, persistence or elevated access.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import importlib.util
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def command(output: Path, *, windows: bool, dry_run: bool = False) -> list[str]:
    if not (ROOT / "packaging/desktop_launcher.py").is_file():
        raise RuntimeError("Desktop executable entrypoint is unavailable.")
    if importlib.util.find_spec("PyInstaller") is None:
        raise RuntimeError("PyInstaller must be installed into the build environment.")
    for name in ("PySide6", "scapy", "subterfuge"):
        if importlib.util.find_spec(name) is None:
            raise RuntimeError(f"Install the package '{name}' into the active build Python before freezing.")
    from importlib.metadata import distribution
    if distribution("subterfuge-framework").version != "2.0.0a5":
        raise RuntimeError("Build Python must contain the current Subterfuge 2.0.0a5.")
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    arguments = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm", "--clean", "--onedir", "--noupx",
        "--name", "Subterfuge",
        "--distpath", str(output),
        "--workpath", str(output / "build-cache"),
        "--specpath", str(output / "spec"),
        "--collect-data", "subterfuge",
        "--collect-submodules", "subterfuge",
        "--collect-submodules", "scapy",
        "--hidden-import", "PySide6.QtSvg",
    ]
    if windows:
        ico = ROOT / "packaging/subterfuge.ico"
        if not ico.is_file():
            raise RuntimeError("Generate packaging/subterfuge.ico first.")
        arguments.extend(["--windowed", "--icon", str(ico)])
    else:
        arguments.append("--console")
    arguments.append(str(ROOT / "packaging/desktop_launcher.py"))
    return arguments


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "dist-frozen")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    windows = sys.platform == "win32"
    builder = command(args.output, windows=windows, dry_run=args.dry_run)
    print("Freeze command:", " ".join(builder), flush=True)
    if args.dry_run:
        return 0
    subprocess.run(builder, cwd=ROOT, check=True)
    executable = args.output.resolve() / "Subterfuge" / (
        "Subterfuge.exe" if windows else "Subterfuge"
    )
    if not executable.is_file():
        raise RuntimeError("Frozen executable was not created.")
    print("FROZEN_EXECUTABLE=", executable, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
