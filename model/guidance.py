"""Guidance index (2026-11-19): every tagged creator claim, ranked, so cards can say HOW.

Rules (Zack 2026-11-19):
- Griffy first. Pulse + Nocturne are tier 1b: they stand in where Griffy has nothing, else supplement + confirm.
- Every accurate claim is used. Recency wins only on a CONFLICT (different target numbers for the same thing,
  or a later meta_change). Older non-conflicting claims stay.
- Off-game rows (system none) and pure opinions/account notes are not guidance.

build()  -> model/guidance.json   (python3 model/guidance.py)
how(section, label, n=2) -> list of claim dicts for a card line (used by plan.py)
"""
import csv, glob, json, os, re, datetime as dt
from functools import lru_cache
import yaml
from rapidfuzz import fuzz, process

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(R, 'model', 'guidance.json')
CREATOR = {'griffybit': 3.0, 'pulseidle': 2.0, 'nocturne': 2.0}
SHORT = {'griffybit': 'Griffy', 'pulseidle': 'Pulse', 'nocturne': 'Nocturne'}
TYPE = {'how_to': 1.0, 'priority': 1.0, 'target': 1.0, 'setup': 0.95, 'warning': 0.9, 'threshold': 0.9, 'active_task': 0.9,
        'afk_spot': 0.9, 'skip': 0.85, 'comparison': 0.8, 'blocker': 0.85, 'meta_change': 0.7, 'mechanic': 0.55}
NOT_GUIDANCE = {'opinion', 'account_note'}
STAGE = {'early_w7': 1.0, 'w7': 1.0, 'endgame': 1.0, 'late': 0.95, 'w6': 0.9, 'any': 0.9, 'unknown': 0.8, 'mid': 0.6,
         'w5': 0.65, 'w4': 0.5, 'early': 0.35, 'w3': 0.4, 'w2': 0.3, 'w1': 0.3}
TODAY = dt.date.today()


def _age_years(d):
    try:
        return max(0.0, (TODAY - dt.date.fromisoformat(d)).days / 365.0)
    except Exception:
        return 3.0   # undated (old speedrun parts): treat as old


def norm(s):
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9\' ]', ' ', (s or '').lower().replace('_', ' '))).strip()


def build():
    rows = []
    rf = os.path.join(R, 'sources', 'findings', 'resection.json')
    RESECT = json.load(open(rf)) if os.path.exists(rf) else {}   # tools/resection.py: advice filed under the wrong system
    for f in glob.glob(os.path.join(R, 'sources', 'creators', '*', 'tags', '*.csv')):
        for r in csv.DictReader(open(f, encoding='utf-8')):
            if r['system'] in ('none', '') or r['claim_type'] in NOT_GUIDANCE or not r.get('statement'):
                continue
            if r.get('explicit') == 'no' and r.get('confidence') == '1':
                continue
            age = _age_years(r.get('date') or '')
            st = r['statement'].strip()
            # general advice beats a creator narrating his own account ("He changes the plan to...")
            narr = 0.55 if re.match(r"(he|his|she|they|their|we|i|the player|this player)\b", st, re.I) else 1.0
            w = (CREATOR.get(r['creator'], 1) * TYPE.get(r['claim_type'], 0.5) * STAGE.get(r.get('stage') or 'unknown', 0.7)
                 * (1.0 if r.get('confidence') in ('3', '') else 0.85) * (1 / (1 + 0.6 * age)) * narr)
            rs = RESECT.get(f"{r['video_id']}|{r['t_start']}|{r.get('subsystem', '')}")
            sysname = rs['to'] if rs and rs['act'] == 'move' else r['system']
            if rs and rs['act'] == 'also':
                rows.append({'sys': rs['to'], 'sub': r.get('subsystem', ''), 'k': norm(r.get('subsystem', '')), 'type': r['claim_type'], 'stage': r.get('stage', ''),
                             'num': r.get('numbers', ''), 'say': r['statement'], 'who': r['creator'], 'date': r.get('date') or '', 'vid': r['video_id'],
                             't': r['t_start'], 'w': round(w, 4), 'refiled_from': r['system']})
            rows.append({'sys': sysname, 'sub': r.get('subsystem', ''), 'k': norm(r.get('subsystem', '')),
                         'type': r['claim_type'], 'stage': r.get('stage', ''), 'num': r.get('numbers', ''),
                         'say': r['statement'], 'who': r['creator'], 'date': r.get('date') or '', 'vid': r['video_id'],
                         't': r['t_start'], 'w': round(w, 4)})
    idx = {}
    for x in rows:
        idx.setdefault(x['sys'], []).append(x)
    for s in idx:
        idx[s].sort(key=lambda x: -x['w'])
    json.dump(idx, open(OUT, 'w'))
    return idx


@lru_cache(None)
def _idx():
    return json.load(open(OUT))


