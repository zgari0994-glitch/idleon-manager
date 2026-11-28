---
name: npc_tokens
description: Npc Tokens: state, how it works, links, plan, today
---
# Npc Tokens

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: GAP: no Toolbox page mapped
- AutoReview: none (AutoReview does not rate it)
- Planner: NONE (nothing checks this yet)
- Creator rows: 0
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 11 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder   # quests -> keys, stamps, star-talent damage, gaming bits multi
goal: "Daily boss keys from quests: 10 daily Chizoar keys (Bellows quest 3) and Djonnut quest 2 key line"
coverage: sourced
ladder:
  - {tier: 1, target: "Bellows quest 3 (giant Neyeptune) on characters to start daily Chizoar keys; 4-5 chars/week = 10 keys in ~2 weeks", source: "Griffy", date: "2026-11-07"}   # __0_dvPFI_E 00:03:45 / 00:04:46 (he "believes")
  - {tier: 2, target: "Djonnut quest 2 (AFK Moonmen, claim ghosts into inventory not storage)", source: "Griffy", date: "2026-11-07"}   # __0_dvPFI_E 00:03:14 / 00:03:25
  - {tier: 3, target: "Seven-figure Follower for Golden Apple + Steve Sword stamps; more quests = more star-talent damage + gaming bits", source: "Griffy", date: "2026-11-07"}   # __0_dvPFI_E 00:00:26 / 00:06:59
objective: {rung: 1, now: null, target: 10, eta_days: null}   # daily Chizoar keys
check: {cadence: weekly, who: "UNASSIGNED", look_at: "python3 tools/lookup.py npc_tokens"}
buffs: []
triggers: []
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Run Bellows quest 3 on characters that lack it", stat: "Chizoar keys", gain_pct: null, unblocks: [weekly_boss], source: "Griffy", active_min: 15, wait_hr: null, cost: null, urgent: false}
# gap: parser lists quests per NPC but per-character completion was not read, so who's missing Bellows 3 / Djonnut 2 is unknown; Griffy's key claims are "he believes".
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
