# Security and historical artifact handling

The active Python 3 package is designed for offline network evidence inspection and a loopback-only dashboard. It does not run the historical Python 2 privileged installer, SSLStrip proxy, DHCP spoofing or NetBIOS response scripts.

## Important history notice

Earlier commits of this **public** repository included an RSA private-key PEM file, a hard-coded legacy Django secret, credential-related text and SQLite databases. Removing such files from the current branch does **not** remove them from Git history, forks, caches or existing clones.

- Treat any private key or password actually used in a live environment as exposed and rotate/revoke it using the owning system. A historical test-only key should still not be reused.
- Verify whether historical databases contain personal data before any distribution. Do not publish their contents or reproduce them in issue reports.
- Before any history rewrite, coordinate with the repository owner: rewriting public history affects clones, forks and commit references and requires a deliberate migration plan.
- The current branch deliberately removes compiled `.pyc`, transient logs, historical database copies, a credential text file and a bundled private key from tracked files.
- The old Django settings module is legacy-only. Its stored secret was removed from the current branch in favor of `SUBTERFUGE_LEGACY_SECRET_KEY`, and `DEBUG` was disabled. These adjustments do **not** make the old Django application supported.

## Runtime boundaries

Run installation inside a Python virtual environment. Do not execute `legacy/setup.py` or `legacy/update.py`, and do not run historical interception modules as an installation or regression check. Use synthetic packets or an isolated authorized lab for network testing. Local audit findings are evidence to investigate, not automatic vulnerability verdicts.

Please report security issues privately to the maintainers rather than adding credentials, captures containing secrets or private keys to a public issue.

## Explicit active inventory

The modern `scan-services` CLI command is opt-in. It accepts one IP address,
at most 32 explicit ports and a bounded timeout, invokes Nmap in user-space
TCP-connect mode and does not use shell interpolation. Its service probes
generate real network traffic. Do not run this command without the network
owner's authorization. Unit tests mock all such process execution.

## Passive live packet observation

The optional `capture-protocols` command is read-only with respect to
network traffic: it does not inject, spoof, reconfigure firewall rules or
retain raw UDP payloads in reports. It may still observe sensitive
network metadata (e.g. hostnames) and requires appropriate authorization,
OS packet-capture privileges and an explicit selected interface. Do not
run it automatically during installation or unit tests.
## Local browser report import hardening — October 2026

Saved report JSON is parsed entirely within the browser, with a 16 MiB file limit.
Nested hosts, ports, addresses, timestamp fields (including null for untimed
PCAPNG observations), finding messages, warnings and passive DHCP/NBNS evidence
are validated for type, length and cardinality before replacing the displayed
report. HTML is not constructed from imported values; the UI uses text nodes.
The parser still runs in the operator's local browser and is not a substitute
for host access controls or a secure user-profile boundary.

Reproducible standalone checks:
- node qa/browser_report_validation.mjs uses built-in Node.js APIs, no npm packages.
- node qa/browser_report_smoke.cjs optionally drives sandboxed Chromium against
  an ephemeral loopback-only dashboard; Puppeteer must be installed separately
  for QA and is not a runtime dependency.

## Archive-only historical source, October 2026

The entire Python 2/Django/Twisted-era framework is now stored under `legacy/historical-framework-2015-2016/`. The modern wheel and source archives exclude this directory. Original bytes and attribution are unchanged; see LEGACY_ARCHIVE_FILE_MAP_2026-10-09.csv. Historical hardcoded network parameters and secrets may persist in the Git history or the separate archival branch; moving paths does not sanitize secrets. Do not run outdated interception or injection scripts on production systems.
