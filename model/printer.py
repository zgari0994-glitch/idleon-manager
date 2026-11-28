"""3D Printer planner: each character's print slots vs material needs, Gold Relic reset rule, AutoReview sample targets
-> each print owner's prints block (jobs.yaml Fish/Bug/Ore/Log prints) + account lines.

Inputs: raw save Print (5 samples + 2 printing per character), systems printer, model/ledger.json (needs), data.py (Toolbox parser).
"""
import gzip, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip()


def _name(code):
    try:
        from utils.text_formatting import getItemDisplayName
        return getItemDisplayName(code)
    except Exception:
        return code


def build():
    r = json.load(gzip.open(SNAP / 'raw.json.gz')); d = r.get('data', r)
    p = d['Print']; p = json.loads(p) if isinstance(p, str) else p
    raw = p[5:]
    chars = [c['character_name'] for c in json.load(open(SNAP / 'chars.json'))['characters']]
    pr = json.load(gzip.open(SNAP / 'systems.json.gz'))['systems']['printer']
    per = {}
    for i, c in enumerate(chars):
        blk = raw[i * 14:(i + 1) * 14]
        pairs = [(blk[j], float(blk[j + 1] or 0)) for j in range(0, len(blk) - 1, 2)]
        per[c] = {'samples': [(_name(k), v) for k, v in pairs[:5] if k and k != 'Blank'],
                  'printing': [(_name(k), v) for k, v in pairs[5:7] if k and k != 'Blank']}
    need = {}
    try:
        L = json.load(open(ROOT / 'model' / 'ledger.json'))
        for x in L.get('runout', []): need[x['item']] = f"runs out in {x['runout_days']:.1f} days"
        for x in L.get('watch', []): need.setdefault(x['item'], x['why'][:70])
        for s in L.get('stamps', []):
            if s.get('next_raise') and s.get('owned') is not None and s['owned'] < s['next_raise']:   # only the NEXT raise counts as a need
                need.setdefault(s['material'], f"{s['stamp']} next max raise needs {s['next_raise']:.3g} (have {s['owned']:.3g})")
    except Exception:
        pass
    # never swap away from AutoReview sample-target items (Oak, Copper, Goldfish, Fly, Spore Cap): Griffy prints for refinery/salts too
    PROTECT = {'Oak Logs', 'Copper Ore', 'Goldfish', 'Fly', 'Spore Cap'}
    swaps = []
    for c, x in per.items():
        printed = {n for n, _ in x['printing']}
        for n, v in x['printing']:
            if n in need or n in PROTECT: continue
            alt = [(sn, sv) for sn, sv in x['samples'] if sn in need and sn not in printed]
            if alt:
                sn, sv = max(alt, key=lambda t: t[1])
                swaps.append({'char': c, 'from': n, 'to': sn, 'sample': sv, 'why': need[sn]}); printed.add(sn)
    tb = {}   # Zack 2026-11-25: atoms-per-hour / threshold were page-only reads; the Atom planner covers particles now
    # print buffs from AutoReview Sampling sources, closest to done first (Zack: push the close ones before print day)
    close = []
    try:
        rv = json.load(gzip.open(SNAP / 'review.json.gz'))
        for w in rv['worlds']:
            for sec in (w.get('sections') or []):
                if sec.get('name') != 'Sampling': continue
                for g in sec['groups']:
                    if not g['name'].startswith('Sources'): continue
                    for it in g['items']:
                        for x in it.get('items', []):
                            if x.get('completed') or x['label'].startswith(('Autis', 'Prayer')): continue
                            c = re.findall(r'[\d.]+', str(x['cur'])); gl = re.findall(r'[\d.]+', str(x['goal']))
                            if c and gl and float(gl[0]) > 0:
                                f = float(c[0]) / float(gl[0])
                                if f < 1: close.append({'label': x['label'][:90], 'cur': x['cur'], 'goal': x['goal'], 'frac': round(f, 2)})
        close.sort(key=lambda x: -x['frac'])
    except Exception:
        pass
    out = {'snapshot': SNAP.name, 'per_char': per, 'close_buffs': close, 'needs': need, 'swaps': swaps, 'gold_relic': (pr.get('gold_relic_days'), pr.get('gold_relic_max_days'), pr.get('gold_relic_multi')),
           'x1': {'Supreme Wiring (event shop)': (pr.get('supreme_wiring_days'), 50), 'Yet Another Printer Multi (legend talent)': (pr.get('yet_another_printer_multi_days'), 20),
                  'Moon of Print (compass)': (pr.get('moon_of_print_days'), 100)}, 'tb': tb, 'doot': pr.get('has_king_doot')}
    json.dump(out, open(ROOT / 'model' / 'printer.json', 'w'), indent=1)
    return out


def char_lines(o, c):
    x = o['per_char'].get(c)
    if not x: return []
    if not x['samples'] and not x['printing']:
        return ['No samples and no prints on this character: 2 print slots idle. Take samples on it (resets Gold Relic? unconfirmed per character; check before).']
    L = ['Printing: ' + ', '.join(f"{n} ({v:.3g})" for n, v in x['printing']) + ' | samples held: ' + ', '.join(f"{n} {v:.3g}" for n, v in x['samples'])]
    for s in o['swaps']:
        if s['char'] == c:
            L.append(f"SWAP print {s['from']} -> {s['to']} (sample {s['sample']:.3g}; {s['why']}). Changing a print does not take a sample, so Gold Relic keeps its days.")
    return L


def card_lines(o):
    gd, gmax, gm = o['gold_relic']
    L = [f"Gold Relic is at {gd} of {gmax} days ({gm}x print output). Taking any sample resets it, so hold off on new samples unless it's worth it (my read)."]
    sw = o['swaps']
    if sw: L.append(f"{len(sw)} print swaps are listed on the owners' cards.")
    cb = o.get('close_buffs') or []
    if cb:
        import datetime as _dt
        days = []
        for x in cb[:6]:
            if 'days' in x['label']:
                c, g = [float(v) for v in (re.findall(r'[\d.]+', str(x['cur']))[0], re.findall(r'[\d.]+', str(x['goal']))[0])]
                days.append(int(g - c))
        when = (_dt.date.today() + _dt.timedelta(days=max(days))).strftime('%b %d') if days else '?'
        lv = [re.split(r'[:(]', x['label'])[0].strip() for x in cb[:6] if 'days' not in x['label']]
        L.append(f"Print day is when all 6 print buffs are done. The day counters finish around {when}." + (f" Push these by then: {', '.join(lv)}." if lv else ''))
    L.append('AutoReview wants one sample goal next: Oak Logs to 10B. That sample resets Gold Relic, so time it for print day.')
    return L


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
    for c in o['per_char']: print(c, char_lines(o, c))
