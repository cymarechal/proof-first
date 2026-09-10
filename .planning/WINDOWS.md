---
schema_version: 1
open_count: 2
waived_count: 0
fixed_count: 0
total_count: 2
last_updated: 2026-09-10T06:46:57.653Z
---

# Broken Windows Ledger

> Cross-phase defect register. With `workflow.windows_enforce` enabled, `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | 01 | unrun-verify | examples/deal-brief.md |  | T-01-04 name-collision web search for 4 invented parties + 5 invented persons not run (no live network access in this environment) — human must confirm via web search before repo goes public | open |  | 2026-09-10T06:46:57.541Z |  |
| 2 | 01 | unrun-verify | examples/deal-brief.md |  | D-07/P-05 boundary check (no sentence compares two real products or companies) reviewed by executor via re-read, not confirmed by an independent human reviewer as the plan's <manual> verify step specifies | open |  | 2026-09-10T06:46:57.653Z |  |

````json
[
  {
    "id": 1,
    "kind": "unrun-verify",
    "phase": "01",
    "file": "examples/deal-brief.md",
    "line": null,
    "description": "T-01-04 name-collision web search for 4 invented parties + 5 invented persons not run (no live network access in this environment) — human must confirm via web search before repo goes public",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-10T06:46:57.541Z",
    "resolved_at": null
  },
  {
    "id": 2,
    "kind": "unrun-verify",
    "phase": "01",
    "file": "examples/deal-brief.md",
    "line": null,
    "description": "D-07/P-05 boundary check (no sentence compares two real products or companies) reviewed by executor via re-read, not confirmed by an independent human reviewer as the plan's <manual> verify step specifies",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-10T06:46:57.653Z",
    "resolved_at": null
  }
]
````
