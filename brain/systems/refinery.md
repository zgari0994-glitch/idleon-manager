---
name: refinery
description: Refinery: state, how it works, links, plan, today
---
# Refinery

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistastic
- Toolbox: world-3/refinery (guide L93)
- AutoReview: Refinery
- Planner: model/refinery.py
- Creator rows: 202
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 5 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: feeder
goal: "Rank salts toward the next locked salt (7/9 unlocked) without starving gear crafts (Griffy 2026-10-04)"
coverage: sourced
ladder:
  - {tier: 1, target: "Fix AutoReview deficits: Red 39 (-164/cycle), Orange 29 (-236), Green 20 (-29), Purple 17 (-33)", source: "AutoReview", date: "2026-11-28"}
  - {tier: 2, target: "Purple auto-refine off to rank toward the next salt; Red + Green auto off", source: "Griffy", date: "2026-10-04"}
  - {tier: 3, target: "Salt 8 then 9 unlocked (void-tier gear)", source: "Griffy", date: "2026-10-04"}
objective: {rung: 1, now: "4 salts in deficit, 7/9 unlocked", target: "0 deficits", eta_days: null}
check: {cadence: daily, who: "Autistastic", look_at: "auto-refine toggles, salt balance vs next rank cost"}
buffs:
  - {source: "Connected lab bonus triples refinery (Griffy 2026-10-16); Doot Omniphau AFK progress", world: 3, owned: null, now: null, next: null, owner: "Autistocat (lab)"}
triggers:
  - {when: "a salt goes to excess", then: "rank it up or let it feed the next tier"}
  - {when: "gear craft needs salts", then: "hold refining that salt until crafted"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Set auto-refine: Red off, Green off, Purple off; cover the Orange deficit first (largest)", stat: "salts", gain_pct: null, unblocks: ["armor_sets"], source: "Griffy 2026-10-04 N5yJ4-tZLbY 19:26", active_min: 2, wait_hr: null, cost: null, urgent: false}
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
