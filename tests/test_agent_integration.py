"""ZIA actions are policy-gated; standalone Subterfuge is independent."""
import unittest
from unittest.mock import patch

from subterfuge.agent_integration import describe_capabilities, run_authorized
from subterfuge.analysis import AnalysisError


class AgentPolicyTests(unittest.TestCase):
    def test_capabilities_exclude_persistent_third_party_hooks(self):
        data = describe_capabilities()
        self.assertTrue(data["standalone_supported"])
        self.assertFalse(data["browser_companion"]["third_party_hook"])
        self.assertNotIn("proxy-lab", data["action_schema"])
        self.assertIn("tls_decrypt", data["action_schema"])

    def test_denies_operations_missing_from_zia_policy(self):
        with self.assertRaises(AnalysisError):
            run_authorized("doctor", {}, {})
        with self.assertRaises(AnalysisError):
            run_authorized("proxy-lab", {}, {"allowed_actions": ["proxy-lab"]})

    def test_allows_local_diagnostic_with_policy(self):
        report = run_authorized("doctor", {}, {"allowed_actions": ["doctor"]})
        self.assertTrue(report["offline_analysis"])

    def test_network_requires_exact_approved_scope(self):
        with self.assertRaisesRegex(AnalysisError, "Active network"):
            run_authorized("inspect_tls", {"host": "example.test"}, {
                "allowed_actions": ["inspect_tls"], "allowed_targets": ["example.test"],
            })
        with self.assertRaisesRegex(AnalysisError, "scope"):
            run_authorized("inspect_tls", {"host": "other.test"}, {
                "allowed_actions": ["inspect_tls"], "allowed_targets": ["example.test"],
                "allow_active_network": True,
            })
        with patch("subterfuge.tls.inspect_tls", return_value={"verified": True}) as tested:
            result = run_authorized("inspect_tls", {"host": "example.test"}, {
                "allowed_actions": ["inspect_tls"], "allowed_targets": ["example.test"],
                "allow_active_network": True,
            })
        self.assertEqual(result, {"verified": True})
        tested.assert_called_once()

    def test_file_scope_is_required_in_zia_mission(self):
        from pathlib import Path
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "safe.json"
            path.write_text("[]", encoding="utf-8")
            policy = {"allowed_actions": ["import_bettercap"], "allowed_files": []}
            with self.assertRaisesRegex(AnalysisError, "file scope"):
                run_authorized("import_bettercap", {"file": str(path)}, policy)
            policy["allowed_files"] = [str(path)]
            report = run_authorized("import_bettercap", {"file": str(path)}, policy)
            self.assertEqual(report["stats"]["total_events"], 0)

    def test_tls_secrets_require_separate_permission(self):
        policy = {"allowed_actions": ["tls_decrypt"]}
        with self.assertRaisesRegex(AnalysisError, "mission"):
            run_authorized("tls_decrypt", {"file": "capture.pcap", "keylog": "keys.txt"}, policy)


if __name__ == "__main__":
    unittest.main()
