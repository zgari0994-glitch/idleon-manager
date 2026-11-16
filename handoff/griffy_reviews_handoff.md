# Handoff for ChatGPT: pull raw IdleOn creator transcripts into the repo

**UPDATE:** Zack runs `get_transcripts.py` on his PC and gives you `idleon_transcripts.zip`. It already holds the raw transcripts and `index.csv` per creator in the exact layout below (with extra columns `coverage` and `max_gap_s`). So skip Steps 1-2: unzip, commit `sources/creators/` as-is, then do Step 4 (verdict files) for every `type=review` video and any guide where they rank systems. Videos with status `failed` or `partial`: list them in your report.

You have access to the private GitHub repo `zgari0994-glitch/idleon-manager`. Your job is to fill `sources/creators/` with **raw, full transcripts** (YouTube captions, word for word, NOT summaries) plus a structured verdict file per review video. Another assistant reads these files with code, so exact formats matter more than prose.

## Hard rules
1. Only create or edit files inside `sources/creators/`. Never touch anything else in the repo.
2. Transcripts must be the full caption text with timestamps. No summarizing, no cleanup beyond removing duplicate lines. If you only have a summary, mark the video `status=failed`; don't save the summary.
3. Before pushing: `git pull --rebase`, then commit, then push to `main`. Commit in batches (e.g. 10 videos per commit), message `sources: <creator> transcripts batch N`.
4. Don't guess. If a field is unknown, leave it empty.

## Creators and scope (get as much as possible)
| Folder | Channel | What to take |
|---|---|---|
| `griffybit` | https://www.youtube.com/channel/UCt5WC8O9Jrb-UeNcI5T9BoQ (NOT @GriffyBit, that handle is a different channel) | Every IdleOn video and stream VOD. Mark type: review (account reviews, roasts, bingos), guide, playthrough, stream, short. |
| `pulseidle` | https://www.youtube.com/@PulseIdle | Every IdleOn video and stream VOD, same types |
| `nocturne` | https://www.youtube.com/@NocturneGamingOfficial | Every IdleOn video and stream VOD, same types |

Skip shorts under 2 minutes and non-IdleOn games.

## Step 1: list the videos
Use yt-dlp (install with `pip install yt-dlp`):
```
yt-dlp --flat-playlist --print "%(id)s\t%(upload_date)s\t%(duration)s\t%(title)s" "<channel URL>/videos" > list_videos.tsv
yt-dlp --flat-playlist --print "%(id)s\t%(upload_date)s\t%(duration)s\t%(title)s" "<channel URL>/streams" > list_streams.tsv
```
If `upload_date` comes back empty in flat mode, fill it per video with `yt-dlp --skip-download --print "%(upload_date)s" <url>`.

Known Griffy account reviews (make sure these are in): RnnRamcdjQ0, aUdMKlRf_v4, 1OKlpmFi1mI (stream VOD), kD7KZ5zX6Ss, GiVFMYM5ZCU, i0OYlSX5yVY, x4_MMA9sNO4, licmpceAPIc, R3YZ6D-EHHE, d3A2hYegsm4, rYUgBM6N4Os.

## Step 2: get the raw captions (programmatic)
Preferred, `youtube-transcript-api` (`pip install youtube-transcript-api`):
```python
from youtube_transcript_api import YouTubeTranscriptApi
t = YouTubeTranscriptApi().fetch(video_id, languages=["en"])
lines = [f"[{int(s.start//3600):02d}:{int(s.start%3600//60):02d}:{int(s.start%60):02d}] {s.text}" for s in t]
```
Fallback 1: `yt-dlp --skip-download --write-auto-subs --write-subs --sub-langs en --sub-format vtt -o "%(id)s" <url>`, then strip the VTT markup and repeated lines.
Fallback 2: open `https://youtubetotranscript.com/transcript?v=<id>` and copy the full transcript text.

Sanity check: full captions run roughly 120-180 words per minute of video. If a transcript is far below that, it's a partial or a summary: retry, or mark it `partial`.

## Step 3: save files
- Transcript: `sources/creators/<folder>/transcripts/<YYYY-MM-DD>_<video_id>.txt`
  First lines (header), then the timestamped captions:
  ```
  title: <title>
  url: https://www.youtube.com/watch?v=<id>
  date: <YYYY-MM-DD>
  duration_min: <n>
  type: review | guide | playthrough | stream
  captions: auto | manual
  ---
  [00:00:01] ...
  ```
- Index, one row per video: `sources/creators/<folder>/index.csv`
  Columns: `video_id,date,title,duration_min,type,captions,words,status` (status = ok | partial | failed)

## Step 4: verdict files (review-type videos, plus any guide where they rank systems)
`sources/creators/<folder>/verdicts/<YYYY-MM-DD>_<video_id>.csv`, one row per judgment the creator makes about a system. Only real judgments ("this is holding you back", "you need to", "max this", "this is fine", "don't bother"). Skip plain descriptions, jokes and numbers read aloud.

Columns:
- `video_id`, `date`, `creator`
- `stage`: the reviewed account's stage (e.g. "early W7", "W5 F2P")
- `system`: exactly one name from the list below, or `OTHER: <name>`
- `verdict`: `blocker` | `priority` | `upgrade` | `fine` | `skip`
- `strength`: 1 passing remark, 2 clear recommendation, 3 stressed or repeated (biggest, huge, most important)
- `detail`: max 25 words, what exactly to do (targets, items, levels if given)
- `relation_to_griffy` (Pulse/Nocturne only): `agrees` | `adds` | `contradicts` | `unknown`
- `timestamp`

System names (use exactly): Alchemy (Bubbles), Vials, Sigils, Stamps, Statues, Star Signs, Talents / Library, Obols, Post Office, Upgrade Vault, Owl, Bribes, Smithing / Forge, Mining, Chopping, Fishing, Catching, Trapping, Worship / Tower Defense, Prayers, Refinery / Salts, Salt Lick, Construction / Cogs / Shrines, 3D Printer / Sampling, Death Note, Atom Collider, Equinox, Breeding / Pets, Cooking / Meals, Lab / Chips / Jewels, Rift, Sailing / Artifacts, Divinity, Gaming, Slab, The Hole / Caverns, Farming, Sneaking / Jade, Summoning, Emperor, Islands, Greenstacks / Storage, Cards, Golden Food, Gear / Armor / Tools, Drop Rate, Crystal Mobs, Money, Gem Shop, Arcade, Kilroy, Ballots / Meritocracy, Merits / Task Board, Achievements, Party Dungeons, Colosseum, Weekly Boss, World Bosses, Companions, Combat / Damage / Accuracy, Candy / AFK, Tome, Grimoire (DB), Compass (WW), Tesseract (AC), Royal Guardian, Character Levels / Classes, Spelunking, Research, Coral Reef, Clam Work, Jelly Operator, The Button, Sushi Station, Zenith Market, Gallery / Trophies, Legend Talents, Luminous Menagerie, Advice Fish

## Order of work
1. Griffy account reviews (the 11 above + any others found), transcripts then verdicts.
2. Pulse, then Nocturne: reviews and endgame guides first, then the rest.
3. Remaining Griffy videos (transcripts only; verdicts only where he ranks systems).

## When done, reply to Zack with
- Counts per creator: videos found, transcripts ok / partial / failed, verdict files written.
- Any videos that failed, with the reason.
