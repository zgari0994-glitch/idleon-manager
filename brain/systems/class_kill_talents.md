---
name: class_kill_talents
description: Class Kill Talents: state, how it works, links, plan, today
---
# Class Kill Talents

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: GAP: no Toolbox page mapped
- AutoReview: none (AutoReview does not rate it)
- Planner: NONE (nothing checks this yet)
- Creator rows: 0
- Findings: none
- Open gaps: 27: Held until transcripts reviewed; Blue Ribbon was an AutoReview target, not Griffy-certified
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 10 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: feeder   # my read: feeds damage/skilling via talent levels
goal: "Define the system first: lookup maps it to plain talents (characters[].talents), not a kill-scaling counter. Until defined, it stays a no-op."
coverage: none
ladder:
  - {tier: 1, target: "Confirm what 'class kill talents' is in Toolbox (kill-scaling talents per class vs plain talent points)", source: "my_read", date: "2026-11-28"}
  - {tier: 2, target: "If kill-scaling: per-character kill counter vs next talent breakpoint, read from parser", source: "my_read", date: "2026-11-28"}
objective: {rung: 1, now: null, target: null, eta_days: null}
check: {cadence: weekly, who: "unassigned", look_at: "none until defined"}
buffs: []
triggers:
  - {when: "system defined + parser path found", then: "redraft ladder with real targets"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Find the Toolbox page for class kill talents and the data path", stat: "unknown", gain_pct: null, unblocks: [], source: "my_read", active_min: 5, wait_hr: null, cost: null, urgent: false}
# data seen: Zemo DB Grimoire 252/308, Marauder Style 151/308 (plain talents, not kill counters).
# gap: no Toolbox page mapped; old auto draft goal ("leveling supplies talent points") was not a real source.
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
