---
phase: 03-completeness-audit-artifact-patterns
plan: 13
subsystem: eval-harness
tags: [python, stdlib, durability, conformance-instrument, data-integrity]

requires:
  - phase: 03-completeness-audit-artifact-patterns
    provides: "03-09's anchored scorer (FAMILY_LINE_WINDOW_CHARS=400) and TimeoutExpired transcript-preservation fix, both left untouched by this plan"
provides:
  - "run_conformance.py's run_matrix()/_write_result_line() per-session write-and-flush durability guarantee, proven offline in --self-test"
  - "RESULTS-mod04.md's corrected Arm A no-family enumeration and its ## Instrument durability fix (03-13) disclosure section"
affects: ["03-14", "any future MOD-04 remeasurement plan"]

actuals:
  tokens: 4879
  tasks: 2
  commits: 3

tech-stack:
  added: []
  patterns:
    - "Write-then-flush-per-record durability: a single named helper (_write_result_line) is the only path any output line takes to disk, so a future edit that drops the flush is a one-line diff instead of a scattered one."
    - "Self-test durability proof via injectable session_fn stub raising an exception outside every handler the loop catches (KeyboardInterrupt), asserting on-disk state before the exception propagates -- offline, no live subprocess."

key-files:
  created: []
  modified:
    - evals/conformance/run_conformance.py
    - evals/conformance/RESULTS-mod04.md

key-decisions:
  - "Committed the orchestrator's own pre-existing STATE.md/milestone.lock/state.json bookkeeping churn as a separate chore commit before Task 1, because the plan's precondition required a clean git tree and its Task 2 verify required `git status --porcelain` to print nothing after the task's own commit -- both were unsatisfiable with that unrelated dirt already present."
  - "Dropped the dead, never-read `run_index` counter when extracting the loop into run_matrix() rather than carrying it forward -- a genuinely inert local variable, not a behavior change, and the plan's own 'moved unchanged in behavior' instruction is about the four exception handlers and the written output, not every local name."
  - "Left Arm B's no-family/conformant enumerations and the pre-existing 'first attempt' labeling ambiguity in the Arm A prose (\"12 attempted\" paragraph) untouched -- re-checked both against their own stated counts per the task's instruction, found no arithmetic disagreement, and the plan explicitly forbids adjusting anything not shown to disagree."

requirements-completed: []

coverage:
  - id: D1
    description: "run_matrix() and _write_result_line() extract the model x fixture x repeat loop so every result line is written and flushed to disk the moment it is scored, closing 03-REVIEW.md CR-01's silent-data-loss-on-interruption defect"
    requirement: "AUD-02"
    verification:
      - kind: other
        ref: "python3 evals/conformance/run_conformance.py --self-test (behavior case 11: KeyboardInterrupt on the 3rd stubbed call, asserts 2 prior verdict lines already on disk)"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py --self-test / --mutation-test (31 codes) and python3 tools/check_repo.py (0 violations)"
        status: pass
    human_judgment: false
  - id: D2
    description: "RESULTS-mod04.md's Arm A no-family enumeration now names all 7 sessions matching its stated count, and a new dated section discloses the durability defect, its fix, and that no figure changed"
    requirement: "MOD-05"
    verification:
      - kind: other
        ref: "grep checks against RESULTS-mod04.md (B-proposal-section presence, section heading count, N_A/N_B figures unmoved, 58+ run-block lines) plus python3 tools/check_repo.py (0 violations)"
        status: pass
    human_judgment: false

duration: 10min
completed: 2026-09-16
status: complete
---

# Phase 03 Plan 13: Instrument Durability Fix (CR-01) and Enumeration Correction (WR-01) Summary

**`run_conformance.py` now writes and flushes each scored session to disk the instant it is scored instead of batching the whole matrix in memory, closing the exact silent-data-loss defect that had already destroyed two earlier MOD-04 measurement attempts — proven offline by a new `KeyboardInterrupt`-based self-test case, with the corresponding `RESULTS-mod04.md` enumeration gap fixed and disclosed in a new dated section.**

## Performance

