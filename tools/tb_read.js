// Toolbox page reader (paste into javascript_tool on any idleontoolbox.com account page).
// Reads every tab's text + every breakdown dialog, returns gzip+base64 (decode with tools/tb_save.py).
// MAXB = max breakdown dialogs per tab (identical label+value pairs are read once).
const MAXB = 60, sleep = ms => new Promise(r => setTimeout(r, ms));
await sleep(5000);
const main = () => document.querySelector('main');
const closeDlg = async () => { document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', bubbles: true})); const bd = document.querySelector('.MuiBackdrop-root'); if (bd) bd.click(); await sleep(400); };
const out = {url: location.href, at: new Date().toISOString(), tabs: {}};
let tabs = [...main().querySelectorAll('[role=tab]')].map(t => t.innerText.trim()).filter(Boolean);
if (!tabs.length) tabs = ['_page'];
for (const name of tabs) {
  if (name !== '_page') { const t = [...main().querySelectorAll('[role=tab]')].find(x => x.innerText.trim() === name); if (t) { t.click(); await sleep(2500); } }
  for (const b of [...main().querySelectorAll('input[type=checkbox], button, [role=button]')].filter(b => /details/i.test(b.name || '') || /^details$/i.test((b.innerText || '').trim()))) { if (!b.checked) { b.click(); await sleep(800); } }
  for (const s of [...main().querySelectorAll('button')].filter(b => /^Show \d+ more/i.test((b.innerText || '').trim()))) { s.click(); await sleep(400); }
  const rec = {text: main().innerText, breakdowns: []};
  const seen = new Set();
  const btns = [...main().querySelectorAll('[role=button][aria-label]')].filter(e => /breakdown|About /i.test(e.getAttribute('aria-label')));
  for (const b of btns) {
    const lab = b.getAttribute('aria-label');
    if (seen.has(lab) || rec.breakdowns.length >= MAXB) continue;
    seen.add(lab);
    b.scrollIntoView({block: 'center'}); b.click(); await sleep(900);
    const d = [...document.querySelectorAll('[role=dialog], .MuiPopover-paper')].map(x => x.innerText).join('\n--\n');
    rec.breakdowns.push({label: lab, text: d});
    await closeDlg();
  }
  out.tabs[name] = rec;
}
const s = JSON.stringify(out);
const cs = new Blob([s]).stream().pipeThrough(new CompressionStream('gzip'));
const buf = new Uint8Array(await new Response(cs).arrayBuffer());
let bin = ''; for (let i = 0; i < buf.length; i += 32768) bin += String.fromCharCode.apply(null, buf.subarray(i, i + 32768));
const b64 = btoa(bin);
'TBREAD|' + b64.length + '|' + b64 + '|END|' + 'x'.repeat(60000)
