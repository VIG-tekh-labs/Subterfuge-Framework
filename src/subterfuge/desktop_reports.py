"""Native desktop report import and presentation, independent of Qt and HTML.

No browser rendering, no remote requests, no execution from imported JSON.
Only bounded, recognized fields are used in the GUI's read-only tables.
"""
from __future__ import annotations

from ipaddress import ip_address
from pathlib import Path
import json
import math

from .analysis import AnalysisError, MAX_FINDINGS, MAX_HOSTS

MAX_DESKTOP_JSON = 16 * 1024 * 1024
MAX_RENDER_ROWS = 5_000
MAX_JSON_PREVIEW = 200_000
MAX_TEXT = 2_048
MAX_REPORT_DEPTH = 9
MAX_ARRAY_LENGTH = 12_000


def _check_bounded(value: object, depth: int = 0) -> None:
    if depth > MAX_REPORT_DEPTH:
        raise AnalysisError("Saved report is too deeply nested.")
    if value is None or isinstance(value, bool) or isinstance(value, int):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise AnalysisError("Saved report contains a non-finite number.")
        return
    if isinstance(value, str):
        if len(value) > MAX_TEXT:
            raise AnalysisError("Saved report contains an excessively long text field.")
        return
    if isinstance(value, (list, tuple)):
        # Native TLS certificate parsers return nested tuple structures;
        # JSON export serializes those immutable tuples to ordinary arrays.
        if len(value) > MAX_ARRAY_LENGTH:
            raise AnalysisError("Saved report contains too many items.")
        for item in value:
            _check_bounded(item, depth + 1)
        return
    if isinstance(value, dict):
        if len(value) > 80:
            raise AnalysisError("Saved report contains too many object fields.")
        for key, item in value.items():
            if not isinstance(key, str) or len(key) > 96:
                raise AnalysisError("Saved report contains an invalid field name.")
            _check_bounded(item, depth + 1)
        return
    raise AnalysisError("Saved report contains an unsupported data type.")


def validate_saved_report(value: object) -> dict:
    """Fail closed on malformed reports; do not trust arbitrary JSON objects."""
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise AnalysisError("Expected a Subterfuge JSON report with schema_version 1.")
    for name in ("kind", "source"):
        if not isinstance(value.get(name), str) or not value[name].strip():
            raise AnalysisError(f"Saved report has an invalid {name}.")
    for name, limit in (("hosts", MAX_HOSTS), ("findings", MAX_FINDINGS),
                        ("warnings", MAX_FINDINGS)):
        group = value.get(name)
        if not isinstance(group, list) or len(group) > limit:
            raise AnalysisError(f"Saved report has invalid {name}.")
    if not isinstance(value.get("stats"), dict):
        raise AnalysisError("Saved report has invalid statistics.")
    _check_bounded(value)
    for host in value["hosts"]:
        if not isinstance(host, dict):
            raise AnalysisError("Saved report contains an invalid host.")
        addresses = host.get("addresses", [host.get("address")])
        if not isinstance(addresses, list) or len(addresses) > 128:
            raise AnalysisError("Saved report has invalid host addresses.")
        for item in addresses:
            if item is not None:
                if not isinstance(item, str):
                    raise AnalysisError("Saved report contains an invalid IP address.")
                try:
                    ip_address(item)
                except ValueError as exc:
                    raise AnalysisError("Saved report contains an invalid IP address.") from exc
        macs = host.get("mac_addresses", [])
        if not isinstance(macs, list) or len(macs) > 256 or any(
            not isinstance(item, str) for item in macs
        ):
            raise AnalysisError("Saved report contains invalid MAC values.")
        ports = host.get("ports", [])
        if not isinstance(ports, list) or len(ports) > 4096 or any(
            not isinstance(item, dict) for item in ports
        ):
            raise AnalysisError("Saved report contains invalid port records.")
    for finding in value["findings"]:
        if not isinstance(finding, dict) or not isinstance(finding.get("message"), str):
            raise AnalysisError("Saved report contains an invalid finding.")
    if any(not isinstance(warning, str) for warning in value["warnings"]):
        raise AnalysisError("Saved report contains an invalid warning.")
    return value


