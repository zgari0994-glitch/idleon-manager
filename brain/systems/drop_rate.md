---
name: drop_rate
description: Drop Rate: state, how it works, links, plan, today
---
# Drop Rate

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: GAP: no Toolbox page mapped
- AutoReview: Drop Rate
- Planner: NONE (nothing checks this yet)
- Creator rows: 662
- Findings: none
- Open gaps: 26: Which islands benefit from drop rate (Tastic owns islands) | 28: Biggie Hours (babaHour) + King Doot (babaMummy): Baba Yaga line, Death Note 'Mini boss', 24h respawn (Toolbox monster data). Not on the Toolbox dashboard, no location in Toolbox wiki. Need: where/how they spawn, whether there's a reason to run them (Death Note rank, drops), then plan on Tastic. Zack: Tastic owns every world boss + Emperor; key-based bosses need tracking
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: DRAFT
role: feeder            # cards, statues, crystals all ride on DR
goal: "Total DR to 30x for Marble statues (Griffy 2026-09-27), via cards first (Pulse S tier)"
coverage: partial
ladder:
  - {tier: 1, target: "DR cards: Crystal Glunko 0 -> 7? stars, Ancient Golem 3 -> 7, Domeo Magmus 3 -> 7", source: "Toolbox", date: "2026-11-27"}
  - {tier: 2, target: "Guild Gold Charm 25 -> 50", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "Golden Cakes (one of the largest sources)", source: "Griffy", date: "2026-11-07"}
  - {tier: 4, target: "30x total drop rate", source: "Griffy", date: "2026-09-27"}
objective: {rung: 1, now: null, target: null, eta_days: null}   # account DR total not in the lookup excerpt
check: {cadence: weekly, who: "UNASSIGNED", look_at: "DR total vs 30x; plunderous kills stop ~1,000"}
buffs:
  - {source: "Glimmerwick Candles on events", world: 0, owned: null, now: null, next: null, owner: "UNASSIGNED"}
triggers:
  - {when: "DR >= 30x", then: "start Marble statue progression (statues owner)"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Farm Crystal Glunko card (shared with cards rung 3)", stat: "drop rate", gain_pct: null, unblocks: [cards, statues], source: "Pulse", active_min: 5, wait_hr: null, cost: null, urgent: false}
# OWNER GAP; gaps 26 + 28 open; AutoReview "(0 -> 7)" means card stars 0 of 7 tiers
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
