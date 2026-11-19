"""Decode a tb_read.js result file into snapshots/<LATEST>/toolbox/<name>.json
usage: python3 tools/tb_save.py <tool-result-file> <name>"""
import base64, gzip, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
raw = Path(sys.argv[1]).read_text()
m = re.search(r'TBREAD\|(\d+)\|([A-Za-z0-9+/=\\]+?)\|END\|', raw)
b64 = m.group(2).replace('\\/', '/').replace('\\', '')
data = json.loads(gzip.decompress(base64.b64decode(b64)))
snap = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip() / 'toolbox'
snap.mkdir(parents=True, exist_ok=True)
out = snap / f'{sys.argv[2]}.json'
json.dump(data, open(out, 'w'), indent=1)
print(out, {k: (len(v['text']), len(v['breakdowns'])) for k, v in data['tabs'].items()})
