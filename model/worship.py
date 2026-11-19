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
    if zero: L.append(f"TOP: {', '.join(zero)} has never been run (wave 0). Every new wave adds to the Worship totalizer (total {o['total']}).")
    L.append('Wave pushes that unlock prayers: ' + '; '.join(f"{t} {o['waves'].get(t)} -> {w} unlocks {n}" for t, w, n in sorted(o['unlocks'], key=lambda x: x[1] - o['waves'].get(x[0], 0))))
    L.append('Best waves: ' + ', '.join(f"{k} {v}" for k, v in o['waves'].items()) + ". (Zack: passed 100 on the W6 totem yesterday, after this save.)")
    if o['msa']: L.append('Totalizer bonuses: ' + ', '.join(f"{k} {v}" for k, v in o['msa'].items()))
    for soul, use in o['soul_use_hr'].items():
        tot = next((k for k, v in SOUL_OF.items() if v == soul), '?')
        L.append(f"Soul budget: {soul} {o['souls'].get(soul, 0):,.0f} held; the salt chain eats {use:,.0f}/hr ({use * 24:,.0f}/day). Refill: {tot} runs (totem-soul map is my read, verify).")
    if o['chars']:
        top = sorted(o['chars'], key=lambda c: c['full'])[:3]
        L.append('Charge (spent on totem runs): ' + ', '.join(f"{c['char']} {c['charge']} ({c['rate']}/day, full in {c['full']})" for c in top) + ' fill first.')
    L.append("Griffy 2026-10 towers: get Voidinator ASAP, Frozen as the last line, Kraken for small enemies, don't call two tiny-enemy waves together. Pulse 2026-10: Clash of Cans soul is best for worship XP.")
    return L


RUNNER = 'Autistacular'   # Beast Master, runs the totems (jobs.yaml)
BUFFS = 'Autistabish'      # soul budget / town (jobs.yaml)


def char_lines(o, name):
    """Zack 2026-11-19: every character levels Worship and keeps its charge collected; the runner spends it on totems."""
    c = next((x for x in o['chars'] if x['char'] == name), None)
    if not c: return []
    rates = sorted(float(x['rate'].rstrip('%').replace(',', '')) for x in o['chars'])
    med = rates[len(rates) // 2]
    r = float(c['rate'].rstrip('%').replace(',', ''))
    L = [f"Worship Lv {c['lv']} ({c['skull']}), charge {c['charge']}, {c['rate']}/day, full in {c['full']}."]
    if r < med * 0.85: L.append(f"Charge rate below the group median {med:.0f}%/day: a higher skull or worship levels close it.")
    if r > med * 1.5: L.append(f"Fastest charger ({r / med:.1f}x median): Elemental Sorcerer, so likely the mage worship talents (my read; verify in talents).")
    if name == RUNNER: L.append("Runs the totems: spend charge on the wave pushes in the Worship block, then the lowest-wave totem.")
    if name == BUFFS:
        L.append("Owns the soul budget: refinery eats Dune + Frigid first, prayers/stamps spend only above reserve.")
        L += [f"{k}: {o['souls'].get(k, 0):,.0f} held, salts eat {v * 24:,.0f}/day ({o['souls'].get(k, 0) / (v * 24):.0f} days cover)." for k, v in o['soul_use_hr'].items()]
    if c['lv'] == min(x['lv'] for x in o['chars']): L.append("Lowest worship level on the account: AFK a few hours at a totem to catch up (my read).")
    return L


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
