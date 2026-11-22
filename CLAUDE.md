# IdleOn Manager (Zack's account, profile Autiszemo, 11 characters)

## LAWS (Zack 2026-11-21, override everything below)
1. Goal chain: the main account goal is the biggest account blocker (measurable target). If another system blocks it, that system's owner makes the unblock their character goal and hard-focuses it, and every task in that system aims at the unblock. The account goal stays until its target is reached, then re-check.
2. Focus never means neglect: a character hard-focusing a blocker STILL does every other system and duty they own, every day. Example: if Construction is the blocker, Autistastic hard-focuses Construction AND still checks his Royal Guardian duties, Gaming and everything else on his card. Nothing drops off a card because something else is the focus.

## How Zack works
- Shop buy orders (Zack 2026-11-21): every system shop shows a sourced buy order on its owner's card (next level, cost vs balance, source per line). Spelunking amber done (model/spelunking.py BUY_ORDER); rest in plans/pending_changes.md.
- Sourced order beats my math (Zack 2026-11-21, after Blooming Axe was ranked over Grand Martial): when a creator names a priority, it goes first. My own weights or gain-per-cost math only order items inside the same sourced tier, never above a sourced pick.
- Digest first: explain understanding + plan, execute only on his approval. Design changes as a whole, no patch-on-patch.
- Zack Mode: short, direct, no em dashes, no filler. Lead with the one most important move, then an ordered list. Exact numbers.
- Guidance = what data and sources say. Own opinion only when he asks "what do you think". Never invent setups.
- Source priority: Griffy > PulseIdle = NocturneGaming (YouTube, endgame; Nocturne may be outdated) > Toolbox / idleon.wiki > 2023 Guide Sheet > Reddit / Discord > rest. Newest wins within a level. Flag fan sources.
- Creators (Zack 2026-11-19): Griffy first; Pulse + Nocturne are tier 1b. Where Griffy lacks advice, Pulse/Nocturne STAND IN as the guidance (say who it's from). Where Griffy covers it, they supplement (expand what he skipped) and confirm. On conflict the newest claim wins (Zack 2026-11-19) and the older one is shown as 'older:'. All accurate source data that adds to guidance is used. A system is a gap only when none of the three cover it.
- Systems AutoReview doesn't rate (and new-world systems): guidance from the creators as above; only where none of the three covers it, report the gap to Zack, never fill it.
- Creator sources live in `sources/creators/<creator>/` (raw transcripts + verdict CSVs, committed by ChatGPT). Read with code, never whole.
- Weekly confirmations (e.g. Kilroy) live in `state/confirmed.json` keyed by week start; a weekly job shows on its cards from the weekly reset until Zack confirms it.
- Rinse goal: answer "what would Griffy do" for an account at Zack's stage.

## Guidance layer (2026-11-19)
- `model/guidance.py` -> guidance.json (all creator tags, weighted creator/type/stage/recency). Feeds rinse push weight and plan.py card lines.
- Card line = Push (AutoReview What) + HOW/WHY (creator claim matched to that item, 2024-06+) ; CREATORS = top system-level how_to/priority/blocker/warning (no narration, 2024-06+).
- Prereqs: AR lock phrases + jobs.yaml `locked` route "Unblocks X" to the unlocking owner's card (top block) and "BLOCKED on Y's job" on the waiting card.

## System planners (Zack 2026-11-19: "this level for all aspects")
- Standard per system: Toolbox numbers + breakdowns + bundle formulas -> model -> concrete moves on owner cards with exact gains -> a "Toolbox should now show N" check -> phases (now / later / gate) -> recomputed every refresh.
- Read a Toolbox page: preview_start the page, paste `tools/tb_read.js` into javascript_tool (all tabs, Details on, every breakdown dialog), close tab, `python3 tools/tb_save.py <result file> <system>` -> snapshots/<LATEST>/toolbox/<system>.json.
- Done: Sailing (`model/sailing.py`, Autisticles + odds levers routed; daily captain shop/trades/boat upgrade checks with explicit move-buy-swap-send steps, Zack 2026-11-21), Farming (`model/farming.py`, Zemo), Cooking (`model/cooking.py`, Zemo), Divinity (`model/divinity.py`, Bish), Breeding (`model/breeding.py`, Tacular), 3D Printer (`model/printer.py`, per-character slots), Alchemy (`model/alchemy.py`, Cat), Prayers (`model/prayers.py`, every card + print-day plan, soul reserve 5%), Stamps (`model/stamps.py`, Topher), Greenstacks (`model/greenstacks.py`, Totle; writes model/protect.json that spenders read), Statues (`model/statues.py`, Ticles turn-ins), Refinery (`model/refinery.py`, Autistastic Construction; safe rank + limiter + soul use/hr), Worship (`model/worship.py`, totem waves -> prayer unlocks on Autistacular, soul cover days on Bish, every_character Worship: level + charge per card), Compass (`model/compass.py`, Tacular: portals, dust buys vs AutoReview, exalt-vs-tier conflict, abominations, Moon of Print), Grimoire (`model/grimoire.py`, Zemo: optimizer buys, next unlock, cross-system upgrades, Pure Opals routed to Bish), Death Note (`model/deathnote.py`, Topher Super CHOWs + Zemo ZOW/CHOW + closest Eclipse, ETAs from two Toolbox reads), Equinox (`model/equinox.py`, Topher: bar cap alert, claimable challenges, locked unlocks), Atom (`model/atom.py`, Autistastic Construction: Neon first, Helium ETA), Salt Lick (`model/saltlick.py`, Topher buy-now + Refinery line), Armor (`model/armor.py`, missing parts per set), Vault (`model/vault.py`, Topher, coins.py costs, top-need upgrades first), Tesseract (`model/tesseract.py`, Cat), Royal Armory (`model/royal_armory.py`, AutoReview only until the Toolbox page loads), Post Office (`model/postoffice.py`, every_character boxes), Lab (`model/lab.py`, Cat: rotation shortfalls), Buildings (`model/buildings.py`, Autistastic: Ready+slotted, slot targets, blocked materials), Gaming (`model/gaming.py`, Autistastic), Sneaking (`model/sneaking.py`, Tacular), Summoning (`model/summoning.py`, Cat), Spelunking (`model/spelunking.py`, Autistomatic; cave gates routed to the systems they unlock), W7 minis (`model/w7minis.py`, Autisticles: Legend, Jelly, Clam, Sushi, Minehead, Glimbo, Zenith/Button gates; Zack: Minehead+Glimbo go to the W7 mini owner), Menagerie (`model/menagerie.py`, Ticles), Research (`model/research.py`, Totle), Reef (`model/reef.py`, Chio; shrine gates routed to Autistastic), Gallery (`model/gallery.py`, Chio), batch C in `model/batchc.py` with thin wrappers: Emperor (Zemo, Zack: best fighter pushes bonuses), Islands (Tastic), Arcade (Ticles W7 minis block), Owl (Topher), Killroy, Hole (Bish), Slab, Beanstalk (Zemo Farming), Cape Vine, Shops+Ballot (Totle), Tome (Topher), Maintenance Rift/Star Signs (Topher). Planners without char_lines fill only the first matching block. Helpers in `model/tbhelp.py`; a second planner on the same block appends. `model/rates.py` = item income from two saves (spend -> how it's replaced). Map sweep: tools/resection.py re-files mis-tagged creator advice; every_character jobs in jobs.yaml. Buys are ranked with `model/spend.py` (gain per share of balance, per currency, source-weighted). Planners register in plan.py PLANNERS. Order next: Farming, Cooking, Breeding, 3D Printer, Alchemy, Stamps, Statues+Greenstacks, Prayers+Worship, Compass/Grimoire/Death Note, Equinox/Atom/Tesseract/Vault/Salt Lick/PO/Armor, rest.
- Per system: report to Zack what system + what was discovered BEFORE building it.
- Account priority = biggest current need, computed every pull by `model/priority.py` (Zack 2026-11-19: never pinned; cooking speed is one input). Need outweighs math (Zack 2026-11-19): when systems compete for the same thing (seats, characters, currency), focus goes to the bigger current NEED (account priority, blockers, prereqs other jobs wait on), not the most-behind tier or the best ratio. Focus it until it reaches an acceptable spot, never cripple the other side, then rebalance.
- Pinchy = reference only (AutoReview account stage), owned by no one.

## Brother's account (Zack 2026-11-19)
- `accounts/brother/` = his separate dashboard (IdleOnLech, 10 chars), fully automatic via his upload page + GitHub Action + Cloudflare Pages (no Claude usage). See accounts/brother/README.md. Never mix his data into Zack's snapshots/plans; Zack's own flow below is unchanged.

## Usage rules (the limit is the #1 constraint)
- No scheduled/hourly tasks. Pull data only on request or at the start of a play session.
- Never read big docs whole. Read `snapshots/$(cat snapshots/LATEST)/meta.json` first, then only the sections/characters the question needs (query with python/jq).
- Never dump raw browser data into context; always use the gzip+file trick below.
- Old Project docs (Index.md, KB, Daily-Rotation...) are legacy reference: search them for one section when needed, never load whole.

## Refresh (≈3 tool calls)
1. Built-in browser: `preview_start` https://idleontoolbox.com/account/misc/general (signed-in session = live save; no Upload needed).
2. javascript_tool (wait ~6s first):
   `const s=sessionStorage.getItem('rawJson'); const cs=new Blob([s]).stream().pipeThrough(new CompressionStream('gzip')); const buf=new Uint8Array(await new Response(cs).arrayBuffer()); let b=''; for(let i=0;i<buf.length;i+=32768) b+=String.fromCharCode.apply(null,buf.subarray(i,i+32768)); const b64=btoa(b); 'GZB64|'+b64.length+'|'+b64+'|END|'+'x'.repeat(60000)`
   The result is saved to a /tmp/claude-tool-results file. Close the tab right after.
3. `tools/snapshot.sh <that file>` -> decodes, runs AutoReview's own code (no website), writes `snapshots/<save UTC>/` and updates `snapshots/LATEST`. Commit + push.
- Public fallback (older, only as fresh as last Upload): profiles.idleontoolbox.workers.dev/api/profiles/?profile=Autiszemo (fetch from a Toolbox tab; workspace shell and WebFetch are blocked).

## Play-session flow (keep it this short)
1. Refresh (above). 1b. Timers: `preview_start` https://idleontoolbox.com/dashboard, wait ~6s, javascript_tool: click every "Show N more", then return `'TBDASH|'+new Date().toISOString()+'|'+document.querySelector('main').innerText+'|END|'+'x'.repeat(60000)`; close tab; `python3 tools/timers.py <file> snapshots/<LATEST>/timers.json`.
2. `python3 tools/build_system_index.py` (only after jobs.yaml/source changes) · `python3 model/ledger.py` (materials vs last save) · `python3 model/coins.py` (coin costs vs money) · `python3 model/buffs.py` (buff sources: every stat's sources owned/missing, routed to owners; run before plan.py) then `python3 model/mechanics.py` 3. `python3 rinse/rinse.py` 4. `python3 model/plan.py` 5. `python3 model/acquire.py` (wiki sources in sources/ are static; re-pull only after a game update)
6. `python3 model/cards2.py` (cards v3: Goal card + per character Dailies / Housekeeping / Goal part / Park; writes plans/cards_<save>.md, plans/cards.json, dashboard/cards.html) -> republish dashboard/cards.html as index.html with publish_files (slug + version in dashboard/ARTIFACT; update version after). Old dashboard.py is the fallback. cards2 pulls in: model/supertalents.py (sourced super picks, open points from save), model/extras.py (RG super hold + unlock trigger, cooking mastery conditions, research points, lab chip end-goal sets + jewels, Naut/AC roster rules, voting, talent ranking 1-55 stored as plans/talents_<save>.json), model/cardpresets.py, plans/trapping.md, plans/money_plan.md. Findings: sources/findings/{divinity_map,kill_milestones,reef_cages,goal_pow_900k}.md. Spec: plans/pending_changes.md 'Agreed spec'. Goal lives in cards2.GOAL (change only with Zack's OK).
7. Guide Zack one character at a time from that character's card only (finish every job before moving on). Never dump all 11.
8. Zack flags what's wrong / unwanted / missing -> after his OK, add to `sources/findings/gaps.md`. Morning run = gap review (findings, tagged rows, index; huge -> ChatGPT Lane A in queue.md).

## "After work" pull (Zack 2026-11-19) = the one full fresh pull of the day
Trigger: Zack says "after work" (he has cloud-saved, closed Steam, is on the tablet). Other refreshes only when he asks.
1. Refresh the save (steps above) + dashboard timers (play-session 1b).
2. Bulk Toolbox read in ONE tab: preview_start any Toolbox page, javascript_tool with `const PAGES=<tools/tb_pages.json compact>;` + `tools/tb_read_multi.js` (hidden iframes, 5 at a time, ~8 min for 55 pages). Poll `window.__tbm ? 'DONE' : 'pending '+window.__tbm_done` (~40s waits). When DONE return `window.__tbm` (saved to a result file), close the tab, `python3 tools/tb_save_multi.py <file>`. Sailing is in the bulk list (saver writes toolbox/sail_detail.txt for model/sailing.py). Retry rule: a slow page waits longer, then reloads once. Pages that still fail keep yesterday's read (listed in toolbox/_from.txt): say so.
3. Pipeline (play-session step 2-6) -> cards + Active plan + dashboard republish. Tell Zack the save age.
4. Cards: dailies, parking, jobs per character. Then ONE block at the end: Active plan = Overnight on the PC (top 2, one long push for one character), Active play tonight (top 5, best first), Morning while at work (idle-friendly checks). Built by `model/active.py`, ranked by biggest need (`model/priority.py`) then job importance.

## Card wording (Zack 2026-11-19)
Plain English, like someone talking. Lead with what to do, a few words of why. Round numbers (29M, not 29,042,118), one number pair at most, no formulas, no breakdown/multi/group talk, no internal IDs or design notes. Sources short: "Griffy: ...", "(my read)". Locked items in one line. `model/plain.py` cleans every line as a safety net; write lines plain at the source. Raw labels it can't clean are dropped; spots that keep producing jargon go to `sources/findings/wording.md` (rewritten each build). Don't re-pull or rebuild just for wording: fix those spots at the planner on the next card build.

- Library checkouts: always show the account rank (#1-55) on every talent line, in cards and when relaying a card in chat. Ranking is rebuilt every pull (extras.talent_rank -> plans/talents_<save>.json), so bought talents drop off and the next ones move up. Zack works single digits first (Zack 2026-11-21).

## Systems, freshness, can't-miss (Zack 2026-11-21)
- Every owned system shows on its character's card every day; every system that pushes the account gets a standing goal + plan (help the main goal first, never "not now").
- GOAL LOGIC (Zack 2026-11-21, exact): the main account goal = the biggest account blocker, with a measurable, achievable target (now: Spelunking POW 900K). When the target is reached, re-check: if Spelunking is no longer the biggest blocker, the new biggest blocker becomes the main goal. If the main goal is BLOCKED by another system, the main goal does NOT switch: that system's owner makes "unblock it" their character main goal and hard-focuses it, and every task in that system becomes a step toward the unblock (map blocked -> someone pushes the map; farming needs levels -> every farming task aims at that) until it is unblocked.
- Never accept stale data: daily counters from this pull's save/timers (every pull refreshes dashboard timers); a page that won't refresh gets diagnosed with the site index (sources/creators/idleon-toolbox-guide.md) and fixed quietly, then reported.
- brain/cant_miss.yaml = time-sensitive dailies (shown at the top of the owner's card until done).
- Queue: Construction facelift (Tiny/Polymer cogs, Flaggy, board review vs meta), Gaming plan, then every system. See plans/pending_changes.md.

## Never say "no data" (Zack rule)
Before a card says no data / gap, check the Toolbox map (sources/creators/idleon-toolbox-guide.md), the system index, the dashboard timers and the raw save. If Toolbox shows it, the card uses it.

## Guiding before the knowledge base is done (Zack 2026-11-17)
Zack wants guidance now. Where Griffy/Pulse/Nocturne have nothing yet, guide from the data (save, Toolbox, AutoReview, game formulas) plus my best read, clearly labeled "my read". Sources upgrade it later; never stay silent just because creators haven't covered it.
Active time focus: push every attainable missing buff source (model/buffs.md). Dailies = bare minimum: check jobs, make sure nothing is wasting.

## Buff sources (Zack 2026-11-17)
Before explaining any level/stat (talent levels past book cap, plate levels, drop rate...), read its list in model/buffs.md. Never guess where levels come from.

## Talent levels (lesson 2026-11-17)
A talent's shown level = book level + bonus levels. Check the book level (max book now 299): Generational Gemstones 368 -> 372 = book 295 -> 299, so it IS a Library checkout.

## Locked = target (Zack rule)
Never hide or drop a locked item. Show it with exactly what unlocks it, where the character is now on that path, and put the unlock on the owner's daily run.

## Clocks
Game save = `data.TimeAway.GlobalTime` (UTC epoch). Store UTC, show Eastern. Always tell Zack the game-save age; data is only as fresh as the game's last cloud save.

## Layout
- `tools/` decode_pull.py, run_ar.py (AutoReview code -> structured JSON), snapshot.sh
- `snapshots/` one folder per game save: raw.json.gz, review.json.gz, chars.json (per-character facts), systems.json.gz (105 parsed systems), meta.json
- `model/` jobs.yaml (layer 2, curated), build_map.py -> map.md (layer 1 facts + layer 2 jobs + tiers)
- `model/` also: mechanics.py -> mechanics.md/json (rule-changers, packs, achievements, trophies/capes), plan.py (daily cards), dashboard.py
- `plans/` per-save daily plans; `dashboard/` page + ARTIFACT pointer
- `rinse/` rinse.py = Thigh Gap v2 formula (ChatGPT build) with Griffy recurrence from griffy_topics.yaml; latest.json
- `model/acquire.py` -> acquire.md/json (missing trophies/capes/nametags/hats + open achievements, wiki sources, in-game vs paid vs event)
- `model/system_index.yaml` (system -> Toolbox page -> AutoReview -> sources -> owners; built by tools/build_system_index.py) · `model/ledger.py` (materials) · `sources/findings/` (saved research + queue.md for ChatGPT)
- Tagging DONE 2026-11-19: all transcripts tagged (ChatGPT 24, Claude Sonnet 5.5 Batch API 291 via handoff/run_tags.py, ~$14.77). ChatGPT tagging retired. New videos later: make_packets.py -> run_tags.py pilot/submit/collect on Zack's PC -> merge_tags.py.
- Tagging pipeline: `tools/make_packets.py` (trimmed packets + ORDER.csv) -> ChatGPT per `handoff/TAGGER.md` writes `handoff/tags_out/` -> on "check tags" run `python3 tools/merge_tags.py` (validates, writes full CSVs to sources/creators/<c>/tags/), commit.
- `tools/timers.py` (Toolbox dashboard timers + AFK spots) · `plans/w7_push.md` (Griffy W7 path + gaps)

## Brain + Report + decision layer (Zack 2026-11-21, supersedes "cards come straight from planners")
- Order after plan.py (from the AutoReview folder, PYTHONPATH=.:<repo>/model): cards2.py -> report.py -> decide.py -> cards3.py. Outputs `reports/<save>/{report,decisions}.{md,json}` and `plans/cards4_<save>.md` (Spend / Do / Bags / Don't / Working toward / Locked / Notes / Park). Guide Zack from cards4, one character at a time. cards3 keeps cards2's parent/sub structure: status lines and multi-day targets never reach Do.
- Read `brain/README.md` first. Flow: snapshot -> Report (every system, stored per save) -> decision layer (`decisions.md`, reserves + links + goal) -> I review decisions -> cards (Spend / Do / Park only).
- `brain/index.md` = every system and whether anything checks it. `tools/build_brain.py` refreshes AUTO blocks only; curated note text is kept.
- `brain/reserves.yaml` is checked before any spend line. `brain/checklist_2026-11-21.md` is the acceptance test.
- Super talents can be reset, but resets are limited (~70, Zack 2026-11-21): picks stay sourced only, suggest a reset only when the current super is wrong vs the sourced list, and say it costs one reset.
- Super talents: preset role (fight/skill) comes from where that preset's regular talent points are spent, never from existing supers; no pick on both presets unless sourced; pick must be in the class tree with points on that preset.
- Lesson 2026-11-21: the 40 gaps logged 11-17 were never closed and weekly boss / anvil / Jade / Bubba / Poppy fell out when the old docs system was replaced (Daily-Rotation step 9 and KB section 26 held the weekly boss how-to). When replacing anything, carry every checked item over and list what moved where.

## Keep rules current (Zack 2026-11-21)
When a rule changes: update this file, Project memory (`/projects/.../areas/idleon.md`, standing rules only) and give Zack the Project text to paste, in the same turn. Project docs are legacy reference (see claude/00-READ-FIRST.md); never act on them over the repo.

## Status (2026-11-21)
Done: card engine v3 (cards2.py), 66 system planners, system index, ledger, coins, guidance layer, tagging, brother's dashboard.
Building now (in order): Report -> reserves -> decision layer -> cards from decisions -> fill brain notes in goal order (Spelunking first) closing gaps.md + the checklist.
Goal (Zack OK 2026-11-21): POW 900K done; now Spelunking caves Chucklemire -> Lunarheim -> Bizarrio (spec in pending_changes). Owners: Emperor = Autiszemo (best fighter). Pending in-game checks: Kitchen Dream-mare next ~9.36e26, Blackheart next max raise ~36,626 Purple Screws, Bummo Bag price.
