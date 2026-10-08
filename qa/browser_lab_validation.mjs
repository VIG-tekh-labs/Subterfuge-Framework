/** Dependency-free MV3 companion behavior regression tests. */
'use strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const extension = path.join(root, 'src/subterfuge/browser_lab');
const manifest = JSON.parse(fs.readFileSync(path.join(extension, 'manifest.json'), 'utf8'));
const content = fs.readFileSync(path.join(extension, 'content.js'), 'utf8');

assert.equal(manifest.manifest_version, 3);
assert.deepEqual(manifest.content_scripts[0].matches, ['http://127.0.0.1/*']);
assert.deepEqual(manifest.permissions, ['storage', 'activeTab']);
assert.equal(manifest.host_permissions, undefined);
assert.equal(content.includes('document.cookie'), false);
assert.equal(content.includes('chrome.cookies'), false);
assert.equal(content.includes('chrome.history'), false);

function environment({host = '127.0.0.1', dashboard = true, stored = false} = {}) {
  const elements = new Map();
  const listeners = {onChanged: [], onMessage: []};
  const body = {
    appendChild(el) {elements.set(el.id, el);},
  };
  const indicators = {
    inventory: {textContent: 'Host table'},
    'findings-count': {textContent: '3'},
    hosts: {textContent: '2'},
    source: {textContent: 'demo'},
  };
  const document = {
    title: dashboard ? 'Subterfuge · Network workspace' : 'Unrelated loopback app',
    body,
    createElement(tag) {
      const obj = {tag, id: null, style: {}, textContent: '',
        setAttribute(name, value) {this[name] = value;},
        remove() {elements.delete(this.id);}};
      return obj;
    },
    getElementById(id) {
      if (id === 'subterfuge-browser-lab-indicator') return elements.get(id) || null;
      return dashboard ? indicators[id] || null : null;
    },
  };
  const chrome = {
    runtime: {
      lastError: undefined,
      onMessage: {addListener(fn) {listeners.onMessage.push(fn);}},
    },
    storage: {
      local: {get(defaults, cb) {cb({labEnabled: stored});}},
      onChanged: {addListener(fn) {listeners.onChanged.push(fn);}},
    },
  };
  const context = vm.createContext({document,chrome,location:{hostname:host}});
  vm.runInContext(content,context,{timeout:1000});
  return {
    indicators: elements,
    listeners,
    setEnabled(value) {
      stored = value;
      for (const fn of listeners.onChanged) {
        fn({labEnabled:{newValue:value}},'local');
      }
    },
    request() {
      let response = null;
      for (const fn of listeners.onMessage) {
        fn({type:'SUBTERFUGE_LAB_INSPECT'},{},val => {response=val;});
      }
      return response;
    },
  };
}

const local = environment();
assert.equal(local.indicators.size, 0,'Default must be opt-out');
local.setEnabled(true);
assert.equal(local.indicators.size, 1,'Visible indicator must appear once the owner enables it');
const report=local.request();
assert.equal(report.valid,true);
assert.equal(report.observedHosts,'2');
assert.equal(report.reviewItems,'3');
assert.equal(report.loadedReport,true);
assert.equal(JSON.stringify(report).includes('cookie'),false);
local.setEnabled(false);
assert.equal(local.indicators.size,0,'Indicator must be removed on disable');

const restarted = environment({stored:true});
assert.equal(restarted.indicators.size,1,'Enabled lab mode should persist on reopening own dashboard');
assert.equal(restarted.request().valid,true);
assert.equal(environment({host:'example.com',stored:true}).indicators.size,0);
assert.equal(environment({dashboard:false,stored:true}).indicators.size,0);

console.log('Browser Lab MV3 QA passed: opt-in only, persistent local preference, own dashboard only, read-only diagnostics, immediate disable.');
