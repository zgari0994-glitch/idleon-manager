---
name: world_bosses
description: World bosses (daily/weekly): state, how it works, links, plan, today
---
# World bosses (daily/weekly)

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: UNASSIGNED
- Toolbox: none mapped
- AutoReview: not rated
- Planner: NONE (nothing checks this yet)
- Creator rows: 0
- Findings: none
- Open gaps: 28: Biggie Hours (babaHour) + King Doot (babaMummy): Baba Yaga line, Death Note 'Mini boss', 24h respawn (Toolbox monster data). Not on the Toolbox dashboard, no location in Toolbox wiki. Need: where/how they spawn, whether there's a reason to run them (Death Note rank, drops), then plan on Tastic. Zack: Tastic owns every world boss + Emperor; key-based bosses need tracking
- Checklist: [[world_bosses]] on the lightest-schedule character
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 12 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder   # loot, flobbers, dungeon drops, tome
goal: "Daily world boss in a max party"
coverage: partial
ladder:
  - {tier: 1, target: "Daily world boss in a maxed party; teleporting multiplies boss HP + loot chance", source: "Pulse", date: "2026-09-08"}   # 0xjp2t-iukY 00:13:18
  - {tier: 2, target: "World boss multiplies flobbers + dungeon drops, feeds tome", source: "Pulse", date: "2026-09-08"}   # 0xjp2t-iukY 00:14:19
objective: {rung: 1, now: null, target: "daily", eta_days: null}
check: {cadence: daily, who: "Autistastic\"   # World bosses + minibosses job (jobs.yaml)", look_at: "in game (not in parser)"}
buffs: []
triggers: []
stall: {pulls_no_progress: 6, eta_over_days: 90}
tasks:
  - {do: "Daily world boss in a max party", stat: "loot", gain_pct: null, unblocks: ["tome"], source: "Pulse", active_min: 5, wait_hr: 24, cost: null, urgent: false}
# gap: nothing in parser (no kill/daily flag); claims are 2025, nothing newer from Griffy.
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

## History and lessons (moved from Project memory 2026-11-21; dated state is history, live data wins)
- 11-16: job for the lightest-schedule character, run efficiently, shown whenever available and worth doing. Also covers minibosses before they hit capacity (Toolbox alerts).
