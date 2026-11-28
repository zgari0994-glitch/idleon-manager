---
name: bribes
description: Bribes: state, how it works, links, plan, today
---
# Bribes

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistopher
- Toolbox: world-1/bribes (guide L71)
- AutoReview: Bribes
- Planner: NONE (nothing checks this yet)
- Creator rows: 30
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 9 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: independent   # maintenance, Topher
goal: "All 41 bribes bought (all are permanent account boosts)"
coverage: sourced
ladder:
  - {tier: 1, target: "40/41 bought", source: "Toolbox (parser)", date: "2026-11-28"}   # done
  - {tier: 2, target: "41/41: The Art of the Flail (last one); the Art of the Bail came via Trash Island expeditions", source: "Griffy", date: "2026-10-28"}   # C2oiRVIpmq8 00:03:25
now_path: "bribes[state=bought]|len"
objective: {rung: 2, now: 40, target: 41, eta_days: null}
check: {cadence: weekly, who: "Autistopher", look_at: "bribes[].done (Maintenance job)"}
buffs: []   # maintenance system
triggers:
  - {when: "The Art of the Flail becomes buyable", then: "Topher buys it"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Find what unlocks The Art of the Flail (likely the next Island/W7 gate, my read) and check it in game", stat: "+41 effect", gain_pct: null, unblocks: [], source: "my_read", active_min: 2, wait_hr: null, cost: null, urgent: false}
# gap: Flail unlock condition not in parser or creator rows.
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
