# Licensing and provenance review

**Status: preliminary file-level review, not a legal clearance or relicensing notice.**

- The complete original GNU General Public License version 3 text is now preserved byte-for-byte in root `LICENSE` (original SHA-256 8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903). The new root `COPYING` contains a pointer to that full text. No relicensing was performed.
- The modern distributable's `pyproject.toml` currently declares `GPL-3.0-or-later`. Its active package is discovered only under `src/subterfuge`; check actual wheel/source distribution contents before any release.
- Archived `legacy/historical-framework-2015-2016/sslstrip/` files display copyright notices for Moxie Marlinspike and GPL version 3 or later. Preserve their attribution and conditions.
- Archived `legacy/historical-framework-2015-2016/modules/harvester/ftp_password_sniffer.py` credits Franck Tabary and explicitly specifies **GPL version 2** (not an explicit 'or later' grant). Combining that GPLv2-only component into a work requiring GPLv3 terms may create a licensing incompatibility; the file is retained only as an unported historical reference, not imported by the modern package.
- Historical jQuery / jQuery UI artifacts now under `legacy/historical-framework-2015-2016/templates/` are third-party assets; their precise versions and corresponding licenses require verification before reuse or bundling. The modern dashboard does not load them.
- The amount of changed code, by itself, does not terminate obligations to authors of copyrighted material that is retained or adapted. There is no automatic 'percentage rewritten' licensing threshold.
- An independently developed, non-derivative program may be offered under other terms by its rights holders. Alternatively, all required copyright holders may expressly grant suitable relicensing permission. A new repository name or package name alone does not change rights.
- GPL permits commercial distribution but imposes source and license obligations for covered redistribution. Running the software privately generally does not trigger the same distribution conditions.
- Do not remove historical copyright notices or assume that applying `GPL-3.0-or-later` to `pyproject.toml` overrides narrower per-file licenses.

Next review: enumerate third-party asset license notices, inspect actual packaging manifests, identify any copied code in modern source and determine whether separate legacy components should be redistributed at all. Consult a qualified open-source licensing specialist before changing the project's public license.

## Relicensing decision gate — October 2026

**Current decision: retain the existing GPL declarations pending a rights-holder and provenance audit.** Rewriting a large fraction of the source does not automatically extinguish copyright obligations for retained or adapted protected expression. The GNU GPL FAQ states that GPLv2-only and GPLv3 code cannot generally be combined and conveyed as a single GPLv3-covered work; an explicit "GPLv2 or later" grant may change that analysis. Source: https://www.gnu.org/licenses/gpl-faq.en.html

Before proposing an alternative license:
1. Identify copyright holders, SPDX/license notice and provenance for **every** source and asset to be included in a distributable artifact.
2. Verify whether modern modules contain copied/adapted original GPL expression, including nonliteral substantial structure, rather than assuming isolation in `src/` automatically makes the work independent.
3. Verify separately that the retained historical FTP sniffer expressly marked GPLv2-only is **absent** from the actual modern wheel and source distribution; document whether a separate historical source archive is being redistributed.
4. Record third-party JS/CSS/icon attribution and licenses. Avoid shipping the historical jQuery/Twisted/Django assets merely for historical feature parity.
5. Obtain express permissions from all relevant rights holders before relicensing derivative material, or undertake a genuine independent implementation with legal review.
6. Distinguish running privately from conveyance to users; publishing GitHub sources and distributing builds requires license-specific compliance review.

**Do not modify the original GPL text in `LICENSE`, delete third-party copyright notices, or claim independent relicensing without appropriate permissions.** The package license-files path now refers to the unchanged LICENSE text. This assessment is preliminary, not legal advice.
