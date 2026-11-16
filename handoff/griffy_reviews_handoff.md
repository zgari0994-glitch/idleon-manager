# Handoff: Griffy account-review transcripts → "what would Griffy do" weights

## Goal
Find which IdleOn systems GriffyBit treats as blockers or priorities when he reviews accounts, and how strongly he says it. The output feeds a ranking formula, so **context matters more than mentions**: a bare mention counts for almost nothing.

## Source
Get each video's full transcript from youtubetotranscript.com: `https://youtubetotranscript.com/transcript?v=<VIDEO_ID>`. These are YouTube auto-captions, not summaries, so names are often garbled. Fix obvious garbles to the real system name, and mark anything you're unsure of with `?`.

## Videos (GriffyBit, channel UCt5WC8O9Jrb-UeNcI5T9BoQ)
| # | Video ID | Date | Title |
|---|---|---|---|
| 1 | RnnRamcdjQ0 | 2026-07-26 | One Character Build Is Killing Their IdleOn Progress |
| 2 | aUdMKlRf_v4 | 2026-07-19 | IdleOn Roast Reviews: Feucreeper / MasterClasses |
| 3 | 1OKlpmFi1mI | 2026-07-12 | NEW And IMPROVED Account Reviews (stream VOD, 7.5h; skip the Feucreeper segment, it duplicates #2) |
| 4 | kD7KZ5zX6Ss | 2026-04-23 | The Most IN-DEPTH Account Review I Have Ever Done |
| 5 | GiVFMYM5ZCU | 2026-01-10 | IdleOn Account Reviews: Agent_Rich |
| 6 | i0OYlSX5yVY | 2025-02-09 | IdleOn Account REVIEW: Burger - Deathbringer |
| 7 | x4_MMA9sNO4 | 2024-10-17 | Insane IdleOn End Game Account Review Bingo |
| 8 | licmpceAPIc | 2024-10-30 | What's Behind This WILD Idleon Account Review Bingo |
| 9 | R3YZ6D-EHHE | 2024-10-06 | IdleOn Account Roast: Jordan - World 4 Prep |
| 10 | d3A2hYegsm4 | 2024-09-01 | IdleOn Account Review BINGO Changed Everything |
| 11 | rYUgBM6N4Os | 2024-02-26 | IdleOn Account Reviews: River - Alchemy and Overall Account |

If you find more GriffyBit account reviews, roasts or bingos (videos or stream VODs), add them with the same columns.

## What to extract (per video)
1. **Account stage** of the reviewed account: the world they're pushing (e.g. "early W7", "W5"), plus anything notable (F2P, endgame, one-character).
2. **Every verdict Griffy gives about a system.** Only statements where he judges it, like "this is holding you back", "you need to", "you're missing", "biggest thing", "max this", "this is fine", "don't bother". Skip descriptions, jokes and reading numbers aloud with no judgment.

## Output: ONE CSV file, one row per verdict
Columns:
- `video_id`
- `date` (YYYY-MM-DD)
- `stage` (account stage from step 1)
- `system`: use EXACTLY one name from the list below (pick the closest); if nothing fits, write `OTHER: <name>`
- `verdict`: one of `blocker` (holding the account back / biggest problem), `priority` (do this soon / important), `upgrade` (worth improving but not urgent), `fine` (good enough / done), `skip` (not worth it / don't bother)
- `strength`: 1 = passing remark, 2 = clear recommendation, 3 = he stresses it or repeats it (biggest, most important, huge)
- `detail`: max 25 words, your paraphrase of what exactly he says to do (target, item, level if given)
- `timestamp` (mm:ss or hh:mm:ss, approximate is fine)

## System names (use these exactly)
Alchemy (Bubbles), Vials, Sigils, Stamps, Statues, Star Signs, Talents / Library, Obols, Post Office, Upgrade Vault, Owl, Bribes, Smithing / Forge, Mining, Chopping, Fishing, Catching, Trapping, Worship / Tower Defense, Prayers, Refinery / Salts, Salt Lick, Construction / Cogs / Shrines, 3D Printer / Sampling, Death Note, Atom Collider, Equinox, Breeding / Pets, Cooking / Meals, Lab / Chips / Jewels, Rift, Sailing / Artifacts, Divinity, Gaming, Slab, The Hole / Caverns, Farming, Sneaking / Jade, Summoning, Emperor, Islands, Greenstacks / Storage, Cards, Golden Food, Gear / Armor / Tools, Drop Rate, Crystal Mobs, Money, Gem Shop, Arcade, Kilroy, Ballots / Meritocracy, Merits / Task Board, Achievements, Party Dungeons, Colosseum, Weekly Boss, World Bosses, Companions, Combat / Damage / Accuracy, Candy / AFK, Tome, Grimoire (DB), Compass (WW), Tesseract (AC), Royal Guardian, Character Levels / Classes, Spelunking, Research, Coral Reef, Clam Work, Jelly Operator, The Button, Sushi Station, Zenith Market, Gallery / Trophies, Legend Talents, Luminous Menagerie, Advice Fish

## Also return (short, at the end of the chat)
- Per video: stage + his top 3 calls in one line.
- Any video you couldn't get a transcript for.

Name the file `griffy_review_verdicts.csv`. Zack uploads it back to Claude, which turns it into the weights (recency-weighted, blockers and priorities count most).
