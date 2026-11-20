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
    o = {}
    L = tb('legend')['_page']['text']; o['legend'] = {'points': _g(L, 'Legend points'), 'unspent': re.search(r'(\d+) unspent', L).group(1) if re.search(r'(\d+) unspent', L) else None}
    J = tb('jelly'); jt = J['Layout']['text']
    o['jelly'] = {'ops': _g(jt, 'Operations left'), 'next': (re.search(r'Next: ([^\n]+)', jt) or [None, None])[1], 'removed': _g(jt, 'Obstructions removed')}
    C = tb('clam'); ct = C['Upgrade Optimizer']['text']
    o['clam'] = {'pearls': _g(ct, 'Pearls'), 'ready': re.findall(r'\n([A-Z][^\n]+)\nLv (\d+) → (\d+) · Upgrade #\d+\nPearl gain\n([^\n]+)\nCost\n([^\n]+)\nready now', ct)}
    S = tb('sushi'); st = S['Sushi']['text']
    fuel = re.search(r'Fuel\n([\d,]+) / ([\d,]+)', st); nxt = re.search(r'Next unlock\n([^\(]+)\(([\d,]+) fuel\)', st)
    sups = [u for u in _ups(S['Upgrades']['text'][S['Upgrades']['text'].find('Total upgrade LV'):]) if u['cost'] and u['held'] and u['cost'] <= u['held'] * 0.05]
    o['sushi'] = {'fuel': fuel.groups() if fuel else None, 'next': nxt.groups() if nxt else None, 'bucks': _g(st, 'Bucks'), 'cheap': [(u['name'], u['lv'], u['cost']) for u in sups]}
    M = tb('minehead'); mt = M['Upgrades']['text']
    o['minehead'] = {'tries': _g(mt, 'Daily tries'), 'cur': _g(mt, 'Mine currency'), 'next': (re.search(r'Next: ([^\n]+)', mt) or [None, None])[1],
                     'buy': [(u['name'], u['lv'], u['cost']) for u in _ups(mt[mt.find('Filters'):]) if u['cost'] and u['held'] and u['cost'] <= u['held']],
                     'opp': re.findall(r'\n([A-Z]\w+head)\nthe honorable, (\w+) opponent\n(?:●\nNext\n)?Max HP\n([^\n]+)\nDepth charges\n\d+\nREWARD\n\n([^\n]+)', M['Opponents']['text'])}
    G = tb('glimbo')['_page']['text']
    o['glimbo'] = {'trades': [(a, int(c.replace(',', '')), int(d.replace(',', ''))) for a, b, c, d in re.findall(r'\n([A-Z][^\n]+)\nTraded (\d+) times\nMax LV\n\d+\nNext trade\n[^\n]+\n([\d,]+)\n/\n([\d,]+)', G)]}
    Z = tb('zenith')['_page']['text']; B = tb('button')['_page']['text']
    o['gates'] = {'zenith': 'hasn\'t reached' in Z, 'button': 'hasn\'t reached' in B,
                  'button_req': re.findall(r'\n([^\n]{12,90})\nNext press\n●\n([^\n]+)', B) + re.findall(r'\n(Reach [^\n]+)\n(Best: [^\n]+)', B)}
    try: o['advice'] = json.load(open(ROOT / 'model' / 'coins.json')).get('advice_fish')
    except Exception: o['advice'] = None
    return save('w7minis', o)


def card_lines(o):
    L = []
    d = []
    if o['jelly']['ops'] and o['jelly']['ops'] != '0': d.append(f"use {o['jelly']['ops']} Jelly operations")
    if o['minehead']['tries'] and not o['minehead']['tries'].startswith('0'): d.append(f"play {o['minehead']['tries'].split(' / ')[0]} Minehead tries")
    f = o['sushi']['fuel']
    if f and int(f[0].replace(',', '')) >= 0.9 * int(f[1].replace(',', '')): d.append('spend Sushi fuel (nearly full)')
    if d: L.append('TOP dailies: ' + ', '.join(d) + '.')
    if o['legend']['unspent'] and o['legend']['unspent'] != '0': L.append(f"Spend {o['legend']['unspent']} Legend Talent points (keep Blue Ribbon and Extended Database on hold).")
    nx = o['sushi']['next']
    if nx and f and int(f[0].replace(',', '')) >= int(nx[1].replace(',', '')): L.append(f"Unlock {nx[0].strip()} in Sushi now.")
    if o['sushi']['cheap']: L.append('Cheap Sushi upgrades: ' + ', '.join(a for a, b, c in o['sushi']['cheap'][:5]) + '.')
    if o['clam']['ready']: L.append('Clam: buy ' + ', '.join(f"{a} ({e} pearls)" for a, b, c, d2, e in o['clam']['ready']) + '.')
    if o['minehead']['buy']: L.append('Minehead: buy ' + ', '.join(a for a, b, c in o['minehead']['buy'][:4]) + '.')
    if o['minehead']['opp']:
        a, b, hp, rw = o['minehead']['opp'][0]; L.append(f"Beat {a} next: {rw.split('.')[0].lower()}.")
    tr = [t for t in o['glimbo']['trades'] if t[1] >= t[2]]
    if tr: L.append(f"Glimbo: make {len(tr)} trades ({', '.join(a for a, h_, nd in tr[:4])}...). Each one raises a Vault max level.")
    g = [x for x, on in (('Zenith Market', o['gates']['zenith']), ('The Button', o['gates']['button'])) if on]
    if g: L.append(f"Not unlocked yet: {', '.join(g)}.")
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
