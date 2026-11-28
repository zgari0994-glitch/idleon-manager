---
name: death_note
description: Death Note: state, how it works, links, plan, today
---
# Death Note

<!-- AUTO:START (tools/build_brain.py rewrites this block) -->
- Owners: Autistopher, Autiszemo
- Toolbox: world-3/death-note (guide L97)
- AutoReview: Death Note
- Planner: model/deathnote.py
- Creator rows: 218
- Findings: death_note_two_dbs
- Open gaps: 3: Plan Topher's Super CHOW rebuild (13 now): which maps first. Settled: counts only on him, WOWs skipped (findings/death_note_two_dbs.md) | 28: Biggie Hours (babaHour) + King Doot (babaMummy): Baba Yaga line, Death Note 'Mini boss', 24h respawn (Toolbox monster data). Not on the Toolbox dashboard, no location in Toolbox wiki. Need: where/how they spawn, whether there's a reason to run them (Death Note rank, drops), then plan on Tastic. Zack: Tastic owns every world boss + Emperor; key-based bosses need tracking
<!-- AUTO:END -->

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT Phase A batch 4 2026-11-27 (save 20261127T2212): not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder
goal: "Push every mob to the next skull, closest first; kills feed damage, portals and Voidwalker"
coverage: partial
ladder:
  - {tier: 1, target: "Gelatinous Cuboid 90% (102M left)", source: "Toolbox", date: "2026-11-27"}
  - {tier: 2, target: "Fire Spirit 83% (170M left)", source: "Toolbox", date: "2026-11-27"}
  - {tier: 3, target: "Soda Can, Flying Worm, Crawler ~62% (372-384M left)", source: "Toolbox", date: "2026-11-27"}
  - {tier: 4, target: "Eclipse skulls (1B kills, multiplicative damage)", source: "Griffy", date: "2026-10-28"}
objective: {rung: 1, now: "90%", target: "100%", eta_days: null}
check: {cadence: daily, who: "Autiszemo + Autistopher", split: "Zemo ZOWs + CHOWs W1-W6, Topher Super CHOWs + big kills", look_at: "AFK maps of multikill chars vs closest mob"}
buffs:
  - {source: "Death Note building (multikill)", world: 3, owned: true, now: null, next: null, owner: "Autistastic"}
  - {source: "Rift Joc (2x kills)", world: 4, owned: null, now: null, next: null, owner: ""}
triggers:
  - {when: "mob hits 100%", then: "move that AFK char to next closest"}
stall: {pulls_no_progress: 3, eta_over_days: 30}
tasks:
  - {do: "Park a multikill AFK char on Gelatinous Cuboid", stat: "skull", gain_pct: null, unblocks: [], source: "my_read", active_min: 1, wait_hr: 24, cost: null, urgent: false}
# ranks W1-W7: 300/220/280/220/200/240/195, minibosses 0. Griffy: Eclipse farming slow without big multikill.
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
- Autiszemo AFK plan (11-14): Super CHOWs in world order; after Biggole Mole, W3 Bloodbone, then Dedotated Ram, then W4 in order. Later rule (11-16/11-20): Zemo does 1M CHOWs W1-W6; Autistopher does Super CHOWs and kill pushes.
