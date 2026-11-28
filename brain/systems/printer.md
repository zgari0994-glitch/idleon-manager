---
name: printer
description: Printer: state, how it works, links, plan, today
---
# Printer

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autisticles, Autistomatic, Autistronaut, Autiszemo
- Toolbox: world-3/printer (guide L92); tools/sampling-companion (guide L239)
- AutoReview: Sampling
- Planner: model/printer.py
- Creator rows: 750
- Findings: none
- Checklist: [[printer]]: is it time to do The Print or near a threshold worth waiting for
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A 2026-11-27: not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder
goal: "Samples near 90% size on the right items, refinery mats first (Griffy 2026-10-28)"
coverage: partial
ladder:
  - {tier: 1, target: "Island stamp to push sample size toward 90%", source: "Griffy", date: "2026-10-28"}
  - {tier: 2, target: "Oak Logs 4.42B -> 10B, Copper 1.34B -> 8B, Goldfish 111.85M -> 150M samples", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "Spore Cap 1.44M -> 10M -> 20M, Fly 131M -> 454M", source: "Toolbox", date: "2026-11-27"}
objective: {rung: 1, now: null, target: "90%", eta_days: null}
check: {cadence: daily, who: "Autisticles, Autistomatic, Autistronaut, Autiszemo", look_at: "per-char slots; take new samples early, don't wait for pending bonuses"}
buffs:
  - {source: "Royal Sampler ~lv11, Skilled Dimwit (prayers)", world: 3, owned: null, now: null, next: null, owner: "every_character"}
  - {source: "Warriors Rule bubble", world: 2, owned: true, now: 765, next: 950, owner: "Autistocat"}
triggers:
  - {when: "sample size buff gained", then: "resample top refinery mats"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Resample refinery monster drops on Wind Walker", stat: "refinery mats", gain_pct: null, unblocks: [refinery], source: "Griffy", active_min: 5, wait_hr: null, cost: null, urgent: false}
# The Print timing question (checklist) not answered yet
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
