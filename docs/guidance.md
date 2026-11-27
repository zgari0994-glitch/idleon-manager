# Guidance + sources: creators, sourced order, never say no data, buff sources, talent levels
Moved verbatim from CLAUDE.md on 2026-11-26 (usage cleanup). Rules here still apply; CLAUDE.md core wins on conflict (usage budget, thread split).

## How Zack works
- Nicknames (Zack 2026-11-25): Zemo, Cat, Ticles, Tastic, Bish, Tacular, Totle, Matic, Naut, Topher, Tachio. Never "Chachio" or "Chio".
- Shop buy orders (Zack 2026-11-21): every system shop shows a sourced buy order on its owner's card (next level, cost vs balance, source per line). Spelunking amber done (model/spelunking.py BUY_ORDER); rest in plans/pending_changes.md.
- Sourced order beats my math (Zack 2026-11-21, after Blooming Axe was ranked over Grand Martial): when a creator names a priority, it goes first. My own weights or gain-per-cost math only order items inside the same sourced tier, never above a sourced pick.
- Digest first: explain understanding + plan, execute only on his approval. Design changes as a whole, no patch-on-patch.
- Zack Mode: short, direct, no em dashes, no filler. Lead with the one most important move, then an ordered list. Exact numbers.
- Guidance = what data and sources say. Own opinion only when he asks "what do you think". Never invent setups.
- Source priority: Griffy > PulseIdle = NocturneGaming (YouTube, endgame; Nocturne may be outdated) > Toolbox / idleon.wiki > 2023 Guide Sheet > Reddit / Discord > rest. Newest wins within a level. Flag fan sources.
- Creators (Zack 2026-11-19): Griffy first; Pulse + Nocturne are tier 1b. Where Griffy lacks advice, Pulse/Nocturne STAND IN as the guidance (say who it's from). Where Griffy covers it, they supplement (expand what he skipped) and confirm. On conflict the newest claim wins (Zack 2026-11-19) and the older one is shown as 'older:'. All accurate source data that adds to guidance is used. A system is a gap only when none of the three cover it.
- Systems AutoReview doesn't rate (and new-world systems): guidance from the creators as above; only where none of the three covers it, report the gap to Zack, never fill it.
- Creator sources live in `sources/creators/<creator>/` (raw transcripts + verdict CSVs, committed by ChatGPT). Read with code, never whole.
- Weekly confirmations (e.g. Kilroy) live in `state/confirmed.json` keyed by week start; a weekly job shows on its cards from the weekly reset until Zack confirms it.
- Rinse goal: answer "what would Griffy do" for an account at Zack's stage.

## Guidance layer (2026-11-19)
- `model/guidance.py` -> guidance.json (all creator tags, weighted creator/type/stage/recency). Feeds rinse push weight and plan.py card lines.
- Card line = Push (AutoReview What) + HOW/WHY (creator claim matched to that item, 2024-06+) ; CREATORS = top system-level how_to/priority/blocker/warning (no narration, 2024-06+).
- Prereqs: AR lock phrases + jobs.yaml `locked` route "Unblocks X" to the unlocking owner's card (top block) and "BLOCKED on Y's job" on the waiting card.

## Never say "no data" (Zack rule)
Before a card says no data / gap, check the Toolbox map (sources/creators/idleon-toolbox-guide.md), the system index, the dashboard timers and the raw save. If Toolbox shows it, the card uses it.

## Guiding before the knowledge base is done (Zack 2026-11-17)
Zack wants guidance now. Where Griffy/Pulse/Nocturne have nothing yet, guide from the data (save, Toolbox, AutoReview, game formulas) plus my best read, clearly labeled "my read". Sources upgrade it later; never stay silent just because creators haven't covered it.
Active time focus: push every attainable missing buff source (model/buffs.md). Dailies = bare minimum: check jobs, make sure nothing is wasting.

## Buff sources (Zack 2026-11-17)
Before explaining any level/stat (talent levels past book cap, plate levels, drop rate...), read its list in model/buffs.md. Never guess where levels come from.

## Talent levels (lesson 2026-11-17)
A talent's shown level = book level + bonus levels. Check the book level (max book is live data: `lookup.py library` -> bookLvRange.maxBookLv; 313 on 2026-11-27, was 299 on 2026-11-17, never hardcode it): Generational Gemstones 368 -> 372 = book 295 -> 299, so it IS a Library checkout.
