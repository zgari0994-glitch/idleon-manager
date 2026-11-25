"""W7 minis planner (Autisticles, Zack 2026-11-19: all W7 minis incl. Minehead + Glimbo). One block, daily items first, then buy-now per system."""
import re, json
from tbhelp import tb, ar_items, n, save, ROOT


def _g(t, k):
    m = re.search(re.escape(k) + r'\n([^\n]+)', t); return m.group(1) if m else None


def _ups(text):
    """name, Lv, held, cost for 'Name\\nLv X(/Y)\\n...\\nheld\\n/\\ncost' blocks"""
    out = []
    for m in re.finditer(r'\n([A-Z][^\n]{2,40})\nLv ([\d,]+)(?: / ([\d,]+))?\n(.*?)(?=\n[A-Z][^\n]{2,40}\nLv [\d,]+|\nDiscord|\Z)', text, re.S):
        b = m.group(4); c = re.search(r'\n([\d.,]+[KMBTQ]*)\n/\n([\d.,]+[KMBTQ]*)\n', b + '\n')
        out.append({'name': m.group(1), 'lv': m.group(2), 'max': m.group(3), 'locked': 'Locked' in b[:40], 'held': n(c.group(1)) if c else None, 'cost': n(c.group(2)) if c else None})
    return out


def build():
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py)
    from data import load
    D = load(); o = {}
    lt = D.system('legend_talents'); o['legend'] = {'points': lt['pointsOwned']['value'], 'unspent': str(lt['pointsLeftToSpend'])}
    J = D.system('jelly_operator'); o['jelly'] = {'ops': str(J['operationsLeft']), 'next': None, 'removed': f"{J['obstructionsDefeated']} / {J['maxObstructionsDefeated']}"}
    C = D.system('clam_work')
    o['clam'] = {'pearls': C['ownedPearls'], 'ready': [(u['name'].replace('_', ' ').title(), u['level'], u['level'] + 1, '', f"{u['cost']:,.0f}") for u in C['upgrades']
                                                      if u.get('unlocked') and u['cost'] <= C['ownedPearls']]}
    S = D.system('sushi_station'); bucks = S['currency']['bucks']
    o['sushi'] = {'fuel': (f"{S['fuel']['current']:,.0f}", f"{S['fuel']['cap']:,.0f}"), 'next': None, 'bucks': bucks, 'unique': S['uniqueSushi'],
                  'cheap': [(u['name'], u['level'], u['cost']) for u in S['upgrades'] if u.get('cost') and u['cost'] <= bucks * 0.05 and str(u.get('maxLevel')) != str(u['level'])]}
    M = D.system('minehead')
    o['minehead'] = {'tries': f"{M['dailyTriesLeft']} / {M['dailyTriesMax']}", 'cur': M['mineCurrency'], 'next': None,
                     'buy': [(u['name'].replace('_', ' '), u['level'], u['cost']) for u in M['upgrades'] if u.get('canAfford') and not u.get('isLocked') and not u.get('isMaxed')],
                     'opp': [(x['name'], x.get('ordinal'), x.get('maxHP'), x.get('bonusDescription', '')) for x in M['opponents'] if not x.get('beaten')][:1]}
    o['glimbo'] = {'total': M['glimboTotalTrades'],
                   'trades': [(g['itemName'].replace('_', ' '), D.item_count(g['rawItemName']), int(float(g['cost']))) for g in M['glimbo'] if g.get('flag')]}
    Bt = D.system('the_button')['currentTask']
    o['gates'] = {'zenith': False, 'button': False, 'button_req': [(Bt['description'], f"{Bt.get('progress')} / {Bt.get('requirement')}")]}
    o['zenith'] = {'clusters': D.system('zenith_market')['clusters']}
    o['advice'] = None
    return save('w7minis', o)


def card_lines(o):
    L = []
    d = []
    if o['jelly']['ops'] and o['jelly']['ops'] != '0': d.append(f"use {o['jelly']['ops']} Jelly operations")
    if o['minehead']['tries'] and not o['minehead']['tries'].startswith('0'): d.append(f"play {o['minehead']['tries'].split(' / ')[0]} Minehead tries")
    f = o['sushi']['fuel']
    if f and int(f[0].replace(',', '')) >= 0.9 * int(f[1].replace(',', '')): d.append('spend Sushi fuel (nearly full)')
    if d: L.append('TOP dailies: ' + ', '.join(d) + '.')
    if o['legend']['unspent'] and o['legend']['unspent'] != '0': L.append(f"Spend {o['legend']['unspent']} Legend Talent points: Coral Restoration first (Griffy: +60% daily coral, an absolute must). Keep Blue Ribbon and Extended Database on hold.")
    nx = o['sushi']['next']
    if nx and f and int(f[0].replace(',', '')) >= int(nx[1].replace(',', '')): L.append(f"Unlock {nx[0].strip()} in Sushi now.")
    if o['sushi']['cheap']: L.append('Cheap Sushi upgrades: ' + ', '.join(a for a, b, c in o['sushi']['cheap'][:5]) + '.')
    if o['clam']['ready']: L.append('Clam: buy ' + ', '.join(f"{a} ({e} pearls)" for a, b, c, d2, e in o['clam']['ready']) + '.')
    if o['minehead']['buy']: L.append('Minehead: buy ' + ', '.join(a for a, b, c in o['minehead']['buy'][:4]) + '.')
    if o['minehead']['opp']:
        a, b, hp, rw = o['minehead']['opp'][0]; L.append(f"Beat {a} next: {rw.split('.')[0].lower()}.")
    tr = [t for t in o['glimbo']['trades'] if t[1] >= t[2]]
    if tr: L.append(f"Glimbo: make {len(tr)} trades ({', '.join(a for a, h_, nd in tr[:4])}{'...' if len(tr) > 4 else ''}). Each one raises a Vault max level. Pulse: push to about 1,000 total trades (you're at {o['glimbo'].get('total')}).")
    g = [x for x, on in (('Zenith Market', o['gates']['zenith']), ('The Button', o['gates']['button'])) if on]
    if g: L.append(f"Not unlocked yet: {', '.join(g)}.")
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
