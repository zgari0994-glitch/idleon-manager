"""Armor Sets planner (Autistastic). Incomplete sets, parts owned, AutoReview missing parts per set."""
import re
from tbhelp import tb, ar_items, save

def build():
    t = tb('armor')['_page']['text']
    done = re.search(r'Completed sets\n(\d+) / (\d+)', t)
    sets = [{'set': a, 'bonus': b, 'parts': c} for a, b, c in re.findall(r'\n([A-Z][a-z]+ set)\n\n([^\n]+)\n\nParts owned\n([^\n]+)', t)]
    tier, items = ar_items('Armor Sets')
    return save('armor', {'done': done.groups() if done else None, 'sets': sets, 'ar_tier': tier, 'ar': items})

def card_lines(o):
    L = [f"Armor sets {o['done'][0]}/{o['done'][1]} (AutoReview tier {o['ar_tier']})."]
    order = sorted(o['sets'], key=lambda s: -eval(s['parts'].replace(' ', '')) if '/' in s['parts'] else 0)
    for s in order:
        miss = [i['label'] for i in o['ar'] if i['group'].startswith(s['set'].split()[0]) and i.get('goal') == '1' and i.get('cur') == '0']
        L.append(f"{s['set']} {s['parts']} ({s['bonus']}). Missing: " + (', '.join(miss) if miss else 'see Toolbox Parts tab'))
    return L

if __name__ == '__main__':
    for l in card_lines(build()): print(l)
