"""Lab planner (Autistocat Lab block). Bonuses/jewels on, players not souped up, chip + jewel rotation with what's missing."""
import re
from tbhelp import tb, n, save


def build():
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py); the chip/jewel shop rotation is website-only (not in the parser)
    from data import load
    L = load().system('lab_bonuses')
    lb, jw = L['labBonuses'], L['jewels']
    on = (sum(1 for b in lb if b.get('active')), len(lb), sum(1 for j in jw if j.get('active')), len(jw), sum(1 for j in jw if j.get('acquired')), len(jw))
    players = [(p['playerName'], 'Souped up' if p.get('soupedUp') else 'not souped', f"{p.get('lineWidth', 0):.0f}") for p in L['playersCords']]
    return save('lab', {'on': on, 'players': players, 'rotation': []})

def card_lines(o):
    L = []
    if o['on']: L.append(f"Lab: {o['on'][0]} of {o['on'][1]} bonuses on, {o['on'][2]} of {o['on'][3]} jewels on ({o['on'][4]} owned)." + ('' if o['on'][0] == o['on'][1] else ' Some bonuses are off: check connections.'))
    nos = [p for p, l, r in o['players'] if 'Souped' not in l]
    if nos: L.append(f"{', '.join(nos)} isn't souped up, so his lab range is lower.")
    blk = [x for x in o['rotation'] if x['need'] and x['state'] != 'Sold out'][:3]
    if blk: L.append('Coming in the shop but you are short: ' + '; '.join(f"{x['item']} on {x['date'][:5]} (need {x['need'][0]} more)" for x in blk) + '.')
    opn = [x for x in o['rotation'] if x['state'] == 'open' and not x['need'] and x['effect']][:3]
    if opn: L.append('You can buy these when they rotate in: ' + '; '.join(f"{x['item']} ({x['effect'][:50]})" for x in opn) + '.')
    return L


def char_lines(o, name): return []


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
