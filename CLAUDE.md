# IdleOn Manager (Zack's account, profile Autiszemo, 11 characters)

## How Zack works
- Digest first: explain understanding + plan, execute only on his approval. Design changes as a whole, no patch-on-patch.
- Zack Mode: short, direct, no em dashes, no filler. Lead with the one most important move, then an ordered list. Exact numbers.
- Guidance = what data and sources say. Own opinion only when he asks "what do you think". Never invent setups.
- Source priority: Griffy > Toolbox / idleon.wiki > 2023 Guide Sheet > Reddit / Discord > rest. Newest wins within a level. Flag fan sources.

## Usage rules (the limit is the #1 constraint)
- No scheduled/hourly tasks. Pull data only on request or at the start of a play session.
- Never read big docs whole. Read `snapshots/$(cat snapshots/LATEST)/meta.json` first, then only the sections/characters the question needs (query with python/jq).
- Never dump raw browser data into context; always use the gzip+file trick below.
- Old Project docs (Index.md, KB, Daily-Rotation...) are legacy reference: search them for one section when needed, never load whole.

## Refresh (≈3 tool calls)
1. Built-in browser: `preview_start` https://idleontoolbox.com/account/misc/general (signed-in session = live save; no Upload needed).
2. javascript_tool (wait ~6s first):
   `const s=sessionStorage.getItem('rawJson'); const cs=new Blob([s]).stream().pipeThrough(new CompressionStream('gzip')); const buf=new Uint8Array(await new Response(cs).arrayBuffer()); let b=''; for(let i=0;i<buf.length;i+=32768) b+=String.fromCharCode.apply(null,buf.subarray(i,i+32768)); const b64=btoa(b); 'GZB64|'+b64.length+'|'+b64+'|END|'+'x'.repeat(60000)`
   The result is saved to a /tmp/claude-tool-results file. Close the tab right after.
3. `tools/snapshot.sh <that file>` -> decodes, runs AutoReview's own code (no website), writes `snapshots/<save UTC>/` and updates `snapshots/LATEST`. Commit + push.
- Public fallback (older, only as fresh as last Upload): profiles.idleontoolbox.workers.dev/api/profiles/?profile=Autiszemo (fetch from a Toolbox tab; workspace shell and WebFetch are blocked).

## Clocks
Game save = `data.TimeAway.GlobalTime` (UTC epoch). Store UTC, show Eastern. Always tell Zack the game-save age; data is only as fresh as the game's last cloud save.

## Layout
- `tools/` decode_pull.py, run_ar.py (AutoReview code -> structured JSON), snapshot.sh
- `snapshots/` one folder per game save: raw.json.gz, review.json.gz, meta.json
- Planned: `model/` account map (systems -> characters -> jobs -> goals), `rinse/` formula, `plans/` daily per-character plans, dashboard artifact.

## Status (2026-11-16)
Done: hourly task deleted, refresh route proven, AutoReview code validated (81 sections / 7,086 rows). Next: account map. Griffy transcripts tabled (6 picks: RnnRamcdjQ0, aUdMKlRf_v4, kD7KZ5zX6Ss, d3A2hYegsm4, x4_MMA9sNO4, R3YZ6D-EHHE).
