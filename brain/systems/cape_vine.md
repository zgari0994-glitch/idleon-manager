---
name: cape_vine
description: Cape Vine: state, how it works, links, plan, today
---
# Cape Vine

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistachio
- Toolbox: world-4/cape-vine (guide L115)
- AutoReview: Cape Vine
- Planner: model/capevine.py
- Creator rows: 27
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 7 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: multiplier   # vine multiplies deposited cape bonuses
goal: "Deposit every owned cape and put golden vines on the strongest capes"
coverage: partial
ladder:
  - {tier: 1, target: "All owned capes deposited (15/23 now)", source: "AutoReview", date: "2026-11-28"}
  - {tier: 2, target: "Golden vine on the strongest damage/drop cape, not Defence", source: "my read from Pulse (weapons pack 6x damage on golden vine)", date: "2026-11-01"}
  - {tier: 3, target: "More golden vines: Ask Cathy button, class level 1000", source: "Pulse", date: "2026-11-01"}
objective: {rung: 1, now: "15/23 capes, 1 golden vine (on Radiant Amarok Backstabber, +11.5% Defence)", target: "23/23", eta_days: null}
check: {cadence: weekly, who: "Autistachio", look_at: "capeVine capesUsed + golden vine placement"}
buffs: []
triggers: []
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Check Ask Cathy (top left) for free golden vines", stat: "golden vines", gain_pct: null, unblocks: [], source: "Pulse 2026-11-01 7EkdEAkWYng 00:01:04", active_min: 1, wait_hr: null, cost: null, urgent: false}
  - {do: "Move the golden vine off the Defence cape to the best damage or drop rate cape owned", stat: "damage/drop", gain_pct: null, unblocks: [emperor], source: "my read", active_min: 1, wait_hr: null, cost: null, urgent: false}
# The 8 undeposited capes (Easter Egg Backpack, Giant Rose/Violet/Starflower, Dragonroll Mantlepiece, Beeg Egg, Bladed Rucksack, Lovely Balloon) look like event/pack capes; ownership not in parser. Paid packs are his call.
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
