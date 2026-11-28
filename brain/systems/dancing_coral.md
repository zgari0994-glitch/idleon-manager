---
name: dancing_coral
description: Dancing Coral: state, how it works, links, plan, today
---
# Dancing Coral

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistachio
- Toolbox: GAP: no Toolbox page mapped
- AutoReview: Dancing Coral
- Planner: model/reef.py
- Creator rows: 0
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 8 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: feeder   # +5% Spelunking POW and +3% amber per Isaccian/Crystal shrine level above 200 -> main goal
goal: "Every Dancing Coral bonus unlocked in order; shrine levels above 200 feed them"
coverage: partial   # Griffy: low coral limits progression; unlock order is the game's, no creator order
ladder:
  - {tier: 1, target: "Unlock 1.04x Class EXP per Pantheon Shrine level above 200: 991 Char Coral (have 159)", source: "AutoReview", date: "2026-11-28"}
  - {tier: 2, target: "Then Research EXP (Clover), Minehead DMG/Money (Summereading), Lumi (Crescent), in game order", source: "AutoReview", date: "2026-11-28"}
  - {tier: 3, target: "Push Isaccian + Crystal shrines past 200 for POW/amber (Spelunking goal)", source: "my_read", date: "2026-11-28"}
objective: {rung: 1, now: "159 Char Coral", target: "991", eta_days: null}
check: {cadence: daily, who: "Autistachio", look_at: "coralReef.dancingCoral + Char Coral"}
buffs: []
triggers:
  - {when: "Char Coral >= 991", do: "unlock Class EXP bonus, next target = Research EXP cost"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Farm Char Coral to 991 for the Class EXP unlock", stat: "Class EXP", gain_pct: null, unblocks: [], source: "AutoReview", active_min: null, wait_hr: null, cost: 991, urgent: false}
  - {do: "Shrine levels above 200 (Isaccian POW, Crystal amber): route to Autistastic's shrine work", stat: "Spelunking POW", gain_pct: null, unblocks: [spelunk], source: "my_read", active_min: null, wait_hr: null, cost: null, urgent: false}
# Removed Griffy Red 4 / Red 10 rows: they're Coral Reef (batch 7). Drop source of Char Coral cut off in AutoReview ("Coralc...").
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
