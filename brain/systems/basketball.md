---
name: basketball
description: Basketball: state, how it works, links, plan, today
---
# Basketball

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: GAP: no Toolbox page mapped
- AutoReview: Basketball
- Planner: NONE (nothing checks this yet)
- Creator rows: 0
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 9 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: independent
goal: "Hoops shop upgrades bought as points come in (Damage, Coins, Class EXP, Skill Efficiency, no caps)"
coverage: none   # AutoReview lists the shop only; Griffy's only line says Goldric's hoops quest is the catching minigame
ladder:
  - {tier: 1, target: "All 4 upgrades unlocked (done: 80/100/20/117)", source: "Toolbox (parser)", date: "2026-11-28"}
  - {tier: 2, target: "my read: cheapest-gain first: Class EXP (cost 3), Damage (8), then Coins (403), Skill Eff (2,345)", source: "my_read", date: "2026-11-28"}
objective: {rung: 2, now: "high score 26, 317 total points", target: null, eta_days: null}
check: {cadence: weekly, who: "UNASSIGNED", look_at: "highscores.minigameHighscores hoops upgrades"}
buffs: []   # minigame, low priority
triggers: []
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "In game: check spendable hoops points; spend on Class EXP (3) and Damage (8)", stat: "class exp / dmg", gain_pct: null, unblocks: [], source: "my_read", active_min: 2, wait_hr: null, cost: null, urgent: false}
# gap: no creator coverage; spendable points (vs 317 total) not in parser; data_map basketball path null (real: highscores.minigameHighscores).
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
