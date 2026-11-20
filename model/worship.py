"""Worship planner: totem waves vs what they unlock (prayers), soul budget (income from totems vs refinery/prayer/stamp use), charge.
-> Bish's Worship block. Zack 2026-11-19: passed wave 100 on the W6 totem yesterday (save predates it)."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip()
SOUL_OF = {'Goblin Gorefest': 'Forest Soul', 'Wakawaka War': 'Dune Soul', 'Acorn Assault': 'Rooted Soul', 'Frosty Firefight': 'Frigid Soul',
           'Clash of Cans': 'Squishy Soul'}   # my read from the soul list order on Toolbox; verify in game


def build():
    t = (SNAP / 'toolbox' / 'worship.txt').read_text()
    waves = {a.strip(): int(b) for a, b in re.findall(r'\n([A-Z][A-Za-z ]+)\n\t(\d+)\t', t)}
    chars = [{'char': a, 'lv': int(b), 'skull': c, 'charge': d, 'rate': e, 'full': f} for a, b, c, d, e, f in
             re.findall(r'\n(Autis\w+)\nWorship Lv (\d+) · ([^\n]+)\nCharge\n([^\n]+)\nCharge rate\n([^\n]+) per day\nFull in\n([^\n]+)', t)]
    msa = dict(re.findall(r'\n(Spelunking Pow|Research Exp|DMG|Class XP|Skill XP)\n([^\n]+)', t))
    pr = {}
    try: pr = json.load(open(ROOT / 'model' / 'prayers.json'))
    except Exception: pass
    unlocks = [(p['totem'], p['wave_need'], p['name']) for p in pr.get('prayers', []) if p.get('locked')]
    ref = {}
    try: ref = json.load(open(ROOT / 'model' / 'refinery.json')).get('soul_use_hr', {})
    except Exception: pass
    out = {'snapshot': SNAP.name, 'waves': waves, 'total': sum(waves.values()), 'chars': chars, 'msa': msa, 'unlocks': unlocks, 'soul_use_hr': ref, 'souls': pr.get('souls', {})}
    json.dump(out, open(ROOT / 'model' / 'worship.json', 'w'), indent=1)
    return out


def card_lines(o):
    L = []
    zero = [k for k, v in o['waves'].items() if v == 0]
    if zero: L.append(f"TOP: run {' and '.join(zero)} for the first time. Every new wave adds to the worship total bonus.")
    un = sorted(o['unlocks'], key=lambda x: x[1] - o['waves'].get(x[0], 0))[:3]
    if un: L.append('Closest prayer unlocks: ' + '; '.join(f"{t} to wave {w} for {n}" for t, w, n in un) + '.')
    if o['chars']:
        top = sorted(o['chars'], key=lambda c: c['full'])[:2]
        L.append(f"Use charge from {' and '.join(c['char'] for c in top)} first, they fill up soonest.")
    L.append('Griffy: get Voidinator early, Frozen as the last line, Kraken for small enemies. Pulse: Clash of Cans souls give the most worship EXP.')
    return L


RUNNER = 'Autistacular'   # Beast Master, runs the totems (jobs.yaml)
BUFFS = 'Autistabish'      # soul budget / town (jobs.yaml)


def char_lines(o, name):
    c = next((x for x in o['chars'] if x['char'] == name), None)
    if not c: return []
    rates = sorted(float(x['rate'].rstrip('%').replace(',', '')) for x in o['chars'])
    med = rates[len(rates) // 2]; r = float(c['rate'].rstrip('%').replace(',', ''))
    L = [f"Worship level {c['lv']}, charge full in {c['full']}."]
    if r > med * 1.5: L.append('Charges much faster than the rest, probably from mage worship talents (my read).')
    if name == RUNNER: L.append('Runs the totems: spend charge on the prayer-unlock waves first, then the lowest totem.')
    if name == BUFFS:
        for k, v in o['soul_use_hr'].items():
            L.append(f"{k}: enough for about {o['souls'].get(k, 0) / (v * 24):.0f} days of salts. Spend souls elsewhere only above that.")
    if c['lv'] == min(x['lv'] for x in o['chars']): L.append('Lowest worship level on the account, sit at a totem for a few hours to catch up (my read).')
    return L


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
