---
name: caverns
description: Caverns: state, how it works, links, plan, today
---
# Caverns

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistabish
- Toolbox: world-5/hole (guide L124)
- AutoReview: Villagers, Shallow Caverns, Glowshroom Tunnels, Underground Overgrowth
- Planner: model/spelunking.py, model/hole.py
- Creator rows: 717
- Findings: hole_caverns_1-5
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: DRAFT
role: independent       # my read; Hole, separate from Spelunking
goal: "Villagers to full implemented unlocks and the next caverns discovered"
coverage: partial
ladder:
  - {tier: 1, target: "Polonai (Explorer) 15 -> 20", source: "Toolbox", date: "2026-11-27"}
  - {tier: 2, target: "Discover Cavern #16 Fountain (15 found)", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "Caverns #17-19 (Trench, Cove, Bruh)", source: "Toolbox", date: "2026-11-27"}
objective: {rung: 1, now: 15, target: 20, eta_days: null}
check: {cadence: daily, who: "Autistabish", look_at: "villager level progress (69%), opals invested, Harp strings"}
buffs:
  - {source: "Harp strings over rupies for schematics (Griffy 2026-10-28)", world: 5, owned: null, now: null, next: null, owner: "Autistabish"}
  - {source: "Conjuror Pts + Opal from gemshop", world: 5, owned: false, now: 0, next: 1, owner: "Autistotle"}
triggers:
  - {when: "Polonai 20", then: "push cavern 16 discovery"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Buy Harp strings before rupies", stat: "schematic resources", gain_pct: null, unblocks: [], source: "Griffy", active_min: 2, wait_hr: null, cost: null, urgent: false}
# Warning: Hole farming over-levels mining/catching chars (Griffy 2026-10-28)
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
