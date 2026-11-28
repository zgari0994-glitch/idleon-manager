# Pending changes (what's left; rewritten 2026-11-27 after the cleanup build)

Built items were removed. Built on 2026-11-27: model/syscheck.py (per-system "current -> goal" lines on every owner's card: Hole per cavern + villagers + study, Slab, Achievements, Lab jewels/chips, Cape Vine, Gallery, Menagerie missions + claim now + boosts + next unlock, Alchemy liquids/vials/sigils, Research observations/rolls/magnifiers/grid, Worship totems + skulls, Killroy, Refinery, Salt Lick, Death Note, Ballot + Meritocracy, Gem Shop paid flags, Beanstalk, Equinox challenges, Dungeons status, Cooking meals vs cap, Artifacts, Breedability heart 7, Stamps by group, ledger material watch) and model/growth.py (rates, ETAs, bottleneck flags, weekly review, talent diffs -> plans/growth_<save>.md). Old line numbers below are "(was L#)" from the 11-16..11-25 file.

## Left to build (data is in the parser)
- Alchemy: affordable levels per bubble vs materials; per-vial print-swap check to max it (was L10, L29).
- Systems with only a status line get a full standing goal per docs/planners.md, one system at a time as found (was L6, L295).
- Toolbox missables routed to owners (sailing -> Ticles) (was L13).
- Fractal Island and Coral Kid status lines (was L49, L58, L68, L161).
- Lab: per-character chip/jewel position check + jewel end goal (was L267, L273, L193).
- Trigger map: every threshold-driven system mapped, Divinity first (was L272).
- Rotation-aware weeks: hard-focus / opportunistic / hold slow tasks for a returning boost (was L258-260).
- Quest-only greenstacks on Tachio: per item, which quest, still open?, farm rate, days to 10M (was L302).
- Inventory + storage + carry capacity sweep, one active task on one character (was L171, L213).
- Construction: trimmed-slot priority list shared by Tastic and Matic (was L170).
- Talent books: perfect-checkout plan (2 talents/day/character), sub-200 bumps (was L148, L197).
- Every-character systems still unchecked: Lab position per character (was L267).
- Planner migration from toolbox/*.json page text to data.py, system by system (was L320).
- Zack's call (brain/plans.yaml is his): Elite Class Swap Token day plan for Naut (was L194); 1M Green Mushroom kills for the W2 weekly boss (was L214).

## Gaps: need creator sources (Griffy > Pulse = Nocturne > Toolbox/wiki), data + "my read" until then
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
- Toolbox website-only: Tesseract optimizer + tachyon per map, Spelunking optimizer, Lab chip/jewel shop rotation, ninja knowledge upgrade costs, building time left, atom particles/hr (now = change since last save) (was L323).
- Green Mushroom kills -> coins rate (was L176).
- Votes on phone pulls: a bare Copy raw data has no serverVars (carried from the last PC pull).
- Per-character drop rate (bag sweep: check Tastic vs Matic in game).
- No AutoReview section for Minehead or Worship.
- basketball, darts, event points shop are now mapped in data_map.yaml: confirm they parse before planning them.

## In-game checks (Zack)
- Fresh-save findings list from the Toolbox map (was L226).
- Trapper Drone: name + the 3 toggles (auto-grab after 24 hrs) (was L153).
- Compass Nomadic Path position vs level needed for Aluminium Atom (was L84).
