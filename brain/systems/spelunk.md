---
name: spelunk
description: Spelunk: state, how it works, links, plan, today
---
# Spelunk

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistomatic
- Toolbox: world-7/spelunking (guide L162)
- AutoReview: Spelunking
- Planner: model/spelunking.py
- Creator rows: 548
- Findings: none
- Checklist: [[spelunk]]: main goal and never once said "go dig / level / play the minigame". Must be a step
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: blocker   # main account goal system
goal: "Spelunking caves: Chucklemire (DONE) -> Lunarheim -> Bizarrio; each cave boss unlocks an account bonus"
coverage: partial
ladder:
  - {tier: 1, target: "POW 900K (Pillar Coral fish)", source: "Zack", date: "2026-11-21", done: true}   # DONE
  - {tier: 2, target: "Chucklemire boss (Teal Summoning)", source: "Toolbox", date: "2026-11-27", done: true}   # DONE
  - {tier: 3, target: "Lunarheim boss: +30 meal max Lv, +1 super talent pt, +2 gallery slots", source: "Toolbox", date: "2026-11-27"}
  - {tier: 4, target: "Bizarrio boss: Ethereal sigils, +0.2% Prisma bubble mult each", source: "Toolbox", date: "2026-11-27"}
objective: {rung: 3, now: "5 caves, best Lv 29/32/40/51/60", target: "Lunarheim boss", eta_days: null}
check: {cadence: daily, who: "Autistomatic", look_at: "deepest cave Lv, stamina, amber shop next buy (57.8T amber)"}
buffs:
  - {source: "Lore chapters: 2.82/11x POW (25.65%), 172/2200% eff (7.83%), 0/11x amber", world: 7, owned: true, now: null, next: null, owner: "Autistomatic"}
triggers:
  - {when: "Lunarheim boss down", then: "meals +30 max Lv -> cooking; +1 super talent pt; +2 gallery slots -> Tachio"}
  - {when: "Bizarrio boss down", then: "Ethereal sigils -> alchemy owner"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Push Lunarheim: amber shop buys ranked by POW per amber", stat: "POW", gain_pct: null, unblocks: ["cooking", "super_talents", "gallery"], source: "Toolbox", active_min: null, wait_hr: null, cost: null, urgent: false}
# GAP: no creator amber-shop buy order for our stage; Lunarheim boss POW requirement not in parser
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
