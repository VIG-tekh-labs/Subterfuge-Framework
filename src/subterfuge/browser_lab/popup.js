'use strict';
// Persistent preference, not a persistent off-site hook. The content script is
// recreated by Chromium only on the local 127.0.0.1 Subterfuge dashboard.
const enabled = document.getElementById('enabled');
const result = document.getElementById('result');
const inspect = document.getElementById('inspect');

function show(message) {
  result.textContent = String(message);
}
function localDashboardUrl(url) {
  try {
    const value = new URL(url);
    return value.protocol === 'http:' && value.hostname === '127.0.0.1';
  } catch (_) {
    return false;
  }
}
async function inspectCurrentTab() {
  const preferences = await chrome.storage.local.get({labEnabled: false});
  if (!preferences.labEnabled) {
    show('Lab mode is off. Enable it to inspect your own dashboard.');
    return;
  }
  const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
  if (!tab || !localDashboardUrl(tab.url || '')) {
    show('Open your own local Subterfuge dashboard at http://127.0.0.1:8080.');
    return;
  }
  try {
    const state = await chrome.tabs.sendMessage(tab.id, {type: 'SUBTERFUGE_LAB_INSPECT'});
    if (!state || !state.valid) {
      show('This page is not a recognized Subterfuge dashboard.');
      return;
    }
    show(
      'Dashboard: recognized\n' +
      'Lab mode: enabled\n' +
      'Observed hosts: ' + state.observedHosts + '\n' +
      'Review items: ' + state.reviewItems + '\n' +
      'Loaded report: ' + (state.loadedReport ? 'yes' : 'no')
    );
  } catch (_) {
    show('No local dashboard is responding. Reload the dashboard and retry.');
  }
}
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const value = await chrome.storage.local.get({labEnabled: false});
    enabled.checked = value.labEnabled === true;
    show(enabled.checked ? 'Local lab mode is ready.' : 'Lab mode is off.');
  } catch (_) {
    show('Local browser storage is unavailable.');
  }
});
enabled.addEventListener('change', async () => {
  try {
    await chrome.storage.local.set({labEnabled: enabled.checked === true});
    show(enabled.checked ? 'Lab mode enabled for your local workspace.' :
      'Lab mode disabled. The local indicator will disappear.');
  } catch (_) {
    enabled.checked = false;
    show('Unable to save the lab preference.');
  }
});
inspect.addEventListener('click', inspectCurrentTab);
