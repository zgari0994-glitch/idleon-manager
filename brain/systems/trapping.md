---
name: trapping
description: Trapping: state, how it works, links, plan, today
---
# Trapping

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistacular
- Toolbox: tools/traps (guide L31); world-3/traps (guide L100)
- AutoReview: Trapping
- Planner: NONE (nothing checks this yet)
- Creator rows: 586
- Findings: none
- Open gaps: 32: Is trapping worth it, W3 auto-grab every 24h (Trapper Drone?), trap setup + what to target
- Checklist: [[trapping]]
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: DRAFT
role: feeder            # critters feed vials + anvil tab 4 (Penguins); "vials vs trapping" open
goal: "Nature traps on every character, critters routed to vials and anvil, a 24h set-and-forget loop"
coverage: partial
ladder:
  - {tier: 1, target: "Nature traps on all 11 characters", source: "Griffy", date: "2026-09-27"}
  - {tier: 2, target: "150,000 bunnies for Dung Beetles", source: "Griffy", date: "2026-11-07"}
  - {tier: 3, target: "Penguins stock for Anvil Tab 4", source: "Griffy", date: "2026-09-27"}
objective: {rung: 1, now: null, target: 11, eta_days: null}   # trap types per char need traps drill-in
check: {cadence: daily, who: "Autistacular", look_at: "traps ready, reset long traps (Royal 40h / Wooden 5d)"}
buffs:
  - {source: "Call Me Ash bubble (trap efficiency)", world: 2, owned: null, now: null, next: null, owner: "Autistocat"}
triggers:
  - {when: "vial critter cost covered", then: "Cat levels the vial (feed alchemy_vials)"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Put Nature traps on every character missing one", stat: "critter gain", gain_pct: null, unblocks: [alchemy_vials, anvil], source: "Griffy", active_min: 10, wait_hr: 24, cost: null, urgent: false}
# GAP 32: worth-it + Trapper Drone auto-grab unsourced; Autistotle shows 8 -> 0 traps in AutoReview
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