def read_saved_report(path: str | Path) -> dict:
    """Read at most 16 MiB from a local report file; do not follow directories."""
    path = Path(path).expanduser()
    if not path.is_file():
        raise AnalysisError("Select an existing regular JSON report file.")
    with path.open("rb") as handle:
        data = handle.read(MAX_DESKTOP_JSON + 1)
    if len(data) > MAX_DESKTOP_JSON:
        raise AnalysisError("JSON report exceeds the 16 MiB desktop import limit.")
    try:
        parsed = json.loads(
            data.decode("utf-8-sig"),
            parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
        )
    except (ValueError, UnicodeDecodeError) as exc:
        raise AnalysisError("Saved report is not valid UTF-8 JSON.") from exc
    return validate_saved_report(parsed)


def _display(value: object, length: int = 160) -> str:
    if value is None:
        return "—"
    if isinstance(value, (list, tuple)):
        result = ", ".join(str(part) for part in value[:6])
        if len(value) > 6:
            result += "…"
    elif isinstance(value, dict):
        result = ", ".join(f"{key}: {val}" for key, val in list(value.items())[:4])
    else:
        result = str(value)
    return result[:length] + ("…" if len(result) > length else "")


def report_summary(report: dict) -> dict:
    """Typed, bounded, inert values for all native report widgets."""
    validate_saved_report(report)
    hosts = []
    for host in report["hosts"][:MAX_RENDER_ROWS]:
        addr = host.get("address") or next(iter(host.get("addresses", [])), None)
        macs = host.get("mac_addresses", [])
        if "ports" in host:
            active = [item for item in host["ports"] if item.get("state") == "open"]
            description = f"{len(active)} port(s) ouvert(s)"
            if host.get("status"):
                description += f" · {host['status']}"
        else:
            description = f"{host.get('observations', 0)} observation(s)"
        hosts.append((_display(addr), _display(macs), description))
    findings = []
    for item in report["findings"][:MAX_RENDER_ROWS]:
        severity = _display(item.get("severity", "info"), 20)
        findings.append((
            severity, _display(item["message"], 420),
            _display(item.get("interpretation"), 580),
        ))
    evidence = []
    for item in report.get("network_evidence", [])[:MAX_RENDER_ROWS]:
        if not isinstance(item, dict):
            continue
        kind = item.get("kind", item.get("protocol", "network"))
        label = item.get("message_type", item.get("name", item.get("code", "observation")))
        evidence.append((_display(kind, 55), _display(label, 150),
                         _display(item.get("server_identifier", item.get("count", "")))))
    if not evidence:
        for item in report.get("observations", [])[:MAX_RENDER_ROWS]:
            if not isinstance(item, dict):
                continue
            evidence.append((
                _display(item.get("tag", item.get("message_type", "event")), 90),
                _display(item.get("ip", item.get("server_identifier", item.get("time"))), 160),
                _display(item.get("label", item.get("mac", "")), 160),
            ))
    stats = report.get("stats", {})
    packets = stats.get("packets", stats.get("arp_packets", stats.get("http_messages",
                           stats.get("total_events", stats.get("open_ports", 0)))))
    if isinstance(packets, bool) or not isinstance(packets, (int, float)):
        packets = 0
    return {
        "source": _display(report["source"], 256),
        "kind": _display(report["kind"], 80),
        "hosts_count": len(report["hosts"]),
        "findings_count": len(report["findings"]),
        "activity_count": int(packets),
        "hosts": hosts,
        "findings": findings,
        "evidence": evidence,
        "warnings": [w[:500] for w in report["warnings"][:200]],
        "tls": report.get("tls") if isinstance(report.get("tls"), dict) else None,
        "http": report.get("http", [])[:MAX_RENDER_ROWS],
    }


def report_preview(report: dict) -> str:
    """Cap raw JSON preview to avoid freezing the GUI on very large reports."""
    validate_saved_report(report)
    formatted = json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False)
    if len(formatted) > MAX_JSON_PREVIEW:
        return (
            "Rapport volumineux : utilisez « Enregistrer JSON » pour l'exporter. "
            "L'aperçu brut est limité à 200 000 caractères."
        )
    return formatted
