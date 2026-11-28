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
status: APPROVED   # Zack 2026-11-28
role: independent   # construction, owner Autistastic (best construction, Lv 1010)
goal: "Every cog slot EXP-positive, build rate up for buildings, flaggy for W3 flags; clean cog inventory"
coverage: full   # Zack 2026-11-28: optimizer = what creators use
ladder:
  - {tier: 1, target: "Scrap spare cogs the board doesn't use (done 2026-11-28: only 2 real spares, both used by the optimizer board; the old 126 counted 115 empty slots + 9 shelf characters); Griffy rates cog inventory F, just scrap cogs", source: "Griffy", date: "2024-04-27"}   # 25bteJumfjg 00:08:43, OLD
  - {tier: 2, target: "Board at Toolbox optimizer's best every week (best plan under +1%); 2026-11-28 save: 10 drags = +1.6% build, +6.9% player con EXP", source: "Toolbox", date: "2026-11-28"}   # tools/cog_plan.mjs, page defaults
  - {tier: 3, target: "Build rate 6.62T -> next building tier need (from buildings.py)", source: "my_read", date: "2026-11-28"}
# now_path: none - rung 2 gain is in snapshots/<save>/cog_plan.json (shown on Tastic's card), not the save
objective: {rung: 2, now: null, target: "optimizer best plan under +1%", eta_days: null}   # gain lives in snapshots/<save>/cog_plan.json, not the save
check: {cadence: weekly, who: "Autistastic", look_at: "card: Toolbox optimizer drags (model/cogs.py), spare cogs"}
buffs: []   # self-running
triggers:
  - {when: "a new cog maker roll finishes", then: "re-run the optimizer at the next pull: it decides slot or scrap"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Do the Toolbox optimizer drags listed on the card", stat: "build + con exp", gain_pct: 2.8, unblocks: [], source: "Toolbox", active_min: 5, wait_hr: null, cost: null, urgent: false}
  - {do: "Scrap spare cogs the optimizer plan doesn't use", stat: "inventory", gain_pct: null, unblocks: [], source: "Griffy", active_min: 3, wait_hr: null, cost: null, urgent: false}
# Zack 2026-11-28: the cog optimizer is what creators use; it IS the guidance, no creator layout needed.
# dropped 2026-11-28: "board EXP mult above 1" (my read) - the multiplier is an input to the optimizer, not set by placement; what raises it is a gap.
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
