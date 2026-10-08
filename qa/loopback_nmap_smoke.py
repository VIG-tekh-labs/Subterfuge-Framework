#!/usr/bin/env python3
"""Manual authorized loopback-only Nmap adapter check; no external targets."""
from __future__ import annotations

import socket
import threading

from subterfuge.environment import scan_services


def main() -> None:
    stopped = threading.Event()
    listener = socket.socket()
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("127.0.0.1", 0))
    listener.listen(8)
    listener.settimeout(1)
    port = listener.getsockname()[1]

    def respond() -> None:
        while not stopped.is_set():
            try:
                connection, _ = listener.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            with connection:
                connection.settimeout(2)
                try:
                    connection.recv(1024)
                    connection.sendall(b"HTTP/1.0 200 OK\r\nContent-Length: 2\r\n\r\nOK")
                except OSError:
                    pass

    thread = threading.Thread(target=respond, daemon=True)
    thread.start()
    try:
        result = scan_services("127.0.0.1", str(port), timeout=70)
        assert result["kind"] == "service_scan" and result["stats"]["open_ports"] == 1
        print("Loopback TCP service inventory: PASS")
    finally:
        stopped.set()
        listener.close()
        thread.join(timeout=3)


if __name__ == "__main__":
    main()