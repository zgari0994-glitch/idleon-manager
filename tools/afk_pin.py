"""Pin / clear an active-play park line. Usage: afk_pin.py <nick> active <activity...> | <nick> clear (Zack 2026-11-27)."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'model'))
from afk import NICK, PIN_PULLS, STATE
nick, verb, *rest = sys.argv[1:]
if nick == 'goal':
    import goalpick as G; print(G.confirm(' '.join([verb] + rest))); sys.exit()
name = NICK[nick.capitalize()]
st = json.loads(STATE.read_text()) if STATE.exists() else {'last_save': None, 'chars': {}}
cs = st['chars'].setdefault(name, {'hist': []})
if verb == 'clear': cs.pop('pin', None); cs['prompt'] = None
elif verb == 'active': cs['pin'] = {'activity': ' '.join(rest), 'left': PIN_PULLS}; cs['prompt'] = None
STATE.write_text(json.dumps(st, indent=1)); print(nick, cs.get('pin') or 'cleared')
