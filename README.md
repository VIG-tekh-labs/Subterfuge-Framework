# Subterfuge Framework

**Modernization in progress — version 2.0.0a2 (alpha).** The modern assessment core is installable; the complete historical framework is not yet restored or validated.

## Project status and modernization branch

The default GitHub branch, master, still contains an earlier alpha snapshot. The active Python 3 modernization is published on modernization-2026-10-08-continuation. See [MODERNIZATION_STATUS.md](MODERNIZATION_STATUS.md) for verified features, outstanding tasks and the historical file-age audit. No merge to master has yet been authorized.

## Historical source archive (October 2026)

The maintained Python 3 runtime is in `src/subterfuge/`. The entire old
Django 1.x, Twisted/SSLStrip, Python 2 and legacy UI framework, including
its original assets and third-party attributions, was moved **without
changing source bytes** into `legacy/historical-framework-2015-2016/`. This inactive code
is excluded from the modern wheel and source distribution. The separate
branch `archive-legacy-original-2026-10-09` retains the complete
pre-reorganization checkout.

The verbatim GNU GPLv3 text is in root `LICENSE`. Root
`COPYING` is now a compatibility pointer, not a new license. The move does not change copyright or license obligations.

See [the file relocation map](LEGACY_ARCHIVE_FILE_MAP_2026-10-09.csv) and
[the archival review](LEGACY_REORGANIZATION_2026-10-09.md) for provenance.
**Recent Git commit dates on archived files indicate reorganization,
not a code upgrade or a security certification.**

## Historic file maintenance review

An October 2026 audit reviewed all 104 tracked files whose last Git commit was more than 24 hours old. Thirty-seven first-party archived Django templates and old configuration/launcher samples received non-executing review comments. Eight unreferenced AppleDouble macOS metadata sidecars were removed; 59 licensed, third-party, real-image, raw-data or active legacy payload files were preserved to prevent damage. These cosmetic annotations do not port historic functionality to Python 3. Read [STALE_24H_REVIEW_2026-10-08.md](STALE_24H_REVIEW_2026-10-08.md) and [FILE_REVIEW_OLDER_24H_2026-10-08.csv](FILE_REVIEW_OLDER_24H_2026-10-08.csv) for per-file classifications and SHA-256 checksums.

## Install the modern runtime

Use Python 3.11 or newer in a virtual environment. Do not run the historical installer or updater.

```sh
git clone --branch modernization-2026-10-08-continuation --single-branch https://github.com/VIG-tekh-labs/Subterfuge-Framework.git
cd Subterfuge-Framework
python3 -m venv .venv
. .venv/bin/activate
python -m pip install .
subterfuge doctor
subterfuge demo
subterfuge serve --open
```

On Windows, create the environment with `py -m venv .venv` and activate it with `.venv\Scripts\Activate.ps1` in PowerShell. Windows execution is awaiting CI validation.

The modern core requires no Django, Twisted, GPU or root privileges for offline work. The previous privileged installer is preserved at `legacy/setup.py`; the root setup.py now delegates packaging to setuptools.

## Migration status and supported components

**Release level: alpha.** The modern Python 3 package is intentionally independent of
the historical Django 1.x/Twisted runtime and does not bundle historical
interception scripts. The dashboard uses Python standard-library HTTP and
plain browser JavaScript; no Django, Twisted or jQuery upgrade is required
to use the active interface.

Classic PCAP and experimental PCAPNG imports now summarize ARP claims and
passive DHCPv4/NetBIOS queries into bounded, deduplicated
`network_evidence` records. The local dashboard displays these records
alongside host inventory and review findings. DHCP option 252 contents and
unrelated packet payloads are not retained. These are **observations, not
proofs of exploitation**. IP fragments and unsupported link protocols
are not reassembled. Live capture remains ARP-only and optional.

See [AUDIT.md](AUDIT.md), [FILE_AUDIT.md](FILE_AUDIT.md),
[SECURITY.md](SECURITY.md) and [LICENSING.md](LICENSING.md) before restoring
historical modules or redistributing historical assets.

## Evidence and assessment

```sh
subterfuge analyze-pcap capture.pcap --output report.json
subterfuge import-nmap inventory.xml --output inventory.json
subterfuge scan-services --target 192.0.2.10 --ports 22,80,443 --output services.json
subterfuge inspect-tls --host example.com --output tls.json
subterfuge interfaces
```

