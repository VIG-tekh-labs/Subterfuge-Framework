"""Standalone native executable. The frozen runtime bundles Python and Qt.

No subprocess or web server is started until the user explicitly requests it.
This entrypoint retains CLI subcommands for headless and scripted server use.
"""
from __future__ import annotations

import sys

from subterfuge.cli import main as cli_main


def self_test() -> int:
    """Verify the bundled native Qt GUI without network requests or browser."""
    from PySide6.QtWidgets import QApplication
    from subterfuge.desktop import DesktopWindow
    from subterfuge.demo import demo_report

    app = QApplication.instance() or QApplication([])
    window = DesktopWindow()
    try:
        if window.pages.count() != 5 or window._web is not None:
            raise RuntimeError("Unexpected native desktop startup state.")
        window._render_report(demo_report())
        if window.host_table.rowCount() != 1:
            raise RuntimeError("Synthetic inventory failed to render.")
        window.show()
        app.processEvents()
        if window.grab().isNull():
            raise RuntimeError("Native Qt window did not paint.")
    finally:
        window.close()
        app.processEvents()
    print("SELF_TEST_GUI_OK", flush=True)
    return 0


if __name__ == "__main__":
    arguments = sys.argv[1:] or ["gui"]
    if arguments == ["--self-test"]:
        raise SystemExit(self_test())
    raise SystemExit(cli_main(arguments))
