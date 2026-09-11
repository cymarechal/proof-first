---
phase: 02-rule-catalog-integrity-skill-md-core
plan: 01
subsystem: rule-catalog
tags: [agent-skill, skill-md, rule-catalog, ci-checker, mutation-test, deletion-test]

# Dependency graph
requires:
  - phase: 01-foundations-legal-scaffolding-numbering-shared-deal
    provides: PF-/MC- numbering namespaces, NOTICES.md attribution pointer and framework statements, examples/deal-brief.md Canonical figures table, tools/check_repo.py's self-test/mutation-test harness
provides:
  - "The first installed Agent Skill in this repo: skills/proof-first/SKILL.md (four-key frontmatter, two-mode task framing, marker-vocabulary grammar, PF-0.1/PF-2.11/PF-3.1 rule bodies)"
  - "skills/proof-first/references/checklist.md and references/deletion-test.md"
  - "NUMBERING.md's PF-2 sub-blocks table and the first three Allocated IDs rows"
  - "A new CI-enforced catalog-id-drift violation code, proven live via --mutation-test"
  - "unlisted-figure widened to scan skills/ in addition to examples/"
affects: [02-02, 02-03, 02-04, 02-05, 02-06]

# Actuals (#2632)
actuals:
  tokens: 6478
  tasks: 3
  commits: 2

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Rule-defining heading extraction (### PF-#.# — Title) kept distinct from citation scanning (undefined-id already owns citations)"
    - "Three-way ID-set equality check (NUMBERING.md / SKILL.md headings / checklist.md rows) reusing split_sections/table_rows, no second table reader"
    - "Marker grammar placeholders (<rule> GAP/REVIEW/retention) used in interface-defining prose instead of concrete not-yet-allocated PF IDs, so undefined-id stays clean until later plans allocate those IDs"

key-files:
  created:
    - skills/proof-first/SKILL.md
    - skills/proof-first/references/checklist.md
    - skills/proof-first/references/deletion-test.md
  modified:
    - NUMBERING.md
    - tools/check_repo.py

key-decisions:
  - "Checkpoint resolved 'adopt-as-proposed': marker keywords GAP/REVIEW (categories commitment/reference/competitor/compliance), register heading '## Unresolved before this document is sent', and the 31-rule ID allocation map are frozen exactly as the plan proposed — no field amended."
  - "SKILL.md's marker-vocabulary section uses a <rule> placeholder instead of the illustrative PF-2.17/PF-3.3 IDs from the frozen decision text, because those specific sub-rules are not allocated until 02-03/02-04 and citing them now would fail undefined-id; the grammar itself (bracket form, keywords, categories) is unchanged."
  - "catalog-id-drift compares ID sets only (declared ceiling), scanning skills/*/SKILL.md (one directory level below skills/, matching the plan's anti-recursive-glob constraint so the shallow self-test fixture at skills/SKILL.md is untouched)."

requirements-completed: [CAT-01, CAT-03, CAT-04, CAT-09, CAT-10, INT-01, INT-02]

coverage:
  - id: D1
    description: "A real, installable three-file skills/proof-first/ folder: SKILL.md with valid four-key frontmatter, the attribution pointer carried exactly once, two-mode task framing with an anti-hallucination instruction, the marker-vocabulary grammar, and three fully-formed rules (PF-0.1, PF-2.11, PF-3.1) each with a Replace-with half and a worked ✗/✓ pair drawn from examples/deal-brief.md"
    requirement: "CAT-01, CAT-03, CAT-04, CAT-09, CAT-10, INT-01, INT-02"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py (live run) — check_repo: 0 violations"
        status: pass
      - kind: other
        ref: "30+ acceptance-criteria grep/python one-liners from 02-01-PLAN.md Task 1 (frontmatter keys, pointer count, rule-heading count, description band/trigger terms, no framework marks in frontmatter, Allocated IDs ascending)"
        status: pass
    human_judgment: true
    rationale: "The plan's own <human-check> requires a human read of SKILL.md against SOURCES.md's reproduction boundary (no framework wording reproduced) and a judgment on PF-0.1/PF-3.1's framing (CAT-03/CAT-04 flagged assumptions A-03/A-04). No tool in this project's stack performs that judgment; per workflow.human_verify_mode=end-of-phase this is harvested into the phase's UAT batch rather than halting this plan."
  - id: D2
    description: "catalog-id-drift: a new CI-enforced check comparing the PF subset of NUMBERING.md's Allocated IDs against each skills/*/SKILL.md's defined-heading IDs and its references/checklist.md rows, firing one violation per divergent ID"
    requirement: "CAT-09"
    verification:
      - kind: unit
        ref: "python3 tools/check_repo.py --self-test — verified-code list includes catalog-id-drift"
        status: pass
      - kind: integration
        ref: "python3 tools/check_repo.py --mutation-test — mutation-test OK: catalog-id-drift (13 codes proven live, up from 12)"
        status: pass
      - kind: integration
        ref: "python3 tools/check_repo.py (live run) — check_repo: 0 violations"
        status: pass
    human_judgment: false
  - id: D3
    description: "NUMBERING.md registers the new PF-2 sub-blocks table (Proof/Integrity) and the first three Allocated IDs rows, with Allocated/Next-free columns updated for PF-0, PF-2, PF-3"
    requirement: "CAT-09"
    verification:
      - kind: other
        ref: "python3 -c ... ids==['PF-0.1','PF-2.11','PF-3.1'] (ascending Allocated IDs check)"
        status: pass
      - kind: other
        ref: "awk PF-reserved-ranges Allocated/Next-free check (manual inspection, see Deviations)"
        status: pass
    human_judgment: false
---

# Phase 2 Plan 1: Rule Catalog & Integrity — Tracer Slice Summary

**Three production-quality PF rules (PF-0.1, PF-2.11, PF-3.1) authored in a real, installable `skills/proof-first/SKILL.md`, with a new `catalog-id-drift` CI check proving the whole registry/skill/checklist pipeline stays consistent — 13 violation codes now proven live via `--mutation-test`, up from 12.**

## Performance

- **Duration:** 11 min
- **Started:** 2026-09-11T00:24:59Z
- **Completed:** 2026-09-11T00:36:23Z
- **Tasks:** 3 (1 checkpoint:decision, 1 tracer, 1 auto)
- **Files modified:** 5 (3 created, 2 modified)

## Accomplishments

- Froze the three one-way output interfaces (marker grammar, register heading, 31-rule ID map) per the resolved checkpoint — adopted verbatim, no field amended.
- Authored `skills/proof-first/SKILL.md`: valid four-key Agent Skills frontmatter (`name`/`description`/`license`/`metadata`), the verbatim attribution pointer, a two-mode task-framing section with an anti-hallucination instruction, the marker-vocabulary grammar (`GAP`/`REVIEW`/retention forms, four `REVIEW` categories), reference-file pointers with named opening conditions, and three complete rules (PF-0.1, PF-2.11, PF-3.1), each with a `**Replace with:**` half and a worked ✗/✓ pair.
- Authored `references/checklist.md` (PF rows index) and `references/deletion-test.md` (four-class worked-pairs edge-case table: connotation-only, customer-first, RFP-mandated, half-empty compounds).
- Registered the three rules in `NUMBERING.md`'s Allocated IDs table and added the new `## PF-2 sub-blocks` table (Proof/Integrity ranges).
- Widened `tools/check_repo.py`'s `unlisted-figure` check to scan `skills/` alongside `examples/`, and added `skills` to `MUTATION_SOURCES` so the mutation-test control copy actually contains the new folder.
- Added `catalog-id-drift`: a new CI-enforced check with its own docstring-declared ceiling, self-test fixtures exercising both divergence directions, and a registered mutation proven to fire — 13 codes now proven live.

## Task Commits

1. **Task 1: End-to-end tracer slice (skill folder + NUMBERING.md + unlisted-figure widening)** — `e15545c` (feat)
2. **Task 2: `catalog-id-drift` check, proven live** — `23f95e0` (feat)

**Plan metadata commit:** recorded below after STATE.md/ROADMAP.md/REQUIREMENTS.md updates.

## Files Created/Modified

- `skills/proof-first/SKILL.md` — the installed skill's rule catalog spine (this plan's 3-rule slice)
- `skills/proof-first/references/checklist.md` — searchable PF-ID index
- `skills/proof-first/references/deletion-test.md` — four-class worked-pairs edge-case table
- `NUMBERING.md` — new `## PF-2 sub-blocks` table, first three `## Allocated IDs` rows, updated reserved-ranges columns
- `tools/check_repo.py` — `catalog-id-drift` check + parsers + self-test fixtures + mutation; `MUTATION_SOURCES` and `unlisted-figure` widened to `skills/`

