"""Research planner (Autistotle). Level, next Posty Note, grid points, observations + daily rolls."""
import re
from tbhelp import tb, ar_items, save


def build():
    T = tb('research'); g = T['Grid']['text']; ob = T['Observations']['text']; pn = T['Posty Notes']['text']
    f = lambda t, k: (re.search(re.escape(k) + r'\n([^\n]+)', t) or [None, None])[1]
    posty = re.findall(r'\n(Posty Note \d+)\nResearch LV (\d+)\nLocked\n\n([^\n]+)', pn)
    found = re.findall(r'\n([A-Z][^\n]+)\n(?!Found)([^\n]*)\n\n(Found in [^\n]+)', ob)
    return save('research', {'level': f(g, 'Research level'), 'to_level': f(g, 'Time to level'), 'registrant': f(g, 'Time with registrant'), 'grid': f(g, 'Grid points'),
                             'obs': f(ob, 'Observations found'), 'rolls': f(ob, 'Rolls per day'), 'posty': posty[:2]})


def card_lines(o):
    L = [f"Research Lv {o['level']}, next level in {o['to_level']} ({o['registrant']} with registrant). Grid points {o['grid']}."]
    if o['posty']: L.append('Next Posty Note: ' + '; '.join(f"{a} at Lv {b}: {c[:80]}" for a, b, c in o['posty']))
    L.append(f"Observations {o['obs']}, {o['rolls']} rolls a day: use them daily.")
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
