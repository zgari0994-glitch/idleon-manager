# IdleOn Manager (Zack's account, profile Autiszemo, 11 characters)

## How Zack works
- Digest first: explain understanding + plan, execute only on his approval. Design changes as a whole, no patch-on-patch.
- Zack Mode: short, direct, no em dashes, no filler. Lead with the one most important move, then an ordered list. Exact numbers.
- Guidance = what data and sources say. Own opinion only when he asks "what do you think". Never invent setups.
- Source priority: Griffy > PulseIdle = NocturneGaming (YouTube, endgame; Nocturne may be outdated) > Toolbox / idleon.wiki > 2023 Guide Sheet > Reddit / Discord > rest. Newest wins within a level. Flag fan sources.
- Pulse/Nocturne are NOT gap-fillers: they confirm Griffy, add context he missed, explain better, and deepen the what-to-do. Griffy sets direction; on conflict Griffy wins and the difference is flagged.
- Systems AutoReview doesn't rate (and new-world systems): guidance from Griffy (+ Pulse/Nocturne as above); where none covers it, report the gap to Zack, never fill it.
- Creator sources live in `sources/creators/<creator>/` (raw transcripts + verdict CSVs, committed by ChatGPT). Read with code, never whole.
- Weekly confirmations (e.g. Kilroy) live in `state/confirmed.json` keyed by week start; a weekly job shows on its cards from the weekly reset until Zack confirms it.
- Rinse goal: answer "what would Griffy do" for an account at Zack's stage.

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
6. `python3 model/dashboard.py` -> republish dashboard/index.html with publish_files (slug + version in dashboard/ARTIFACT; update version after).
7. Guide Zack one character at a time from that character's card only (finish every job before moving on). Never dump all 11.
8. Zack flags what's wrong / unwanted / missing -> after his OK, add to `sources/findings/gaps.md`. Morning run = gap review (findings, tagged rows, index; huge -> ChatGPT Lane A in queue.md).

## Never say "no data" (Zack rule)
Before a card says no data / gap, check the Toolbox map (sources/creators/idleon-toolbox-guide.md), the system index, the dashboard timers and the raw save. If Toolbox shows it, the card uses it.

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
- `tools/timers.py` (Toolbox dashboard timers + AFK spots) · `plans/w7_push.md` (Griffy W7 path + gaps)

## Status (2026-11-17)
Done: Phase 1 card engine v2 (fixed layout, all sub-systems, matching fixes, untiered sections, account block, ranked active list, daily loop), Phase 1b system index (105 systems), material ledger (+ AutoReview-targeted stamp needs), coin costs vs money (Upgrade Vault, Advice Fish, vendor; Toolbox formulas, tools/stamp_cost.py), Toolbox ready-timer routing, Hole 1-5 findings, ChatGPT queue (Lane A gaps / Lane B proactive), gap loop. Owners: maintenance systems on Autistopher, minigames + drop rate/storage/world progress account-wide, Emperor unassigned.
Next: 3pm refresh = first daily close (Phase 3 growth tracking), card run-through, morning gap reviews. Pending in-game checks: Kitchen Dream-mare next ~9.36e26, Blackheart next max raise ~36,626 Purple Screws, Bummo Bag price.
