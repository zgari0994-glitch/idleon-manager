---
name: glimbo
description: Glimbo: state, how it works, links, plan, today
---
# Glimbo

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: world-7/glimbo (guide L171)
- AutoReview: none (AutoReview does not rate it)
- Planner: model/w7minis.py
- Creator rows: 25
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 7 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder   # trades -> vault max levels, drop rate, Tome
goal: "Trade spare resources to Glimbo (not reserved ones); push trades toward Pulse's 1000+"
coverage: sourced
ladder:
  - {tier: 1, target: "All cost-1 trades with the item on hand (Neon Coral, Deepsea Soul, Zenith Cluster, Pirate Anchor, Chapter Five)", source: "data + Pulse spend rule", date: "2026-11-16"}
  - {tier: 2, target: "1000 trades (drop rate, +50 Tome points)", source: "Pulse", date: "2026-09-04"}
  - {tier: 3, target: "1800-1900 trades at late strength", source: "Pulse", date: "2026-11-16"}
objective: {rung: 1, now: "167 trades by parser sum (verify; Pulse's counts are in the thousands)", target: 1000, eta_days: null}
check: {cadence: daily, who: "Autisticles", look_at: "minehead.glimbo cost vs owned"}
buffs: []
triggers: []
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Do every cheap Glimbo trade you can afford, except items reserved (Dreadnought+, candy)", stat: "trades / vault max", gain_pct: null, unblocks: [vault], source: "Pulse 2026-11-16 glvAam8Mol8 00:04:53", active_min: 5, wait_hr: null, cost: null, urgent: false}
  - {do: "Don't craft 24 HR candies for Glimbo", stat: null, gain_pct: null, unblocks: [], source: "Griffy 2026-07-29 _maMoJLg6YE 01:51:21", active_min: null, wait_hr: null, cost: null, urgent: false}
# Pulse S tier: Glimbo VIP pass (+2 vault max per trade) and 1 point in Glimbo Insider. Dreadnought Captain makes prices 5x cheaper (Griffy 2026-07-19). Owned item counts not joined to the trade list = gap.
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
