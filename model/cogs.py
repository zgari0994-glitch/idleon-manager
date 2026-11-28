"""Cog board plan for the cog_board owner's card (Zack 2026-11-28, Phase C step E).
Source: Idleon Toolbox's own construction optimizer (tools/cog_plan.mjs -> snapshots/<save>/cog_plan.json), page defaults
(build / player con EXP / flaggy weighted 1:1:1, max 2 characters on the board, swap budgets 1/4/10/20).
Replaces monoblos Cogtimizer (last updated 2023-07; crashes on the newer cogs). Plain cog names are my read of the game codes."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TYPE = {'A00': 'plain', 'A0': 'plain', 'A1': 'average', 'A2': 'spur', 'A3': 'stacked', 'A4': 'deckered', 'B0': 'double',
        'B1': 'trips', 'B2': 'trabble', 'B3': 'quad', 'B4': 'penta', 'ad': 'adjacent', 'di': 'diagonal', 'up': 'up', 'do': 'down',
        'le': 'left', 'ri': 'right', 'ro': 'row', 'co': 'column', 'cr': 'corners'}
QUAL = {'0': 'Nooby', '1': 'Decent', '2': 'Superb', '3': 'Ultimate'}
MIN_GAIN = 0.01   # under 1% weighted gain = board already at Toolbox's best, no moves listed (my read of "worth the drags")


def plain(n):
    n = str(n or '')
    if n == 'CogY': return 'Yang cog'
    if n.startswith('CogZA0'): return 'Excogia piece'
    if n.startswith('Player_'): return n[7:]
    if n.startswith('Cog') and n[3:4] in QUAL: return f"{QUAL[n[3]]} {TYPE.get(n[4:], n[4:])} cog"
    return n


def plan(save=None):
    save = save or (ROOT / 'snapshots' / 'LATEST').read_text().strip()
    p = ROOT / 'snapshots' / save / 'cog_plan.json'
    return json.loads(p.read_text()) if p.exists() else None


def pct(a, b):
    if not b: return '?'
    v = (a / b - 1) * 100
    return 'same' if abs(v) < 0.05 else f"{v:+.1f}%"


def lines(save=None):
    P = plan(save)
    if not P: return ['Cog board: no optimizer plan for this save (tools/cog_plan.mjs did not run)']
    best = next((x for x in P['plans'] if x['swaps'] == P['best']), None)
    if not best or best['gain'] < MIN_GAIN or not best['moves']:
        return [f"Cog board: already at Toolbox optimizer's best (best plan +{(best or {}).get('gain', 0) * 100:.1f}%), no moves (Toolbox)"]
    n, t = P['now'], best['totals']
    out = [f"Cog board (weekly, Thu): {len(best['moves'])} drags -> build {pct(t['build'], n['build'])}, player con EXP "
           f"{pct(t['playerExp'], n['playerExp'])}, flaggy {pct(t['flaggy'], n['flaggy'])} (Toolbox optimizer, max {P['maxCharacters']} characters on board). In order:"]
    for i, m in enumerate(best['moves'], 1):
        frm = m['from'].replace('Inv ', 'inventory ').replace('P1', 'page 1')
        out.append(f"   {i}. drag the {plain(m['cog'])} at {frm} onto {m['to']}")
    small = [x for x in P['plans'] if x['moves'] and x['gain'] >= MIN_GAIN and x['swaps'] != P['best']]
    if small:
        ok = [x for x in small if x['gain'] >= 0.8 * best['gain']]   # smallest plan with 80%+ of the gain (my read)
        s = min(ok or small, key=lambda x: len(x['moves']))
        out.append(f"   short on time: Toolbox's {len(s['moves'])}-drag plan gets +{s['gain'] * 100:.1f}% of the +{best['gain'] * 100:.1f}% "
                   f"(different drags: W3 Construction page in Toolbox, Optimize)")
    used = sum(1 for m in best['moves'] if m['from'].startswith('Inv'))
    if P.get('spares'):
        left = P['spares'] - used
        out.append(f"   spares: {'nothing to scrap, the drags put your spare cogs on the board' if left <= 0 else f'scrap the {left} spare cogs these drags leave unused'} (Griffy 2024, old: just scrap cogs)")
    return out


if __name__ == '__main__':
    print('\n'.join(lines()))
