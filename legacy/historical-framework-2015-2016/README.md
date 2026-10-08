# Subterfuge historical framework, 2015–2016

**Archived, not modernized.** The source tree beneath this directory is
the 2015–2016 Subterfuge implementation, with previous 2026 reference-only
maintenance comments preserved. It is not installed, tested as active
functionality, or imported by the maintained Python 3 runtime.

Django 1.x, Twisted/SSLStrip, old JavaScript, credential/session handling,
historical network injection and legacy service scripts are out-of-date.
**Do not run historical setup scripts, root launchers, interception modules
or old example network configs on production systems.**

All original paths beneath this archive root retain their original bytes,
including original third-party attribution and copyright headers. A file
map with SHA-256 provenance is in the repository root:
`LEGACY_ARCHIVE_FILE_MAP_2026-10-09.csv`. The public branch
`archive-legacy-original-2026-10-09` preserves the complete pre-move
repository snapshot for forensic and historical comparison.

The exact original GPLv3 text has been relocated from root COPYING
to root LICENSE without any byte changes (SHA-256: 8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903).
Historical files with other SPDX/license notices keep their own terms.

Modern code lives in `src/subterfuge/`, with current README and tests at
repository root. This archive is excluded from wheel and sdist packages.
