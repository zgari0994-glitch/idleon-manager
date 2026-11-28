---
name: caverns
description: Caverns: state, how it works, links, plan, today
---
# Caverns

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistabish
- Toolbox: world-5/hole (guide L124)
- AutoReview: Villagers, Shallow Caverns, Glowshroom Tunnels, Underground Overgrowth
- Planner: model/spelunking.py, model/hole.py
- Creator rows: 717
- Findings: hole_caverns_1-5
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT synthesis 2026-11-28 batch 1 (claims DB, save 20261128T0256): not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: independent       # my read; feeds Spelunking via Gambit bones + monuments, not a blocker
goal: "Explorer finishes cavern unlocks (16-20), then opals move to Studies; every cavern run on its cadence"
coverage: sourced
ladder:
  - {tier: 1, target: "Explorer (Polonai) 15 -> 20, discovers caverns 16-20 (now 15, 73% to 16)", source: "Toolbox + Griffy (opals to Explorer first)", date: "2024-11-09 / 2026-11-28"}
  - {tier: 2, target: "Fountain (cavern 16) pushed: study rate + Fountain EXP first, bucket a bit, treasure boost last", source: "Pulse", date: "2026-11-12"}
  - {tier: 3, target: "Explorer done -> most opals into Studies villager", source: "Griffy", date: "2026-01-29"}
  - {tier: 4, target: "Evertree + Trench layers (Evertree 13 now; Pulse example account at 29)", source: "Pulse", date: "2026-11-16"}
now_path: "hole.villagers[0].level"
objective: {rung: 1, now: 15, target: 20, eta_days: null}
check: {cadence: daily, who: "Autistabish", look_at: "12 lanterns dropped, Bravery run, Bell coins + Lamp push, Gambit points vs 710K"}
opal_split:             # villager opals now: Explorer 60, Engineer 40, Conjuror 30, Measurer 20, Studies 20
  - {rule: "keep at least 1 opal in every villager", source: "Griffy", date: "2026-10-28"}
  - {rule: "Conjuror to the 10th-opal breakpoint, then Measurer, while schematics continue", source: "Griffy", date: "2026-10-28"}
  - {rule: "Measurer when schematic resources are far off; Engineer when close to the next schematic", source: "Griffy", date: "2026-10-28"}
  - {rule: "Explorer needs far more XP per level, so it gets the most opals until caverns are unlocked", source: "Griffy", date: "2024-11-09"}
caverns:                # how it works / what to level / when to run
  - {cavern: "Bravery (Monument)", do: "run daily; take mining efficiency + reward multipliers; it is the biggest mining-efficiency source", source: "Griffy 2026-01-29; Pulse 2026-09-08 + 2026-09-15 (mining eff underinvested, cooking speed overinvested)"}
  - {cavern: "Bravery timing", do: "don't let reward multi sit far above ~3 (diminishing); run before 60x. Now 1.86x at 371 hrs, +1 sword at 750 hrs", source: "Griffy 2026-03-10 (older: 2026-01-29 60x cap); Toolbox"}
  - {cavern: "Bell", do: "coins + daily Lamp pushes are the strongest Bell picks; bucket focus not needed; reset after Triple Tap Tinkle", source: "Pulse 2026-11-12; Griffy 2026-10-28"}
  - {cavern: "Lamp", do: "W5 wishes (Divinity pts): ~50 is very good; don't neglect infinite resources wish; opal wish when it costs 1", source: "Pulse 2026-11-12; Griffy 2026-10-04"}
  - {cavern: "Harp", do: "Harp strings over rupies; keep making C notes toward overdue schematics", source: "Griffy", date: "2026-10-28"}
  - {cavern: "Blinding Lantern", do: "drop all 12 lanterns every day (0 of 12 used this save)", source: "Pulse", date: "2026-11-03"}
  - {cavern: "Gambit", do: "push points: 535K now, next unlock 710K = +2 bones on Deathbringer", source: "Toolbox", date: "2026-11-28"}
  - {cavern: "Den", do: "damage setup, 1,800 score for the next opal", source: "Griffy", date: "2026-10-28"}
  - {cavern: "Collectibles", do: "reset collectible levels toward the current goal (Minecraft Gem for monument AFK, Rose Emerald / study collectible for study rate)", source: "Pulse 2026-11-16 (older: Griffy 2026-01-29)"}
  - {cavern: "Node pushing", do: "push Motherlode, Evertree, Fractal Fly, Trench Fish with the matching skill class", source: "Pulse", date: "2026-10-31"}
buffs:
  - {source: "Conjuror Pts + Opal from gemshop", world: 5, owned: false, now: 0, next: 1, owner: "Autistotle"}
  - {source: "Villager EXP talent (B tier) / Best Story Ever Told (A tier)", world: 7, owned: null, now: null, next: null, owner: "Autistabish"}
triggers:
  - {when: "Gambit points 710K", then: "claim +2 bones on Deathbringer (Death Note / bones push)"}
  - {when: "Explorer 20 (all caverns found)", then: "move most opals to Studies"}
  - {when: "Bravery 750 AFK hrs", then: "+1 sword; run it"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Drop 12 blinding lanterns", stat: "daily lantern reward", gain_pct: null, unblocks: [], source: "Pulse 2026-11-03", active_min: 2, wait_hr: null, cost: null, urgent: true}
  - {do: "Push Gambit 535K -> 710K", stat: "Gambit points", gain_pct: null, unblocks: ["death_note"], source: "Toolbox 2026-11-28", active_min: 5, wait_hr: null, cost: null, urgent: false}
  - {do: "Run Bravery, take mining eff + reward multi", stat: "mining efficiency", gain_pct: null, unblocks: [], source: "Griffy 2026-01-29", active_min: 3, wait_hr: null, cost: null, urgent: false}
  - {do: "Bell: coins + Lamp push", stat: "Divinity pts via W5 wishes", gain_pct: null, unblocks: ["divinity"], source: "Pulse 2026-11-12", active_min: 2, wait_hr: null, cost: null, urgent: false}
  - {do: "Buy Harp strings before rupies, keep C notes going", stat: "schematic resources", gain_pct: null, unblocks: [], source: "Griffy 2026-10-28", active_min: 2, wait_hr: null, cost: null, urgent: false}
# Warning: Hole farming over-levels mining/catching chars (Griffy 2026-10-28)
```
<!-- GOAL:END -->

## How it works (mechanics, multipliers, formulas; cite source)

## Links
- Feeds ->
- Fed by <-
- Uses (reserve-checked) :
- Unlocks / is gated by :

## Creator rule of thumb (Griffy > Pulse = Nocturne; newest wins)

## Plan
- Now:
- Next:
- Stop point (bottleneck / slow burn):
- Waiting on:

## Today (written by the decision layer each pull)
