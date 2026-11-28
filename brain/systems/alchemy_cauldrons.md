---
name: alchemy_cauldrons
description: Alchemy Cauldrons: state, how it works, links, plan, today
---
# Alchemy Cauldrons

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistocat
- Toolbox: world-2/cauldrons (guide L79)
- AutoReview: none (AutoReview does not rate it)
- Planner: model/alchemy.py
- Creator rows: 204
- Findings: none
- Checklist: [[alchemy_cauldrons]] / [[alchemy_bubbles]]: everyone in cauldrons with hard bubbles left. Cranium Cooking run to level pots and find last bubbles, then move people to liquids? Who sits where
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 4 2026-11-27 (save 20261127T2212): not approved, not in the pipeline -->
```yaml
status: DRAFT
role: feeder
goal: "Every cauldron brewing and liquids never capped; liquid is the current bottleneck (Griffy 2026-11-07)"
coverage: partial
ladder:
  - {tier: 1, target: "Quicc cauldron brew speed 0 -> brewing (697M/716M, 0 attempts)", source: "Toolbox", date: "2026-11-27"}
  - {tier: 2, target: "Equinox Liquidvestment 5 -> 11", source: "Zack", date: "2026-11-16"}
  - {tier: 3, target: "Bleach cauldrons owned (Griffy S)", source: "Griffy", date: "2024-04-27"}
objective: {rung: 1, now: 0, target: null, eta_days: null}
check: {cadence: daily, who: "Autistocat", look_at: "brew speed per cauldron, liquids spent"}
buffs:
  - {source: "Cranium Cooking (liquid recovery)", world: 2, owned: true, now: null, next: null, owner: "Autistocat"}
triggers:
  - {when: "a cauldron shows brew speed 0", then: "assign a brewer"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Put a character on the Quicc cauldron", stat: "bubble unlock", gain_pct: null, unblocks: [], source: "my_read", active_min: 1, wait_hr: null, cost: null, urgent: true}
  - {do: "Spend most liquid daily", stat: "liquids", gain_pct: null, unblocks: [], source: "Griffy", active_min: 2, wait_hr: null, cost: null, urgent: false}
# owner Cat (Zack 2026-11-27). Quicc brewer = active task quicc_brew, importance 1.
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
