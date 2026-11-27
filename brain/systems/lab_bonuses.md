---
name: lab_bonuses
description: Lab Bonuses: state, how it works, links, plan, today
---
# Lab Bonuses

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: world-4/laboratory (guide L112)
- AutoReview: none (AutoReview does not rate it)
- Planner: model/lab.py
- Creator rows: 623
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: DRAFT
role: feeder
goal: "Every lab bonus that matters connected (9 of 18 off now)"
coverage: my_read
ladder:
  - {tier: 1, target: "Off now: Animal Farm, Gilded Cyclical Tubing, Viaduct of the Gods, My 1st Chemistry Set, Unadulterated Banking Fury, Sigils of Olden Alchemy, Viral Connection, Spiritual Growth, Depot Studies PhD", source: "Toolbox", date: "2026-11-27"}
  - {tier: 2, target: "Order them by what they feed (my read until a creator ranks them)", source: "my_read", date: "2026-11-27"}
objective: {rung: 1, now: "9/18 on", target: null, eta_days: null}
check: {cadence: weekly, who: "UNASSIGNED (model/lab.py says Cat)", look_at: "lab layout: which bonuses are lit"}
buffs:
  - {source: "line width/range: breeding +5% line width, Wild Boar, summoning range, jewels", world: 4, owned: null, now: null, next: null, owner: "lab owner"}
triggers:
  - {when: "a lab-wide jewel or more line width lands", then: "re-layout and re-check which bonuses light"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Confirm in game why each of the 9 is off (out of range vs not unlocked)", stat: "lab", gain_pct: null, unblocks: [], source: "my_read", active_min: 5, wait_hr: null, cost: null, urgent: false}
# GAP: no creator order for lab bonuses; the parser doesn't say off-because-range vs locked
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
