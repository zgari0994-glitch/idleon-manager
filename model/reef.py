"""Coral Reef + Dancing Coral planner (Autistachio). Affordable reef upgrades, coral bonuses gated by shrine levels (routed to Autistastic)."""
import re
from tbhelp import tb, n, save


def build():
    T = tb('reef'); r = T['Reef Upgrades']['text']; d = T['Dancing Coral']['text']
    coral = n((re.search(r'Coral\n([\d,]+)', r) or [0, '0'])[1])
    ups = [(a, int(lv), int(mx), n(c)) for a, lv, mx, c in re.findall(r'\n([^\n]{6,120})\nLv (\d+) / (\d+)\n(?:Unlocks\n[^\n]+\n)?[\d.,]+[KMB]?\n/\n([\d.,]+[KMB]?)', r)]
    dance = re.findall(r'\n([A-Z]\w+ Coral)\n(\+100 max LV for [^\n]+)\n.*?\n([A-Z]\w+ Shrine) LV\n(\d+)\nSource\n([^\n]+)\nBonus starts\n([^\n]+)', d, re.S)
    return save('reef', {'coral': coral, 'ups': ups, 'dance': dance})


def card_lines(o):
    aff = sorted([u for u in o['ups'] if u[3] and u[3] <= o['coral'] and u[1] < u[2]], key=lambda u: u[3])
    L = []
    if aff:
        run = sum(u[3] for u in aff if u[3] <= o['coral'])
        L.append(f"TOP: spend coral on all {len(aff)} Reef upgrades ({run:,.0f} of your {o['coral']:,.0f}). The big one gives a Menagerie shell.")
    if o['dance']: L.append('Dancing Coral bonuses start when ' + ' and '.join(f"{s} reaches 201 (now {lv})" for c, b, s, lv, src, st in o['dance']) + '. Autistastic levels the shrines.')
    return L


def routed(o):
    return {'Autistastic': [f"Level {s} from {lv} to 201 to start Autistachio's {c} bonus." for c, b, s, lv, src, st in o['dance'] if int(lv) < 201][:3]} if o['dance'] else {}


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
    print(routed(o))
