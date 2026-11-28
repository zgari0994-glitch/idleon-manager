---
name: companions
description: Companions: state, how it works, links, plan, today
---
# Companions

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: GAP: no Toolbox page mapped
- AutoReview: none (AutoReview does not rate it)
- Planner: NONE (nothing checks this yet)
- Creator rows: 0
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 10 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: independent
goal: "Own the top creator pets: Doot (S), Rift Slug (A), Ancient Golem (A)"
coverage: partial   # tiers sourced, owned data bad
ladder:
  - {tier: 1, target: "Fix data: parser shows only 1 acquired (Coralcave Guardian via token #141), almost certainly a bad read", source: "my_read", date: "2026-11-28"}
  - {tier: 2, target: "Doot owned (S, early-to-late power, falls off endgame)", source: "Griffy", date: "2026-07-19"}   # 8C9vFwK6bUg 00:01:01
  - {tier: 3, target: "Rift Slug + Ancient Golem (A)", source: "Griffy", date: "2026-07-19"}
objective: {rung: 1, now: 1, target: null, eta_days: null}
check: {cadence: weekly, who: "unassigned", look_at: "companions.list[].acquired"}
buffs: []
triggers:
  - {when: "new companion token", then: "spend on highest-tier unowned pet"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Count owned pets in game, compare with parser (1)", stat: "data", gain_pct: null, unblocks: [], source: "my_read", active_min: 2, wait_hr: null, cost: null, urgent: true}
# gap: acquired flag unreliable (storedPets 0, 179 open); fix parser before any pet ranking.
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
