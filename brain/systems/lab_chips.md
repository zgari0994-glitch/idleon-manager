---
name: lab_chips
description: Lab Chips: state, how it works, links, plan, today
---
# Lab Chips

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistocat
- Toolbox: world-4/laboratory (guide L112)
- AutoReview: none (AutoReview does not rate it)
- Planner: model/lab.py
- Creator rows: 623
- Findings: none
- Checklist: [[lab_chips]] / [[lab_jewels]] / [[lab_mainframe]]: what's missing, how to get there, blockers
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder
goal: "Own every chip worth slotting so each lab player runs its best chip (Griffy: farm a chip's mats before its rotation comes)"
coverage: partial
ladder:
  - {tier: 1, target: "Chocolatey Chip owned (statue/crystal farming)", source: "Griffy", date: "2026-11-07", done: true}   # DONE: 6 owned
  - {tier: 2, target: "Missing chips owned: Grounded Motherboard 0, Grounded Processor 0, Conductive Motherboard 0, Silkrode Nanochip 0", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "Grounded Nanochip 10 -> 11, Conductive Nanochip 5 -> 6", source: "Toolbox", date: "2026-11-27"}
objective: {rung: 2, now: "4 chip types at 0", target: "1+ each", eta_days: null}
check: {cadence: weekly, who: "Autistocat", look_at: "chip repo rotation (now idx 5,3,2), mats for the next missing chip"}
buffs:
  - {source: "Drop-rate chip: remove once DR passes 6x (Griffy 2026-10-16)", world: 4, owned: null, now: null, next: null, owner: "lab owner"}
triggers:
  - {when: "a missing chip enters rotation", then: "buy it that week; it takes a long time to come back (Griffy)"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Check which missing chip is in rotation and stock its mats", stat: "lab", gain_pct: null, unblocks: [], source: "Griffy", active_min: 2, wait_hr: null, cost: null, urgent: false}
# GAP: which missing chips are worth slotting is unsourced; rotation index -> chip name mapping is my read, verify in game
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
