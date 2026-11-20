"""Upgrade Vault planner (Autistopher). AutoReview vault targets + coin costs from coins.py.
Order: upgrades that serve a current top need first (model/priority.py), then AutoReview's order. Nothing pinned (Zack 2026-11-19)."""
import json
from tbhelp import ar_items, save, ROOT
from spend import h
SERVES = {'Kitchen Dream-mare': 'Cooking', 'Cooking Knowledge': 'Cooking', 'Artifact Find Chance': 'Sailing', 'Sailing Loot': 'Sailing',
          'Croppius Evolvius': 'Farming', 'Summoning Knowledge': 'Summoning', 'Big Blessings': 'Divinity', 'Super Slab': 'Slab'}


def build():
    c = json.load(open(ROOT / 'model' / 'coins.json'))
    cost = {v['name']: v for v in c['vault']}
    tier, items = ar_items('Upgrade Vault')
    tg = {}
    for i in items:
        if i['group'] == 'Progression Tiers': tg.setdefault(i['label'].split(':')[0], i)
    try: needs = [x['section'] for x in json.load(open(ROOT / 'model' / 'priority.json'))['needs'][:5]]
    except Exception: needs = []
    t = [{'name': k, 'cur': v['cur'], 'goal': v['goal'], 'coins': cost.get(k), 'need': SERVES.get(k) in needs} for k, v in tg.items()]
    t.sort(key=lambda x: not x['need'])
    return save('vault', {'ar_tier': tier, 'targets': t, 'richest': c.get('richest'), 'money': c.get('money', {}).get(c.get('richest'))})


def card_lines(o):
    L = []
    for i, x in enumerate(o['targets'][:6]):
        cc = x['coins'] or {}
        why = f" (helps {SERVES[x['name']]}, one of the biggest needs)" if x['need'] else ''
        if i == 0 and cc:
            L.append(f"Buy {x['name']} first{why}: {x['cur']} -> {x['goal']}. {o['richest']} has the coins for about {cc['buy_richest']} levels.")
        else:
            L.append(f"Then {x['name']} {x['cur']} -> {x['goal']}{why}.")
    L.append(f"Buy on {o['richest']}, he has the most coins. Each level count assumes all his coins go to that one upgrade.")
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
