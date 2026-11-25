#!/usr/bin/env python3
"""One-stop lookup (Zack 2026-11-25): every game answer starts here, so nothing gets skipped.
Usage:  tools/lookup.py <system> [extra terms...]      e.g.  lookup.py tesseract arcanist
        tools/lookup.py --terms "super talent reset"     (free search, no system)
        tools/lookup.py <system> --path account.tesseract.upgrades   (drill into the data)
Prints, compactly:
  1. DATA      your numbers from Toolbox's parser on the latest save (+ save age)
  2. AUTOREVIEW items for the system (cur -> goal)
  3. CREATORS  claims, ranked Griffy > Pulse = Nocturne > others, newest first; flags pre-2024-06 as old
  4. FINDINGS  saved research files that mention it
  5. COVERAGE  "NO CREATOR COVERAGE" when no creator covers it (then: wiki/data + "my read", never invented)
Every call is logged to state/lookups.log so lookups can be audited.
"""
import csv, glob, gzip, json, re, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'model'))
from data import load, DataMissing, MAP  # noqa: E402
import yaml  # noqa: E402

IDX = yaml.safe_load(open(ROOT / 'model' / 'system_index.yaml'))
RANK = {'griffybit': 0, 'pulseidle': 1, 'nocturne': 1}
args = sys.argv[1:]
path = None
if '--path' in args:
    i = args.index('--path'); path = args[i + 1]; del args[i:i + 2]
if args and args[0] == '--terms':
    system, terms = None, args[1].lower().split()
else:
    system = args[0] if args else None
    terms = [t.lower() for t in args[1:]]
if system and system not in MAP:
    near = [s for s in MAP if system.lower() in s or s in system.lower()]
    if len(near) == 1:
        system = near[0]
    else:
        print(f"unknown system '{system}'. Close: {near or sorted(MAP)[:40]}"); sys.exit(2)

out = []
D = load()
out.append(f"# lookup: {system or ''} {' '.join(terms)}  (save {D.stamp}, {D.age_hours:.1f}h old)" if D.age_hours else f"# lookup {system}")


def compact(v, depth=0, maxk=40):
    if isinstance(v, dict):
        items = list(v.items())[:maxk]
        if depth >= 1:
            return '{' + ', '.join(f"{k}: {compact(x, depth + 1)}" for k, x in items[:12]) + (' ...' if len(v) > 12 else '') + '}'
        return '\n'.join(f"  {k}: {compact(x, depth + 1)}" for k, x in items) + (f"\n  ... {len(v) - maxk} more keys" if len(v) > maxk else '')
    if isinstance(v, list):
        if v and not isinstance(v[0], (dict, list)):
            return str(v[:12]) + (f" ...({len(v)})" if len(v) > 12 else '')
        return f"[{len(v)} items]" + (f" first: {compact(v[0], depth + 1)}" if v and depth < 2 else '')
    s = str(v)
    return s if len(s) < 120 else s[:117] + '...'


# 1. DATA
out.append('\n## 1. DATA (Toolbox parser)')
try:
    if path:
        out.append(compact(D.get(path, allow_empty=True)))
    elif system:
        v = D.system(system, allow_empty=True)
        out.append(f"path: {MAP[system].get('path')}")
        out.append(compact(v))
except DataMissing as e:
    out.append(f"DATA MISSING: {e}")

# 2. AUTOREVIEW
labels = []
if system:
    names = [n.lower() for n in IDX.get(system, {}).get('autoreview', [])]
    rv = json.load(gzip.open(ROOT / 'snapshots' / D.stamp / 'review.json.gz'))

    def walk(o, sec=''):
        if isinstance(o, dict):
            nm = str(o.get('name') or '')
            sec2 = nm if nm.lower() in names else sec
            if sec2 and o.get('label'):
                labels.append(f"  [{sec2}] {o['label'][:110]}" + (f"  ({o.get('cur')} -> {o.get('goal')})" if o.get('goal') not in (None, '') else ''))
            for x in o.values():
                walk(x, sec2)
        elif isinstance(o, list):
            for x in o:
                walk(x, sec)
    walk(rv)
out.append(f"\n## 2. AUTOREVIEW ({len(labels)} items)")
out += labels[:25] + ([f"  ... {len(labels) - 25} more"] if len(labels) > 25 else [])

# 3. CREATORS
_tr = IDX.get(system, {}).get('transcripts') if system else None; slug = (_tr.get('slug') if isinstance(_tr, dict) else None) or system
claims = []
for f in glob.glob(str(ROOT / 'sources/creators/*/tags/*.csv')):
    for r in csv.DictReader(open(f)):
        st = r.get('statement', '').lower()
        tg = (MAP.get(system, {}).get('tags') or [slug]) if system else []
        kw = MAP.get(system, {}).get('kw') or [] if system else []
        hit_sys = (r.get('system') in tg) or (kw and any(k in st for k in kw))
        hit_terms = terms and all(t in st for t in terms)
        if (hit_sys and (not terms or any(t in st for t in terms))) or (not slug and hit_terms) or (slug and hit_terms):
            claims.append(r)
seen, uniq = set(), []
for r in sorted(claims, key=lambda r: (RANK.get(r['creator'], 2), r.get('date') == 'nodate', [-ord(c) for c in r.get('date', '')])):
    k = (r['creator'], r['statement'])
    if k not in seen:
        seen.add(k); uniq.append(r)
useful = [r for r in uniq if r.get('claim_type') in ('priority', 'how_to', 'setup', 'skip', 'warning', 'target', 'comparison', 'meta_change', 'opinion', 'mechanic')]
out.append(f"\n## 3. CREATORS ({len(useful)} claims; Griffy > Pulse = Nocturne > others, newest first)")
for r in useful[:30]:
    old = ' OLD' if r.get('date', '') < '2024-06' else ''
    out.append(f"  {r['creator'][:7]} {r.get('date')}{old} {r.get('claim_type')}: {r['statement'][:170]}  [{r['video_id']} {r.get('t_start')}]")
if len(useful) > 30:
    out.append(f"  ... {len(useful) - 30} more (add terms to narrow)")

# 4. FINDINGS
keys = [k for k in [system, slug] + terms if k]
fnd = [p.name for p in (ROOT / 'sources/findings').glob('*.md') if any(k.replace('_', ' ') in p.read_text().lower() or k in p.name for k in keys)]
out.append(f"\n## 4. FINDINGS: {', '.join(fnd) or 'none'}")

# 5. COVERAGE
by = {}
for r in useful:
    by[r['creator']] = by.get(r['creator'], 0) + 1
out.append('\n## 5. COVERAGE: ' + (', '.join(f"{k} {v}" for k, v in by.items()) if by else
           'NO CREATOR COVERAGE: answer from data/wiki and label it "my read"; report the gap'))
print('\n'.join(out))

(ROOT / 'state').mkdir(exist_ok=True)
with open(ROOT / 'state' / 'lookups.log', 'a') as lg:
    lg.write(json.dumps({'t': time.strftime('%Y-%m-%dT%H:%M:%S'), 'system': system, 'terms': terms, 'path': path,
                         'save': D.stamp, 'ar_items': len(labels), 'claims': len(useful), 'by': by}) + '\n')
