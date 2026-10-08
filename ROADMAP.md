# Maintenance roadmap

Last checkpoint: 2026-10-08, Europe/Brussels.
Repository: https://github.com/VIG-tekh-labs/Subterfuge-Framework
Reference branch: master.
Publication parent: 634979fdb8cc71f309bb168706906be7a6817e61.

## Start here

The modern assessment runtime is 2.0.0a1. It is an installable alpha, not complete historical feature parity. Use README.md for installation and CAPABILITIES.md for the migration matrix. Historical source remains in the repository and is not imported by the modern package. No replacement repository was created.

## Owner requirements

- Restore usability on current machines and review every historical capability, not ARP alone.
- Keep documentation, instructions, comments and commit messages in English.
- Preserve authorship and license; add no generated branding or signatures.
- Automatically update this roadmap after development steps, checks, publication, failures and before interruption.
- Keep checkpoint bookkeeping in the background. Report newly updated directories once.
- Count functional modernization separately from cosmetic maintenance.
- Do not claim full compatibility, released status or feature parity without checks.

## Functional changes in this checkpoint

- Publish src/subterfuge, CLI and a loopback-only dashboard.
- Add pyproject.toml packaging for Python 3.11+, without core runtime dependencies.
- Replace the root privileged Python 2 installer with a setuptools shim; preserve the previous installer in legacy/setup.py.
- Import classic PCAP with Ethernet, VLAN and Linux cooked headers; consolidate ARP conflicts and bound input/resource sizes.
- Import standard Nmap XML including the normal plain DOCTYPE; reject XML entities, external DTDs and excessive nesting.
- Retain IPv4/IPv6 inventory, ports, service products/versions and OS evidence.
- Add service transport review items with explicit uncertainty about STARTTLS, redirects and policy.
- Add inspect-tls: normal certificate-verified TLS connection, negotiated cipher/protocol and expiry review.
- Bound dashboard uploads; validate Host, Origin and session token; use CSP and local assets.
- Add atomic private JSON exports, optional passive Scapy capture and explicit bounded Nmap host discovery.
- Add 50 regression tests and a CI matrix requesting Linux/Python 3.11–3.14 plus Windows/macOS/Python 3.12.

## Actual validation

- Linux, Python 3.12.14: all 50 tests passed from source and against an installed wheel.
- Wheel built using setuptools 84.0.0 and installed into a fresh venv without package-index access.
- Installed doctor and synthetic demo passed outside the source directory.
- Local TLSv1.3 handshake passed using a temporary trusted localhost certificate; expiry finding observed.
- The first additional TLS fixture encountered a server-side broken pipe from TLS session ticket timing. Disabling tickets in the fixture resolved the race; certificate verification was not disabled.
- No external scan, live capture or historical interception script was executed.
- Dashboard HTTP boundary tests passed; visual browser validation is still pending.
- CI results, Windows/macOS behavior and Python versions other than 3.12 remain unverified.

## Historical capabilities

CAPABILITIES.md identifies ARP interception, DHCP race, WPAD/NetBIOS, wireless AP, SSLStrip/proxy, credential/session handling, HTTP injection and other plugins. These historical implementations are retained, not restored. POODLE, Heartbleed and SSLv3 downgrade were advertised as future roadmap items; dedicated modules were not found in inspected paths. New TLS inspection is a separate assessment function, not a replacement claiming interception parity.

## Exact next actions

1. Verify published paths, branch head and CI results. If workflow publication is rejected, retain the prepared workflow and record the exact error.
2. Perform dashboard browser QA and fix any usability problems.
3. Add PCAPNG import with malformed-input and resource-limit regressions.
4. Add passive DHCP and name-resolution evidence analysis with isolated fixtures.
5. Review historical proxy/plugin contracts against modern TLS and browser protections before porting them.
6. Validate Scapy/Nmap adapters in an isolated test network; they remain optional and unverified here.

## Previous checkpoints

Commit d917e53bfe46647495794c2c8897789c61c2e94e published the initial documentation.
Commit 634979fdb8cc71f309bb168706906be7a6817e61 added 71 comment-only markers and 26 directory notes; no functional fixes or dependency upgrades were included. Filesystem touch is not tracked by Git.
Earlier GitHub writes returned 403 Resource not accessible by integration; installation/reconnection subsequently restored publishing.

## Continuation discipline

Read the current remote head before writes. Preserve unrelated work and use an expected-head lease. Keep separately prepared working copies intact; one older draft exists at /workspace/scratch/977d15b140db/Subterfuge-Framework and may contain unpublished changes. The source used for this checkpoint was validated independently. Never overwrite another working copy as part of reconciliation. Record actual checks and remaining gaps; maintain an explicit alpha status.

## Continuation checkpoint — 2026-10-08 (new session)

- Verified the connected GitHub integration can read this repository, its README, ROADMAP, CAPABILITIES, MAINTENANCE, packaging metadata and source.
- Verified master HEAD at the start of this session: `4bc3c2ec439d6c978d5b51a3c9d310c39aed590e`.
- Created dedicated continuation branch `modernization-2026-10-08-continuation` from that exact commit; master was not modified.
- Remote Desktop Commander device `eden` was offline when checked. No dependencies were installed and no runtime tests were executed in this session; previous 50-test checkpoint remains historical evidence only.
- Confirmed PCAPNG import remains absent; `src/subterfuge/analysis.py` explicitly rejects PCAPNG. Preserve input limits, parsing safety and synthetic test coverage during implementation.
- Immediate next action: obtain an available isolated execution environment, implement and test bounded PCAPNG parsing with malformed-input fixtures, run the complete regression suite, inspect GitHub CI, and record the results before publication or feature claims.
- Documentation rule: update this roadmap after every verified checkpoint; only claim tests that were actually executed. Do not merge continuation into master without owner authorization.

## PCAPNG implementation checkpoint — 2026-10-08

- Commit `cc247f214b0a43fba41b50b24d79f800bf3fe400` adds an initial PCAPNG section/interface/enhanced-packet reader to `src/subterfuge/analysis.py` on the continuation branch.
- Status: **UNTESTED DRAFT**. Desktop Commander `eden` remains offline and direct Git clone was blocked by DNS in the fallback environment. Do not advertise PCAPNG support as validated or merge this branch.
- Next action is mandatory: review the parser, simplify packet-ignore accounting, add PCAPNG fixtures and malformed-input tests, execute the full regression suite, and correct any defects before release.

## Continued parser review — 2026-10-08

- Commit `3e3abb5933b50099614b7bee9cd8686b4e3c7c1d`: simplified PCAPNG ignored-packet accounting.
- Commit `1f76782f1729807cda69fafd9701e0442b109c54`: added `tests/test_pcapng.py` with synthetic endian, malformed-length, missing-interface and non-ARP cases.
- **Not validated**: no Python execution environment was available through Desktop Commander. Test files were committed but have not run; all PCAPNG work remains draft. Do not merge or release.
- Next: run `python -m unittest discover -s tests -v` in a Python 3.11+ venv; correct failing fixtures/parser; verify dashboard PCAPNG import and CI; inspect historical modules one at a time. Keep `master` unchanged.
