# Pending changes (what's left; rewritten 2026-11-27 after the cleanup build)

Built items were removed. Built on 2026-11-27: model/syscheck.py (per-system "current -> goal" lines on every owner's card: Hole per cavern + villagers + study, Slab, Achievements, Lab jewels/chips, Cape Vine, Gallery, Menagerie missions + claim now + boosts + next unlock, Alchemy liquids/vials/sigils, Research observations/rolls/magnifiers/grid, Worship totems + skulls, Killroy, Refinery, Salt Lick, Death Note, Ballot + Meritocracy, Gem Shop paid flags, Beanstalk, Equinox challenges, Dungeons status, Cooking meals vs cap, Artifacts, Breedability heart 7, Stamps by group, ledger material watch) and model/growth.py (rates, ETAs, bottleneck flags, weekly review, talent diffs -> plans/growth_<save>.md). Built 2026-11-28 (the old "Left to build" list): tools/tbparse/zack.test.mjs now adds account._zack (bubbleCosts with Toolbox's Bubbles page math; alerts = Toolbox's own dashboard alerts with default trackers). model/syscheck2.py (wired into syscheck.lines, so it lands on cards at the next pull): Toolbox missables/alerts routed to owners (character alerts on their own card, unowned to Tachio), affordable bubble levels per bubble, vial-to-max + print-swap check (Cat + Matic), Fractal Island + Coral Kid lines, Lab position per character + jewel end goal, trigger map (brain/triggers.yaml, Divinity first), rotation-aware weeks (Ballot + Meritocracy: hard-focus / opportunistic / hold, on Totle), quest-only greenstacks (Tachio), inventory + storage + carry cap sweep (one session on Tachio), Construction trimmed-slot list (Griffy order, Tastic + Matic), talent books (2 checkouts a day per character + sub-200 bumps). tools/draft_goals.py drafted GOAL blocks for the 65 systems that had none. Planner migration finished: sailing reads model/sail_consts.json, dead toolbox page readers removed. Old line numbers below are "(was L#)" from the 11-16..11-25 file.

## Left to build (data is in the parser)
- Zack's call (brain/plans.yaml is his): Elite Class Swap Token day plan for Naut (was L194); 1M Green Mushroom kills for the W2 weekly boss (was L214).
- Review + approve the 65 auto-drafted GOAL blocks (status: DRAFT, auto: true); 14 gaps listed in brain/goal_gaps.md.

## Gaps: need creator sources (Griffy > Pulse = Nocturne > Toolbox/wiki), data + "my read" until then
Checked 2026-11-28: none are truly missing. The claims DB (sources/creators/*/tags, 32.6K claims) has 40-1500 claims per item; thin ones are Research grid (40, mostly Pulse) and Minehead/Clamworks (83, mostly Pulse). The work left is synthesis into each system's GOAL ladder, not fetching.
- The Hole: per-cavern how it works / what to level / when to run / goal, opal split across villagers (was L122-138).
- Gaming plan: bits, upgrades, superbits order, Snail, Duper/Zuper (was L82, L300).
- Construction facelift: cogs, Polymerization, Flaggy, cog board vs meta, spare tower levels (was L299).
- Sneaking/Jade: method, BiS, floors, point spend, Pristine Charms, daily charm rolls (was L149, L152, L306).
- Breeding: shiny order after faster-shiny pets, fence plan, arena team past wave 120, spice (was L145, L305).
- Dungeons planner (Pulse keychains, party world bosses, Griffy DK/RG party class) (was L285).
- Minehead: what it is, upgrade plan (was L64, L205). Clamworks buy order (was L61-62).
- Buy orders: Menagerie boosts, sigil charge order, refinery priority, every other shop beyond Spelunking amber (was L313).
- Card presets per role + set-tier card farming (was L107, L192).
- Money plan: rinse-and-repeat DK/RG money, best item owned vs better to unlock (was L172, L177, L184, L281).
- Research grid path: node order, 1 vs 4, magnifier placement (was L157).
- Cooking: cap sources with thresholds, mastery choice method, best bone-farm spot (was L19-20).
- Alchemy: W7 bubble unlock condition, Luck vs rolling, cauldron upgrades, Summoning targets, Arcanist Form guidance (was L30-31).
- Sailing: artifact 3 -> 4 method, Fractal Island unlock path, print-burst session idea (was L46, L47, L49).
- Transcripts via Apify: compile Griffy/Pulse/Nocturne list, then fetch (was L216-219).

## Gaps: data the parser doesn't have
Closed 2026-11-28 (harness now runs Toolbox's own page functions into account._zack.web, status lines in model/syscheck2.py): per-character drop rate (getDropRate: Tastic 229 vs Matic 139, Tastic sweeps), atom particles/hr (calcTotals), building time left + real max levels (Buildings page math), Tesseract tachyon per map + upgrade optimizer, Spelunking POW/amber optimizer, Lab chip shop rotation (lab.currentRotation), ninja knowledge upgrade costs (getJadeUpgCost), event shop rotation (getEventShopRotation), basketball (hoops) + darts (highscores.minigameHighscores, mapped in data_map.yaml), Minehead + Worship covered by parser status lines instead of AutoReview.
- Green Mushroom kills -> coins: CLOSED 2026-11-28. Lab bonus Fungi Finger Pocketer = +2% monster cash per 1M Green Mushroom kills (linear, Toolbox parsers/world-4/lab.ts). 83.0B kills = +166,084% now; another 1M kills adds +2 points (~0.001% more cash), so it is not a reason to farm them (my math).
- Votes on phone pulls: known limit. A bare Copy raw data has no serverVars; the workflow carries them from the last PC pull and flags "[votes from save X]". A new vote week needs a PC pull or an in-game check.

## In-game checks (Zack)
- Fresh-save findings list from the Toolbox map (was L226).
- Trapper Drone: name + the 3 toggles (auto-grab after 24 hrs) (was L153).
- Compass Nomadic Path position vs level needed for Aluminium Atom (was L84).
