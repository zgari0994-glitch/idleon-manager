---
name: world_progress
description: World Progress: state, how it works, links, plan, today
---
# World Progress

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: GAP: no Toolbox page mapped
- AutoReview: Pinchy high, Pinchy low, Pinchy all
- Planner: NONE (nothing checks this yet)
- Creator rows: 47
- Findings: none
- Open gaps: 28: Biggie Hours (babaHour) + King Doot (babaMummy): Baba Yaga line, Death Note 'Mini boss', 24h respawn (Toolbox monster data). Not on the Toolbox dashboard, no location in Toolbox wiki. Need: where/how they spawn, whether there's a reason to run them (Death Note rank, drops), then plan on Tastic. Zack: Tastic owns every world boss + Emperor; key-based bosses need tracking
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 9 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: feeder   # later W7 maps unlock spelunking progression, Glimbo trades, research mining (Griffy)
goal: "Push W7 maps to the next useful unlock, then pause (Griffy)"
coverage: partial
ladder:
  - {tier: 1, target: "W1-W6 finished", source: "Toolbox (parser)", date: "2026-11-28"}   # done
  - {tier: 2, target: "Push W7 instead of leveling every skill to 100; void tools on everyone first", source: "Griffy", date: "2026-01-29"}   # dliS5ZjijlA 01:39:59
  - {tier: 3, target: "Push to Litterfish (Billy), maybe Demon Blob (Meritocracy), then pause", source: "Griffy", date: "2026-04-23"}   # kD7KZ5zX6Ss 00:26:02
  - {tier: 4, target: "Later map goals: spelunking progression, Glimbo trades, research mining minigame", source: "Griffy", date: "2026-04-23"}   # kD7KZ5zX6Ss 00:27:02
objective: {rung: 3, now: "W7 not finished; current map not in parser", target: "Litterfish", eta_days: null}
check: {cadence: weekly, who: "UNASSIGNED", look_at: "finishedWorlds + W7 map kills (not in parser yet)"}
buffs:
  - {source: "Kills per kill ballot week", world: 2, owned: true, now: null, next: null, owner: "Autistotle"}   # Griffy 2026-01-29 dliS5ZjijlA 01:43:06
triggers:
  - {when: "kills per kill wins the ballot", then: "push week: best fighter on the next W7 portal"}
  - {when: "a W7 map gate blocks spelunking", then: "Law 1: map push becomes the blocker"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Confirm current W7 map in game and whether Litterfish is reached", stat: "unlock", gain_pct: null, unblocks: [spelunk, glimbo, research], source: "Griffy 2026-04-23 kD7KZ5zX6Ss 00:26:02", active_min: 1, wait_hr: null, cost: null, urgent: false}
# Old auto draft had Blood Marrow 291->294 as 'now'; that's an AutoReview talent line, not map progress (removed).
# Pinchy = reference only, owned by no one. gap: W7 map progress not in parser; owner unassigned.
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
