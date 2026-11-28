# Task Score (Zack 2026-11-27, approved)
One score ranks every task across every system, so "what next" is not only Zack's call or AutoReview's next tier. Replaces nothing: it merges the inputs of `model/spend.py` (gain per share of balance) and `model/priority.py` (biggest need) into one ranking. Built 2026-11-27: `model/score.py`, weights in `model/score_weights.yaml` (all my read). K = 0.5, effort unit = 30 active minutes. Night watch compares value without effort (a full night either way). Candidates: jobs.yaml active_tasks (ids in brain/plans.yaml show as Zack's plan instead), data-driven tasks (Compass, Tesseract, Grimoire, Emperor, Spelunking), and one push task per owned need (priority.py, top 12).

## Rules that win over the score
- Law 1: the score never changes the main goal. Law 2: the score ranks, it never removes a duty from a card.
- A sourced order beats the score inside one system (docs/guidance.md). The score ranks across systems.

## Formula
`Raw = (Impact x Reach x Confidence x Urgency) / Effort`
`Score = 100 x Raw / (Raw + K)`; K is a fixed constant tuned once so scores mean the same thing every pull. Cards also show rank ("#2 of 140").

- **Impact** = % gain to the stat x stat weight. Weight 1.0 if the stat moves the main goal (now Spelunking: next lore boss), lower the further it sits from the goal chain. Weights start as "my read" and are listed in `model/score_weights.yaml`.
- **Reach** = 1 + 0.5 per system it unblocks; x2 if it is on the main goal's blocker chain.
- **Confidence** = source tier: Griffy 1.0, Pulse/Nocturne 0.9, Toolbox/wiki 0.8, 2023 Guide Sheet 0.6, my read 0.5, Reddit/Discord 0.4. Lowered by save age (stale data).
- **Urgency** = x1.5 for can't-miss dailies, a cap about to overflow, or a weekly reset; else x1.
- **Effort** = active minutes + 0.1 x wait hours + cost as share of balance (spend.py). Spending a protected reserve (reserves.yaml / protect.json) = large penalty.

## Guardrails
- Effort floor 1 minute and a minimum Impact, so trivial 5-second tasks with tiny gains don't flood the top.
- Calibration: each pull compares predicted gain vs actual (two saves, rates.py). Weights adjust; a task type that keeps missing gets flagged in the report.

## Examples (illustrative, not live numbers)
- 50K sticks into inventory as a greenstack, +5% chopping account-wide, Toolbox sourced: effort ~floor -> ~99.
- Sailing speed that unblocks 5 systems: high effort, Reach ~3.5 x2 on the chain -> ~97, top 3.

## Output
- Card: each Do line carries its score. Report: two account-wide top 10s, quick (under 10 min) and long (10+ min), same score, inputs shown (Zack 2026-11-27).

## Calibration 2026-11-28 (Phase C finish, save 20261128T0256): APPLIED (Zack "go" 2026-11-28; #1 = Fix B K 5, #2 = max of section/task unblocks)
Run: `python3 model/score.py --top`. 166 tasks, 48 score 90+, 13 score 95+.
1. Saturation (K 0.5): Score = 100 x Raw / (Raw + 0.5), so any Raw over ~5 lands at 91-100. A 1-minute task at the default impact 0.3 (Raw = 0.3 x 1 x 1 x 1 / 0.03 = 10) scores 95, above the main goal row (Matic Spelunking, Raw 1 x 5 x 0.8 x 1 / 2 = 2, score 80). Three-way tie at 97.8, four-way at 96.4. Fix A: rank each top 10 by `value` (Impact x Reach x Conf x Urgency, no effort) and keep Score as the cross-list number; Fix B: K 0.5 -> 5 (spreads 90-100 back out). No effort floor either way (Zack 2026-11-27).
2. Reach double count: "Push Lunarheim amber buys" reach 8.0 = (1 + 0.5 x (3 section unblocks + 3 task unblocks [cooking, super_talents, gallery])) x 2. The goal row itself gets 5.0. Same unblocks counted twice. Fix: reach = 1 + 0.5 x len(set(section unblocks + task unblocks)).
3. Check-in-game rows score like gains: "World Progress: Confirm current W7 map" (unowned, impact 0.3, reach 2.5 from 3 listed unblocks, conf 1.0 because the claim is Griffy) = 97.8, top of the quick list. A confirm/check has no gain until done. Fix: tasks starting "Confirm/Check ... in game" get impact x 0.5 and route to the system owner, not 'unowned'.
4. Unowned rows in the top 10 (World Progress, NPC Tokens Bellows quest 3): no card shows them, so they hold a top-10 slot for nothing. Fix: owner from data_map owners, else LIGHT (every character), else drop from top 10 with a 'no owner' flag.
5. Old sources at full confidence: Post Office Potion Package (Griffy 2025-06-07) conf 1.0 = same as a 2026-11 Griffy claim. Fix: conf x 0.9 per year of age, floor at the next tier down.
