"""Royal Armory planner (Autistastic, Royal Guardian #1). AutoReview only until the Toolbox page reads (it didn't load 2026-11-19)."""
from tbhelp import ar_items, save, tb


def build():
    tier, items = ar_items('Royal Armory')
    return save('royal_armory', {'ar_tier': tier, 'ar': items, 'toolbox': bool(tb('royal_armory') and any('Loading account data' not in t['text'][:400] for t in tb('royal_armory').values())), 'tabs': list(tb('royal_armory') or {})})


def card_lines(o):
    L = []
    it = [i for i in o['ar'] if i['group'] == 'Royal Statues' and i.get('cur') == '0']
    if it: L.append(f"Next Royal statue to build: {it[0]['label'].split(':')[0]}.")
    up = [i for i in o['ar'] if i['group'] == 'Armory Upgrades' and i.get('goal') not in (None, '', '✔') and i.get('cur') != i.get('goal')]
    if up: L.append('Armory upgrades to push: ' + ', '.join(i['label'].split(':')[0] for i in up[:3]) + '.')
    if not o['toolbox']: L.append("Toolbox's Royal Armory page didn't load, so costs come next time.")
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
