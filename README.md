# Subterfuge Framework

**Modernization in progress — version 2.0.0a1.** The modern assessment core is installable; the complete historical framework is not yet restored or validated.

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

## Evidence and assessment

```sh
subterfuge analyze-pcap capture.pcap --output report.json
subterfuge import-nmap inventory.xml --output inventory.json
subterfuge inspect-tls --host example.com --output tls.json
subterfuge interfaces
```

The dashboard runs on `127.0.0.1` and imports PCAP/Nmap XML files locally. PCAP limits are 16 MiB for dashboard uploads and 64 MiB for CLI imports. PCAPNG requires conversion before import. Nmap service/version and OS data are retained as reported evidence. Transport review items require investigation; they do not establish exploitation or missing STARTTLS.

TLS inspection opens one normal certificate-verified connection to the specified endpoint, records its negotiated protocol/cipher and reports certificate expiry or verification failure. It does not enumerate every server configuration or test HSTS.

Optional live adapters, only on a network you are authorized to assess:

```sh
python -m pip install '.[capture]'
subterfuge capture --interface eth0 --duration 30 --output arp.json
subterfuge discover --target 192.0.2.0/24 --output hosts.json
```

Nmap must be installed separately. Discovery performs host discovery, not a service scan. The interface name above is an example: use `subterfuge interfaces`. Capture permissions and drivers depend on your OS. Live adapters remain unvalidated in this checkpoint.

## Validation and continuity

```sh
python -m pip install .
python -m unittest discover -s tests -v
```

Read [ROADMAP.md](ROADMAP.md) first, then [CAPABILITIES.md](CAPABILITIES.md) for historical module coverage and [MAINTENANCE_COUNTS.md](MAINTENANCE_COUNTS.md) for cosmetic versus functional changes. Follow [MAINTENANCE.md](MAINTENANCE.md) when continuing development.

Linux/Python 3.12 passed local checks. Other OS/Python combinations are CI targets, not yet verified support claims. Contributions are welcome through issues and pull requests.

Original source, authorship and [GPL license](COPYING) are retained. Historical source outside `src/` remains reference material and is not imported by the modern package. No replacement repository has been created.
