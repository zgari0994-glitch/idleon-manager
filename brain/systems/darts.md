---
name: darts
description: Darts: state, how it works, links, plan, today
---
# Darts

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: GAP: no Toolbox page mapped
- AutoReview: Darts
- Planner: NONE (nothing checks this yet)
- Creator rows: 0
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 10 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: independent   # W7 minigame, Baby Boa shop
goal: "Darter Trophy, then level the dart shop (damage, talent pts, vault discount, move speed)"
coverage: partial
ladder:
  - {tier: 1, target: "Darter Trophy", source: "Griffy", date: "2026-04-23"}   # kD7KZ5zX6Ss 01:00:44
  - {tier: 2, target: "Shop: Damage 178%, Talent PTS 15, Vault 1.79x cheaper, Move 7% -> keep raising", source: "AutoReview", date: "2026-11-28"}
objective: {rung: 1, now: 199, target: null, eta_days: null}
check: {cadence: weekly, who: "unassigned", look_at: "AutoReview Darts upgrades"}
buffs: []
triggers:
  - {when: "Darter Trophy owned", then: "rung 2, spend points"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Check Darter Trophy status + spendable dart points in game", stat: "trophy", gain_pct: null, unblocks: [], source: "Griffy", active_min: 3, wait_hr: null, cost: null, urgent: false}
# gap: darts score/points not in minigameHighscores; trophy ownership not in parser; Darter Trophy requirement unknown.
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
