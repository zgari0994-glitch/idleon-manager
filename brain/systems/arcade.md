---
name: arcade
description: Arcade: state, how it works, links, plan, today
---
# Arcade

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autisticles
- Toolbox: world-2/arcade-shop (guide L82)
- AutoReview: Arcade
- Planner: model/arcade.py
- Creator rows: 221
- Findings: none
- Open gaps: 23: Arcade Bonus 0 11 -> 101: how, is it possible
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 4 2026-11-27 (save 20261127T2212): not approved, not in the pipeline -->
```yaml
status: DRAFT
role: feeder
goal: "Spend balls on S/A tier shop bonuses only, skip F tier"
coverage: sourced
ladder:
  - {tier: 1, target: "Spend 292 balls on S tier (Tab 1 talent points first)", source: "Griffy", date: "2025-01-02"}
  - {tier: 2, target: "Spirit Reindeer companion: 2x gold ball shop bonuses (0 -> 1)", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "First omega ball -> S tier bonus", source: "Pulse", date: "2026-10-21"}
objective: {rung: 1, now: 292, target: 0, eta_days: null}
check: {cadence: daily, who: "Autisticles", look_at: "balls 292, gold 47, cosmic 53"}
buffs:
  - {source: "gold ball multi", world: 2, owned: true, now: 3.18, next: null, owner: "Autisticles"}
triggers:
  - {when: "Pulse posts updated arcade tier list", then: "replace Griffy 2025 ladder"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Dump balls into Tab 1 talent points bonus", stat: "talent pts", gain_pct: null, unblocks: [], source: "Griffy", active_min: 2, wait_hr: null, cost: null, urgent: false}
# Base Damage (bonus 0, Lv 11) is Griffy F tier: stop buying it. Tier list is ~11 months old.
# lookup shows "?" for every shop name (parser has bonusName/effect): lookup bug.
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
