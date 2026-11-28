---
name: sailing
description: Sailing: state, how it works, links, plan, today
---
# Sailing

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autisticles
- Toolbox: world-5/sailing (guide L121)
- AutoReview: Sailing
- Planner: model/sailing.py
- Creator rows: 432
- Findings: sailing_plan
- Checklist: [[sailing]]: captains reviewed, when to trade, how to get a ship to 300 for the buff, right boats/captains/islands
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder
goal: "Artifact find until the missing artifacts and tiers are reachable (Zack 2026-11-26)"
coverage: partial
ladder:
  - {tier: 1, target: "Find the 4 missing: Fang of the Gods, Nomenclature, Me First Dollar, Bloodclot", source: "AutoReview", date: "2026-11-27"}
  - {tier: 2, target: "18 artifacts at tier 4 -> 5 (Gummy Orb, Fury Relic, Weatherbook, Crystal Steak...)", source: "AutoReview", date: "2026-11-27"}
  - {tier: 3, target: "tier 5 -> 6 (11 at 5, 8 at 6)", source: "AutoReview", date: "2026-11-27"}
objective: {rung: 1, now: "37/41 found", target: "41/41", eta_days: null}
check: {cadence: daily, who: "Autisticles", look_at: "captain shop vs Griffy advice, trades, boat upgrades, boat->island sends"}
buffs:
  - {source: "x1 artifact find levers (card ranks them); summoning Teal: Monty 1.59x, Jojo 1.7x, Mr. K 1.81x artifact find", world: 6, owned: false, now: null, next: null, owner: "Autistocat"}
triggers:
  - {when: "Teal summoning artifact-find battles won", then: "re-run odds; recheck which missing artifact is reachable"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Daily captain shop/trades/boat upgrades per the card", stat: "artifact find", gain_pct: null, unblocks: [], source: "Griffy + Toolbox", active_min: 5, wait_hr: null, cost: null, urgent: false}
# Boat 400 out of reach for now (Zack 2026-11-26). 20 boats, 1 at 300
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

## History and lessons (moved from Project memory 2026-11-21; dated state is history, live data wins)
- Autisticles card: read boat/captain assignments, confirm vs artifact targets, say only what changes; captain swaps from verified info only (Toolbox formulas). Goal: artifacts only, as efficiently as possible; accepts short slowdowns (new captain from 1) if better overall.
