---
name: emperor
description: Emperor: state, how it works, links, plan, today
---
# Emperor

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistocat
- Toolbox: world-6/emperor (guide L156)
- AutoReview: Emperor
- Planner: model/emperor.py
- Creator rows: 30
- Findings: none
- Open gaps: 28: Biggie Hours (babaHour) + King Doot (babaMummy): Baba Yaga line, Death Note 'Mini boss', 24h respawn (Toolbox monster data). Not on the Toolbox dashboard, no location in Toolbox wiki. Need: where/how they spawn, whether there's a reason to run them (Death Note rank, drops), then plan on Tastic. Zack: Tastic owns every world boss + Emperor; key-based bosses need tracking
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 7 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: multiplier   # Emperor bonuses = real multis (bones, dust, tachyons, bits, drop rate)
goal: "Never waste Emperor attempts; push showdowns with an Arcane Cultist, big pushes in statue week"
coverage: sourced
ladder:
  - {tier: 1, target: "Use attempts before 11 cap (0 wasted)", source: "data", date: "2026-11-28"}
  - {tier: 2, target: "Showdown 78 (WW dust) -> 79 (+10% drop rate) -> 83 (AC tachyons) -> 85 (farming 20% cheaper)", source: "data", date: "2026-11-28"}
  - {tier: 3, target: "Big pushes in statue week with boost foods (Feasty + dragon statue multiply foods)", source: "Pulse", date: "2026-11-16"}
now_path: "emperor.highestEmperorShowdown"
objective: {rung: 2, now: "highest showdown 77, 2/11 attempts banked", target: 78, eta_days: null}
check: {cadence: daily, who: "Autistocat", look_at: "emperor attempts + highestEmperorShowdown"}
buffs: []
triggers: []
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Emperor fights on Cat: stand on the small platform next to the boss and auto (skulls bounce)", stat: "showdown", gain_pct: null, unblocks: [compass, grimoire, tesseract], source: "Griffy 2026-08-03 ypb7kpQov30 00:05:36 + Pulse 2026-10-31 6JgdYbiEKus 00:14:18", active_min: 5, wait_hr: null, cost: "1 attempt", urgent: false}
  - {do: "Eat boost foods for the push (Cold Seekers, Midnight Cookies, Kebabs)", stat: "damage", gain_pct: null, unblocks: [], source: "Pulse 2026-10-31 6JgdYbiEKus 00:15:49", active_min: null, wait_hr: null, cost: null, urgent: false}
# Owner = Cat per jobs.yaml (Zack 2026-11-25); lookup header still says Autistastic (stale owner map). Profile memory said Zemo does Emperor; jobs.yaml is newer.
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
