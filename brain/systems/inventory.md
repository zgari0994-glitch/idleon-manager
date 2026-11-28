---
name: inventory
description: Inventory: state, how it works, links, plan, today
---
# Inventory

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: GAP: no Toolbox page mapped
- AutoReview: none (AutoReview does not rate it)
- Planner: NONE (nothing checks this yet)
- Creator rows: 0
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 11 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder   # split from storage: storage = chests + bags (Totle); inventory = carry cap + clean bags
goal: "Carry capacity at least Void, preferably Marble, on every character; no useful gear sitting unused"
coverage: partial
ladder:
  - {tier: 1, target: "Carry capacity to Void, then Marble", source: "Griffy", date: "2026-04-23"}   # kD7KZ5zX6Ss 00:07:36
  - {tier: 2, target: "Clear useful gear sitting in inventories (Griffy warning)", source: "Griffy", date: "2026-04-23"}   # kD7KZ5zX6Ss 00:04:03
objective: {rung: 1, now: null, target: "Marble", eta_days: null}
check: {cadence: weekly, who: "Autistotle", look_at: "characters[].carryCapBags, inventorySlots (92-96 now)"}
buffs: []
triggers: []
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Upgrade carry bags below Marble", stat: "carry cap", gain_pct: null, unblocks: [], source: "Griffy", active_min: 10, wait_hr: null, cost: null, urgent: false}
# split rule: bag unlocks (Inventory Bag D, vendor bags) and chests stay in storage.md only, never here.
# gap: carry bag tier per material not mapped (parser gives bag IDs, no names); slots 92-96 vs max unknown.
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
