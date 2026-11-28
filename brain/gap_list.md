# GOAL gap list (Phase C finish 2026-11-28, save 20261128T0256)

Every GOAL block with coverage partial/none/my_read, a my_read rung, or a logged `# gap:`. Skipped: guild_bonuses (Zack: guild ignored); cog_board (Zack: Toolbox optimizer, no creator guidance needed); class_kill_talents (merged).
Plan kinds: **Data** = map it (raw save / parser), **Source** = find a creator claim, **Audit** = partial with no gap logged, **Zack decides**.

| # | system | cov | my_read rungs | owner | gap | plan |
|---|---|---|---|---|---|---|
| 1 | achievements | partial | 0 | stopher | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 2 | advice_fish | sourced | 2 | sticles | (no gap logged) | Source: find Griffy/Pulse, else Zack decides |
| 3 | alchemy_bubbles | partial | 0 | stocat | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 4 | alchemy_cauldrons | partial | 0 | stocat | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 5 | alchemy_vials | partial | 0 | stocat | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 6 | anvil | partial | 0 | every character (own anvil) | lookup.py has no 'anvil' system (data is characters[].anvil); tab level + item names not in parser. | Data: map from raw save, else in-game check |
| 7 | armor_sets | partial | 0 | stastic | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 8 | basketball | none | 1 | UNASSIGNED | no creator coverage; spendable points (vs 317 total) not in parser; data_map basketball path null (real: highs | Data: map from raw save, else in-game check; Source: find Griffy/Pulse, else Zack decides |
| 9 | bribes | sourced | 0 | stopher | Flail unlock condition not in parser or creator rows. | Data: map from raw save, else in-game check |
| 10 | bubba | my_read | 1 | stopher | lookup.py has no 'bubba' system; no creator upgrade order; Santa's Little Helper ownership unknown. | Data: map from raw save, else in-game check; Source: find Griffy/Pulse, else Zack decides |
| 11 | cape_vine | partial | 1 | stachio | (no gap logged) | Source: find Griffy/Pulse, else Zack decides |
| 12 | cards | partial | 0 | stronaut | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 13 | clam_work | partial | 1 | sticles | (no gap logged) | Source: find Griffy/Pulse, else Zack decides |
| 14 | colo_scores | partial | 0 | unassigned | ticket count not in parser; which golden foods drop where not in creator rows. | Data: map from raw save, else in-game check |
| 15 | companions | partial | 1 | unassigned | owned pets not in the pull at all (raw.data has no companion key; tournament matches/leaderboard empty, Gold d | Data: map from raw save, else in-game check; Source: find Griffy/Pulse, else Zack decides |
| 16 | cooking | partial | 0 | szemo | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 17 | coral_reef | partial | 1 | stachio | (no gap logged) | Source: find Griffy/Pulse, else Zack decides |
| 18 | crystal_spawn_chance | partial | 1 | unassigned | crystal chance breakdown per source not in parser. | Data: map from raw save, else in-game check; Source: find Griffy/Pulse, else Zack decides |
| 19 | dancing_coral | partial | 1 | stachio | (no gap logged) | Source: find Griffy/Pulse, else Zack decides |
| 20 | darts | partial | 0 | unassigned | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 21 | death_note | partial | 0 | szemo + stopher | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 22 | divinity | partial | 0 | stabish | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 23 | divinity_coral_kid | partial | 1 | stabish | (no gap logged) | Source: find Griffy/Pulse, else Zack decides |
| 24 | drop_rate | partial | 0 | UNASSIGNED | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 25 | equinox | partial | 0 | stopher | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 26 | event_points_shop | partial | 0 | stotle | no creator buy order beyond candles; stars earned + points balance not in parser; old objective 8->35 was an i | Data: map from raw save, else in-game check; Source: find Griffy/Pulse, else Zack decides |
| 27 | family_bonuses | partial | 0 | UNASSIGNED | family bonus formula per class not in model, so no "level X for +Y" ranking; Shaman/Beast Master/Bubonic have  | Data: map from raw save, else in-game check |
| 28 | farming | partial | 0 | szemo | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 29 | friend_bonuses | sourced | 0 | Zack | multiplier 1 (Piggy not owned?), Spearfish ownership not in parser; Griffy: bonuses cap at 12,000 account leve | Data: map from raw save, else in-game check |
| 30 | gallery | partial | 1 | stachio | (no gap logged) | Source: find Griffy/Pulse, else Zack decides |
| 31 | gaming | partial | 0 | stastic | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 32 | gemshop | partial | 0 | stotle | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 33 | hat_rack | partial | 0 | UNASSIGNED | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 34 | inventory | partial | 0 | stotle | carry bag tier per material not mapped (parser gives bag IDs, no names); slots 92-96 vs max unknown. | Data: map from raw save, else in-game check |
| 35 | jelly_operator | partial | 0 | sticles | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 36 | killroy | partial | 0 | class of the week: szemo (warrior), stacular (archer), stocat (mage) | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 37 | lab_bonuses | my_read | 1 | stocat | (no gap logged) | Source: find Griffy/Pulse, else Zack decides |
| 38 | lab_chips | partial | 0 | stocat | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 39 | lab_jewels | partial | 0 | stocat | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 40 | lab_mainframe | partial | 0 | stocat | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 41 | meals | partial | 1 | szemo | (no gap logged) | Source: find Griffy/Pulse, else Zack decides |
| 42 | menagerie | partial | 0 | sticles | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 43 | meritocracy | none | 0 | stotle | (no gap logged) | Source: find Griffy/Pulse, else Zack decides |
| 44 | merits | my_read | 0 | stronaut | (no gap logged) | Source: find Griffy/Pulse, else Zack decides |
| 45 | minehead | partial | 0 | sticles | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 46 | money | partial | 1 | stomatic | (no gap logged) | Source: find Griffy/Pulse, else Zack decides |
| 47 | npc_tokens | sourced | 0 | UNASSIGNED | parser lists quests per NPC but per-character completion was not read, so who's missing Bellows 3 / Djonnut 2  | Data: map from raw save, else in-game check |
| 48 | obols | sourced | 0 | EVERY CHARACTER (own obol slots, Zack 2026-11-28); system unowned | per-character obol slots read as 0/3 filled (parser path wrong, not real); Efaunt obol achievement postponed p | Audit: rungs without a dated creator source -> find one or mark my_read |
| 49 | palette | partial | 0 | stastic"   # Gaming owner (data_map gaming) | color unlock condition, active slot count and black star source not in parser; Pulse's 8 placements not in our | Data: map from raw save, else in-game check |
| 50 | poppy | partial | 0 | stopher"   # clickers job (Owl, Bubba, Poppy), Zack 2026-11-28 | pet Poppy drop source/odds unknown; kangaroo upgrade levels + fish balance not in lookup. | Data: map from raw save, else in-game check |
| 51 | prayers | partial | 1 | every_character | (no gap logged) | Source: find Griffy/Pulse, else Zack decides |
| 52 | printer | partial | 0 | every character (own prints) | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 53 | quests | partial | 0 | UNASSIGNED | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 54 | royal_armory | partial | 0 | stastic | names of RGres0-34 + no creator buy order | Data: names from Toolbox RG static data if it has them; Source: Griffy/Pulse RA video |
| 55 | sailing | partial | 0 | sticles | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 56 | saltlick | partial | 0 | stopher | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 57 | shrines | sourced | 0 | anyone"   # Zack 2026-11-28: anyone moves them | XP needed per level not in parser (only progress), Collective Agreement ownership unknown, map 150 name not ma | Data: map from raw save, else in-game check |
| 58 | snail_mail | partial | 0 | stastic"   # Gaming owner | Snail Mail balance not in parser (gaming.envelopes = 0.05, meaning unknown). Cap: none per Zack 2026-11-28 (pa | Data: map from raw save, else in-game check |
| 59 | spelunk | partial | 0 | stomatic | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 60 | stamps | partial | 0 | stopher | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 61 | statues | partial | 1 | sticles | (no gap logged) | Source: find Griffy/Pulse, else Zack decides |
| 62 | storage | partial | 0 | stotle | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 63 | summoning | partial | 0 | stocat | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 64 | talents | partial | 0 | every character (own talents, Zack 2026-11-28) | no per-talent "below cap" list in lookup; super_talents batch 8 flags Topher + Totle reset candidates. | Audit: rungs without a dated creator source -> find one or mark my_read |
| 65 | the_button | partial | 0 | sticles | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 66 | trapping | partial | 0 | stacular | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 67 | weekly_boss | sourced | 0 | stastic | done-state (d_*) not read by Toolbox | Zack decides: keep daily line (current) or mark done by hand each week |
| 68 | world_bosses | partial | 0 | stastic | no kill flag in save; Pulse 2026-09-08 newest | Zack decides: in-game daily check is fine as is |
| 69 | world_progress | partial | 0 | UNASSIGNED | (no gap logged) | Audit: rungs without a dated creator source -> find one or mark my_read |
| 70 | worship | partial | 3 | every_character | (no gap logged) | Source: find Griffy/Pulse, else Zack decides |
| 71 | zenith_market | partial | 1 | sticles | (no gap logged) | Source: find Griffy/Pulse, else Zack decides |
