# Maintenance instructions

## Root cleanup approved; source of truth is modern src/subterfuge

- The owner explicitly authorized applying modernization to the default branch master. Master fast-forwarded without force from 4bc3c2e to f50bd4a (79 commits).
- To remove the 10–11-year-old files from the active GitHub tree, all 193 tracked files in the legacy directory were deleted from the maintained branch (190 older framework files, archive README, original update.py and setup.py).
- The separate branch archive-legacy-original-2026-10-09 preserves the old source, history and copyright attribution. No history rewrite, force push, archival branch deletion or relicensing was performed.
- The active Python 3 runtime remains under src/subterfuge; it is version 2.0.0a2 alpha and does not restore unported historical interception features.
- The original complete GPLv3 text remains byte-for-byte unchanged in LICENSE, with COPYING as a pointer. Historical relocation maps remain documentation, not active source paths.
- Verify Python/Node regression tests, wheel and source archive hygiene, and six-platform CI after this cleanup. Synchronize both modernization and master through non-forced fast-forward, then verify the GitHub default root has no legacy folder.
- Remaining modernization: diverse actual authorized PCAP/PCAPNG captures, safe Scapy passive lab testing, browser accessibility/keyboard checks, provenance and module-by-module feature migration decisions.



1. Read `ROADMAP.md` before changing files. Confirm repository, branch, current commit and actual published state.
2. Continue in https://github.com/VIG-tekh-labs/Subterfuge-Framework. Do not create a replacement repository.
3. Use English in documentation, instructions, code comments and commit messages. Preserve original authorship and license information.
4. Review historical functionality before removing or replacing it. An archived module is not a restored feature.
5. Keep installation isolated. Do not run the historical installer or scripts that reset host firewall rules as part of routine validation.
6. Validate with synthetic captures and isolated fixtures first. Document unsupported features and unresolved failures.
7. Keep status statements precise: draft, tested, committed and published are separate states.
8. Automatically update `ROADMAP.md` after each development step, check, publication, failure or blocker, and before interruption. Do not wait for an owner reminder. Record changed paths, actual check results, publication state, remaining issues and the exact next action so work can continue from the recorded state.
9. Notify the owner of changed paths, validation results and publication status after each checkpoint.
10. Do not insert generated branding or signatures into project files.
11. Keep the development status explicit: initial checks do not establish a functional, validated complete application. Review external contributions and record their checks before including them in a release.

## Historic source archive workflow

The legacy Django/Twisted and old UI sources have moved intact into `legacy/historical-framework-2015-2016/`. Their full pre-move layout can be inspected in branch `archive-legacy-original-2026-10-09`. Never treat a renamed old file as a completed port. Confirm original SHA-256 values using LEGACY_ARCHIVE_FILE_MAP_2026-10-09.csv and preserve GPL notices.