The dashboard runs on `127.0.0.1`, imports PCAP/Nmap XML files locally and can reopen previously exported JSON reports entirely in the browser without re-uploading them. PCAP limits are 16 MiB for dashboard uploads and 64 MiB for CLI imports. PCAPNG packet imports remain experimental on the modernization branch. Enhanced packet (type 6), obsolete packet (type 2), and simple packet (type 3) blocks are decoded, and interface timestamp-offset options are recognized. Simple packet blocks have no timestamps: unknown host times are represented by null, never an invented timestamp. Synthetic format/passive protocol tests have passed, but diverse real-world capture coverage is incomplete. Classic PCAP remains the better validated format. Nmap service/version and OS data are retained as reported evidence. Transport review items require investigation; they do not establish exploitation or missing STARTTLS.

TLS inspection is available both in the CLI and through the dashboard's
explicit **Inspect TLS** form. The user selects a host and port; the backend
requires a local authenticated JSON request and opens one normal
certificate-verified connection, recording the negotiated protocol/cipher
and reporting certificate expiry or verification failure. It does not
enumerate every server configuration, test HSTS, intercept or downgrade TLS.

Optional live adapters, only on a network you are authorized to assess:

```sh
python -m pip install '.[capture]'
subterfuge capture --interface eth0 --duration 30 --output arp.json
subterfuge capture-protocols --interface eth0 --duration 30 --output protocols.json
subterfuge discover --target 192.0.2.0/24 --output hosts.json
```

Nmap must be installed separately. Discovery performs host discovery. The optional `scan-services` command explicitly opens TCP connections and performs light service detection for one selected IP and at most 32 TCP ports; run it only against networks you are authorized to assess. The interface name above is an example: use `subterfuge interfaces`. Capture permissions and drivers depend on your OS. The new `capture-protocols` adapter observes ARP/DHCPv4/NetBIOS metadata passively when Scapy permissions are available. It has synthetic adapter tests but has **not** been validated on a real interface. It does not send packets or retain raw UDP payloads.

## Browser report-import quality checks

The dashboard opens a saved JSON audit report entirely in the browser (no server upload). Import validates nested host, port, finding and passive-evidence field types, bounds and optional timestamp values before modifying the current view.

The dependency-free Node.js regression harness runs against valid records, malformed input and genuine CLI demo/Nmap exports:

```sh
node qa/browser_report_validation.mjs
```

Optional interactive Chromium QA (requires a separately installed Puppeteer, **not** a production dependency):

```sh
node qa/browser_report_smoke.cjs
```

This local smoke test starts only a temporary loopback dashboard, checks saved report reopening/rejection and then closes the browser and server.

The QA scripts are bundled with the source distribution but not with the installed runtime wheel. Distribution hygiene can be checked after building both artifacts by running the source-only command: python qa/audit_distributions.py dist.

## Validation and continuity

```sh
python -m pip install .
python -m unittest discover -s tests -v
```

Read [ROADMAP.md](ROADMAP.md) first, then [CAPABILITIES.md](CAPABILITIES.md) for historical module coverage and [MAINTENANCE_COUNTS.md](MAINTENANCE_COUNTS.md) for cosmetic versus functional changes. Follow [MAINTENANCE.md](MAINTENANCE.md) when continuing development.

Linux/Python 3.12 passed local checks. Other OS/Python combinations are CI targets, not yet verified support claims. Contributions are welcome through issues and pull requests.

Original source, authorship and [complete GPL license](LICENSE) are retained. Historical source outside `src/` remains reference material and is not imported by the modern package. No replacement repository has been created.

## Updating a modern checkout

The historical Python 2/SVN updater has been retired. Its original implementation is retained in `legacy/update.py` for reference only and must not be executed. The root `update.py` is a safe Python 3 migration notice, not an automatic updater. To update a reviewed checkout, use Git to inspect and select changes, then reinstall the modern package inside its virtual environment using `python -m pip install --upgrade .`.

For the module-by-module restoration checklist and technology choices, see
[MIGRATION_MATRIX.md](MIGRATION_MATRIX.md). The full historical functionality is
not yet present in the active alpha package.

## Reproducible additional QA

On a machine with Nmap installed, to verify the optional active Nmap adapter
**against your own loopback only**, run:

```sh
PYTHONPATH=src python qa/loopback_nmap_smoke.py
```

The script starts an ephemeral HTTP-like listener bound to `127.0.0.1`,
scans only that listener and closes it. It does not scan the LAN or Internet.

If Wireshark `editcap` is installed, the regression suite also independently
converts a synthetic classic PCAP to PCAPNG and compares the observed ARP
evidence. If `editcap` is missing, that optional test is explicitly skipped.
## Continuation handoff

Read [HANDOFF.md](HANDOFF.md) and [ROADMAP.md](ROADMAP.md) before continuing modernization. The current branch is an alpha; historical feature parity remains incomplete.
