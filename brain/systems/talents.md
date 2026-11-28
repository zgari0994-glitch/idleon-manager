---
name: talents
description: Talent points (both presets): state, how it works, links, plan, today
---
# Talent points (both presets)

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: UNASSIGNED
- Toolbox: none mapped
- AutoReview: not rated
- Planner: NONE (nothing checks this yet)
- Creator rows: 0
- Findings: none
- Open gaps: 27: Held until transcripts reviewed; Blue Ribbon was an AutoReview target, not Griffy-certified
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 12 2026-11-28: not approved, not in the pipeline (replaces the auto draft) -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder   # every character, damage + skilling; MERGED class_kill_talents (2026-11-28)
goal: "Each character runs their own talents: one skilling + one fighting preset (break the standard only for a reason: masterclass or a niche focus that helps), every talent at cap, super points spent, multikill on the AFK bar"
coverage: partial
ladder:
  - {tier: 1, target: "Multikill talent on the bar when going AFK (else no extra multikill per tier)", source: "Griffy", date: "2025-11-20"}   # GFmPSIRIPX4 00:47:39
  - {tier: 2, target: "Get the extra-kill talent for portals + Death Note", source: "Griffy", date: "2026-04-23"}   # kD7KZ5zX6Ss 01:01:14
  - {tier: 3, target: "Raise caps: Library checkouts (rank #1-55, book cap 299)", source: "Toolbox", date: "2026-11-28"}
objective: {rung: 1, now: "super points unspent: Totle 1, Tachio 4", target: "0 unspent", eta_days: null}
check: {cadence: weekly, who: "every character (own talents, Zack 2026-11-28)", look_at: "characters[].talents + superTalentLeftToSpend"}
buffs: []
triggers:
  - {when: "superTalentLeftToSpend > 0", then: "spend it; shown on the card until spent (cant_miss super_left)"}
  - {when: "a character has no skilling/fighting preset pair", then: "flag it unless a masterclass/niche reason is on file"}
  - {when: "Library checkout done", then: "re-rank next max talent"}
stall: {pulls_no_progress: 4, eta_over_days: 60}
tasks:
  - {do: "Spend Totle's 1 + Tachio's 4 super talent points", stat: "talent", gain_pct: null, unblocks: [], source: "Toolbox", active_min: 3, wait_hr: null, cost: null, urgent: false}
  - {do: "Check multikill talent is on every AFK character's bar", stat: "multikill", gain_pct: null, unblocks: [], source: "Griffy", active_min: 5, wait_hr: null, cost: null, urgent: false}
# warning: stat-based kills-per-kill talent doesn't work in W7 after the nerf (Griffy 2025-11-28 fo2WwEKsty0 00:08:10).
# data: talentPointsLeft per tab is large (e.g. Zemo 1436/1915/1471/311): points aren't the limit, caps are. account.talentPoints [8,8,12,7,0,3] meaning unknown.
# gap: no per-talent "below cap" list in lookup; super_talents batch 8 flags Topher + Totle reset candidates.
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
