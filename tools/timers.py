"""Parse a Toolbox /dashboard capture (browser-pane tool-result file with 'TBDASH|<iso>|<text>|END|') into
timers.json: resets, per-character AFK spot/time, and timers grouped by Toolbox's own buckets.
Usage: python tools/timers.py <tool_result_file> <out.json>"""
import sys, json, re
arr = json.load(open(sys.argv[1])); t = arr[0]['text']
t = t[t.index('TBDASH|'):]
t = json.loads('"' + t.split('|END|')[0].replace('"', '\\"') + '"') if '\\n' in t else t.split('|END|')[0]
_, captured, body = t.split('|', 2)
lines = [l.strip() for l in body.split('\n') if l.strip()]
out = {'captured_utc': captured, 'resets': {}, 'characters': [], 'timers': {}}
# characters: name, "Lv N · AFK x", spot
for i, l in enumerate(lines):
    m = re.match(r'Lv (\d+) · AFK (.+)', l)
    if m and i + 1 < len(lines):
        out['characters'].append({'name': lines[i - 1], 'level': int(m.group(1)), 'afk_for': m.group(2), 'spot': lines[i + 1]})
for key in ('Daily', 'Weekly', 'Server weekly', 'Vote›', 'Meritocracy›'):
    if key in lines:
        out['resets'][key.rstrip('›')] = lines[lines.index(key) + 1]
BUCKETS = ['READY NOW', 'NEXT 24 HOURS', 'THIS WEEK', 'LATER']
for bi, b in enumerate(BUCKETS):
    if b not in lines: continue
    start = lines.index(b) + 1
    end = min([lines.index(x) for x in BUCKETS[bi + 1:] if x in lines] + [len(lines)])
    seg = [l for l in lines[start:end] if l not in ('●', 'Show fewer') and not re.match(r'^\d+ to act on$|^Show \d+ more$', l)]
    items, cur = [], None
    for l in seg:
        if l.endswith('›'):
            cur = {'name': l.rstrip('›'), 'info': []}; items.append(cur)
        elif cur is not None and l not in ('Discord', '·', 'Discord bot', 'Buy me a coffee', 'Cookie Policy', 'Theme'):
            cur['info'].append(l)
    out['timers'][b] = [{'name': x['name'], 'value': ' · '.join(x['info'][:3])} for x in items]
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print(len(out['characters']), 'chars,', {k: len(v) for k, v in out['timers'].items()}, out['resets'])
