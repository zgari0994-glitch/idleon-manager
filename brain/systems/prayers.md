---
name: prayers
description: Prayers: state, how it works, links, plan, today
---
# Prayers

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: world-3/prayers (guide L99)
- AutoReview: Prayers
- Planner: model/prayers.py
- Creator rows: 265
- Findings: none
- Checklist: [[prayers]]: clear on/off guidance (Shiny Snitch line contradicted itself)
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: DRAFT
role: feeder            # prayers boost every system; TD unlocks feed new ones
goal: "Clear on/off per character, then level the prayers that matter"
coverage: partial
ladder:
  - {tier: 1, target: "on/off list per card, no contradictions (Shiny Snitch line)", source: "my_read", date: "2026-11-27"}
  - {tier: 2, target: "Midas Minded 35 -> 50, Unending Energy 40 -> 50", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "Shiny Snitch unlocked (Goblin Gorefest wave 81)", source: "Griffy", date: "2026-11-07"}
objective: {rung: 2, now: "Midas 35, Unending 40", target: 50, eta_days: null}
check: {cadence: daily, who: "every_character", look_at: "equipped prayers vs card on/off list"}
buffs:
  - {source: "soul income (worship), 5% soul reserve", world: 3, owned: true, now: null, next: null, owner: "Autistabish"}
triggers:
  - {when: "worship unlocks a prayer", then: "add it to the on/off list"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Level Unending Energy to 50", stat: "AFK", gain_pct: null, unblocks: [], source: "Toolbox", active_min: 1, wait_hr: null, cost: null, urgent: false}
# OWNER GAP: unassigned in jobs.yaml
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
