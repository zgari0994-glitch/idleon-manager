# IdleOn Manager (Zack, profile Autiszemo, 11 characters)
Lean core, re-read every call: keep it small. Details live in docs/ and are opened ONLY when a task needs them (index at the bottom).

## LAWS (Zack 2026-11-21, override everything below)
1. Goal chain: the main account goal is the biggest account need from the review each pull (model/goalpick.py on model/priority.py), with a measurable target. If another system blocks it, that system's owner makes the unblock their character goal and hard-focuses it, and every task in that system aims at the unblock. The goal stays until its target is hit OR another need outranks it on 2 pulls in a row; then the card asks "switch goal?" and Zack confirms (`tools/afk_pin.py goal <section>`). Spelunking's target is the next lore boss, not every boss (Zack 2026-11-27).
2. Focus never means neglect: a character hard-focusing a blocker STILL does every other system and duty they own, every day. Example: if Construction is the blocker, Autistastic hard-focuses Construction AND still checks his Royal Guardian duties, Gaming and everything else on his card. Nothing drops off a card because something else is the focus.
3. Side goals (Zack 2026-11-27): a character may leave the main goal for a short personal goal that also helps the account (e.g. Ticles' bars), finish it fast, then go straight back. Anyone with no active personal goal works the main goal (now Spelunking). Death Bringers: Zemo bursts small Death Note kills then pushes bones; Topher grinds the big remaining kills.

## Card jobs (Zack 2026-11-27): from the model, never hand-written
- Order on every card: Zack's plan (brain/plans.yaml, his plans ONLY, dated, shown "Zack's plan") > Law 2 duties > masterclass duty (jobs.yaml masterclass:) > top-scored task in that character's systems (model/score.py). No personal goal -> main goal (Law 3).
- Masterclass: Tacular Compass, Zemo Grimoire (Topher bench only if needed), Cat Tesseract (+ Arcanist map push). Daily, check tier vs account; top-10 need = work it NOW alongside Spelunking. A Death Bringer Spelunks only once Grimoire is not a top-10 need. Compass/Tesseract active work = short daytime sessions.
- Overnight active slot = Cat only (frogs, Zack's plan). Night watch: an active-only task beating it 2 pulls in a row -> Cat's card lists the top 3 "reconsider?". Flag only.
- Live goals + challenge (Zack 2026-11-28, Phase C A+B): GOAL `now_path` (model/livepath.py spec) is read live every pull; no path = "not in save (last written: ...)", never None. Stall = live now unchanged N pulls (state/goal_now_history.json), so timers can't fake progress. TARGET HIT (live) advances the rung itself. Triggers (brain/triggers.yaml + GOAL block triggers) = when_path + op + value: fired = DO NOW on the row owner's card (or the `target:` system owner's), armed = next, no path = check in game. Objectives are recomputed each pull; Zack's plans stay but show "challenge?" when a sourced `challenge: {why, source}` or one of his tasks scores 15+ higher (score_weights challenge_margin). Equal scores tie-break by impact x reach.
- Dry run: `python3 model/score.py` (one line per character, writes nothing); `--top` = two account top 10s, quick (under 10 min) and long (10+ min), same score, inputs shown; also on cards4 under Account goal (`tools/card.py goal`). Zack 2026-11-27: no effort floor, quick wins stay high.

## Usage budget (the weekly limit is the #1 constraint)
- A normal question gets at most 2 tool calls. Call 1 is always `python3 tools/lookup.py <system> [terms]`. Call 2 only if needed (`--path` drill-in, or a second system).
- Anything bigger (builds, rewrites, multi-system reviews, research): ask Zack first with an estimated call count.
- Follow-ups: answer from what is already loaded. Do not re-run a lookup or re-read a file already in this chat.
- Never re-run the pipeline or pull unless Zack says "pull" or "after work". No scheduled tasks.
- Batch work into one big script per step. Never read big files whole (query with python/jq). Never dump raw browser data (gzip trick in docs/pipeline.md).
- When a chat gets long (about 15+ tool calls or 20+ turns), recommend a fresh thread.

## Threads
- **Q&A thread** (default, phone is fine, no browser): clone the repo (`--depth 1`), then lookup.py / `python3 tools/card.py <nickname>` / `snapshots/LATEST`. Card questions: card.py for ONLY the asked character (goal + their section); never read cards4 whole. Answer from the latest committed snapshot and say its age. Never pull here.
- **Phone pull** (default pull, no PC, no Claude usage, Zack 2026-11-27): Zack does Toolbox Account menu -> Copy raw data, pastes it at idleon-brother.pages.dev/zack.html (passcode) -> commits inbox/zack/raw.json.gz -> `.github/workflows/zack-pull.yml` runs snapshot + pipeline + cards4 and commits. Skips dashboard timers + artifact republish (browser only). A bare "Copy raw data" save has no serverVars: the workflow copies them from the newest PC-pull save and tags `_carried` in raw.json.gz (votes then show "[votes from save X]" on cards; a new week needs a PC pull or an in-game check). Toolbox's profile API refuses non-browser requests (403): never spoof headers. The repo is public: never commit secrets.
- **Pull thread** (fallback only, "pull" or "after work" when the phone pull can't): needs the built-in browser on Zack's PC (Toolbox signed in). If its tools are missing, the VERY FIRST tool call of the thread must be `enable__mcp__remote-devices__Claude_Browser` (ToolSearch first, nothing else before it: no clone, no memory read). Any other tool call first locks the thread out of the browser for good (seen 2026-11-27). The PC desktop app must be open and online. If that is unavailable or can't reach the PC, tell Zack: open this thread in the Claude desktop app on the PC and use + -> Add folder, then say "pull" again. Run Refresh below, then the pipeline (docs/pipeline.md), commit + push, republish the dashboard, then tell Zack to start a fresh Q&A thread.

## How Zack works
- Zack Mode: short, direct, no em dashes, no filler. Lead with the one most important move, then a short ordered list, exact numbers.
- Digest first: explain understanding + plan, execute only on his approval. Design changes as a whole, no patch-on-patch.
- Guide one character at a time from that character's card (`plans/cards4_<save>.md`), finish every job before moving on, never dump all 11. Library checkouts always show the account rank #1-55.
- Nicknames: Zemo, Cat, Ticles, Tastic, Bish, Tacular, Totle, Matic, Naut, Topher, Tachio. Never "Chachio" or "Chio".
- Source priority: Griffy > Pulse = Nocturne > Toolbox / idleon.wiki > 2023 Guide Sheet > Reddit / Discord > rest. Newest wins on conflict (show the older one as 'older:'). Flag fan sources. Say "my read" vs sourced. A sourced order beats my math. Never invent setups. No creator coverage -> data + "my read" + report the gap. Full rules: docs/guidance.md.
- Always say how old the game save is. Never accept stale data: find why it is stale and fix it.
- Own opinion only when he asks "what do you think".

## Data layer
- `model/data.py`: `load()` -> `.system(name)`, `.get('account.x.y')`, `.char(name)`, `.age_hours`. Reads Toolbox's own parser output `snapshots/<save>/tb_parsed.json.gz`; anything missing raises DataMissing. `model/data_map.yaml` = system -> parsed path (null = not in parser: use AutoReview / raw save and say so).
- Phase C D views (salt stall, trash shop list, obol meta watch, world bosses, guild from raw, compass dust, next lore boss POW): `model/phase_d.py`, docs/planners.md.
- `account._zack` (added by tools/tbparse/zack.test.mjs with Toolbox's own functions): `bubbleCosts` (Bubbles page math) and `alerts` (Toolbox dashboard alerts). Status lines: model/syscheck.py + model/syscheck2.py; triggers: brain/triggers.yaml.
- `tools/lookup.py <system> [terms]` = the one-shot answer tool, under ~4K tokens: save age + owner; DATA (levels, max, next cost vs balance OK/SHORT, LOCKED + exact unlock condition, creator tier grade per item); AutoReview open items; creator claims ranked with tier grades, date, video; findings; coverage; a final `TRUNCATED:` line saying what was cut. `--path a.b.c` drills in, `--full` lifts caps, `--terms "..."` free search. Answer from what it returned. Logs to state/lookups.log.

- Owners (Zack 2026-11-28): Killroy = Zemo warrior / Tacular archer / Cat mage (locked); Printer = every character own prints; Guild ignored. GOAL `check.helpers` = works it without owning, `check.split` = owners Zack decided (no 'Zack decides' tag).
- Weekly boss (Zack 2026-11-28, can't be skipped): `brain/weekly_boss.yaml` (current + next week) from the fan sheet "Weekly Boss Rotations" (Drive 1z1P2ouvYhe2pryWoF0kIQE7QichYpJt1GaPPos-e-aw). Daily line on the runner's card (cant_miss weekly_boss, Tastic = world bosses owner): "do the weekly boss today" every day with both the 5 Skulls and trophy runs until the boss changes (done-state not read). Refresh after the Thu 00:00 GMT reset, or when the card says stale: 1 Drive call (search_files title = 'Weekly Boss Rotations', snippetVerbosity MAX_ALLOWED) then `python3 tools/weekly_boss.py <saved dump>`. The Action can't read it.

## Refresh (pull thread only, about 3 calls)
1. Built-in browser: `preview_start` https://idleontoolbox.com/account/misc/general (signed-in session = live save).
2. Wait ~6s, javascript_tool: `const s=sessionStorage.getItem('rawJson'); const cs=new Blob([s]).stream().pipeThrough(new CompressionStream('gzip')); const buf=new Uint8Array(await new Response(cs).arrayBuffer()); let b=''; for(let i=0;i<buf.length;i+=32768) b+=String.fromCharCode.apply(null,buf.subarray(i,i+32768)); const b64=btoa(b); 'GZB64|'+b64.length+'|'+b64+'|END|'+'x'.repeat(60000)` -> saved to a /tmp/claude-tool-results file. Close the tab.
3. `tools/snapshot.sh <that file>` (decode, AutoReview, tb_parse, check_data) -> `snapshots/<save UTC>/` + `snapshots/LATEST`. Commit + push.
4. Timers (dashboard) + pipeline + cards + dashboard republish: docs/pipeline.md (play-session 1b onward).

## Keep rules current
When a rule changes: update this file or its docs/ file, Project memory (`/projects/.../areas/idleon.md`, standing rules only), and give Zack the Project description text to paste, same turn. When replacing anything, carry every item over and list what moved where. Project docs are legacy reference: search one section only when needed, never act on them over the repo.

## Docs index (open only when the task needs it)
- docs/pipeline.md: data layer v2 details, old usage rules, full Refresh, play-session flow, after-work pull steps (pipeline order, Active plan), retired bulk read.
- docs/guidance.md: creators rules (stand-in/supplement, newest wins), sourced order beats math, shop buy orders, weekly confirmations, rinse goal, guidance layer, never say "no data", guiding before the KB is done, buff sources (model/buffs.md), talent levels (book cap 299).
- docs/cards.md: AFK park lines v2 (model/afk.py), card wording, Library rank, every system on its card daily, GOAL LOGIC detail + current goal, can't-miss, locked = target, clocks, brain/report/decision layer (cards4, reserves, super talent resets).
- docs/planners.md: per-system GOAL standard (9 fields + template), per-system planner standard, the done list (owners per system), order, need outweighs math, Pinchy, planner migration to data.py.
- docs/layout.md: repo layout, tagging pipeline, brother's account (accounts/brother, never mix), status + pending in-game checks, keep-rules-current origin.
- docs/scoring.md: Task Score 0-100 (Impact x Reach x Confidence x Urgency / Effort), guardrails, calibration. Built 2026-11-27: model/score.py (weights model/score_weights.yaml), card job picker + night watch.
