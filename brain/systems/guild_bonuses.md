---
name: guild_bonuses
description: Guild Bonuses: state, how it works, links, plan, today
---
# Guild Bonuses

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
status: DRAFT
role: independent
goal: "Join a guild: account is in no guild (level 1, 0 GP, 0 members, unlocked false), so all 18 guild bonuses are 0"
coverage: sourced
ladder:
  - {tier: 1, target: "Join an existing active guild (not start one); you get every bonus the guild has earned", source: "Griffy", date: "2026-01-29"}   # Rr5KiEflTWE 00:04:35; V7VpzEe0uek 00:03:34
  - {tier: 2, target: "Log in daily on every character for guild points", source: "Griffy", date: "2026-01-29"}   # dliS5ZjijlA 00:03:40
  - {tier: 3, target: "If leading or small guild: Guild Gifts first, then GP into bonuses", source: "Griffy", date: "2026-11-07"}   # __0_dvPFI_E 01:14:35
objective: {rung: 1, now: "no guild", target: "in a guild", eta_days: null}
check: {cadence: weekly, who: "Zack", look_at: "account.guild"}
buffs: []
triggers:
  - {when: "guild joined", then: "add daily GP line to every card"}
stall: {pulls_no_progress: 3, eta_over_days: 14}
tasks:
  - {do: "Find and join an active guild (Griffy: Discord lists open guilds)", stat: "all guild bonuses", gain_pct: null, unblocks: [], source: "Griffy", active_min: 15, wait_hr: null, cost: null, urgent: true}
# gap: confirm in game that the account really has no guild (parser could miss it); guild ballot = F tier (Griffy).
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
