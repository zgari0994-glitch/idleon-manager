"""Equinox planner (Autistopher). Bar fill/cap, claimable challenges, locked upgrades + unlock progress, AutoReview targets."""
import re
from tbhelp import tb, ar_items, n, save


def build():
    T = tb('equinox'); u = T['Upgrades']['text']; c = T['Challenges']['text']
    fill = re.search(r'Fill rate\n([\d,.]+)/hr', u); bar = re.search(r'Equinox bar\n([\d,]+) / ([\d,]+)', u)
    ups = []
    for m in re.finditer(r'\n([A-Z][^\n]{2,30})\nLv (\d+) / (\d+)\n(.*?)(?=\n[A-Z][^\n]{2,30}\nLv \d+ / |\nDiscord|\Z)', u, re.S):
        b = m.group(4); un = re.search(r'UNLOCKS WITH\n\n([^\n]+)\n\n([^\n]+)', b)
        ups.append({'name': m.group(1), 'lv': int(m.group(2)), 'max': int(m.group(3)), 'locked': '\nLocked' in b[:20] or b.startswith('Locked'),
                    'unlock': un.group(1) if un else None, 'progress': un.group(2) if un else None})
    ch = []
    for m in re.finditer(r'\n([^\n]{20,200})\n(?:●\n([^\n]+)\n)?Reward\n([^\n]+)\nProgress\n([^\n]+)', c):
        ch.append({'task': m.group(1), 'state': m.group(2), 'reward': m.group(3), 'progress': m.group(4)})
    tier, items = ar_items('Equinox')
    return save('equinox', {'fill_hr': n(fill.group(1)) if fill else None, 'bar': (n(bar.group(1)), n(bar.group(2))) if bar else None,
                            'upgrades': ups, 'challenges': ch, 'ar_tier': tier, 'ar': items})


def card_lines(o):
    L = []
    if o['bar'] and o['fill_hr']:
        cur, cap = o['bar']; mins = cap / o['fill_hr'] * 60
        L.append(f"TOP: spend the Equinox bar{' (it is full)' if cur >= cap else ''}. It refills in about {mins:.0f} minutes, so spend it every time you're on.")
    claim = [x for x in o['challenges'] if x['state'] and 'met' in x['state'].lower()]
    if claim: L.append(f"Claim {len(claim)} finished challenges: " + '; '.join(x['reward'] for x in claim) + '.')
    fillc = [x for x in o['challenges'] if 'fill rate' in x['reward'].lower() and x not in claim and 'Requires' not in x['task']]
    if fillc: L.append('Faster bar: ' + '; '.join(f"{x['task'].split('.')[0].split(' in a party')[0][:45]} ({x['progress']}) gives {x['reward'].replace(' Equinox Bar fill rate', ' fill')}" for x in fillc[:3]) + '.')
    lk = [u for u in o['upgrades'] if u['locked']]
    odd = [u['name'] for u in lk if u['progress'] == 'Done']
    if odd: L.append(f"Check in game: {', '.join(odd)} shows locked even though its unlock is done.")
    lk = [u for u in lk if u['progress'] != 'Done']
    if lk: L.append('Locked: ' + '; '.join(f"{u['name']} ({u['unlock'].split(',')[0][:55] if u['unlock'] else '?'}, {u['progress']})" for u in lk[:4]) + '.')
    up = [i for i in o['ar'] if i['group'].startswith('Upgrade more')]
    if up: L.append('AutoReview wants: ' + ', '.join(f"{i['label'].split(' (')[0]} {i['cur']} -> {i['goal']}" for i in up) + '.')
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
