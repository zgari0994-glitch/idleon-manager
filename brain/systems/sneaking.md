---
name: sneaking
description: Sneaking: state, how it works, links, plan, today
---
# Sneaking

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistacular
- Toolbox: world-6/sneaking (guide L153)
- AutoReview: Sneaking
- Planner: model/sneaking.py
- Creator rows: 312
- Findings: sneaking_charm_rolls
- Open gaps: 19: Path to Sneaking Mastery 2 (Menagerie mission) | 33: Talent pushes must say HOW: Generational Gemstones 368 -> 372 is past the 299 book cap; Max Book checkout vs saving, what raises it | 34: Science Fancy Pen: where it comes from (Jade shop?) and cost | 35: Sneaking plan: mastery 1 -> 2, best-in-slot gear per character, what to target, charms (11 -> 23)
- Checklist: [[sneaking]]: mastery spend (he pushed mastery for the W7 shell job), upgrade order, Jade Emporium, ninja floors for gear, inventory keep/trash
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 4 2026-11-27 (save 20261127T2212): not approved, not in the pipeline -->
```yaml
status: DRAFT
role: feeder
goal: "Open the rest of the Jade Emporium (43/52) and start Moissanite, which multiplies every gemstone"
coverage: partial
ladder:
  - {tier: 1, target: "Moissanite (Bonuses from Gemstones) Lv 0 -> started", source: "Toolbox", date: "2026-11-27"}
  - {tier: 2, target: "Jade Emporium 43 -> 52 unlocked", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "Hats 12 -> 15, Pristine Charms 15 -> 23", source: "Toolbox", date: "2026-11-27"}
  - {tier: 4, target: "Ninja mastery 2 -> 3", source: "my_read", date: "2026-11-27"}
objective: {rung: 1, now: 0, target: 1, eta_days: null}
check: {cadence: daily, who: "Autistacular", look_at: "jade balance vs next emporium cost, door 5 HP"}
buffs:
  - {source: "Wind Walker Tab 5 Generational Gemstones talent", world: 6, owned: true, now: 371, next: 389, owner: ""}
  - {source: "Science Marker (8% jade per crop)", world: 6, owned: null, now: null, next: null, owner: ""}
triggers:
  - {when: "Jade Emporium 52/52", then: "shift to mastery 3 + pristine charms"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Put first levels into Moissanite", stat: "gemstone multi", gain_pct: null, unblocks: [], source: "my_read", active_min: 2, wait_hr: null, cost: null, urgent: false}
  - {do: "Buy next Jade Emporium upgrade when jade covers it", stat: "emporium", gain_pct: null, unblocks: [], source: "Toolbox", active_min: 1, wait_hr: null, cost: null, urgent: false}
# Pulse 2026-11-05: extra jade not needed right now (Jade merit D tier). Emporium unlock costs not shown by lookup.
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
- Daily check (Zack asked to remember), on Autistacular, decide every swap from data: Toolbox world-6/sneaking React state account.sneaking (players[].floor 0-indexed, equipment, inventory, itemsMaxLevel, dropList, gemStones). Confirm placement vs phase; flag KO or >10% detection; min-max gear (best Lotus/Rosaries/Silk Veil/Smoke Bomb on the stack, best gloves on looters, Scroll of Power on one ninja with Rosaries, only highest Gold item of each type kept, alone-belts Black/Yellow/Blue/Green only on a ninja alone); list trash + gems to use; phase gate to the next floor when stacked detection there is 10% or lower (Claude's call); Ninja Knowledge cheapest first, skip Star Sweeping; Jade Emporium buy when an item is ~1-2 days of jade (track jade day over day).
- LESSON: Lotus Flower stealth stacks per floor, so What-if "All together" is wrong for a split team; check "Alone" and live per-ninja detection.
- Item max levels (11-13): Charm 344, Gloves 235, Kunai 250, Nunchaku 300, Gemstone 300. Gem floors (wiki): Aquamarine 2, Malachite 4, Emerald 5, Garnet 6, Starite 9, Firefrost 10. Cheap Lv0 upgrades gated by Pillar Coral levels 1-15 (wiki).
- Floor drops: F2 Aquamarine/Smoke Bomb, F3 Meteorite/Blue Belt/Goodie Bag, F4 Scroll of Power/Gold Coin/Malachite, F5 Silk Veil/Gold Eye/Emerald, F6 Green Belt/Gold Coupon/Garnet, F7 Gold Dagger/Taunting Mark, F8 Leather Gloves/Yellow Belt/Shiny Smoke, F9 Lotus 19%/Gold Scroll 17%/Starite 3.2%, F10 Rosaries 20%/Chainmail Gloves 5%/Firefrost 6%, F11 Thundergloves, F12 Black Belt.
- History: 11-13 plan v2 = 10 stacked on F9, Autistachio F1 alone with Black + Yellow Belt (untied 11-13 with Time Sand). 12 pristine charms missing then, incl. Glowing Veil (1.4x Artifact Find), Bubblegum Law (1.25x KPK). Next Jade Emporium then: Science Fancy Pen 1.72e31.
