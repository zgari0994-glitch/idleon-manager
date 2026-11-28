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
