# ChatGPT work queue

**2026-11-17: replaced by the packet run.** ChatGPT follows `handoff/TAGGER.md` over `handoff/packets/` (ORDER.csv: Lane A AFK video first, then tag_priority tiers 1-6). Lane B is dropped (everything gets tagged in order). New Lane A gaps: Claude moves those videos to the front by re-running tools/make_packets.py with LANE_A updated. Below is history.

Lane A (gap orders from cards) always goes first. Lane B (proactive, thinnest systems first) runs whenever Lane A is empty. One order = 1 system, max 3 videos, listed ranges only. Long ranges (streams): read only the keyword-hit minutes +-2 min (run `python3 tools/transcript_index.py find <system> --creator X` to get them), not the whole span. Bias to systems on Zack's active cards. Output: tags CSV per tagging_spec.md.

## Lane A: gap orders
1. hole | Pulse 0DX3KPt_VlM + glvAam8Mol8 | monument hour targets (Bravery/Justice/Wisdom): exact numbers + reasoning
2. hole | Griffy + Pulse, any Well section | bucket split between rock layer and sediments
3. afk_spots | Griffy ypb7kpQov30 00:00-00:10 + streams | best AFK map for Siege Breaker (forge) and Arcane Cultist

## Lane B: proactive (tagged rows now -> order)
- clam_work (0 rows): pulseidle wL0qRyP7GGU (2026-10-16) 00:14-00:17 [3 hits]; pulseidle DiimMepKdIs (2026-10-19) 00:13-00:16 [3 hits]; griffybit KZH_HUZf8rc (2025-12-27) 00:02-01:25 [2 hits]
- equinox (0 rows): griffybit UGgnjvIRdms (2026-03-10) 00:10-00:34 [8 hits]; griffybit kD7KZ5zX6Ss (2026-04-23) 00:20-00:25 [3 hits]; griffybit 8C9vFwK6bUg (2026-07-19) 00:09-00:20 [3 hits]
- gallery (0 rows): griffybit dliS5ZjijlA (2026-01-29) 01:02-04:57 [6 hits]; pulseidle 0xjp2t-iukY (2026-09-08) 00:02-00:21 [5 hits]; griffybit JZVtqVNk5DI (2025-11-17) 00:29-01:19 [4 hits]
- killroy (0 rows): griffybit GFmPSIRIPX4 (2025-11-20) 00:30-00:31 [1 hits]; griffybit KZH_HUZf8rc (2025-12-27) 00:12-00:13 [1 hits]; griffybit dliS5ZjijlA (2026-01-29) 00:42-00:43 [1 hits]
- merits (0 rows): pulseidle pj3l9w3oOp8 (2026-11-07) 00:03-00:38 [9 hits]; griffybit Ks4F_wrmVRA (2026-02-14) 00:00-00:22 [5 hits]; griffybit 8C9vFwK6bUg (2026-07-19) 00:13-00:40 [5 hits]
- salt_lick (0 rows): griffybit GFmPSIRIPX4 (2025-11-20) 00:15-00:21 [3 hits]; griffybit jLXMoJ09P30 (2025-12-08) 00:50-00:52 [2 hits]; griffybit kD7KZ5zX6Ss (2026-04-23) 00:35-00:36 [1 hits]
- w7_push (0 rows): griffybit dliS5ZjijlA (2026-01-29) 00:15-06:07 [13 hits]; griffybit GIs09k2bhkY (2025-11-10) 00:00-00:22 [10 hits]; griffybit KHuU392EW-4 (2026-09-21) 00:00-01:23 [8 hits]
- advice_fish (1 rows): pulseidle NEQ-qRLEfC4 (2026-10-16) 00:04-00:05 [1 hits]
- arcade (1 rows): griffybit 8C9vFwK6bUg (2026-07-19) 00:04-00:28 [5 hits]; griffybit kD7KZ5zX6Ss (2026-04-23) 00:12-00:15 [2 hits]; pulseidle oEq-mndoO64 (2026-08-29) 00:00-00:08 [2 hits]
- atom_collider (1 rows): griffybit kD7KZ5zX6Ss (2026-04-23) 00:17-00:57 [4 hits]; griffybit ypb7kpQov30 (2026-08-03) 00:07-00:16 [4 hits]; griffybit dliS5ZjijlA (2026-01-29) 02:19-05:10 [3 hits]
- cape_vine (1 rows): griffybit dliS5ZjijlA (2026-01-29) 04:03-08:06 [7 hits]; pulseidle 7EkdEAkWYng (2026-11-01) 00:00-00:08 [7 hits]; pulseidle UcgdzLvBLMc (2026-11-01) 00:00-00:04 [4 hits]
- coral_reef (1 rows): pulseidle NlppEKJNCZM (2026-10-14) 00:01-00:26 [9 hits]; pulseidle pj3l9w3oOp8 (2026-11-07) 00:03-00:40 [9 hits]; griffybit Ks4F_wrmVRA (2026-02-14) 00:02-00:16 [7 hits]
- emperor (1 rows): griffybit kD7KZ5zX6Ss (2026-04-23) 00:01-00:57 [4 hits]; pulseidle 6JgdYbiEKus (2026-10-31) 00:01-00:26 [4 hits]; griffybit ypb7kpQov30 (2026-08-03) 00:00-00:06 [3 hits]
- sigils (1 rows): griffybit yjN-r2-Dy_w (2025-11-08) 00:00-00:51 [2 hits]; griffybit JZVtqVNk5DI (2025-11-17) 00:05-00:51 [2 hits]; griffybit Rr5KiEflTWE (2026-01-29) 00:09-00:11 [2 hits]
- the_button (1 rows): pulseidle oRTdKQdYJv0 (2026-09-02) 00:20-00:22 [2 hits]; griffybit Gkwf75q4NUk (2025-10-31) 01:02-01:03 [1 hits]; griffybit 8C9vFwK6bUg (2026-07-19) 00:34-00:35 [1 hits]
- upgrade_vault (1 rows): griffybit 4nwsLYYOjtI (2025-11-14) 00:01-00:50 [7 hits]; griffybit Gkwf75q4NUk (2025-10-31) 00:07-00:47 [6 hits]; griffybit N5yJ4-tZLbY (2026-10-04) 00:03-00:56 [5 hits]
- damage (2 rows): griffybit IEJEvG1RkPM (2026-04-16) 00:00-01:11 [36 hits]; griffybit ycZCe2N0Uzc (2026-05-03) 00:00-00:57 [35 hits]; pulseidle DWEVaYI4iWA (2026-09-20) 00:01-00:54 [29 hits]
- jelly_operator (2 rows): pulseidle NlppEKJNCZM (2026-10-14) 00:06-00:24 [5 hits]; pulseidle 1r5m4CvmZ-0 (2026-09-18) 00:00-00:05 [4 hits]; pulseidle s5M5dcdwXc4 (2026-09-22) 00:00-00:09 [4 hits]
- legend_talents (2 rows): pulseidle UrAwekQpjOE (2026-09-25) 00:00-00:50 [4 hits]; griffybit Ks4F_wrmVRA (2026-02-14) 00:04-00:13 [2 hits]; pulseidle DiimMepKdIs (2026-10-19) 00:23-00:25 [2 hits]
- money (2 rows): griffybit dliS5ZjijlA (2026-01-29) 00:20-08:53 [28 hits]; griffybit _maMoJLg6YE (2026-07-29) 00:08-05:22 [24 hits]; griffybit Gkwf75q4NUk (2025-10-31) 00:08-01:12 [14 hits]
- greenstacks (3 rows): griffybit dliS5ZjijlA (2026-01-29) 02:15-08:26 [4 hits]; pulseidle kbgSJRuGMRE (2026-10-23) 00:28-00:32 [4 hits]; griffybit UGgnjvIRdms (2026-03-10) 00:29-00:31 [2 hits]
- storage (3 rows): griffybit Gkwf75q4NUk (2025-10-31) 00:09-01:14 [17 hits]; griffybit dliS5ZjijlA (2026-01-29) 01:16-08:30 [16 hits]; griffybit IEJEvG1RkPM (2026-04-16) 00:04-00:25 [10 hits]
- tesseract (3 rows): griffybit fo2WwEKsty0 (2025-11-28) 00:34-00:37 [3 hits]; griffybit gPQrOK53BDI (2026-01-15) 00:35-00:36 [1 hits]; griffybit ypb7kpQov30 (2026-08-03) 00:05-00:06 [1 hits]
- tome (3 rows): griffybit dliS5ZjijlA (2026-01-29) 01:03-03:20 [8 hits]; griffybit _maMoJLg6YE (2026-07-29) 01:07-02:37 [5 hits]; pulseidle ofuB4YV8gkM (2026-09-04) 00:00-00:20 [5 hits]
- talent_points (4 rows): griffybit Gkwf75q4NUk (2025-10-31) 00:08-00:58 [4 hits]; griffybit yjN-r2-Dy_w (2025-11-08) 00:22-00:36 [4 hits]; griffybit fo2WwEKsty0 (2025-11-28) 00:00-00:30 [4 hits]
- vials (4 rows): griffybit IEJEvG1RkPM (2026-04-16) 00:22-01:08 [9 hits]; griffybit KZH_HUZf8rc (2025-12-27) 00:06-00:55 [7 hits]; griffybit Sn28VbELcLw (2025-11-02) 00:01-01:06 [5 hits]
- zenith_market (4 rows): griffybit kD7KZ5zX6Ss (2026-04-23) 00:43-01:03 [4 hits]; griffybit Ks4F_wrmVRA (2026-02-14) 00:02-00:07 [2 hits]; pulseidle NEQ-qRLEfC4 (2026-10-16) 00:02-00:05 [2 hits]
- beanstalk (5 rows): griffybit 8C9vFwK6bUg (2026-07-19) 00:10-00:20 [3 hits]; griffybit ws-p4VWnZBQ (2025-11-11) 00:10-00:12 [2 hits]; griffybit Rr5KiEflTWE (2026-01-29) 00:01-00:18 [2 hits]
- class_exp (5 rows): pulseidle DWEVaYI4iWA (2026-09-20) 00:26-00:52 [6 hits]; pulseidle oRTdKQdYJv0 (2026-09-02) 00:02-00:38 [4 hits]; pulseidle Pxeb4iWgXr4 (2026-08-29) 00:01-00:13 [3 hits]
- glimbo (5 rows): griffybit 8C9vFwK6bUg (2026-07-19) 00:31-00:33 [2 hits]; griffybit _maMoJLg6YE (2026-07-29) 01:50-01:52 [2 hits]; pulseidle oRTdKQdYJv0 (2026-09-02) 00:28-00:30 [2 hits]
- cauldrons_liquids (6 rows): griffybit yCkTzQzeLn8 (2025-06-07) 00:00-00:07 [7 hits]; griffybit Sn28VbELcLw (2025-11-02) 00:00-01:05 [6 hits]; griffybit GFmPSIRIPX4 (2025-11-20) 00:21-01:00 [4 hits]
- refinery (6 rows): griffybit 0qlwJ8Qm-4w (2026-03-27) 00:06-01:01 [11 hits]; griffybit kD7KZ5zX6Ss (2026-04-23) 00:14-01:02 [10 hits]; griffybit JZVtqVNk5DI (2025-11-17) 00:05-01:04 [8 hits]
- achievements (7 rows): griffybit dliS5ZjijlA (2026-01-29) 00:55-08:46 [8 hits]; griffybit IEJEvG1RkPM (2026-04-16) 00:08-00:49 [7 hits]; griffybit Sn28VbELcLw (2025-11-02) 00:11-01:01 [4 hits]
- research (7 rows): pulseidle oRTdKQdYJv0 (2026-09-02) 00:00-00:40 [18 hits]; griffybit jvcxwsBebQI (2026-02-21) 00:00-00:10 [10 hits]; pulseidle _wJJ9siUFLk (2026-10-31) 00:18-00:46 [7 hits]
- slab (7 rows): griffybit lYZrYL3VZOY (2026-06-17) 00:01-00:21 [6 hits]; griffybit Rh_Oj08oB8A (2026-01-08) 00:47-00:50 [3 hits]; griffybit Gkwf75q4NUk (2025-10-31) 00:02-01:09 [2 hits]
- buildings (8 rows): griffybit N5yJ4-tZLbY (2026-10-04) 00:06-01:09 [11 hits]; griffybit jLXMoJ09P30 (2025-12-08) 00:17-01:02 [10 hits]; griffybit KZH_HUZf8rc (2025-12-27) 00:06-01:26 [10 hits]
- library (9 rows): griffybit 4nwsLYYOjtI (2025-11-14) 00:23-00:28 [4 hits]; griffybit RnnRamcdjQ0 (2026-07-26) 00:06-00:17 [4 hits]; griffybit m2eio1vBHvE (2025-12-15) 00:41-01:14 [3 hits]
- death_note (10 rows): griffybit dliS5ZjijlA (2026-01-29) 00:45-08:06 [19 hits]; griffybit _maMoJLg6YE (2026-07-29) 00:18-05:40 [13 hits]; griffybit N5yJ4-tZLbY (2026-10-04) 00:07-01:13 [8 hits]
- drop_rate (10 rows): griffybit dliS5ZjijlA (2026-01-29) 00:11-05:45 [17 hits]; griffybit 8C9vFwK6bUg (2026-07-19) 00:02-00:38 [15 hits]; pulseidle ofuB4YV8gkM (2026-09-04) 00:00-00:13 [11 hits]
- prayers (10 rows): griffybit gPQrOK53BDI (2026-01-15) 00:23-00:57 [10 hits]; griffybit dliS5ZjijlA (2026-01-29) 01:25-09:03 [10 hits]; griffybit UeKUd2tJM2o (2025-11-24) 00:29-00:59 [5 hits]
- gem_shop (12 rows): griffybit dliS5ZjijlA (2026-01-29) 00:39-03:28 [16 hits]; griffybit Gkwf75q4NUk (2025-10-31) 00:00-01:22 [12 hits]; griffybit Sn28VbELcLw (2025-11-02) 00:03-01:15 [12 hits]
- bubbles (14 rows): griffybit Sn28VbELcLw (2025-11-02) 00:00-01:04 [14 hits]; griffybit dliS5ZjijlA (2026-01-29) 01:28-07:18 [14 hits]; griffybit KHuU392EW-4 (2026-09-21) 00:10-01:09 [13 hits]
- statues (15 rows): pulseidle 6JgdYbiEKus (2026-10-31) 00:00-00:27 [9 hits]; pulseidle loL-bMjqkKY (2026-08-29) 00:06-00:24 [8 hits]; pulseidle DWEVaYI4iWA (2026-09-20) 00:09-00:52 [7 hits]
- menagerie (18 rows): pulseidle DiimMepKdIs (2026-10-19) 00:00-00:38 [12 hits]; pulseidle wL0qRyP7GGU (2026-10-16) 00:00-00:23 [10 hits]; pulseidle NlppEKJNCZM (2026-10-14) 00:00-00:16 [8 hits]
- rift (18 rows): griffybit kD7KZ5zX6Ss (2026-04-23) 00:05-00:42 [6 hits]; griffybit 8C9vFwK6bUg (2026-07-19) 00:01-00:36 [5 hits]; griffybit KZH_HUZf8rc (2025-12-27) 00:04-01:25 [4 hits]
- divinity (23 rows): griffybit dliS5ZjijlA (2026-01-29) 00:04-09:00 [44 hits]; griffybit Rh_Oj08oB8A (2026-01-08) 00:16-00:53 [21 hits]; griffybit KHuU392EW-4 (2026-09-21) 00:00-01:17 [17 hits]
- cards (24 rows): griffybit m2eio1vBHvE (2025-12-15) 00:02-01:26 [14 hits]; griffybit dliS5ZjijlA (2026-01-29) 00:46-08:17 [12 hits]; griffybit JZVtqVNk5DI (2025-11-17) 00:07-01:22 [8 hits]
- grimoire (24 rows): griffybit N5yJ4-tZLbY (2026-10-04) 00:44-01:06 [13 hits]; griffybit dliS5ZjijlA (2026-01-29) 00:50-08:48 [6 hits]; griffybit Gkwf75q4NUk (2025-10-31) 01:03-01:14 [3 hits]
- sailing (24 rows): griffybit Rh_Oj08oB8A (2026-01-08) 00:06-00:49 [14 hits]; griffybit KHuU392EW-4 (2026-09-21) 00:03-01:09 [14 hits]; pulseidle DiimMepKdIs (2026-10-19) 00:00-00:24 [7 hits]
- traps (25 rows): griffybit dliS5ZjijlA (2026-01-29) 00:39-08:35 [31 hits]; griffybit 0qlwJ8Qm-4w (2026-03-27) 00:06-01:04 [15 hits]; griffybit ycZCe2N0Uzc (2026-05-03) 00:08-00:25 [10 hits]
- worship (26 rows): griffybit gPQrOK53BDI (2026-01-15) 00:22-01:03 [15 hits]; griffybit 0qlwJ8Qm-4w (2026-03-27) 00:07-01:04 [13 hits]; griffybit GFmPSIRIPX4 (2025-11-20) 00:09-01:15 [8 hits]
- masterclass (29 rows): griffybit N5yJ4-tZLbY (2026-10-04) 00:00-01:16 [10 hits]; griffybit _maMoJLg6YE (2026-07-29) 01:49-05:41 [7 hits]; griffybit KHuU392EW-4 (2026-09-21) 00:06-00:45 [6 hits]
- cooking (30 rows): griffybit dliS5ZjijlA (2026-01-29) 01:00-08:41 [38 hits]; griffybit KZH_HUZf8rc (2025-12-27) 00:11-01:26 [14 hits]; griffybit m2eio1vBHvE (2025-12-15) 00:20-01:20 [11 hits]
- stamps (30 rows): griffybit IEJEvG1RkPM (2026-04-16) 00:03-00:41 [14 hits]; griffybit Gkwf75q4NUk (2025-10-31) 00:10-01:14 [10 hits]; griffybit m2eio1vBHvE (2025-12-15) 00:06-01:27 [9 hits]
- sneaking (31 rows): griffybit ycZCe2N0Uzc (2026-05-03) 00:35-00:53 [10 hits]; griffybit KHuU392EW-4 (2026-09-21) 00:23-00:39 [6 hits]; griffybit N5yJ4-tZLbY (2026-10-04) 00:30-01:12 [6 hits]
- gaming (32 rows): griffybit _maMoJLg6YE (2026-07-29) 01:09-05:45 [15 hits]; griffybit KHuU392EW-4 (2026-09-21) 00:10-01:14 [10 hits]; griffybit Rh_Oj08oB8A (2026-01-08) 00:16-00:47 [8 hits]
- printer (33 rows): griffybit JZVtqVNk5DI (2025-11-17) 00:04-01:26 [37 hits]; griffybit 0qlwJ8Qm-4w (2026-03-27) 00:01-01:01 [22 hits]; griffybit UGgnjvIRdms (2026-03-10) 00:01-01:04 [14 hits]
- breeding (36 rows): griffybit dliS5ZjijlA (2026-01-29) 00:39-08:35 [42 hits]; griffybit KZH_HUZf8rc (2025-12-27) 00:00-00:42 [16 hits]; griffybit 8C9vFwK6bUg (2026-07-19) 00:00-00:40 [13 hits]
- lab (38 rows): griffybit UeKUd2tJM2o (2025-11-24) 00:14-01:04 [13 hits]; griffybit KZH_HUZf8rc (2025-12-27) 00:06-01:15 [10 hits]; griffybit Rh_Oj08oB8A (2026-01-08) 00:05-00:47 [10 hits]

## Done
(move orders here with commit hash)
