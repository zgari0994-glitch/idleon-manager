---
name: forge_upgrades
description: Forge Upgrades: state, how it works, links, plan, today
---
# Forge Upgrades

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: world-1/anvil (guide L69); world-1/forge (guide L70)
- AutoReview: Smithing
- Planner: NONE (nothing checks this yet)
- Creator rows: 0
- Findings: none
- Open gaps: 24: Siege Breaker forge AFK: which map (Zack guesses Green Mushrooms) + how it works
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 11 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: feeder   # bars for anvil, armor, vials
goal: "Forge capacity up (Griffy S tier); all 6 forge upgrades already maxed, 16/16 slots"
coverage: sourced
ladder:
  - {tier: 1, target: "Forge Stamp 100 -> 240 (+34.29% cap now)", source: "AutoReview", date: "2026-11-28"}
  - {tier: 2, target: "Arcade Bonus 26 forge capacity 0 -> 101", source: "AutoReview", date: "2026-11-28"}
  - {tier: 3, target: "Godshard Ore card 5 -> 7 stars, Beeg Beeg Forge 1 -> 5", source: "AutoReview", date: "2026-11-28"}
  - {tier: 4, target: "Capacity keeps rising: forge cap is S tier, new bars and Godshard/Dreadlo vials need more", source: "Griffy", date: "2025-01-02"}   # 6Xx0tTVFLBE 00:09:47
objective: {rung: 1, now: 100, target: 240, eta_days: null}   # forge stamp level; cap 2.09M
check: {cadence: weekly, who: "UNASSIGNED", look_at: "python3 tools/lookup.py forge_upgrades"}
buffs: []
triggers:
  - {when: "a new bar tier is needed (anvil tab 4, Lustre set)", then: "raise its forge slot count"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Level Forge Stamp toward 240", stat: "forge cap", gain_pct: null, unblocks: [], source: "AutoReview", active_min: 2, wait_hr: null, cost: null, urgent: false}
  - {do: "Check every character's thread/bar production in forge", stat: "bars", gain_pct: null, unblocks: [], source: "Griffy", active_min: 5, wait_hr: null, cost: null, urgent: false}   # GgGwaPlW90M 00:14:14
# owner: none (Zack 2026-11-28, raised only when needed). gap: open gap 24 Siege Breaker forge AFK map; forge stamp cost not shown.
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
