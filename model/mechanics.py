"""Mechanics layer: everything owned that changes the rules or gives account-wide buffs.
Reads the latest snapshot -> model/mechanics.md (tagged list) + model/mechanics.json.
Facts only (from the save via AutoReview's parser). Reward/steps text for missing items comes from
sources added later (wiki achievements table etc.), never guessed."""
import json, gzip, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
snap = os.path.join(R, 'snapshots', open(os.path.join(R, 'snapshots', 'LATEST')).read().strip())
S = json.load(gzip.open(os.path.join(snap, 'systems.json.gz')))['systems']
meta = json.load(open(os.path.join(snap, 'meta.json')))
clean = lambda t: re.sub(r'\s+', ' ', str(t or '')).strip()

M = {}
# 1. Companions (global effects). Upgraded text applies only when level > 0.
M['companions'] = [{'name': k, 'effect': clean(v['_upgraded_description'] if v.get('level') else v['_base_description']),
                    'upgraded': bool(v.get('level'))}
                   for k, v in S['companions'].items() if v.get('copies')]
M['companions_missing'] = [k for k, v in S['companions'].items() if not v.get('copies')]
# 2. Packs / bundles
b = S['gemshop']['bundles']
M['packs_owned'] = [v['display'] for v in b.values() if v.get('owned')]
M['packs_missing'] = [v['display'] for v in b.values() if not v.get('owned')]
# 3. Gem shop permanent purchases (owned levels)
M['gemshop'] = [{'name': k, 'lv': v['owned'], 'max': v.get('max_level'), 'section': v.get('section')}
                for k, v in S['gemshop']['purchases'].items() if v.get('owned')]
# 4. Event shop
M['event_shop'] = [{'name': k, 'effect': clean(v.get('description'))} for k, v in S['event_points_shop'].items() if v.get('owned')]
M['event_shop_missing'] = [{'name': k, 'cost': v.get('cost'), 'effect': clean(v.get('description'))}
                           for k, v in S['event_points_shop'].items() if not v.get('owned')]
# 5. Legend talents
M['legend_talents'] = [{'name': k, 'lv': v['level'], 'max': v.get('max_level'),
                        'effect': clean(v.get('_description_template'))} for k, v in S['legend_talents'].items()]
# 6. Research nodes leveled
M['research'] = [{'name': k, 'lv': v['level'], 'effect': clean(v.get('description_template'))}
                 for k, v in S['research']['grid'].items() if v.get('level')]
# 7. Class-level family bonuses (account-wide, scale with that class's top level)
M['family_bonuses'] = [{'class': k, 'level': v.get('level'), 'value': v.get('value')} for k, v in S['family_bonuses'].items()]
# 8. Kill-count talents
M['kill_talents'] = [{'name': k, 'type': v.get('bonus_type'), 'kills': v.get('kills'),
                      'value': v.get('total_value'), 'how': clean(re.sub('<[^>]+>', ' ', v.get('_farm_label', '')))}
                     for k, v in S['class_kill_talents'].items()]
# 9. Divinity (King Doot makes W5 divinities count as active)
M['divinity'] = [{'god': v['name'], 'blessing': v.get('blessing_level')} for v in S['divinity'].values()]
# 10. Achievements
A = S['achievements']
M['achievements_done'] = sum(1 for v in A.values() if v.get('complete'))
M['achievements_open'] = [v['name'] for v in A.values() if not v.get('complete')]
# 11. Cosmetics with stats: hats (hat rack), capes (cape vine), trophies/nametags (gallery)
M['hats_owned'] = S['hat_rack'].get('count')
cv = S['cape_vine']
M['capes_deposited'] = cv.get('deposited_count')
M['capes_missing'] = [(c.get('cape') or {}).get('name') for c in (cv.get('missing') or []) if isinstance(c, dict)]
g = S['gallery']
M['gallery_multi'] = g.get('gallery_multi')
M['gallery_missing'] = {k: [x.get('name') for x in v] for k, v in (g.get('missing') or {}).items()}

json.dump(M, open(os.path.join(R, 'model', 'mechanics.json'), 'w'), indent=1, default=str)
L = [f"# Mechanics layer · game save {meta['game_save_et']}", '',
     'Rule-changers and account-wide buffs you own. Facts from the save; sources for missing items added separately.', '']
L.append(f"## Companions ({len(M['companions'])} owned, {len(M['companions_missing'])} missing)")
L += [f"- {c['name']}{' (upgraded)' if c['upgraded'] else ''}: {c['effect']}" for c in M['companions']]
L.append(f"- Missing: {', '.join(M['companions_missing'])}")
L += ['', f"## Packs ({len(M['packs_owned'])} owned)", '- Owned: ' + ', '.join(M['packs_owned']),
      '- Not owned: ' + ', '.join(M['packs_missing'])]
L += ['', f"## Gem shop upgrades owned ({len(M['gemshop'])})",
      '- ' + '; '.join(f"{x['name']} {x['lv']}/{x['max']}" for x in M['gemshop'])]
L += ['', f"## Event shop ({len(M['event_shop'])} owned)"] + [f"- {x['name']}: {x['effect']}" for x in M['event_shop']]
L.append('- Not owned: ' + '; '.join(f"{x['name']} ({x['cost']} pts): {x['effect']}" for x in M['event_shop_missing']))
lt = [x for x in M['legend_talents'] if x['lv']]
L += ['', f"## Legend talents ({len(lt)} leveled)"] + [f"- {x['name']} {x['lv']}/{x['max']}: {x['effect']}" for x in lt]
L += ['', '## Research nodes leveled'] + [f"- {x['name']}: {x['effect']}" for x in M['research']]
L += ['', '## Kill-count talents'] + [f"- {x['name']} ({x['type']}): {x['kills']} kills, value {round(x['value'] or 0, 2)}. {x['how']}" for x in M['kill_talents']]
L += ['', '## Family bonuses (top level of each class, account-wide)',
      '- ' + '; '.join(f"{x['class']} {x['level']}" for x in M['family_bonuses'])]
L += ['', '## Divinity blessings', '- ' + '; '.join(f"{x['god']} {x['blessing']}" for x in M['divinity'])]
L += ['', f"## Achievements: {M['achievements_done']} done, {len(M['achievements_open'])} open",
      '- Open: ' + ', '.join(M['achievements_open'])]
L += ['', '## Cosmetics with stats',
      f"- Hats on rack: {M['hats_owned']}",
      f"- Capes on vine: {M['capes_deposited']}; missing: {', '.join(map(str, M['capes_missing'])) or 'none listed'}",
      f"- Gallery multi {round(M['gallery_multi'] or 0, 2)}x",
      f"- Trophies missing: {', '.join(M['gallery_missing'].get('trophy', []))}",
      f"- Nametags missing: {', '.join(M['gallery_missing'].get('nametag', []))}",
      '- How to get each missing one (pack vs in-game): source pass pending (wiki).']
open(os.path.join(R, 'model', 'mechanics.md'), 'w').write('\n'.join(L) + '\n')
print(len('\n'.join(L)), 'chars written')
