# Subterfuge Framework

**Modernization in progress — version 2.0.0a2 (alpha).** The modern assessment core is installable; the complete historical framework is not yet restored or validated.

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

The dashboard runs on `127.0.0.1` and imports PCAP/Nmap XML files locally. PCAP limits are 16 MiB for dashboard uploads and 64 MiB for CLI imports. PCAPNG enhanced-packet import is experimental on the modernization branch; synthetic format and passive protocol tests have passed, but real-world capture coverage is incomplete. Classic PCAP remains the better validated format. Nmap service/version and OS data are retained as reported evidence. Transport review items require investigation; they do not establish exploitation or missing STARTTLS.

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

## Validation and continuity

```sh
python -m pip install .
python -m unittest discover -s tests -v
```

Read [ROADMAP.md](ROADMAP.md) first, then [CAPABILITIES.md](CAPABILITIES.md) for historical module coverage and [MAINTENANCE_COUNTS.md](MAINTENANCE_COUNTS.md) for cosmetic versus functional changes. Follow [MAINTENANCE.md](MAINTENANCE.md) when continuing development.

Linux/Python 3.12 passed local checks. Other OS/Python combinations are CI targets, not yet verified support claims. Contributions are welcome through issues and pull requests.

Original source, authorship and [GPL license](COPYING) are retained. Historical source outside `src/` remains reference material and is not imported by the modern package. No replacement repository has been created.

## Updating a modern checkout

The historical Python 2/SVN updater has been retired. Its original implementation is retained in `legacy/update.py` for reference only and must not be executed. The root `update.py` is a safe Python 3 migration notice, not an automatic updater. To update a reviewed checkout, use Git to inspect and select changes, then reinstall the modern package inside its virtual environment using `python -m pip install --upgrade .`.

For the module-by-module restoration checklist and technology choices, see
[MIGRATION_MATRIX.md](MIGRATION_MATRIX.md). The full historical functionality is
not yet present in the active alpha package.