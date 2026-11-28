"""Trophies (Zack 2026-11-28): owned from Toolbox gallery.allTrophies (isAcquired), how-to from brain/trophies.yaml.
Gallery card: have / not yet + how to get. Minigame lines: '<Trophy>: have / not yet'."""
from pathlib import Path
import yaml
from data import load

ROOT = Path(__file__).resolve().parent.parent
HOW = yaml.safe_load(open(ROOT / 'brain' / 'trophies.yaml'))


def status(D=None):
    D = D or load()
    G = D.system('gallery', allow_empty=True)
    hs = {x.get('name'): x for x in (D.account.get('highscores') or {}).get('minigameHighscores') or []}
    out = []
    for t in G.get('allTrophies') or []:
        h = HOW['trophies'].get(t.get('rawName'), {})
        best = (hs.get(h['minigame']) or {}).get('score') if h.get('minigame') else None
        out.append({'raw': t.get('rawName'), 'name': str(t.get('displayName')).replace('_', ' '), 'have': bool(t.get('isAcquired')),
                    'how': h.get('how', 'how-to not mapped yet'), 'retired': h.get('retired', False),
                    'minigame': h.get('minigame'), 'best': best, 'need': h.get('need')})
    return out


def one(t):
    if t['have']:
        return f"{t['name']}: have"
    s = f"{t['name']}: not yet, {t['how']}"
    if t.get('best') is not None and t.get('need'):
        s += f" (your best {t['best']}" + (f", need {t['need']}" if t.get('need') else '') + ')'
    return s


def gallery_lines(D=None):
    S = status(D)
    have = [t for t in S if t['have']]
    todo = [t for t in S if not t['have'] and not t['retired']]
    L = [f"Trophies: have {len(have)}/{len(S)}, {len(todo)} obtainable not yet (how-to: {HOW['source']})"]
    L += ['  ' + one(t) for t in todo]
    return L


def minigame_line(key, D=None):
    ts = [t for t in status(D) if t.get('minigame') == key]
    return '; '.join(one(t) for t in ts) if ts else None


if __name__ == '__main__':
    print('\n'.join(gallery_lines()))
