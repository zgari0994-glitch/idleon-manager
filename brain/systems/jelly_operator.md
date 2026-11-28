---
name: jelly_operator
description: Jelly Operator: state, how it works, links, plan, today
---
# Jelly Operator

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autisticles
- Toolbox: world-7/jelly-operator (guide L173)
- AutoReview: Jelly Operator
- Planner: model/w7minis.py
- Creator rows: 157
- Findings: none
- Open gaps: 18: Pink Jellyfish unlock: what it takes | 21: Unlock plan + who unlocks it
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 5 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder
goal: "Unlock all 8 cells (3/8 now); each lock is a Research level gate (Research Lv 41)"
coverage: partial
ladder:
  - {tier: 1, target: "Buy Organelle Cell Cultivation 0/1 (314K, affordable: 11.3M bloodcells)", source: "Toolbox", date: "2026-11-28"}
  - {tier: 2, target: "Research 41 -> 42 (Organelle cell), 45-53 (Cell Mutilation, Immuno Weakening, Critical Status, Feverizer, Bloodletting II)", source: "Toolbox", date: "2026-11-28"}
  - {tier: 3, target: "Research 55/64/75/82 for Immunoid, Virus, Mitochondria, Gigacyst", source: "Toolbox", date: "2026-11-28"}
objective: {rung: 1, now: "3/8 cells", target: "4/8", eta_days: null}
check: {cadence: daily, who: "Autisticles", look_at: "3 daily operations, bloodcells vs cheapest OK upgrade"}
buffs:
  - {source: "Bloodcell multi 41.8x: upgrades 13.7, event shop 2, DPS record 1.39", world: 7, owned: true, now: "41.8x", next: null, owner: "Autisticles"}
triggers:
  - {when: "Research level rises (Totle)", then: "re-check which jelly locks opened"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Buy Organelle Cell Cultivation now, then cheapest OK upgrades (Cell Biology 840K, Bloodletting I 1.07M, Daily Transfusion 7/20 1.53M)", stat: "bloodcells", gain_pct: null, unblocks: [], source: "Toolbox", active_min: 2, wait_hr: null, cost: "314K", urgent: true}
# GAP 18 (Pink Jellyfish unlock) + 21 (unlock plan) still open; no creator upgrade order, cheapest-first is my read
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
