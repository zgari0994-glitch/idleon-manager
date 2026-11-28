---
name: weekly_boss
description: W2 weekly boss: state, how it works, links, plan, today
---
# W2 weekly boss

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: UNASSIGNED
- Toolbox: none mapped
- AutoReview: not rated
- Planner: NONE (nothing checks this yet)
- Creator rows: 0
- Findings: none
- Open gaps: 28: Biggie Hours (babaHour) + King Doot (babaMummy): Baba Yaga line, Death Note 'Mini boss', 24h respawn (Toolbox monster data). Not on the Toolbox dashboard, no location in Toolbox wiki. Need: where/how they spawn, whether there's a reason to run them (Death Note rank, drops), then plan on Tastic. Zack: Tastic owns every world boss + Emperor; key-based bosses need tracking
- Checklist: [[weekly_boss]]: who does it, numbered fight steps. Zack believes 2 fights day one, then 1 a day (verify)
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- APPROVED 2026-11-28 (Zack): weekly boss set up from the rotation sheet -->
```yaml
status: APPROVED
role: independent   # weekly boss battle, rotation known ahead from the community sheet
goal: "Never skip: 5 Skulls run on the first kill of the week, trophy run every other day, both from the sheet's 11-character rotation"
coverage: sourced
ladder:
  - {tier: 1, target: "5 Skulls run on the week's first kill", source: "Weekly Boss Rotations sheet (fan)", date: "2026-11-28"}
  - {tier: 2, target: "Misc + Trophy run daily for the rest of the week", source: "Weekly Boss Rotations sheet (fan)", date: "2026-11-28"}
objective: {rung: 1, now: "Unit T-31 (2026-11-26 to 2026-12-03)", target: "5 skulls + daily trophy", eta_days: null}
check: {cadence: daily, who: "Autistastic", look_at: "brain/weekly_boss.yaml via tools/weekly_boss.py --today"}   # runner = whoever does world bosses (standing rule 2026-11-21)
buffs: []
triggers:
  - {when: "Thursday 00:00 GMT reset", then: "new boss; stored next week becomes current, refresh the sheet so the following week is stored too"}
  - {when: "weekly_boss.yaml has no week covering today", then: "card says stale, refresh before the run"}
stall: {pulls_no_progress: 99, eta_over_days: null}
tasks:
  - {do: "Weekly boss: daily run from the card line (sheet rotation)", stat: "trophies", gain_pct: null, unblocks: [], source: "Weekly Boss Rotations sheet", active_min: 5, wait_hr: 24, cost: null, urgent: true}
# source: Google Sheet 'Weekly Boss Rotations' (Drive 1z1P2ouvYhe2pryWoF0kIQE7QichYpJt1GaPPos-e-aw), Discord tab = current + next week. Fan source (roronoa_zoro93, DiamondDoge, Druzzt/Morgoth simulator).
# digits = option picks (1 top, 2 middle, 3 bottom), read left to right; FR = full rewind. Requirements (e.g. "Laboratory lvl - 1, 2, 7, 11") as written by the sheet.
# gap: weeklyBossesRaw: Toolbox reads only c (Class EXP week buff); d_*/set* not read, so "first kill done" is not in the save; GitHub Action can't read the sheet (needs the Drive connector in a thread).
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

## History and lessons (moved from Project memory 2026-11-21; dated state is history, live data wins)
- 11-14: wanted a reminder when the W2 weekly boss is available and not done; had never finished one. Old how-to lived in Project doc Daily-Rotation.md step 9 and KB section 26 (weekly boss sheet): MOVE IT HERE. 11-21: believes 2 fights day one then 1 a day (verify); give numbered fight steps to whoever does world bosses.
