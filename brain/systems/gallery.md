---
name: gallery
description: Gallery: state, how it works, links, plan, today
---
# Gallery

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistachio
- Toolbox: world-7/gallery (guide L164)
- AutoReview: Gallery
- Planner: model/gallery.py
- Creator rows: 48
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 7 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: multiplier   # gallery multiplies trophy + nametag bonuses
goal: "Fill gallery podiums with the strongest trophies and nametags; get Nine Dart Finish and relic nametags"
coverage: partial
ladder:
  - {tier: 1, target: "At least one nametag in (true multi, multiplied by gallery)", source: "Pulse", date: "2026-10-31"}
  - {tier: 2, target: "Nine Dart Finish trophy (9% drop rate multi, x four-liner)", source: "Pulse", date: "2026-09-15"}
  - {tier: 3, target: "Relic aquarium nametags via Coral Cave Crab on an Arcane Cultist", source: "Pulse", date: "2026-09-04"}
  - {tier: 4, target: "Podium upgrades: 2 at Lv3, 0 at Lv4 -> all Lv3, then Lv4", source: "my read", date: "2026-11-28"}
objective: {rung: 2, now: "15 podiums (11 Lv2, 2 Lv3, 0 Lv4), bonus multi 1.16", target: "Nine Dart Finish", eta_days: null}
check: {cadence: weekly, who: "Autistachio", look_at: "gallery podiums + AutoReview Gallery missing trophies"}
buffs: []
triggers: []
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Grind Nine Dart Finish (gets easier after a day or two; easier than Baller)", stat: "drop rate multi", gain_pct: 9, unblocks: [], source: "Pulse 2026-09-15 r43UqKC2axI 00:18:08", active_min: null, wait_hr: null, cost: null, urgent: false}
  - {do: "Relic nametags: buy relic aquarium tags in W7 store, Cat hands them to Coral Cave Crab", stat: "nametag", gain_pct: null, unblocks: [], source: "Pulse 2026-09-04 ofuB4YV8gkM 00:08:48", active_min: null, wait_hr: null, cost: null, urgent: false}
  - {do: "King of Food trophy (Picnic Stowaway daily quest, already working)", stat: "20% food effect", gain_pct: 20, unblocks: [], source: "AutoReview + Zack", active_min: null, wait_hr: null, cost: null, urgent: false}
# Podium upgrade costs/order not in claims or parser = my read. Pulse: Yolk Master pet ($35) A tier, paid.
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
