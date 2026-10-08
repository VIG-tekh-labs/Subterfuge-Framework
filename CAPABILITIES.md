# Capability migration

This is an alpha modernization, not historical feature parity. Source paths below refer to historical files retained in the repository; presence is not proof of current compatibility.

| Historical capability | Evidence | Modern runtime status |
| --- | --- | --- |
| ARP observation and address inventory | utilities/arpwatch.py, utilities/scan.py | Classic PCAP/experimental PCAPNG analysis, VLAN and Linux cooked captures; optional passive Scapy adapter |
| ARP interception | utilities/arpmitm.py, utilities/rearp.py | Historical active implementation retained for reference, not ported; safe offline evidence analysis added where noted |
| DHCP race / rogue DHCP | utilities/dhcprace.py, utilities/dhcptools.py | Historical active implementation retained for reference, not ported; safe offline evidence analysis added where noted |
| WPAD / NetBIOS | utilities/wpadhijack.py, utilities/nbtools.py | Historical source retained; not ported |
| Wireless access point | utilities/apgen.py | Historical source retained; not ported |
| SSLStrip / interception proxy | sslstrip/, sslstrip.py, attackctrl.py | Historical source retained; not ported. New verified TLS endpoint inspection is a separate assessment function |
| HTTP / FTP credential handling | modules/harvester/ | Historical source retained; not ported |
| Session cookies | modules/sessionhijacking/ | Historical source retained; not ported |
| HTTP code injection | modules/httpcodeinjection/ | Historical source retained; not ported |
| Tunnel blocking and denial-of-service modules | modules/TunnelBlock/, modules/dos/ | Historical source retained; not ported |
| Django dashboard / plugins | main/, modules/, templates/ | New loopback dashboard supports evidence imports; historical plugin contracts not restored |
| Installation / updates | setup.py, update.py | Isolated pip installation replaces privileged installer; old installer retained in legacy/setup.py |
| POODLE / Heartbleed / SSLv3 downgrade | Historical README upcoming-content list | Announced in historical roadmap; no dedicated implementation found in inspected paths |

## Passive capture modernization

- DHCPv4: static UDP metadata decoder; reports message type, server identifier
  and presence of WPAD option 252, without retaining option contents.
  Historical DHCP race/rogue reply code is not part of the modern runtime.
- NetBIOS name service: offline first-level name-query decoder with WPAD
  observation; historical response/spoofing code is not part of the runtime.
- A bounded, deduplicated `network_evidence` summary is integrated into classic
  PCAP and experimental PCAPNG analysis and shown in the local dashboard.
  Ethernet/VLAN and Linux cooked v1/v2 IPv4 UDP are supported.
- These are passive parsers for unfragmented IPv4 UDP only. No DHCP/NBNS
  packet transmission, IPv4 reassembly, full DNS parser or live capture
  integration is claimed.

## New supported assessment paths

- Nmap XML imports include IPv4/IPv6 hosts, open ports, service names, product/version evidence and OS guesses.
- Transport review items identify service records lacking a recorded SSL tunnel. These are not confirmed vulnerabilities: STARTTLS, redirects and policy require separate verification.
- `inspect-tls` verifies certificate trust and hostname, records the negotiated TLS version/cipher and checks imminent expiry. It does not perform interception, downgrade tests or exhaustive protocol enumeration.

## Compatibility and validation

The offline core has no runtime dependencies and targets Python 3.11+. Linux/Python 3.12 was exercised locally. The CI matrix requests Linux/Python 3.11–3.14 plus Windows/macOS/Python 3.12; results must be checked before expanding verified support claims. Live Scapy capture requires OS capture permissions and appropriate platform drivers. Nmap discovery requires Nmap installed separately. Neither live adapter was validated against a real network in this checkpoint. Experimental PCAPNG enhanced-packet parsing is available only on the modernization branch and has passed synthetic fixtures on Linux/Python 3.14; real capture compatibility is not yet validated.

## Next migration work

1. Expand PCAPNG regression coverage with real captures and additional malformed-input/resource-limit cases.
2. Add passive DHCP and name-resolution evidence analysis with isolated fixtures.
3. Review historical proxy and plugin contracts against modern TLS and browser protections, documenting protocol and environment constraints before implementation.
4. Verify live adapters in an isolated test network and reconcile historical functionality one module at a time.