---
name: brain-readme
description: How the brain, the Report, the reserve list and the decision layer fit together (agreed with Zack 2026-11-21)
---
# The brain (Obsidian-compatible: open this folder as a vault for the graph view)

## Flow every pull
1. **Data**: snapshot (save + AutoReview + Toolbox reads + timers) -> `snapshots/<save>/`.
2. **Report** (`model/report.py`, stored in `reports/<save>/`): every system in `brain/index.md`, every pull. Per system:
   state numbers, change since last save (rates), every candidate action with its gain, resources it would spend, blockers.
   Pull as much as possible; never trimmed. Kept per save so past reports can be compared.
3. **Decision layer** (`model/decide.py` -> `reports/<save>/decisions.md`): reads the Report + brain notes + AutoReview + rinse +
   priority + `brain/reserves.yaml`. For each system: DO today / HOLD (why) / NOTHING (why) / BLOCKED on X (whose card).
   Cross-checks: shared resources vs reservations, what a move unlocks or feeds (brain Links), how it helps the account goal.
   Flags: systems nothing checks, stale plans (> 7 days), checklist lines still open, two systems wanting one resource.
4. **Claude reviews `decisions.md`** (not raw data), fixes wrong calls, writes lessons back into the brain note.
5. **Cards** (from decisions only): per character in rotation order: Spend (open points: where + why) / Do (in-game steps) / Park.
   Standing lines on every card: grab anvil production, PO points if any. Then one Active plan block.

## Brain notes (`brain/systems/<slug>.md`)
AUTO block = facts rebuilt by `tools/build_brain.py`. Everything else is curated and kept:
How it works (mechanics, multipliers, formulas, cited) · Links (feeds / fed by / uses / gated by) · Creator rule of thumb ·
Plan (now / next / stop point / waiting on) · Today (decision layer).
A note with an empty Plan counts as unplanned in `brain/index.md`.

## Reserves (`brain/reserves.yaml`)
Resource -> amount held, for what system, until when, why. Any spend line is checked against it first
(e.g. ladles held for Equinox, souls held for construction).

## Rules that keep it honest
- Every system gets a line every day, even back-burnered ("nothing today because X").
- A rule change updates CLAUDE.md, Project memory and the Project text in the same turn.
- Anything found unchecked gets said out loud and a note/planner gets built.
- `brain/checklist_2026-11-21.md` is the acceptance test; lines close only with a sourced answer, "my read", or a gap with a plan.
