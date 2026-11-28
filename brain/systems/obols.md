---
name: obols
description: Obols: state, how it works, links, plan, today
---
# Obols

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
status: DRAFT
role: feeder   # drop rate, damage, stats
goal: "Obols toward best-in-slot drop rate; spend 6,009 fragments on rerolls; sort 116 loose obols"
coverage: sourced
ladder:
  - {tier: 1, target: "Glacial Guard random event every time it shows (1/60 BiS drop-rate obol)", source: "Griffy", date: "2026-10-28"}   # C2oiRVIpmq8 01:13:39
  - {tier: 2, target: "Reroll bronze POP obols for +1% before upgrading (POP stops at silver); family board has 12 Silver POP", source: "Griffy", date: "2026-10-16"}   # yxgmoZQ59mY 00:01:41
  - {tier: 3, target: "Keep rare non-droppable obols; skip Chizoar obol upgrade (expensive)", source: "Griffy", date: "2026-11-07"}   # __0_dvPFI_E 00:52:04 / 01:02:48
objective: {rung: 1, now: "124% family DR", target: null, eta_days: null}
check: {cadence: weekly, who: "UNASSIGNED", look_at: "account.obols (stats, inventory 116), currencies.ObolFragments 6009"}
buffs: []
triggers:
  - {when: "Glacial Guard event appears", then: "do it now"}
stall: {pulls_no_progress: 6, eta_over_days: 60}
tasks:
  - {do: "Sort the 116 loose obols: slot upgrades, trash junk", stat: "drop rate", gain_pct: null, unblocks: [], source: "my_read", active_min: 10, wait_hr: null, cost: null, urgent: false}
# gap: per-character obol slots read as 0/3 filled (parser path wrong, not real); Efaunt obol achievement postponed per Griffy.
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
