"""Account priority = the biggest current need (Zack 2026-11-19). Recomputed every pull, never pinned.
Need score: AutoReview sections still behind in an EARLIER stage group than the account (they hold the account back most),
weighted by how early the group is and the tier gap, plus systems that other systems are blocked on (gates)."""
import json, gzip, re
import yaml
from tbhelp import SNAP, ROOT

STAGE_W = {'Early W6': 6, 'Mid W6': 5, 'Late W6': 4, 'Early W7': 3, 'Mid W7': 2, 'Late W7': 1}


def _groups():
    r = json.load(gzip.open(SNAP / 'review.json.gz'))
    out, seen = [], set()
    def walk(o):
        if isinstance(o, dict):
            if isinstance(o.get('name'), str) and o['name'].endswith('rated sections') and 'items' in o and o['name'] not in seen:
                seen.add(o['name']); out.append(o)
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(r); return out


def _owners():
    y = yaml.safe_load(open(ROOT / 'model' / 'system_index.yaml'))
    m = {}
    for k, v in y.items():
        if isinstance(v, dict):
            for a in v.get('autoreview') or []: m[a] = [o for o in (v.get('owners') or []) if o.startswith('Autis')]
    return m


def _t(s):
    m = re.search(r'(\d+)', s or ''); return int(m.group(1)) if m else 0


def build():
    own = _owners(); needs = []
    for g in _groups():
        stage = g['name'].replace(' rated sections', '')
        w = STAGE_W.get(stage)
        if not w: continue
        for t in g['items']:
            for i in t['items']:
                gap = _t(i['goal']) - _t(i['cur'])
                if gap > 0:
                    needs.append({'section': i['label'], 'stage': stage, 'cur': i['cur'], 'goal': i['goal'], 'score': w * 10 + gap,
                                  'why': f"still at {i['cur'].replace('T ', 'tier ')} of {i['goal'].replace('T ', '')}, a stage behind the rest of the account", 'owners': own.get(i['label'], [])})
    # gates: systems other systems wait on (Spelunking caves today)
    try:
        sp = json.load(open(ROOT / 'model' / 'spelunking.json'))
        n = len([c for c in sp.get('caves', []) if not c['done']])
        if n: needs.append({'section': 'Spelunking', 'stage': 'gate', 'cur': '', 'goal': '', 'score': 50 + n, 'owners': ['Autistomatic'],
                            'why': f"its next {n} caves unlock things other systems are waiting on (Teal Summoning, +30 meal levels, Ethereal Sigils)"})
    except Exception: pass
    needs.sort(key=lambda x: -x['score'])
    o = {'snapshot': SNAP.name, 'top': needs[0] if needs else None, 'needs': needs[:8]}
    json.dump(o, open(ROOT / 'model' / 'priority.json', 'w'), indent=1)
    return o


def line(o=None):
    o = o or json.load(open(ROOT / 'model' / 'priority.json'))
    t = o['needs'][:3]
    return 'Biggest needs right now: ' + '; '.join(f"{i + 1}. {x['section']} ({', '.join(x['owners']) or 'account'}): {x['why']}" for i, x in enumerate(t)) + '.'


if __name__ == '__main__':
    build(); print(line())
