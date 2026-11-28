---
name: quests
description: Quests: state, how it works, links, plan, today
---
# Quests

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: misc/quests (guide L185)
- AutoReview: none (AutoReview does not rate it)
- Planner: NONE (nothing checks this yet)
- Creator rows: 696
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: independent
goal: "Finish quests that unlock permanent things (Chizoar keys, Death Wish)"
coverage: partial
ladder:
  - {tier: 1, target: "Bellows quest 3 (giant Neyeptune kill) -> daily Chizoar keys", source: "Griffy", date: "2026-11-07"}
  - {tier: 2, target: "Secret-area quest: 777 Bone Meal -> Death Wish", source: "Griffy", date: "2026-10-28"}
objective: {rung: 1, now: null, target: 1, eta_days: null}
check: {cadence: weekly, who: "UNASSIGNED", look_at: "open quest steps; claim ghosts to inventory, not storage"}
buffs:
  - {source: "none, one line", world: 0, owned: null, now: null, next: null, owner: "UNASSIGNED"}
triggers:
  - {when: "Chizoar keys unlocked", then: "add daily key to the owner card"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Kill a giant Neyeptune for Bellows quest 3", stat: "Chizoar keys", gain_pct: null, unblocks: [], source: "Griffy", active_min: 10, wait_hr: null, cost: null, urgent: false}
# OWNER GAP; 76 quests listed, only 2 creator-backed rungs
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
