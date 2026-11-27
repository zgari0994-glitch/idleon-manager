---
name: research
description: Research: state, how it works, links, plan, today
---
# Research

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistotle
- Toolbox: world-7/research (guide L163)
- AutoReview: Research
- Planner: model/research.py
- Creator rows: 232
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 4 2026-11-27 (save 20261127T2212): not approved, not in the pipeline -->
```yaml
status: DRAFT
role: feeder
goal: "Level Research and fill the grid by Pulse tiers (S first), find the other 21 observations"
coverage: sourced
ladder:
  - {tier: 1, target: "Optical Monocle 0 -> 1 (Pulse S)", source: "Pulse", date: "2026-09-02"}
  - {tier: 2, target: "Kaleidoscope 4 -> max (Pulse S)", source: "Pulse", date: "2026-09-02"}
  - {tier: 3, target: "Better Button 0 -> 1, Tiny Cogs up (Pulse A)", source: "Pulse", date: "2026-09-22"}
  - {tier: 4, target: "Observations 22 -> 43", source: "Toolbox", date: "2026-11-27"}
objective: {rung: 1, now: 0, target: 1, eta_days: null}
check: {cadence: daily, who: "Autistotle", look_at: "daily rolls (9 left), grid points, research level 41"}
buffs:
  - {source: "Research AFK rate", world: 7, owned: true, now: "42.8%", next: null, owner: "Autistotle"}
triggers:
  - {when: "research level up (grid point)", then: "spend on next ladder rung"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Use the 9 daily rolls", stat: "observations", gain_pct: null, unblocks: [], source: "Toolbox", active_min: 3, wait_hr: null, cost: null, urgent: false}
  - {do: "Next grid point -> Optical Monocle", stat: "kaleidoscope", gain_pct: null, unblocks: [], source: "Pulse", active_min: 1, wait_hr: null, cost: null, urgent: false}
# W7 minis gate "Research ~10" in jobs.yaml is long done (Lv 41). Most grid squares show "Name" in lookup (parser gap).
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
