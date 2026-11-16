"""Run AutoReview's own code on a raw Toolbox JSON and save structured findings (no HTML).
Usage: python run_ar.py <live.json> <out.json>   (run from IdleOnAutoReviewBot/mysite)
"""
import sys, json, re, datetime as dt
from zoneinfo import ZoneInfo

src, out = sys.argv[1], sys.argv[2]
raw = open(src).read()

import taskSuggester
captured = {}
_orig = taskSuggester.main
def _wrap(*a, **k):
    r = _orig(*a, **k)
    captured['r'] = r
    return r
taskSuggester.main = _wrap

from flask_app import app
SW = {'autoloot': 'on', 'doot': 'on', 'riftslug': 'on', 'sheepie': 'on', 'tabbed_advice_groups': 'on'}
with app.test_client() as c:
    resp = c.post('/results', data=json.dumps({'player': raw, **SW}),
                  content_type='application/json', headers={'Accept-Language': 'en-US'})
assert 'r' in captured, f'AutoReview did not run (HTTP {resp.status_code})'
reviews, header = captured['r']

TAG = re.compile(r'<[^>]+>')
def txt(v):
    return re.sub(r'\s+', ' ', TAG.sub('', str(v))).strip() if v not in (None, '') else ''

def adv(a):
    d = {'label': txt(a.label), 'cur': txt(getattr(a, 'progression', '')), 'goal': txt(getattr(a, 'goal', ''))}
    for k in ('completed', 'optional', 'informational', 'unrated'):
        if getattr(a, k, False):
            d[k] = True
    if getattr(a, 'resource', ''):
        d['res'] = txt(a.resource)
    return d

def advlist(x):
    if isinstance(x, dict):
        return [{'tab': txt(k), 'items': [adv(a) for a in v]} for k, v in x.items()]
    return [adv(a) for a in x]

def grp(g):
    if hasattr(g, 'tabbed_advices'):  # tabbed group: one subgroup per tab (often per character)
        d = {'name': 'tabbed', 'tier': txt(getattr(g, 'tier', '')),
             'tabs': [{'tab': txt(t.label) or txt(k), **grp(sub)} for k, (t, sub) in g.tabbed_advices.items()]}
        for k in ('completed', 'optional', 'informational'):
            if getattr(g, k, False):
                d[k] = True
        return d
    d = {'name': txt(getattr(g, 'pre_string', '')), 'tier': txt(getattr(g, 'tier', '')),
         'items': advlist(g.advices)}
    for k in ('completed', 'optional', 'informational'):
        if getattr(g, k, False):
            d[k] = True
    return d

worlds = []
for w in reviews:
    secs = []
    for s in w.sections:
        sd = {'name': txt(s.name), 'tier': txt(getattr(s, 'tier', '')),
              'header': txt(getattr(s, '_raw_header', '')), 'groups': [grp(g) for g in s.groups]}
        for k in ('completed', 'optional', 'informational', 'unreached'):
            if getattr(s, k, False):
                sd[k] = True
        secs.append(sd)
    worlds.append({'world': txt(getattr(w, 'title', '') or w.name), 'sections': secs})

j = json.loads(raw)
d = j.get('data', j)
ta = d['TimeAway']; ta = json.loads(ta) if isinstance(ta, str) else ta
NY = ZoneInfo('America/New_York')
meta = {
    'game_save_utc': dt.datetime.fromtimestamp(ta['GlobalTime'], dt.timezone.utc).isoformat(),
    'game_save_et': dt.datetime.fromtimestamp(ta['GlobalTime'], NY).strftime('%Y-%m-%d %I:%M %p ET'),
    'review_run_et': dt.datetime.now(NY).strftime('%Y-%m-%d %I:%M %p ET'),
    'autoreview_last_update': txt(getattr(header, 'last_update', '')),
    'switches': SW, 'chars': j.get('charNames'),
}
json.dump({'meta': meta, 'worlds': worlds}, open(out, 'w'), ensure_ascii=False)
print(json.dumps(meta), sum(len(w['sections']) for w in worlds), 'sections')
