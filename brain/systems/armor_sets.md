---
name: armor_sets
description: Armor Sets: state, how it works, links, plan, today
---
# Armor Sets

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistastic
- Toolbox: world-3/armor-smithy (guide L103)
- AutoReview: Armor Sets
- Planner: model/armor.py
- Creator rows: 0
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder            # set bonuses: Prehistoric = W7 skill EXP, Emperor = ribbons/exalted stamps multi
goal: "Every armor set completed for its bonus even when not worn (Griffy 2026-10-28)"
coverage: partial
ladder:
  - {tier: 1, target: "Lustre set bonus obtained (75%) even though Lustre isn't worn", source: "Griffy", date: "2026-11-07"}
  - {tier: 2, target: "Prehistoric Set (W7 skill EXP)", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "Emperor Set (ribbons + exalted stamps multi)", source: "Toolbox", date: "2026-11-27"}
  - {tier: 4, target: "Secret Set (gold food), Godshard Set (summoning winners); 19/19 sets", source: "Toolbox", date: "2026-11-27"}
objective: {rung: 1, now: "15/19 sets unlocked", target: 19, eta_days: null}
check: {cadence: weekly, who: "Autistastic", look_at: "missing parts per set (model/armor.py)"}
buffs:
  - {source: "W6 upgrade stones, buy immediately (Griffy 2026-05-03)", world: 6, owned: null, now: null, next: null, owner: "Autistotle"}
triggers:
  - {when: "a set completes", then: "next set by bonus vs main goal (Prehistoric first if W7 skills on POW chain)"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Craft/farm the cheapest missing part of the lowest open rung", stat: "set bonus", gain_pct: null, unblocks: [], source: "Griffy", active_min: 10, wait_hr: null, cost: null, urgent: false}
# Zack rollout item "anvil + armor": anvil block still missing (nothing bucket)
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

## History and lessons (moved from Project memory 2026-11-21; dated state is history, live data wins)
- 11-14 (superseded goal): Breezy Souls for Tatters of the Gods + Crystal Skull to finish one Godshard set; Autistotle wears it to claim, armor back to Autistastic. Also wants to know each character's golden food/gear and whether upgrading matters now (old doc Gear-and-Food.md).
