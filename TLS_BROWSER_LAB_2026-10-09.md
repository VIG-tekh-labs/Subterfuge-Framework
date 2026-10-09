# TLS & local Browser Lab — Subterfuge 2.0.0a3

## Available modules

The modern Python 3 runtime is standalone and does not depend on a local agent.

1. **tls-decrypt** — TShark/Wireshark offline decryption when the user supplies a
   PCAP or PCAPNG capture and the corresponding SSLKEYLOGFILE secrets, acquired
   from a browser/application that the operator controls or administers.
   TShark handles cryptography; Subterfuge extracts limited HTTP/1 and HTTP/2
   metadata. Decrypting HTTP/3/QUIC is NOT claimed by the current summary tool.
2. **proxy-lab** — local, explicitly configured MITMProxy (mitmdump) regular
   HTTP/HTTPS test proxy. It binds only to loopback and requires the explicit
   --authorized-clients confirmation. A client must be manually pointed at
   the proxy and explicitly trust the laboratory certificate authority.
   Nothing installs that trust or changes the network automatically.
3. **browser-lab** — an unpacked Chromium Manifest V3 companion with a visible
   on/off switch, a read-only diagnostic button and a setting that persists
   across browser restarts. The content script is scoped to 127.0.0.1 and
   refuses any page that is not the recognizable Subterfuge dashboard.
   No third-party website hook, hidden persistence, cookies, credentials,
   history collection, arbitrary JavaScript execution, or browser elevation.
4. **import-bettercap** — an offline, sanitizing JSON event import compatible
   with an authorized Bettercap REST API /api/events JSON export. This accepts
   discovery/network host events only, ignoring offensive, key and payload
   events. Bettercap itself is not executed or required for this import.
5. **agent-capabilities** — machine-readable tool contract so a local automation agent can discover actions. A Python function,
   subterfuge.agent_integration.run_authorized(action, args, mission_policy),
   requires a per-task explicit list of allowed actions. Sensitive TLS
   actions additionally require allow_sensitive_tls and exact allowed_files;
   active network operations require allow_active_network and an exact
   allowed_targets match. A caller policy can further restrict operations, but
   cannot bypass the OS or Subterfuge safety checks.

## Standalone commands

Requires Python 3.11+:

    python3 -m venv .venv
    . .venv/bin/activate
    python -m pip install .
    subterfuge doctor

To analyze a locally recorded, authorized TLS session (on Unix the TLS key log
must belong to you and have permission 0600):

    chmod 600 ~/captures/session.keys
    subterfuge tls-decrypt --pcap ~/captures/session.pcapng --keylog ~/captures/session.keys --output ~/captures/summary.json

The default summary does **not** contain request URI paths, secret values,
cookies, passwords, or HTTP bodies. To intentionally include sensitive fields,
on your own permitted test captures only:

    subterfuge tls-decrypt --pcap ~/captures/session.pcapng --keylog ~/captures/session.keys --include-uris --export-decrypted-json ~/captures/details.json

The decrypted JSON output is created mode 0600 and never overwrites an existing
file. Handle it as sensitive evidence. Unlike intercepting a TLS handshake,
providing the corresponding session secrets makes decryption possible.

Optional dependencies:

- TShark 4.x from Wireshark must be installed for tls-decrypt. Not bundled.
- mitmdump from mitmproxy 12.x must be installed for proxy-lab. Not bundled.
- Bettercap is not required; export JSON records manually from an authorized
  Bettercap endpoint or supported local program to import.
- The core Python package has no mandatory third-party runtime dependencies.

Opt-in, LOCAL-ONLY proxy on its own computer (not a general LAN proxy):

    subterfuge proxy-lab --authorized-clients --host 127.0.0.1 --port 8081

The operator then configures their own browser HTTP proxy to 127.0.0.1:8081
and manually installs the laboratory mitmproxy CA trust only in their own test
profile. Some pinned applications will not trust the CA. Remove that test trust
after the experiment. The proxy does not save flow files automatically. There
is no transparent network interception, DNS hijacking or automatic infection.

