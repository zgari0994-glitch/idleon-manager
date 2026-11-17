"""Coin cost vs money (Phase 1 item 6). Formulas copied from Idleon Toolbox source (2026-11-17):
- Upgrade Vault: parsers/misc/upgradeVault.ts getUpgradeCost (base = lv + (x1+lv)*x2^lv; Darts opt 437,
  Cryosnake companion 50%, vault upgrade 13 for idx<33, 1.1^(idx-61) for idx>61). Sushi discount NOT applied (flag).
- Advice Fish: parsers/misc.ts getAdviceFish (1.15^lv * 10.01^x3).
- Stamps: tools/stamp_cost.py. Vendor items: item Sell Price (verify one in game).
Coins are per character: affordability is checked against each character's own coins.
Writes model/coins.json + coins.md. Usage: python3 model/coins.py"""
import json, gzip, os, sys, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '/home/claude/ar/mysite')
from consts.generated.raw_item_data import raw_item_data as RD
stamp = open(os.path.join(R, 'snapshots', 'LATEST')).read().strip()
d = json.load(gzip.open(os.path.join(R, 'snapshots', stamp, 'raw.json.gz'))); d = d.get('data', d)
g = lambda k: json.loads(d[k]) if isinstance(d.get(k), str) else d.get(k)
S = json.load(gzip.open(os.path.join(R, 'snapshots', stamp, 'systems.json.gz'))); S = S.get('systems', S)
chars = json.load(open(os.path.join(R, 'snapshots', stamp, 'chars.json')))['characters']
CD = json.load(open(os.path.join(R, 'sources', 'toolbox', 'cost_data.json')))
money = {c['character_name']: d.get(f"Money_{c['character_index']}", 0) for c in chars}
richest = max(money, key=money.get)
def who(cost): return [n for n, m in money.items() if m >= cost]

# ---- Upgrade Vault ----
lv = g('UpgVault') or []
V = CD['upgradeVault']
total_lv = sum(lv)
darts = 1 / (1 + ((g('OptLacc') or [0] * 500)[437] or 0) / 100)
cryo = 0.5 if 'Cryosnake' in S.get('companions', {}) else 1.0
bonus13 = (lv[13] if len(lv) > 13 else 0) * V[13].get('x5', 1)
def vcost(i, L):
    u = V[i]; base = L + (u['x1'] + L) * u['x2'] ** L
    if i < 33: return max(0.001, (1 / (1 + bonus13 / 100)) * darts) * cryo * base
    return max(0.01, darts) * cryo * 1.1 ** max(0, i - 61) * base
vault = []
for i, u in enumerate(V):
    L = lv[i] if i < len(lv) else 0
    if total_lv < u.get('unlockLevel', 0) or L >= u['maxLevel'] or u['name'].startswith('_'): continue
    nxt = vcost(i, L); tomax = sum(vcost(i, k) for k in range(L, u['maxLevel']))
    buy, spent, k = 0, 0.0, L
    while k < u['maxLevel'] and spent + vcost(i, k) <= money[richest]: spent += vcost(i, k); k += 1; buy += 1
    vault.append({'buy_richest': buy, 'buy_cost': spent, 'i': i, 'name': u['name'].replace('_', ' '), 'level': L, 'max': u['maxLevel'], 'next': nxt, 'to_max': tomax,
                  'next_ok': who(nxt), 'max_ok': who(tomax)})

# ---- Advice Fish ----
sp = g('Spelunk') or []
alv = sp[11] if len(sp) > 11 else []
fish = []
for i, row in enumerate(CD['adviceFish']):
    name, desc, x2, x3 = row.split(',')[:4]
    L = alv[i] if i < len(alv) else 0
    c = 1.15 ** L * 10.01 ** float(x3)
    fish.append({'name': name.replace('_', ' '), 'level': L, 'next': c, 'bonus_now': L / (100 + L) * float(x2), 'max_bonus': float(x2), 'next_ok': who(c)})

# ---- Vendor items still missing (Storage section) ----
review = json.load(gzip.open(os.path.join(R, 'snapshots', stamp, 'review.json.gz')))
store = next(s for w in review['worlds'] for s in w['sections'] if s['name'] == 'Storage')
names = set()
def walk(n):
    for a in n.get('items', []):
        if 'items' in a: walk(a)
        elif 'Vendor' in a.get('label', '') and not a.get('completed'): names.add(a['label'].split(':')[0].strip())
    for t in n.get('tabs', []): walk(t)
for gr in store['groups']: walk(gr)
byname = {v['Name'].lower(): v for v in RD.values() if isinstance(v, dict) and 'Name' in v}
vendor = []
for n in sorted(names):
    it = byname.get(n.lower())
    if it: vendor.append({'name': n, 'price': float(it['Sell Price']), 'ok': who(float(it['Sell Price'])),
                          'check': float(it['Sell Price']) < 1e6})  # suspiciously cheap: sell price may not be the vendor price

out = {'stamp': stamp, 'money': money, 'richest': richest, 'vault_multi': {'darts': darts, 'cryosnake': cryo, 'vault13_bonus': bonus13},
       'vault': sorted(vault, key=lambda x: x['next']), 'advice_fish': fish, 'vendor': sorted(vendor, key=lambda x: x['price']),
       'caveats': ['Sushi vault discount not applied (costs may be lower)', 'Vault max levels exclude event shop/bundle/Glimbo extras',
                   'Vendor price = item Sell Price: verify one in game', 'Coins are per character: buy on the character that holds them']}
json.dump(out, open(os.path.join(R, 'model', 'coins.json'), 'w'), indent=1)
e = lambda x: f"{x:.2e}"
L = [f"# Coins vs costs · save {stamp}", f"Money: total {e(sum(money.values()))}; richest {richest} {e(money[richest])}", '', '## Upgrade Vault (cheapest next first)']
for v in out['vault'][:25]:
    L.append(f"- {v['name']} {v['level']}/{v['max']}: next {e(v['next'])} ({len(v['next_ok'])} chars can) · {richest} can buy +{v['buy_richest']} ({e(v['buy_cost'])}) · to max {e(v['to_max'])}" + (f" ({', '.join(v['max_ok'][:3])})" if v['max_ok'] else ' (nobody)'))
L += ['', '## Advice Fish'] + [f"- {f['name']} lv {f['level']}: next {e(f['next'])} · {', '.join(f['next_ok'][:3]) or 'nobody'} · bonus {f['bonus_now']:.2f}/{f['max_bonus']}" for f in fish]
L += ['', '## Vendor items missing'] + [f"- {v['name']}: {e(v['price'])} · {', '.join(v['ok'][:3]) or 'nobody'}" + (' · CHECK PRICE IN GAME' if v['check'] else '') for v in out['vendor']]
L += ['', '## Caveats'] + [f"- {c}" for c in out['caveats']]
open(os.path.join(R, 'model', 'coins.md'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
