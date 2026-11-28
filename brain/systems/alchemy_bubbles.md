---
name: alchemy_bubbles
description: Alchemy Bubbles: state, how it works, links, plan, today
---
# Alchemy Bubbles

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistocat
- Toolbox: world-2/bubbles (guide L78)
- AutoReview: Bubbles
- Planner: model/alchemy.py
- Creator rows: 1037
- Findings: none
- Checklist: [[alchemy_cauldrons]] / [[alchemy_bubbles]]: everyone in cauldrons with hard bubbles left. Cranium Cooking run to level pots and find last bubbles, then move people to liquids? Who sits where
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder            # big multi-resource bubbles drive prints (Griffy 2026-10-16)
goal: "All bubbles unlocked, then big multi-resource bubbles toward caps"
coverage: partial
ladder:
  - {tier: 1, target: "Unlock 160 total bubbles (155 now), W8 colors 5/5 each", source: "Griffy", date: "2026-10-04"}
  - {tier: 2, target: "Warriors Rule (Printing) 765 -> 950, Stronk Tools 615 -> 630", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "Kill per Kill + Mr Massacre before W6 push", source: "Griffy", date: "2026-11-07"}
objective: {rung: 1, now: 155, target: 160, eta_days: null}
check: {cadence: daily, who: "Autistocat", look_at: "cauldron seats: everyone with hard bubbles left sits in a cauldron"}
buffs:
  - {source: "Diamond Chef (needs level-11 meals); else spend the discount on Mr Massacre", world: 2, owned: null, now: null, next: null, owner: "Autistocat"}
triggers:
  - {when: "160 bubbles unlocked", then: "move cauldron seats to liquids (checklist question, confirm with Zack)"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Level Warriors Rule toward 950", stat: "print output", gain_pct: null, unblocks: [printer], source: "Griffy", active_min: 2, wait_hr: null, cost: null, urgent: false}
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
- Particle routine (Zack asked to remember): pick Alternate Particle Upgrade targets fresh each day from AutoReview Bubbles next-tier targets (sample-boosting orange/green/purple + utility), in its order, cross-checked with Griffy's bubble tiers and the Toolbox bubble table.
- Facts: particles only work on bubbles costing 100M+. 90/day = Boron atom (2/level, lvl 40 = 80) + 10 from "All Hail Purrmep". Recycled Particle Upgrades legend talent auto-spends leftovers on the 1st bubble of each colour (weak, spend manually). More uses: Boron 40->50, cavern "2x daily particle bubble upg".
- Bargain tag (25% off next bubble, stacks to 90%) goes on the priciest resource-paid upgrade, not particle upgrades.
- Every bubble rec gives colour + position (Toolbox Table view order) and checks mats owned vs next cost; split particle (100M+, mats short) / material-paid (affordable) / No Bubble Left Behind.
- Never recommend buying gems with liquid (Zack buys gems with money).
