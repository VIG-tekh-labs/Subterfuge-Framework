"""Native Qt smoke checks. Without optional PySide6, core tests still run."""
import os
import unittest
from unittest.mock import patch

try:
    from PySide6.QtCore import Qt, QTimer
    from PySide6.QtWidgets import QApplication, QPushButton, QTableWidget
    from subterfuge.desktop import DesktopWindow, _perform_job
    HAS_QT = True
except ImportError:
    HAS_QT = False

from subterfuge.demo import demo_report
from subterfuge.analysis import AnalysisError


@unittest.skipUnless(HAS_QT, "Optional Qt dependency is not installed")
class NativeWindowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        cls.app.setQuitOnLastWindowClosed(False)

    def setUp(self):
        self.window = DesktopWindow()

    def tearDown(self):
        self.window.close()
        self.app.processEvents()

    def test_window_is_native_without_browser_engine(self):
        self.assertEqual(self.window.pages.count(),5)
        self.assertIn("Subterfuge",self.window.windowTitle())
        self.assertIsInstance(self.window.host_table,QTableWidget)
        self.assertEqual(self.window._proxy,None)
        self.assertFalse(self.window._busy)
        self.assertEqual(len(self.window.findChildren(QPushButton))>10,True)

    def test_all_pages_and_demo_are_accessible(self):
        for page in range(5):
            self.window._navigate(page)
            self.assertEqual(self.window.pages.currentIndex(),page)
            self.assertTrue(self.window._nav_buttons[page].property("active"))
        self.window._render_report(demo_report())
        self.assertEqual(self.window.metric_hosts.text(),"1")
        self.assertEqual(self.window.metric_findings.text(),"1")
        self.assertEqual(self.window.host_table.rowCount(),1)
        self.assertEqual(self.window.findings_table.rowCount(),1)
        self.assertEqual(self.window.pages.currentIndex(),0)

    def test_untrusted_html_is_displayed_as_plain_text(self):
        report=demo_report()
        report["source"]="<b>unsafe markup</b>"
        self.window._render_report(report)
        self.assertEqual(self.window.overview_source.textFormat(),Qt.TextFormat.PlainText)
        self.assertIn("<b>unsafe markup</b>",self.window.overview_source.text())

    def test_no_network_request_during_startup(self):
        with patch("socket.create_connection",side_effect=AssertionError("Unexpected socket open")):
            with patch("subterfuge.environment.discover",side_effect=AssertionError("unexpected discover")):
                instance=DesktopWindow()
                self.assertIsNone(instance._report)
                instance.close()

    def test_demo_worker_does_not_block_window(self):
        self.window._launch("demo",{})
        self.assertTrue(self.window._busy)
        for _ in range(120):
            self.app.processEvents()
            if not self.window._busy:
                break
            self.app.thread().msleep(10)
        self.assertFalse(self.window._busy)
        self.assertEqual(self.window.metric_hosts.text(),"1")

    def test_offscreen_screenshot_possible(self):
        self.window._render_report(demo_report())
        self.window.show()
        self.app.processEvents()
        pixmap=self.window.grab()
        self.assertFalse(pixmap.isNull())
        self.assertGreaterEqual(pixmap.width(),900)
        self.window.hide()


if __name__=="__main__":
    unittest.main()
