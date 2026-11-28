"""Live value resolver for GOAL now_path and trigger when_path (Phase C A + B, Zack 2026-11-28).
Spec forms: 'a.b[*].c|reducer' on the parsed account (tb_parsed), '@Autiszemo.path' on one character, 'metric:name' = syscheck2.metrics(),
or a plain number. Tokens: key, * (every dict value / list item), [N], [*], [k=v], [k~v] (contains, any case), [k>N], [k<N].
Reducers: min max sum len count first. Missing path -> None (shown as 'not in save'), never a guess."""
import re, operator
OPS = {'>=': operator.ge, '<=': operator.le, '>': operator.gt, '<': operator.lt, '==': operator.eq, '!=': operator.ne}
TOK = re.compile(r'\[([^\]]*)\]|([^.\[\]]+)')
_D = _M = None


def _data():
    global _D
    if _D is None:
        from data import load; _D = load()
    return _D


def _metrics():
    global _M
    if _M is None:
        try: import syscheck2; _M = syscheck2.metrics()
        except Exception: _M = {}
    return _M


def num(x):
    if isinstance(x, bool): return float(x)
    if isinstance(x, (dict, list)) or x is None: return None
    try: return float(str(x).replace(',', ''))
    except Exception: return None


def _idx(o, tok):
    return isinstance(o, list) and tok.lstrip('-').isdigit() and -len(o) <= int(tok) < len(o)


def _step(objs, tok, br):
    out = []
    for o in objs:
        if o is None: continue
        if tok == '*':
            out += list(o.values()) if isinstance(o, dict) else list(o) if isinstance(o, list) else []
        elif not br:
            if isinstance(o, dict) and tok in o: out.append(o[tok])
            elif _idx(o, tok): out.append(o[int(tok)])
        elif tok.lstrip('-').isdigit():
            if _idx(o, tok): out.append(o[int(tok)])
        else:
            m = re.match(r'(\w+)\s*(=|~|>|<)\s*(.*)', tok)
            if not m or not isinstance(o, list): continue
            k, op, v = m.groups()
            for it in o:
                if not isinstance(it, dict) or k not in it: continue
                x = it[k]
                if (op == '=' and str(x) == v) or (op == '~' and v.lower() in str(x).lower()) or \
                   (op in '<>' and num(x) is not None and num(v) is not None and (num(x) > num(v) if op == '>' else num(x) < num(v))):
                    out.append(it)
    return out


def resolve(spec):
    if spec is None: return None
    if isinstance(spec, (int, float)) and not isinstance(spec, bool): return spec
    s = str(spec).strip()
    if s.startswith('metric:'): return _metrics().get(s[7:])
    if num(s) is not None: return num(s)
    path, _, red = s.partition('|'); red = red.strip()
    D = _data()
    if path.startswith('@'):
        who, _, path = path[1:].partition('.')
        try: root = D.char(who)
        except Exception: return None
    else: root = D.raw.get('account')
    objs, many = [root], False
    for br, key in TOK.findall(path):
        tok = br if br else key
        if tok == '*' or (br and not tok.lstrip('-').isdigit()): many = True
        objs = _step(objs, tok, bool(br))
        if not objs: return 0 if many and red in ('len', 'count', 'sum') else None
    if red == 'len': return len(objs[0]) if not many and isinstance(objs[0], (list, dict)) else len(objs)
    if red == 'count': return sum(1 for o in objs if o)
    if red in ('min', 'max', 'sum'):
        vals = [num(o) for o in objs if num(o) is not None]
        return ({'min': min, 'max': max, 'sum': sum}[red])(vals) if vals else None
    return objs[0] if (red == 'first' or not many) else objs


def check(t):
    """Trigger row -> (state, cur, value). state: fired / armed / missing (path not in save) / manual (no path yet)."""
    spec = t.get('when_path'); val = t.get('value')
    if not spec: return 'manual', None, None
    cur = resolve(spec); goal = resolve(val) if val is not None else None
    op = str(t.get('op') or '>=')
    if op == 'truthy': return (('fired' if cur else 'armed') if cur is not None else 'missing'), cur, None
    if num(cur) is None or num(goal) is None: return 'missing', cur, goal
    return ('fired' if OPS.get(op, operator.ge)(num(cur), num(goal)) else 'armed'), cur, goal


def fmt(v):
    n = num(v)
    if n is None or (isinstance(v, str) and not re.fullmatch(r'[\d.,eE+-]+', v.strip())): return str(v)
    if abs(n) >= 1e7: return f'{n:.3g}'
    return f'{int(n):,}' if n == int(n) else f'{n:,.2f}'
