'use strict';
// Declarative injection limited to 127.0.0.1. Never read cookies, passwords,
// input values, page scripts, browsing history or user-entered page content.
(() => {
  if (location.hostname !== '127.0.0.1') return;
  function isSubterfugeDashboard() {
    return document.title === 'Subterfuge · Network workspace' &&
      !!document.getElementById('inventory') &&
      !!document.getElementById('findings-count') &&
      !!document.getElementById('hosts');
  }
  if (!isSubterfugeDashboard()) return;
  const indicatorId = 'subterfuge-browser-lab-indicator';
  function removeIndicator() {
    document.getElementById(indicatorId)?.remove();
  }
  function showIndicator() {
    if (document.getElementById(indicatorId)) return;
    const indicator = document.createElement('div');
    indicator.id = indicatorId;
    indicator.setAttribute('role', 'status');
    indicator.textContent = 'Subterfuge Browser Lab · ON';
    Object.assign(indicator.style, {
      position: 'fixed', right: '10px', bottom: '10px', zIndex: '2147483640',
      background: '#172d2a', color: '#fff', border: '2px solid #5fe2b3',
      padding: '8px 12px', borderRadius: '8px', fontFamily: 'system-ui,sans-serif',
      fontSize: '12px', pointerEvents: 'none'
    });
    document.body.appendChild(indicator);
  }
  function setMode(active) {
    if (active === true) showIndicator();
    else removeIndicator();
  }
  chrome.storage.local.get({labEnabled: false}, (value) => {
    setMode(chrome.runtime.lastError ? false : value.labEnabled);
  });
  chrome.storage.onChanged.addListener((changes, area) => {
    if (area === 'local' && changes.labEnabled) {
      setMode(changes.labEnabled.newValue === true);
    }
  });
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (!message || message.type !== 'SUBTERFUGE_LAB_INSPECT') return;
    chrome.storage.local.get({labEnabled: false}, (value) => {
      const allowed = value.labEnabled === true && isSubterfugeDashboard();
      sendResponse({
        valid: allowed,
        observedHosts: allowed ? document.getElementById('hosts')?.textContent.trim() || '—' : null,
        reviewItems: allowed ? document.getElementById('findings-count')?.textContent.trim() || '—' : null,
        loadedReport: allowed ? Boolean(
          document.getElementById('source')?.textContent.trim() &&
          document.getElementById('source').textContent.trim() !== 'No report loaded'
        ) : false
      });
    });
    return true;
  });
})();
