"""Patch a throwaway COPY of Zack's code so it fits the brother's account. Never run on the real repo.
Swaps Zack-only text (title, his watch notes, his character-name regexes, his material watchlist).
Usage: python3 patch_copy.py <copy_dir>
"""
import sys, os, re

C = sys.argv[1]
assert os.path.abspath(C) != os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')), 'refusing to patch the real repo'

def sub(path, old, new, regex=False, count=0):
    p = os.path.join(C, path)
    s = open(p).read()
    n = len(re.findall(old, s)) if regex else s.count(old)
    if n == 0:
        print(f'WARN patch not applied (code changed?): {path}: {old[:60]}')
        return
    s = re.sub(old, new, s, count=count) if regex else s.replace(old, new)
    open(p, 'w').write(s)

# dashboard header + Zack's personal watch notes
sub('model/dashboard.py', 'IdleOn Manager · Autiszemo', 'IdleOn Manager · IdleOnLech')
sub('model/dashboard.py', r"\n\s*'Elite Class Swap Token: watch gem shop -> Autistronaut to Arcane Cultist',", '', regex=True)
sub('model/dashboard.py', r"\n\s*'Idle Skilling \(Steam\)[^\n]*Autiszemo',", '', regex=True)
# character-name patterns used to strip "Name:" prefixes and park rules
sub('model/plan.py', r'with (Autis\w+)', r'with (IdleOnLech\w*)')
sub('model/plan.py', r"r'^Autis\w+:\s*'", r"r'^IdleOnLech\w*:\s*'")
sub('model/plan.py', r"r'^Autis[a-z]+:\s*'", r"r'^IdleOnLech\w*:\s*'")
sub('model/sailing.py', "w.startswith('Autis')", "w.startswith('IdleOnLech')")
# Zack's material watchlist describes his account: start the brother empty
open(os.path.join(C, 'model', 'ledger.yaml'), 'w').write('# Brother: no material watchlist yet (auto setup)\nwatch: []\n')
print('patched copy')
