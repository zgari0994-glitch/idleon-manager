---
name: cog_board
description: Cog Board: state, how it works, links, plan, today
---
# Cog Board

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: GAP: no Toolbox page mapped
- AutoReview: none (AutoReview does not rate it)
- Planner: NONE (nothing checks this yet)
- Creator rows: 0
- Findings: none
- Open gaps: 10: Not visible on phone: guide in chat from the card until fixed | 28: Biggie Hours (babaHour) + King Doot (babaMummy): Baba Yaga line, Death Note 'Mini boss', 24h respawn (Toolbox monster data). Not on the Toolbox dashboard, no location in Toolbox wiki. Need: where/how they spawn, whether there's a reason to run them (Death Note rank, drops), then plan on Tastic. Zack: Tastic owns every world boss + Emperor; key-based bosses need tracking
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT synthesis 2026-11-28 batch 1 (claims DB, save 20261128T0256): not approved, not in the pipeline -->
```yaml
status: DRAFT
role: independent
goal: "Every cog EXP%, directional cogs on the Divine Knights, booster XP at the 65% cap, then jeweled cogs past it"
coverage: partial       # EXP rule sourced; Polymerization + Flaggy detail = my read (gap logged)
ladder:
  - {tier: 1, target: "all cogs EXP% (EXP over build rate: build rate trades long-term for short-term)", source: "Pulse 2026-09-12 + Griffy 2026-03-27", date: "2026-09-12"}
  - {tier: 2, target: "only Divine Knights on the board; point every directional/booster cog at them", source: "Griffy 2026-04-23; Pulse 2026-09-12", date: "2026-09-12"}
  - {tier: 3, target: "booster cog XP at the 65% cap", source: "Griffy", date: "2025-03-07"}
  - {tier: 4, target: "Cog Lover: up to +5 jeweled cogs/day past the 65% cap", source: "Griffy 2025-11-10; Pulse 2026-09-25 (A tier)", date: "2026-09-25"}
objective: {rung: 1, now: null, target: null, eta_days: null}
check: {cadence: daily, who: "Autistastic", look_at: "new cogs vs board, Tiny Cog daily, 126 spare cogs"}
meta_vs_board:
  - {rule: "yellow jellyfish week: directional + tiny cogs may flip to build rate for a day or two, then back to EXP", source: "Pulse 2026-10-19 (flip) + my read (flip back)", date: "2026-10-19"}
  - {rule: "Polymerization + Flaggy: no creator claims; flaggy rate 26B with board flaggy multi 4, keep as-is", source: "my_read", date: "2026-11-28"}
buffs:
  - {source: "Cog Lover talent (jeweled cogs)", world: 7, owned: null, now: null, next: null, owner: "Autistastic"}
triggers:
  - {when: "booster XP hits 65%", then: "switch cog upgrades to jeweled cogs (Cog Lover)"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Claim Tiny Cog before daily reset", stat: "tiny cogs", gain_pct: null, unblocks: [], source: "Griffy 2026-02-21", active_min: 1, wait_hr: null, cost: null, urgent: false}
  - {do: "Swap any non-EXP cog for a higher EXP% cog; trash low spares", stat: "construction EXP", gain_pct: null, unblocks: [], source: "Griffy 2026-01-29 (trash spares: my read)", active_min: 3, wait_hr: null, cost: null, urgent: false}
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
