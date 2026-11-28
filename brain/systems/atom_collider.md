---
name: atom_collider
description: Atom Collider: state, how it works, links, plan, today
---
# Atom Collider

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistastic
- Toolbox: world-3/atom-collider (guide L94)
- AutoReview: Atom Collider
- Planner: model/atom.py
- Creator rows: 110
- Findings: none
- Checklist: [[atom_collider]]: never mentioned. Points, tweaks, creator rule
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 6 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: independent
goal: "Spend particles every day; Boron first (Griffy 2026-04-23), then cheapest useful atoms"
coverage: sourced
ladder:
  - {tier: 1, target: "Boron 40 -> 50 (alchemy upgrading)", source: "Griffy", date: "2026-04-23"}
  - {tier: 2, target: "Aluminium Stamp Supercharger 0 -> 50 (printer output feeds it)", source: "Griffy", date: "2026-01-29"}
  - {tier: 3, target: "AutoReview targets: Neon 32->50, Carbon 30->50, Fluoride 30->50, Oxygen 28->50, Magnesium 10->50", source: "AutoReview", date: "2026-11-28"}
objective: {rung: 1, now: "Boron 40/50 (next 410M), particles 61.9M", target: "Boron 50", eta_days: null}
check: {cadence: daily, who: "Autistastic", look_at: "particles vs cheapest atom; Boron cost"}
buffs:
  - {source: "Atom Collider building (Construction 130 -> 200)", world: 3, owned: true, now: 130, next: 200, owner: "Autistastic"}
triggers:
  - {when: "particles > cheapest open atom", then: "spend"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Boron is 410M, out of reach. Spend 51.5M of the 61.9M now: one level each of Aluminium, Lithium, Nitrogen, Hydrogen, Beryllium, Carbon, Oxygen, Sodium, Magnesium (all AutoReview targets), then save for Boron", stat: "particles", gain_pct: null, unblocks: [], source: "Griffy 2026-04-23 kD7KZ5zX6Ss 00:19:52", active_min: 5, wait_hr: null, cost: "61.9M particles", urgent: true}
# Filled 2026-11-28: Boron 410M, Helium 468M, Neon 44.8M. 61.9M is the parser value; confirm in game before spending
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
