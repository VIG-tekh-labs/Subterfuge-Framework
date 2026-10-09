"""Bounded saved-report import and native table summaries with no GUI dependency."""
from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch

from subterfuge.analysis import AnalysisError
from subterfuge.demo import demo_report
from subterfuge.desktop_reports import (
    MAX_JSON_PREVIEW, read_saved_report, report_preview,
    report_summary, validate_saved_report,
)


class NativeReportTests(unittest.TestCase):
    def test_demo_summarizes_correctly(self):
        view = report_summary(demo_report())
        self.assertEqual(view["hosts_count"], 1)
        self.assertEqual(view["activity_count"], 2)
        self.assertEqual(view["findings_count"], 1)
        self.assertIn("192.0.2.10", view["hosts"][0][0])
        self.assertTrue(view["warnings"])

    def test_import_saved_report(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/"report.json"
            expected = demo_report()
            path.write_text(json.dumps(expected),encoding="utf-8")
            imported = read_saved_report(path)
            self.assertEqual(imported, expected)
            self.assertIn('"hosts"', report_preview(imported))

    def test_generic_nmap_host_and_ports_render(self):
        from subterfuge.analysis import analyze_nmap
        fixture = Path(__file__).parent/"fixtures/nmap_inventory.xml"
        result = report_summary(analyze_nmap(fixture.read_bytes()))
        self.assertEqual(result["hosts_count"], 2)
        self.assertIn("port(s)", result["hosts"][0][2])
        self.assertTrue(result["hosts"][1][0].startswith("2001:db8"))

    def test_tls_certificate_tuple_is_accepted_in_native_memory(self):
        from subterfuge.analysis import base_report
        report = base_report("tls", "localhost")
        report["tls"] = {
            "host": "localhost", "port": 443,
            "certificate_verified": True,
            "subject": ((("commonName", "localhost"),),),
            "issuer": ((("commonName", "Local CA"),),),
        }
        summary = report_summary(report)
        self.assertEqual(summary["kind"], "tls")
        self.assertIn("commonName", report_preview(report))

    def test_bettercap_metadata_render(self):
        from subterfuge.bettercap_events import import_bettercap_events
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"events.json"
            path.write_text(json.dumps([{
                "tag":"endpoint.new", "time":"2026-10-09T02:00:00Z",
                "data":{"ipv4":"192.0.2.7","mac":"02:00:00:00:00:07"},
            }]))
            summary=report_summary(import_bettercap_events(path))
            self.assertEqual(summary["activity_count"],1)
            self.assertEqual(summary["evidence"][0][0],"endpoint.new")

    def test_rejects_arbitrary_object_and_nan(self):
        invalid = [
            {}, [], 3, {"schema_version":2},
            {"schema_version":1,"kind":"demo","source":"s","hosts":[],"warnings":[], "findings":[], "stats":{"x":float("nan")}},
        ]
        for item in invalid:
            with self.subTest(item=item), self.assertRaises(AnalysisError):
                validate_saved_report(item)

    def test_malformed_host_finding_and_warning_rejected(self):
        base=demo_report()
        for key, value in [
            ("hosts",[{"address":"192.0.2.999","mac_addresses":[]}]),
            ("findings",["not a finding"]),
            ("warnings",[{"arbitrary":"object"}]),
        ]:
            with self.subTest(key=key):
                modified={**base,key:value}
                with self.assertRaises(AnalysisError):
                    report_summary(modified)

    def test_dangerous_markup_is_plain_text_not_executed(self):
        doc=demo_report()
        doc["findings"][0]["message"]="<img src=x onerror=alert(1)>"
        view=report_summary(doc)
        self.assertEqual(view["findings"][0][1],"<img src=x onerror=alert(1)>")

    def test_rejects_oversized_and_nested(self):
        report=demo_report()
        report["extra"]={"x":{"x":{"x":{"x":{"x":{"x":{"x":{"x":{"x":"x"}}}}}}}}}
        with self.assertRaises(AnalysisError):
            validate_saved_report(report)
        report=demo_report()
        report["source"]="a"*3000
        with self.assertRaises(AnalysisError):
            validate_saved_report(report)

    def test_input_limit(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"too_big.json"
            with path.open("wb") as f:
                f.write(b"0"*(16*1024*1024+1))
            with self.assertRaises(AnalysisError):
                read_saved_report(path)

    def test_json_preview_is_bounded(self):
        report=demo_report()
        # The preview is capped without exposing excess characters to Qt.
        with patch("subterfuge.desktop_reports.MAX_JSON_PREVIEW", 32):
            preview=report_preview(report)
        self.assertIn("Rapport volumineux",preview)

    def test_no_html_or_script_execution(self):
        from subterfuge import desktop_reports
        self.assertFalse(hasattr(desktop_reports,"QWebEngineView"))
        self.assertFalse(hasattr(desktop_reports,"eval"))


if __name__=="__main__":
    unittest.main()
