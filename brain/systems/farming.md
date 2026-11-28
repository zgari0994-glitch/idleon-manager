---
name: farming
description: Farming: state, how it works, links, plan, today
---
# Farming

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autiszemo
- Toolbox: world-6/farming (guide L152)
- AutoReview: Farming
- Planner: model/farming.py
- Creator rows: 630
- Findings: none
- Open gaps: 38: Crop Depot Crayon 125 -> 330: what it is (farming?)
- Checklist: [[farming]]: clear goal + method (new crops, shop levels), consistent on collect vs hold, land rank points daily, anything wrong vs creator guidance
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: independent
goal: "Discover crops to unlock OG first, then land rank + shop upgrades (Griffy 2026-11-07)"
coverage: partial
ladder:
  - {tier: 1, target: "crop discoveries for OG unlock", source: "Griffy", date: "2026-11-07"}
  - {tier: 2, target: "Rank Boost 73 -> 100, More Beenz 92 -> 100", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "Stronger Vines 112 -> 170", source: "Toolbox", date: "2026-11-27"}
objective: {rung: 1, now: "208 crops found", target: null, eta_days: null}   # OG threshold count not sourced for this account
check: {cadence: daily, who: "Autiszemo", look_at: "collect, land rank points (465 available), exotic market 2/6"}
buffs:
  - {source: "Exotic market + land rank talents (Pulse A tier)", world: 6, owned: null, now: null, next: null, owner: "Autiszemo"}
triggers:
  - {when: "OG unlocked", then: "switch spend to Rank Boost + exotic market"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Spend 465 land rank points", stat: "rank XP", gain_pct: null, unblocks: [], source: "Toolbox", active_min: 3, wait_hr: null, cost: null, urgent: false}
# GAP 38 Crop Depot Crayon unknown; Griffy's 13/19 crops note is his account, check ours in game
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
- Goal (Zack): unlock new crops. He does NOT claim crops one at a time (guide tip, not his practice).
- Source rule (11-14): land rank points follow Toolbox Farming > Rank Optimizer; Night Market follows Discord 2nd-grind order (OG Fertilizer ~1.6x, Speed GMO 9-10%, EXP GMO 10-15%, Value GMO ~10%, Super GMO 5%+) plus AutoReview Evo GMO target; Day Market uses the fan order (gameslikefinder, FAN) only where nothing higher covers it: Land Plots, Stronger Vines, Product Doubler, More Beenz, Soil, Biology, Rank Boost, Smarter Seeds.
- In game the Night Market shows bonus text + bean cost, not levels: give stop points as displayed bonus + bean cost.
- Day Market plot method (Zack asked to remember): each upgrade costs a crop that shifts with level: crop = floor(cropId + cropIdIncrement x level) (Toolbox account.farming.market, nextUpgrades). Seed ranges: Basic 0-20, Earthy 21-45, Bulbo 46-60, Sushi 61-83, Mushie 84-106, Glassy 107-229, Medal 230-329. One locked plot per upgrade sits on its current crop; when it moves, unlock, climb one, relock. Give a plot -> target crop table.
- Daily steps (11-14): plots (unlock any locked plot with no stockpile reason, flag plots at the top crop of their seed), land ranks from optimizer + new perk thresholds, Day Market, Crop Transfer Ticket daily, Night Market, Beanstalk foods, weekly land rank reset reminder.
- Exotic Market not unlocked (only Day, Night, Crop Depot; fan: 4th Spelunking boss unlocks it). Skip until unlocked even though Toolbox lists it.
