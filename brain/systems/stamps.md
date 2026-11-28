---
name: stamps
description: Stamps: state, how it works, links, plan, today
---
# Stamps

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistopher
- Toolbox: world-1/stamps (guide L72)
- AutoReview: Stamps
- Planner: model/stamps.py
- Creator rows: 490
- Findings: none
- Checklist: [[stamps]]: which tab + which stamp; check the materials aren't needed elsewhere (souls for construction got bricked once)
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder            # Ladle stamp feeds cooking; my read on POW link
goal: "Total stamp levels 9,919 -> 11,000 -> 13,000 without spending reserved materials"
coverage: partial
ladder:
  - {tier: 1, target: "Ladle 160 -> 180, Multitool 180 -> 210", source: "Toolbox", date: "2026-11-27"}
  - {tier: 2, target: "Total stamp levels 11,000", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "Total stamp levels 13,000", source: "Toolbox", date: "2026-11-27"}
  - {tier: 4, target: "Crystalline Stamp exalted", source: "Griffy", date: "2026-10-28"}
objective: {rung: 2, now: 9919, target: 11000, eta_days: null}
check: {cadence: daily, who: "Autistopher", look_at: "next stamp buy vs reserves.yaml (souls got bricked once)"}
buffs:
  - {source: "Prisma/exalted stamp talent, S tier (Pulse 2026-09-25)", world: 6, owned: null, now: null, next: null, owner: "Autistopher"}
triggers:
  - {when: "Ladle hits 180", then: "tell cooking owner, re-rank new-recipe speed"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Level Ladle stamp toward 180 if materials not reserved", stat: "cooking", gain_pct: null, unblocks: [cooking], source: "Toolbox", active_min: 2, wait_hr: null, cost: null, urgent: false}
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
