"""Join layer 1 (snapshot facts) with layer 2 (jobs.yaml) -> model/map.md (compact, readable)."""
import json, gzip, os, sys, yaml
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
snap = os.path.join(R, 'snapshots', open(os.path.join(R, 'snapshots', 'LATEST')).read().strip())
review = json.load(gzip.open(os.path.join(snap, 'review.json.gz')))
chars = json.load(open(os.path.join(snap, 'chars.json')))['characters']
yaml_all = yaml.safe_load(open(os.path.join(R, 'model', 'jobs.yaml'))); jobs = yaml_all['characters']

tiers = {s['name']: s for w in review['worlds'] for s in w['sections']}
owned = set()
by_name = {c['character_name']: c for c in chars}
SKILLS = [k for k in chars[0]['skills'] if k != 'Combat' and 'Lol' not in k]
best = {s: max(chars, key=lambda c: c['skills'].get(s, 0)) for s in SKILLS}
vw = next(c for c in chars if c['class_name'] == 'Voidwalker')

def tier(sec):
    s = tiers.get(sec)
    if not s: return 'n/a'
    if s.get('completed'): return 'done'
    t = s['tier'] or '-'
    if '/' in t and t.split('/')[0].strip() == t.split('/')[1].strip() and t != '0/0': return 'done'
    return 'untiered' if t == '0/0' else t

out = [f"# Account map · game save {review['meta']['game_save_et']}", '']
pin = {k: tiers[k]['tier'] for k in ('Pinchy high', 'Pinchy low') if k in tiers}
out.append(f"AutoReview stage: strongest systems {pin.get('Pinchy high')}, weakest {pin.get('Pinchy low')}.")
out.append('')
for name, cfg in jobs.items():
    c = by_name[name]
    out.append(f"## {c['character_index']+1}. {name} · {c['class_name']} {c['combat_level']} · AFK W{c['world']} map {c['current_map_index']}")
    for j in cfg['jobs']:
        bits = []
        for sec in j.get('sections', []):
            owned.add(sec); bits.append(f"{sec} {tier(sec)}")
        if j.get('skill'):
            s = j['skill']; lv = c['skills'].get(s, 0); top = best[s]
            flag = '' if top['character_name'] == name else f" (best: {top['character_name']} {top['skills'][s]})"
            bits.append(f"{s} {lv}{flag}")
        if j.get('rule') == 'maestro':
            behind = [f"{s} ({best[s]['character_name']} {best[s]['skills'][s]} vs {vw['skills'][s]})"
                      for s in SKILLS if best[s]['skills'][s] > vw['skills'][s]]
            tied = [s for s in SKILLS if best[s]['skills'][s] == vw['skills'][s] and best[s]['character_name'] != vw['character_name']]
            bits.append(f"behind in {len(behind)}/{len(SKILLS)}: " + ', '.join(behind) if behind else 'top in all skills')
            if tied: bits.append('tied (not ahead) in: ' + ', '.join(tied))
        if j.get('note'):
            bits.append(j['note'])
        if j.get('needs'):
            bits.append(f"NEEDS: {j['needs']}")
        out.append(f"- **{j['job']}**: " + ' · '.join(bits))
    if cfg.get('needs'):
        out.append(f"- NEEDS: {cfg['needs']}")
    if cfg.get('plan'):
        out.append(f"- PLAN: {cfg['plan']}")
    extra = (yaml_all.get('extra_light') or {}).get(name)
    if extra:
        for sec in extra: owned.add(sec)
        out.append('- **W7 minis (light)**: ' + ', '.join(f"{x} {tier(x)}" for x in extra))
    out.append('')
skip = {'Pinchy high', 'Pinchy low', 'Pinchy all'}
unowned = [f"{n} {tier(n)}" for n in tiers if n not in owned and n not in skip and tier(n) not in ('done',)]
out.append('## Not owned by any character (open)')
out.append(', '.join(unowned))
open(os.path.join(R, 'model', 'map.md'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
