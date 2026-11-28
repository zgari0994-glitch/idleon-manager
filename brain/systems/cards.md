---
name: cards
description: Cards: state, how it works, links, plan, today
---
# Cards

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistronaut
- Toolbox: tools/card-search (guide L241)
- AutoReview: Cards
- Planner: NONE (nothing checks this yet)
- Creator rows: 788
- Findings: none
- Open gaps: 8: What is this character working toward for the account goal | 9: Too informational, not guided: needs do-this-now steps | 40: Run-through output is information, not guidance: makes Zack anxious. Every line must say what to do + how, or not show
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT synthesis 2026-11-28 batch 2 (claims DB, save 20261128T0256): not approved, not in the pipeline -->
```yaml
status: DRAFT
role: feeder
goal: "Get one Drop Rate Multi card started and doubled (Coralcave Guardian first), then the other multi cards; card sets via faster collection"
coverage: partial       # per-role presets + set-tier farming order thin (gap logged)
ladder:
  - {tier: 1, target: "Coralcave Guardian 321 / 400,001 -> 1 star, then double it (~7% DR multi doubled)", source: "Pulse", date: "2026-09-07 / 2026-09-04"}
  - {tier: 2, target: "Mantaray 0 / 6,000,001 and Ancientfish 0 / 20,000,001 started; Ancientfish replaces the lowest additive DR card even at base", source: "Pulse", date: "2026-09-13"}
  - {tier: 3, target: "doubled slots (top left, bottom right) hold whichever multi gives the most DR", source: "Pulse", date: "2026-09-13"}
  - {tier: 4, target: "improve card collection to build card sets before buying more exaltations", source: "Griffy", date: "2026-10-28"}
  - {tier: 5, target: "accuracy/damage cards: Wood Mushroom 5 -> 6 (14.4K of 151K), Bloodbone 5 -> 6 (30.5K of 227K)", source: "Griffy 2025-12-15 / 2026-05-03; counts Toolbox", date: "2026-05-03"}
objective: {rung: 1, now: 321, target: 400001, eta_days: null}
check: {cadence: weekly, who: "Autistronaut", look_at: "DR multi card progress, doubled slots, preset per role"}
done:
  - {item: "Chaotic Troll 6/6 (Griffy target 4 stars, all-skill efficiency)", source: "Griffy 2026-10-28", date: "2026-11-28"}
  - {item: "card drop cards Gigafrog, Snelbie, Sir Stache all 6/6", source: "Griffy 2025-11-14", date: "2026-11-28"}
presets:
  - {role: "drop rate / farming", rule: "DR multi cards in doubled slots; swapping cards alone gave Pulse 50K+ DR", source: "Pulse", date: "2026-09-25"}
  - {role: "EXP farming", rule: "active monster EXP cards are underrated", source: "Griffy", date: "2026-10-28"}
  - {role: "skilling", rule: "Chaotic Troll all-skill efficiency card", source: "Griffy", date: "2026-04-23"}
buffs:
  - {source: "card doubling: W7 + Demon Genie (6/6 owned)", world: 7, owned: true, now: null, next: null, owner: "Autistronaut"}
triggers:
  - {when: "Coralcave Guardian hits 1 star", then: "put it in a doubled slot"}
stall: {pulls_no_progress: 4, eta_over_days: 60}
tasks:
  - {do: "Farm Coralcave Guardian cards with the DR preset", stat: "drop rate multi", gain_pct: null, unblocks: [], source: "Pulse 2026-09-07", active_min: null, wait_hr: 24, cost: null, urgent: false}
  - {do: "Card farming on Elemental Sorcerer (Bish) when a slot is free", stat: "card drops", gain_pct: null, unblocks: [], source: "Griffy 2026-08-03", active_min: null, wait_hr: 8, cost: null, urgent: false}
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
