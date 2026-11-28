#!/usr/bin/env python3
"""Weekly boss: parse the community sheet 'Weekly Boss Rotations' (Drive id 1z1P2ouvYhe2pryWoF0kIQE7QichYpJt1GaPPos-e-aw,
by roronoa_zoro93 / DiamondDoge, 11-char rotations) into brain/weekly_boss.yaml (current + next week).
Refresh: Drive search_files(query="title = 'Weekly Boss Rotations'", snippetVerbosity=MAX_ALLOWED) -> saved dump file,
then: python3 tools/weekly_boss.py <dump file>. Reads the Discord tab (pre-formatted current + next week).
Week = Thu 00:00 GMT to next Thu. Card line: tools/weekly_boss.py --today."""
import sys, re, json, yaml, datetime as dt, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; OUT = ROOT / 'brain' / 'weekly_boss.yaml'

def flat(block):  # "3 2 3 - 2 3 2 (FR)" lines -> "323232 FR | ..."
    return ' | '.join(re.sub(r'[^0-9]', '', l.replace('(FR)', '')) + (' FR' if '(FR)' in l else '') for l in block.strip().splitlines() if l.strip())

def parse(text):
    try: text = json.loads(text)['files'][0]['contentSnippet']
    except Exception: pass
    i = text.find('# Discord'); d = text[i:] if i >= 0 else text
    weeks = {}
    for m in re.finditer(r'\*\*__([^_*\n]+?)__\*\*\s*\n\*\*(\d\d \w\w\w \d\d) - (\d\d \w\w\w \d\d)\*\*(.*?)Character requirements\s*\n```(.*?)```', d, re.S):
        name, a, b, body, req = m.groups()
        blocks = re.findall(r'```(.*?)```', body, re.S)
        bon = re.search(r'Trophies - (\d+) \| Class EXP - (\d+)% \| Damage - (\d+)%', body)
        start = dt.datetime.strptime(a, '%d %b %y').date().isoformat()
        weeks[start] = {'boss': name, 'start': start, 'end': dt.datetime.strptime(b, '%d %b %y').date().isoformat(),
            'skulls5': flat(blocks[0]), 'trophy': flat(blocks[1]), 'skulls5_raw': blocks[0].strip(), 'trophy_raw': blocks[1].strip(),
            'trophies': int(bon[1]) if bon else None, 'class_exp_pct': int(bon[2]) if bon else None, 'dmg_pct': int(bon[3]) if bon else None,
            'requirements': [l.strip() for l in req.strip().splitlines() if l.strip()]}
    return weeks

def today_line(now=None):
    if not OUT.exists(): return "Weekly boss: no rotation stored. Refresh: see tools/weekly_boss.py"
    W = yaml.safe_load(open(OUT)) or {}; now = now or dt.datetime.now(dt.timezone.utc).date()
    cur = [w for w in W.get('weeks', {}).values() if w['start'] <= now.isoformat() < w['end']]
    if not cur: return f"Weekly boss: stored rotation is stale (fetched {W.get('fetched')}), refresh the sheet before the run"
    w = cur[0]   # Zack 2026-11-28: done-state not readable, so remind daily with both runs until the boss changes
    s = (f"Do the weekly boss today: {w['boss']} ({w['start']} to {w['end']}, resets 00:00 GMT). "
         f"5 Skulls run: {w['skulls5']}. Trophy run: {w['trophy']} (trophies {w['trophies']}, class EXP {w['class_exp_pct']}%, dmg {w['dmg_pct']}%). "
         f"Requirements: {'; '.join(w['requirements'])}")
    nxt = [x for x in W['weeks'].values() if x['start'] == w['end']]
    return s + (f". Next week: {nxt[0]['boss']}" if nxt else '. Next week not stored yet: refresh the sheet')

if __name__ == '__main__':
    if sys.argv[1:] == ['--today']: print(today_line()); sys.exit()
    weeks = parse(open(sys.argv[1], encoding='utf-8').read())
    if not weeks: sys.exit('no weeks parsed (Discord tab format changed?)')
    old = (yaml.safe_load(open(OUT)) or {}).get('weeks', {}) if OUT.exists() else {}
    old.update(weeks)
    yaml.safe_dump({'source': 'Weekly Boss Rotations (Google Sheet, fan source: roronoa_zoro93 / DiamondDoge sim)', 'sheet_id': '1z1P2ouvYhe2pryWoF0kIQE7QichYpJt1GaPPos-e-aw',
                    'fetched': dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%MZ'), 'weeks': dict(sorted(old.items())[-6:])}, open(OUT, 'w'), sort_keys=False, allow_unicode=True, width=200)
    print('stored', ', '.join(f"{k} {v['boss']}" for k, v in weeks.items()))
