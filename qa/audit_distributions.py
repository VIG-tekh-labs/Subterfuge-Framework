"""Audit wheel and source archive membership without executing packaged code."""
from __future__ import annotations

import argparse
from pathlib import Path, PurePosixPath
import tarfile
import zipfile

BANNED_COMPONENTS = {
    "legacy", "modules", "main", "cease", "sslstrip", "utilities", "templates",
}
BANNED_NAMES = {
    "cert.pem", "credentials.txt", "base_db", "db",
    "settings.pyc", "ftp_password_sniffer.py",
}
BANNED_SUFFIXES = (".pem", ".key", ".p12", ".pfx", ".db", ".sqlite",
                   ".sqlite3", ".log", ".pyc")
REQUIRED_SDIST = {
    "PUBLICATION_POLICY.md", "COPYING", "LICENSE", "README.md", "HANDOFF.md", "SECURITY.md", "LICENSING.md",
    "MODERNIZATION_STATUS.md", "LEGACY_AGE_REVIEW_2026-10-08.md",
    "FILE_AGE_INVENTORY_2026-10-08.csv",
    "STALE_24H_REVIEW_2026-10-08.md", "FILE_REVIEW_OLDER_24H_2026-10-08.csv",
    "LEGACY_ARCHIVE_FILE_MAP_2026-10-09.csv", "LEGACY_REORGANIZATION_2026-10-09.md",
    "TLS_BROWSER_LAB_2026-10-09.md",
    "qa/loopback_nmap_smoke.py", "qa/browser_report_smoke.cjs",
    "qa/browser_lab_validation.mjs",
    "qa/browser_report_validation.mjs", "qa/audit_distributions.py",
}
REQUIRED_WHEEL = {
    "subterfuge/analysis.py", "subterfuge/cli.py",
    "subterfuge/static/index.html", "subterfuge/tls_lab.py",
    "subterfuge/bettercap_events.py", "subterfuge/agent_integration.py",
    "subterfuge/browser_lab/manifest.json",
    "subterfuge/browser_lab/content.js",
    "subterfuge/browser_lab/popup.html",
    "subterfuge/browser_lab/popup.js",
    "subterfuge/browser_lab/popup.css",
}


def forbidden(name: str) -> bool:
    path = PurePosixPath(name)
    return (any(component in BANNED_COMPONENTS for component in path.parts)
            or path.name in BANNED_NAMES or name.endswith(BANNED_SUFFIXES))


def audit(path: Path) -> tuple[int, int]:
    wheels = list(path.glob("*.whl"))
    archives = list(path.glob("*.tar.gz"))
    if len(wheels) != 1 or len(archives) != 1:
        raise ValueError("Expected exactly one wheel and one source archive.")
    with zipfile.ZipFile(wheels[0]) as archive:
        wheel_files = set(item.filename for item in archive.infolist()
                          if not item.is_dir())
        license_members = [name for name in wheel_files
                           if name.endswith(".dist-info/licenses/LICENSE")]
        if len(license_members) != 1:
            raise ValueError("Wheel must include the complete GPL license.")
        from hashlib import sha256
        if sha256(archive.read(license_members[0])).hexdigest() != (
            "8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903"
        ):
            raise ValueError("Wheel license bytes are not the original GPL text.")
    with tarfile.open(archives[0], "r:gz") as archive:
        source_files = set()
        for item in archive:
            if not item.isfile():
                continue
            parts = PurePosixPath(item.name).parts
            if len(parts) < 2:
                raise ValueError("Unexpected source archive layout.")
            source_files.add(PurePosixPath(*parts[1:]).as_posix())
    bad_wheel = sorted(name for name in wheel_files if forbidden(name))
    bad_source = sorted(name for name in source_files if forbidden(name))
    if bad_wheel or bad_source:
        raise ValueError(f"Historical or sensitive files included: wheel={bad_wheel}, source={bad_source}")
    missing_wheel = sorted(REQUIRED_WHEEL - wheel_files)
    missing_source = sorted(REQUIRED_SDIST - source_files)
    if missing_wheel or missing_source:
        raise ValueError(f"Missing distribution entries: wheel={missing_wheel}, source={missing_source}")
    if not any(name.endswith(".dist-info/METADATA") for name in wheel_files):
        raise ValueError("Missing wheel license/packaging metadata.")
    print(f"Distribution audit OK: wheel {len(wheel_files)} files; source {len(source_files)} files.")
    return len(wheel_files), len(source_files)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Subterfuge distribution memberships.")
    parser.add_argument("dist", type=Path, nargs="?", default=Path("dist"))
    args = parser.parse_args()
    audit(args.dist)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
