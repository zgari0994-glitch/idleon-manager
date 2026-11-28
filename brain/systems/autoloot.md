---
name: autoloot
description: Autoloot: state, how it works, links, plan, today
---
# Autoloot

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: GAP: no Toolbox page mapped
- AutoReview: none (AutoReview does not rate it)
- Planner: NONE (nothing checks this yet)
- Creator rows: 0
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT auto 2026-11-27 (tools/draft_goals.py from lookup: creator claims + AutoReview): not approved, not in the pipeline -->
```yaml
status: DRAFT
auto: true
role: independent
goal: "Turn off autoloot and stand still until enemies approach then walk over the required coin."
coverage: partial
ladder:
  - {tier: 1, target: "Turn off autoloot and stand still until enemies approach then walk over the required coin.", source: "Griffy", date: "2026-04-16"}   # IEJEvG1RkPM 00:36:52
objective: {rung: 1, now: null, target: null, eta_days: null}
check: {cadence: weekly, who: "UNASSIGNED", look_at: "python3 tools/lookup.py autoloot"}
buffs: []   # only filled for systems behind / needing a push
triggers: []
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Turn off autoloot and stand still until enemies approach then walk over the required coin.", stat: "", gain_pct: null, unblocks: [], source: "Griffy", active_min: null, wait_hr: null, cost: null, urgent: false}
# gap: thin creator coverage; rungs from AutoReview / my read (logged in brain/goal_gaps.md)
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
