---
name: crystal_spawn_chance
description: Crystal Spawn Chance: state, how it works, links, plan, today
---
# Crystal Spawn Chance

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: GAP: no Toolbox page mapped
- AutoReview: none (AutoReview does not rate it)
- Planner: NONE (nothing checks this yet)
- Creator rows: 0
- Findings: none
- Open gaps: 28: Biggie Hours (babaHour) + King Doot (babaMummy): Baba Yaga line, Death Note 'Mini boss', 24h respawn (Toolbox monster data). Not on the Toolbox dashboard, no location in Toolbox wiki. Need: where/how they spawn, whether there's a reason to run them (Death Note rank, drops), then plan on Tastic. Zack: Tastic owns every world boss + Emperor; key-based bosses need tracking
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 10 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: feeder   # crystals -> drops/candy; Monolith farming
goal: "Substantial crystal spawn chance + ~30x drop rate before farming the Monolith requirement"
coverage: partial
ladder:
  - {tier: 1, target: "Lift the 3 low characters (Ticles, Naut, Tachio 0.674%) to the 1.46% the other 7 have", source: "my_read", date: "2026-11-28"}
  - {tier: 2, target: "~30x drop rate + high crystal chance on the Monolith farmer", source: "Griffy", date: "2026-07-19"}   # old auto-draft claim
objective: {rung: 1, now: 3, target: 0, eta_days: null}   # characters below 1.46%
check: {cadence: weekly, who: "unassigned", look_at: "characters[].crystalSpawnChance"}
buffs: []
triggers:
  - {when: "all 10 non-Totle chars at 1.46%+", then: "rung 2"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Find what the 7 have that Ticles/Naut/Tachio lack (talent, star sign, or class bonus)", stat: "crystal %", gain_pct: 117, unblocks: [], source: "my_read", active_min: 5, wait_hr: null, cost: null, urgent: false}
# my read: Totle 4.46% is the best crystal farmer. Griffy rates the daily-first-kill crystal merit F (2025-04-29).
# gap: crystal chance breakdown per source not in parser.
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
