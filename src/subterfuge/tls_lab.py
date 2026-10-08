"""Explicitly authorized TLS inspection: offline TShark and opt-in HTTP proxy.

Never extracts session keys from handshakes, changes a gateway, or redirects
other devices. Decrypted application payloads are saved only when requested.
"""
from __future__ import annotations

from datetime import datetime, timezone
from ipaddress import ip_address
from pathlib import Path
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile

from .analysis import AnalysisError, MAX_INPUT_BYTES, MAX_PACKETS, base_report

MAX_KEYLOG_BYTES = 4 * 1024 * 1024
MAX_DETAIL_BYTES = 32 * 1024 * 1024
MAX_HTTP_ROWS = 20_000
MAX_TIMEOUT_SECONDS = 300
KEY_LABELS = {
    "CLIENT_RANDOM",
    "CLIENT_EARLY_TRAFFIC_SECRET",
    "EARLY_EXPORTER_SECRET",
    "CLIENT_HANDSHAKE_TRAFFIC_SECRET",
    "SERVER_HANDSHAKE_TRAFFIC_SECRET",
    "CLIENT_TRAFFIC_SECRET_0",
    "SERVER_TRAFFIC_SECRET_0",
    "EXPORTER_SECRET",
}
HEX = re.compile(r"^[0-9a-fA-F]+$")
FIELDS = [
    "frame.number", "tcp.stream", "ip.src", "ipv6.src", "ip.dst",
    "ipv6.dst", "http.request.method", "http.host",
    "http.request.uri", "http.response.code",
    "http2.headers.method", "http2.headers.authority",
    "http2.headers.path", "http2.headers.status",
]
DECRYPTED_HTTP_FILTER = (
    "tls && (http.request || http.response || "
    "http2.headers.method || http2.headers.status)"
)


def _regular_input(value: Path | str, *, private: bool, limit: int) -> Path:
    path = Path(value).expanduser()
    if path.is_symlink():
        raise AnalysisError("Symbolic-link inputs are not permitted for TLS inspection.")
    try:
        info = path.stat()
    except OSError as exc:
        raise AnalysisError("Input file is unavailable: " + str(path)) from exc
    if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= limit:
        raise AnalysisError(f"Input must be a nonempty regular file no larger than {limit} bytes.")
    if private:
        if hasattr(os, "getuid") and info.st_uid != os.getuid():
            raise AnalysisError("TLS secrets must belong to the current user.")
        if os.name == "posix" and info.st_mode & 0o077:
            raise AnalysisError("TLS key-log permissions must be private (chmod 600).")
    return path.resolve(strict=True)


def _validate_keylog(path: Path) -> int:
    with path.open("rb") as handle:
        content = handle.read(MAX_KEYLOG_BYTES + 1)
    if len(content) > MAX_KEYLOG_BYTES or b"\x00" in content:
        raise AnalysisError("TLS key log exceeds the limit or contains binary data.")
    try:
        lines = content.decode("ascii").splitlines()
    except UnicodeDecodeError as exc:
        raise AnalysisError("TLS key logs must contain ASCII key-log entries.") from exc
    count = 0
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split()
        if (len(fields) != 3 or fields[0] not in KEY_LABELS
                or len(fields[1]) != 64 or not HEX.fullmatch(fields[1])
                or len(fields[2]) < 32 or len(fields[2]) > 512
                or len(fields[2]) % 2 or not HEX.fullmatch(fields[2])):
            raise AnalysisError("Invalid or unsupported SSLKEYLOGFILE entry; no key value is exposed.")
        count += 1
    if count == 0:
        raise AnalysisError("The TLS key-log file contains no usable session-secret entries.")
    return count


def _validate_capture(path: Path) -> None:
    with path.open("rb") as handle:
        signature = handle.read(4)
    if signature not in (
        b"\xd4\xc3\xb2\xa1", b"\xa1\xb2\xc3\xd4",
        b"\x4d\x3c\xb2\xa1", b"\xa1\xb2\x3c\x4d",
        b"\x0a\x0d\x0d\x0a",
    ):
        raise AnalysisError("Only PCAP or PCAPNG files are accepted.")


def _tshark_command(capture: Path, keylog: Path, maximum_frames: int) -> list[str]:
    executable = shutil.which("tshark")
    if executable is None:
        raise AnalysisError("TShark is required; install Wireshark/TShark separately.")
    return [
        executable, "-n", "-r", str(capture),
        "-o", "tls.keylog_file:" + str(keylog),
        "-c", str(maximum_frames),
        "-Y", DECRYPTED_HTTP_FILTER,
    ]


