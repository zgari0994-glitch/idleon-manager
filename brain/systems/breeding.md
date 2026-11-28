---
name: breeding
description: Breeding: state, how it works, links, plan, today
---
# Breeding

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistacular
- Toolbox: world-4/breeding (guide L111)
- AutoReview: Breeding
- Planner: model/breeding.py
- Creator rows: 593
- Findings: none
- Open gaps: 36: Fence plan from his actual pets: which shinies in, which out, Sheepie 5 -> 13 worth it? | 37: Total Heart VII+ pets 0 -> 68: what it is (heart pets in fence + level?), priority vs shinies, which pets are closest | 38: Crop Depot Crayon 125 -> 330: what it is (farming?)
- Checklist: [[breeding]]: all monsters unlocked/upgraded/spliced. DNA shop spend, how to get DNA faster, Crucible unlock, arena worth it, team comps per spice map (Crypt, Frosty Peaks, Twilight Desert), meta changes per location, heart pets on the fence (level 15 breedability), shiny-rate mobs for overnight shiny leveling, eggs vs upgrades, daily doable steps
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT synthesis 2026-11-28 batch 2 (claims DB, save 20261128T0256): not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder
goal: "Faster-shiny pets to Lv 24-25 first, then meal-bonus shinies, then Crucible to round 250 once Luminous Menagerie opens it"
coverage: sourced       # fence in/out list not in claims (gap logged)
ladder:
  - {tier: 1, target: "faster-shiny-rate shinies Lv 20 -> 24-25 on every critter, then level critter by critter (Faster Shiny Lv Up now +168%)", source: "Zack 2026-11-21 + Pulse", date: "2026-10-31"}
  - {tier: 2, target: "meal-bonus shinies next (meals = strongest shiny bonus; drop rate bonus negligible ~80 total)", source: "Pulse", date: "2026-10-19"}
  - {tier: 3, target: "Crucible round 0 -> 250 (max bonuses, ~3 min run); gated by Luminous Menagerie (Ticles)", source: "Pulse 2026-10-19; gate Zack 2026-11-19", date: "2026-10-19"}
  - {tier: 4, target: "shiny pets for extra Infinite Star Signs", source: "Griffy", date: "2026-10-16"}
  - {tier: 5, target: "replace weak Fleeters, keep pushing Pet Arena (max arena now 247)", source: "Griffy", date: "2026-10-16"}
now_path: "breeding.maxShinyLevel"
objective: {rung: 1, now: 20, target: 24, eta_days: null}
check: {cadence: daily, who: "Autistacular", look_at: "eggs not capped, shiny levels on faster-shiny pets, spices claimed, meals"}
method:
  - {rule: "Wind Walker active is fine for W4 breeding: Whale Wallop cuts breeding timers incl. eggs and shiny level up", source: "Pulse", date: "2026-11-09 / 2026-10-19"}
  - {rule: "Crucible cheese: Rattler, Looter, Refiller, Burger front, Defender + Badom; fight to round 130-150 then toggle high performance off", source: "Pulse", date: "2026-10-19"}
  - {rule: "daily: use eggs, claim spices, check meals, never sit egg-capped", source: "Griffy", date: "2025-12-27"}
  - {rule: "fence: faster-shiny pets first, then meal shinies (my read from the shiny order; no creator fence list)", source: "my_read", date: "2026-11-28"}
buffs:
  - {source: "Luminous Menagerie (Crucible + Shiny OverLVs gate)", world: 7, owned: false, now: null, next: null, owner: "Autisticles"}
triggers:
  - {when: "faster-shiny pets all at Lv 24+", then: "move shiny time to meal-bonus pets"}
  - {when: "Crucible unlocked", then: "run the cheese team to round 250 once"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Wind Walker active on W4 breeding for shiny over levels", stat: "shiny levels", gain_pct: null, unblocks: [], source: "Pulse 2026-11-09", active_min: 30, wait_hr: null, cost: null, urgent: false}
  - {do: "Fence the faster-shiny pets below Lv 24", stat: "Faster Shiny Lv Up", gain_pct: null, unblocks: [], source: "Pulse 2026-10-31 + my read", active_min: 3, wait_hr: 24, cost: null, urgent: false}
  - {do: "Use eggs + claim spices before cap", stat: "eggs", gain_pct: null, unblocks: [], source: "Griffy 2025-12-27", active_min: 2, wait_hr: null, cost: null, urgent: false}
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
- Shiny fence plan (Zack asked to remember), checked on Autistacular: Toolbox Breeding > Shinies > On the fence. When a fence pet hits its phase target, move its copies to the next pet. Fence 26 slots; copies stack linearly; off-fence pets keep their days.
- Order is from gameslikefinder (FAN, unverified; replace with creator source when found): S to 15 -> A to 10 -> B to 5 -> S to 20 -> rest to 20. 11-13 start: Green Mushroom 7, Wode Board 7, Crescent Spud 6, Quenchie 6. S queue: Red Mushroom, Sheepie, Squirrel, Mr Pig, Glublin, Bop Box, Sir Stache, Penguin. A-to-10: Bored Bean, Whale, Carrotman, Gigafrog, Mashed Potato, Sand Giant, Slime, Choccie, Bloque, Dedotated Ram. Mamooth/Soda Can (Artifact Find) wait for the last phase.
- Daily: say exact swaps (pet out, pet in, copies) only when something changes; confirm fence matches plan.
