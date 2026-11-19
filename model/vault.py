"""Upgrade Vault planner (Autistopher). AutoReview vault targets + coin costs from coins.py (who can afford, levels the richest can buy).
Priority: account priority first (cooking speed = Kitchen Dream-mare, jobs.yaml), then AutoReview order."""
import json
from tbhelp import ar_items, save, ROOT
from spend import h
PRIORITY = ['Kitchen Dream-mare', 'Cooking Knowledge']   # jobs.yaml: cooking speed = account priority (Zack)


def build():
    c = json.load(open(ROOT / 'model' / 'coins.json'))
    cost = {v['name']: v for v in c['vault']}
    tier, items = ar_items('Upgrade Vault')
    tg = {}
    for i in items:
        if i['group'] != 'Progression Tiers': continue
        nm = i['label'].split(':')[0]
        tg.setdefault(nm, i)
    return save('vault', {'ar_tier': tier, 'targets': [{'name': k, 'cur': v['cur'], 'goal': v['goal'], 'coins': cost.get(k)} for k, v in tg.items()],
                          'richest': c.get('richest'), 'money': c.get('money', {}).get(c.get('richest'))})


def card_lines(o):
    L = []
    t = sorted(o['targets'], key=lambda x: (x['name'] not in PRIORITY, PRIORITY.index(x['name']) if x['name'] in PRIORITY else 0))
    top = t[0] if t else None
    if top and top['coins']:
        cc = top['coins']
        L.append(f"TOP (account priority): {top['name']} {top['cur']} -> {top['goal']}. Next level {h(cc['next'])} coins; {o['richest']} ({h(o['money'])}) can buy {cc['buy_richest']} levels now ({h(cc['buy_cost'])}).")
    for x in t[1:8]:
        cc = x['coins'] or {}
        L.append(f"{x['name']} {x['cur']} -> {x['goal']}" + (f": next {h(cc['next'])}, richest alone could buy {cc['buy_richest']} levels" if cc else ' (cost not in coins.py)'))
    L.append("Level counts assume all of that character's coins go to that one upgrade; buy the TOP one first, then re-check.")
    L.append(f"AutoReview Upgrade Vault tier {o['ar_tier']}. Coins are per character: buy on {o['richest']} first. Toolbox Upgrade Vault total levels should rise by what you bought.")
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
