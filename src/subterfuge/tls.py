"""Inspect one TLS endpoint using normal certificate-verified negotiation."""

from __future__ import annotations

from datetime import datetime, timezone
import math
import socket
import ssl

from .analysis import AnalysisError, base_report


def inspect_tls(host: str, port: int = 443, timeout: float = 10) -> dict:
    if not host or len(host) > 253 or any(c.isspace() or c in "/\\\x00" for c in host):
        raise AnalysisError("Use a hostname or IP address without a URL scheme or path.")
    if not 1 <= port <= 65535:
        raise AnalysisError("TLS port must be between 1 and 65535.")
    if not math.isfinite(timeout) or not 0 < timeout <= 60:
        raise AnalysisError("TLS timeout must be greater than zero and at most 60 seconds.")
    report = base_report("tls", host)
    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    try:
        with socket.create_connection((host, port), timeout=timeout) as connection:
            with context.wrap_socket(connection, server_hostname=host) as secured:
                certificate = secured.getpeercert()
                cipher = secured.cipher()
                details = {
                    "host": host, "port": port, "certificate_verified": True,
                    "negotiated_version": secured.version(),
                    "cipher": cipher[0] if cipher else None,
                    "cipher_bits": cipher[2] if cipher else None,
                    "subject": certificate.get("subject", []),
                    "issuer": certificate.get("issuer", []),
                    "not_after": certificate.get("notAfter"),
                }
    except ssl.SSLCertVerificationError as exc:
        report["tls"] = {"host": host, "port": port, "certificate_verified": False}
        report["findings"].append({
            "code": "tls_certificate_verification_failed", "severity": "warning",
            "address": host, "message": "Certificate verification failed.",
            "interpretation": str(exc.verify_message)[:300],
        })
    except (OSError, ValueError) as exc:
        raise AnalysisError("TLS connection failed: " + str(exc)[:300]) from exc
    else:
        if details["not_after"]:
            expires = ssl.cert_time_to_seconds(details["not_after"])
            days = (expires - datetime.now(timezone.utc).timestamp()) / 86400
            details["days_until_expiry"] = round(days, 2)
            if days <= 30:
                report["findings"].append({
                    "code": "tls_certificate_expiring", "severity": "warning",
                    "address": host, "message": "Certificate expires within 30 days.",
                    "interpretation": "Review certificate renewal before expiry.",
                })
        report["tls"] = details
    report["warnings"].append("A single negotiated connection does not enumerate all supported protocols or ciphers, test HSTS or prove resistance to interception. DNS resolution may exceed the socket timeout.")
    report["stats"] = {"findings": len(report["findings"])}
    return report
