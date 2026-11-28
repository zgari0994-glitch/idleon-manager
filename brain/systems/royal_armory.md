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
```yaml
status: APPROVED   # Zack 2026-11-28 (rungs re-based Phase C finish: shelf 230 was hit on save 20261128T0256)
role: feeder
goal: "Next armory shelf (260 levels), then unlock Resource Grades (270) and the next outpost (300)"
coverage: partial   # all rungs from Toolbox data; no creator buy order found
ladder:
  - {tier: 1, target: "Armory levels 230 -> 260 (next shelf)", source: "Toolbox", date: "2026-11-28"}
  - {tier: 2, target: "270 levels unlocks Resource Grades (+1 Grade per refill: +50% max resources, +25% collection), then buy it (61.8K RGres10)", source: "Toolbox", date: "2026-11-28"}
  - {tier: 3, target: "300 levels unlocks Yumyum Outpost PTS (104K RGres11)", source: "Toolbox", date: "2026-11-28"}
now_path: "royalGuardian.armory.totalLevels"
objective: {rung: 1, now: 230, target: 260, eta_days: null}
check: {cadence: daily, who: "Autistastic", helpers: ["Autistomatic"], look_at: "Royal Guardian orbs, outposts, marble, idle deployments"}   # Zack 2026-11-28: Tastic RG #1 owns, Matic RG #2 helps (jobs.yaml)
buffs:
  - {source: "Industrial Politics (outpost rate)", world: 0, owned: null, now: null, next: null, owner: "Autistastic"}
triggers:
  - {when: "Resource Grades cost covered (61.8K RGres10)", when_path: "royalGuardian.resourceStorage[10]", op: ">=", value: 61824, then: "buy Resource Grades once 270 armory levels unlock it", source: "Toolbox"}
  - {when: "marble found", then: "spend on statue unlocks (Griffy 2026-10-16)"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Buy the affordable armory levels each day (cheapest first, card lists them live), Royal Talent Points I 66 -> 200 when covered", stat: "armory levels", gain_pct: null, unblocks: ["shelf 260"], source: "Toolbox", active_min: 2, wait_hr: null, cost: null, urgent: false}
# gap: resource names (RGres0-34) not named in the parser; no creator buy order (Griffy/Pulse) for armory upgrades.
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
