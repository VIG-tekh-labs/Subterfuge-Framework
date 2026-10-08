#!/usr/bin/env python3
"""Compatibility notice for the retired Subterfuge SVN updater.

The historical script relied on Python 2, an obsolete SVN checkout, a remote
version socket and privileged system-wide installation. It must not execute.
"""
from __future__ import annotations

import argparse
from importlib import metadata


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Show supported update instructions.")
    parser.add_argument("--version", action="store_true", help="Show installed package version.")
    args = parser.parse_args(argv)
    if args.version:
        try:
            print(metadata.version("subterfuge-framework"))
        except metadata.PackageNotFoundError:
            print("Not installed; use an isolated virtual environment.")
        return 0
    print("The historical SVN auto-updater is retired.")
    print("For a Git checkout, review changes with 'git fetch' and 'git log' first.")
    print("After selecting a reviewed revision, activate your virtual environment")
    print("and run: python -m pip install --upgrade .")
    print("Never run legacy/update.py or legacy/setup.py on a host system.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