- **Duration:** ~10 min
- **Started:** 2026-09-16T10:34Z (approx, from STATE.md's pre-spawn timestamp)
- **Completed:** 2026-09-16T10:41Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Extracted the `model x fixture x repeat` loop out of `main()` into a new `run_matrix()` function that takes an open append-mode file handle and an injectable `session_fn` (defaulting to `run_session`), writing and flushing every result line through a new `_write_result_line()` helper the moment each session is scored — no in-memory accumulator remains anywhere in `main()` or `run_matrix()`.
- Added self-test behavior case 11: a stub matching `run_session`'s keyword signature returns a conformant transcript for its first two calls and raises `KeyboardInterrupt` on its third (an exception type outside every handler `run_matrix()` catches), then asserts the results file already contains exactly two `| verdict=` lines, both `conformant`, before the exception propagates — proving the durability property offline with no `claude` binary and no network call.
- Corrected the module docstring's `Usage:` block to state the new write-and-flush guarantee and its one disclosed residual: concurrent invocations appending to the same results file may interleave, and the tool makes no parallel-safety claim.
- Fixed `RESULTS-mod04.md`'s Arm A `no-family: 7` bullet, which previously enumerated only six sessions, by adding the omitted `B-proposal-section` first attempt (`2026-09-16T06:42:11.983431+00:00Z`, `verdict=no-family`) — the stated count of 7 was already correct and is unchanged.
- Appended `## Instrument durability fix (03-13)` to `RESULTS-mod04.md`, stating the defect, the fix and its commit, the disclosed parallel-invocation residual, that no figure in the file moves, and the enumeration correction with the omitted session's timestamp.

## Task Commits

Each task was committed atomically:

1. **Pre-task: sync orchestrator session bookkeeping** - `b825fea` (chore) — deviation, see below
2. **Task 1: Make every scored session durable, hold the property in CI** - `c99a848` (fix)
3. **Task 2: Correct the Arm A enumeration, record the durability fix** - `dc8f899` (docs)

**Plan metadata:** committed as part of this SUMMARY's own commit (see below)

## Files Created/Modified
- `evals/conformance/run_conformance.py` - Adds `run_matrix()` and `_write_result_line()`; `main()` now opens the results file once in append mode and holds it open across the run; adds self-test behavior case 11; corrects the module docstring's `Usage:` block.
- `evals/conformance/RESULTS-mod04.md` - Corrects the Arm A `no-family` enumeration to name all 7 sessions; appends `## Instrument durability fix (03-13)`.

## Decisions Made
- Committed the orchestrator's pre-existing `STATE.md`/`milestone.lock`/`state.json` bookkeeping diff as a standalone `chore` commit before Task 1 rather than leaving it dirty, so the plan's clean-tree precondition and Task 2's post-commit `git status --porcelain` verify assertion were both satisfiable. This is unrelated to the plan's own `files_modified` list and carries no content risk (auto-generated session-tracking fields only).
- Dropped the pre-existing, never-read `run_index` counter when extracting the loop into `run_matrix()` — it was incremented but never consumed anywhere in the original code, so removing it changes no observable behavior.
- Re-checked Arm B's `no-family: 6` and both arms' `conformant:` bullets against their own stated counts per the task's instruction; all three already agreed with their enumerations, so none was touched — the plan explicitly forbids adjusting anything not shown to disagree.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Committed pre-existing dirty tree before starting Task 1**
- **Found during:** Precondition check, before Task 1
- **Issue:** `git status --porcelain` was not empty at plan start — `.planning/STATE.md`, `.planning/milestone.lock`, and `.planning/state.json` carried uncommitted orchestrator session-bookkeeping churn from before this executor was spawned. This blocked the plan's explicit `<precondition>` ("git status --porcelain prints nothing before this task starts") and would also have failed Task 2's own `git status --porcelain` verify check (which requires nothing printed after that task's commit).
- **Fix:** Committed the three files as a standalone `chore(03): sync session bookkeeping before 03-13 execution` commit before starting Task 1, restoring a clean tree with no content risk (auto-generated timestamp/session-id fields only, unrelated to this plan's `files_modified`).
- **Files modified:** `.planning/STATE.md`, `.planning/milestone.lock`, `.planning/state.json`
- **Verification:** `git status --porcelain` printed nothing immediately after this commit and before Task 1 began.
- **Committed in:** `b825fea`

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Necessary to satisfy the plan's own precondition and post-commit clean-tree verify assertion. No scope creep — no file in this plan's `files_modified` list was touched by the fix.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- `run_conformance.py` is now durable per-session; a future MOD-04 remeasurement invocation can be interrupted between sessions without losing already-scored results.
- `RESULTS-mod04.md`'s Arm A enumeration now matches its own stated count, and the file's durability-fix disclosure is in place for any reader auditing the instrument's history.
- `MOD-04` remains unchecked, as required — this plan closes no requirement. WINDOWS.md entry 8 remains `waived`, unaffected by this plan.
- 03-REVIEW.md's remaining Warning (WR-02, `check_skill_family_line_gate()`/`check_skill_family_order_gate()` case-sensitivity inconsistency) and Info (IN-01, stale `check_repo.py` docstring) findings are out of this plan's scope and remain open for a future gap-closure plan.

---
*Phase: 03-completeness-audit-artifact-patterns*
*Completed: 2026-09-16*

## Self-Check: PASSED

- `evals/conformance/run_conformance.py` — FOUND on disk
- `evals/conformance/RESULTS-mod04.md` — FOUND on disk
- `.planning/phases/03-completeness-audit-artifact-patterns/03-13-SUMMARY.md` — FOUND on disk
- Commit `b825fea` (chore: sync session bookkeeping) — FOUND in git log
- Commit `c99a848` (fix: run_conformance.py durability) — FOUND in git log
- Commit `dc8f899` (docs: RESULTS-mod04.md enumeration + durability section) — FOUND in git log
- `python3 evals/conformance/run_conformance.py --self-test` — re-ran, PASS
- `python3 tools/check_repo.py --self-test` / `--mutation-test` (31 codes) / plain run (0 violations) — re-ran, PASS
- `.planning/REQUIREMENTS.md` MOD-04 checkbox — confirmed still `[ ]`, unchanged by this plan
