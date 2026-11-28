# Phase C plan (Zack 2026-11-28, after Phase B commit 023857f). Save 20261128T0256.
Each step: digest first, Zack OK, build in one pass, dry run, commit + push. Est. calls in [ ].

## Zack's answers (standing unless he changes them)
- Quick tasks at 95-98 are fine ("pound out simple tasks"); a tie-break is optional, only if it helps.
- Goals are re-evaluated fluidly. Hand-written goals come only from Zack and get challenged when inefficient (card says why, with source).
- Anvil: no quantity tracking needed, but show each character's anvil setup.
- Companions: ignore. Construction costs: ignore. Owl feathers: ignore (pushed passively with Bubba + Poppy). Trash balance: Zack runs it.
- Obols: Zack's setup on every character + family = silver Pop, gold Trip 6s, platinum Yahtzee 6s, molten Dead Divine. Only flag if creator meta changes; otherwise obols are disregarded.
- Trash shop: after Fractal opens (570 bottles), tell Zack what to buy.
- Salt: only care that saltlick/refinery items are not stalling salt production.
- Cog board: review vs newest creator guidance (things changed since 2024).
- Advice Fish: add currency if it's in the save, else wing it.
- Trophies (minigames): only have it / not yet, no how-to.

## Steps (in order)
A. Live "now" + real stall [~8] DONE 2026-11-28 (docs/planners.md Phase C A+B)
   - Add `now_path` per GOAL block (data_map path or a small resolver in goals.py), refreshed every pull. No path -> "now: not in save" (never None).
   - Stall fingerprint = the now_path value only (not the whole system blob), so timers can't fake progress. Fixes gap 8.
   - TARGET HIT works anywhere now + target are numbers.
B. Machine triggers + goal challenge [~6] DONE 2026-11-28
   - Trigger rows get `when_path` + op/value; fired triggers put "then" on the target system owner's card, armed ones show as "next".
   - Rule: objectives recomputed each pull; Zack-written objectives kept but flagged "challenge?" when a sourced order or score says it's inefficient. Update CLAUDE.md LAWS/Card jobs, docs/planners.md, Project memory, give Zack Project description text.
   - Optional: tie-break equal scores by value (impact x reach) so the quick top 10 orders sensibly. No effort floor.
C. Anvil setup + lookup systems + trophies [~8]
   - Anvil: decode anvilSelected/anvilProduction to item names (Toolbox item list in tools/tbparse) and point split (speed/cap/exp); per-character "producing X, Y; points S/C/E; unspent N" on Do 1. Gas Shard + Historium bars named once mapped. Verify Topher -435 / Bish cap 0.
   - lookup.py: add anvil, bubba, super_talents, palette, poppy, snail_mail, weekly_boss, world_bosses; fix shrines rows.
   - Trophies: read owned trophies from the save; minigame lines say "Darter Trophy: have / not yet" (basketball, darts, minehead, any other minigame trophy).
D. Data gaps that still matter [~6]
   - Salt: flag only if a refinery/saltlick input is short and production stalls.
   - Trash shop: buy list on Fractal unlock (trigger from B).
   - Obols: meta watch only (source refresh compares Zack's setup above vs newest Griffy/Pulse; flag on change).
   - Advice Fish currency from raw save if present.
   - Still open: world bosses (not parsed), weeklyBossesRaw decode, guild reads as none (check in game), Royal Armory, compass dust type, Lunarheim boss POW requirement.
E. Cog board review vs creator guidance [~5, research: ask first]
   - Current board (126 spare cogs, EXP mult 1x) vs newest Griffy > Pulse = Nocturne layout guidance; report sourced vs my read.

Suggested threads: 1 = A + B (~14). 2 = C (~8). 3 = D + E (~11).
Owner tie-breaks still waiting on Zack: Grimoire (Zemo + Topher), Killroy (class of the week), Printer (Ticles, Matic, Naut, Zemo); mismatches cog_board, death_note, glimbo, grimoire, inventory, statues.
