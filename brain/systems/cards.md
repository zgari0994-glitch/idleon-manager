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
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: DRAFT
role: feeder            # my read: 4 Spelunking cards at 0 stars feed Spelunking EXP/AFK (main goal chain)
goal: "Spelunking cards first, then every slotted card to 6 stars, because cards are flat account stats players neglect (Griffy 2026-10-28)"
coverage: partial
ladder:
  - {tier: 1, target: "Spelunking cards One Way Opening, Plunder Cranny, Kelp Forest, Burned Tunnel at 1+ star (all 0 now)", source: "my_read", date: "2026-11-27"}
  - {tier: 2, target: "Chaotic Troll 4 stars (all-skill efficiency)", source: "Griffy", date: "2026-10-28"}
  - {tier: 3, target: "Crystal Glunko 1+ star (+42% DR passive at max, 0 now)", source: "Toolbox", date: "2026-11-27"}
  - {tier: 4, target: "every slotted card 6 stars", source: "my_read", date: "2026-11-27"}
objective: {rung: 1, now: "0/4 cards at 1 star", target: "4/4", eta_days: null}   # needs drop-rate based ETA, rates.py has no card income yet
check: {cadence: daily, who: "Autistronaut", look_at: "card count of the current rung's card vs nextLevelReq"}
buffs:
  - {source: "card drop rate (drop_rate system, Crystal Glunko)", world: 1, owned: false, now: null, next: null, owner: "Autistronaut"}
triggers:
  - {when: "a rung card hits its star target", then: "move Autistronaut's farm map to the next rung card"}
  - {when: "all 4 Spelunking cards at 1 star", then: "re-rank Spelunking cards vs Chaotic Troll by POW impact"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Farm the cheapest Spelunking card to 1 star", stat: "Spelunking EXP", gain_pct: null, unblocks: [spelunk], source: "my_read", active_min: 5, wait_hr: null, cost: null, urgent: false}
  - {do: "Farm Chaotic Troll toward 4 stars", stat: "all-skill efficiency", gain_pct: null, unblocks: [], source: "Griffy", active_min: 5, wait_hr: null, cost: null, urgent: false}
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
