# Repo layout, tagging, brother's account, status, keep-rules-current
Moved verbatim from CLAUDE.md on 2026-11-26 (usage cleanup). Rules here still apply; CLAUDE.md core wins on conflict (usage budget, thread split).

## Brother's account (Zack 2026-11-19)
- `accounts/brother/` = his separate dashboard (IdleOnLech, 10 chars), fully automatic via his upload page + GitHub Action + Cloudflare Pages (no Claude usage). See accounts/brother/README.md. Never mix his data into Zack's snapshots/plans; Zack's own flow below is unchanged.

## Layout
- `tools/` decode_pull.py, run_ar.py (AutoReview code -> structured JSON), snapshot.sh
- `snapshots/` one folder per game save: raw.json.gz, review.json.gz, chars.json (per-character facts), systems.json.gz (105 parsed systems), meta.json
- `model/` jobs.yaml (layer 2, curated), build_map.py -> map.md (layer 1 facts + layer 2 jobs + tiers)
- `model/` also: mechanics.py -> mechanics.md/json (rule-changers, packs, achievements, trophies/capes), plan.py (daily cards), dashboard.py
- `plans/` per-save daily plans; `dashboard/` page + ARTIFACT pointer
- `rinse/` rinse.py = Thigh Gap v2 formula (ChatGPT build) with Griffy recurrence from griffy_topics.yaml; latest.json
- `model/acquire.py` -> acquire.md/json (missing trophies/capes/nametags/hats + open achievements, wiki sources, in-game vs paid vs event)
- `model/system_index.yaml` (system -> Toolbox page -> AutoReview -> sources -> owners; built by tools/build_system_index.py) · `model/ledger.py` (materials) · `sources/findings/` (saved research + queue.md for ChatGPT)
- Tagging DONE 2026-11-19: all transcripts tagged (ChatGPT 24, Claude Sonnet 5.5 Batch API 291 via handoff/run_tags.py, ~$14.77). ChatGPT tagging retired. New videos later: make_packets.py -> run_tags.py pilot/submit/collect on Zack's PC -> merge_tags.py.
- Tagging pipeline: `tools/make_packets.py` (trimmed packets + ORDER.csv) -> ChatGPT per `handoff/TAGGER.md` writes `handoff/tags_out/` -> on "check tags" run `python3 tools/merge_tags.py` (validates, writes full CSVs to sources/creators/<c>/tags/), commit.
- `tools/timers.py` (Toolbox dashboard timers + AFK spots) · `plans/w7_push.md` (Griffy W7 path + gaps)

## Keep rules current (Zack 2026-11-21)
When a rule changes: update this file, Project memory (`/projects/.../areas/idleon.md`, standing rules only) and give Zack the Project text to paste, in the same turn. Project docs are legacy reference (see claude/00-READ-FIRST.md); never act on them over the repo.

## Status (2026-11-21)
Done: card engine v3 (cards2.py), 66 system planners, system index, ledger, coins, guidance layer, tagging, brother's dashboard.
Building now (in order): Report -> reserves -> decision layer -> cards from decisions -> fill brain notes in goal order (Spelunking first) closing gaps.md + the checklist.
Goal (Zack OK 2026-11-21): POW 900K done; now Spelunking caves Chucklemire -> Lunarheim -> Bizarrio (spec in pending_changes). Owners: Emperor = Autistocat (Zack 2026-11-25, creators: AC is the Emperor farmer). Pending in-game checks: Kitchen Dream-mare next ~9.36e26, Blackheart next max raise ~36,626 Purple Screws, Bummo Bag price.
