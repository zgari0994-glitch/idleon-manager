# Next actions (queue, Zack 2026-11-27). Work top to bottom, one per fresh thread. Remove a line when done.

1. NOW: Ticles bars (Melting Every Day). Zack needs 1B Copper Bars for a vial and bars for all God armor and beyond.
   Find how Melting Every Day turns AFK kills into forge/bar progress, what scales it, and the map creators park on (Griffy ypb7kpQov30 00:01, 2026-08-03 first, then Pulse/Nocturne). Then rebuild his afk line in model/jobs.yaml with a live finish line (Copper Bars have / 1B) and the sourced map. ~5 calls.
2. Tacular + Compass: does the AFK map matter, or does AFK only bank 1-hour skips spent on the dust map? Then make his park line per pull from the dust with the biggest need (upgrades that push the goal, accuracy, defense, medallion find chance). model/compass.py exists. ~5 calls.
3. Cranium Cooking (Cat): what scales it now (creators + data). It used to give ~10 levels per use. If it can't get back near that, drop it as its own active session. ~5 calls.
4. After the next phone pull: check one card (e.g. "card Totle"). The Park section should show cave + reason + "now:" with real mob names (not w7b6 codes). Confirms afk.py runs in the workflow.
5. Open gaps (fill as answers come): XP per cave not in the parser (Totle checks the AFK window), Tacular has no sourced Wind Walker spot (item 2 replaces it), Cat's Cranium line has no finish line (item 3).
