---
name: ballot
description: Ballot: state, how it works, links, plan, today
---
# Ballot

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistotle
- Toolbox: world-2/vote-ballot (guide L86)
- AutoReview: Bonus Ballot
- Planner: model/shops.py
- Creator rows: 0
- Findings: none
- Checklist: [[ballot]] / [[meritocracy]]: pros and cons for him and for the server, never "vote X"
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 8 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder   # weekly multiplier on whatever system wins the vote
goal: "Weekly vote decided with pros/cons for him and the server; vote multi (now x1.84) raised over time"
coverage: sourced
ladder:
  - {tier: 1, target: "Every reset: card shows the options with Griffy's tier (S: kills per kill, nuggets, shrine XP; A top: refinery; F: guild points) + pros/cons, never 'vote X'", source: "Griffy + Zack rule", date: "2026-01-29"}   # Rr5KiEflTWE
  - {tier: 2, target: "Pre-stack for strong weeks: bank AFK 24h before kills-per-kill week; pre-stack divinity before divinity week", source: "Griffy / Pulse", date: "2026-07-29"}   # _maMoJLg6YE 02:20:46; Pulse NlppEKJNCZM 00:16:17
  - {tier: 3, target: "Vote multi up: Crystal Cuttlefish +40%, Mashed Potato +5%, Poppy doubles Ballot + Meritocracy (consider around W7)", source: "Griffy", date: "2026-09-21"}   # 8C9vFwK6bUg 00:15:15 / 00:11:13; KHuU392EW-4 00:04:47
objective: {rung: 1, now: "this week Sailing Artifact Find (x1.84), votes carried from save 20261127T1704", target: "weekly read every reset", eta_days: null}
check: {cadence: weekly, who: "Autistotle", look_at: "voteBallot.selectedBonus + voteMulti; phone saves carry votes (flag)"}
buffs:
  - {src: "Crystal Cuttlefish", gives: "+40% ballot multi", owned: true, owner: "Autistotle"}
  - {src: "Mashed Potato", gives: "+5% ballot multi", owned: true, owner: "Autistotle"}
  - {src: "Poppy (companion)", gives: "x2 Ballot + Meritocracy", owned: false, owner: "account"}   # the one missing lever (Griffy: consider around W7)
triggers:
  - {when: "weekly reset", do: "pros/cons on Totle's card, then week plan on the owner of the voted system (e.g. sailing week -> Ticles long trips)"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Get Poppy (companion): doubles Ballot + Meritocracy; Cuttlefish + Mashed Potato already owned (Zack 2026-11-28)", stat: "vote multi x2", gain_pct: 100, unblocks: [meritocracy], source: "Griffy 2026-09-21 KHuU392EW-4 00:04:47", active_min: null, wait_hr: null, cost: null, urgent: false}
# Never recommend a vote (Zack 2026-11-21): pros/cons only.
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
