---
name: alchemy_vials
description: Alchemy Vials: state, how it works, links, plan, today
---
# Alchemy Vials

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistocat
- Toolbox: world-2/vials (guide L80)
- AutoReview: Vials
- Planner: model/alchemy.py
- Creator rows: 241
- Findings: none
- Checklist: [[alchemy_vials]]: is there a plan, or paused for bigger needs, and why
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: DRAFT
role: feeder            # vials are flat multipliers; critters from trapping
goal: "Unlock and level every vial, all to level 4+ first"
coverage: partial
ladder:
  - {tier: 1, target: "Total level 4+ vials 77 -> 83 (Krabbo and library vial first)", source: "Griffy", date: "2026-03-27"}
  - {tier: 2, target: "Unlock vials 80 -> 82 -> 86", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "Maxed vials 52 -> 56 -> 60 -> 65", source: "Toolbox", date: "2026-11-27"}
objective: {rung: 1, now: 77, target: 83, eta_days: null}
check: {cadence: daily, who: "Autistocat", look_at: "vial attempts used (Griffy forgets them, 2026-10-28)"}
buffs:
  - {source: "turtle vial is multiplicative, prioritize (Griffy 2026-09-21)", world: 2, owned: null, now: null, next: null, owner: "Autistocat"}
triggers:
  - {when: "vial hits level 4", then: "next lowest vial"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Use all vial attempts", stat: "vial levels", gain_pct: null, unblocks: [], source: "Griffy", active_min: 1, wait_hr: null, cost: null, urgent: true}
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
