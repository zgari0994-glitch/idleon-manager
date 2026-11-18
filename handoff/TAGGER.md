# Tagger card (read once per chat; replaces tagging_spec.md for packets)

Job: tag every IdleOn claim in each packet. You are a tagger, not a judge. Max detail, front to back, no skimming, no summaries.

## Loop
1. `git pull --rebase`. Next packet = lowest-numbered file in `handoff/packets/` with no matching `handoff/tags_out/<video_id>.csv`.
2. Read that packet once. Write `handoff/tags_out/<video_id>.csv`.
3. `git add handoff/tags_out && git commit -m "tags: <video_id>" && git pull --rebase && git push`. One commit per video.
4. Go to 1. Never stop to ask, report or summarize. Keep chat output to one line per video: `<n> <video_id> <rows> rows`.
5. Don't validate, re-read, write drafts, write scripts or edit anything else. Claude validates later.

## CSV (header exactly)
`t_start,t_end,system,subsystem,class,claim_type,stage,numbers,statement,explicit,confidence`

- t_start / t_end: copy the `[HH:MM:SS]` of the paragraph where the claim starts / ends. Never compute times.
- system: slug from the list. Claim on 2+ systems = one row, slugs joined with `|` (e.g. `cooking|farming`).
- subsystem: exact part (bubble, meal, cavern, talent, map...). class: from list or blank.
- claim_type: priority, blocker, target, threshold, how_to, setup, afk_spot, active_task, mechanic, skip, warning, comparison, meta_change, account_note, opinion
- stage: any, early, mid, late, endgame, w1..w7, early_w7, unknown
- numbers: every number in the claim as `name=value;name=value`.
- statement: paraphrase, 25 words max, what he said only. Quote fields with commas.
- explicit: yes/no. confidence: 3 clear, 2 some garble, 1 bad (mark unreadable names with `?`).
- One distinct claim per row. Don't merge, don't skip minor ones. No claims at all = one row, system `none`.
- `[skip ...]` lines are cut stream chatter: ignore them.

## Systems
characters dashboard anvil forge bribes stamps bubbles cauldrons_liquids vials sigils arcade islands killroy weekly_boss ballot printer refinery atom_collider equinox buildings death_note worship prayers traps salt_lick construction armor_smithy hat_rack library cooking breeding lab rift tome cape_vine sailing divinity gaming hole slab farming sneaking summoning beanstalk emperor spelunking research gallery legend_talents coral_reef zenith_market clam_work advice_fish minehead glimbo sushi jelly_operator menagerie the_button w7_push storage quests constellations upgrade_vault apocalypses grimoire compass tesseract royal_armory speedrun dungeons friends random_events event_shop guild tournament achievements tasks merits recipe_unlocks owl kangaroo bubba gem_shop pets bundles statues cards drop_rate money class_exp damage talent_points greenstacks masterclass class_choice account_structure daily_routine general none

## Classes
beginner journeyman maestro voidwalker warrior barbarian blood_berserker death_bringer squire divine_knight royal_guardian archer bowman siege_breaker hunter beast_master wind_walker mage wizard elemental_sorcerer shaman bubonic_conjuror arcane_cultist
