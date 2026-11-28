---
name: anvil
description: Anvil production: state, how it works, links, plan, today
---
# Anvil production

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: UNASSIGNED
- Toolbox: none mapped
- AutoReview: not rated
- Planner: NONE (nothing checks this yet)
- Creator rows: 0
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 9 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder   # smithing mats -> armor_sets, tools, forge
goal: "No character's anvil idle or capped, all anvil points spent, production aimed at the next craft"
coverage: partial   # creator routine + tab gates from Griffy's fresh-account series; no ladder for our stage
ladder:
  - {tier: 1, target: "Every character: anvil producing, not capped, 0 unspent points", source: "Griffy", date: "2025-12-27"}   # KZH_HUZf8rc 00:08:44 + 00:53:12; thread check GgGwaPlW90M 00:14:14 (2026-09-27)
  - {tier: 2, target: "Carry capacity up so production storage stops overflowing", source: "Griffy", date: "2026-04-23"}   # kD7KZ5zX6Ss 00:08:39
  - {tier: 3, target: "Anvil Tab 4 (Void Bars + Eternal Lords) -> Lustre crafting + next tools; produce Purple Screws ahead of a Lustre set", source: "Griffy", date: "2026-11-07"}   # __0_dvPFI_E 00:27:25; C2oiRVIpmq8 01:11:34 / 01:26:28; 0qlwJ8Qm-4w 01:04:38
objective: {rung: 1, now: "unspent points: Ticles 29, Totle 11, Cat 4, Tacular 3, Matic 3, Bish 2, Naut 2; Topher -435 (bad read); Bish cap 0", target: "0 unspent on all 11, no cap 0", eta_days: 0}
check: {cadence: daily, who: "every character (own anvil)", look_at: "characters[].anvil: producing, cap, availablePoints"}
buffs: []   # not behind, routine system
triggers:
  - {when: "availablePoints > 0 on a character", then: "that card: spend anvil points (speed vs capacity = my read: capacity while anything caps)"}
  - {when: "Tab 4 unlocked", then: "switch production to Purple Screws / Lustre mats (Griffy 2026-11-07)"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Spend 29 anvil points on Ticles, 11 on Totle (then the 2-4 on the rest)", stat: "anvil speed/cap", gain_pct: null, unblocks: [], source: "my_read (data)", active_min: 2, wait_hr: null, cost: null, urgent: false}
  - {do: "In game: Topher shows -435 available points and Bish cap 0; check both anvils", stat: "data check", gain_pct: null, unblocks: [], source: "my_read (data)", active_min: 2, wait_hr: null, cost: null, urgent: false}
  - {do: "Confirm anvil tab level in game (Tab 4 gates Lustre + next tools per Griffy)", stat: "unlock", gain_pct: null, unblocks: [armor_sets], source: "Griffy 2026-10-28 C2oiRVIpmq8 01:11:34", active_min: 1, wait_hr: null, cost: null, urgent: false}
# data now: all 11 produce item slot 2 (Tastic also slot 9; Totle, Matic, Naut, Topher run slot 9 too). Item names per slot not mapped.
# gap: lookup.py has no 'anvil' system (data is characters[].anvil); tab level + item names not in parser.
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
