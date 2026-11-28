---
name: event_points_shop
description: Event Points Shop: state, how it works, links, plan, today
---
# Event Points Shop

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistotle
- Toolbox: misc/event-shop (guide L207)
- AutoReview: Event Shop
- Planner: NONE (nothing checks this yet)
- Creator rows: 0
- Findings: none
- Open gaps: 34: Science Fancy Pen: where it comes from (Jade shop?) and cost
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 10 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: independent   # Totle
goal: "Buy the permanent account boosts from the event shop each event, Glimmerwick Candles whenever offered"
coverage: partial
ladder:
  - {tier: 1, target: "Halloween Event 2026 finished (1.26K stars to finish)", source: "Toolbox (parser)", date: "2026-11-28"}
  - {tier: 2, target: "Off-rotation shop 14/56 -> more owned; Glimmerwick Candles when offered (0.1% nametag)", source: "Griffy", date: "2026-07-19"}
  - {tier: 3, target: "Event tiers 1/3 -> 3/3", source: "Toolbox (parser)", date: "2026-11-28"}
objective: {rung: 1, now: null, target: 1260, eta_days: null}   # stars earned not in parser
check: {cadence: daily, who: "Autistotle", look_at: "_zack.web.eventShop (stars, owned)"}
buffs: []
triggers:
  - {when: "event points cover the next off-rotation item", then: "Totle buys by rank"}
  - {when: "Glimmerwick Candles in shop", then: "buy first"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Rank the 42 unowned off-rotation items (Smiley Statue 1.30x statues, Golden Tome, Stamp Stack, Bubble Broth first, my read)", stat: "account boosts", gain_pct: null, unblocks: [], source: "my_read", active_min: 5, wait_hr: null, cost: null, urgent: false}
# gap: no creator buy order beyond candles; stars earned + points balance not in parser; old objective 8->35 was an item cost, not progress.
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
