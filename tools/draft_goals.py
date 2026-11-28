"""Auto-draft the per-system GOAL block (docs/planners.md standard) for every brain/systems/*.md that has none.
pending_changes L7, built 2026-11-28. Reads tools/lookup.py output per system (creator claims, AutoReview, owner).
Drafts are marked status: DRAFT + auto: true, never approved, never read as Zack's plan. Systems without creator
coverage get "my_read" rungs and a line in brain/goal_gaps.md (the standard's "logged gap").
Usage: python3 tools/draft_goals.py [system ...]   (no args = every system missing a GOAL block)"""
import json, re, subprocess, sys, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYS = ROOT / 'brain' / 'systems'
TODAY = dt.date.today().isoformat()
CREATORS = {'Griffy': 0, 'Pulse': 1, 'Nocturne': 1}
CLAIM = re.compile(r'^\s+(\S+)( \(fan src\))? (\d{4}-\d{2}-\d{2})( OLD)? ([a-z_]+): (\[[A-F S]\] )?(.+?) \[([\w-]+) ([\d:]+)\]$')
sys.path.insert(0, str(ROOT / 'model'))


def lookup(name):
    r = subprocess.run([sys.executable, str(ROOT / 'tools' / 'lookup.py'), name], capture_output=True, text=True, timeout=120)
    return r.stdout


def parse(txt):
    head = txt.splitlines()[0] if txt else ''
    own = (re.search(r'owner (.+)$', head) or [None, ''])[1].strip()
    sec, ar, claims, data = None, [], [], []
    for ln in txt.splitlines():
        m = re.match(r'## (\d)\.', ln)
        if m: sec = m.group(1); continue
        if sec == '1' and ln.strip() and not ln.startswith('path:'): data.append(ln.strip())
        if sec == '2':
            m = re.match(r'\s+\[(.+?)\] (.+?)(?: \((.+?) -> (.+?)\))?$', ln)
            if m and 'TRUNCATED' not in ln: ar.append({'sec': m.group(1), 'label': m.group(2), 'cur': m.group(3), 'goal': m.group(4)})
        if sec == '3':
            m = CLAIM.match(ln)
            if m: claims.append({'who': m.group(1), 'fan': bool(m.group(2)), 'date': m.group(3), 'old': bool(m.group(4)), 'type': m.group(5),
                                 'tier': (m.group(6) or '').strip('[] '), 'say': m.group(7), 'vid': m.group(8), 't': m.group(9)})
    return own, data, ar, claims


def q(s):
    return json.dumps(str(s))


def checked_daily():
    try:
        import syscheck, syscheck2
        return set(syscheck.CHECKS) | set(syscheck.ALIAS) | set(syscheck2.CHECKS2) | set(syscheck2.ROUTE.values())
    except Exception:
        return set()


