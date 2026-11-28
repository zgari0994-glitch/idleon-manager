---
name: alchemy_p2w
description: Alchemy P2W: state, how it works, links, plan, today
---
# Alchemy P2W

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistocat
- Toolbox: world-2/cauldrons (guide L79)
- AutoReview: Pay2Win
- Planner: model/alchemy.py
- Creator rows: 204
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 5 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: feeder
goal: "P2W cauldron/liquid/vial levels maxed so brewing never caps; liquid spent daily (Griffy 2026-11-07)"
coverage: partial
ladder:
  - {tier: 1, target: "Power cauldron P2W maxed (speed 150, new bubble 125, boost req 100)", source: "Toolbox", date: "2026-11-28"}   # DONE: costToMax 0
  - {tier: 2, target: "Other 3 cauldrons + liquids + vial attempts P2W maxed", source: "Toolbox", date: "2026-11-28"}
  - {tier: 3, target: "Liquid supply from Cranium Cooking once AC talents pass Lv 200 (Griffy 2026-08-03)", source: "Griffy", date: "2026-08-03"}
objective: {rung: 2, now: "power cauldron maxed, rest unread", target: "all P2W costToMax 0", eta_days: null}
check: {cadence: daily, who: "Autistocat", look_at: "liquid levels, Bargain Tag + Dense Water buy"}
buffs: []
triggers:
  - {when: "all P2W maxed", then: "drop to a one-line check; liquids go fully to Cranium Cooking days"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Buy a 90% Bargain Tag + Dense Water daily, spend most liquid each day", stat: "alchemy", gain_pct: null, unblocks: ["alchemy_bubbles"], source: "Griffy 2026-11-07 __0_dvPFI_E 24:41", active_min: 1, wait_hr: null, cost: null, urgent: false}
# GAP: lookup shows cauldron data, not the p2w block; only power cauldron's costToMax read this batch
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