Bettercap example after exporting the events to a local JSON file:

    subterfuge import-bettercap ~/captures/bettercap-events.json --output ~/captures/events-summary.json

Browser companion:

    subterfuge browser-lab

In Chromium navigate to chrome://extensions, enable Developer mode, choose
Load unpacked, and select the printed browser_lab directory. Pin the visible
Subterfuge Lab Companion icon. Activate Lab mode and click Inspect current tab
while viewing a Subterfuge dashboard served at http://127.0.0.1:8080/.
The preference survives browser restart because of chrome.storage.local,
but the script does not run in closed tabs and never follows unrelated sites.

## Agent policy precedence

Standalone installation does not require any external agent files, credentials or services.
When a local agent calls Subterfuge, it should supply the scoped mission policy and
the explicit action to run through its existing task executor. The
run_authorized interface enforces the provided allowed_actions,
allowed_files, allowed_targets and optional affirmative flags; network and
sensitive operations also obey the independent technical limits.

Example for an approved offline automation task in Python:

    from subterfuge.agent_integration import run_authorized
    policy = {"allowed_actions": ["doctor"]}
    report = run_authorized("doctor", {}, policy)

The bridge excludes unattended proxy launching and active live capture.
It never grants root, changes certificate trust, disables a browser's
security controls, or sends messages to third-party browser sessions.

## Verified boundaries and limitations

A self-generated TLS 1.3 connection on loopback was captured as PCAPNG,
five TLS key-log entries were generated by the controlled client, and TShark
recovered two HTTP messages and the expected synthetic request URI. Offline
unit tests are separate from that genuine loopback test.

This does not mean Subterfuge can extract secrets from TLS handshakes,
decrypt an arbitrary user's HTTPS, defeat certificate pinning or keep
a BeEF hook running on someone else's browser. Browser controls, OS trust,
TLS session secrets and user authorization remain separate.

The extension is meant to persist as an installed, visible, opt-in laboratory
utility. It may be disabled or uninstalled through Chromium's normal controls.
No administrator/elevated privileges or silent installation is needed.

## Local release verification — pre-publication

- System test on Kali: TShark 4.6.6 processed a genuine, self-generated
  TLS connection captured on loopback as PCAPNG. The controlled client
  generated five session-key entries, and Subterfuge recovered two HTTP
  messages and the synthetic request path.
- System proxy test on the same loopback: mitmdump 12.2.3, started through
  subterfuge proxy-lab, forwarded an explicit HTTP request to a temporary
  127.0.0.1 test server and returned HTTP 200 with the expected body.
- The proxy code disables external version-check traffic and refuses all
  non-loopback listeners, including an explicit LAN flag, until a future
  authenticated multi-client transport is developed and tested.
- The Chromium extension Manifest V3 test harness checks the opt-in switch,
  persistence of the preference across a simulated browser restart, visible
  local indicator, explicit disable and rejection of non-Subterfuge pages.
- Automated Python tests, JavaScript schema checks and package QA must be
  rerun on the published commit; no installation on third-party clients was
  performed. In particular, actual persisted MV3 UI state has not been
  observed across a manual Chromium restart on this workstation.

## Publication and continuous integration

The TLS/proxy/browser/agent version 2.0.0a3 was published in feature commit `6d5329320e9669a54217ac996731447479a59440` with a cross-platform test fix in `02aaa76d3529b599e445b24d6377a3bea076c2c8`. Six GitHub Actions matrix jobs succeeded in [run 37862358235](https://github.com/VIG-tekh-labs/Subterfuge-Framework/actions/runs/37862358235). A clean checkout of the published master code discovered 134 Python tests (132 successful, two expected skips) and passed Node Browser Lab and saved-report validations. The live agent tool registry still needs to import the optional agent bridge and pass its approved mission policy before The calling agent can use it.

