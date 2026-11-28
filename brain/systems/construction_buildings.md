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
<!-- DRAFT synthesis 2026-11-28 batch 1 (claims DB, save 20261128T0256): not approved, not in the pipeline -->
```yaml
status: DRAFT
role: independent
goal: "Trapper Drone to 50 and shrines to 200, then Poisonic Elder and the other towers"
coverage: partial       # building order sourced; spare tower levels = my read
ladder:
  - {tier: 1, target: "Trapper Drone 27 -> 50 (Automation Arm alongside)", source: "Griffy", date: "2026-10-04"}
  - {tier: 2, target: "Shrines to 200 (Undead 72, Clover 100, Pantheon 100, Summereading 100, Crescent 102)", source: "Pulse (push shrines + construction boost)", date: "2026-11-12"}
  - {tier: 3, target: "Poisonic Elder 120 -> 240", source: "Griffy", date: "2026-09-27"}
  - {tier: 4, target: "Talent Book Library 132 -> 201", source: "Griffy (Library + Automation Arm important)", date: "2026-07-26"}
  - {tier: 5, target: "spare tower levels: Voidinator 67, Kraken 114, Stormcaller 119 -> 240", source: "my_read", date: "2026-11-28"}
objective: {rung: 1, now: 27, target: 50, eta_days: null}
check: {cadence: daily, who: "Autistastic", look_at: "build queue, Trapper Drone materials (Shiny Scorpions), shrine levels"}
buffs:
  - {source: "Construction build-rate pellet doubler (very strong, meta)", world: 5, owned: null, now: null, next: null, owner: "Autistastic"}
  - {source: "Jewel spinner Sapphire Rhinestone weeks (up to 2 trimmed slots)", world: 7, owned: null, now: null, next: null, owner: "Autistastic"}
  - {source: "Inevitable Builder talent (extra trimmed slot, A tier)", world: 7, owned: null, now: null, next: null, owner: "Autistastic"}
triggers:
  - {when: "Trapper Drone 50", then: "queue Poisonic Elder"}
  - {when: "all shrines 200", then: "spare levels to Voidinator / Kraken / Stormcaller (my read)"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Build Trapper Drone; gather Shiny Scorpions", stat: "Trapper Drone level", gain_pct: null, unblocks: ["trapping"], source: "Griffy 2026-09-27", active_min: 2, wait_hr: null, cost: null, urgent: false}
  - {do: "Level lowest shrine (Undead 72)", stat: "shrine bonuses", gain_pct: null, unblocks: [], source: "Pulse 2026-11-12", active_min: 2, wait_hr: null, cost: null, urgent: false}
# Pulse 2025-10-19 + 2026-10-18 yellow jellyfish meta lives in jelly_operator, not here.
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
