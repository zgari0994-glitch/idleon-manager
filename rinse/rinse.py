"""Griffy rinse = the Thigh Gap formula from the ChatGPT build (v2, the one Zack picked in the blind test).

Score = round(100 x GapFactor x ActionabilityFactor x GriffyFactor)
  GapFactor            1.0 required; 0.5 if optional at item, group or section level
  ActionabilityFactor  1.25 if current AND goal present and neither is a tier-only label (T1, T2...)
                       0.65 if current or goal is a tier-only label
                       0.80 otherwise
  GriffyFactor         1 + 0.2 x (Griffy KB videos covering the topic) / (total videos)
Completed and informational rows excluded. Sort: score desc, then section, then label.
Known limits (same as the original): no gap size, no affordability, no effort, no dependencies.
Adjustments go in ADJUST below, each with a reason, only on Zack's approval.

Usage: python rinse/rinse.py [top N]  -> rinse/latest.json (all scored rows) + prints top N."""
import json, gzip, os, re, sys, yaml
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
stamp = open(os.path.join(R, 'snapshots', 'LATEST')).read().strip()
review = json.load(gzip.open(os.path.join(R, 'snapshots', stamp, 'review.json.gz')))
# 2026-11-19: creator push from ALL tagged videos (Griffy 3x, Pulse/Nocturne 2x, recency + stage weighted),
# replacing the old 101-video griffy_topics.yaml counts. Same factor shape: 1 + 0.2 x push (normalized, capped at 1).
sys.path.insert(0, os.path.join(R, 'model'))
import guidance as GD
PUSH = GD.push_weight()
SI = yaml.safe_load(open(os.path.join(R, 'model', 'system_index.yaml')))
SEC_PUSH = {}
for k, v in SI.items():
    slug = v.get('transcripts', {}).get('slug') if isinstance(v.get('transcripts'), dict) else None
    for sec in v.get('autoreview', []) or []:
        SEC_PUSH[sec] = max(SEC_PUSH.get(sec, 0), PUSH.get(slug, 0))
P90 = sorted(SEC_PUSH.values())[int(len(SEC_PUSH) * 0.9)] or 1
ADJUST = {}  # e.g. {'section': multiplier}  (none yet)
TIER = re.compile(r'^\s*(T\s*\d+|Tier\s*\d+|\d+\s*/\s*\d+)\s*$', re.I)
SKIP = {'Pinchy high', 'Pinchy low', 'Pinchy all'}

def griffy(section):
    return 1 + 0.2 * min(1.0, SEC_PUSH.get(section, 0) / P90)

def actionability(cur, goal):
    if (cur and TIER.match(cur)) or (goal and TIER.match(goal)):
        return 0.65
    sym = re.compile(r'^[\W_]+$')  # ❌ / ✔ style flags are not concrete numbers
    if cur and goal and not sym.match(cur) and not sym.match(goal):
        return 1.25
    return 0.8

def leaves(g, gname, opt):
    if 'tabs' in g:
        for t in g['tabs']:
            yield from leaves(t, t.get('tab') or gname, opt or t.get('optional'))
        return
    for a in g.get('items', []):
        if 'items' in a:
            for b in a['items']:
                yield gname, b, opt
        else:
            yield gname, a, opt

rows = []
for w in review['worlds']:
    for s in w['sections']:
        if s['name'] in SKIP or s.get('completed') or s.get('informational'):
            continue
        for g in s['groups']:
            if g.get('completed') or g.get('informational'):
                continue
            for gname, a, gopt in leaves(g, g.get('name', ''), g.get('optional')):
                if a.get('completed') or a.get('informational') or not (a['cur'] or a['goal']):
                    continue
                optional = bool(a.get('optional') or gopt or s.get('optional'))
                gap = 0.5 if optional else 1.0
                act = actionability(a['cur'], a['goal'])
                gf = griffy(s['name'])
                score = round(100 * gap * act * gf * ADJUST.get(s['name'], 1))
                rows.append({'_i': len(rows), 'score': score, 'section': s['name'], 'world': w['world'], 'group': gname[:90],
                             'label': a['label'][:140], 'cur': a['cur'], 'goal': a['goal'],
                             'factors': {'gap': gap, 'act': act, 'griffy': round(gf, 3)}})
rows.sort(key=lambda r: (-r['score'], r['section'], r['label']))
# next step only: keep the first (nearest) goal per section+label, in AutoReview's own order
seen, nxt = set(), []
for r in sorted(rows, key=lambda r: r.get('_i', 0)):
    k = (r['section'], r['label'])
    if k not in seen:
        seen.add(k); nxt.append(r)
rows = sorted(nxt, key=lambda r: (-r['score'], r['section'], r['label']))
by_section = []
for r in rows:
    if r['section'] not in {x['section'] for x in by_section}:
        by_section.append(r)
json.dump({'meta': review['meta'], 'formula': 'Thigh Gap v2 (creator push from all tags)', 'by_section': by_section, 'rows': rows},
          open(os.path.join(R, 'rinse', 'latest.json'), 'w'), indent=1)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 15
print(len(rows), 'scored rows')
print('-- top section gaps --')
for r in by_section[:N]:
    print(r['score'], '|', r['section'], '|', r['label'][:70], ':', r['cur'], '->', r['goal'])