def _run_tshark(command: list[str], *, timeout: int, stdout=None) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE if stdout is None else stdout,
            stderr=subprocess.PIPE, timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise AnalysisError("TShark reached the analysis time limit.") from exc
    except OSError as exc:
        raise AnalysisError("TShark could not start: " + str(exc)[:180]) from exc
    if result.returncode:
        stderr = result.stderr.decode("utf-8", errors="replace")[:350]
        raise AnalysisError("TShark failed: " + stderr.strip())
    return result


def _output_destination(value: Path | str, inputs: tuple[Path, ...]) -> Path:
    destination = Path(value).expanduser()
    if destination.is_symlink() or destination.is_dir():
        raise AnalysisError("Choose a new ordinary file for decrypted details.")
    if destination.exists():
        raise AnalysisError("Decrypted export already exists; refusing to overwrite it.")
    parent = destination.parent.resolve(strict=True)
    resolved = parent / destination.name
    if resolved in inputs:
        raise AnalysisError("Refusing to replace an input file.")
    return resolved


def _export_decrypted_json(command: list[str], output: Path, timeout: int) -> None:
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=output.parent, prefix=".subterfuge-tls-", suffix=".json",
            delete=False, mode="wb",
        ) as handle:
            temporary = Path(handle.name)
            os.chmod(temporary, 0o600)
            _run_tshark(command + ["-T", "json"], timeout=timeout, stdout=handle)
            handle.flush()
            os.fsync(handle.fileno())
        if temporary.stat().st_size > MAX_DETAIL_BYTES:
            raise AnalysisError("Decrypted packet details exceed the 32 MiB export limit.")
        with temporary.open("rb") as handle:
            try:
                loaded = json.load(handle)
            except (ValueError, UnicodeDecodeError) as exc:
                raise AnalysisError("TShark returned invalid decrypted JSON.") from exc
        if not isinstance(loaded, list):
            raise AnalysisError("Decrypted packet export has an unexpected structure.")
        if output.exists():
            raise AnalysisError("Output was created during analysis; refusing to replace it.")
        os.replace(temporary, output)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def decrypt_https(
    capture: Path | str,
    keylog: Path | str,
    *,
    include_uris: bool = False,
    export_json: Path | str | None = None,
    maximum_frames: int = 100_000,
    timeout: int = 120,
) -> dict:
    """Decode HTTPS sessions for which matching authorized TLS secrets exist.

    The safe JSON report contains only HTTP metadata; decrypted packet details
    including sensitive headers/content require an explicit 0600 local export.
    """
    if not 1 <= maximum_frames <= MAX_PACKETS:
        raise AnalysisError(f"Limit the capture to between 1 and {MAX_PACKETS} frames.")
    if not 1 <= timeout <= MAX_TIMEOUT_SECONDS:
        raise AnalysisError(f"Analysis timeout must be within 1–{MAX_TIMEOUT_SECONDS} seconds.")
    source = _regular_input(capture, private=False, limit=MAX_INPUT_BYTES)
    secrets = _regular_input(keylog, private=True, limit=MAX_KEYLOG_BYTES)
    if source == secrets:
        raise AnalysisError("Capture and TLS key log must be separate files.")
    _validate_capture(source)
    key_count = _validate_keylog(secrets)
    destination = _output_destination(export_json, (source, secrets)) if export_json else None
    base = _tshark_command(source, secrets, maximum_frames)
    field_command = base + [
        "-T", "fields", "-E", "separator=/t", "-E", "quote=n",
        "-E", "occurrence=f",
    ]
    for field in FIELDS:
        field_command.extend(("-e", field))
    raw = _run_tshark(field_command, timeout=timeout).stdout
    if len(raw) > MAX_DETAIL_BYTES:
        raise AnalysisError("Too many decrypted HTTP records for a single analysis.")
    try:
        lines = raw.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise AnalysisError("TShark returned invalid UTF-8 metadata.") from exc
    if len(lines) > MAX_HTTP_ROWS:
        raise AnalysisError("Too many decrypted HTTP records; use a smaller capture.")
    report = base_report("tls_decryption", source.name)
    entries = []
    for line in lines:
        values = line.split("\t")
        values += [""] * (len(FIELDS) - len(values))
        if len(values) != len(FIELDS):
            raise AnalysisError("Unexpected TShark HTTP output format.")
        packet, stream, ipv4src, ipv6src, ipv4dst, ipv6dst, method, host, uri, status, h2method, h2host, h2path, h2status = values
        try:
            frame_num = int(packet)
            stream_num = int(stream)
        except ValueError as exc:
            raise AnalysisError("Invalid TShark frame/stream index.") from exc
        protocol = "http2" if h2method or h2status else "http1"
        if not any((method, status, h2method, h2status)):
            continue
        entry = {
            "frame": frame_num, "stream": stream_num,
            "protocol": protocol, "src": ipv4src or ipv6src or None,
            "dst": ipv4dst or ipv6dst or None,
            "method": method or h2method or None,
            "host": host or h2host or None,
            "status": int(status or h2status) if status or h2status else None,
        }
        if include_uris:
            entry["uri"] = uri or h2path or None
        entries.append(entry)
    report["http"] = entries
    report["tls"] = {
        "offline": True, "keylog_entries": key_count,
        "decrypted_http_messages": len(entries),
        "uri_visibility": "included" if include_uris else "redacted",
        "raw_http_content_exported": bool(destination and entries),
        "secret_values_in_report": False,
        "tshark_backend": True,
    }
    if not entries:
        report["warnings"].append(
            "No decrypted HTTP/1 or HTTP/2 messages found. TLS secrets may not match, "
            "capture may be incomplete, or traffic may use unsupported HTTP/3/QUIC."
        )
    if destination is not None and entries:
        _export_decrypted_json(base, destination, timeout)
        report["tls"]["decrypted_json_saved_to"] = str(destination)
        report["warnings"].append(
            "Decrypted JSON may contain authentication tokens, cookies and content. "
            "Keep this private file restricted and delete it when no longer required."
        )
    report["stats"] = {"http_messages": len(entries), "tls_keylog_entries": key_count}
    return report


