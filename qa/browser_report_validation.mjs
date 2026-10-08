/* Standalone browser-import validation tests; no npm dependencies. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const html = fs.readFileSync(path.join(root, 'src/subterfuge/static/index.html'), 'utf8');
const match = html.match(/<script nonce="__TOKEN__">([\s\S]*?)<\/script>/);
if (!match) throw Error('Unable to find inline dashboard script');

const controls = new Map();
const fakeElement = () => ({
  addEventListener() {}, replaceChildren() {}, append() {},
  classList: { toggle() {} }, textContent: '', disabled: false, value: '',
});
const document = {
  getElementById(id) {
    if (!controls.has(id)) controls.set(id, fakeElement());
    return controls.get(id);
  },
  createElement: fakeElement,
};
const context = vm.createContext({
  document,
  fetch: () => new Promise(() => {}),
});
vm.runInContext(match[1], context, { timeout: 1500 });

const check = value => {
  context.input = value;
  return vm.runInContext('validateImportedReport(input)', context, { timeout: 500 });
};
const clone = value => JSON.parse(JSON.stringify(value));
const valid = {
  schema_version: 1, kind: 'pcapng', source: 'local.pcapng',
  stats: { arp_packets: 1, packets: 1, findings: 0 },
  hosts: [{
    address: '192.0.2.1', mac_addresses: ['02:00:00:00:00:01'],
    observations: 1, first_seen: null, last_seen: null,
  }],
  findings: [], warnings: ['Simple packet timestamps are unknown'],
  network_evidence: [],
};

check(valid);
const python = process.env.SUBTERFUGE_PYTHON || 'python';
function cliReport(args) {
  const result = spawnSync(python, ['-m', 'subterfuge', ...args], {
    cwd: root,
    env: {...process.env, PYTHONPATH: path.join(root, 'src')},
    encoding: 'utf8',
    timeout: 10000,
  });
  if (result.status !== 0) {
    throw Error('Failed to build genuine report fixture: ' + (result.stderr || String(result.error)));
  }
  return JSON.parse(result.stdout);
}
check(cliReport(['demo']));
check(cliReport(['import-nmap', path.join('tests', 'fixtures', 'nmap_inventory.xml')]));
const inventory = clone(valid);
inventory.kind = 'nmap';
inventory.hosts = [{
  addresses: ['192.0.2.1'], mac_addresses: [],
  ports: [{ port: 443, protocol: 'tcp', service: 'https', state: 'open' }],
  status: 'up',
}];
check(inventory);
const passive = clone(valid);
passive.network_evidence = [{
  protocol: 'dhcp', message_type: 'offer',
  server_identifier: null, wpad_option_present: false, observations: 1,
}];
check(passive);

const invalid = [];
let item = clone(inventory); item.hosts[0].ports = [null]; invalid.push(item);
item = clone(inventory); item.hosts[0].ports = [{ port: 70000, protocol: 'tcp' }]; invalid.push(item);
item = clone(valid); item.hosts[0].mac_addresses = [{ value: 'invalid' }]; invalid.push(item);
item = clone(valid); item.hosts[0].first_seen = 'unknown'; invalid.push(item);
item = clone(valid); item.findings = [{ message: { text: 'nested object' } }]; invalid.push(item);
item = clone(valid); item.warnings = [{ value: 'unexpected' }]; invalid.push(item);
item = clone(valid); item.network_evidence = [{ protocol: 'dhcp', observations: 'many' }]; invalid.push(item);
item = clone(valid); item.stats.arp_packets = 'infinite'; invalid.push(item);
item = clone(valid); item.hosts[0].addresses = 'not an array'; invalid.push(item);
item = clone(valid); item.kind = 'x'.repeat(128); invalid.push(item);

for (const [index, bad] of invalid.entries()) {
  let rejected = false;
  try {
    check(bad);
  } catch (error) {
    if (!String(error.message).includes('Invalid')) throw error;
    rejected = true;
  }
  if (!rejected) throw Error('Malformed saved report accepted: case ' + (index + 1));
}
console.log('Dashboard JSON validator: 5 valid fixtures accepted (including 2 genuine CLI reports); ' + invalid.length + ' malformed fixtures rejected.');