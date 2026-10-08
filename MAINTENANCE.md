# Maintenance instructions

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