def proxy_command(
    host: str,
    port: int,
    *,
    authorized_clients: bool,
    allow_lan: bool = False,
    confdir: Path | str | None = None,
) -> list[str]:
    """Prepare an opt-in regular proxy, never a transparent or forced proxy."""
    if not authorized_clients:
        raise AnalysisError("Confirm explicitly configured, authorized client devices first.")
    try:
        address = ip_address(host)
    except ValueError as exc:
        raise AnalysisError("Proxy listen host must be an IP address, not a hostname.") from exc
    if address.is_unspecified or address.is_multicast or address.is_reserved:
        # IPv6 loopback is treated as reserved by some ipaddress versions.
        if not address.is_loopback:
            raise AnalysisError("Wildcard, multicast and reserved listen addresses are not permitted.")
    if not 1024 <= port <= 65535:
        raise AnalysisError("Proxy port must be between 1024 and 65535.")
    # Prevent becoming an unauthenticated open proxy on a shared LAN.
    # A future authenticated LAN mode must bind an explicit client scope.
    if not address.is_loopback or allow_lan:
        raise AnalysisError(
            "This release permits loopback-only explicit proxy use. "
            "Authenticated LAN clients are not implemented."
        )
    executable = shutil.which("mitmdump")
    if executable is None:
        raise AnalysisError("mitmdump 12+ is required; install mitmproxy separately.")
    folder = Path(confdir).expanduser() if confdir is not None else (
        Path.home() / ".local/share/subterfuge/mitmproxy"
    )
    if folder.exists() and (folder.is_symlink() or not folder.is_dir()):
        raise AnalysisError("The proxy configuration directory is invalid.")
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    if os.name == "posix":
        os.chmod(folder, 0o700)
    return [
        executable, "--mode", "regular",
        "--listen-host", str(address), "--listen-port", str(port),
        "--set", "confdir=" + str(folder.resolve()),
        "--set", "check_for_updates=false",
        "--flow-detail", "0", "--quiet",
    ]


def serve_proxy(host: str, port: int, *, authorized_clients: bool, allow_lan: bool = False) -> None:
    command = proxy_command(host, port, authorized_clients=authorized_clients, allow_lan=allow_lan)
    print(f"Explicit HTTPS test proxy listening at {host}:{port}.")
    print("Only local clients are supported. Explicitly configure your own browser to use this proxy.")
    print("Trust its test CA only for this laboratory; remove the test trust after use.")
    print("The proxy does not change gateways, disconnect devices or install certificates.")
    print("No flow recordings are saved automatically; press Ctrl+C to stop.", flush=True)
    try:
        result = subprocess.run(command, check=False)
    except OSError as exc:
        raise AnalysisError("Unable to launch the opt-in proxy: " + str(exc)) from exc
    if result.returncode:
        raise AnalysisError(f"Opt-in proxy exited with status {result.returncode}.")
