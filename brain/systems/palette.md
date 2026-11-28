---
name: palette
description: Palette / Black Star: state, how it works, links, plan, today
---
# Palette / Black Star

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: UNASSIGNED
- Toolbox: none mapped
- AutoReview: not rated
- Planner: NONE (nothing checks this yet)
- Creator rows: 0
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 12 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: feeder   # gaming palette, account-wide multipliers
goal: "Black stars on the best colors, then level owned colors in palette weeks"
coverage: partial
ladder:
  - {tier: 1, target: "Pick up a black star or two (first 8 doubler placements are solved)", source: "Pulse", date: "2026-11-12"}   # 6sAjlzBW2sk 00:12:18
  - {tier: 2, target: "Push palette levels during a palette week", source: "Pulse", date: "2026-11-16"}   # glvAam8Mol8 00:07:23
  - {tier: 3, target: "Bright Cyan (Artifact Find) with 2 black stars", source: "Pulse", date: "2026-10-31"}   # _wJJ9siUFLk 00:28:44
objective: {rung: 1, now: "9/37 colors owned, black stars 2 (all on Light Cyan)", target: null, eta_days: null}
check: {cadence: weekly, who: "gaming owner (jobs.yaml)", look_at: "account.gaming.palette + paletteLuck"}
buffs: []
triggers:
  - {when: "palette week in ballot", then: "rung 2, spend on owned colors"}
  - {when: "a new black star is available", then: "place it (rung 1)"}
stall: {pulls_no_progress: 4, eta_over_days: 60}
tasks:
  - {do: "Check black star count + where Pulse's doubler placements go; move/add stars", stat: "palette", gain_pct: null, unblocks: [], source: "Pulse", active_min: 5, wait_hr: null, cost: null, urgent: false}
# data: active Minty Blue L23 (4.68x sprout speed), Offwhite L21 (3.52x bits), Light Cyan L18 (+83.72% double statues, 2 black stars); 6 more at L1; Bright Cyan L0. Palette Luck 3.55 (Rat King 1.75x), final bonus 68.
# gap: color unlock condition, active slot count and black star source not in parser; Pulse's 8 placements not in our claims text.
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
