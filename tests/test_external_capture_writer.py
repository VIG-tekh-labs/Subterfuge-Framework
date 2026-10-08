"""Optional interoperability check with Wireshark editcap's PCAPNG output."""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from subterfuge.analysis import analyze_pcap
from subterfuge.demo import sample_capture


class ExternalCaptureWriterTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which("editcap"), "editcap is not installed")
    def test_editcap_generated_pcapng_matches_classic_pcap(self):
        with tempfile.TemporaryDirectory(prefix="subterfuge-editcap-") as folder:
            classic = Path(folder) / "fixture.pcap"
            converted = Path(folder) / "fixture.pcapng"
            classic.write_bytes(sample_capture())
            subprocess.run(["editcap", "-F", "pcapng", str(classic), str(converted)],
                           check=True, capture_output=True, timeout=20)
            original = analyze_pcap(classic.read_bytes())
            report = analyze_pcap(converted.read_bytes())
            self.assertEqual(report["kind"], "pcapng")
            self.assertEqual(report["stats"]["arp_packets"], original["stats"]["arp_packets"])
            self.assertEqual(report["stats"]["findings"], original["stats"]["findings"])


if __name__ == "__main__":
    unittest.main()