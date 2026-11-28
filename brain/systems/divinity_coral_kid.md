---
name: divinity_coral_kid
description: Coral Kid: state, how it works, links, plan, today
---
# Divinity: Coral Kid shop

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistabish
- Toolbox: GAP: no Toolbox page mapped
- AutoReview: Coral Kid
- Planner: model/reef.py
- Creator rows: 0
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 8 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder   # divinity -> Class EXP, Blessing cap, Lumi, DMG, Time Elapse
goal: "Coral Kid shop (Divinity tree, paid in Divinity PTS) bought out in a sourced order; 3.21B banked"   # Zack 2026-11-28: own shop under Divinity
coverage: partial   # Griffy/Pulse say why it matters; no creator buy order
ladder:
  - {tier: 1, target: "Keep a divinity point stack for Coral Kid; pre-stack in divinity ballot weeks", source: "Pulse", date: "2026-10-14"}   # NlppEKJNCZM 00:16:17; currency = Div PTS (Zack confirmed 2026-11-28)
  - {tier: 2, target: "my read: Blessing max +4 (93.8M) and volcano link 2.30x Div EXP (34.5M) first, then God Rank Class EXP (396M), then Minor Link (2.16B)", source: "my_read", date: "2026-11-28"}
  - {tier: 3, target: "Unlock the Total Divinity LV gated upgrades (Transmute, Div EXP, Time Elapse on any AFK, Lumi, God Rank DMG)", source: "AutoReview", date: "2026-11-28"}
objective: {rung: 2, now: "volcano 13, blessing +2 levels, class EXP 1, rest 0; 3.21B points", target: "blessing + volcano + class EXP bought", eta_days: null}
check: {cadence: daily, who: "Autistabish", look_at: "coralReef.coralKidUpgrades vs divinity points"}
buffs: []
triggers:
  - {when: "Total Divinity LV hits a gated upgrade's requirement", do: "add it to the buy list"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Buy Blessing max +4 (93.8M Div PTS) and volcano link (34.5M), then God Rank Class EXP (396M) (my read order)", stat: "divinity", gain_pct: null, unblocks: [], source: "my_read + Pulse 2026-10-13 PnEVVlBrUdQ", active_min: 3, wait_hr: null, cost: null, urgent: false}
# Data lives at coralReef.coralKidUpgrades, but data_map.yaml points divinity_coral_kid at divinity (lookup shows divinity data). Griffy: Coral Kid makes divinity endgame relevant (2026-01-29), amplifies Arctis (2026-07-19).
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
