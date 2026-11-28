---
name: meals
description: Meals: state, how it works, links, plan, today
---
# Meals

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autiszemo
- Toolbox: world-4/cooking (guide L110)
- AutoReview: Cooking
- Planner: model/cooking.py
- Creator rows: 646
- Findings: none
- Open gaps: 5: Which meals get ribbons and when
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: independent       # rides on cooking; my read
goal: "Ribbons on the meals that matter, all meals 150 then 180"
coverage: partial
ladder:
  - {tier: 1, target: "ribbon the speed meals first (Egg, Turkey), lowest ribbon 4 -> higher", source: "my_read", date: "2026-11-27"}
  - {tier: 2, target: "74/74 meals at 150", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "74/74 meals at 180", source: "Toolbox", date: "2026-11-27"}
objective: {rung: 1, now: "25/74 meals ribboned, lowest rank 4, highest 19", target: null, eta_days: null}
check: {cadence: daily, who: "Autiszemo", look_at: "ribbon shelf (18 queued), combine two ribbons into a higher one (Griffy 2026-10-28)"}
buffs:
  - {source: "timed: daily ribbons (talent 133, grimoire 32, sushi 20)", world: 4, owned: true, now: null, next: null, owner: "Autiszemo"}
triggers:
  - {when: "shelf has 2 of the same ribbon", then: "combine and place on the top speed meal"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Combine shelf ribbons and place on Egg/Turkey", stat: "meal cooking speed", gain_pct: null, unblocks: [cooking], source: "Griffy", active_min: 3, wait_hr: null, cost: null, urgent: false}
# GAP 5: which meals get ribbons and when, needs a creator order
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
