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
    L = [f"{o['done'][0]} of {o['done'][1]} armor sets done."]
    for s in sorted(o['sets'], key=lambda s: -eval(s['parts'].replace(' ', '')) if '/' in s['parts'] else 0):
        miss = [i['label'] for i in o['ar'] if i['group'].startswith(s['set'].split()[0]) and i.get('goal') == '1' and i.get('cur') == '0']
        more = f" and {len(miss) - 3} more" if len(miss) > 3 else ''
        L.append(f"{s['set']} ({s['parts']} parts) gives {s['bonus'][0].lower() + s['bonus'][1:]}. Still need {', '.join(miss[:3])}{more}." if miss else f"{s['set']} ({s['parts']} parts).")
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
