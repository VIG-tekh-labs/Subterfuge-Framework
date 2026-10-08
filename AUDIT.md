# Subterfuge modernization audit

Checkpoint: 2026-10-08. Target: `modernization-2026-10-08-continuation`, separate from `master`.

## Scope and evidence

An automated sweep classified all **293** paths tracked at the start of this checkpoint; see `FILE_AUDIT.md`. Python 3.14 AST parsing succeeded for **56 of 82** tracked `.py` files, and failed for **26**, mostly Python 2 legacy code. This is a syntax-only survey: successful parsing does not establish operational compatibility.

### What is active and what is not

- Active package: `src/subterfuge/` installed via setuptools/venv, with standard-library-based offline capture analysis, local HTTP interface, Nmap XML import and TLS endpoint inspection. Optional Scapy/Nmap adapters remain environment-dependent.
- Historical code outside `src/` (including `main/`, `cease/`, `modules/`, `sslstrip/`, `utilities/`, root `manage.py`, `settings.py` and `templates/`) is kept for feature analysis but is **not imported by the modern distribution**.
- Django 1.x project configuration and Twisted interception architecture are obsolete. Do not install or upgrade them merely to make historical files importable: first decide which functionality remains legitimate, safe and useful, then implement maintained interfaces.
- The old SSLStrip/downgrade assumptions do not generally match modern TLS, HSTS and browser behavior. Restoring attack parity is not a claim of this alpha.

## Findings and action priorities

| Priority | Finding | Action |
| --- | --- | --- |
| Critical | Public Git history contains a private-key PEM and hard-coded legacy Django key | Remove them from current tracked branch; assess actual deployment and rotate secrets if used; owner-led history remediation later |
| High | Tracked credential-related file, databases and logs | Remove these generated/runtime artifacts from the current branch; avoid redistributing archived data |
| High | 50 tracked historical `.pyc` files | Remove from tracking and exclude future binary artifacts |
| High | 26 legacy `.py` files fail Python 3 syntax parsing | Document and migrate functions selectively, retaining historical provenance |
| High | GPLv3 project plus a historical GPLv2-only third-party file | Keep separate and obtain professional licensing review; see `LICENSING.md` |
| Medium | DHCP/NBNS passive analyzers not yet in PCAP report | Implement bounded capture aggregation with explicit tests, no transmission |
| Medium | Existing dashboard focused on ARP/inventory only | Surface passive metadata and use browser QA; avoid unsafe HTML insertion |
| Medium | Optional Scapy/Nmap live adapters and multi-OS matrix insufficiently verified | Isolated, authorized integration tests and CI review |
| Medium | PCAPNG initially tested only on synthetic data | Validate real capture files and malformed cases before claiming production support |
| Low | Legacy UI assets and jQuery files are unmaintained | Keep as historical references only; modern UI is self-contained |

## Non-goals for routine modernization tests

Do not execute old privileged installers, host firewall resets, packet interception, credential interception or network disruption. These actions are not required for safe parser and dashboard regression tests. Do not claim that a preserved historical module is restored.

## Next checkpoint

Run all regression tests, build and inspect wheel/sdist, perform Chromium QA, review open CI runs, and publish code plus checkpoints to the continuation branch without merging `master`.

## Local TLS dashboard follow-up (alpha 2)

The modern dashboard now exposes the previously CLI-only `inspect_tls`
function behind its same-origin session token. It accepts a bounded JSON
request with host, port and timeout and runs one certificate-verified
connection only after user action. Invalid content types, oversized input,
malformed JSON and invalid parameters are tested. No historical SSLStrip
or Twisted intercepting proxy is reactivated.

## Reproducible release and repository hygiene checks

`tests/test_repository_hygiene.py` rejects any newly tracked compiled
Python bytecode, runtime logs, key files and known historical credential/DB
paths in a Git checkout, and detects a literal Django SECRET_KEY. These tests
protect the **current branch** but cannot erase secrets from public history.

`tests/test_external_capture_writer.py` can validate PCAPNG interoperability
with Wireshark `editcap`, when available; this is not a substitute for a
diverse corpus of real authorized captures.

`qa/loopback_nmap_smoke.py` checks a self-hosted ephemeral TCP service on
127.0.0.1 only; it is an opt-in test, not an external scan or a CI requirement.