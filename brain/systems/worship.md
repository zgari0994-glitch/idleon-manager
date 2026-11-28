---
name: worship
description: Worship: state, how it works, links, plan, today
---
# Worship

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistabish
- Toolbox: world-3/worship (guide L98)
- AutoReview: none (AutoReview does not rate it)
- Planner: model/worship.py
- Creator rows: 767
- Findings: none
- Open gaps: 39: Breezy Battle (10) + Citric Conflict (28): one-time proper push plan; worship 500+ needed for Equinox + Menagerie
- Checklist: [[worship]]: green souls, one day of everyone's worship power to hit 1B and max (verify), when
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: DRAFT
role: feeder            # Worship 500+ gates Equinox + Menagerie (gap 39)
goal: "Totem waves high enough to unlock every TD prayer and reach Worship 500+ for Equinox and Menagerie"
coverage: partial
ladder:
  - {tier: 1, target: "Breezy Battle wave 10+", source: "my_read", date: "2026-11-27"}
  - {tier: 2, target: "Citric Conflict wave 28+", source: "my_read", date: "2026-11-27"}
  - {tier: 3, target: "Goblin Gorefest wave 81 (Shiny Snitch prayer)", source: "Griffy", date: "2026-11-07"}
  - {tier: 4, target: "Worship 500+ on the characters Equinox/Menagerie need", source: "my_read", date: "2026-11-27"}
objective: {rung: 1, now: null, target: 10, eta_days: null}   # wave numbers not in the lookup output, need totems drill-in
check: {cadence: daily, who: "every_character", look_at: "Worship level + charge on each card; owner does the totem push"}
buffs:
  - {source: "Poisonic Elder to 5, Boulder Rollers to 10 (TD defense)", world: 3, owned: null, now: null, next: null, owner: "UNASSIGNED"}
triggers:
  - {when: "a totem rung wave reached", then: "route new prayer unlock to prayers owner (model/worship.py -> Autistacular)"}
  - {when: "wave 14 reached on a totem", then: "souls obtainable there (Griffy 2026-10-28): add to soul cover on Bish"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "One proper push on Breezy Battle to wave 10", stat: "prayer unlocks", gain_pct: null, unblocks: [prayers, equinox, menagerie], source: "my_read", active_min: 15, wait_hr: null, cost: null, urgent: false}
# OWNER GAP: unassigned in jobs.yaml; needs Zack's pick
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
