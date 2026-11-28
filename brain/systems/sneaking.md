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
<!-- DRAFT synthesis 2026-11-28 batch 1 (claims DB, save 20261128T0256): not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: independent
goal: "Break the floor-5 door with the flower stack + one breaker, fix charms, then climb masteries (now Mastery 2)"
coverage: sourced       # BiS gear not in claims (gap logged)
ladder:
  - {tier: 1, target: "floor-5 door: 8.9e20 of 4.0e23 HP (stack funeral flowers, swap to lotus, one breaker)", source: "Pulse", date: "2026-11-10"}
  - {tier: 2, target: "fix charms on all equipment (about half a week), symbols too", source: "Pulse", date: "2026-11-10"}
  - {tier: 3, target: "Mastery 2 -> 3 and up; new mastery bottom floor = sit for XP in black belts (~100 lv each)", source: "Pulse", date: "2026-11-03"}
  - {tier: 4, target: "gemstones up, Moissanite (bonuses from gemstones) 0 -> leveled; Pulse aims 100K on all", source: "Pulse 2026-11-10; Griffy 2026-04-23", date: "2026-11-10"}
  - {tier: 5, target: "Jade Emporium 43 -> 52 (Science Junk, Laboratory Bling among them)", source: "Griffy 2026-02-21 + 2026-01-29", date: "2026-02-21"}
objective: {rung: 1, now: 8.92e20, target: 4.0e23, eta_days: null}
check: {cadence: daily, who: "Autistacular", look_at: "flower stack, door HP, daily charm rolls (49 pristine left), sneaking window open while AFK"}
method:
  - {rule: "only one pusher/breaker; everyone else stacks funeral flowers on the floor", source: "Pulse", date: "2026-11-10"}
  - {rule: "funeral flowers only stack while the sneaking window is open: keep it open when AFK", source: "Pulse", date: "2026-11-03"}
  - {rule: "point spend: Sneak EXP + actions/hr first; buy upgrades with the discount active", source: "Griffy", date: "2026-11-07 / 2026-10-16"}
  - {rule: "Pristine Charms: best source is the W6 gem shop world bonus", source: "Pulse", date: "2026-11-05"}
  - {rule: "weak Fractal Island progress explains trouble at masteries 7-9", source: "Pulse", date: "2026-11-15"}
buffs:
  - {source: "Moon of Sneak (~500 reachable)", world: 7, owned: null, now: null, next: null, owner: "Autistacular"}
  - {source: "Land rank database stealth for ninja twins (exotic market)", world: 6, owned: null, now: null, next: null, owner: "Autistacular"}
triggers:
  - {when: "flower stack hits the door break point", then: "swap breaker to lotus and break the door"}
  - {when: "new mastery bottom floor", then: "black belts on everyone, sit for XP"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Keep the sneaking window open while AFK, stack flowers", stat: "door damage", gain_pct: null, unblocks: [], source: "Pulse 2026-11-03", active_min: 1, wait_hr: 24, cost: null, urgent: false}
  - {do: "Use daily charm rolls on the lowest charms", stat: "charm levels", gain_pct: null, unblocks: [], source: "Pulse 2026-11-10", active_min: 5, wait_hr: null, cost: null, urgent: false}
  - {do: "Buy Sneak EXP / actions-per-hr upgrades with discount on", stat: "sneak EXP", gain_pct: null, unblocks: [], source: "Griffy 2026-11-07", active_min: 2, wait_hr: null, cost: null, urgent: false}
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
