---
name: colo_scores
description: Colo Scores: state, how it works, links, plan, today
---
# Colo Scores

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: GAP: no Toolbox page mapped
- AutoReview: none (AutoReview does not rate it)
- Planner: NONE (nothing checks this yet)
- Creator rows: 0
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 10 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: independent
goal: "Run W5 + W6 Colosseums for golden food drops, stockpile tickets for expensive late entries"
coverage: partial
ladder:
  - {tier: 1, target: "Stockpile tickets (W6 entry ~30 tickets)", source: "Griffy", date: "2026-11-07"}   # __0_dvPFI_E 00:58:55
  - {tier: 2, target: "Farm W5 + W6 colos for golden foods", source: "Griffy", date: "2026-07-19"}   # aUdMKlRf_v4 00:25:30
objective: {rung: 1, now: null, target: 30, eta_days: null}   # ticket count not in parser
check: {cadence: weekly, who: "unassigned", look_at: "coloHighscores (W1 462K, W2 1.30M, W3 9.67M, W4 90.7M, W5 23.8M, W6 256M)"}
buffs: []
triggers:
  - {when: "tickets >= 30", then: "spend on W6 colo for golden food"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Check ticket count in game, then hold for W6 entries", stat: "golden food", gain_pct: null, unblocks: ["golden_food"], source: "Griffy", active_min: 2, wait_hr: null, cost: null, urgent: false}
# my read: W5 score (23.8M) is below W4 (90.7M), the one lagging; worth a run if a W5 golden food is still missing.
# gap: ticket count not in parser; which golden foods drop where not in creator rows.
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
