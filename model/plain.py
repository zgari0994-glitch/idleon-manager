"""Plain-English cleanup for every card line (Zack 2026-11-19: read like someone talking, not tooltips or notes to self).
Rules: round long numbers, short big numbers (89K, 1.3B), no sci notation, no internal tags/timestamps/design notes,
creator lines as 'Griffy: ...', 'Push:' as 'Next goal:', cap long lists."""
import re

UNITS = [(1e18, 'QQ'), (1e15, 'Q'), (1e12, 'T'), (1e9, 'B'), (1e6, 'M'), (1e3, 'K')]


def short(v):
    if abs(v) >= 1e21: return f"{v:.1e}".replace('e+', 'e')
    for d, u in UNITS:
        if abs(v) >= d:
            x = v / d
            return (f"{x:.0f}" if x >= 100 else f"{x:.1f}".rstrip('0').rstrip('.')) + u
    return f"{v:,.0f}" if abs(v) >= 100 else (f"{v:.1f}".rstrip('0').rstrip('.') if v != int(v) else f"{int(v)}")


def _sci(m): return short(float(m.group(0)))


def _num(m):
    s = m.group(0); v = float(s.replace(',', ''))
    if '.' in s:
        if v >= 100: return short(v) if v >= 100000 else f"{round(v):,}"
        return f"{v:.1f}".rstrip('0').rstrip('.')
    return short(v) if v >= 100000 else s


WHO = {'griffybit': 'Griffy', 'Griffy': 'Griffy', 'pulseidle': 'Pulse', 'Pulse': 'Pulse', 'nocturnegaming': 'Nocturne', 'Nocturne': 'Nocturne'}


def plain(t):
    if not isinstance(t, str): return t
    # creator lines: "CREATORS: text [tag=x] (Griffy 2026-09 @01:12:23)" -> "Griffy: text"
    m = re.match(r'^(.*?)CREATORS: (.*?)\s*(?:\[[^\]]*\]\s*)*\((\w+)[^)]*@[\d:]+\)\s*$', t)
    if m: t = f"{m.group(1)}{WHO.get(m.group(3), m.group(3))}: {m.group(2)}"
    t = re.sub(r'\s*\[[\w ./%-]+=[^\]]*\]', '', t)                     # [displayed_sprinkler=0/7]
    t = re.sub(r'\s*\(\w+ \d{4}-\d\d @[\d:]+\)', '', t)                # (Griffy 2026-09 @01:12:23)
    t = re.sub(r'\s*\[s:[^\]]*\]', '', t)
    t = re.sub(r'(^|: )Push: ', r'\1Next goal: ', t)
    m2 = re.match(r'^Next goal: ([^:]{3,40}): .*?(\S+ -> \S+)$', t)
    if m2: t = f"Next goal: {m2.group(1)} {m2.group(2)}"
    t = re.sub(r'\((Griffy|Pulse|Nocturne)[^)]*?\d{4}-\d\d[^)]*\)', r'(\1)', t)
    t = re.sub(r'\b(Griffy|Pulse|Nocturne) \d{4}-\d\d\b', r'\1', t)
    t = re.sub(r'\b\d+(?:\.\d+)?e[+-]?\d+\b', _sci, t)                 # 1.3e+09 -> 1.3B
    t = re.sub(r'(?<![\w.])\d{1,3}(?:,\d{3})+(?:\.\d+)?(?![\w.])|(?<![\w.,])\d+\.\d{2,}(?![\w.])', _num, t)
    t = re.sub(r'\+[\d.,]+[KMBTQ]* \((\+[\d.]+%)\)', r'\1', t)    # +6,733 (+2.5%) -> +2.5%
    parts = t.split('; ')
    if len(parts) > 6: t = '; '.join(parts[:5]) + f"; and {len(parts) - 5} more"
    return t.strip()


JARGON = re.compile(r'breakdown|multi\b|\bAR\b|AutoReview|\btier \d|[a-z][A-Z]\w*_|\w+_\w+|\[|\]|->|\bcur\b|\bgoal=|\bTODO\b|\bNone\b', re.I)
RAW = re.compile(r'\w+_\w+|\{|\}|\bNone\b')
_LOG = {}

def _flag(x):
    """lines that still read like tooltip/AutoReview talk: drop raw labels, log the rest for the next card build"""
    if JARGON.search(x):
        k = x.split(' · ')[0] if ' · ' in x else ' '.join(x.split()[:4])
        _LOG.setdefault(k.strip()[:80], [0, x.strip()[:160]])[0] += 1
    return bool(RAW.search(x))

def write_log():
    """append new flagged lines to sources/findings/wording.md (dedup). Fixed at source next card build, no extra pulls."""
    from pathlib import Path
    f = Path(__file__).resolve().parent.parent / 'sources' / 'findings' / 'wording.md'
    head = '# Wording: spots to check next card build\nOne line per spot that keeps producing jargon/padding (count = lines this build, example). Raw labels were dropped from cards. Fix at the planner, then delete the line. Rewritten each build.\n\n'
    rows = sorted(_LOG.items(), key=lambda kv: -kv[1][0])
    f.write_text(head + ''.join(f'- {k} ({c}x): {ex}\n' for k, (c, ex) in rows))
    return len(rows)

def clean(o):
    """apply plain() to every string in a nested structure; drop internal design-note lines"""
    if isinstance(o, str): return plain(o)
    if isinstance(o, list):
        o = [x for x in o if not (isinstance(x, str) and _flag(plain(x)))]
        return [clean(x) for x in o if not (isinstance(x, str) and (re.match(r'^\((Zack|Every character|Equipped per|Zack:)', x) or re.match(r'^\(.*\)$', x.strip())))]
    if isinstance(o, dict): return {k: clean(v) if k not in ('src', 'block', 'name') else v for k, v in o.items()}
    return o
