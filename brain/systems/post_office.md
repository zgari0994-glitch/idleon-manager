---
name: post_office
description: Post Office: state, how it works, links, plan, today
---
# Post Office

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: GAP: no Toolbox page mapped
- AutoReview: Post Office
- Planner: model/postoffice.py
- Creator rows: 0
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 8 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: independent   # low tier (Griffy F/D, 2022-24); a few boxes feed live goals
goal: "Boxes that feed live goals maxed on each character; the rest is a 'you have points' ping"
coverage: sourced
ladder:
  - {tier: 1, target: "Potion Package 400 on every character (+30s Cranium duration)", source: "Griffy", date: "2025-06-07"}   # yCkTzQzeLn8 00:01:32
  - {tier: 2, target: "Core boxes 400, Scurvy/Gaming 800 (Box of Gosh), new points into Myriad Crate", source: "history 2026-11-14", date: "2026-11-14"}
  - {tier: 3, target: "Myriad Crate toward 100K (AutoReview), slow burn", source: "AutoReview", date: "2026-11-28"}
objective: {rung: 1, now: "Tacular 183, Matic/Naut/Topher/Tachio 0", target: "400 each", eta_days: null}
check: {cadence: daily, who: "every character (own boxes)", look_at: "card line when a character has points (Zack 2026-11-21)"}
buffs: []
triggers:
  - {when: "a character has PO points", do: "spend on the lowest rung box on their card"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Potion Package to 400 on Tacular, Matic, Naut, Topher, Tachio", stat: "Cranium duration", gain_pct: null, unblocks: [], source: "Griffy 2025-06-07 yCkTzQzeLn8", active_min: 2, wait_hr: null, cost: null, urgent: false}
  - {do: "Allocate fishing boxes before taking fishing print samples", stat: "prints", gain_pct: null, unblocks: [], source: "Griffy 2026-03-27 0qlwJ8Qm-4w", active_min: 1, wait_hr: null, cost: null, urgent: false}
# Owner in jobs.yaml unassigned; lookup header says Autiszemo. Griffy skip: PO reset (event drop).
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
- Zemo boxes (11-14): core 400, Scurvy/Gaming 800, Myriad 1,000; new points to Myriad. 11-21 rule: just say when a character has points.
