"""Decode a TBMULTI result file (tools/tb_read_multi.js) into snapshots/<LATEST>/toolbox/<name>.json (+ prayers.txt, worship.txt)."""
import sys, json, re, gzip, base64
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
raw = open(sys.argv[1]).read()
m = re.search(r'TBMULTI\|(\d+)\|([A-Za-z0-9+/=]+)\|END', raw)
data = json.loads(gzip.decompress(base64.b64decode(m.group(2))))
out = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip() / 'toolbox'
out.mkdir(parents=True, exist_ok=True)
bad = []
for name, rec in data.items():
    if rec.get('error') or not rec.get('tabs') or all(len(t["text"]) < 150 for t in rec['tabs'].values()): bad.append(name); continue
    if name == 'prayers': (out / 'prayers.txt').write_text('\n'.join(t['text'] for t in rec['tabs'].values()))
    elif name == 'sailing':
        tb = rec['tabs']; g = lambda k: next((v['text'] for n, v in tb.items() if k in n.lower()), '')
        if 'Boat 1\n' not in g('boats'): bad.append(name); continue
        (out / 'sail_detail.txt').write_text(g('boats') + '\n=== LOOT\n' + g('loot') + '\n=== ART tail\n' + g('artifact'))
    elif name == 'worship': (out / 'worship.txt').write_text('\n'.join(f"=== {k}\n{t['text']}" for k, t in rec['tabs'].items()))
    else: json.dump(rec, open(out / f'{name}.json', 'w'))
note = out / '_from.txt'
note.write_text(f"Fresh bulk read {list(data.values())[0]['at'][:16]}Z: {len(data) - len(bad)} pages. Not refreshed: {', '.join(bad) or 'none'}.\n")
print(f"saved {len(data) - len(bad)} pages; failed/empty: {bad}")
