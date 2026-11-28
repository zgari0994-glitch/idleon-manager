"""One character's card from the latest cards4, plus the account goal. Q&A threads use this instead of reading cards4 whole.
Usage: python3 tools/card.py <name or nickname>   (e.g. Totle, Autistotle, goal)"""
import sys, re, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
NICK = {'zemo':'Autiszemo','cat':'Autistocat','ticles':'Autisticles','tastic':'Autistastic','bish':'Autistabish',
        'tacular':'Autistacular','totle':'Autistotle','matic':'Autistomatic','naut':'Autistronaut',
        'topher':'Autistopher','tachio':'Autistachio'}
save = (R/'snapshots'/'LATEST').read_text().strip()
f = R/'plans'/f'cards4_{save}.md'
if not f.exists(): sys.exit(f'MISSING {f.name}: the last pull did not build cards4. Tell Zack to re-run the pull.')
secs = re.split(r'(?m)^(?=## )', f.read_text())
def sec(prefix): return next((s for s in secs if s.startswith('## '+prefix)), '')
q = (sys.argv[1] if len(sys.argv) > 1 else 'goal').strip().lower()
name = NICK.get(q) or next((v for v in NICK.values() if v.lower() == q), None)
print(f'save {save}'); print(sec('Account goal').strip())
if q in ('goal', 'account', 'unowned'): print(); print(sec('Account systems').strip())
if name:
    print(); print(sec(name).strip() or f'no section for {name}')
elif q != 'goal':
    sys.exit(f'unknown name {q}; use a nickname: ' + ', '.join(NICK))
