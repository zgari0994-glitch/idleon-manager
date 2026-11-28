---
name: storage
description: Storage: state, how it works, links, plan, today
---
# Storage

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistronaut
- Toolbox: misc/storage (guide L184)
- AutoReview: Storage
- Planner: NONE (nothing checks this yet)
- Creator rows: 148
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 5 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: feeder
goal: "Every storage chest and bag owned (46/50 chests); never lose loot to full storage"
coverage: partial
ladder:
  - {tier: 1, target: "Inventory Bag D on every character missing it (Baba Yaga quest, Zack rule)", source: "AutoReview", date: "2026-11-28"}
  - {tier: 2, target: "Vendor bags: Loot Luggage + Rucksack Of Riches on characters missing them", source: "AutoReview", date: "2026-11-28"}
  - {tier: 3, target: "Storage chests 46 -> 50", source: "Toolbox", date: "2026-11-28"}
objective: {rung: 1, now: "46/50 chests, 539 slots", target: null, eta_days: null}
check: {cadence: weekly, who: "Autistronaut", look_at: "free slots, missing bags per character"}
buffs: []
triggers:
  - {when: "Baba Yaga up", then: "kill her on the next character in card order missing Bag D"}
  - {when: "storage tight", then: "dump cereal/butterflies first, easy to re-farm (Griffy 2026-10-28)"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Buy missing Loot Luggage from the vendor on each character that lacks it", stat: "slots", gain_pct: null, unblocks: [], source: "AutoReview", active_min: 5, wait_hr: null, cost: null, urgent: false}
# GAP: 4th Anniversary Bag is limited/unbuyable now; which 4 chests are locked not named
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
