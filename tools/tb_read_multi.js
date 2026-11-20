// Bulk Toolbox reader (Zack 2026-11-19 "after work" pull). Paste into javascript_tool on any idleontoolbox.com page,
// with PAGES = {name: '/account/...'} prepended (see tools/tb_pages.json). Loads pages in hidden same-origin iframes,
// N at a time, reads every tab + Details + breakdown dialogs, then gzip+base64 of {name: {url, at, tabs}}.
// Runs in the background: poll with  (window.__tbm || ('pending ' + (window.__tbm_done||0) + '/' + Object.keys(PAGES).length))
window.__tbm = null; window.__tbm_done = 0;
(async () => {
const N = 5, MAXB = 30, sleep = ms => new Promise(r => setTimeout(r, ms));
const readOne = async (name, path) => {
  const f = document.createElement('iframe');
  f.style = 'position:fixed;left:-6000px;top:0;width:1400px;height:1200px'; f.src = path; document.body.appendChild(f);
  let doc = null;
  for (let i = 0; i < 40; i++) { await sleep(750); try { doc = f.contentDocument; const m = doc && doc.querySelector('main'); if (m && m.innerText.length > 400 && !/Loading account data/.test(m.innerText)) break; } catch (e) {} }
  await sleep(1500);
  const main = () => doc.querySelector('main');
  const closeDlg = async () => { doc.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', bubbles: true})); const bd = doc.querySelector('.MuiBackdrop-root'); if (bd) bd.click(); await sleep(350); };
  const out = {url: f.contentWindow.location.href, at: new Date().toISOString(), tabs: {}};
  try {
    const seen = new Set();
    let tabs = [...main().querySelectorAll('[role=tab]')].map(t => t.innerText.trim()).filter(Boolean);
    if (!tabs.length) tabs = ['_page'];
    for (const tn of tabs) {
      if (tn !== '_page') { const t = [...main().querySelectorAll('[role=tab]')].find(x => x.innerText.trim() === tn); if (t) { t.click(); await sleep(2200); } }
      for (const b of [...main().querySelectorAll('input[type=checkbox], button, [role=button]')].filter(b => /details/i.test(b.name || '') || /^details$/i.test((b.innerText || '').trim()))) { if (!b.checked) { b.click(); await sleep(700); } }
      for (const s of [...main().querySelectorAll('button')].filter(b => /^Show \d+ more/i.test((b.innerText || '').trim()))) { s.click(); await sleep(350); }
      const rec = {text: main().innerText, breakdowns: []};
      for (const b of [...main().querySelectorAll('[role=button][aria-label]')].filter(e => /breakdown|About /i.test(e.getAttribute('aria-label')))) {
        const lab = b.getAttribute('aria-label');
        if (seen.has(lab) || rec.breakdowns.length >= MAXB) continue;
        seen.add(lab); b.click(); await sleep(800);
        rec.breakdowns.push({label: lab, text: [...doc.querySelectorAll('[role=dialog], .MuiPopover-paper')].map(x => x.innerText).join('\n--\n')});
        await closeDlg();
      }
      out.tabs[tn] = rec;
    }
  } catch (e) { out.error = String(e); }
  f.remove(); window.__tbm_done++;
  return out;
};
const names = Object.keys(PAGES), res = {};
let i = 0;
await Promise.all(Array.from({length: N}, async () => { while (i < names.length) { const n = names[i++]; res[n] = await readOne(n, PAGES[n]); } }));
const s = JSON.stringify(res);
const buf = new Uint8Array(await new Response(new Blob([s]).stream().pipeThrough(new CompressionStream('gzip'))).arrayBuffer());
let bin = ''; for (let k = 0; k < buf.length; k += 32768) bin += String.fromCharCode.apply(null, buf.subarray(k, k + 32768));
const b64 = btoa(bin);
window.__tbm = 'TBMULTI|' + b64.length + '|' + b64 + '|END|' + 'x'.repeat(60000);
})(); 'started ' + Object.keys(PAGES).length
