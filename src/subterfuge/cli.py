"""Command-line entry point for installation checks, observation and reports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from . import __version__
from .analysis import AnalysisError, analyze_nmap, analyze_pcap, read_input, write_report
from .environment import capture, capture_protocols, discover, doctor, interfaces, scan_services


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="subterfuge", description="Network inventory, ARP observation and local audit reports.")
    root.add_argument("--version", action="version", version=__version__)
    commands = root.add_subparsers(dest="command")
    commands.add_parser("doctor", help="Check the local runtime and optional tools")
    commands.add_parser("interfaces", help="List local network interfaces")
    command = commands.add_parser("inspect-tls", help="Inspect one explicitly selected TLS endpoint")
    command.add_argument("--host", required=True)
    command.add_argument("--port", type=int, default=443)
    command.add_argument("--timeout", type=float, default=10)
    command.add_argument("--output", type=Path)
    command = commands.add_parser("demo", help="Analyze a synthetic capture without sending traffic")
    command.add_argument("--output", type=Path)
    for name, label in [("analyze-pcap", "Analyze a PCAP or experimental PCAPNG capture"), ("import-nmap", "Import an Nmap XML inventory")]:
        command = commands.add_parser(name, help=label)
        command.add_argument("file", type=Path)
        command.add_argument("--output", type=Path, help="Write a private JSON report")
    command = commands.add_parser("discover", help="Inventory an explicitly authorized IP or CIDR using Nmap")
    command.add_argument("--target", required=True, help="IP or CIDR; at most 256 addresses")
    command.add_argument("--timeout", type=float, default=60)
    command.add_argument("--output", type=Path)
    command = commands.add_parser("scan-services", help="Explicit TCP connect inventory of one authorized IP (Nmap)")
    command.add_argument("--target", required=True, help="One IPv4 or IPv6 address; no CIDR or hostnames")
    command.add_argument("--ports", default="22,80,443", help="Comma-separated list of at most 32 TCP ports")
    command.add_argument("--timeout", type=float, default=120)
    command.add_argument("--output", type=Path)
    command = commands.add_parser("capture", help="Passively observe ARP on an explicitly selected interface")
    command.add_argument("--interface", required=True)
    command.add_argument("--duration", type=float, default=30)
    command.add_argument("--limit", type=int, default=10_000)
    command.add_argument("--output", type=Path)
    command = commands.add_parser("capture-protocols", help="Passive ARP/DHCPv4/NBNS metadata capture on one interface")
    command.add_argument("--interface", required=True)
    command.add_argument("--duration", type=float, default=30)
    command.add_argument("--limit", type=int, default=10_000)
    command.add_argument("--output", type=Path)
    command = commands.add_parser(
        "tls-decrypt", help="Offline HTTPS inspection with a user-provided SSLKEYLOGFILE (TShark)"
    )
    command.add_argument("--pcap", required=True, type=Path, help="Existing PCAP/PCAPNG capture")
    command.add_argument("--keylog", required=True, type=Path, help="Owned 0600 SSLKEYLOGFILE containing TLS session secrets")
    command.add_argument("--include-uris", action="store_true", help="Include sensitive HTTP request paths in the summary")
    command.add_argument("--export-decrypted-json", type=Path, help="Explicit private export of decrypted TShark protocol fields")
    command.add_argument("--limit", type=int, default=100_000, help="Maximum packets to process")
    command.add_argument("--timeout", type=int, default=120, help="Processing timeout in seconds")
    command.add_argument("--output", type=Path, help="Save summary report (not TLS session secrets)")
    command = commands.add_parser("proxy-lab", help="Start an opt-in regular HTTPS proxy for explicitly configured test clients")
    command.add_argument("--host", default="127.0.0.1", help="Local proxy address (loopback by default)")
    command.add_argument("--port", type=int, default=8081)
    command.add_argument("--authorized-clients", action="store_true", help="Confirm own/authorized clients are configured explicitly")
    commands.add_parser("browser-lab", help="Show where to install the opt-in Chromium laboratory companion")
    command = commands.add_parser("import-bettercap", help="Summarize offline JSON discovery events exported from Bettercap")
    command.add_argument("file", type=Path, help="A Bettercap /api/events JSON export from your authorized laboratory")
    command.add_argument("--output", type=Path)
    commands.add_parser("agent-capabilities", help="Report supported actions for standalone use and optional local-agent integration")
    commands.add_parser("gui", help="Launch the native Qt desktop application (no browser)")
    commands.add_parser("desktop-shortcut", help="Install a per-user Linux applications-menu shortcut")
    command = commands.add_parser("serve", help="Open the local dashboard")
    command.add_argument("--port", type=int, default=8080, help="Local dashboard port (default: 8080)")
    command.add_argument("--open", action="store_true", help="Open the local dashboard in the default browser")
    command.add_argument(
        "--public-origin", help="Optional authenticated HTTPS reverse proxy origin, e.g. https://192.0.2.10:8443. The HTTP backend remains loopback-only.",
    )
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command in (None, "serve"):
            from .web import serve
            serve(
                getattr(args, "port", 8080), getattr(args, "open", False),
                getattr(args, "public_origin", None),
            )
            return 0
        if args.command == "doctor":
            report = doctor()
        elif args.command == "interfaces":
            report = interfaces()
        elif args.command == "inspect-tls":
            from .tls import inspect_tls
            report = inspect_tls(args.host, args.port, args.timeout)
        elif args.command == "demo":
            from .demo import demo_report
            report = demo_report()
        elif args.command == "analyze-pcap":
            report = analyze_pcap(read_input(args.file), args.file.name)
        elif args.command == "import-nmap":
            report = analyze_nmap(read_input(args.file), args.file.name)
        elif args.command == "discover":
            report = discover(args.target, args.timeout)
        elif args.command == "scan-services":
            report = scan_services(args.target, args.ports, args.timeout)
        elif args.command == "capture-protocols":
            report = capture_protocols(args.interface, args.duration, args.limit)
        elif args.command == "capture":
            report = capture(args.interface, args.duration, args.limit)
        elif args.command == "tls-decrypt":
            from .tls_lab import decrypt_https
            report = decrypt_https(
                args.pcap, args.keylog, include_uris=args.include_uris,
                export_json=args.export_decrypted_json,
                maximum_frames=args.limit, timeout=args.timeout,
            )
        elif args.command == "proxy-lab":
            from .tls_lab import serve_proxy
            serve_proxy(args.host, args.port, authorized_clients=args.authorized_clients)
            return 0
        elif args.command == "browser-lab":
            from importlib.resources import files
            extension = files("subterfuge").joinpath("browser_lab")
            report = {
                "kind": "browser_lab", "installed_extension_directory": str(extension),
                "install": [
                    "In Chromium open chrome://extensions",
                    "Enable Developer mode, then Load unpacked",
                    "Select installed_extension_directory",
                    "Pin the visible Subterfuge Lab Companion icon",
                    "Toggle Lab mode in its popup, then analyze only your own local Subterfuge page",
                ],
                "scope": "Visible, opt-in, local loopback page diagnostics; no arbitrary-site hooks.",
            }
        elif args.command == "import-bettercap":
            from .bettercap_events import import_bettercap_events
            report = import_bettercap_events(args.file)
        elif args.command == "agent-capabilities":
            from .agent_integration import describe_capabilities
            report = describe_capabilities()
        elif args.command == "gui":
            try:
                from .desktop import main as desktop_main
            except ImportError as exc:
                raise AnalysisError(
                    "Qt desktop GUI requires PySide6. Install: "
                    "python -m pip install 'subterfuge-framework[desktop]' "
                    "(or use your OS Qt/PySide6 package)."
                ) from exc
            return desktop_main()
        elif args.command == "desktop-shortcut":
            from .desktop_shortcut import install_shortcut
            report = {"shortcut": str(install_shortcut()), "kind": "desktop_shortcut"}
        else:
            raise AnalysisError("Unknown command.")
        if getattr(args, "output", None):
            write_report(report, args.output)
            print(f"Report saved: {args.output}", file=sys.stderr)
        print(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False))
        return 0
    except (AnalysisError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("Stopped.", file=sys.stderr)
        return 130