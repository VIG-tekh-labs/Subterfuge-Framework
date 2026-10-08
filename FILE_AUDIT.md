# Repository-wide file inventory (automated triage)

Baseline: continuation branch before this checkpoint, 293 tracked paths. This inventory programmatically classifies every baseline path; it is **not** a manual code review or functionality claim for each file. Files absent from the new branch remain in Git history.

## Categories

- Documentation / packaging: 22
- Historical / other: 16
- Historical Python / unported: 35
- Historical Python 2 / incompatible: 25
- Historical UI / asset: 113
- Legacy / GPLv2-only: 1
- Modern Python 3: 12
- New regression test: 1
- Regression tests: 11
- Removed from branch: 58

## Files

| Path | Classification | Next action |
| --- | --- | --- |
| `.github/workflows/modern-runtime.yml` | Documentation / packaging | Review and keep current |
| `.gitignore` | Documentation / packaging | Review and keep current |
| `CAPABILITIES.md` | Documentation / packaging | Review and keep current |
| `COPYING` | Documentation / packaging | Review and keep current |
| `MAINTENANCE.md` | Documentation / packaging | Review and keep current |
| `MAINTENANCE_COUNTS.md` | Documentation / packaging | Review and keep current |
| `MANIFEST.in` | Documentation / packaging | Review and keep current |
| `README.md` | Documentation / packaging | Review and keep current |
| `ROADMAP.md` | Documentation / packaging | Review and keep current |
| `__init__.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `__init__.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `attackctrl.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `base_db` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `cease/MAINTENANCE.md` | Documentation / packaging | Review and keep current |
| `cease/__init__.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `cease/__init__.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `cease/models.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `cease/models.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `cease/tests.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `cease/tests.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `cease/views.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `cease/views.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `cease/views.py~` | Historical / other | Preserve for review |
| `cert.pem` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `configure.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `credentials.txt` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `db` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `definitions/MAINTENANCE.md` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `definitions/passwordfields.lst` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `definitions/usernamefields.lst` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `exportcreds.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `harvester.log` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `httpall.log` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `legacy/setup.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `legacy/update.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `lock.ico` | Historical / other | Preserve for review |
| `main/MAINTENANCE.md` | Documentation / packaging | Review and keep current |
| `main/__init__.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `main/__init__.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `main/models.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `main/models.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `main/models.py~` | Historical / other | Preserve for review |
| `main/views.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `main/views.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `main/views.py~` | Historical / other | Preserve for review |
| `manage.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `mitmproxy.log` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `modules/MAINTENANCE.md` | Documentation / packaging | Review and keep current |
| `modules/TunnelBlock/MAINTENANCE.md` | Documentation / packaging | Review and keep current |
| `modules/TunnelBlock/TunnelBlock.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `modules/TunnelBlock/TunnelBlock.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `modules/__init__.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `modules/__init__.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `modules/db` | Historical / other | Preserve for review |
| `modules/dos/MAINTENANCE.md` | Documentation / packaging | Review and keep current |
| `modules/dos/dos.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `modules/dos/dos.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `modules/exportcreds.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `modules/exportcreds.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `modules/harvester/MAINTENANCE.md` | Documentation / packaging | Review and keep current |
| `modules/harvester/ftp_password_sniffer.py` | Legacy / GPLv2-only | Isolate; do not combine into GPLv3 derivative without license review |
| `modules/harvester/ftp_password_sniffer.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `modules/harvester/harvester.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `modules/harvester/harvester.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `modules/httpcodeinjection/MAINTENANCE.md` | Documentation / packaging | Review and keep current |
| `modules/httpcodeinjection/httpcodeinjection.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `modules/httpcodeinjection/httpcodeinjection.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `modules/httpcodeinjection/httpcodeinjection.rc` | Historical / other | Preserve for review |
| `modules/httpcodeinjection/inject.x` | Historical / other | Preserve for review |
| `modules/models.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `modules/models.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `modules/modextras.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `modules/modextras.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `modules/sessionhijacking/MAINTENANCE.md` | Documentation / packaging | Review and keep current |
| `modules/sessionhijacking/cookiestealer.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `modules/sessionhijacking/cookiestealer.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `modules/sessionhijacking/cookieswapper.js` | Historical / other | Preserve for review |
| `modules/templatetags/MAINTENANCE.md` | Documentation / packaging | Review and keep current |
| `modules/templatetags/__init__.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `modules/templatetags/__init__.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `modules/templatetags/modextras.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `modules/templatetags/modextras.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `modules/views.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `modules/views.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `pyproject.toml` | Documentation / packaging | Review and keep current |
| `scan.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `settings.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `settings.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `setup.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `src/subterfuge/__init__.py` | Modern Python 3 | Active package; continue regression and platform validation |
| `src/subterfuge/__main__.py` | Modern Python 3 | Active package; continue regression and platform validation |
| `src/subterfuge/analysis.py` | Modern Python 3 | Active package; continue regression and platform validation |
| `src/subterfuge/cli.py` | Modern Python 3 | Active package; continue regression and platform validation |
| `src/subterfuge/demo.py` | Modern Python 3 | Active package; continue regression and platform validation |
| `src/subterfuge/dhcp.py` | Modern Python 3 | Active package; continue regression and platform validation |
| `src/subterfuge/environment.py` | Modern Python 3 | Active package; continue regression and platform validation |
| `src/subterfuge/name_resolution.py` | Modern Python 3 | Active package; continue regression and platform validation |
| `src/subterfuge/static/index.html` | Modern Python 3 | Active package; continue regression and platform validation |
| `src/subterfuge/tls.py` | Modern Python 3 | Active package; continue regression and platform validation |
| `src/subterfuge/udp_evidence.py` | Modern Python 3 | Active package; continue regression and platform validation |
| `src/subterfuge/web.py` | Modern Python 3 | Active package; continue regression and platform validation |
| `sslstrip.log` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `sslstrip.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `sslstrip/ClientRequest.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `sslstrip/ClientRequest.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `sslstrip/CookieCleaner.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `sslstrip/CookieCleaner.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `sslstrip/DnsCache.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `sslstrip/DnsCache.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `sslstrip/MAINTENANCE.md` | Documentation / packaging | Review and keep current |
| `sslstrip/SSLServerConnection.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `sslstrip/SSLServerConnection.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `sslstrip/ServerConnection.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `sslstrip/ServerConnection.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `sslstrip/ServerConnectionFactory.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `sslstrip/ServerConnectionFactory.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `sslstrip/StrippingProxy.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `sslstrip/StrippingProxy.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `sslstrip/URLMonitor.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `sslstrip/URLMonitor.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `sslstrip/__init__.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `sslstrip/__init__.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `sslstrip/clientip` | Historical / other | Preserve for review |
| `sslstrip/db` | Historical / other | Preserve for review |
| `sslstrip/sslstrip` | Historical / other | Preserve for review |
| `subterfuge.conf` | Historical / other | Preserve for review |
| `templates/._home.ext` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/._netview.ext` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/MAINTENANCE.md` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/basic.tm` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/css/._main.css` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/css/MAINTENANCE.md` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/css/domtab.css` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/css/jquery-ui.css` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/css/main.css` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/css/settings.css` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/domtab/MAINTENANCE.md` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/domtab/domtab.css` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/domtab/domtab.js` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/domtab/index.html` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/home.ext` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/._down copy 2.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/._down copy.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/._down.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/MAINTENANCE.md` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/TranspFills/MAINTENANCE.md` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/TranspFills/transpBlack10.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/TranspFills/transpBlack25.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/TranspFills/transpBlack50.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/TranspFills/transpBlack75.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/TranspFills/transpBlack90.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/TranspFills/transpBlue10.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/TranspFills/transpBlue25.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/TranspFills/transpBlue50.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/TranspFills/transpBlue75.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/TranspFills/transpBlue90.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/activity.gif` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/black_arrow.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/down copy 2.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/down copy.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/down.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/expand.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/help.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/loader.gif` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/logo.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/menu.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/netview/MAINTENANCE.md` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/netview/green.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/netview/lnx.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/netview/osx.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/netview/red.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/netview/unknown.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/netview/win.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/notify.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/panel.jpg` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/panelsmall.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/plugins/MAINTENANCE.md` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/plugins/builder.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/plugins/dos.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/plugins/evilgrade.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/plugins/harvester.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/plugins/hijacking.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/plugins/httpcodeinjection.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/plugins/injection.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/plugins/netview.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/plugins/tunnelblock.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/redbuttonbg.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/subterfugebg.jpg` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/title.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/transpBlack75.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/transpBlue50.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/images/transpBlue90.png` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/includes/._credtable.inc` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/includes/._netview.inc` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/includes/MAINTENANCE.md` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/includes/credtable.inc` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/includes/footer.inc` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/includes/header.inc` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/includes/hostcheck.inc` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/includes/nav.inc` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/includes/netview.inc` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/includes/notificationtable.inc` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/js/MAINTENANCE.md` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/js/domtab.js` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/js/jquery-ui.js` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/js/jquery.js` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/mod.ext` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/mods/MAINTENANCE.md` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/mods/builder.mod` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/mods/builder_page.mod` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/mods/builder_settings.mod` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/mods/default.mod` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/mods/default_settings.mod` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/mods/dos.mod` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/mods/dos_settings.mod` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/mods/harvester.mod` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/mods/harvester_settings.mod` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/mods/netview.mod` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/mods/netview_settings.mod` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/mods/tunnelblock.mod` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/mods/tunnelblock_settings.mod` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/netview.ext` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/notifications.ext` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/plugins.ext` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/profile.tm` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/settings.ext` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/settings.ext~` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/settings/MAINTENANCE.md` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/settings/advanced/MAINTENANCE.md` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/settings/advanced/menu.set` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/settings/vectors/MAINTENANCE.md` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/settings/vectors/arpcachepoisoning.set` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/settings/vectors/roguedhcp.set` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/settings/vectors/wirelessapgenerator.set` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/settings/vectors/wpadhijack.set` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `templates/wpad.dat` | Historical UI / asset | Reference only; replace obsolete UI or libraries as needed |
| `tests/fixtures/nmap_inventory.xml` | Regression tests | Maintain as modern code evolves |
| `tests/test_analysis.py` | Regression tests | Maintain as modern code evolves |
| `tests/test_cli.py` | Regression tests | Maintain as modern code evolves |
| `tests/test_dhcp.py` | Regression tests | Maintain as modern code evolves |
| `tests/test_environment.py` | Regression tests | Maintain as modern code evolves |
| `tests/test_name_resolution.py` | Regression tests | Maintain as modern code evolves |
| `tests/test_pcapng.py` | Regression tests | Maintain as modern code evolves |
| `tests/test_tls.py` | Regression tests | Maintain as modern code evolves |
| `tests/test_udp_evidence.py` | Regression tests | Maintain as modern code evolves |
| `tests/test_updater.py` | Regression tests | Maintain as modern code evolves |
| `tests/test_web.py` | Regression tests | Maintain as modern code evolves |
| `uninstall.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `update.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `update.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `urls.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `urls.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `utilities/MAINTENANCE.md` | Documentation / packaging | Review and keep current |
| `utilities/apgen.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `utilities/apgen.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `utilities/arpmitm.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `utilities/arpmitm.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `utilities/arpwatch.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `utilities/arpwatch.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `utilities/dev/MAINTENANCE.md` | Documentation / packaging | Review and keep current |
| `utilities/dev/build_db.sql` | Historical / other | Preserve for review |
| `utilities/dev/package.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `utilities/dev/package.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `utilities/dev/webdump` | Historical / other | Preserve for review |
| `utilities/dhcpd.conf` | Historical / other | Preserve for review |
| `utilities/dhcprace.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `utilities/dhcprace.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `utilities/dhcptools.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `utilities/dhcptools.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `utilities/errorhandler.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `utilities/errorhandler.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `utilities/nbtools.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `utilities/nbtools.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `utilities/notification.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `utilities/notification.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `utilities/rearp.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `utilities/rearp.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `utilities/scan.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `utilities/scan.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `utilities/scanindicator.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `utilities/scanindicator.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `utilities/stop.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `utilities/stop.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `utilities/subfunctions.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `utilities/subfunctions.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `utilities/subutils.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `utilities/subutils.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `utilities/wpadhijack.py` | Historical Python 2 / incompatible | Reference only; migrate purpose, not blindly translate |
| `utilities/wpadhijack.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `versioninfo.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `versioninfo.pyc` | Removed from branch | Generated or sensitive artifact; original Git history still contains it |
| `wsgi.py` | Historical Python / unported | Not imported by modern package; review before reuse |
| `xsubterfuge` | Historical / other | Preserve for review |
| `tests/test_capture_evidence.py` | New regression test | Verify, document and maintain |