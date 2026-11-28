---
name: summoning
description: Summoning: state, how it works, links, plan, today
---
# Summoning

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistocat
- Toolbox: world-6/summoning (guide L154)
- AutoReview: Summoning
- Planner: model/summoning.py
- Creator rows: 416
- Findings: none
- Checklist: [[summoning]]: where points go, what to push now, the plan
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder
goal: "Teal Summoning (unlocked by Chucklemire): win the Teal battles, artifact find + damage first"
coverage: partial
ladder:
  - {tier: 1, target: "Teal battles 0 -> win: Danny 9.75x DMG, Monty 1.59x artifact find, Rhea +17.5% DR...", source: "AutoReview", date: "2026-11-27"}
  - {tier: 2, target: "Unlock the 11 locked upgrades (Teal Tirade, Teal Knowledge, Glombolic Units...)", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "Endless 100 -> more (Griffy pushed from 357 on his account)", source: "Griffy", date: "2026-07-29"}
objective: {rung: 1, now: "0 Teal wins", target: "first Teal win", eta_days: null}
check: {cadence: daily, who: "Autistocat", look_at: "essence spend, Teal battle attempt, endless"}
buffs:
  - {source: "White Essence Champ 425 + essence upgrades", world: 6, owned: true, now: null, next: null, owner: "Autistocat"}
triggers:
  - {when: "Monty/Jojo/Mr. K won", then: "tell sailing (Autisticles): artifact odds change"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Attempt first Teal battle; buy essence upgrades that raise army DMG/HP", stat: "army power", gain_pct: null, unblocks: ["sailing"], source: "AutoReview", active_min: 5, wait_hr: null, cost: null, urgent: false}
# GAP: no creator Teal order; jobs.yaml line 179 still says Chucklemire not reached (stale)
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
