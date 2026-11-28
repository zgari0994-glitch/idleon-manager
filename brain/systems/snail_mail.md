---
name: snail_mail
description: Snail mail: state, how it works, links, plan, today
---
# Snail mail

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
role: feeder   # gaming snail (Snail Mail drives it)
goal: "Level the Immortal Snail toward max (14/30) on Snail Mail from Meadow runs"
coverage: partial
ladder:
  - {tier: 1, target: "Snail Mail comes from Meadow runs: normal run (no shortcut), go as deep as possible, 3-4 characters", source: "Pulse", date: "2026-11-13"}   # 0DX3KPt_VlM 00:02:26 + 00:02:36
  - {tier: 2, target: "Snail is the top gaming-gains upgrade", source: "Griffy", date: "2026-07-29"}   # _maMoJLg6YE 01:58:43
  - {tier: 3, target: "Skip the Double Snail Mail vote (about 8.5 extra/day)", source: "Pulse", date: "2026-11-13"}   # 0DX3KPt_VlM 00:01:40
objective: {rung: 1, now: 14, target: 30, eta_days: null}
check: {cadence: daily, who: "gaming owner (jobs.yaml)", look_at: "account.gaming.snailLevel / snail"}
buffs: ["Pastel Yellow palette: +7.69% double Snail Mail"]
triggers:
  - {when: "snailLevel >= 30", then: "done, keep encouragement"}
stall: {pulls_no_progress: 4, eta_over_days: 60}
tasks:
  - {do: "Meadow run (normal, deepest) with 3-4 characters for Snail Mail + Blinding Lanterns", stat: "snail", gain_pct: null, unblocks: ["hole lanterns"], source: "Pulse", active_min: 10, wait_hr: null, cost: null, urgent: false}
# data: snail 14/30, success 66.0%, reset 16.4%, encouragement 10, holeBonus 44. Lanterns 12/12 unused.
# gap: Snail Mail balance not in parser (gaming.envelopes = 0.05, meaning unknown); Griffy said maxed at 49 (2026-07-29) vs our maxLevel 30, verify cap.
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
