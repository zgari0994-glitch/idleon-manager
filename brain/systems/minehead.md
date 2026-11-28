---
name: minehead
description: Minehead: state, how it works, links, plan, today
---
# Minehead

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autisticles
- Toolbox: world-7/minehead (guide L170)
- AutoReview: none (AutoReview does not rate it)
- Planner: model/w7minis.py
- Creator rows: 120
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 5 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: feeder
goal: "Beat more Minehead opponents (9/32, next Threadhead) for its bonuses, 3 tries daily"
coverage: partial
ladder:
  - {tier: 1, target: "3 daily tries used every day", source: "Toolbox", date: "2026-11-28"}
  - {tier: 2, target: "Final-life damage all in (A tier, Pulse 2026-09-02) to beat Threadhead", source: "Pulse", date: "2026-09-02"}
  - {tier: 3, target: "Extra Lives 1/7, Grid Expansion 4/16, Golden Tiles 1/16", source: "Toolbox", date: "2026-11-28"}
objective: {rung: 2, now: "9 beaten, best hit 2.85K, 1.18K currency at 103/hr", target: "Threadhead", eta_days: null}
check: {cadence: daily, who: "Autisticles", look_at: "tries left, currency vs cheapest damage upgrade"}
buffs: []
triggers:
  - {when: "an opponent falls", then: "note its bonus; re-check next opponent's HP"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Use 3 tries; spend currency on Base Damage I/Mega Damage I (cheapest damage)", stat: "minehead dmg", gain_pct: null, unblocks: [], source: "Pulse 2026-09-02 oRTdKQdYJv0 26:01", active_min: 5, wait_hr: null, cost: "137-172", urgent: false}
# Owner = W7 minigames owner (Zack 2026-11-27). GAP: no Griffy guidance for Minehead; opponent HP not in parser; Pulse says rest of J6 points not worth it now
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
