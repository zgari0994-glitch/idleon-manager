---
name: shrines
description: Shrines: state, how it works, links, plan, today
---
# Shrines

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: GAP: no Toolbox page mapped
- AutoReview: none (AutoReview does not rate it)
- Planner: NONE (nothing checks this yet)
- Creator rows: 0
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 12 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: feeder   # damage, drop rate, crystal/giant spawn, class EXP
goal: "Keep all 9 shrines on the farming map leveling; never move them before a big claim"
coverage: sourced
ladder:
  - {tier: 1, target: "All shrines on the farming map for damage + drop rate", source: "Griffy", date: "2026-09-27"}   # GgGwaPlW90M 00:01:17
  - {tier: 2, target: "Place new shrines before large claims (lost XP otherwise)", source: "Griffy", date: "2026-09-21"}   # KHuU392EW-4 01:15:28
  - {tier: 3, target: "Shrine Collective Agreement: moves keep shrine XP", source: "Griffy", date: "2026-11-07"}   # __0_dvPFI_E 00:18:44
  - {tier: 4, target: "Slow burn: Shrine XP ballot is S tier, shrines are time gated", source: "Griffy", date: "2026-01-29"}   # Rr5KiEflTWE 00:09:09
objective: {rung: 1, now: "9/9 placed on map 150, world tour on, levels 22-25 (lowest 22: Crystal, Summereading, Undead, Primordial)", target: null, eta_days: null}
check: {cadence: weekly, who: "unassigned", look_at: "account.shrines"}
buffs: ["Shrine XP ballot week (S tier, Griffy 2026-01-29)"]
triggers:
  - {when: "farming map changes", then: "move shrines (check Collective Agreement first)"}
  - {when: "Shrine XP ballot week", then: "note it, no action needed"}
stall: {pulls_no_progress: 6, eta_over_days: 120}
tasks:
  - {do: "Confirm map 150 is where the farmers AFK; if not, move shrines", stat: "shrine", gain_pct: null, unblocks: [], source: "Griffy", active_min: 3, wait_hr: null, cost: null, urgent: false}
# gap: XP needed per level not in parser (only progress), Collective Agreement ownership unknown, map 150 name not mapped.
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
