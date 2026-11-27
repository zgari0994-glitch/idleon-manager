---
name: saltlick
description: Saltlick: state, how it works, links, plan, today
---
# Saltlick

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistopher
- Toolbox: world-3/salt-lick (guide L101)
- AutoReview: Salt Lick
- Planner: model/saltlick.py
- Creator rows: 53
- Findings: none
- Checklist: [[saltlick]]: ready to put points in the two sections, or later, with the plan
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: DRAFT
role: feeder            # Refinery Speed + Cooking Mastery lines feed other systems
goal: "Max the 3 open Salt Lick lines, Refinery Speed first because Refinery is A-above-cooking (Griffy 2026-01-29)"
coverage: partial
ladder:
  - {tier: 1, target: "Explosive Salts (Refinery Speed) 76 -> 100", source: "Toolbox", date: "2026-11-27"}
  - {tier: 2, target: "Nullo Salt (Cooking Mastery) 35 -> 100", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "Purple Salt (Damage) 178 -> 250", source: "Toolbox", date: "2026-11-27"}
objective: {rung: 1, now: 76, target: 100, eta_days: null}
check: {cadence: daily, who: "Autistopher", look_at: "Salt Lick buy-now line vs Refinery salt reserve"}
buffs:
  - {source: "timed: salt income from Refinery (Autistastic)", world: 3, owned: true, now: null, next: null, owner: "Autistastic"}
triggers:
  - {when: "Explosive Salts hits 100", then: "switch buys to Nullo Salt, tell cooking owner"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Level Explosive Salts when salts aren't reserved for Refinery", stat: "refinery speed", gain_pct: null, unblocks: [refinery], source: "Toolbox", active_min: 1, wait_hr: null, cost: null, urgent: false}
# my read: rung order Refinery > Cooking Mastery > Damage, no creator order found
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
