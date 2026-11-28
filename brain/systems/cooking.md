---
name: cooking
description: Cooking: state, how it works, links, plan, today
---
# Cooking

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autiszemo
- Toolbox: world-4/cooking (guide L110)
- AutoReview: Cooking
- Planner: model/cooking.py
- Creator rows: 646
- Findings: none
- Open gaps: 4: Cooking mastery ranks need a source (what to take, order) | 5: Which meals get ribbons and when | 6: Card says cooking needs a lot but gives no plan: needs speed levers ranked by current values + steps
- Checklist: [[cooking]]: a cooking goal (speed), what Zemo does daily to improve it, mastery points, ladle reserve vs Equinox
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: independent       # my read: no direct POW link found; recheck if a meal hits Spelunking
goal: "Raise meal cooking speed so meals clear 120 -> 150 -> 180, because total meal levels drive Blood Marrow and every meal bonus"
coverage: partial
ladder:
  - {tier: 1, target: "Turkey + Egg past 111 (Egg = meal cooking speed, Turkey toward a power-of-ten breakpoint)", source: "Griffy", date: "2026-11-07"}
  - {tier: 2, target: "Unlock max level 150 plates (now 120)", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "74 meals at 150 (3,177 levels, ~1,064 NMLB triggers)", source: "Toolbox", date: "2026-11-27"}
  - {tier: 4, target: "Max 180 plates, 74 meals at 180 (total 7,923 -> 13,320)", source: "Toolbox", date: "2026-11-27"}
objective: {rung: 1, now: 111, target: null, eta_days: null}   # breakpoint level for Turkey not sourced yet
check: {cadence: daily, who: "Autiszemo", look_at: "kitchens on speed meals, cheap kitchen upgrade, mastery points"}
buffs:
  - {source: "cheap kitchen upgrades (Griffy 2026-10-16)", world: 4, owned: true, now: null, next: null, owner: "Autiszemo"}
  - {source: "new-recipe speed via stamps + meals if recipes take 7-9h (Griffy 2026-11-07)", world: 1, owned: null, now: null, next: null, owner: "Autistopher"}
  - {source: "Menagerie unlock 21: +10 max cooking LV (29.75M Lumi)", world: 7, owned: false, now: 0, next: 1, owner: "Autisticles"}
triggers:
  - {when: "max plates reach 150", then: "switch focus to NMLB triggers, then 180"}
  - {when: "a ribbon rank threshold hit (1/5/10/25)", then: "re-rank ribbon placement (gap 5)"}
stall: {pulls_no_progress: 3, eta_over_days: 30}   # already flagged: "stuck at 111"
tasks:
  - {do: "Spend on the cheapest kitchen speed upgrade", stat: "meal cooking speed", gain_pct: null, unblocks: [meals], source: "Griffy", active_min: 2, wait_hr: null, cost: null, urgent: false}
  - {do: "Keep Egg on a kitchen until its next breakpoint", stat: "meal cooking speed", gain_pct: null, unblocks: [], source: "Griffy", active_min: 1, wait_hr: null, cost: null, urgent: false}
# GAPS: mastery rank picks (gap 4) still unsourced, no picks until sourced
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

## History and lessons (moved from Project memory 2026-11-21; dated state is history, live data wins)
- 11-16: mastery factored in, but no mastery picks until a creator source and a choosing method exist.
