"""Local-only dashboard with bounded uploads and origin validation."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
import hmac
import json
import secrets
import threading
import webbrowser
from urllib.parse import urlsplit

from .analysis import AnalysisError, analyze_nmap, analyze_pcap, base_report
from .environment import doctor

MAX_UPLOAD = 16 * 1024 * 1024
MAX_TLS_REQUEST = 4096


def _tls_request(raw: bytes) -> dict:
    """Decode a strictly bounded, explicit local TLS inspection request."""
    try:
        params = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AnalysisError("TLS inspection requires valid UTF-8 JSON.") from exc
    if not isinstance(params, dict) or "host" not in params or set(params) - {"host", "port", "timeout"}:
        raise AnalysisError("Expected host, optional port and optional timeout.")
    host, port, timeout = params["host"], params.get("port", 443), params.get("timeout", 10)
    if not isinstance(host, str) or type(port) is not int or type(timeout) not in (int, float):
        raise AnalysisError("TLS host, port or timeout has an invalid type.")
    from .tls import inspect_tls
    return inspect_tls(host, port, timeout)



def validate_public_origin(value: str | None) -> str | None:
    """Accept only one explicitly declared HTTPS reverse-proxy origin.

    The underlying HTTP server continues to bind loopback; TLS, access
    control and user authentication belong to the operator's reverse proxy.
    """
    if value is None:
        return None
    if not isinstance(value, str) or not value.startswith("https://"):
        raise AnalysisError("Public server origin requires https://host:port.")
    try:
        parsed = urlsplit(value)
        hostname, port = parsed.hostname, parsed.port
    except ValueError as exc:
        raise AnalysisError("Invalid public HTTPS origin.") from exc
    if (parsed.scheme != "https" or not hostname or port is None
            or not 1 <= port <= 65535 or parsed.username is not None
            or parsed.password is not None or parsed.path not in ("", "/")
            or parsed.query or parsed.fragment or any(c.isspace() for c in value)):
        raise AnalysisError("Specify an HTTPS origin with an explicit port and no path or credentials.")
    host = f"[{hostname}]" if ":" in hostname else hostname
    return f"https://{host}:{port}"


def make_server(port: int = 8080, public_origin: str | None = None) -> ThreadingHTTPServer:
    trusted_origin = validate_public_origin(public_origin)
    if not 0 <= port <= 65535:
        raise AnalysisError("Dashboard port must be between 0 and 65535.")
    token = secrets.token_urlsafe(32)
    lock = threading.Lock()
    state = {"report": base_report("empty", "local dashboard")}
    page = files("subterfuge").joinpath("static/index.html").read_text(encoding="utf-8")

    class Handler(BaseHTTPRequestHandler):
        server_version = "Subterfuge"
        sys_version = ""

        def setup(self):
            super().setup()
            self.connection.settimeout(15)

        def log_message(self, format, *args):
            return

        def reply(self, status: int, body: bytes, content_type: str = "application/json"):
            self.send_response(status)
            self.send_header("Content-Type", content_type + "; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'nonce-" + token + "'; style-src 'nonce-" + token + "'; connect-src 'self'; img-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")
            self.end_headers()
            self.wfile.write(body)

        def json(self, status: int, payload: dict):
            self.reply(status, json.dumps(payload, ensure_ascii=False, allow_nan=False).encode())

        def allowed(self) -> bool:
            if self.headers.get("Host") != self.server.expected_host:
                self.json(403, {"error": "Unexpected dashboard host."})
                return False
            origin = self.headers.get("Origin")
            if origin is not None and origin not in self.server.allowed_origins:
                self.json(403, {"error": "Cross-origin dashboard requests are not accepted."})
                return False
            return True

        def do_GET(self):
            if not self.allowed():
                return
            if self.path == "/":
                self.reply(200, page.replace("__TOKEN__", token).encode(), "text/html")
            elif self.path == "/api/doctor":
                self.json(200, doctor())
            elif self.path == "/api/demo":
                from .demo import demo_report
                self.json(200, demo_report())
            elif self.path == "/api/report":
                with lock:
                    result = state["report"]
                self.json(200, result)
            else:
                self.json(404, {"error": "Not found."})

        def do_POST(self):
            if not self.allowed():
                return
            supplied = self.headers.get("X-Subterfuge-Token", "")
            if not supplied.isascii() or not hmac.compare_digest(supplied, token):
                self.json(403, {"error": "Missing or invalid dashboard token."})
                return
            if self.path not in ("/api/analyze-pcap", "/api/import-nmap", "/api/inspect-tls"):
                self.json(404, {"error": "Not found."})
                return
            if self.headers.get("Transfer-Encoding") is not None:
                self.json(400, {"error": "Chunked uploads are not supported."})
                self.close_connection = True
                return
            try:
                length = int(self.headers.get("Content-Length", ""))
            except ValueError:
                self.json(411, {"error": "A valid Content-Length is required."})
                return
            maximum = MAX_TLS_REQUEST if self.path == "/api/inspect-tls" else MAX_UPLOAD
            if not 0 < length <= maximum:
                self.json(413, {"error": "Request size is outside the permitted limit."})
                self.close_connection = True
                return
            if self.path == "/api/inspect-tls" and self.headers.get("Content-Type", "").split(";")[0].strip().lower() != "application/json":
                self.json(415, {"error": "TLS inspection requires application/json."})
                return
            try:
                data = self.rfile.read(length)
                if len(data) != length:
                    raise AnalysisError("Incomplete upload.")
                if self.path == "/api/inspect-tls":
                    result = _tls_request(data)
                else:
                    analyze = analyze_pcap if self.path == "/api/analyze-pcap" else analyze_nmap
                    result = analyze(data, "dashboard upload")
            except (AnalysisError, OSError) as exc:
                self.json(400, {"error": str(exc)})
                return
            with lock:
                state["report"] = result
            self.json(200, result)

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.daemon_threads = True
    server.expected_host = f"127.0.0.1:{server.server_port}"
    server.expected_origin = f"http://{server.expected_host}"
    server.allowed_origins = frozenset(
        {server.expected_origin, trusted_origin} if trusted_origin
        else {server.expected_origin}
    )
    server.public_origin = trusted_origin
    return server


def serve(port: int = 8080, open_browser: bool = False,
          public_origin: str | None = None) -> None:
    server = make_server(port, public_origin=public_origin)
    url = server.expected_origin + "/"
    print(f"Subterfuge dashboard: {url}", flush=True)
    print("Press Ctrl+C to stop. Reports stay in memory until downloaded.", flush=True)
    if server.public_origin:
        print(
            "External HTTPS origin configured: " + server.public_origin
            + " (reverse proxy must enforce HTTPS authentication and rewrite upstream Host).",
            flush=True,
        )
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    finally:
        server.server_close()