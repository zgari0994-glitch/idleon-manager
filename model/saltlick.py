"""Salt Lick planner (Autistopher). Levels buyable now per upgrade (Toolbox 'Can buy now')."""
import re
from tbhelp import tb, ar_items, save

def build():
    t = tb('saltlick')['_page']['text']
    ups = []
    for m in re.finditer(r'\n([^\n]{15,140})\nLv (\d+) / (\d+)\n(.*?)(?=\n[^\n]{15,140}\nLv \d+ / |\nDiscord|\Z)', t, re.S):
        b = m.group(4); buy = re.search(r'Can buy now\n\+(\d+) LV', b)
        ups.append({'desc': m.group(1), 'lv': int(m.group(2)), 'max': int(m.group(3)), 'buy': int(buy.group(1)) if buy else 0})
    tier, items = ar_items('Salt Lick')
    return save('saltlick', {'upgrades': ups, 'ar_tier': tier, 'ar': items})

def card_lines(o):
    buy = [u for u in o['upgrades'] if u['buy']]
    L = ['TOP: buy now: ' + '; '.join(f"{re.split(r'\. ', u['desc'])[0][:50]} {u['lv']} -> {u['lv'] + u['buy']} (+{u['buy']})" for u in buy)] if buy else []
    left = [u for u in o['upgrades'] if u['lv'] < u['max']]
    L.append(f"AutoReview tier {o['ar_tier']}: to max " + ', '.join(f"{re.split(r'\. ', u['desc'])[0][:40]} {u['lv']}/{u['max']}" for u in left) + '. Toolbox should show the new levels after buying.')
    return L

def refinery_line(o):
    u = next((u for u in o['upgrades'] if 'Refinery Speed' in u['desc']), None)
    return f"Salt Lick Refinery Speed {u['lv']}/{u['max']}" + (f": +{u['buy']} buyable now (Autistopher)" if u['buy'] else '') if u else None

if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
    print(refinery_line(o))
