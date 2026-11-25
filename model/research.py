"""Research planner (Autistotle). Level, next Posty Note, grid points, observations + daily rolls."""
import re
from tbhelp import tb, ar_items, save


def build():
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py)
    from data import load
    D = load(); R = D.system('research')
    best = max(D.characters, key=lambda c: (c.get('skillsInfo') or {}).get('research', {}).get('level', 0))
    sk = best['skillsInfo']['research']
    posty = [(p['description'].replace('_', ' '), p['unlockLevel']) for p in R['postyNotes'] if not p['unlocked']]
    return save('research', {'level': f"{sk['level']} ({best['name']})", 'to_level': f"{(sk['expReq'] - sk['exp']) / max(sk['expReq'], 1) * 100:.0f}% of the level left",
                             'grid': f"{R['gridPTSavailable']} free of {R['gridPTSearned']}", 'obs': sum(1 for x in R['observations'] if x.get('found')),
                             'rolls': R['dailyRollsLeft'], 'posty': [(f"Posty Note", lv, d) for d, lv in sorted(posty, key=lambda x: x[1])[:2]],
                             'grid_free': R['gridPTSavailable'], 'next_unlock_lv': R.get('nextUnlockResearchLv')})

def card_lines(o):
    L = [f"Research is level {o['level'].split(' ')[0]}, next level in {o['to_level']}."]
    if o['posty']: L.append(f"Level {o['posty'][0][1]} unlocks {o['posty'][0][0]}: {o['posty'][0][2].split('!')[0].lower()}.")
    if o['rolls']: L.append(f"Use today's {o['rolls']} observation rolls ({o['obs']} found).")
    if o.get('grid_free'): L.append(f"Spend {o['grid_free']} free research grid points.")
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
