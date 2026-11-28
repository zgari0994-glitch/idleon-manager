# Next actions (queue, Zack 2026-11-27). Work top to bottom, one per fresh thread. Remove a line when done.

1. NOW: Tacular + Compass: does the AFK map matter, or does AFK only bank 1-hour skips spent on the dust map? Then make his park line per pull from the dust with the biggest need (upgrades that push the goal, accuracy, defense, medallion find chance). model/compass.py exists. ~5 calls.
2. Cranium Cooking (Cat): what scales it now (creators + data). It used to give ~10 levels per use. If it can't get back near that, drop it as its own active session. ~5 calls.
3. After the next phone pull: check one card (e.g. "card Totle"). The Park section should show cave + reason + "now:" with real mob names (not w7b6 codes). Confirms afk.py runs in the workflow.
4. Open gaps (fill as answers come): XP per cave not in the parser (Totle checks the AFK window), Tacular has no sourced Wind Walker spot (item 2 replaces it), Cat's Cranium line has no finish line (item 3).
5. Ticles bars follow-ups (bars line done 2026-11-27, commit 29d10b7+):
   a. After the next pull: check his card shows "Copper Bars x / 1B" and the Green Mushroom line. Load more forge slots with Copper Ore (only 1 of 16 was copper).
   b. Copper Ore supply for 1B bars: check ore in storage vs need.
   c. Gods gear other ingredients (Marble helmet, fish, Royal Fabric etc.) per item: idleon.wiki item pages, ~3 calls.
   d. Vial costs per level (Barium 12, Barley 11, Dreadnog 8) not in parser: source them.
   e. Zemo bones push: map + finish line not set (gap line in jobs.yaml).
   f. Ticles Smelting Every Day talent level not found in parser.

- [PC pull, Zack 2026-11-28] Companions: read owned pets from the Toolbox Companions page in the built-in browser (raw copy has no companion data). Write owned list into the snapshot, then mark base/special pets in brain/systems/companions.md from real data.
