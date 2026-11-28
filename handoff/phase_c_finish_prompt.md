Phase C finish (last bit before tests). Repo zgari0994-glitch/idleon-manager, follow CLAUDE.md. Save = snapshots/LATEST (say its age). Budget ~20-25 calls: batch each step into one script, dry run, one commit + push at the end. No pull.

Done already (2026-11-28, don't redo): Phase C A-E; owner tie-breaks (Grimoire = Zemo, Topher bench; Killroy = Tastic warrior / Tacular archer / Cat mage, locked; Printer = every character own prints; mismatches fixed with check.helpers / check.split); guild dropped (Zack: ignore it); cog board = Toolbox optimizer, no creator guidance needed.

1. Half-baked step D items: make each one good to go or say exactly why not. World bosses (parsed?), weeklyBossesRaw decode, compass dust type, Lunarheim boss POW requirement. For each: run it on the latest save, sanity check vs Toolbox / game data, fix, show the card line it produces.
2. Royal Armory: get what we can. What's in the save + Toolbox parser (model/royal_armory.py exists), map it in data_map.yaml, live now_path on its GOAL block, owner (Royal Guardians: Tastic / Matic, check jobs + GOAL), card line.
3. Gap list: every GOAL block with coverage partial/none, "my_read" rungs, or a logged "# gap:" -> one table: system, gap, plan to fill (source to find, data to map, or Zack decides). Show me, I pick.
4. Scoring calibration (docs/scoring.md): python3 model/score.py --top; flag anything that looks wrong (order, ties, a quick task outranking a blocker unfairly) with the inputs that caused it. Propose fixes, don't apply until I say go.
Then tests: phone pull, then "card Tastic" and "card Cat" from the phone.