def block(name, own, data, ar, claims, daily):
    junk = re.compile(r'^(commenter|chat|viewer|someone|he agrees|people)', re.I)
    good = [c for c in claims if c['who'] in CREATORS and not c['old'] and c['type'] in ('priority', 'target', 'how_to', 'blocker') and not junk.match(c['say'])]
    if not good:   # fall back to graded opinions only when nothing actionable exists
        good = [c for c in claims if c['who'] in CREATORS and not c['old'] and c['tier'] and not junk.match(c['say'])]
    good.sort(key=lambda c: (CREATORS[c['who']], c['type'] not in ('priority', 'target'), c['date']), reverse=False)
    # newest first inside the same creator rank
    good.sort(key=lambda c: c['date'], reverse=True); good.sort(key=lambda c: (CREATORS[c['who']], c['type'] not in ('priority', 'target')))
    rungs = [{'target': c['say'][:140], 'source': c['who'], 'date': c['date'], 'vid': f"{c['vid']} {c['t']}"} for c in good[:3]]
    num = [a for a in ar if a['goal'] not in (None, '', '∞')]
    if len(rungs) < 3:
        for a in (num or ar)[:3 - len(rungs)]:
            rungs.append({'target': a['label'][:140] + (f" ({a['cur']} -> {a['goal']})" if a['goal'] else ''), 'source': 'Toolbox', 'date': TODAY, 'vid': 'AutoReview'})
    cov = 'sourced' if any(r['source'] in CREATORS for r in rungs) and len([r for r in rungs if r['source'] in CREATORS]) >= 2 else \
          'partial' if rungs else 'none'
    if not rungs:
        rungs = [{'target': f"my read: read {name} state every pull and push its cheapest open upgrade", 'source': 'my_read', 'date': TODAY, 'vid': ''}]
    goal = (f"{rungs[0]['target'][:110]}" if rungs[0]['source'] != 'my_read' else f"my read: keep {name.replace('_', ' ')} moving; no creator goal yet")
    feeds = any(re.search(r'spelunk|\bpow\b', c['say'], re.I) for c in claims[:20])
    obj = next(({'now': a['cur'], 'target': a['goal']} for a in num), {'now': None, 'target': None})
    who = own if own and 'unassigned' not in own else 'UNASSIGNED'
    cad = 'daily' if name in daily else 'weekly'
    L = ['<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->',
         f'<!-- DRAFT auto {TODAY} (tools/draft_goals.py from lookup: creator claims + AutoReview): not approved, not in the pipeline -->',
         '```yaml', 'status: DRAFT', 'auto: true', f"role: {'feeder' if feeds else 'independent'}", f"goal: {q(goal)}", f'coverage: {cov}', 'ladder:']
    for i, r in enumerate(rungs, 1):
        L.append(f"  - {{tier: {i}, target: {q(r['target'])}, source: {q(r['source'])}, date: {q(r['date'])}}}" + (f"   # {r['vid']}" if r['vid'] else ''))
    L += [f"objective: {{rung: 1, now: {q(obj['now']) if obj['now'] is not None else 'null'}, target: {q(obj['target']) if obj['target'] is not None else 'null'}, eta_days: null}}",
          f"check: {{cadence: {cad}, who: {q(who)}, look_at: {q('card line (syscheck)' if cad == 'daily' else f'python3 tools/lookup.py {name}')}}}",
          'buffs: []   # only filled for systems behind / needing a push',
          'triggers: []', 'stall: {pulls_no_progress: 3, eta_over_days: 30}', 'tasks:',
          f"  - {{do: {q(rungs[0]['target'][:120])}, stat: \"\", gain_pct: null, unblocks: [], source: {q(rungs[0]['source'])}, active_min: null, wait_hr: null, cost: null, urgent: false}}"]
    if data: L.append(f"# data now: {'; '.join(data[:2])[:200]}")
    if cov != 'sourced': L.append(f"# gap: {'no creator coverage' if cov == 'none' else 'thin creator coverage'}; rungs from AutoReview / my read (logged in brain/goal_gaps.md)")
    L += ['```', '<!-- GOAL:END -->']
    return '\n'.join(L), cov


def main(names):
    daily = checked_daily()
    files = [SYS / f'{n}.md' for n in names] if names else sorted(p for p in SYS.glob('*.md') if not p.name.startswith('_') and 'GOAL:START' not in p.read_text())
    gaps, done = [], []
    for p in files:
        name = p.stem; t = p.read_text()
        if 'GOAL:START' in t and not names: continue
        own, data, ar, claims = parse(lookup(name))
        b, cov = block(name, own, data, ar, claims, daily)
        if 'GOAL:START' in t:
            t = re.sub(r'<!-- GOAL:START.*?<!-- GOAL:END -->', lambda _m: b, t, flags=re.S)
        elif '<!-- AUTO:END -->' in t:
            t = t.replace('<!-- AUTO:END -->', '<!-- AUTO:END -->\n\n' + b, 1)
        else:
            t = t.rstrip() + '\n\n' + b + '\n'
        p.write_text(t); done.append((name, cov))
        if cov != 'sourced': gaps.append((name, cov, own))
    gp = ROOT / 'brain' / 'goal_gaps.md'
    keep = gp.read_text() if gp.exists() else '# GOAL gaps (systems whose ladder is not creator-sourced)\nEach needs Griffy > Pulse = Nocturne guidance; until then rungs are AutoReview / my read.\n'
    keep += f"\n## {TODAY} auto-drafts ({len(gaps)} of {len(done)})\n" + '\n'.join(f"- {n}: {c} (owner {o or 'UNASSIGNED'})" for n, c, o in gaps) + '\n'
    gp.write_text(keep)
    print(f"drafted {len(done)}: " + ', '.join(f"{n}={c}" for n, c in done))


if __name__ == '__main__':
    main(sys.argv[1:])
