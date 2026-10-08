"""User-exported Bettercap events are analyzed without executing Bettercap."""
from pathlib import Path
import json
import tempfile
import unittest

from subterfuge.analysis import AnalysisError
from subterfuge.bettercap_events import import_bettercap_events


class BettercapEventsTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.file=Path(self.tmp.name)/"events.json"

    def write(self, events):
        self.file.write_text(json.dumps(events), encoding="utf-8")

    def test_allows_only_discovery_metadata(self):
        self.write([
            {"tag":"endpoint.new", "time":"2026-10-09T01:15:00Z",
             "data":{"ipv4":"192.0.2.4", "mac":"AA:BB:CC:00:01:02",
                     "hostname":"test-device", "secret":"must-not-leak"}},
            {"tag":"wifi.client.handshake", "time":"2026-10-09T01:16:00Z",
             "data":{"handshake":"private key material"}},
            {"tag":"http.spoofed-request", "time":"2026-10-09T01:17:00Z",
             "data":{"password":"never"}},
        ])
        report=import_bettercap_events(self.file)
        self.assertEqual(report["kind"],"bettercap_events")
        self.assertEqual(report["stats"]["accepted_events"],1)
        self.assertEqual(report["stats"]["ignored_events"],2)
        self.assertEqual(report["observations"][0]["mac"],"aa:bb:cc:00:01:02")
        serialized=json.dumps(report)
        self.assertNotIn("must-not-leak",serialized)
        self.assertNotIn("private key material",serialized)
        self.assertNotIn("never",serialized)

    def test_accepts_wrapped_export(self):
        self.write({"events":[
            {"tag":"gateway.change","time":"2026-10-09T01:15:00+00:00",
             "data":{"ipv4":"192.0.2.1"}}
        ]})
        report=import_bettercap_events(self.file)
        self.assertEqual(report["stats"]["accepted_events"],1)

    def test_rejects_malformed_json_and_structures(self):
        self.file.write_text("{bad")
        with self.assertRaises(AnalysisError):import_bettercap_events(self.file)
        self.write({"anything":"not array"})
        with self.assertRaises(AnalysisError):import_bettercap_events(self.file)
        self.write([0])
        with self.assertRaises(AnalysisError):import_bettercap_events(self.file)

    def test_caps_event_count(self):
        self.write([{"tag":"endpoint.new"}]*10001)
        with self.assertRaisesRegex(AnalysisError,"10000"):
            import_bettercap_events(self.file)


if __name__=="__main__":
    unittest.main()
