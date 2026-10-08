"""Local-only dashboard with bounded uploads and origin validation."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
import hmac
import json
import secrets
import threading
import webbrowser

from .analysis import AnalysisError, analyze_nmap, analyze_pcap, base_report
from .environment import doctor

MAX_UPLOAD = 16 * 1024 * 1024


def make_server(port: int = 8080) -> ThreadingHTTPServer:
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
            if origin is not None and origin != self.server.expected_origin:
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
            if self.path not in ("/api/analyze-pcap", "/api/import-nmap"):
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
            if not 0 < length <= MAX_UPLOAD:
                self.json(413, {"error": "Upload must be between 1 byte and 16 MiB."})
                self.close_connection = True
                return
            try:
                data = self.rfile.read(length)
                if len(data) != length:
                    raise AnalysisError("Incomplete upload.")
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
    return server


def serve(port: int = 8080, open_browser: bool = False) -> None:
    server = make_server(port)
    url = server.expected_origin + "/"
    print(f"Subterfuge dashboard: {url}", flush=True)
    print("Press Ctrl+C to stop. Reports stay in memory until downloaded.", flush=True)
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    finally:
        server.server_close()
