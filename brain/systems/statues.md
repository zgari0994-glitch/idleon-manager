---
name: statues
description: Statues: state, how it works, links, plan, today
---
# Statues

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistabish, Autistastic, Autisticles, Autistomatic
- Toolbox: GAP: no Toolbox page mapped
- AutoReview: Statues
- Planner: model/statues.py
- Creator rows: 365
- Findings: none
- Open gaps: 14: Onyx base bonus 3 -> 7: what it means and what to do | 15: Demon Genie card row says 'minimum 3 star' but shows 6 -> 7: what is it really (6 star is max?)
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 4 2026-11-27 (save 20261127T2212): not approved, not in the pipeline -->
```yaml
status: DRAFT
role: feeder
goal: "Pull Kachow (Lv 27) up to the pack (240+) and keep every statue climbing; statues multiply damage, drop, skill power account-wide"
coverage: partial
ladder:
  - {tier: 1, target: "Kachow 27 -> 240 (lowest statue by ~215 levels)", source: "my_read", date: "2026-11-27"}
  - {tier: 2, target: "Startue Exp bubble 171 -> 240", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "Onyx Lantern artifact 4 -> 7", source: "Toolbox", date: "2026-11-27"}
  - {tier: 4, target: "Statues 700-800 range via Double Ain't Nothing legend talent", source: "Pulse", date: "2026-09-25"}
objective: {rung: 1, now: 27, target: 240, eta_days: null}
check: {cadence: daily, who: "Autisticles", look_at: "statue turn-ins (farmed by AFK chars)"}
buffs:
  - {source: "Meritocracy: all statues 1.5x", world: 0, owned: false, now: "not active", next: "vote when on ballot", owner: "Autistronaut"}
  - {source: "Smiley Statue (event shop)", world: 0, owned: false, now: 0, next: 1, owner: ""}
triggers:
  - {when: "Meritocracy statue bonus on the ballot", then: "vote it"}
  - {when: "drop rate >= 30x", then: "start Marble statue progression (Griffy 2026-11-07)"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Turn in Kachow statues first until it reaches 240", stat: "Kachow Lv", gain_pct: null, unblocks: [], source: "my_read", active_min: 2, wait_hr: null, cost: null, urgent: false}
  - {do: "Level Startue Exp bubble 171 -> 240", stat: "statue exp", gain_pct: null, unblocks: [], source: "Toolbox", active_min: 2, wait_hr: null, cost: null, urgent: false}
# owner Ticles (Zack 2026-11-27); farmers (Bish, Tastic, Matic) keep their statue jobs on their own cards.
# Tastic AFK line says "Dragon Statue 4 -> 150" but Dragon Statue is already Lv 187: AFK line is stale.
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
