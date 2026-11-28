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
status: APPROVED   # Zack 2026-11-28
role: independent
goal: "All P2W maxed (Zack 2026-11-27); only the small buy when the highest alchemy level rises"
coverage: sourced
ladder:
  - {tier: 1, target: "All cauldron, liquid and vial P2W maxed", source: "Zack", date: "2026-11-27"}   # DONE
  - {tier: 2, target: "Buy the new P2W level each time the highest character's alchemy level sets a new high (minor)", source: "Zack", date: "2026-11-27"}
objective: {rung: 2, now: "maxed", target: "next alchemy-level unlock", eta_days: null}
check: {cadence: weekly, who: "Autistocat", look_at: "highest alchemy level vs last P2W unlock"}
buffs: []
triggers:
  - {when: "highest alchemy level rises", then: "buy the new P2W level (minor, low score)"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Buy a 90% Bargain Tag + Dense Water daily, spend most liquid each day", stat: "alchemy", gain_pct: null, unblocks: ["alchemy_bubbles"], source: "Griffy 2026-11-07 __0_dvPFI_E 24:41", active_min: 1, wait_hr: null, cost: null, urgent: false}
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
