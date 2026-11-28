---
name: friend_bonuses
description: Friend Bonuses: state, how it works, links, plan, today
---
# Friend Bonuses

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
goal: "Fill the empty friend bonuses: Total Damage + Skill Efficiency are 0 (Griffy: get them for damage and efficiency)"
coverage: sourced
ladder:
  - {tier: 1, target: "3 slots in use, all IdleOnLech: Class EXP 13.5%, Drop Rate 11.2%, Coins 23.3%. Damage, Skill Eff, Skill EXP, Extra Kills = 0", source: "Toolbox", date: "2026-11-28"}
  - {tier: 2, target: "Pick which 3 bonuses the slots hold; Griffy values damage + skill efficiency", source: "Griffy", date: "2026-09-27"}   # GgGwaPlW90M 00:15:30
  - {tier: 3, target: "More slots: Spearfish +1; Piggy doubles bonuses + 2 slots; Slot of Friendship (200) = D tier", source: "Griffy", date: "2026-07-19"}   # 8C9vFwK6bUg 00:17:18 / 00:24:03; Pulse 2026-10-21 D tier
objective: {rung: 1, now: 3, target: null, eta_days: null}   # bonuses filled
check: {cadence: monthly, who: "Zack", look_at: "friendBonusStats"}
buffs: []
triggers: []
stall: {pulls_no_progress: 6, eta_over_days: 90}
tasks:
  - {do: "Decide slot picks (keep Drop Rate/Class EXP/Coins vs swap one to Total Damage or Skill Eff)", stat: "dmg / eff", gain_pct: null, unblocks: [], source: "Griffy", active_min: 5, wait_hr: null, cost: null, urgent: false}
# gap: multiplier 1 (Piggy not owned?), Spearfish ownership not in parser; Griffy: bonuses cap at 12,000 account levels.
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