## Decisions Made

- Checkpoint resolved `adopt-as-proposed`: all three frozen interfaces (marker grammar, register heading, 31-rule ID map) adopted exactly as the plan proposed — see key-decisions above.
- `SKILL.md`'s marker-vocabulary section states the grammar with a `<rule>` placeholder rather than the checkpoint's illustrative concrete IDs (`PF-2.17`, `PF-3.3`), since those specific rule numbers are allocated by later plans (02-03/02-04) and citing them now would trip `undefined-id`. The grammar itself — bracket form, keywords, four `REVIEW` categories, rule-number-first ordering — is unchanged from the frozen decision.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Removed premature citations of not-yet-allocated PF IDs**
- **Found during:** Task 1, first `python3 tools/check_repo.py` run
- **Issue:** The initial draft of `SKILL.md`'s marker-vocabulary examples and `references/deletion-test.md`'s verdicts cited `PF-2.17`, `PF-3.2`, and `PF-3.3` — real IDs from the checkpoint's illustrative examples, but ones this plan does not allocate (they belong to plans 02-03 and 02-04). `undefined-id` correctly flagged all of them as citations with no Allocated IDs row.
- **Fix:** Replaced the marker-vocabulary section's illustrative examples with a `<rule>` placeholder (grammar stays fully specified: bracket form, keywords, categories, rule-number-first ordering) and reworded `deletion-test.md`'s verdicts to describe the mechanisms (provenance override, per-token testing) without naming the specific unallocated sub-rule IDs.
- **Files modified:** `skills/proof-first/SKILL.md`, `skills/proof-first/references/deletion-test.md`
- **Verification:** `python3 tools/check_repo.py` → `check_repo: 0 violations`
- **Committed in:** `e15545c` (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 blocking).
**Impact on plan:** No scope creep — the fix only removes premature citations; the marker grammar itself is unchanged from the frozen checkpoint decision, and PF-2.17/PF-3.2/PF-3.3 will cite correctly once 02-03/02-04 allocate them.

