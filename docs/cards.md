# Cards, brain/report/decision layer, wording, goal logic, locked = target, clocks
Moved verbatim from CLAUDE.md on 2026-11-26 (usage cleanup). Rules here still apply; CLAUDE.md core wins on conflict (usage budget, thread split).

## Card wording (Zack 2026-11-19)
Plain English, like someone talking. Lead with what to do, a few words of why. Round numbers (29M, not 29,042,118), one number pair at most, no formulas, no breakdown/multi/group talk, no internal IDs or design notes. Sources short: "Griffy: ...", "(my read)". Locked items in one line. `model/plain.py` cleans every line as a safety net; write lines plain at the source. Raw labels it can't clean are dropped; spots that keep producing jargon go to `sources/findings/wording.md` (rewritten each build). Don't re-pull or rebuild just for wording: fix those spots at the planner on the next card build.

- Library checkouts: always show the account rank (#1-55) on every talent line, in cards and when relaying a card in chat. Ranking is rebuilt every pull (extras.talent_rank -> plans/talents_<save>.json), so bought talents drop off and the next ones move up. Zack works single digits first (Zack 2026-11-21).

## Systems, freshness, can't-miss (Zack 2026-11-21)
- Every owned system shows on its character's card every day; every system that pushes the account gets a standing goal + plan (help the main goal first, never "not now").
- GOAL LOGIC (Zack 2026-11-21, exact): the main account goal = the biggest account blocker, with a measurable, achievable target (now: Spelunking POW 900K). When the target is reached, re-check: if Spelunking is no longer the biggest blocker, the new biggest blocker becomes the main goal. If the main goal is BLOCKED by another system, the main goal does NOT switch: that system's owner makes "unblock it" their character main goal and hard-focuses it, and every task in that system becomes a step toward the unblock (map blocked -> someone pushes the map; farming needs levels -> every farming task aims at that) until it is unblocked.
- Never accept stale data: daily counters from this pull's save/timers (every pull refreshes dashboard timers); a page that won't refresh gets diagnosed with the site index (sources/creators/idleon-toolbox-guide.md) and fixed quietly, then reported.
- brain/cant_miss.yaml = time-sensitive dailies (shown at the top of the owner's card until done).
- Queue: Construction facelift (Tiny/Polymer cogs, Flaggy, board review vs meta), Gaming plan, then every system. See plans/pending_changes.md.

## Locked = target (Zack rule)
Never hide or drop a locked item. Show it with exactly what unlocks it, where the character is now on that path, and put the unlock on the owner's daily run.

## Clocks
Game save = `data.TimeAway.GlobalTime` (UTC epoch). Store UTC, show Eastern. Always tell Zack the game-save age; data is only as fresh as the game's last cloud save.

## Brain + Report + decision layer (Zack 2026-11-21, supersedes "cards come straight from planners")
- Order after plan.py (from the AutoReview folder, PYTHONPATH=.:<repo>/model): cards2.py -> report.py -> decide.py -> cards3.py. Outputs `reports/<save>/{report,decisions}.{md,json}` and `plans/cards4_<save>.md` (Spend / Do / Bags / Don't / Working toward / Locked / Notes / Park). Guide Zack from cards4, one character at a time. cards3 keeps cards2's parent/sub structure: status lines and multi-day targets never reach Do.
- Read `brain/README.md` first. Flow: snapshot -> Report (every system, stored per save) -> decision layer (`decisions.md`, reserves + links + goal) -> I review decisions -> cards (Spend / Do / Park only).
- `brain/index.md` = every system and whether anything checks it. `tools/build_brain.py` refreshes AUTO blocks only; curated note text is kept.
- `brain/reserves.yaml` is checked before any spend line. `brain/checklist_2026-11-21.md` is the acceptance test.
- Super talents can be reset, but resets are limited (~70, Zack 2026-11-21): picks stay sourced only, suggest a reset only when the current super is wrong vs the sourced list, and say it costs one reset.
- Super talents: preset role (fight/skill) comes from where that preset's regular talent points are spent, never from existing supers; no pick on both presets unless sourced; pick must be in the class tree with points on that preset.
- Lesson 2026-11-21: the 40 gaps logged 11-17 were never closed and weekly boss / anvil / Jade / Bubba / Poppy fell out when the old docs system was replaced (Daily-Rotation step 9 and KB section 26 held the weekly boss how-to). When replacing anything, carry every checked item over and list what moved where.

## AFK park lines v2 (Zack 2026-11-27, model/afk.py + model/goalpick.py)
- Rebuilt every pull. Ranked candidates: LAW (weekly override, Law 2 duties only he does, Law 1 goal) > JOB (jobs.yaml afk list, live finish line) > CLASS (sourced spot) > MY READ (+ gap). Each line: world/map/mob, why, finish line, source.
- Hit targets retire automatically (card "retired: X", state/retired.json) and never stay on a card. A line with no finish line is flagged. Goal target hit -> re-check.
- "now: X" when the save shows him elsewhere. Same off-line spot 2 pulls -> "keep?" prompt. `tools/afk_pin.py <nick> active <activity>` pins 3 pulls, `<nick> clear` removes.
- Spelunking spots (re-checked every pull): cave N drops Chapter N pages (1 Fearful Tunnel, 2 Decaying Crevasse, 3 Buried Church, 4 Coral cave, 5 Pirate Upper Deck cave). Every cave 1-4 covered; Royal Guardians + strongest on the deepest; everyone else on their most efficient cave (my read: level 50+ cave 4, 30+ cave 3, 10+ cave 2), then spread by page need, cave 1 fewest. Close calls flagged: Zack decides in the moment. Nobody fit for cave 4 -> goal card says what it takes. GAP: XP per cave not in the parser.
- Not tracked (Zack 2026-11-27): monument placement outside monument week. Zemo bones-mob line removed.
