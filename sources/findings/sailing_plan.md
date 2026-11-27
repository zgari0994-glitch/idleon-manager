# Sailing plan, save 20261125T2340 (my calc with Toolbox's own artifact formula, parsers/world-5/sailing.ts)
- All 17 islands unlocked; transcendent tier unlocked (research grid 109), verisimilitude unlocked (Menagerie 0) but odds ~0 at Safari.
- 11 boats sat on Safari Island = 0% artifact odds (all 4 artifacts transcendent, next tier odds ~1e-9).
- Odds per chest for the best boat: World's End 5.07% (Obsidian + Ender Pearl new), Beachy Coast 2.98%, Rocky Peaks 1.35%, Isolated Woods 1.24%, Candied 1.13%, Toxic Bay 1.13%, Stormy 0.71%, Snowy 0.58%, The Maw 0.95% (4 new artifacts, 15h+ trips).
- Every boat reaches island 14 at minimum trip time (32 min) except boat 16 (level 94, reaches up to Candied). World's End at <=42 min: boats 13 and 11 only.
- Chest pile (30) fills in ~1h, so chest quality beats trip count: plan = boats 13 + 11 to World's End, everything else to Beachy Coast; re-rank after each find.
- Captains: no swaps needed; shop captains (A: 3% artifact lvl1, B/C/D cloud rolls) don't beat current ones.
- Sourced: Pulse 2026-09-02 boat lv400+ = Undead Battalion (3x treasure, 3x speed, more artifact find); Pulse 2026-10-23 lv600 boats big for artifact find; Pulse 2026-08-29 Black Market page 2 = 30% cheaper boat upgrades; Pulse 2026-10-31 harbor trick (de-level Unending Loot Search on Siege Breaker, boats wait in harbor, first-tier chests, hourly claims ~54 min, extra boats = 40 chests); Griffy 2026-01-08 replace low base-roll captains; Nocturne 2023: speed > loot > artifact > cloud (early game, outdated for this stage).

## 2026-11-26 goal reset (Zack): raise artifact find, not boat Lv 400
- Toolbox getBoatUpgradeCost (sailing.ts): costs compound ~10-17%/level. Lv 400 for each boat = 50x-14,000x banked loot (save 20261126T2330). Best on bank alone: Boat 1 -> 311, Boat 4 -> 310 (shared T0). Boat 14 (Lv 300) needs 10,000x+ its T18/T19.
- Undead Battalion 3x (Davey Jones) = boat Lv 400 AND Research grid 105. Nightmariner = Lv 600 boats + Menagerie unlock 13 (rank 21, 1.59M Lumi).
- Boat Discount = event shop 55 (30% off), not owned. Older Pulse note said Black Market page 2; Toolbox code wins.
- Ranked x1 levers: Magni Pufferfin 5x (+25x loot), Glimbo 2x, Artifacto Discoveries superbit 1.02^discoveries (35 = 2.0x), Purple Chest Slugs 1.5x/copy (summer event). Card: model/sailing.py ODDS_GOAL.
- Boat 14 (World's End) Captain F gives +0% artifact find; Boat 1's Captain A gives +119%.