# AutoReview sections the system index never tied to a transcript slug (sweep 2026-11-19)
SEC_OVERRIDE = {'Sigils': ['sigils'], 'Event Shop': ['event_shop'], 'Smithing': ['anvil', 'forge'], 'Star Signs': ['constellations'],
                'Bonus Ballot': ['ballot'], 'Armor Sets': ['armor_smithy'], 'Dancing Coral': ['coral_reef'], 'Coral Kid': ['divinity', 'coral_reef'],
                'Combat Levels': ['characters'], 'Secret Class Path': ['class_choice'], 'Drop Rate': ['drop_rate'], 'Storage': ['storage'],
                'Regular Candy': ['general'], 'Post Office': ['general']}


@lru_cache(None)
def _sec2slug():
    si = yaml.safe_load(open(os.path.join(R, 'model', 'system_index.yaml')))
    m = {k: list(v) for k, v in SEC_OVERRIDE.items()}
    for k, v in si.items():
        slug = v.get('transcripts', {}).get('slug') if isinstance(v.get('transcripts'), dict) else None
        for sec in v.get('autoreview', []) or []:
            if slug:
                m.setdefault(sec, []).append(slug)
    return m


def label_name(label):
    """'Wicked Smart: +990% ...' -> wicked smart ; 'Artifact: Omnipotent Causticolumn 0' -> omnipotent causticolumn"""
    lab = re.sub(r'^(Push|Lever on \w+):\s*', '', label.strip(), flags=re.I)
    if ':' in lab:
        pre, post = lab.split(':', 1)
        post = post.strip()
        lab = pre if (not post or re.match(r'[+\-\d.]', post)) else post
    lab = re.split(r'\(|\s\d|\s->|\+', lab, maxsplit=1)[0]
    return norm(lab)


def _nums(x):
    return set(re.findall(r'\d[\d.,]*', x['num'] or ''))


def _dedupe(cands):
    """Drop near-duplicate claims; on a target conflict (same thing, different numbers) the newest wins."""
    out = []
    for c in cands:
        dup = False
        for o in out:
            if fuzz.token_set_ratio(c['say'], o['say']) > 80:
                dup = True; break
            if c['type'] == o['type'] == 'target' and c['k'] == o['k'] and _nums(c) and _nums(o) and _nums(c) != _nums(o):
                newer = c if c['date'] > o['date'] else o
                older = o if newer is c else c
                if newer is c:
                    out[out.index(o)] = dict(c, older=f"{SHORT[o['who']]} {o['date'][:7]} said {o['num']}")
                else:
                    o.setdefault('older', f"{SHORT[c['who']]} {c['date'][:7]} said {c['num']}")
                dup = True; break
        if not dup:
            out.append(c)
    return out


def how(section, label, n=2):
    """Best creator claims for one card line: exact upgrade first, else the system's top actionable claims."""
    slugs = _sec2slug().get(section, [])
    pool = [x for s in slugs for x in _idx().get(s, [])]
    if not pool:
        return [], 'gap'
    name = label_name(label)
    exact = []
    if len(name) >= 4:
        keys = list({x['k'] for x in pool if x['k']})
        hits = {k for k, sc, _ in process.extract(name, keys, scorer=fuzz.token_sort_ratio, limit=8) if sc >= 86 and len(k) >= 5}
        exact = [x for x in pool if x['k'] in hits or (len(name) >= 8 and len(name.split()) >= 2 and name in norm(x['say']))]
        exact = [x for x in exact if x['date'] >= '2024-06']   # older claims only via the system take
    if exact:
        return _dedupe(sorted(exact, key=lambda x: -x['w']))[:n], 'exact'
    sysl = [x for x in pool if x['type'] in ('priority', 'how_to', 'target', 'blocker', 'warning')]
    return _dedupe(sysl)[:1], 'system'


def fmt(c):
    d = c['date'][:7] if c['date'] else 'undated'
    num = f" [{c['num']}]" if c['num'] and c['num'] not in c['say'] else ''
    older = f" (older: {c['older']})" if c.get('older') else ''
    return f"{c['say']}{num} ({SHORT.get(c['who'], c['who'])} {d} @{c['t'][:8]}){older}"


def tag(c):
    return 'WHY' if c['type'] in ('mechanic', 'comparison') else 'HOW'


def push_weight():
    """Creator push per system slug for the rinse: actionable claims, creator + recency weighted."""
    w = {}
    for s, xs in _idx().items():
        w[s] = round(sum(x['w'] for x in xs if x['type'] in ('priority', 'target', 'how_to', 'blocker')), 2)
    return w


if __name__ == '__main__':
    idx = build()
    print('guidance rows', sum(len(v) for v in idx.values()), 'systems', len(idx))
    _idx.cache_clear()
    for sec, lab in [('Stamps', 'Skill: Drippy Drop Stamp'), ('Compass', 'Atomic Cost Crash'), ('Upgrade Vault', 'Wicked Smart: +990% Class EXP'),
                     ('Farming', 'Evolution Gmo'), ('Menagerie', 'Shells')]:
        cs, kind = how(sec, lab)
        print('\n#', sec, '|', lab, '->', kind)
        for c in cs:
            print('  -', fmt(c)[:230])
