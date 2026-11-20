"""Lab planner (Autistocat Lab block). Bonuses/jewels on, players not souped up, chip + jewel rotation with what's missing."""
import re
from tbhelp import tb, n, save


def build():
    T = tb('lab'); m = T['Main frame']['text']
    on = re.search(r'Lab bonuses on\n(\d+) / (\d+)\nJewels on\n(\d+) / (\d+)\n(\d+) of (\d+) found', m)
    players = re.findall(r'\n(Autis\w+)\nLinked by ([^\n]+)\nRange\n([\d,]+)px', m)
    r = T['Chips And Jewels Rotation']['text']
    rot = []
    for wk in re.split(r'\n(?=\d\d/\d\d/\d{4} )', r):
        date = re.match(r'(\d\d/\d\d/\d{4})', wk)
        if not date: continue
        for nm, body in re.findall(r'\n([A-Z][A-Za-z ]+(?:chip|Chip|Processor|Motherboard|ite|Rhombol|Navette|Pyramite|Ulthurite)[A-Za-z ]*)\n(.*?)(?=\n[A-Z][A-Za-z ]+\n(?:Sold out|Found|\n)|\Z)', wk, re.S):
            need = re.findall(r'need ([\d.,]+[KMB]?) more', body)
            rot.append({'date': date.group(1), 'item': nm.strip(), 'state': 'Sold out' if 'Sold out' in body[:12] else 'Found' if 'Found' in body[:8] else 'open',
                        'effect': next((l for l in body.split('\n') if len(l) > 20), '')[:90], 'need': need})
    return save('lab', {'on': on.groups() if on else None, 'players': players, 'rotation': rot})


def card_lines(o):
    L = []
    if o['on']: L.append(f"Lab bonuses {o['on'][0]}/{o['on'][1]}, jewels {o['on'][2]}/{o['on'][3]} on, {o['on'][4]}/{o['on'][5]} jewels found.")
    nos = [p for p, l, r in o['players'] if 'Souped' not in l]
    if nos: L.append(f"Not souped up: {', '.join(nos)} (lower range). Souped up = linked by a buffed connector, my read.")
    blk = [x for x in o['rotation'] if x['need'] and x['state'] != 'Sold out']
    if blk: L.append('Rotation items short on materials: ' + '; '.join(f"{x['item']} ({x['date']}) needs {', '.join(x['need'])} more" for x in blk))
    opn = [x for x in o['rotation'] if x['state'] == 'open' and not x['need']]
    if opn: L.append('Buyable from rotation: ' + '; '.join(f"{x['item']} ({x['date']}): {x['effect']}" for x in opn[:4]))
    return L


def char_lines(o, name): return []


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
