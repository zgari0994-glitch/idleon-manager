---
name: islands
description: Islands: state, how it works, links, plan, today
---
# Islands

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistastic
- Toolbox: world-2/islands (guide L83)
- AutoReview: Islands
- Planner: model/islands.py
- Creator rows: 109
- Findings: none
- Open gaps: 26: Which islands benefit from drop rate (Tastic owns islands)
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 6 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: independent
goal: "Hold bottles for Fractal (570), never spend on Rando; collect trash for island stamps"
coverage: sourced
ladder:
  - {tier: 1, target: "Collect trash, buy missing island stamps first (Golden Sixes)", source: "Griffy", date: "2026-09-21"}
  - {tier: 2, target: "Unlock Fractal: 570 bottles", source: "data", date: "2026-11-28"}
  - {tier: 3, target: "Shimmer weekly points -> skill efficiency", source: "Griffy", date: "2026-04-23"}
objective: {rung: 2, now: "512 / 570 bottles, +9/day", target: "570", eta_days: 7}
check: {cadence: weekly, who: "Autistastic", look_at: "bottles, trash, Shimmer points"}
buffs: []
triggers:
  - {when: "bottles >= 570", then: "unlock Fractal (my read, Zack 2026-11-28: he saves candy, so Griffy's candy reason to skip does not apply)"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Collect trash; buy any missing island stamp", stat: "stamps", gain_pct: null, unblocks: [], source: "Griffy 2026-09-21 KHuU392EW-4 00:58:30", active_min: 3, wait_hr: null, cost: null, urgent: false}
  - {do: "Spend weekly Shimmer points on skill efficiency", stat: "skill eff", gain_pct: null, unblocks: [], source: "Griffy 2026-04-23 kD7KZ5zX6Ss 00:15:16", active_min: 3, wait_hr: null, cost: null, urgent: false}
# Trash shop costs: Golden Sixes Stamp 80, Bribe set 135, Garbage Gain 202, Stat Wallstreet 300, Filthy Damage book 450, Trash Tuna Nametag 1500
# GAP: trash balance not in parser ('acquired' field meaning unclear)
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