### Acceptance-Criterion Discrepancies (verification-script bugs, not implementation defects)

**`## PF-2 sub-blocks` row-count awk check reports 3, not the plan's stated 2.**
The plan's acceptance criterion `awk '/^## PF-2 sub-blocks/{f=1;next} /^## /{f=0} f && /^\| [A-Z]/' NUMBERING.md | wc -l` expects `2`. The table was built in the exact form the action text requires — identical to `## PF-1 sub-blocks`' own `| Element | Range |` header, with exactly two data rows (`Proof`, `Integrity`) — but the awk pattern `/^\| [A-Z]/` also matches the header row itself (`| Element | Range |` starts with `| E`, an uppercase letter), so it counts 3 lines (header + 2 data), not 2. This is reproduced identically against the pre-existing, unmodified `## PF-1 sub-blocks` table using the analogous pattern, which prints `8` (header + 7 data rows), not 7 — confirming this is a property of the verification one-liner itself, not of this plan's table. The substantive requirement (D-05: exactly two data rows, `Proof | PF-2.1-PF-2.10` and `Integrity | PF-2.11-PF-2.20`, same form as PF-1) is met and independently verified via the Allocated-IDs-style parse (`table_rows()`-equivalent row extraction excluding header/separator, which reports exactly 2). No code depends on this table's exact text shape — it is documentation only, not read by `parse_numbering` (confirmed in RESEARCH.md's Accepted Gaps: "the PF-2 sub-block table lands in this plan but is not enforced until 02-06").

## Issues Encountered

None beyond the deviation and acceptance-criterion discrepancy documented above.

## Authentication Gates

None — no external service or CLI authentication was required.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- The three frozen interfaces (marker grammar, register heading, 31-rule ID map) are now committed to `SKILL.md`/`NUMBERING.md` and ready for plans 02-02 through 02-06 to build on without renegotiation.
- `catalog-id-drift` will now catch any future drift the moment plans 02-02/02-03/02-04 add rows to `checklist.md` or headings to `SKILL.md`.
- Open item for end-of-phase UAT: the tracer's `<human-check>` (SOURCES.md reproduction-boundary read; PF-0.1/PF-3.1 framing judgment tied to flagged assumptions A-03/A-04) is harvested into the phase's UAT batch per `workflow.human_verify_mode: end-of-phase` — not yet signed off by an actual human reviewer.
- No blockers for 02-02 (the next plan, authoring `PF-1`'s Command of the Message spine rules).

## Self-Check: PASSED

- `[ -f skills/proof-first/SKILL.md ]` → FOUND
- `[ -f skills/proof-first/references/checklist.md ]` → FOUND
- `[ -f skills/proof-first/references/deletion-test.md ]` → FOUND
- `git log --oneline --all | grep -q e15545c` → FOUND
- `git log --oneline --all | grep -q 23f95e0` → FOUND
- `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py` → all green, 13 codes proven live, 0 live violations
- All Task 1 and Task 2 acceptance criteria re-run: all PASS (see Deviations for the one documented acceptance-script discrepancy, which does not affect any code-enforced check)

---
*Phase: 02-rule-catalog-integrity-skill-md-core*
*Completed: 2026-09-11*
