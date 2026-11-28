---
name: gemshop
description: Gemshop: state, how it works, links, plan, today
---
# Gemshop

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistotle
- Toolbox: prem-currency/gem-shop (guide L222)
- AutoReview: Gem Shop
- Planner: model/shops.py
- Creator rows: 854
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder            # sample slots feed printer; caverns items feed Bish
goal: "Gems only on permanent multipliers: sample slots, Caverns conjuror/opal, card slots"
coverage: partial
ladder:
  - {tier: 1, target: "Extra sample slot", source: "Griffy", date: "2026-10-28"}
  - {tier: 2, target: "Conjuror Pts (Caverns) 0 -> 1 -> 3 -> 6 -> 12", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "Opal (Caverns) 0 -> 8 -> 20", source: "Toolbox", date: "2026-11-27"}
objective: {rung: 1, now: null, target: null, eta_days: null}   # gem balance + sample slot count need drill-in
check: {cadence: weekly, who: "Autistotle", look_at: "gem balance vs next ladder item price"}
buffs:
  - {source: "gems are a currency, no buffs; one line", world: 0, owned: null, now: null, next: null, owner: "Autistotle"}
triggers:
  - {when: "gems >= next rung price", then: "buy it, next rung"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Buy the next sample slot", stat: "print samples", gain_pct: null, unblocks: [printer], source: "Griffy", active_min: 1, wait_hr: null, cost: null, urgent: false}
# Skip: 6-star card offers (880 gems) too pricey for F2P (Griffy 2026-10-28)
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
