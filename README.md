# Subterfuge Framework

**Current tested version 2.0.0a3:** TLS key-log decryption and an opt-in local HTTP(S) proxy were tested against synthetic localhost connections. Browser Lab is a visible, local-only Chromium companion, and Bettercap data import is passive and offline. See [the module guide](TLS_BROWSER_LAB_2026-10-09.md) and the [six-platform CI result](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37862358235). The optional vendor-neutral automation API is available but is not automatically registered in other applications.


## TLS & Browser Lab 2.0.0a3 (optional)

### New optional TLS / Browser Lab capabilities — 2026-10-09 (2.0.0a3)

- Added a TShark-backed offline tls-decrypt command for PCAP/PCAPNG plus a user-supplied SSLKEYLOGFILE, with strict key-log input permissions (0600 on Unix), limits, metadata-only default, opt-in URI inclusion and private atomic decrypted JSON export.
- Proved a real loopback-only TLS/HTTPS test: a locally generated server certificate, a controlled client producing five TLS secrets, an actual PCAPNG capture on lo and TShark reporting two decrypted HTTP messages, including the expected synthetic test URI.
- Added a mitmproxy-based proxy-lab command for visible local test clients. Only explicit regular proxy mode on 127.0.0.1/loopback is allowed; LAN binding, stealth interception, unauthorized client redirection and automatic CA trust changes are excluded.
- Added a Chromium Manifest V3 Browser Lab companion shipped with the Python wheel and sdist. It has a simple enable/disable toggle, persisted local setting and read-only inspect action. It operates ONLY on 127.0.0.1 with a recognized local Subterfuge dashboard; it does not read cookies or credentials, inject into arbitrary sites, or run background remote commands.
- Added a read-only Bettercap JSON event importer accepting only network discovery tags and discarding packet contents, handshake keys and attack-related events.
- Added agent-capabilities and an independent optional agent-compatible Python policy bridge: standalone operation requires no external agent; a calling agent must supply exact allowed_actions, allowed_files and allowed_targets with additional affirmative gates for sensitive TLS/network operations. Those caller-defined rules can further restrict but never bypass OS controls.
- These modules are optional components. Python 3.11+ modern offline analysis remains zero mandatory external runtime dependencies; TShark and mitmdump are optional installed system tools.
- For installation, examples, scope, privacy and security rules, consult TLS_BROWSER_LAB_2026-10-09.md. Current release remains alpha (2.0.0a3), not a recreation of historical SSLStrip, BeEF, Bettercap spoofing or user-session hooks.

See [the setup and privacy guide](TLS_BROWSER_LAB_2026-10-09.md) for executable examples.


**Verified on master (October 9, 2026):** [cleanup commit 9a986a1](https://github.com/VIG-tekh-labs/Subterfuge-Framework/commit/9a986a148eb34cf74596df8b6d2adbfa34714ad8) removed 193 historic files from the active tree. A fresh clone has 63 tracked files and no legacy directory. [All six cross-platform CI jobs passed](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37858737482).


**Modernization in progress — version 2.0.0a3 (alpha).** The modern assessment core is installable; the complete historical framework is not yet restored or validated.

## Project status — current default master

The default GitHub branch master now contains the modern Python 3 alpha. At the owner's request, the old 2015–2016 framework and unused assets have been removed from the maintained branch. The older source and its copyright notices remain available on a separate archival branch. See MODERNIZATION_STATUS.md for current supported capabilities and remaining work.

## Historical source preservation without obsolete files on main

The default branch contains only the maintained Python 3 alpha and the
supporting documentation, tests and license files. The 2015–2016 Python 2,
Django, Twisted/SSLStrip framework and unused old images were **removed**
from the active repository tree.

Those source files, original author notices and old versions remain available
from the [original historical archive branch](https://github.com/VIG-tekh-labs/Subterfuge-Framework/tree/archive-legacy-original-2026-10-09).
Earlier modernization commits documented the move into a legacy directory;
the later cleanup removed that directory from the active branch as requested.
The Git history remains intact; removal does not mean the old features were
ported or that earlier copyright obligations have disappeared.

The verbatim complete GNU GPLv3 text remains at [LICENSE](LICENSE).
COPYING is a compatibility pointer; the licensing terms have not changed.
The [relocation ledger](LEGACY_ARCHIVE_FILE_MAP_2026-10-09.csv) and
[archival audit](LEGACY_REORGANIZATION_2026-10-09.md) are historical
provenance references, not active files.


## Historic file maintenance review

An October 2026 audit reviewed all 104 tracked files whose last Git commit was more than 24 hours old. Thirty-seven first-party archived Django templates and old configuration/launcher samples received non-executing review comments. Eight unreferenced AppleDouble macOS metadata sidecars were removed; 59 licensed, third-party, real-image, raw-data or active legacy payload files were preserved to prevent damage. These cosmetic annotations do not port historic functionality to Python 3. Read [STALE_24H_REVIEW_2026-10-08.md](STALE_24H_REVIEW_2026-10-08.md) and [FILE_REVIEW_OLDER_24H_2026-10-08.csv](FILE_REVIEW_OLDER_24H_2026-10-08.csv) for per-file classifications and SHA-256 checksums.

## Install the modern runtime

Use Python 3.11 or newer in a virtual environment. Do not run the historical installer or updater.

```sh
git clone https://github.com/VIG-tekh-labs/Subterfuge-Framework.git
cd Subterfuge-Framework
python3 -m venv .venv
. .venv/bin/activate
python -m pip install .
subterfuge doctor
subterfuge demo
subterfuge serve --open
```

On Windows, create the environment with `py -m venv .venv` and activate it with `.venv\Scripts\Activate.ps1` in PowerShell. Automated Windows regression and packaging checks have passed; actual network interface capture on Windows is still unverified.

The modern core requires no Django, Twisted, GPU or root privileges for offline work. The privileged 2015-era installer exists only in the historical archive branch; modern setup.py delegates packaging to setuptools.

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
are not reassembled. Optional passive capture supports ARP and DHCPv4/NBNS metadata on explicitly selected interfaces, but real-device capture interoperability is still incompletely verified.

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

Original authorship and the [complete GPL license](LICENSE) are preserved. Historical source remains available in the separate archive branch and Git history, not in the installable modern package.

## Updating a modern checkout

The historical Python 2/SVN updater has been retired. Its original implementation exists only in the original archived branch and must not be executed. Root update.py is a safe Python 3 migration notice, not an automatic updater. Use Git to select changes, then reinstall with python -m pip install --upgrade . inside your virtual environment.

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
