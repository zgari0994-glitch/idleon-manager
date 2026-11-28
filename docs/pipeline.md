# Pipeline: data layer, refresh, play-session, after-work pull (old usage rules too)
Moved verbatim from CLAUDE.md on 2026-11-26 (usage cleanup). Rules here still apply; CLAUDE.md core wins on conflict (usage budget, thread split).

## Data layer v2 (Zack 2026-11-25, supersedes the 57-page Toolbox scrape)
- Pull = the save only (Refresh below, ~3 calls) + dashboard timers. `tools/snapshot.sh` now also runs `tools/tb_parse.sh` (updates the Idleon Toolbox source Morta1/IdleonToolbox and runs its own parser on the save -> `snapshots/<save>/tb_parsed.json.gz`, 108 sections + 11 characters, ~6s) and `tools/check_data.py` (coverage + sanity -> `snapshots/<save>/check.md`). AutoReview source is git-pulled too.
- Planners read game numbers ONLY through `model/data.py` (`load().system('sailing')`, `.get(path)`, `.char(name)`); missing/empty raises DataMissing. `model/data_map.yaml` = system -> parsed path (null = not in parser: AutoReview/raw save, say so).
- LOOKUP RULE: every game answer starts with `python3 tools/lookup.py <system> [terms]` (or `--terms "..."`): data + AutoReview + ranked creator claims + findings + coverage. Answer from what it returned; NO CREATOR COVERAGE -> data/wiki + "my read". Calls log to state/lookups.log (auditable).
- The old bulk page read (tools/tb_read_multi.js) is retired except for website-only pieces (upgrade optimizers, some dashboard alerts) found while migrating planners; list each one in plans/pending_changes.md.
- Toolbox page JSONs in snapshots/<save>/toolbox/ are legacy: planners move to tb_parsed system by system.

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
2. `python3 tools/build_system_index.py` (only after jobs.yaml/source changes) · `python3 model/ledger.py` (materials vs last save) · `python3 model/growth.py` (rates, ETAs, weekly review, talent diffs -> plans/growth_<save>.md; cache state/growth.json) · `python3 model/coins.py` (coin costs vs money) · `python3 model/buffs.py` (buff sources: every stat's sources owned/missing, routed to owners; run before plan.py) then `python3 model/mechanics.py` 3. `python3 rinse/rinse.py` 4. `python3 model/plan.py` 5. `python3 model/acquire.py` (wiki sources in sources/ are static; re-pull only after a game update)
6. `python3 model/cards2.py` (cards v3: Goal card + per character Dailies / Housekeeping / Goal part / Park; writes plans/cards_<save>.md, plans/cards.json, dashboard/cards.html) -> republish dashboard/cards.html as index.html with publish_files (slug + version in dashboard/ARTIFACT; update version after). Old dashboard.py is the fallback. cards3 adds model/syscheck.py lines (per-system current -> goal from data.py, owners from system_index.yaml) to every card's Systems block. cards2 pulls in: model/supertalents.py (sourced super picks, open points from save), model/extras.py (RG super hold + unlock trigger, cooking mastery conditions, research points, lab chip end-goal sets + jewels, Naut/AC roster rules, voting, talent ranking 1-55 stored as plans/talents_<save>.json), model/cardpresets.py, plans/trapping.md, plans/money_plan.md. Findings: sources/findings/{divinity_map,kill_milestones,reef_cages,goal_pow_900k}.md. Spec: plans/pending_changes.md 'Agreed spec'. Goal lives in cards2.GOAL (change only with Zack's OK).
6b. REQUIRED, Q&A threads read cards4: from the AutoReview folder (/home/claude/work/ar/mysite), `PYTHONPATH=.:<repo>/model python3 <repo>/model/report.py`, then `decide.py`, then `cards3.py` -> reports/<save>/ + plans/cards4_<save>.md. A pull is not done until cards4_<LATEST>.md exists and is pushed. Workspace setup: `pip install --break-system-packages rapidfuzz`.
7. Guide Zack one character at a time from that character's card only (finish every job before moving on). Never dump all 11.
8. Zack flags what's wrong / unwanted / missing -> after his OK, add to `sources/findings/gaps.md`. Morning run = gap review (findings, tagged rows, index; huge -> ChatGPT Lane A in queue.md).

## "After work" pull (Zack 2026-11-19) = the one full fresh pull of the day
Trigger: Zack says "after work" (he has cloud-saved, closed Steam, is on the tablet). Other refreshes only when he asks.
1. Refresh the save (steps above) + dashboard timers (play-session 1b).
2. (RETIRED 2026-11-25, replaced by tools/tb_parse.sh inside snapshot.sh) Bulk Toolbox read in ONE tab: preview_start any Toolbox page, javascript_tool with `const PAGES=<tools/tb_pages.json compact>;` + `tools/tb_read_multi.js` (hidden iframes, 5 at a time, ~8 min for 55 pages). Poll `window.__tbm ? 'DONE' : 'pending '+window.__tbm_done` (~40s waits). When DONE return `window.__tbm` (saved to a result file), close the tab, `python3 tools/tb_save_multi.py <file>`. Sailing is in the bulk list (saver writes toolbox/sail_detail.txt for model/sailing.py). Retry rule: a slow page waits longer, then reloads once. Pages that still fail keep yesterday's read (listed in toolbox/_from.txt): say so.
3. Pipeline (play-session step 2-6) -> cards + Active plan + dashboard republish. Tell Zack the save age.
4. Cards: dailies, parking, jobs per character. Then ONE block at the end: Active plan = Overnight on the PC (top 2, one long push for one character), Active play tonight (top 5, best first), Morning while at work (idle-friendly checks). Built by `model/active.py`, ranked by biggest need (`model/priority.py`) then job importance.
