"""Standalone native desktop console launcher with lazy Qt dependency."""

from .cli import main as cli_main


def main() -> int:
    return cli_main(["gui"])
