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
    aff = [u for u in o['ups'] if u[3] and u[3] <= o['coral'] and u[1] < u[2]]
    L = []
    if aff:
        run, pick = 0, []
        for u in sorted(aff, key=lambda u: u[3]):
            if run + u[3] <= o['coral']: run += u[3]; pick.append(u)
        L.append(f"TOP: coral {o['coral']:,.0f}: buy " + ', '.join(f"{u[0][:55]} Lv {u[1]} ({u[3]:,.0f})" for u in pick) + f" = {run:,.0f}.")
    if o['dance']: L.append('Dancing Coral bonuses start at shrine Lv 201: ' + ', '.join(f"{s} {lv} ({st})" for c, b, s, lv, src, st in o['dance']) + ' (shrine levels = Construction on Autistastic).')
    return L


def routed(o):
    return {'Autistastic': [f"Shrine {s} {lv} -> 201 starts the {c} bonus (Autistachio's reef)" for c, b, s, lv, src, st in o['dance'] if int(lv) < 201][:3]} if o['dance'] else {}


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
    print(routed(o))
