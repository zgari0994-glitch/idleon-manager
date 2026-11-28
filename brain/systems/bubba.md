---
name: bubba
description: Bubba (W1 clicker): state, how it works, links, plan, today
---
# Bubba (W1 clicker)

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: UNASSIGNED
- Toolbox: none mapped
- AutoReview: not rated
- Planner: NONE (nothing checks this yet)
- Creator rows: 0
- Findings: none
- Open gaps: 1: No AutoReview section: needs goals, upgrade order, daily steps
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 9 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: feeder   # Build Rate 28% -> construction, Total DMG 42%, Soul Gain 14% -> worship, Critter 14% -> trapping, XP 11.2%, All Kills 2.8%, Atom Cost -4.2%
goal: "Keep Bubba's slices spent and climb Megaflesh tiers (each tier multiplies all Bubba bonuses)"
coverage: my_read   # only 3 Griffy mechanic claims, no order
ladder:
  - {tier: 1, target: "Slices never idle: buy every affordable upgrade each check", source: "my_read", date: "2026-11-28"}
  - {tier: 2, target: "Megaflesh 6 Salmon (emulsify a Charisma attribute for 3x)", source: "Toolbox (parser)", date: "2026-11-28"}
  - {tier: 3, target: "Megaflesh 7 Golden (all Bubba bonuses 1.60x)", source: "Toolbox (parser)", date: "2026-11-28"}
  - {tier: 4, target: "Santa's Little Helper triples Bubba bonuses (older 2026-02-14: clicker option does not affect Bubba)", source: "Griffy", date: "2026-07-19"}   # 8C9vFwK6bUg 00:29:11
objective: {rung: 2, now: "3.24T slices, 13.6B/min; Megaflesh lv5 next costs 459T", target: "459T", eta_days: 23}   # my read: (459T-3.24T)/13.6B per min, no other spending
check: {cadence: daily, who: "Autistopher", look_at: "bubba.meatSlices vs upgrades[].cost"}
buffs:
  - {source: "Santa's Little Helper", world: null, owned: null, now: null, next: "3x Bubba bonuses", owner: "account"}   # ownership not in parser
triggers:
  - {when: "meatSlices >= 459T", then: "buy Megaflesh 6 (Salmon), then emulsify Hustle"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Buy the 12 affordable upgrades now (Dice Roll 1.4B, Buyer Grin 2.6B, Bargain 9.1B, Charisma 10B, Great Meat 20B, 2nd Slice 67B, 1st Slice 104B, Happi Boi 117B, Good Meat 444B, Super Chart 661B, More Sides unlock 956B, Smoker/Open Gift 2.9T)", stat: "slices/min + bonuses", gain_pct: null, unblocks: [], source: "my_read (parser costs)", active_min: 3, wait_hr: null, cost: "3.24T slices", urgent: false}
  - {do: "Decide: save for Megaflesh (459T, ~23 days) vs keep buying levels (my read: levels first, they raise slice rate)", stat: "", gain_pct: null, unblocks: [], source: "my_read", active_min: null, wait_hr: null, cost: null, urgent: false}
# Zack 2026-11-28: there is known Bubba tech; find a source before ranking levels vs Megaflesh (task 2 on hold).
# gap: lookup.py has no 'bubba' system; no creator upgrade order; Santa's Little Helper ownership unknown.
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
