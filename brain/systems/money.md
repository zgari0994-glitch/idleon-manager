---
name: money
description: Money: coin farming, money gear, Vault / Menagerie coin targets
---
# Money

- Owners: Autistomatic (jobs.yaml Money)
- Toolbox: none (no parser path yet)
- Planner: model/coins.py

<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
<!-- DRAFT synthesis 2026-11-28 batch 2 (claims DB, save 20261128T0256): not approved, not in the pipeline -->
```yaml
status: APPROVED   # Zack 2026-11-28
role: feeder
goal: "Enough coins for Upgrade Vault, Luminous Menagerie and Pink Jellyfish; BiS money gear on the money farmer"
coverage: partial       # gear ownership not in parser; best-item-owned vs unlock has no claims
ladder:
  - {tier: 1, target: "BiS money gear owned + on the farmer: Emerald Bling Pendant, Corsair outfit, Emerald Rumble chip, Golden Bread food", source: "Pulse", date: "2026-11-11 / 2026-09-18 / 2026-08-02"}
  - {tier: 2, target: "Draw Breaker prayer (W3 shrine) in the money setup", source: "Pulse", date: "2026-08-02"}
  - {tier: 3, target: "coins far enough for Pink Jellyfish (8 shells + Lumi gains); short of the final coin = account needs coin work", source: "Pulse", date: "2026-11-12 / 2026-10-19"}
  - {tier: 4, target: "more unique cards: +4% monster coins per discovered card", source: "Griffy", date: "2026-10-04"}
  - {tier: 5, target: "money cards 5 -> 6: Baba Yaga (1.6K of 22.7K), Dilapidated Slush (9.1K of 75.6K); Kattlekruk 4 -> 5 (18%/tier)", source: "my_read (Toolbox counts)", date: "2026-11-28"}
objective: {rung: 1, now: null, target: 4, eta_days: null}
check: {cadence: weekly, who: "Autistomatic", look_at: "coin balance vs next Vault / Menagerie cost, money gear on"}
method:
  - {rule: "Divine Knight is the best money farmer (orb); Matic is DK", source: "Griffy", date: "2026-08-03"}
  - {rule: "AFK spot: final map Pufferfins, best for EXP and coins", source: "Pulse 2026-10-31 (older: Green Mushroom is the biggest coin source, Pulse 2026-08-02; sheet says RG at Deck Hands, Pulse disagrees)", date: "2026-10-31"}
  - {rule: "rinse day: a half or full day of RG coin farming is an option, Wind Walker active is still better", source: "Pulse", date: "2026-10-31"}
  - {rule: "W7 coins: 5 new types, each 100x the last (~10B of the previous best for one)", source: "Pulse", date: "2026-10-16"}
buffs:
  - {source: "Emerald Bling Pendant", world: null, owned: null, now: null, next: null, owner: "Autistomatic"}
  - {source: "Draw Breaker prayer", world: 3, owned: null, now: null, next: null, owner: "Autistomatic"}
triggers:
  - {when: "Luminous Menagerie patch cost known", then: "set coin target to it"}
stall: {pulls_no_progress: 4, eta_over_days: 30}
tasks:
  - {do: "In-game: check Bling Pendant / Corsair / Rumble chip / Golden Bread / Draw Breaker on Matic", stat: "monster cash", gain_pct: null, unblocks: [], source: "Pulse 2026-08-02..11-11", active_min: 5, wait_hr: null, cost: null, urgent: false}
  - {do: "AFK Matic on final map Pufferfins with the money setup", stat: "coins", gain_pct: null, unblocks: [], source: "Pulse 2026-10-31", active_min: 2, wait_hr: 24, cost: null, urgent: false}
```
<!-- GOAL:END -->
