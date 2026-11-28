---
name: menagerie
description: Menagerie: state, how it works, links, plan, today
---
# Menagerie

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autisticles
- Toolbox: world-7/menagerie (guide L174)
- AutoReview: Luminous Menagerie
- Planner: model/menagerie.py
- Creator rows: 290
- Findings: none
- Open gaps: 17: How to get Shells (3 for rank 4) | 18: Pink Jellyfish unlock: what it takes | 19: Path to Sneaking Mastery 2 (Menagerie mission) | 39: Breezy Battle (10) + Citric Conflict (28): one-time proper push plan; worship 500+ needed for Equinox + Menagerie
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 4 2026-11-27 (save 20261127T2212): not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder
goal: "Rank up the Menagerie (rank 6) to open its gates: plate cap +10, Breeding Crucible, Shiny OverLVs, Night Marina odds, Cooking T13"
coverage: partial
ladder:
  - {tier: 1, target: "Rank 6 -> 7 (needs 3 shells, have 0)", source: "Toolbox", date: "2026-11-27"}
  - {tier: 2, target: "Mission 6: Worship best waves 961 -> 1100", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "Buy next Black Star (owned 2)", source: "Pulse", date: "2026-11-16"}
objective: {rung: 1, now: 0, target: 3, eta_days: null}
check: {cadence: daily, who: "Autisticles", look_at: "lumi (6.49K, +241), shells, missions"}
buffs:
  - {source: "Black Stars (doubler)", world: 7, owned: true, now: 2, next: 3, owner: "Autisticles"}
triggers:
  - {when: "shell gained", then: "check rank-up"}
  - {when: "Black Star affordable", then: "buy it (Pulse: strongest, scales hard, 1-2 more)"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Buy cheapest boost (#4, Lv 6, 1.25K lumi) with the 6.49K on hand", stat: "boost", gain_pct: null, unblocks: [], source: "my_read", active_min: 1, wait_hr: null, cost: 1250, urgent: false}
  - {do: "Push Worship waves 961 -> 1100 for Mission 6", stat: "mission", gain_pct: null, unblocks: ["shells"], source: "Toolbox", active_min: 20, wait_hr: null, cost: null, urgent: false}
# feeds Cooking speed (account priority) via Cooking T13. Mission 6 depends on Worship (Bish drives it, Tacular runs totem waves).
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
