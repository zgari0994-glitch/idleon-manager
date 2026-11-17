# Change plan (from the 2026-11-16 test session)

Source of every item: plans/pending_changes.md (approved line by line during the session).
Built as one design, in 4 phases. Each phase ends with a check-in with Zack before the next starts.

## Phase 1: Fix the card engine (code only, no new research)
Goal: every card shows everything we already have data for, in the agreed format.
1. Card layout per character, fixed order:
   1. Most important move
   2. Quick wins (ready now / cheap)
   3. Active tasks (separate line)
   4. AFK spot + why (separate line, never an active spot)
   5. Every sub-system of every job, each with "current -> goal (next tier)" or a next step. Nothing silent.
   6. Locked features: what unlocks them + where that unlock sits in a plan.
   7. That character's AutoReview Library talents: High / Medium / Low, Combat and Skilling.
   8. Bags missing (for the bag-sweep pull).
2. Fix job-section matching bugs (ES statue rows on Autistomatic, non-ore rows under ore prints, W7 mini systems skipped because untiered, Hole caverns skipped).
3. Pull untiered AutoReview sections into cards: W7 minis, all 15 caverns + villagers, Gaming snail, Atom Collider costs vs atoms owned, Coral Reef/Dancing Coral/Coral Kid, Gallery, Cape Vine, Storage.
4. Job changes: world bosses + minibosses -> Autistastic (minibosses only at max stored spawns); Minehead -> Autistopher; worship totems -> Autistacular; ES statues -> one ES (Naut or Bish, Zack picks); monuments -> Autistachio after Divinity; Emperor unassigned until researched; Spelunking -> an RG once unlocked.
5. Account alerts block (not tied to a character): Equinox point available, Kilroy weekly (tracking live), Menagerie mission claimable, missables whitelist routed to owners (sailing -> Autisticles).
6. Money: coins per character + total + bank on the dashboard; every coin cost checked against what's affordable.
7. Materials: resources needed per upgrade vs owned (stamps, Salt Lick, prayers, schematics, bubbles); refinery salts + every 3D printer material tracked with run-out warnings (material foresight, Tangled Cords case).
8. Active-task list for play time, ranked by importance and time to finish, with a quick-wins mode. Includes: Cranium Cooking session (+ its 3 notes), statue farming with map per statue, Compass Nomadic push, achievement runs, bag sweep, Green Mushroom 1M, observation hunt, greenstack runs, Bandit Bob/Mimic seeds, overnight active slot (account-wide pick).
9. Daily loop on the dashboard: morning quick run (7am PC), workday active task, 3pm tablet lists. Two refreshes a day max, save age always shown.

## Phase 1b: System index
- model/system_index.yaml: every system -> Toolbox page(s) + tools -> raw-save fields -> AutoReview section -> creator topics. Cards and answers pull data through it first.

## Phase 2: Gap catcher + research (needs transcripts + ChatGPT Toolbox map)
Method (approved 2026-11-17, replaces tagging all 327 transcripts):
- tools/transcript_index.py = free keyword index (15,121 one-minute chunks tagged by system). One gap at a time: find top passages (newest Griffy first), read only those, capped.
- For depth: Claude writes ChatGPT a small work order (specific videos + timestamp ranges, full tagging spec). Never whole-corpus tagging.
- Every conclusion saved once in sources/findings/<system>.md (conclusion, timestamps, date). Cards read findings; one finding serves every character. Revisit only when a new video/patch touches the system.
- Research is triggered by need (gap register ranked by rinse, or what Zack is doing now), never "just in case".
Goal: replace every "gap" with sourced guidance. Order: Griffy -> Pulse/Nocturne -> idleon.wiki/Toolbox -> Discord. Each finding goes to Zack as a plan; approved -> card.
1. Gap register file listing every open gap from the session (W7 bubble unlock, Hole per-cavern guides, Gaming full system, Research grid path, Lab full map, Sneaking, Breeding full review, Worship/souls ramp, Trapping flow + auto-collect, Compass dust/perks, prints redo, card presets per role, talent top-10 per character + raising the 441 cap, money farming, Death Note with 2 DBs, Emperor/boss ownership, Minehead, reef, Gallery, capes, Tesseract/Arcanist, cauldron upgrades, cooking mastery, Clamworks, Advice Fish later, Legend Talents, Zenith fastest statue, Lunarheim/Spelunking POW, Coral Kid present, Fractal Island, artifact Maw).
2. Rebuild the rinse from creator verdict CSVs (recency-weighted, wider range), shown to Zack before it goes live.

## Phase 3: Growth tracking (approved)
1. Daily close at the 2nd refresh: cards + stats sheet saved.
2. Rates + ETAs per goal; bottleneck flags.
3. Weekly review report by code.
4. Measured-impact factor in the rinse, weights tuned weekly. Griffy sets direction.

## Phase 4: Cleanup
1. Update CLAUDE.md with the new rules (locked features, AFK vs active, no setups from my own read, sourced-or-labeled opinion, money awareness).
2. Republish the dashboard.

## Rules carried into every phase
- Every recommendation considers the raw data, and follows the Toolbox map protocol (sources/creators/idleon-toolbox-guide.md): evidence -> action -> benefit -> cost -> verify/stop.
- Digest first, build only on approval. No patch-on-patch.
- Guidance = sources. My opinion only when asked, always labeled.
- Never judge from Toolbox text what the game shows differently (passive cards lesson).
- Usage: all heavy lifting in code; never read big files whole.
