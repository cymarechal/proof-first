---
schema_version: 1
open_count: 2
waived_count: 0
fixed_count: 3
total_count: 5
last_updated: 2026-09-11T04:32:38.278Z
---

# Broken Windows Ledger

> Cross-phase defect register. With `workflow.windows_enforce` enabled, `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | 01 | unrun-verify | examples/deal-brief.md |  | T-01-04 name-collision web search for 4 invented parties + 5 invented persons not run (no live network access in this environment) — human must confirm via web search before repo goes public | fixed |  | 2026-09-10T06:46:57.541Z | 2026-09-10T11:02:49.274Z |
| 2 | 01 | unrun-verify | examples/deal-brief.md |  | D-07/P-05 boundary check (no sentence compares two real products or companies) reviewed by executor via re-read, not confirmed by an independent human reviewer as the plan's <manual> verify step specifies | fixed |  | 2026-09-10T06:46:57.653Z | 2026-09-10T11:02:55.089Z |
| 3 | 02 | unrun-verify | skills/proof-first/SKILL.md |  | Tracer feedback human-check (02-01 Task 1): SOURCES.md reproduction-boundary read plus PF-0.1/PF-3.1 framing judgment (CAT-03/CAT-04 flagged assumptions A-03/A-04) - harvested for end-of-phase UAT per workflow.human_verify_mode=end-of-phase, not yet signed off | open |  | 2026-09-11T00:38:23.292Z |  |
| 4 | 02 | unrun-verify | evals/pressure-tests.md |  | D-31 trigger pressure-test: must-fire/must-not-fire phrasings recorded with method only — this environment cannot drive a fresh harness session to install the skill and observe activation, so every Observed cell reads 'not yet observed'; a human must run each phrasing in a real harness session and fill in Observed/Date/Harness before this is fixed | open |  | 2026-09-11T01:22:59.066Z |  |
| 5 | 02 | unmet-truth | skills/proof-first/SKILL.md |  | CAT-08 token half: skill-token-budget-exceeded fires against the real SKILL.md (estimated 6207 tokens, words x 1.3, against the 5000-token ceiling) -- content-volume finding, not a formatting artifact (368 lines, well under the line ceiling). Needs catalog trimming or content restructuring in a future plan; do not resolve by re-wrapping or raising the ceiling. | fixed |  | 2026-09-11T01:48:55.000Z | 2026-09-11T04:32:38.278Z |

````json
[
  {
    "id": 1,
    "kind": "unrun-verify",
    "phase": "01",
    "file": "examples/deal-brief.md",
    "line": null,
    "description": "T-01-04 name-collision web search for 4 invented parties + 5 invented persons not run (no live network access in this environment) — human must confirm via web search before repo goes public",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-10T06:46:57.541Z",
    "resolved_at": "2026-09-10T11:02:49.274Z"
  },
  {
    "id": 2,
    "kind": "unrun-verify",
    "phase": "01",
    "file": "examples/deal-brief.md",
    "line": null,
    "description": "D-07/P-05 boundary check (no sentence compares two real products or companies) reviewed by executor via re-read, not confirmed by an independent human reviewer as the plan's <manual> verify step specifies",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-10T06:46:57.653Z",
    "resolved_at": "2026-09-10T11:02:55.089Z"
  },
  {
    "id": 3,
    "kind": "unrun-verify",
    "phase": "02",
    "file": "skills/proof-first/SKILL.md",
    "line": null,
    "description": "Tracer feedback human-check (02-01 Task 1): SOURCES.md reproduction-boundary read plus PF-0.1/PF-3.1 framing judgment (CAT-03/CAT-04 flagged assumptions A-03/A-04) - harvested for end-of-phase UAT per workflow.human_verify_mode=end-of-phase, not yet signed off",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-11T00:38:23.292Z",
    "resolved_at": null
  },
  {
    "id": 4,
    "kind": "unrun-verify",
    "phase": "02",
    "file": "evals/pressure-tests.md",
    "line": null,
    "description": "D-31 trigger pressure-test: must-fire/must-not-fire phrasings recorded with method only — this environment cannot drive a fresh harness session to install the skill and observe activation, so every Observed cell reads 'not yet observed'; a human must run each phrasing in a real harness session and fill in Observed/Date/Harness before this is fixed",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-11T01:22:59.066Z",
    "resolved_at": null
  },
  {
    "id": 5,
    "kind": "unmet-truth",
    "phase": "02",
    "file": "skills/proof-first/SKILL.md",
    "line": null,
    "description": "CAT-08 token half: skill-token-budget-exceeded fires against the real SKILL.md (estimated 6207 tokens, words x 1.3, against the 5000-token ceiling) -- content-volume finding, not a formatting artifact (368 lines, well under the line ceiling). Needs catalog trimming or content restructuring in a future plan; do not resolve by re-wrapping or raising the ceiling.",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-11T01:48:55.000Z",
    "resolved_at": "2026-09-11T04:32:38.278Z"
  }
]
````
