---
name: lab_mainframe
description: Lab Mainframe: state, how it works, links, plan, today
---
# Lab Mainframe

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
goal: "Max players connected and wired to the right bonuses (8 of 11 connected)"
coverage: partial
ladder:
  - {tier: 1, target: "Connected players 8 -> 11", source: "Toolbox", date: "2026-11-27"}
  - {tier: 2, target: "More line width/range: summoning range bonus, Wild Boar line width (Griffy 2026-10-16 / 11-07)", source: "Griffy", date: "2026-11-07"}
objective: {rung: 1, now: 8, target: 11, eta_days: null}
check: {cadence: weekly, who: "Autistocat", look_at: "who sits in lab vs who is AFK elsewhere"}
buffs:
  - {source: "Griffy: lab + account dev beats pushing weakly (2026-10-16)", world: 4, owned: null, now: null, next: null, owner: "lab owner"}
triggers:
  - {when: "a character's AFK job frees up", then: "park them in lab if they connect"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Name which 3 characters aren't connected and whether moving them costs a higher-score job", stat: "lab", gain_pct: null, unblocks: ["lab_bonuses"], source: "Toolbox", active_min: 3, wait_hr: null, cost: null, urgent: false}
# NOTE: 3 of 11 off is a choice (AFK jobs) not a hole; Law 2 still checks it
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
