"""Royal Armory planner (Autistastic, Royal Guardian #1). AutoReview only until the Toolbox page reads (it didn't load 2026-11-19)."""
from tbhelp import ar_items, save, tb


def build():
    tier, items = ar_items('Royal Armory')
    return save('royal_armory', {'ar_tier': tier, 'ar': items, 'toolbox': bool(tb('royal_armory') and 'Loading' not in tb('royal_armory')['_page']['text'][:200])})


def card_lines(o):
    L = []
    if not o['toolbox']: L.append('Toolbox Royal Armory page did not load on the last read: re-read it next refresh (costs + optimizer).')
    for g in ['Royal Statues', 'Armory Upgrades', 'Lil\' Orblet Shop', 'Statue Flair']:
        it = [i for i in o['ar'] if i['group'] == g and i.get('goal') not in (None, '', '✔') and i.get('cur') != i.get('goal')]
        if it: L.append(f"{g}: " + '; '.join(f"{i['label'][:60]} {i['cur']} -> {i['goal']}" for i in it[:5]))
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
