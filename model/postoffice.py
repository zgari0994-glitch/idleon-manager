"""Post Office boxes per character (every_character). AutoReview Post Office targets name the character + box."""
from tbhelp import ar_items, save


def build():
    tier, items = ar_items('Post Office')
    per = {}
    for i in items:
        if ':' in i['label'] and i['label'].startswith('Autis'):
            c, box = i['label'].split(':', 1); per.setdefault(c.strip(), []).append((box.strip(), i['cur'], i['goal']))
    return save('postoffice', {'ar_tier': tier, 'per': per})


def char_lines(o, name):
    return [f"Post Office: get {b} to {g} (it's at {c})." for b, c, g in o['per'].get(name, [])[:2]]


if __name__ == '__main__':
    o = build()
    for k in o['per']: print(k, char_lines(o, k))
