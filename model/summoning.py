"""Summoning planner (Autistocat). Unclaimed familiar EXP, daily Familiar buy, affordable essence upgrades per colour, Teal gate (Spelunking)."""
import re
from tbhelp import tb, ar_items, save

UNIT = {'': 1, 'K': 1e3, 'M': 1e6, 'B': 1e9, 'T': 1e12, 'Q': 1e15, 'QQ': 1e18}
def q(s):
    m = re.match(r'([\d.,]+)\s*(QQ|Q|T|B|M|K)?', s.strip()); return float(m.group(1).replace(',', '')) * UNIT[m.group(2) or ''] if m else None


def build():
    T = tb('summoning'); u = T['Upgrades']['text']
    unc = re.search(r'Unclaimed familiar EXP\n([^\n]+)\n([^\n]+)', u); end = re.search(r'Highest endless level\n(\d+)', u)
    ess = {c: (q(a), b) for c, a, b in re.findall(r'\n(\w+) essence\n([^\n]+)\n(\+[^\n]+)', u)}
    ups = []; colour = None
    for line_block in re.finditer(r'\n([A-Z][^\n]+)\nLv ([\d,]+) / ([\d,]+)\n(.*?)(?=\n[A-Z][^\n]+\nLv [\d,]+ / |\nDiscord|\Z)', u[u.find('Filters'):], re.S):
        b = line_block.group(4); c = re.search(r'\n([\d.,]+\s*(?:QQ|Q|T|B|M|K)?)\n/\n([\d.,]+\s*(?:QQ|Q|T|B|M|K)?)\n', b + '\n')
        if c:
            held = q(c.group(1)); colour = next((k for k, (v, _) in ess.items() if v and held and abs(v - held) / v < 0.02), colour)
        ups.append({'name': line_block.group(1), 'lv': int(line_block.group(2).replace(',', '')), 'max': int(line_block.group(3).replace(',', '')), 'cost': q(c.group(2)) if c else None,
                    'held': q(c.group(1)) if c else None, 'colour': colour, 'daily': 'Cost resets' in b})
    bt = T['Battles']['text']; teal = re.search(r'Teal \((\d+)/(\d+)\)', bt)
    return save('summoning', {'unclaimed': unc.groups() if unc else None, 'endless': int(end.group(1)) if end else None, 'essence': ess, 'upgrades': ups,
                              'teal': teal.groups() if teal else None})


def card_lines(o):
    L = []
    if o['unclaimed']: L.append(f"TOP: claim the familiar EXP ({o['unclaimed'][0]}, {o['unclaimed'][1].split(' unclaimed')[0]} of it).")
    if [x for x in o['upgrades'] if x['daily'] and x['lv'] < x['max']]: L.append('Buy Familiar every day. It costs 1 essence and the price resets daily.')
    aff = [x for x in o['upgrades'] if x['cost'] and x['held'] and x['cost'] <= x['held'] * 0.01 and x['lv'] < x['max'] and not x['daily']]
    if aff: L.append(f"{len(aff)} upgrades are basically free right now: " + ', '.join(x['name'] for x in aff[:6]) + '.')
    if o['teal']: L.append(f"Teal battles ({o['teal'][0]} of {o['teal'][1]}) open up after Autistomatic's Spelunking cave.")
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
