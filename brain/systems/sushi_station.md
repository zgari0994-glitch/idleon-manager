---
name: sushi_station
description: Sushi Station: state, how it works, links, plan, today
---
# Sushi Station

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autisticles
- Toolbox: world-7/sushi-station (guide L172)
- AutoReview: Sushi Station
- Planner: model/w7minis.py
- Creator rows: 88
- Findings: none
- Open gaps: 16: What to do at Sushi Station: keep combining? method?
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 6 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: independent   # feeds Spelunking (triple spelunking POW bonus) + Bubba
goal: "Stop wasting capped fuel, then push tiers for the Bubba meat and Spelunking POW bonuses (Griffy 2026-04-01)"
coverage: sourced
ladder:
  - {tier: 1, target: "Fuel off cap: Fuel Capacity III 0 -> 1 (319M), then Fuel Capacity II/I, Fastburn I/II", source: "data + AutoReview", date: "2026-11-28"}
  - {tier: 2, target: "Bonus tiers: triple Bubba meat slices (Griffy's top pick), triple spelunking POW", source: "Griffy", date: "2026-04-01"}
  - {tier: 3, target: "Griffy high-tier strategy (tier 54, Perfectos) needs research level 52 (Heat of the East Wind)", source: "Griffy", date: "2026-04-01"}
objective: {rung: 1, now: "fuel 546K/546K cap, bucks 4.22T, +393B/hr, 0 Perfectos", target: "Fuel Capacity III 1", eta_days: 0}
check: {cadence: daily, who: "Autisticles", look_at: "fuel vs cap, bucks vs cheapest upgrade"}
buffs:
  - {source: "Phosphorus atom (Sushi Bucks Generator) 0/50, 187K particles", world: 3, owned: true, now: 0, next: 1, owner: "Autistastic"}
triggers:
  - {when: "fuel at cap", then: "buy fuel capacity/fastburn"}
  - {when: "research level 52", then: "start Griffy's high-tier sushi strategy"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Buy Fuel Capacity III (319M), Sushi Tier Vision (1.07B), Shake N' Bake (1.31B), then Fuel Capacity II/I + Fastburn I/II: 4.22T covers all", stat: "fuel cap, bucks", gain_pct: null, unblocks: [], source: "AutoReview + data", active_min: 5, wait_hr: null, cost: "~300B", urgent: true}
# Research is under level 50 (next unlock at 50), so the tier-54 strategy is 2+ levels away (Totle)
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
