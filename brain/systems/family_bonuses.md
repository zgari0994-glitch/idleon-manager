---
name: family_bonuses
description: Family Bonuses: state, how it works, links, plan, today
---
# Family Bonuses

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: unassigned in jobs.yaml
- Toolbox: GAP: no Toolbox page mapped
- AutoReview: none (AutoReview does not rate it)
- Planner: NONE (nothing checks this yet)
- Creator rows: 0
- Findings: none
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 11 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: DRAFT
role: feeder   # passive: highest level per class feeds all characters
goal: "Family bonuses rise as a side effect of leveling; no direct spend"
coverage: partial
ladder:
  - {tier: 1, target: "Keep every character leveling (talent points + family bonus)", source: "Griffy", date: "2026-10-04"}   # N5yJ4-tZLbY 00:01:00
  - {tier: 2, target: "Lowest family values: Shaman 1.36, Voidwalker 3.76, Beast Master 4.09, Bubonic Conjuror 4.09, Royal Guardian 4.96 (gain per level not known)", source: "Toolbox", date: "2026-11-28"}
objective: {rung: 1, now: "passive", target: null, eta_days: null}
check: {cadence: weekly, who: "UNASSIGNED", look_at: "characters[].familyBonuses"}
buffs: []
triggers:
  - {when: "a class swap or new class is planned", then: "check which family bonus it raises or drops"}
stall: {pulls_no_progress: 6, eta_over_days: 90}
tasks: []   # no direct action; Family Guy only buffs the character using it (Griffy 2026-10-04)
# gap: family bonus formula per class not in model, so no "level X for +Y" ranking; Shaman/Beast Master/Bubonic have no roster character.
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
