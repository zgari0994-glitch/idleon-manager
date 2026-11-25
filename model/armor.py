"""Armor Sets planner (Autistastic). Incomplete sets, parts owned, AutoReview missing parts per set."""
import re
from tbhelp import tb, ar_items, save

def build():
    # Zack 2026-11-25: Toolbox parser (sets) + AutoReview (missing parts)
    from data import load
    A = load().system('armor_sets')
    tier, items = ar_items('Armor Sets')
    sets = []
    for s in A['sets']:
        nm = s['setName'].replace('_', ' ').title().replace('Set', 'set')
        grp = [i for i in items if i['group'].lower().startswith(nm.split()[0].lower())]
        have = sum(1 for i in grp if i.get('goal') == '✔' or (str(i.get('cur')) not in ('0', '', 'None') and str(i.get('cur')) == str(i.get('goal'))))
        sets.append({'set': nm, 'bonus': s['description'].replace('_', ' '), 'parts': f"{have} / {len(grp)}" if grp else '?', 'done': s.get('unlocked')})
    comp = [i for i in items if i['group'] == 'Completed Set Bonuses']
    done = (sum(1 for i in comp if str(i.get('cur')) == str(i.get('goal')) or i.get('goal') == '✔'), len(comp) or len(sets))
    sets = [s for s in sets if s['parts'] != '?']   # only sets AutoReview lists parts for (the unfinished ones)
    return save('armor', {'done': done, 'sets': sets, 'ar_tier': tier, 'ar': items})

def card_lines(o):
    L = [f"{o['done'][0]} of {o['done'][1]} armor sets done."]
    for s in sorted(o['sets'], key=lambda s: -eval(s['parts'].replace(' ', '')) if '/' in s['parts'] else 0):
        miss = [i['label'] for i in o['ar'] if i['group'].startswith(s['set'].split()[0]) and i.get('goal') == '1' and i.get('cur') == '0']
        more = f" and {len(miss) - 3} more" if len(miss) > 3 else ''
        L.append(f"{s['set']} ({s['parts']} parts) gives {s['bonus'][0].lower() + s['bonus'][1:]}. Still need {', '.join(miss[:3])}{more}." if miss else f"{s['set']} ({s['parts']} parts).")
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
