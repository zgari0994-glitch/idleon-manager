---
name: lab_jewels
description: Lab Jewels: state, how it works, links, plan, today
---
# Lab Jewels

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistocat
- Toolbox: world-4/laboratory (guide L112)
- AutoReview: none (AutoReview does not rate it)
- Planner: model/lab.py
- Creator rows: 623
- Findings: none
- Checklist: [[lab_chips]] / [[lab_jewels]] / [[lab_mainframe]]: what's missing, how to get there, blockers
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: DRAFT
role: feeder
goal: "All 24 jewels (21/24 now); North Winds + Eternal Energy boost the whole lab"
coverage: partial
ladder:
  - {tier: 1, target: "North Winds Jewel + Eternal Energy Jewel: 1000 Dark Lantern, 10M Sticky Bun, 10K Bamboo Forest spice each", source: "Toolbox", date: "2026-11-27"}
  - {tier: 2, target: "Pure Opal Rhombol (boosts Depot Studies PhD): 5000 Tottoise, 100M Bill Jack Pep, 10K Lullaby Airway spice", source: "Toolbox", date: "2026-11-27"}
objective: {rung: 1, now: "21/24", target: "23/24", eta_days: null}
check: {cadence: weekly, who: "Autistocat", look_at: "Dark Lantern, Sticky Bun and Bamboo Forest counts vs cost"}
buffs:
  - {source: "jewel spinner (Griffy: Sapphire Rhombol cost him 30 Golden Plops)", world: 4, owned: null, now: null, next: null, owner: "lab owner"}
triggers:
  - {when: "North Winds or Eternal Energy bought", then: "re-check which lab bonuses turn on (9 of 18 off now)"}
  - {when: "Pure Opal Rhombol bought", then: "Depot Studies PhD bonus becomes worth wiring"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Stock Sticky Bun (meal) + Bamboo Forest spice + Dark Lantern for the 2 lab-wide jewels", stat: "lab range", gain_pct: null, unblocks: ["lab_bonuses"], source: "Toolbox", active_min: null, wait_hr: null, cost: "2x (1000 / 10M / 10K)", urgent: false}
# GAP: no creator ranking of North Winds vs Eternal Energy vs Pure Opal; my read: lab-wide ones first
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
