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
<!-- DRAFT Phase A batch 10 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: independent   # construction, owner Autistastic (best construction, Lv 1010)
goal: "Every cog slot EXP-positive, build rate up for buildings, flaggy for W3 flags; clean cog inventory"
coverage: partial
ladder:
  - {tier: 1, target: "Scrap junk: 126 spare cogs, 0 free small-cog slots; Griffy rates cog inventory F, just scrap cogs", source: "Griffy", date: "2024-04-27"}   # 25bteJumfjg 00:08:43, OLD
  - {tier: 2, target: "Board EXP mult above 1 (now 1, flaggy mult 4): place EXP cogs/boosters", source: "my_read", date: "2026-11-28"}
  - {tier: 3, target: "Build rate 6.62T -> next building tier need (from buildings.py)", source: "my_read", date: "2026-11-28"}
objective: {rung: 1, now: 126, target: 0, eta_days: null}   # spares to scrap/sort
check: {cadence: weekly, who: "Autistastic", look_at: "construction.boardMultipliers, smallCogs.freeSlots, spareCogs"}
buffs: []   # self-running
triggers:
  - {when: "a new cog maker roll finishes", then: "compare vs board, slot or scrap"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Scrap/sort the 126 spare cogs, keep only upgrades", stat: "inventory", gain_pct: null, unblocks: [], source: "Griffy", active_min: 10, wait_hr: null, cost: null, urgent: false}
  - {do: "Get board EXP mult off 1x (EXP cogs near players)", stat: "con exp", gain_pct: null, unblocks: [], source: "my_read", active_min: 10, wait_hr: null, cost: null, urgent: false}
# gap: no creator board layout rule newer than 2024; cog placement optimizer not in model.
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
