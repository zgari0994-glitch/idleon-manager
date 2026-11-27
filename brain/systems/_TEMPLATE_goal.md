<!-- GOAL:START (per-system standard, docs/planners.md; read by build_brain + cards) -->
```yaml
role: blocker | feeder | independent      # vs main goal (Law 1 if blocker)
goal: ""                                   # end state + why, one sentence
coverage: sourced | partial | my_read | none
ladder:                                    # rungs, measurable
  - {tier: 1, target: "", source: "Griffy|Pulse|Nocturne|Toolbox|wiki|guide2023|my_read|reddit", date: ""}
objective: {rung: 1, now: null, target: null, eta_days: null}   # eta from model/rates.py
check: {cadence: daily | weekly, who: "", look_at: ""}          # becomes the card Do line (Law 2)
buffs:                                     # only for systems behind / needing a push; timed systems: one line
  - {source: "", world: 1, owned: false, now: null, next: null, owner: ""}
triggers:
  - {when: "", then: ""}
stall: {pulls_no_progress: 3, eta_over_days: 30}   # whichever first; reason routes per Law 1
tasks:                                     # each scored by docs/scoring.md
  - {do: "", stat: "", gain_pct: null, unblocks: [], source: "", active_min: null, wait_hr: null, cost: null, urgent: false}
```
<!-- GOAL:END -->
