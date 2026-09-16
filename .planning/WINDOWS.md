---
schema_version: 1
open_count: 4
waived_count: 0
fixed_count: 5
total_count: 9
last_updated: 2026-09-16T04:37:00.274Z
---

# Broken Windows Ledger

> Cross-phase defect register. With `workflow.windows_enforce` enabled, `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | 01 | unrun-verify | examples/deal-brief.md |  | T-01-04 name-collision web search for 4 invented parties + 5 invented persons not run (no live network access in this environment) — human must confirm via web search before repo goes public | fixed |  | 2026-09-10T06:46:57.541Z | 2026-09-10T11:02:49.274Z |
| 2 | 01 | unrun-verify | examples/deal-brief.md |  | D-07/P-05 boundary check (no sentence compares two real products or companies) reviewed by executor via re-read, not confirmed by an independent human reviewer as the plan's <manual> verify step specifies | fixed |  | 2026-09-10T06:46:57.653Z | 2026-09-10T11:02:55.089Z |
| 3 | 02 | unrun-verify | skills/proof-first/SKILL.md |  | Tracer feedback human-check (02-01 Task 1): SOURCES.md reproduction-boundary read plus PF-0.1/PF-3.1 framing judgment (CAT-03/CAT-04 flagged assumptions A-03/A-04) - signed off at end-of-phase UAT 2026-09-11 (02-UAT.md test 1, result pass); stays open because the formal reproduction-boundary gate is Phase 6 LEG-04 | open |  | 2026-09-11T00:38:23.292Z |  |
| 4 | 02 | unrun-verify | evals/pressure-tests.md |  | D-31 trigger pressure-test: must-fire/must-not-fire phrasings recorded with method only — this environment cannot drive a fresh harness session to install the skill and observe activation, so every Observed cell reads 'not yet observed'; a human must run each phrasing in a real harness session and fill in Observed/Date/Harness before this is fixed | open |  | 2026-09-11T01:22:59.066Z |  |
| 5 | 02 | unmet-truth | skills/proof-first/SKILL.md |  | CAT-08 token half: skill-token-budget-exceeded fires against the real SKILL.md (estimated 6207 tokens, words x 1.3, against the 5000-token ceiling) -- content-volume finding, not a formatting artifact (368 lines, well under the line ceiling). Needs catalog trimming or content restructuring in a future plan; do not resolve by re-wrapping or raising the ceiling. | fixed |  | 2026-09-11T01:48:55.000Z | 2026-09-11T04:32:38.278Z |
| 6 | 03 | unrun-verify | skills/proof-first/references/completeness-audit.md |  | The eight MC dimension names (Metric, Economic Buyer, Decision Criteria, Decision Process, Paper Process, Pain, Champion, Competition) and their MC-1 through MC-40 ID-range order were frozen in NUMBERING.md and .planning/REQUIREMENTS.md before Phase 3 began, and that order matches the MEDDICC acronym's own canonical sequence. SOURCES.md states that a source's own ordered list reproduced in its order is reproduction, not paraphrase, and that no tool in this stack performs that judgment. Phase 3 used content levers only: every dimension's audit question is written in this repository's own words, grounded entirely in examples/deal-brief.md's facts, and Phase 3 deliberately did not reorder or rename any dimension. The paraphrase-boundary judgment on the inherited ID-range order itself is routed to Phase 6's LEG-04 gate, which is this entry's closure condition. | open |  | 2026-09-14T08:17:27.877Z |  |
| 7 | 03 | unmet-truth | skills/proof-first/references/completeness-audit.md |  | 03-05's single standalone-audit re-check (docs/B-proposal-section.md) printed an unrequested ## Artifact family section before ## Completeness gaps, diverging from 'Running the audit on its own's stated shape ('returns...and nothing more') and from 03-UAT.md test 1's 6/6 clean result. One-sample variance, not reproduced across multiple runs; AUD-03 was still marked Complete in this plan on the strength of the 6/6 Phase 3 UAT evidence, but this single later sample is recorded so it isn't silently lost. | fixed |  | 2026-09-14T12:38:38.005Z | 2026-09-15T03:04:40.278Z |
| 8 | 03 | unmet-truth | skills/proof-first/SKILL.md |  | MOD-04 residual after 03-07's two content levers (five-value family line, self-check gate), measured by 03-08's committed instrument (evals/conformance/run_conformance.py): 16 of 20 scoreable write-mode sessions conformant across claude-sonnet-5 and claude-opus-5, five fixtures, two repeats (measured SKILL.md blob 9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a). A same-instrument, same-model paired baseline against the pre-03-07 skill (blob 1fc1e1092941157191268a8294ab4e1edc65cdac, commit 6f62385) measured 5 of 11 scoreable sonnet-5-only sessions conformant. Restricted to sonnet-5 on both sides for a like-for-like comparison: 6 of 10 (60.0%) post-03-07 versus 5 of 11 (45.5%) pre-03-07 -- a real, measured improvement from 03-07's levers that still falls short of the 87.5% bar this entry's pre-committed closure rule uses. Zero sessions in either arm omitted the family line entirely (no genuine no-family verdict); every non-conformant session cited a rule marker before naming the family (rule-before-family), which is the residual failure mode MOD-04 actually tracks -- the family must be named before any rule is applied, not merely present somewhere in the response. This fixture set and prompt differ from the earlier 5/6 and 14/16 figures' recipe (03-05's UAT), so these rates are not directly comparable to those. Instruction-text changes (03-05, 03-07) have now been tried and measured twice; both times the rate stayed under the closure bar, so per 03-08-PLAN.md's pre-committed decision rule, closure now requires a lever other than instruction wording. Full run-by-run evidence and reproduction commands: evals/conformance/RESULTS-mod04.md. | open |  | 2026-09-15T01:50:32.188Z |  |
| 9 | 03 | unmet-truth | skills/proof-first/references/artifact-patterns.md |  | Residual source label outside 03-05's scope: artifact-patterns.md line 103 still reads 'Diane Osoria, the economic buyer'. Plan 03-05 scoped the G-03-5 fix to the six affected MC bodies in completeness-audit.md, so this one occurrence in the Executive summary family section was not covered and is the last remaining instance of a frozen NUMBERING.md registry label used as this repository's own unattributed noun in shipped skill content. One-word fix ('the person who signs'); left unmade rather than silently widening a verified plan's scope. Closure: fold into the next content plan or into Phase 6 LEG-04 alongside entries 3 and 6. | fixed |  | 2026-09-15T01:50:41.248Z | 2026-09-15T03:04:40.161Z |

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
    "description": "Tracer feedback human-check (02-01 Task 1): SOURCES.md reproduction-boundary read plus PF-0.1/PF-3.1 framing judgment (CAT-03/CAT-04 flagged assumptions A-03/A-04) - signed off at end-of-phase UAT 2026-09-11 (02-UAT.md test 1, result pass); stays open because the formal reproduction-boundary gate is Phase 6 LEG-04",
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
  },
  {
    "id": 6,
    "kind": "unrun-verify",
    "phase": "03",
    "file": "skills/proof-first/references/completeness-audit.md",
    "line": null,
    "description": "The eight MC dimension names (Metric, Economic Buyer, Decision Criteria, Decision Process, Paper Process, Pain, Champion, Competition) and their MC-1 through MC-40 ID-range order were frozen in NUMBERING.md and .planning/REQUIREMENTS.md before Phase 3 began, and that order matches the MEDDICC acronym's own canonical sequence. SOURCES.md states that a source's own ordered list reproduced in its order is reproduction, not paraphrase, and that no tool in this stack performs that judgment. Phase 3 used content levers only: every dimension's audit question is written in this repository's own words, grounded entirely in examples/deal-brief.md's facts, and Phase 3 deliberately did not reorder or rename any dimension. The paraphrase-boundary judgment on the inherited ID-range order itself is routed to Phase 6's LEG-04 gate, which is this entry's closure condition.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-14T08:17:27.877Z",
    "resolved_at": null
  },
  {
    "id": 7,
    "kind": "unmet-truth",
    "phase": "03",
    "file": "skills/proof-first/references/completeness-audit.md",
    "line": null,
    "description": "03-05's single standalone-audit re-check (docs/B-proposal-section.md) printed an unrequested ## Artifact family section before ## Completeness gaps, diverging from 'Running the audit on its own's stated shape ('returns...and nothing more') and from 03-UAT.md test 1's 6/6 clean result. One-sample variance, not reproduced across multiple runs; AUD-03 was still marked Complete in this plan on the strength of the 6/6 Phase 3 UAT evidence, but this single later sample is recorded so it isn't silently lost.",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-14T12:38:38.005Z",
    "resolved_at": "2026-09-15T03:04:40.278Z"
  },
  {
    "id": 8,
    "kind": "unmet-truth",
    "phase": "03",
    "file": "skills/proof-first/SKILL.md",
    "line": null,
    "description": "MOD-04 residual after 03-07's two content levers (five-value family line, self-check gate), measured by 03-08's committed instrument (evals/conformance/run_conformance.py): 16 of 20 scoreable write-mode sessions conformant across claude-sonnet-5 and claude-opus-5, five fixtures, two repeats (measured SKILL.md blob 9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a). A same-instrument, same-model paired baseline against the pre-03-07 skill (blob 1fc1e1092941157191268a8294ab4e1edc65cdac, commit 6f62385) measured 5 of 11 scoreable sonnet-5-only sessions conformant. Restricted to sonnet-5 on both sides for a like-for-like comparison: 6 of 10 (60.0%) post-03-07 versus 5 of 11 (45.5%) pre-03-07 -- a real, measured improvement from 03-07's levers that still falls short of the 87.5% bar this entry's pre-committed closure rule uses. Zero sessions in either arm omitted the family line entirely (no genuine no-family verdict); every non-conformant session cited a rule marker before naming the family (rule-before-family), which is the residual failure mode MOD-04 actually tracks -- the family must be named before any rule is applied, not merely present somewhere in the response. This fixture set and prompt differ from the earlier 5/6 and 14/16 figures' recipe (03-05's UAT), so these rates are not directly comparable to those. Instruction-text changes (03-05, 03-07) have now been tried and measured twice; both times the rate stayed under the closure bar, so per 03-08-PLAN.md's pre-committed decision rule, closure now requires a lever other than instruction wording. Full run-by-run evidence and reproduction commands: evals/conformance/RESULTS-mod04.md.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-15T01:50:32.188Z",
    "resolved_at": null
  },
  {
    "id": 9,
    "kind": "unmet-truth",
    "phase": "03",
    "file": "skills/proof-first/references/artifact-patterns.md",
    "line": null,
    "description": "Residual source label outside 03-05's scope: artifact-patterns.md line 103 still reads 'Diane Osoria, the economic buyer'. Plan 03-05 scoped the G-03-5 fix to the six affected MC bodies in completeness-audit.md, so this one occurrence in the Executive summary family section was not covered and is the last remaining instance of a frozen NUMBERING.md registry label used as this repository's own unattributed noun in shipped skill content. One-word fix ('the person who signs'); left unmade rather than silently widening a verified plan's scope. Closure: fold into the next content plan or into Phase 6 LEG-04 alongside entries 3 and 6.",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-15T01:50:41.248Z",
    "resolved_at": "2026-09-15T03:04:40.161Z"
  }
]
````
