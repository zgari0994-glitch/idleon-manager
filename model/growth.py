"""Growth tracking (pending_changes 'Growth tracking', built 2026-11-27).
Counters per save from Toolbox's parser, cached in state/growth.json. Rates per day from saves over the last
~3 days give ETAs; the weekly review compares the newest save with the one closest to 7 days back.
Also diffs talent levels between the last two saves (plans/talents_<save>.json).
Use: growth.eta(key, cur, goal) -> ', +x/day, ETA n d' ; python3 model/growth.py -> plans/growth_<save>.md"""
import json, sys, gzip
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import data

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / 'state' / 'growth.json'
SNAPS = sorted(p.name for p in (ROOT / 'snapshots').glob('2026*') if (p / 'tb_parsed.json.gz').exists())


def ts(stamp): return datetime.strptime(stamp, '%Y%m%dT%H%M').replace(tzinfo=timezone.utc)


def _s(d, name):
    try: return d.system(name, allow_empty=True)
    except Exception: return None


COUNTERS = {  # key: (label, goal or None, fn(d))
    'achievements': ('Achievements done', 420, lambda d: sum(1 for x in _s(d, 'achievements') if x.get('completed'))),
    'slab': ('Slab items looted', 1938, lambda d: _s(d, 'slab')['lootedItems']),
    'vials_maxed': ('Vials maxed', 87, lambda d: sum(1 for x in _s(d, 'alchemy_cauldrons')['vials'] if (x.get('level') or 0) >= 13)),
    'opals': ('Hole opals found', None, lambda d: _s(d, 'caverns')['totalOpalsFound']),
    'villager_levels': ('Hole villager levels', None, lambda d: _s(d, 'caverns')['totalVillagersLevels']),
    'observations': ('Observations found', 43, lambda d: sum(1 for o in _s(d, 'research')['observations'] if o.get('found'))),
    'capes': ('Capes', 23, lambda d: _s(d, 'cape_vine')['totalCapes']),
    'jewels': ('Lab jewels', 24, lambda d: sum(1 for j in _s(d, 'lab_mainframe')['jewels'] if j.get('acquired'))),
    'refinery_ranks': ('Refinery total ranks', None, lambda d: _s(d, 'refinery')['totalLevels']),
    'menagerie_rank': ('Menagerie rank', None, lambda d: _s(d, 'menagerie')['rank']),
    'lumi': ('Lumi', None, lambda d: round(_s(d, 'menagerie')['lumi'])),
    'equinox_levels': ('Equinox upgrade levels', None, lambda d: _s(d, 'equinox')['totalUpgradeLevels']),
    'worship_waves': ('Worship totem waves (sum)', 1100, lambda d: sum(t.get('maxWave') or 0 for t in _s(d, 'worship'))),
    'dungeon_rank': ('Dungeon rank', None, lambda d: _s(d, 'dungeons')['rank']),
}


def table():
    c = json.load(open(CACHE)) if CACHE.exists() else {}
    changed = False
    for s in SNAPS:
        if s in c and set(c[s]) >= set(COUNTERS): continue
        try: d = data.load(s)
        except Exception: continue
        row = c.get(s, {})
        for k, (_, _, fn) in COUNTERS.items():
            if k in row: continue
            try: row[k] = fn(d)
            except Exception: row[k] = None
        c[s] = row; changed = True
    if changed:
        CACHE.parent.mkdir(exist_ok=True); json.dump(c, open(CACHE, 'w'), indent=0, sort_keys=True)
    return c


_T = None
def _tab():
    global _T
    if _T is None: _T = table()
    return _T


def rate(key, days=3.0):
    """per-day rate from the newest save vs the oldest save within `days` (needs 12+ h of span)."""
    t = _tab(); ss = [s for s in sorted(t) if t[s].get(key) is not None]
    if len(ss) < 2: return None
    new = ss[-1]; old = next((s for s in ss if (ts(new) - ts(s)).total_seconds() <= days * 86400), None)
    if not old or old == new: old = ss[-2]
    span = (ts(new) - ts(old)).total_seconds() / 86400
    if span < 0.5: return None
    return (t[new][key] - t[old][key]) / span


def eta(key, cur, goal):
    r = rate(key)
    if r is None: return ''
    gap = goal - cur
    if gap <= 0: return ', done'
    if r == 0 or (gap > 0) != (r > 0): return f", {r:+.2f}/day: not moving (bottleneck)"
    return f", {r:+.2f}/day, ETA {gap / r:.0f} d" + (' (long: bottleneck)' if gap / r > 60 else '')


def weekly():
    t = _tab(); ss = sorted(t)
    if len(ss) < 2: return []
    new = ss[-1]
    old = min(ss[:-1], key=lambda s: abs((ts(new) - ts(s)).total_seconds() - 7 * 86400))
    days = (ts(new) - ts(old)).total_seconds() / 86400
    out = [f"Weekly review: save {new} vs {old} ({days:.1f} days)"]
    moved, still = [], []
    for k, (lab, goal, _) in COUNTERS.items():
        a, b = t[old].get(k), t[new].get(k)
        if a is None or b is None: continue
        (moved if a != b else still).append(f"{lab}: {a} -> {b} ({b - a:+,})" + (f", goal {goal}{eta(k, b, goal)}" if goal is not None else ''))
    return out + ['Moved:'] + [f"- {x}" for x in moved] + ['Not moving:'] + [f"- {x}" for x in still]


def _talents(stamp):
    p = ROOT / 'plans' / f'talents_{stamp}.json'
    if not p.exists(): return {}
    r = json.load(open(p)).get('ranked') or []
    out = {}
    for x in r if isinstance(r, list) else []:
        if not isinstance(x, dict): continue
        who = x.get('char') or x.get('character') or x.get('owner') or ''
        tal = x.get('name') or x.get('talent') or ''
        lv = x.get('level', x.get('lv'))
        if tal: out[(who, tal)] = lv
    return out


def talent_diffs():
    ps = sorted(p.stem[8:] for p in (ROOT / 'plans').glob('talents_2026*.json'))
    if len(ps) < 2: return []
    a, b = _talents(ps[-2]), _talents(ps[-1])
    ch = [f"{w + ': ' if w else ''}{t} {a[(w, t)]} -> {b[(w, t)]}" for (w, t) in b if (w, t) in a and a[(w, t)] != b[(w, t)]]
    return [f"Talent changes {ps[-2]} -> {ps[-1]}: {len(ch)}"] + [f"- {x}" for x in ch[:40]]


if __name__ == '__main__':
    t = _tab(); new = sorted(t)[-1]
    L = [f"# Growth · save {new}", '', '## Rates + ETAs (last ~3 days)']
    for k, (lab, goal, _) in COUNTERS.items():
        cur = t[new].get(k); r = rate(k)
        if cur is None: continue
        L.append(f"- {lab}: {cur:,}" + (f" ({r:+.2f}/day)" if r is not None else ' (rate n/a)') + (f", goal {goal}{eta(k, cur, goal)}" if goal is not None else ''))
    L += ['', '## ' + (weekly() or ['Weekly review: needs 2+ saves'])[0]] + weekly()[1:]
    L += ['', '## Talents'] + (talent_diffs() or ['- no talent files to diff'])
    (ROOT / 'plans' / f'growth_{new}.md').write_text('\n'.join(L) + '\n')
    print('\n'.join(L))
