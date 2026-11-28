---
name: tesseract
description: Tesseract: state, how it works, links, plan, today
---
# Tesseract

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistocat
- Toolbox: class-specific/tesseract (guide L196)
- AutoReview: The Tesseract
- Planner: model/tesseract.py
- Creator rows: 32
- Findings: tesseract_plan
- Open gaps: 12: How to push Tesseract; it needs active play until ~1,000 of its currency (Zack)
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 7 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: masterclass   # Arcane Cultist only; Cat's masterclass duty
goal: "Raise total Tesseract levels to the next unlocks (2000 Jewel of the North Winds, 2050 Arcanist Damage IV)"
coverage: sourced
ladder:
  - {tier: 1, target: "2000 total levels (Jewel of the North Winds)", source: "data", date: "2026-11-28"}
  - {tier: 2, target: "Inviting a Plus One above 200 (extra mob spawn)", source: "Pulse", date: "2026-09-13"}
  - {tier: 3, target: "2-min claims until claim multi ~50x, then the big claims", source: "Pulse", date: "2026-10-20"}
  - {tier: 4, target: "2050 (Arcanist Damage IV), 2350 (Eternal Stream), 2600, 2750 (Fractal Tesseract)", source: "data", date: "2026-11-28"}
now_path: "tesseract.totalUpgradeLevels"
objective: {rung: 1, now: "1932 total levels", target: 2000, eta_days: null}
check: {cadence: daily, who: "Autistocat", look_at: "tesseract total levels + cheapest open upgrades"}
buffs: []
triggers: []
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Buy the cheapest open levels until 2000 total (68 to go): Ring Drops 1.02M, Arcanist Defence III 1.21M, Ethereal Opals 1.22M, Villager Indoctrination 1.38M, Fastcasting 1.76M...", stat: "total levels", gain_pct: null, unblocks: [], source: "parser costs", active_min: 5, wait_hr: null, cost: "~1M+ tachyons each", urgent: false}
  - {do: "Push Inviting a Plus One 48 -> 200+", stat: "extra mob chance", gain_pct: null, unblocks: [], source: "Pulse 2026-09-13 hM-HC11gshI 00:14:26", active_min: null, wait_hr: null, cost: "8.15M next", urgent: false}
# Tachyons: Purple 383M, Brown 1.58B, Green 644K, Red 1.59M, Silver 4.98K, Gold 0. Which color each upgrade costs isn't in the parser, so "affordable" is unverified. Pulse's "One drops ~1200" doesn't match a parser name.
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
