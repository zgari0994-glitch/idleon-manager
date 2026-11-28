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
role: independent
goal: "Never sit at fuel cap; bucks into the cheapest upgrades; push Perfectos (0 so far)"
coverage: data   # creator claims hidden by lookup crash, all below is my read
ladder:
  - {tier: 1, target: "Fuel below cap (now at cap 545.6K, 2.58M over-cap)", source: "data", date: "2026-11-28"}
  - {tier: 2, target: "Spend 4.22T bucks on cheapest upgrades (cheapest 24.3B)", source: "data", date: "2026-11-28"}
  - {tier: 3, target: "First Perfecto (0/20 unique, 60% odds)", source: "data", date: "2026-11-28"}
objective: {rung: 1, now: "fuel 545.6K/545.6K, bucks 4.22T, +393B/hr", target: "fuel under cap", eta_days: null}
check: {cadence: daily, who: "Autisticles", look_at: "fuel vs cap, bucks vs cheapest upgrade"}
buffs:
  - {source: "Phosphorus atom (Sushi Bucks Generator) 0/50", world: 3, owned: true, now: 0, next: 1, owner: "Autistastic"}
triggers:
  - {when: "fuel at cap", then: "spend fuel (next cost 1.77M)"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Spend fuel + bucks: fuel is capped, 4.22T bucks idle", stat: "bucks", gain_pct: null, unblocks: [], source: "data (my read)", active_min: 5, wait_hr: null, cost: null, urgent: true}
# GAP: lookup.py crashes on sushi_station (render_levels int >= str, same bug as gaming); 88 creator rows unseen; fireplace/slot setup not reviewed
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
