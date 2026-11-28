---
name: royal_armory
description: Royal Armory: state, how it works, links, plan, today
---
# Royal Armory

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistastic
- Toolbox: class-specific/royal-armory (guide L197)
- AutoReview: Royal Armory
- Planner: model/royal_armory.py
- Creator rows: 291
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 4 2026-11-27 (save 20261127T2212): not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder
goal: "Reach the next armory shelf (230 levels) and open Resource Grades + Kingdom Expansions"
coverage: partial
ladder:
  - {tier: 1, target: "Armory levels 226 -> 230 (next shelf)", source: "Toolbox", date: "2026-11-27"}
  - {tier: 2, target: "Unlock Resource Grades (cost 61.8K)", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "Royal Talent Points I 66 -> 200", source: "Toolbox", date: "2026-11-27"}
objective: {rung: 1, now: 226, target: 230, eta_days: null}
check: {cadence: daily, who: "Autistastic", look_at: "Royal Guardian orbs, outposts, marble"}
buffs:
  - {source: "Industrial Politics (outpost rate)", world: 0, owned: null, now: null, next: null, owner: "Autistastic"}
triggers:
  - {when: "shelf 230 reached", then: "next rung"}
  - {when: "marble found", then: "spend on statue unlocks (Griffy 2026-10-16)"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Buy 4 cheapest levels: Resource Replenish (6.35K), Solo Militia (9.94K), Anti-Rodent I (30.8K), Royal Talent Points I (39.5K)", stat: "armory levels", gain_pct: null, unblocks: ["shelf 230"], source: "my_read", active_min: 2, wait_hr: null, cost: "~86.6K", urgent: false}
# 64 locked upgrades, unlock conditions not in parser. Currency balance not shown by lookup.
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
