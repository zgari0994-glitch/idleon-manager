---
name: construction_buildings
description: Construction Buildings: state, how it works, links, plan, today
---
# Construction Buildings

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistastic
- Toolbox: world-3/buildings (guide L96); world-3/construction (guide L102)
- AutoReview: Buildings
- Planner: model/buildings.py
- Creator rows: 97
- Findings: none
- Checklist: [[construction_buildings]]: only leveling worship towers. Should something else be first
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 6 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: independent   # Law 2 duty for Tastic
goal: "Talent Library + Death Note + Trapper Drone first, shrines to 200 next (Griffy 2026-10/11)"
coverage: sourced
ladder:
  - {tier: 1, target: "Talent Book Library 132 -> 201 (checkout speed)", source: "Griffy", date: "2026-10-28"}
  - {tier: 2, target: "Death Note building while cheap; Trapper Drone 27 -> 50", source: "Griffy", date: "2026-11-07"}
  - {tier: 3, target: "Shrines to 200 (Undead 72, Clover 100, Crescent 102, Pantheon 100, Summereading 100); Voidinator 67 -> 240", source: "AutoReview", date: "2026-11-28"}
objective: {rung: 1, now: "Talent Book Library 132", target: "201", eta_days: null}
check: {cadence: daily, who: "Autistastic", look_at: "build queue, build rate 6.62T"}
buffs:
  - {source: "Shrine Collective Agreement (shrines keep XP when moved)", world: null, owned: null, now: null, next: null, owner: "Autistastic"}
triggers:
  - {when: "a building finishes", then: "queue the next from the ladder"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Keep Talent Book Library + Death Note + Trapper Drone in the build slots", stat: "library speed, multikill", gain_pct: null, unblocks: [library, death_note], source: "Griffy 2026-10-28 C2oiRVIpmq8 01:02:26", active_min: 5, wait_hr: null, cost: null, urgent: false}
# GAP: building costs/build time not in lookup; cog board optimization not covered; Poisonic towers salt-gated (Griffy)
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
