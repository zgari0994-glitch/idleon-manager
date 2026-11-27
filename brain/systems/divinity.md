---
name: divinity
description: Divinity: state, how it works, links, plan, today
---
# Divinity

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistabish
- Toolbox: world-5/divinity (guide L122)
- AutoReview: Divinity
- Planner: model/divinity.py
- Creator rows: 576
- Findings: none
- Checklist: [[divinity]]
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: DRAFT
role: independent       # timed, mostly self-running
goal: "All deities blessed to 134, high offering only at 100% chance"
coverage: partial
ladder:
  - {tier: 1, target: "Flutterbis 75, Kattlekruk 88, Bagur 63 all to 100", source: "Toolbox", date: "2026-11-27"}
  - {tier: 2, target: "Goharut 109, Omniphau 103 to 134", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "all 10 deities 134", source: "Toolbox", date: "2026-11-27"}
objective: {rung: 1, now: "Bagur 63 / Flutterbis 75 / Kattlekruk 88", target: 100, eta_days: null}
check: {cadence: daily, who: "Autistabish", look_at: "offering: high only if 100% (Hearty Meal 61.76% now), else low + pray"}
buffs:
  - {source: "timed: Doot uses Omniphau AFK procs (Griffy 2026-09-21)", world: 5, owned: null, now: null, next: null, owner: "Autistabish"}
triggers:
  - {when: "a blessing hits 100", then: "move points to the next lowest rung deity"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Low offering + pray until high offering is 100%", stat: "divinity points", gain_pct: null, unblocks: [], source: "Toolbox", active_min: 1, wait_hr: null, cost: null, urgent: false}
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
