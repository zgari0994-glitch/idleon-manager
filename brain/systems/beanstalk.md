---
name: beanstalk
description: Beanstalk: state, how it works, links, plan, today
---
# Beanstalk

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autiszemo
- Toolbox: world-6/beanstalk (guide L155)
- AutoReview: Beanstalk
- Planner: model/beanstalk.py
- Creator rows: 60
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 7 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder   # golden food -> account-wide food bonuses
goal: "Every golden food deposited to the next tier, Griffy's 5 first (Ham, Cheese, Grilled Cheese, Hamsters, Dumplings)"
coverage: sourced
ladder:
  - {tier: 1, target: "Every owned golden food at 10K deposited (account-wide)", source: "Griffy", date: "2026-11-07"}
  - {tier: 2, target: "Griffy's 5 to 100K (Ham, Cheese, Grilled Cheese, Hamsters, Dumplings)", source: "Griffy", date: "2026-04-23"}
  - {tier: 3, target: "Every golden food to 100K, then 1M", source: "Griffy", date: "2026-11-07"}
objective: {rung: 1, now: "35 slots: 2 at 1M tier, 10 at 100K, 2 at 10K, 21 at 0", target: "the 21 at 0 reach 10K", eta_days: null}
check: {cadence: daily, who: "Autiszemo", look_at: "beanstalkData tiers + AutoReview Beanstalk rows"}
buffs: []
triggers: []
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Stack golden food on one character (the active farmer) and deposit at 10K", stat: "golden food tier", gain_pct: null, unblocks: [], source: "Griffy 2026-11-07 __0_dvPFI_E 00:20:30", active_min: 5, wait_hr: null, cost: null, urgent: false}
  - {do: "Golden Cake 1.90K -> 10K (Smithing)", stat: "tier 1", gain_pct: null, unblocks: [], source: "AutoReview", active_min: null, wait_hr: null, cost: null, urgent: false}
  - {do: "Golden Peanut 10.9K -> 100K and Golden Bread 15.2K -> 100K (Smithing; Bread W3 Colo efficient / W5 Colo fast)", stat: "tier 2", gain_pct: null, unblocks: [], source: "AutoReview + Nocturne 2024-03-02 2sZ62Yvmod4", active_min: null, wait_hr: null, cost: null, urgent: false}
# Names of the 21 empty slots aren't mapped in the parser; some may be foods he doesn't own yet. Golden-food swap advice lives with golden food (Zack 2026-11-27).
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
