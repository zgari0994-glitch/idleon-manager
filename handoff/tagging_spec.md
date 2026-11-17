# Tagging spec for ChatGPT: turn every transcript into tagged excerpts

Replaces "Step 4: verdict files" in griffy_reviews_handoff.md. Follow this exactly. Formats matter more than prose, because code reads your output.

## Your role
You are a **tagger, not a judge**. Do not decide what is important or what Zack should do. Record **what the creator says**, where he says it, and which system it belongs to. Claude decides importance later by combining your tags with Zack's live account data.

- Tag **every** transcript in `sources/creators/*/transcripts/` (all ~327), not only reviews. Every video gets a tag file.
- Tag **every distinct claim**. Do not merge two claims into one row. Do not skip a claim because it seems minor, obvious or outdated. Long videos produce many rows; that is expected. A 60-minute review should usually give 40+ rows.
- Do not summarize the video. Rows are excerpt pointers with a short paraphrase.
- Work through each transcript **front to back**. Do not sample or skim.

## Output files
One CSV per video: `sources/creators/<creator>/tags/<video_id>.csv` (UTF-8, comma separated, header row exactly as below, quote fields that contain commas).

```
video_id,creator,date,t_start,t_end,system,toolbox_page,subsystem,class,claim_type,stage,numbers,statement,explicit,confidence
```

If a transcript truly contains no IdleOn claims (off-topic chatter), write one row with `system=none` and `statement` saying why.

## Column rules
| Column | Rule |
|---|---|
| video_id, creator, date | From the transcript header. `creator` = folder name (griffybit / pulseidle / nocturne). `date` = header date or blank. |
| t_start, t_end | `HH:MM:SS` from the transcript lines where the claim starts and ends. Required. |
| system | One slug from the **System list** below. If a claim spans two systems, write two rows. |
| toolbox_page | The matching Toolbox page from the list (e.g. `world-4/cooking`). Blank only for `general`/`none`. |
| subsystem | Short free text naming the exact part: a bubble, upgrade, talent, meal, cavern, atom, stamp, card, map, etc. Example: `Kitchen Dream-mare`, `Cavern 15 Temple`, `Multorange`. |
| class | Class the claim is about, if any: beginner, journeyman, maestro, voidwalker, warrior, barbarian, blood_berserker, death_bringer, squire, divine_knight, royal_guardian, archer, bowman, siege_breaker, hunter, beast_master, wind_walker, mage, wizard, elemental_sorcerer, shaman, bubonic_conjuror, arcane_cultist. Blank if none. |
| claim_type | One of the **Claim types** below. |
| stage | Account stage the claim applies to, as the creator says or clearly implies: `any`, `early`, `mid`, `late`, `endgame`, or a world `w1`..`w7` (e.g. `w6`, `early_w7`). Use `unknown` if not stated. |
| numbers | Every number tied to the claim, as `name=value` pairs separated by `;`. Examples: `Grimoire Major Damage=3750 upgrades`, `bubble=Multorange;target=170`, `cap=90`. Blank if none. **Always capture numbers**: levels, thresholds, costs, rates, multipliers, wave counts, kill counts. |
| statement | The creator's claim paraphrased in **25 words or fewer**, in plain words. Say exactly what he said, no added advice. |
| explicit | `yes` if he says it outright, `no` if it is only implied by what he does on screen/says indirectly. |
| confidence | `3` captions clear, `2` some garbling, `1` badly garbled (flag names you could not read with `?`). |

## Claim types (use exactly these)
| claim_type | Use when the creator... |
|---|---|
| priority | ranks or orders things ("do X first", "this is S tier", "most important") |
| blocker | says something holds progress back ("you're stuck because", "this is gating you") |
| target | gives a level/amount to reach ("get it to 170", "aim for wave 50") |
| threshold | names an unlock point or breakpoint ("at 4,600 upgrades you get") |
| how_to | explains how to do or get something (location, steps, farming spot) |
| setup | names gear, cards, card presets, talents, talent presets, prayers, signs, obols, chips for a job |
| afk_spot | says where a character should AFK or farm, and for what |
| active_task | says something should be done actively (crystal farming, runs, minigames) |
| mechanic | explains how a system works (formula, caps, what stacks) |
| skip | says something is not worth doing / can be ignored / low value |
| warning | says something is a trap, a mistake, can brick/waste resources |
| comparison | compares two options ("A is better than B because") |
| meta_change | says advice changed with a patch / something is outdated now |
| account_note | a fact about the reviewed account (review videos only), e.g. "this player has 0 in Tesseract" |
| opinion | personal take with no reasoning, clearly labeled as preference |

## System list (system slug = toolbox_page)
Dashboard/characters: `characters` (talents, cards, presets, equipment, obols, prayers, signs, bubbles equipped, chips, bags, inventory, post office, anvil details), `dashboard`.

