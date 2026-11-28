---
name: super_talents
description: Super talents (both presets): state, how it works, links, plan, today
---
# Super talents (both presets)

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: UNASSIGNED
- Toolbox: none mapped
- AutoReview: not rated
- Planner: model/supertalents.py
- Creator rows: 0
- Findings: none
- Open gaps: 3: Plan Topher's Super CHOW rebuild (13 now): which maps first. Settled: counts only on him, WOWs skipped (findings/death_note_two_dbs.md) | 27: Held until transcripts reviewed; Blue Ribbon was an AutoReview target, not Griffy-certified
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 8 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder   # efficiency and kill scaling on every character
goal: "Every open super point spent on the creator pick for that preset; wrong supers reset (about 70 resets, only for a wrong super)"
coverage: sourced   # model/supertalents.py: Griffy 2025-11-28 fo2WwEKsty0 + Pulse 2026-09
ladder:
  - {tier: 1, target: "Reset supers left from old classes (Topher Siege Breaker slots; Totle Extra Bags / Happy Dude not in tree)", source: "Zack rule 2026-11-21", date: "2026-11-21"}
  - {tier: 2, target: "Spend open points in the planner's sourced order (e.g. Tastic Brute Efficiency on skilling)", source: "Griffy + Pulse", date: "2025-11-28"}
  - {tier: 3, target: "More points: Lunarheim lore (+1 Super Talent PTS, Spelunking goal); RG own talents after 290 more Royal Armory levels", source: "Toolbox + Griffy/Pulse", date: "2026-08"}
objective: {rung: 1, now: "Topher + Totle have wrong supers", target: "0 wrong supers", eta_days: null}
check: {cadence: daily, who: "every character (own presets)", look_at: "cards4 Spend: Super talents lines (model/supertalents.py)"}
buffs: []
triggers:
  - {when: "Royal Armory total levels +290", do: "RG supers unlock: Pit of Pages, Marble, Orb, Regal Intervention, Warbound Politics"}
  - {when: "Lunarheim lore boss down", do: "+1 point on every character, spend per planner"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Topher: reset the Siege Breaker supers, re-super per DB list", stat: "DB kills", gain_pct: null, unblocks: [], source: "model/supertalents.py", active_min: 3, wait_hr: null, cost: null, urgent: false}
  - {do: "Totle: reset Extra Bags (fight) and Happy Dude (skill), then spend", stat: "Maestro", gain_pct: null, unblocks: [], source: "model/supertalents.py", active_min: 3, wait_hr: null, cost: null, urgent: false}
  - {do: "Tastic: super Brute Efficiency (skilling preset)", stat: "efficiency", gain_pct: null, unblocks: [], source: "Griffy+Pulse", active_min: 1, wait_hr: null, cost: null, urgent: false}
# Tachio holds 4+4 points: no sourced Beginner pick (held until next master class, Griffy). lookup.py has no super_talents system (gap).
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
