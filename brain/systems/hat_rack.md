---
name: hat_rack
description: Hat Rack: state, how it works, links, plan, today
---
# Hat Rack

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: world-3/hat-rack (guide L104)
- AutoReview: none (AutoReview does not rate it)
- Planner: NONE (nothing checks this yet)
- Creator rows: 16
- Findings: none
- Open gaps: 28: Biggie Hours (babaHour) + King Doot (babaMummy): Baba Yaga line, Death Note 'Mini boss', 24h respawn (Toolbox monster data). Not on the Toolbox dashboard, no location in Toolbox wiki. Need: where/how they spawn, whether there's a reason to run them (Death Note rank, drops), then plan on Tastic. Zack: Tastic owns every world boss + Emperor; key-based bosses need tracking
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 9 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: independent   # Griffy: not an immediate concern, strong later
goal: "Grow the Hat Rack multi (now 1.51x) as hats and multi sources come in"
coverage: partial
ladder:
  - {tier: 1, target: "41 hats on the rack (+1% each) + Event shop 10%", source: "Toolbox (parser)", date: "2026-11-28"}   # done
  - {tier: 2, target: "Wild Boar companion +15% multi", source: "Griffy", date: "2026-07-19"}   # 8C9vFwK6bUg 00:25:35
  - {tier: 3, target: "Minehead + Sushi Station multi (both 0 now)", source: "Toolbox (parser)", date: "2026-11-28"}
  - {tier: 4, target: "Sneaking hats once Sneaking is further along", source: "Griffy", date: "2026-09-21"}   # KHuU392EW-4 00:38:49; kD7KZ5zX6Ss 00:36:43
objective: {rung: 2, now: "1.51x", target: "1.66x (Wild Boar)", eta_days: null}
check: {cadence: weekly, who: "UNASSIGNED", look_at: "hatRack.bonusMultiBreakdown + any new hat to deposit"}
buffs:
  - {source: "Wild Boar (companion)", world: null, owned: false, now: 0, next: 15, owner: "account"}
  - {source: "Minehead", world: 7, owned: false, now: 0, next: null, owner: "Autisticles"}
  - {source: "Sushi Station", world: 7, owned: false, now: 0, next: null, owner: "Autisticles"}
triggers:
  - {when: "new premium or sneaking hat found", then: "deposit it (Pulse 2026-10-16: deposited vanity ninja hats leave the drop table)"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Route Minehead + Sushi hat-rack bonuses onto Ticles' W7 minis lines", stat: "hat multi", gain_pct: null, unblocks: [], source: "my_read (parser breakdown)", active_min: null, wait_hr: null, cost: null, urgent: false}
# Most hats come from paid packs (Pulse 2026-11-01, fan opinion). gap: owned-not-deposited hats not in parser; owner unassigned.
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
