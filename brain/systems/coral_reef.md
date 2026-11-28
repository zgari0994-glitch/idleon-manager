---
name: coral_reef
description: Coral Reef: state, how it works, links, plan, today
---
# Coral Reef

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistachio
- Toolbox: world-7/coral-reef (guide L166)
- AutoReview: Coral Reef
- Planner: model/reef.py
- Creator rows: 38
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 7 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: feeder   # coral -> Coral Kid / Dancing Coral upgrades (Divinity, Lumi, DMG)
goal: "Grow daily coral (Coral Restoration +60% first) and buy the cheap Coral Kid levels"
coverage: partial
ladder:
  - {tier: 1, target: "Coral Restoration (Red 10) +60% daily coral", source: "Griffy", date: "2025-11-10"}
  - {tier: 2, target: "Coral Kid cheap levels: Transmute (1), Transmute base (9), Divinity EXP (121), Time Elapsed any AFK (2.2K)", source: "my read (costs from parser)", date: "2026-11-28"}
  - {tier: 3, target: "Stack Divinity PTS ahead of Divinity ballot weeks for Coral Kid", source: "Pulse", date: "2026-10-14"}
objective: {rung: 1, now: "336 coral owned, 3 corals unlocked, Coral Kid total 16 levels", target: "Coral Restoration owned", eta_days: null}
check: {cadence: daily, who: "Autistachio", look_at: "coralReef owned + next Coral Kid costs"}
buffs: []
triggers: []
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Check Coral Restoration (Red 10) is owned; if not it's the first coral buy", stat: "daily coral", gain_pct: 60, unblocks: [], source: "Griffy 2025-11-10 GIs09k2bhkY 00:12:52", active_min: 2, wait_hr: null, cost: null, urgent: false}
  - {do: "Buy the 3 cheapest Coral Kid levels (1, 9, 121)", stat: "Divinity PTS / EXP", gain_pct: null, unblocks: [], source: "parser costs, my read", active_min: 2, wait_hr: null, cost: "1 / 9 / 121", urgent: false}
# Coral Kid cost currency isn't named in the parser (verify in game). Pulse 2026-09-25 rates Coral Restoration C tier vs Griffy "absolute must"; newer is Pulse but Griffy ranks higher; flagged for Zack.
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
