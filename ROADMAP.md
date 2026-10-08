# Maintenance roadmap

Last checkpoint: 2026-10-08T15:45+02:00, Europe/Brussels.

## Start here

Repository: https://github.com/VIG-tekh-labs/Subterfuge-Framework
Reference branch: `master`.
Inspected baseline: `6c35097c202ee2c23fa68ab966711c9cf9300c95`.
Development branch in the current working copy: `maintenance/python3-modernization`.

The goal is to make this fork usable on current environments, replace obsolete components and add supported features. Keep existing authorship and license information. Do not assume that a draft implementation restores every historical capability.

## Current owner requirements

- Make development activity visible in the existing repository as soon as write access is restored.
- Clearly mark the current development version as not yet functional and validated as a complete application.
- Accept proposed contributions for review, record findings and relevant checks, and avoid presenting unvalidated changes as release-ready.
- Automatically maintain this roadmap and the project requirements after each development step, check, publication, failure or blocker, and before interruption. Do not wait for an owner reminder.
- Use English in repository documentation, instructions, code comments and commit messages; do not add generated branding or signatures.

## Verified facts

- The runtime source on `master` is still the historical implementation. This documentation checkpoint changes only `README.md`, `ROADMAP.md` and `MAINTENANCE.md`.
- The initial audit found 26 Python 3 syntax or indentation failures among 59 historical Python files.
- The historical installer uses system-wide file operations and Django 1.7.
- The historical updater depends on obsolete SVN and custom update mechanisms.
- Historical control scripts include broad firewall resets.
- No new repository has been created.

## Draft work — not a tested release

A separate working copy contains:
- Historical files preserved under `legacy/`, with `COPYING` retained at the root.
- A `src/subterfuge/` Python 3 package.
- A command-line interface and a loopback-only local dashboard.
- Classic PCAP ARP analysis, host inventory, conflict review and JSON reports.
- Nmap XML import, optional bounded Nmap discovery and optional passive Scapy capture.
- Packaging metadata targeting Python 3.11 or newer.

The source draft passes initial syntax and synthetic demo smoke checks. It has not been installed from a wheel, committed or published; full functional and interface validation remains pending. Historical interception modules are preserved for reference and are not restored in the draft runtime. Review the capability migration before claiming feature parity.

### Initial checks completed

On 2026-10-08, with Python 3.12:
- Parsed all seven current Python modules under `src/subterfuge/`; no syntax failures.
- Executed `PYTHONPATH=src python3 -m subterfuge demo`; exit code 0.
- The synthetic capture contained two ARP replies claiming `192.0.2.10` from two different MAC addresses. The report recorded one host and one `arp_address_conflict` finding, as expected.
- No external network scan or live packet capture was run. These checks do not establish clean installation, adapter compatibility or complete interface behavior.

## Known issues and validation gaps

1. The Nmap XML parser currently rejects the harmless DOCTYPE in normal Nmap output. Accept the standard declaration while rejecting external/internal entity declarations and unsupported encodings.
2. The packaging minimum setuptools version must match the license metadata syntax.
3. Wheel installation, functional tests, documentation completeness and dashboard visual checks remain pending.
4. The capability migration is incomplete. Historical interception modules have not been restored in the new runtime.

## Documentation and access checkpoint

This maintenance restart updates `README.md`, adds this roadmap and adds `MAINTENANCE.md`. All historical runtime source, history and the root `COPYING` file are preserved on `master`. The separately drafted Python 3 source is not part of this documentation change.

Earlier publication attempts returned HTTP 403, `Resource not accessible by integration`, while the owner account already had administrator and push permissions. The connection listed no GitHub App installations. On 2026-10-08, the owner reconnected GitHub and completed the installation flow. The integration now returns an installation belonging to `VIG-tekh-labs`. The reference branch was refreshed before preparing this change.

User repository permissions and integration authorization are separate. Always verify actual writes and the resulting branch head. Do not repeatedly retry a write when the authorization state has not changed.

## Exact next action

Fix the XML and packaging issues in the source draft, then validate a clean installation and meaningful functional behavior before a source release. Synchronize the development branch with this documentation checkpoint while preserving uncommitted work.

1. Fix standard Nmap XML import and compatible packaging metadata.
2. Review historical capabilities and record what is retained, replaced or still pending.
3. Add meaningful parser, CLI, HTTP boundary and optional adapter checks.
4. Validate a clean installation and the synthetic demo without scanning external systems.
5. Update this roadmap with changed paths, validation results, unsupported features and the exact next action before publishing source changes.

For every publication, refresh the target branch, preserve unrelated files, verify the resulting commit and read back the changed files. If publication is denied, record the exact response and retain the source checkpoint. Never describe the complete application as functional or validated before the necessary checks pass.

## Checkpoint discipline

Automatically update this file after each development step, check, publication, failed attempt or blocker, and before starting a long step or ending a session. Do not wait for an owner reminder. Record changed paths, actual validation, publication state, remaining issues and the exact next action. Keep routine checkpoint bookkeeping in the background; report newly updated directories once.

Never mark implementation, tests or publication complete without corresponding evidence. Use English for repository documentation, instructions, comments and commit messages. Keep the repository free of generated branding or signatures.

## Repository-wide maintenance checkpoint — 2026-10-08

Owner requested visible activity across historical files and directories, with cosmetic maintenance counted separately from real modernization. Git does not record filesystem touch operations.

This checkpoint adds comment-only markers to 71 historical Python, JavaScript and CSS files and a maintenance note in all 26 existing directories. It updates README.md and this roadmap and adds MAINTENANCE_COUNTS.md. It introduces no dependency upgrades or functional fixes. Binary assets, databases, compiled files, license text and unsupported text formats retain their original content. The large bundled jquery-ui.js is also unchanged. Directory activity does not imply every contained file was modified.

The separate working copy contains unpublished development work. Preserve it and validate its latest state before publication. Next: reconcile this checkpoint with the development branch, verify packaging and functional tests, then publish actual runtime modernization with a separate change count. Do not treat comment-only maintenance as a modern release.
