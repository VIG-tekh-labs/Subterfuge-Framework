"""Explicit, per-user desktop shortcut installer for Linux XDG desktops."""
from __future__ import annotations

from importlib.resources import files
from pathlib import Path
import os
import sys
import tempfile

from .analysis import AnalysisError


def _safe_quote(value: str) -> str:
    if any(character in value for character in ("\n", "\r", "\x00")):
        raise AnalysisError("Unsafe executable path.")
    # Desktop Entry command values need quoted backslash/quotes and no shell.
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("%", "%%") + '"'


def _atomic_write(path: Path, data: bytes, mode: int = 0o644) -> None:
    if path.is_symlink():
        raise AnalysisError("Refusing to replace a symbolic-link shortcut.")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=path.parent, prefix=".subterfuge-", delete=False
        ) as handle:
            temporary = Path(handle.name)
            os.chmod(temporary, mode)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _expected_entry(executable: Path) -> bytes:
    """Build the exact launcher content without writing to the filesystem."""
    launch_arguments = "" if getattr(sys, "frozen", False) else " -m subterfuge gui"
    return (
        "[Desktop Entry]\n"
        "Type=Application\n"
        "Name=Subterfuge Framework\n"
        "GenericName=Network analysis workstation\n"
        "Comment=Native Qt interface for local network assessments\n"
        f"Exec={_safe_quote(str(executable))}{launch_arguments}\n"
        "TryExec=" + str(executable) + "\n"
        "Icon=subterfuge-framework\n"
        "Terminal=false\n"
        "Categories=Network;Utility;\n"
        "StartupNotify=true\n"
    ).encode("utf-8")


def remove_shortcut() -> dict:
    """Remove only the shortcut and icon belonging to this Python installation.

    A customized shortcut or replaced icon is never deleted automatically.
    """
    if not sys.platform.startswith("linux"):
        raise AnalysisError("Menu shortcuts are currently supported on Linux XDG desktops.")
    root = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share").expanduser()
    if not root.is_absolute():
        raise AnalysisError("XDG_DATA_HOME must be an absolute directory.")
    shortcut = root / "applications/subterfuge-framework.desktop"
    icon = root / "icons/hicolor/scalable/apps/subterfuge-framework.svg"
    if shortcut.is_symlink():
        raise AnalysisError("Refusing to remove a symbolic-link shortcut.")
    if not shortcut.exists():
        return {"shortcut_removed": False, "icon_removed": False}
    if not shortcut.is_file() or shortcut.read_bytes() != _expected_entry(Path(sys.executable)):
        raise AnalysisError("Existing shortcut differs from this installation; refusing removal.")
    shortcut.unlink()
    removed_icon = False
    if icon.is_file() and not icon.is_symlink():
        bundled_icon = files("subterfuge").joinpath("assets/subterfuge.svg").read_bytes()
        if icon.read_bytes() == bundled_icon:
            icon.unlink()
            removed_icon = True
    return {"shortcut_removed": True, "icon_removed": removed_icon}


def install_shortcut() -> Path:
    if not sys.platform.startswith("linux"):
        raise AnalysisError("Menu shortcuts are currently supported on Linux XDG desktops.")
    root = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share").expanduser()
    if not root.is_absolute():
        raise AnalysisError("XDG_DATA_HOME must be an absolute directory.")
    applications = root / "applications"
    icons = root / "icons/hicolor/scalable/apps"
    applications.mkdir(parents=True, exist_ok=True)
    icons.mkdir(parents=True, exist_ok=True)
    shortcut = applications / "subterfuge-framework.desktop"
    icon = icons / "subterfuge-framework.svg"
    executable = Path(sys.executable)
    if not executable.is_absolute() or not executable.is_file():
        raise AnalysisError("Could not locate a reliable Python executable.")
    entry = _expected_entry(executable)
    if shortcut.exists() and (not shortcut.is_file() or shortcut.read_bytes() != entry):
        raise AnalysisError(
            "An existing Subterfuge menu shortcut differs. Review it manually before replacement."
        )
    if icon.is_symlink():
        raise AnalysisError("Refusing to use a symbolic-link icon.")
    if not icon.exists():
        image = files("subterfuge").joinpath("assets/subterfuge.svg").read_bytes()
        _atomic_write(icon, image)
    if not shortcut.exists():
        _atomic_write(shortcut, entry)
    return shortcut


def main() -> int:
    try:
        location = install_shortcut()
    except (AnalysisError, OSError) as exc:
        print("Error:", exc, file=sys.stderr)
        return 2
    print("Native application shortcut:", location)
    return 0
