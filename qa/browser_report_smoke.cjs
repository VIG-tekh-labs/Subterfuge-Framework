/* Optional isolated Chromium UI smoke test. Run with Puppeteer installed externally. */
'use strict';
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {spawn} = require('node:child_process');

async function main() {
  let puppeteer;
  try {
    puppeteer = require('puppeteer');
  } catch {
    console.error('Puppeteer is needed for optional UI QA; install it outside the runtime package.');
    process.exitCode = 2;
    return;
  }
  const root = path.resolve(__dirname, '..');
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'subterfuge-dashboard-'));
  const python = process.env.SUBTERFUGE_PYTHON || 'python3';
  const server = spawn(python, ['-m', 'subterfuge', 'serve', '--port', '0'], {
    cwd: root, env: {...process.env, PYTHONPATH: path.join(root, 'src')},
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  let browser;
  try {
    let errors = [];
    const url = await new Promise((resolve, reject) => {
      let output = '';
      const timeout = setTimeout(() => reject(new Error('Dashboard startup timed out')), 10000);
      server.stdout.on('data', chunk => {
        output += chunk.toString();
        const match = output.match(/Subterfuge dashboard: (http:\/\/127\.0\.0\.1:\d+\/)/);
        if (match) {clearTimeout(timeout); resolve(match[1]);}
      });
      server.on('error', err => {clearTimeout(timeout); reject(err);});
      server.on('exit', (code) => {clearTimeout(timeout); reject(new Error('Server exited: '+code));});
    });
    browser = await puppeteer.launch({
      executablePath: process.env.CHROMIUM_PATH || '/usr/bin/chromium',
      headless: true,
      args: ['--disable-dev-shm-usage'],
    });
    const page = await browser.newPage();
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(url, {waitUntil: 'domcontentloaded'});
    const report = {
      schema_version: 1, kind: 'pcapng', source: 'qa-untimed.pcapng',
      stats: {arp_packets: 1, packets: 1, findings: 0},
      hosts: [{
        address: '192.0.2.10', mac_addresses: ['02:00:00:00:00:01'],
        observations: 1, first_seen: null, last_seen: null,
      }],
      findings: [], warnings: ['Simple PCAPNG packet timestamps are unknown.'],
      network_evidence: [],
    };
    const goodPath = path.join(temp, 'valid-report.json');
    fs.writeFileSync(goodPath, JSON.stringify(report), 'utf8');
    const input = await page.$('#report-file');
    await input.uploadFile(goodPath);
    await page.click('#load-report');
    await page.waitForFunction(() => document.querySelector('#status').textContent.includes('Saved report opened locally.'));
    const hosts = await page.$eval('#hosts', node => node.textContent);
    if (hosts !== '1') throw new Error('Expected one imported host, got ' + hosts);
    const tableLabel = await page.$eval('#inventory', node => node.getAttribute('aria-label'));
    if (tableLabel !== 'Observed host inventory') throw new Error('Host inventory lacks an accessible name');
    const warningRole = await page.$eval('#warnings [role="listitem"]', node => node.getAttribute('role'));
    if (warningRole !== 'listitem') throw new Error('Warnings lack accessible list semantics');
    const warnings = await page.$eval('#warnings', node => node.textContent);
    if (!warnings.includes('timestamps are unknown')) throw new Error('Missing timestamp warning');

    const bad = structuredClone(report);
    bad.hosts[0].mac_addresses = [{value: 'not an address'}];
    const badPath = path.join(temp, 'invalid-report.json');
    fs.writeFileSync(badPath, JSON.stringify(bad), 'utf8');
    await input.uploadFile(badPath);
    await page.click('#load-report');
    await page.waitForFunction(() => document.querySelector('#status').textContent.includes('Invalid host structure in saved report.'));
    const retained = await page.$eval('#hosts', node => node.textContent);
    if (retained !== '1') throw new Error('Invalid import replaced the valid report');
    if (errors.length) throw new Error('Browser errors: ' + errors.join('; '));
    console.log('Chromium UI QA: valid untimed PCAPNG JSON reopened; malformed JSON structure rejected; valid report retained; zero uncaught page errors.');
  } finally {
    if (browser) await browser.close();
    server.kill('SIGTERM');
    fs.rmSync(temp, {recursive: true, force: true});
  }
}

main().catch(error => {console.error(error.stack || error); process.exitCode = 1;});