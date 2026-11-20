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
    if o['on']: L.append(f"Lab is fine: all {o['on'][1]} bonuses on, {o['on'][2]} of {o['on'][3]} jewels on.")
    nos = [p for p, l, r in o['players'] if 'Souped' not in l]
    if nos: L.append(f"{', '.join(nos)} isn't souped up, so his lab range is lower.")
    blk = [x for x in o['rotation'] if x['need'] and x['state'] != 'Sold out'][:3]
    if blk: L.append('Coming in the shop but you are short: ' + '; '.join(f"{x['item']} on {x['date'][:5]} (need {x['need'][0]} more)" for x in blk) + '.')
    opn = [x for x in o['rotation'] if x['state'] == 'open' and not x['need'] and x['effect']][:3]
    if opn: L.append('You can buy these when they rotate in: ' + '; '.join(f"{x['item']} ({x['effect'][:50]})" for x in opn) + '.')
    return L


def char_lines(o, name): return []


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
