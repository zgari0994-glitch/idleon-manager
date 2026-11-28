"""Main account goal = the biggest need from the review each pull (Zack 2026-11-27, Law 1 v2).
- Candidate goal = #1 need in model/priority.py (score, owners, why).
- The current goal stays until its target is hit OR another need outranks it on 2 pulls in a row.
  Then the card shows "switch goal to X?" and Zack confirms. Nothing switches silently.
- Spelunking's measurable target = the next lore boss (not "every boss"). When it falls, re-check from the review.
State: state/goal_state.json (written only by record(), i.e. on a pull).
"""
import json
from pathlib import Path
from data import load

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / 'state' / 'goal_state.json'
LEAD_PULLS = 2
D = load()
CAVES = ['Pebble Cove', 'Sedimeadow', 'Rustbelt 03', 'Blushpit', 'Chucklemire', 'Lunarheim', 'Bizarrio', 'Glitter End', 'Scoutpost', 'Exiled Throne']


def _needs():
    import priority as P
    return P.build().get('needs', [])


def _state():
    try: return json.loads(STATE.read_text())
    except Exception: return {'goal': 'Spelunking', 'lead': {}, 'last_save': None, 'confirmed': 'Zack 2026-11-27 (still #1 need)'}


def target(section):
    """Measurable target + done flag for a goal section."""
    if section == 'Spelunking':
        S = D.system('spelunk'); b = S['loreBosses']
        nxt = next((i for i, x in enumerate(b) if not x.get('defeated')), None)
        if nxt is None: return ('all lore bosses beaten', True)
        best = S['bestCaveLevels'][nxt] if nxt < len(S['bestCaveLevels']) else 0
        done = sum(1 for x in b if x.get('defeated'))
        nc = S['discoveries'][nxt] if nxt < len(S['discoveries']) else []
        need = min([x['powerReq'] for x in nc if not x.get('acquired')] or [0])
        pw = S['power']['value']
        how = (f"cave {nxt + 1} not entered yet" if best == 0 else f"best depth {best}") + (f"; next unbroken object there needs POW {need:,.0f} (you have {pw:,.0f})" if need else '')
        return (f"lore boss {done + 1}/10 in cave {nxt + 1} (boss at depth {b[nxt].get('foundAt')}; {how}). "
                f"Unlocks: {b[nxt]['description'].replace('_', ' ').replace(' @ ', '; ')}", False)
    n = next((x for x in _needs() if x['section'] == section), None)
    if not n: return (f"{section}: not behind anymore", True)
    return (f"{section} {n.get('cur')} -> {n.get('goal')}", False)


def status(st=None):
    st = st or _state()
    needs = _needs()
    g = st['goal']
    gn = next((x for x in needs if x['section'] == g), None)
    tgt, hit = target(g)
    top = needs[0] if needs else None
    out = {'goal': g, 'target': tgt, 'hit': hit, 'score': gn['score'] if gn else 0, 'owners': gn['owners'] if gn else [],
           'why': gn['why'] if gn else 'not in the needs list anymore', 'prompt': None,
           'runners_up': [f"{x['section']} {x['score']}" for x in needs[:4] if x['section'] != g][:3]}
    if hit or not gn:
        if top: out['prompt'] = f"goal target hit: switch goal to {top['section']} (score {top['score']}: {top['why']})?"
    else:
        for sec, n in st.get('lead', {}).items():
            if n >= LEAD_PULLS:
                x = next((y for y in needs if y['section'] == sec), None)
                if x: out['prompt'] = f"{sec} has outranked {g} for {n} pulls ({x['score']} vs {out['score']}): switch goal?"
    return out


def record(save):
    st = _state()
    if st.get('last_save') == save: return st
    needs = _needs(); g = st['goal']
    gs = next((x['score'] for x in needs if x['section'] == g), -1)
    lead = {}
    for x in needs:
        if x['section'] != g and x['score'] > gs: lead[x['section']] = st.get('lead', {}).get(x['section'], 0) + 1
    st['lead'] = lead; st['last_save'] = save
    STATE.write_text(json.dumps(st, indent=1)); return st


def confirm(section):
    """Zack says 'switch goal to X' (tools/afk_pin.py goal X)."""
    st = _state(); st.update(goal=section, lead={}, confirmed=f"Zack, save {D.stamp}")
    STATE.write_text(json.dumps(st, indent=1)); return st


def project_line():
    s = status()
    return f"Main goal = biggest account need from the review each pull (now {s['goal']}: {s['target']})."
