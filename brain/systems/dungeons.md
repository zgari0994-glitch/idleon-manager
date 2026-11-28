---
name: dungeons
description: Dungeons: state, how it works, links, plan, today
---
# Dungeons

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: misc/dungeons (guide L204)
- AutoReview: none (AutoReview does not rate it)
- Planner: NONE (nothing checks this yet)
- Creator rows: 1104
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT synthesis 2026-11-28 batch 2 (claims DB, save 20261128T0256): not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: independent
goal: "Rank 44 -> 45, flurbos into weapon power + class XP/accuracy, roll a 10-12% keychain, daily world boss in a full party"
coverage: sourced       # RNG item tier list is 2022 (old)
ladder:
  - {tier: 1, target: "Dungeon rank 44 -> 45: 451K of 490K progress (39K left)", source: "Toolbox", date: "2026-11-28"}
  - {tier: 2, target: "flurbos (14.9K) into weapon power and class XP / accuracy, not Mega Crit gambling", source: "Griffy", date: "2026-10-04"}
  - {tier: 3, target: "-7 keychain at 10% (ideal double-6 = 12%); Diamond Hunk chain BiS with skill speed roll (~4%)", source: "Pulse", date: "2026-09-08"}
  - {tier: 4, target: "Happy Hour runs: Serrated Rex Rings for the characters", source: "Griffy", date: "2026-09-27"}
  - {tier: 5, target: "S-tier RNG items: Tax Ledger 0/8, Sneaky Cap 0/5, Super Soda 0/5", source: "Griffy (older: 2022-09 tier list)", date: "2022-09-24"}
objective: {rung: 1, now: 451000, target: 490000, eta_days: null}
check: {cadence: weekly, who: "UNASSIGNED (DK runs it: Autistomatic is DK)", look_at: "Happy Hour, flurbo balance, daily world boss party"}
method:
  - {rule: "Divine Knight for party dungeons (auto Shockwave Slash works in dungeons); Arcane Cultist can come close", source: "Griffy", date: "2026-08-03 / 2025-12-08"}
  - {rule: "daily world boss in a maxed party; teleporting multiplies boss HP and loot chance; Pulse skips dungeon runs this way", source: "Pulse", date: "2026-09-08"}
  - {rule: "wait for a full group: more players = more flurbos", source: "Griffy", date: "2025-12-08"}
  - {rule: "ballot: flower bow dungeon drops vote helps keychain rolls (world bosses drop flower bows)", source: "Pulse", date: "2026-09-03"}
buffs: []
triggers:
  - {when: "rank 45 reached", then: "next rank target from Toolbox rankReq"}
  - {when: "Happy Hour live", then: "join carried runs, spend credits on upgrades"}
stall: {pulls_no_progress: 4, eta_over_days: 45}
tasks:
  - {do: "Spend flurbos on weapon power then class XP / accuracy", stat: "dungeon dmg", gain_pct: null, unblocks: [], source: "Griffy 2026-10-04", active_min: 3, wait_hr: null, cost: null, urgent: false}
  - {do: "Daily world boss in a full party (Tastic's world boss job)", stat: "keychain rolls", gain_pct: null, unblocks: [], source: "Pulse 2026-09-08", active_min: 5, wait_hr: null, cost: null, urgent: false}
  - {do: "Happy Hour: Serrated Rex Rings", stat: "rings", gain_pct: null, unblocks: [], source: "Griffy 2026-09-27", active_min: 20, wait_hr: null, cost: null, urgent: false}
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
