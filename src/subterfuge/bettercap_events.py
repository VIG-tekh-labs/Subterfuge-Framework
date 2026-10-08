"""Offline, allowlisted summaries of Bettercap exported JSON observation events.

Accepts a user-provided JSON export of a Bettercap /api/events response.
Does not connect to, control, or start Bettercap or reproduce attack modules.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime
from ipaddress import ip_address
from pathlib import Path
import json
import re

from .analysis import AnalysisError, base_report, read_input

MAX_EVENTS = 10_000
ALLOWLIST = frozenset({
    "endpoint.new", "endpoint.lost", "gateway.change",
    "wifi.ap.new", "wifi.ap.lost", "wifi.client.new", "wifi.client.lost",
})
MAC_PATTERN = re.compile(r"^(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$")


def _as_address(value: object) -> str | None:
    if not isinstance(value, str) or len(value) > 45:
        return None
    try:
        result = ip_address(value)
    except ValueError:
        return None
    return str(result)


def _mac(value: object) -> str | None:
    return value.lower() if isinstance(value, str) and MAC_PATTERN.fullmatch(value) else None


def _name(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    name = "".join(ch for ch in value[:128] if ch.isprintable() and ch not in "\r\n\x00")
    return name or None


def import_bettercap_events(path: str | Path) -> dict:
    raw = read_input(path)
    try:
        events = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AnalysisError("Bettercap observation export must be valid UTF-8 JSON.") from exc
    if isinstance(events, dict) and set(events) == {"events"}:
        events = events["events"]
    if not isinstance(events, list) or len(events) > MAX_EVENTS:
        raise AnalysisError("Expected a JSON array of at most 10000 Bettercap events.")
    report = base_report("bettercap_events", Path(path).name)
    counters: Counter[str] = Counter()
    observations = []
    ignored = 0
    for event in events:
        if not isinstance(event, dict) or not isinstance(event.get("tag"), str):
            raise AnalysisError("Unexpected Bettercap event structure.")
        tag = event["tag"]
        if tag not in ALLOWLIST:
            ignored += 1
            continue
        data = event.get("data")
        if not isinstance(data, dict):
            ignored += 1
            continue
        timestamp = event.get("time")
        if not isinstance(timestamp, str) or len(timestamp) > 64:
            ignored += 1
            continue
        try:
            datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            ignored += 1
            continue
        summary = {
            "tag": tag,
            "time": timestamp,
            "ip": _as_address(data.get("ipv4")) or _as_address(data.get("ipv6")),
            "mac": _mac(data.get("mac")) or _mac(data.get("Mac")),
            "label": _name(data.get("hostname")) or _name(data.get("alias")),
        }
        counters[tag] += 1
        observations.append(summary)
    report["observations"] = observations
    report["stats"] = {
        "total_events": len(events), "accepted_events": len(observations),
        "ignored_events": ignored, "by_tag": dict(sorted(counters.items())),
    }
    report["warnings"].append(
        "This is a limited offline summary of user-exported discovery events. "
        "No active Bettercap network, spoofing, proxy or wireless modules were invoked."
    )
    return report
