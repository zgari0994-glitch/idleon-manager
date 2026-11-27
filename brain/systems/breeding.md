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
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: DRAFT
role: feeder
goal: "Shiny pets to their AutoReview targets, faster-shiny-rate pets to 20-25 first (Zack 2026-11-21), then by importance"
coverage: partial
ladder:
  - {tier: 1, target: "Faster-shiny-rate shinies to Lv 20-25 (Faster Shiny Lv Up now +168%)", source: "Zack + Pulse", date: "2026-11-21"}
  - {tier: 2, target: "AutoReview targets, e.g. Sheepie 5 -> 13 + Red Mushroom 5 -> 13 (meals), Mashed Potato/Sand Giant 5 -> 12 (skill eff), Choccie/Slime 5 -> 12 (DR)", source: "AutoReview", date: "2026-11-27"}
  - {tier: 3, target: "Gene Splicing 15 -> 20; Grand Martial of Shinytown 44 -> 300", source: "Toolbox", date: "2026-11-27"}
objective: {rung: 1, now: "507 total shiny Lv", target: null, eta_days: null}
check: {cadence: daily, who: "Autistacular", look_at: "fence pets vs phase targets, overnight WW shiny leveling"}
buffs:
  - {source: "shiny rate: Faster Shiny Mob Lv Up +168% (breeding passives)", world: 4, owned: true, now: "168%", next: null, owner: "Autistacular"}
triggers:
  - {when: "a fence pet hits its phase target", then: "move its copies to the next pet in order"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Overnight WW shiny leveling (breeding_ww job)", stat: "shiny days", gain_pct: null, unblocks: [], source: "Pulse 6JgdYbiEKus 23:23", active_min: 2, wait_hr: 8, cost: null, urgent: false}
# GAP 36 fence plan from his actual pets; GAP 37 Heart VII+ pets 0 -> 68; fence order still FAN (gameslikefinder)
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
