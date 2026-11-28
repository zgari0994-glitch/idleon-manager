"""Goal + needs + weekly buffs + parks, recomputed every build (Zack 2026-11-25).
- goal(): the main account goal (Spelunking caves: next lore boss) with its status from this save.
- ranked(): biggest needs (model/priority.py) next to the goal; flags when a need outranks the goal (LAW 1: goal only switches when its
  target is hit or Zack OKs it).
- weekly(): this week's Ballot + Meritocracy bonus from the save, with what each one changes this week.
- personal(name): a character's own goal when one of their systems is a top need (impact warrants it).
- park(name, card): where each character sits, from current needs + Zack's standing rules. Nothing is a fixed list.
All numbers come from Toolbox's parser on the save (model/data.py).
"""
from data import load

D = load()
SPEL = D.system('spelunk')
VOTE = D.system('ballot')
CAVES = ['Pebble Cove', 'Sedimeadow', 'Rustbelt 03', 'Blushpit', 'Chucklemire', 'Lunarheim', 'Bizarrio', 'Glitter End', 'Scoutpost', 'Exiled Throne']
cl = lambda x: str(x).replace('_', ' ').replace(' @ ', '; ')


def _fmt(t, v):
    try: v = float(v)
    except (TypeError, ValueError): return t.replace('{', '').replace('}', '')
    return t.replace('{', f"{v:g}").replace('}', f"{1 + v / 100:.2f}")


def goal():
    bosses = SPEL['loreBosses']
    nxt = next((i for i, b in enumerate(bosses) if not b.get('defeated')), None)
    done = sum(1 for b in bosses if b.get('defeated'))
    g = {'name': 'Spelunking caves (lore bosses)', 'done': done, 'total': len(bosses), 'prereqs': [], 'levers': []}
    if nxt is None:
        g['next'] = None; g['status'] = 'all caves cleared: re-check the biggest blocker'; return g
    b = bosses[nxt]; cave = CAVES[nxt] if nxt < len(CAVES) else f"cave {nxt + 1}"
    g['next'] = cave
    g['unlocks'] = cl(b['description'])
    best = SPEL['bestCaveLevels'][nxt] if nxt < len(SPEL['bestCaveLevels']) else 0
    g['status'] = f"{done} of {len(bosses)} lore bosses beaten. Next: {cave} (boss at depth {b.get('foundAt')}, your best there is {best})"
    if best == 0:
        g['prereqs'].append({'who': 'Autistomatic', 'do': f"Get into {cave} (not entered yet). How the next cave opens isn't in the data: check in game and tell me"})
    else:
        g['prereqs'].append({'who': 'Autistomatic', 'do': f"Reach depth {b.get('foundAt')} in {cave} (best {best}) and beat its lore boss"})
    g['power'] = SPEL['power']['value']
    return g


def weekly():
    sb, sm = VOTE.get('selectedBonus') or {}, VOTE.get('selectedMeritocracyBonus') or {}
    ballot = _fmt(cl(sb.get('0', '')), sb.get('1'))
    merit = _fmt(cl(sm.get('description', '')), sm.get('bonus'))
    notes = []
    both = (ballot + ' ' + merit).lower()
    if 'monument' in both: notes.append(('Autistachio', 'Monument week: claim and restart the monuments and keep him parked there', 'monument rewards are multiplied this week'))
    if 'divinity' in both: notes.append(('everyone', 'Divinity week: put spare characters on the Divinity platform', 'Pulse: end gamers sweat Divinity week (talent levels, class EXP, coral)'))
    if 'statue' in both: notes.append(('Autistocat', 'Statue week: push Emperor showdowns now', 'Pulse 2026-11-16: next showdowns are realistic in statue week'))
    if 'stamina' in both or 'overstim' in both: notes.append(('Autistomatic', 'Stamina week: stack overstim before a big amber run', 'Pulse 2026-10-15'))
    if 'artifact' in both or 'sailing' in both: notes.append(('Autisticles', 'Sailing bonus week: keep every boat on long trips and claim on time', 'ballot boosts artifact finds this week'))
    from data import carried
    c = carried(D.stamp).get('serverVars')
    tag = f" [votes from save {c}: phone save has none, confirm in game if a new week started]" if c else ''
    if not sb and not sm:
        tag = ' [NO vote data in this save: check the ballot in game]'
    return {'ballot': f"{ballot} (x{round(VOTE.get('voteMulti') or 0, 2)}){tag}", 'merit': f"{merit} (x{round(VOTE.get('meritocracyMult') or 0, 2)}){tag}", 'notes': notes}


_RANK = None


def ranked():
    global _RANK
    if _RANK is None:
        import priority as P
        _RANK = [{'section': x['section'], 'owners': x['owners'], 'why': x['why']} for x in P.build().get('needs', [])[:5]]
    return _RANK


def personal(name):
    """A character's own goal when a top need they own isn't the account goal."""
    for i, x in enumerate(ranked()[:3]):
        if name in x['owners'] and 'Spelunking' not in x['section']:
            return {'do': f"Your goal: {x['section']}", 'why': f"#{i + 1} biggest account need: {x['why']}", 'sub': []}
    return None


def _div_points_needed():
    kid = D.get('account.coralReef.coralKidUpgrades', True)
    pts = D.get('account.divinity', True).get('divinityPoints') or 0
    nxt = sorted([k for k in kid if k.get('cost') and k.get('level', 0) < 1], key=lambda k: k['cost'])
    return (nxt[0], pts) if nxt and pts < nxt[0]['cost'] else (None, pts)


_IN_PARK = set()


def park(name, card_park=''):
    """(where, why). Weekly override, the Divinity-points rule, then the AFK engine's chosen line (model/afk.py, from jobs.yaml +
    plans.yaml + Laws). No character is special-cased here (Zack 2026-11-27 clean-up)."""
    for who, do, why in weekly()['notes']:
        if who == name and 'parked' in do: return ('Monument (Hole) this week', why)
    if name == 'Autistronaut':
        k, pts = _div_points_needed()
        if k: return ('W5 Divinity altar, Mindful style', f"divinity points {pts:,.0f}, next Coral Kid upgrade needs {k['cost']:,.0f} (Pulse: Mindful is the best style)")
    if name not in _IN_PARK:
        _IN_PARK.add(name)
        try:
            import afk as A
            _r, c, _s, _x = A.pick(name)
            if c: return (c.get('where') or ' / '.join(x for x in (c.get('world'), c.get('map'), c.get('mob')) if x) or (f"Spelunking cave {c['cave']}" if c.get('cave') else 'spot = GAP'), c.get('why', '?'))
        except Exception:
            pass
        finally:
            _IN_PARK.discard(name)
    return (f"Spelunking: {goal().get('next') or 'next cave'}", f"account goal: {goal().get('next') or 'Spelunking'} (Law 3: no personal goal)")