World 1: `anvil`=world-1/anvil, `forge`=world-1/forge, `bribes`=world-1/bribes, `stamps`=world-1/stamps.
World 2: `bubbles`=world-2/bubbles, `cauldrons_liquids`=world-2/cauldrons, `vials`=world-2/vials, `sigils`=world-2/sigils, `arcade`=world-2/arcade-shop, `islands`=world-2/islands, `killroy`=world-2/killroy, `weekly_boss`=world-2/weekly-bosses, `ballot`=world-2/vote-ballot.
World 3: `printer`=world-3/printer, `refinery`=world-3/refinery, `atom_collider`=world-3/atom-collider, `equinox`=world-3/equinox, `buildings`=world-3/buildings, `death_note`=world-3/death-note, `worship`=world-3/worship, `prayers`=world-3/prayers, `traps`=world-3/traps, `salt_lick`=world-3/salt-lick, `construction`=world-3/construction, `armor_smithy`=world-3/armor-smithy, `hat_rack`=world-3/hat-rack, `library`=account/misc/general.
World 4: `cooking`=world-4/cooking, `breeding`=world-4/breeding, `lab`=world-4/laboratory, `rift`=world-4/rift, `tome`=world-4/tome, `cape_vine`=world-4/cape-vine.
World 5: `sailing`=world-5/sailing, `divinity`=world-5/divinity, `gaming`=world-5/gaming, `hole`=world-5/hole (put the cavern/villager in `subsystem`), `slab`=world-5/slab.
World 6: `farming`=world-6/farming, `sneaking`=world-6/sneaking, `summoning`=world-6/summoning, `beanstalk`=world-6/beanstalk, `emperor`=world-6/emperor.
World 7: `spelunking`=world-7/spelunking, `research`=world-7/research, `gallery`=world-7/gallery, `legend_talents`=world-7/legend-talents, `coral_reef`=world-7/coral-reef (incl. dancing coral, coral kid), `zenith_market`=world-7/zenith-market, `clam_work`=world-7/clam-work, `advice_fish`=world-7/advice-fish, `minehead`=world-7/minehead, `glimbo`=world-7/glimbo, `sushi`=world-7/sushi-station, `jelly_operator`=world-7/jelly-operator, `menagerie`=world-7/menagerie, `the_button`=world-7/the-button, `w7_push`=(blank; pushing W7 maps/progression).
Account: `storage`=account/misc/storage, `quests`=account/misc/quests, `constellations`=account/misc/constellations, `upgrade_vault`=account/misc/upgrade-vault, `apocalypses`=account/class-specific/apocalypses (ZOW/CHOW/WOW), `grimoire`=account/class-specific/grimoire, `compass`=account/class-specific/compass, `tesseract`=account/class-specific/tesseract, `royal_armory`=account/class-specific/royal-armory, `speedrun`=account/class-specific/speedrun, `dungeons`=account/misc/dungeons, `friends`=account/misc/friends-stats, `random_events`=account/misc/random-events, `event_shop`=account/misc/event-shop, `guild`=account/misc/guild, `tournament`=account/misc/tournament, `achievements`=account/task-board/achievements, `tasks`=account/task-board/tasks, `merits`=account/task-board/merits, `recipe_unlocks`=account/task-board/unlocks, `owl`=account/clickers/owl, `kangaroo`=account/clickers/kangaroo, `bubba`=account/clickers/bubba, `gem_shop`=account/prem-currency/gem-shop, `pets`=account/prem-currency/pets, `bundles`=account/prem-currency/bundles.
Cross-cutting (toolbox_page blank unless one page clearly fits): `statues`, `cards` (card sets/drop/what to farm), `drop_rate`, `money`, `class_exp`, `damage`, `talent_points`, `greenstacks`, `masterclass` (unlocking/choosing master classes), `class_choice` (what class/elite to pick), `account_structure` (jobs per character, how many of each class), `daily_routine`, `general`, `none`.

If a claim fits no slug, use `general` and put the topic in `subsystem`. Never invent a new slug.

## Quality checks before each commit
1. Every transcript you processed has a tag file.
2. Every row has t_start, system, claim_type and statement filled.
3. Rows per video look reasonable for its length (roughly one row per 1-2 minutes of on-topic talk; reviews denser).
4. Any number spoken in a claim is in `numbers`.
5. No row merges two claims; no claim is skipped as "minor".

## Commits
- Only write inside `sources/creators/`. `git pull --rebase` before every push. Push to `main`.
- Commit per creator per ~20 videos: `sources: <creator> tags batch N`.
- Order: griffybit (newest first), then pulseidle (newest first), then nocturne.
- Final report message (in chat to Zack): videos tagged per creator, total rows per creator, any transcripts skipped and why.
