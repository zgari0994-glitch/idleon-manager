---
name: rift
description: Rift: state, how it works, links, plan, today
---
# Rift

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistopher
- Toolbox: world-4/rift (guide L113)
- AutoReview: Rift
- Planner: model/maint.py
- Creator rows: 138
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 5 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: independent
goal: "Rift is complete (65, 'cannot progress further'); only Topher's Super CHOW on the Rift is left"
coverage: sourced
ladder:
  - {tier: 1, target: "Rift 65 cleared", source: "Toolbox", date: "2026-11-28"}   # DONE
  - {tier: 2, target: "Super CHOW on the Rift monster (Autistopher)", source: "AutoReview", date: "2026-11-28"}
objective: {rung: 2, now: "no Super CHOW", target: "Super CHOW done", eta_days: null}
check: {cadence: weekly, who: "Autistopher", look_at: "Rift Super CHOW kill count"}
buffs: []
triggers:
  - {when: "a game update adds rifts", then: "re-open the ladder"}
  - {when: "Super CHOW done", then: "drop to a one-line check"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Fit the Rift Super CHOW into Topher's Super CHOW rotation", stat: "CHOW", gain_pct: null, unblocks: [], source: "AutoReview", active_min: null, wait_hr: null, cost: null, urgent: false}
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
