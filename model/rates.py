"""Item income rates from two game saves: storage + inventories now vs an earlier snapshot (>= 3h apart).
rate(name) -> per hour (can be negative = net consumption). Used to say how fast a spend is replaced.
"""
import gzip, json, os
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SN = ROOT / 'snapshots'


def _load(stamp):
    d = json.load(gzip.open(SN / stamp / 'raw.json.gz')); d = d.get('data', d)
    g = lambda k: json.loads(d[k]) if isinstance(d.get(k), str) else d.get(k)
    c = {}
    for code, q in zip(g('ChestOrder') or [], g('ChestQuantity') or []): c[code] = c.get(code, 0) + float(q or 0)
    for i in range(12):
        for code, q in zip(g(f'InventoryOrder_{i}') or [], g(f'ItemQTY_{i}') or []): c[code] = c.get(code, 0) + float(q or 0)
    t = float(d['TimeAway']['GlobalTime'] if isinstance(d.get('TimeAway'), dict) else json.loads(d['TimeAway'])['GlobalTime'])
    return c, t


@lru_cache(None)
def table():
    stamps = sorted(p for p in os.listdir(SN) if (SN / p / 'raw.json.gz').exists())
    latest = (SN / 'LATEST').read_text().strip()
    now, tn = _load(latest)
    prev = None
    for s in reversed(stamps):
        if s >= latest: continue
        c, t = _load(s)
        if tn - t >= 3 * 3600: prev = (c, t, s); break
    if not prev: return {}, now, None
    c, t, s = prev
    hrs = (tn - t) / 3600
    return {k: (now.get(k, 0) - c.get(k, 0)) / hrs for k in set(now) | set(c)}, now, {'from': s, 'hours': round(hrs, 1)}


def code_of(name):
    try:
        from consts.generated.raw_item_data import raw_item_data as RD
    except Exception:
        return None
    return next((k for k, v in RD.items() if isinstance(v, dict) and v.get('Name', '').lower() == name.lower()), None)


def info(name):
    r, now, meta = table()
    code = code_of(name)
    if not code: return None
    return {'item': name, 'owned': now.get(code, 0), 'rate_hr': r.get(code), 'window': meta}


def replace_line(name, spend):
    i = info(name)
    if not i or i['rate_hr'] is None: return f"{name}: income rate unknown (need two saves 3h+ apart)"
    if i['rate_hr'] <= 0: return f"{name}: spending {spend:,.3g} is NOT replaced right now (net {i['rate_hr']:,.3g}/hr over {i['window']['hours']}h)"
    return f"{name}: spending {spend:,.3g} comes back in {spend / i['rate_hr']:.1f}h at +{i['rate_hr']:,.3g}/hr (measured over {i['window']['hours']}h)"
