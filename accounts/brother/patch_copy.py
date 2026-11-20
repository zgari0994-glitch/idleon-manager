"""Patch a throwaway COPY of Zack's code so it fits the brother's account. Never run on the real repo.
- AutoReview path -> the build's own AutoReview checkout
- AutoReview switches -> accounts/brother/switches.json (his companions, not Zack's)
- Zack-only plan pieces in cards2 (his goal, trap/money plans, divinity runner, ZOW park note) -> off / the rinse goal
- Zack's character names in the code -> the brother's character in the same role (roles.json)
- Zack's generated outputs in the copy are wiped so nothing of his leaks into the brother's cards
Usage: python3 patch_copy.py <copy_dir> <autoreview_dir>
"""
import sys, os, re, json, glob

C, AR = sys.argv[1], sys.argv[2]
B = os.path.dirname(os.path.abspath(__file__))
assert os.path.abspath(C) != os.path.abspath(os.path.join(B, '..', '..')), 'refusing to patch the real repo'

def sub(path, old, new, regex=False):
    p = os.path.join(C, path)
    s = open(p).read()
    n = len(re.findall(old, s)) if regex else s.count(old)
    if n == 0:
        print(f'WARN patch not applied (code changed?): {path}: {old[:70]}')
        return
    s = re.sub(old, new, s) if regex else s.replace(old, new)
    open(p, 'w').write(s)

# 1) Zack's generated outputs: wipe (inputs kept: jobs/ledger/system_index yaml, guidance.json, system_index.md)
for f in glob.glob(os.path.join(C, 'model', '*.json')) + glob.glob(os.path.join(C, 'model', '*.md')):
    if os.path.basename(f) not in ('guidance.json', 'system_index.md'):
        os.remove(f)
for f in ('rinse/latest.json',):
    if os.path.exists(os.path.join(C, f)): os.remove(os.path.join(C, f))
for f in glob.glob(os.path.join(C, 'dashboard', '*')):
    if os.path.isfile(f): os.remove(f)
open(os.path.join(C, 'model', 'ledger.yaml'), 'w').write('# Brother: no material watchlist yet (auto setup)\nwatch: []\n')

# 2) AutoReview switches: his own
sub('tools/run_ar.py', r"SW = \{[^}]*\}", "SW = json.load(open(os.environ['BRO_SWITCHES']))", regex=True)
sub('tools/run_ar.py', 'import sys, json, re', 'import sys, json, re, os')

# 3) cards2: Zack-only plan pieces
cp = 'model/cards2.py'
sub(cp, "for row in (ROOT / 'plans' / 'trapping.md').read_text().splitlines():",
        "for row in ((ROOT / 'plans' / 'trapping.md').read_text().splitlines() if (ROOT / 'plans' / 'trapping.md').exists() else []):")
sub(cp, "mp = (ROOT / 'plans' / 'money_plan.md').read_text()",
        "mp = (ROOT / 'plans' / 'money_plan.md').read_text() if (ROOT / 'plans' / 'money_plan.md').exists() else ''")
sub(cp, r"DIV_RUNNER = '[^']*'", "DIV_RUNNER = None", regex=True)
sub(cp, r' Pushing W7 also gets him toward Jellofish Fields\. "\s*"Autistopher keeps the Dedotated Ram kills"', '"', regex=True)
sub(cp, '# ---------------- step transform ----------------',
        'from bro_goal import goal_card  # brother: goal from the rinse (accounts/brother/goal.py)\n# ---------------- step transform ----------------')
sub(cp, 'IdleOn cards · save', 'IdleOnLech cards · save')
# No Toolbox reads for him, so planners give few action lines: fall back to AutoReview's own next goals
# (Zack 2026-11-20: review the raw AutoReview suggestions), with the creator's reason as the why.
sub(cp, """    if not acts:
        return {'do': f"{name}: nothing needed", 'why': '', 'sub': []}""",
"""    if not acts:
        _st = [s for s in block.get('steps', []) if isinstance(s, str)]
        _ng = [(m.group(1) + ': ' if m.group(1) else '') + m.group(2) for m in (re.match(r'^(?:([^:]{1,40}): )?Next goal: (.*)', s) for s in _st) if m]
        _gw = next((re.sub(r'^(?:[^:]{1,40}: )(?=(Griffy|Pulse|Nocturne): )', '', s) for s in _st if re.match(r'^(?:[^:]{1,40}: )?(Griffy|Pulse|Nocturne): ', s)), '')
        if not _ng:
            _own = [s[len(owner) + 1:].strip('()') for s in _st if owner and s.startswith(owner + ' (')]
            if _own:
                return {'do': f"{name}: {_own[0]}", 'why': 'AutoReview target for this character', 'sub': []}
            if not _st:
                return {'do': f"{name}: not checked (needs Toolbox page data this account doesn't have)", 'why': '', 'sub': []}
            return {'do': f"{name}: nothing needed", 'why': '', 'sub': []}
        _gw = _gw.split('. ')[0].rstrip('.')
        return {'do': f"{name}: push {_ng[0]}", 'why': (_gw[:110] if _gw else 'AutoReview next tier'), 'sub': _ng[1:4]}""")

# 4) paths + character names across all code in the copy
ROLE = json.load(open(os.path.join(B, 'roles.json')))
names = sorted(ROLE, key=len, reverse=True)
for p in glob.glob(os.path.join(C, '**', '*.py'), recursive=True):
    s0 = s = open(p).read()
    s = s.replace('/home/claude/work/ar', AR).replace('/home/claude/ar', AR)
    for n in names:
        s = s.replace(n, ROLE[n])
    s = s.replace(r'Autis\w+', r'IdleOnLech\w*').replace(r'Autis[a-z]+', r'IdleOnLech\w*').replace("'Autis'", "'IdleOnLech'")
    if s != s0:
        open(p, 'w').write(s)
print('patched copy')
