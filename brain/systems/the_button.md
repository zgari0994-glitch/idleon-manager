---
name: the_button
description: The Button: state, how it works, links, plan, today
---
# The Button

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autisticles
- Toolbox: world-7/the-button (guide L175)
- AutoReview: The Button
- Planner: model/w7minis.py
- Creator rows: 7
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 8 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder   # once unlocked: Spelunking POW, Class EXP, Cooking Speed, crop evo, masterclass drop rate multis
goal: "Unlock The Button, then press every task as it comes and use both weekly insta skips on walls"
coverage: partial   # bonuses + skips sourced; unlock path from cards, press order my read
ladder:
  - {tier: 1, target: "Unlock The Button (W7 map push + Totle Research level, per cards4)", source: "Toolbox/cards4", date: "2026-11-28"}
  - {tier: 2, target: "Use both weekly insta skips on the walls; insta skip is S tier, only way through some walls", source: "Pulse", date: "2026-09-02"}   # oRTdKQdYJv0 00:22:26
  - {tier: 3, target: "Manta Ray (1.5x all Button bonuses) when it fits", source: "Griffy", date: "2026-07-19"}   # 8C9vFwK6bUg 00:34:18
objective: {rung: 1, now: "locked (totalPresses 0, 0 insta skips/week)", target: "unlocked", eta_days: null}
check: {cadence: daily, who: "Autisticles", look_at: "button.totalPresses + currentTask; until unlocked, the gate on Totle's card"}
buffs: []
triggers:
  - {when: "totalPresses > 0", do: "switch check to the current task requirement + weekly 2 insta skips"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Totle: W7 map push + Research level to unlock Jelly Operator / The Button", stat: "unlock", gain_pct: null, unblocks: [the_button, jelly_operator], source: "cards4 2026-11-28", active_min: null, wait_hr: null, cost: null, urgent: false}
  - {do: "After unlock: spend both weekly insta skips on the hardest wall (Pulse S tier)", stat: "presses", gain_pct: null, unblocks: [], source: "Pulse 2026-09-02 oRTdKQdYJv0 00:22:26", active_min: 2, wait_hr: null, cost: null, urgent: false}
# Presses are heavily time-gated (Pulse 2026-11-16); AutoReview lists 25 press requirements (Slab 500 items, Spelunk LV 27, 133x Class EXP ...). Exact unlock condition not in parser.
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
