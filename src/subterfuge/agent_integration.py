"""Optional local agent bridge with explicit capabilities and scoped actions.

Standalone Subterfuge works without any agent. If a local orchestrator
invokes the Python API, it must provide a scoped task policy. No external
policy is modified here. The bridge independently requires explicit permissions for risky operations.
"""
from __future__ import annotations

from pathlib import Path

from . import __version__
from .analysis import AnalysisError, analyze_nmap, analyze_pcap, read_input
from .environment import doctor, interfaces
from .demo import demo_report

ACTIONS = {
    "doctor": {"risk": "local", "network": False, "requires": []},
    "interfaces": {"risk": "local", "network": False, "requires": []},
    "demo": {"risk": "local", "network": False, "requires": []},
    "analyze_pcap": {"risk": "local", "network": False, "requires": ["file"]},
    "import_nmap": {"risk": "local", "network": False, "requires": ["file"]},
    "import_bettercap": {"risk": "local", "network": False, "requires": ["file"]},
    "tls_decrypt": {
        "risk": "sensitive", "network": False,
        "requires": ["file", "keylog"], "additional_gate": "allow_sensitive_tls",
    },
    "inspect_tls": {
        "risk": "active_network", "network": True,
        "requires": ["host"], "additional_gate": "allowed_targets",
    },
    "discover": {
        "risk": "active_network", "network": True,
        "requires": ["target"], "additional_gate": "allowed_targets",
    },
    "scan_services": {
        "risk": "active_network", "network": True,
        "requires": ["target"], "additional_gate": "allowed_targets",
    },
}
EXCLUDED = {
    "proxy-lab": "Launch explicitly from a visible user session after configuring own clients.",
    "capture": "Run explicitly with interface capture permissions and scope.",
    "capture-protocols": "Run explicitly with interface capture permissions and scope.",
}


def describe_capabilities() -> dict:
    return {
        "integration": "optional_local_agent",
        "version": __version__,
        "standalone_supported": True,
        "action_schema": ACTIONS,
        "interactive_only": EXCLUDED,
        "browser_companion": {
            "type": "Chromium Manifest V3",
            "persists_configuration": True,
            "host_scope": "http://127.0.0.1/* and recognized Subterfuge dashboard only",
            "third_party_hook": False,
            "credential_collection": False,
        },
        "policy": (
            "The calling agent must approve each task and provide its allowed_actions and scoped "
            "allowed_targets and allowed_files. Subterfuge enforces its own technical limits and "
            "never grants root to a calling agent or bypasses operating-system authorization."
        ),
    }


def run_authorized(action: str, args: dict, policy: dict) -> dict:
    """Run a validated, policy-authorized single action, with no shell execution."""
    if not isinstance(args, dict) or not isinstance(policy, dict):
        raise AnalysisError("Agent task arguments and mission policy must be mappings.")
    if action not in ACTIONS:
        raise AnalysisError("Unsupported or interactive-only agent action.")
    allowed = policy.get("allowed_actions", [])
    if not isinstance(allowed, list) or action not in allowed:
        raise AnalysisError("The calling agent's mission policy did not authorize this action.")
    needed = ACTIONS[action]["requires"]
    for key in needed:
        value = args.get(key)
        if not isinstance(value, str) or not value.strip():
            raise AnalysisError(f"Missing required agent argument: {key}.")
    if action == "tls_decrypt" and policy.get("allow_sensitive_tls") is not True:
        raise AnalysisError("TLS secret handling requires explicit mission authorization.")
    if "file" in needed or "keylog" in needed:
        approved_files = policy.get("allowed_files", [])
        if not isinstance(approved_files, list):
            raise AnalysisError("The caller's mission file scope must be a list of paths.")
        for key in ("file", "keylog"):
            if key not in needed:
                continue
            try:
                requested = Path(args[key]).expanduser().resolve(strict=True)
            except OSError as exc:
                raise AnalysisError("An authorized file is unavailable.") from exc
            accepted = []
            for entry in approved_files:
                if isinstance(entry, str):
                    accepted.append(Path(entry).expanduser().resolve(strict=False))
            if requested not in accepted:
                raise AnalysisError("Requested file is outside this mission's approved file scope.")
    if ACTIONS[action]["network"]:
        if policy.get("allow_active_network") is not True:
            raise AnalysisError("Active network access is not authorized in this mission.")
        targets = policy.get("allowed_targets", [])
        value = args.get("host") or args.get("target")
        if not isinstance(targets, list) or value not in targets:
            raise AnalysisError("Requested target is absent from the authorized mission scope.")
    if action == "doctor":
        return doctor()
    if action == "interfaces":
        return {"interfaces": interfaces()}
    if action == "demo":
        return demo_report()
    if action == "analyze_pcap":
        return analyze_pcap(read_input(args["file"]), Path(args["file"]).name)
    if action == "import_nmap":
        return analyze_nmap(read_input(args["file"]), Path(args["file"]).name)
    if action == "import_bettercap":
        from .bettercap_events import import_bettercap_events
        return import_bettercap_events(args["file"])
    if action == "tls_decrypt":
        from .tls_lab import decrypt_https
        # The optional agent bridge only returns minimal metadata; decrypted packet exports
        # and URI exposure require the visible standalone command instead.
        return decrypt_https(args["file"], args["keylog"])
    if action == "inspect_tls":
        from .tls import inspect_tls
        return inspect_tls(args["host"], int(args.get("port", 443)))
    if action == "discover":
        from .environment import discover
        return discover(args["target"])
    if action == "scan_services":
        from .environment import scan_services
        return scan_services(args["target"], str(args.get("ports", "22,80,443")))
    raise AnalysisError("Unknown agent action.")
