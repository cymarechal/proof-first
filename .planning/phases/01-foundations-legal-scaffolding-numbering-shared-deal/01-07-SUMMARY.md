---
phase: 01-foundations-legal-scaffolding-numbering-shared-deal
plan: 07
subsystem: testing
tags: [python, ci, mutation-testing, stdlib, github-actions]

# Dependency graph
requires:
  - phase: 01-foundations-legal-scaffolding-numbering-shared-deal
    provides: pointer-unparseable parsing fix (01-05) and per-block MC/end-of-file figure enforcement (01-06)
provides:
  - "--mutation-test mode in tools/check_repo.py that injects one named defect per violation code into a throwaway copy of the real repository files and asserts the matching code fires"
  - "CI wired to run self-test, mutation-test, and the live check on every push/PR, in that order, with zero pip install lines"
  - "a recorded red run proving the harness is fail-first, not merely green by construction"
affects: [phase-02, phase-03, phase-05]

actuals:
  tokens: 2888
  tasks: 2
  commits: 2

tech-stack:
  added: []
  patterns:
    - "mutation testing against production document shapes, not hand-built fixtures, using shutil.copytree/copy2 into tempfile.TemporaryDirectory scratch trees"
    - "table-row insertion by locating the separator row after a '## ' heading and writing immediately below it, for tables with zero data rows"

key-files:
  created: []
  modified:
    - tools/check_repo.py
    - .github/workflows/ci.yml

key-decisions:
  - "One mutation function per violation code (10 total), each editing exactly one file in an isolated scratch tree, so one mutation's violations can never mask another's absence."
  - "mutation_test() reads MUTATIONS/ALL_CHECK_CODES set equality as a hard requirement -- a code added later with no registered mutation is a reported failure, not a silent pass."
  - "Neutering check_pointer() with an injected early return also silences pointer-duplicated, not only pointer-missing -- both routed through the same disabled function is the correct signal, not a bug in the mutation design."

requirements-completed: [CAT-07, EX-01, LEG-03]

coverage:
  - id: D1
    description: "--mutation-test mode proves every one of the 10 violation codes fires against a deliberately mutated copy of the repository's real documents"
    requirement: CAT-07
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --mutation-test"
        status: pass
    human_judgment: false
  - id: D2
    description: "The mutation registry (MUTATIONS) covers exactly ALL_CHECK_CODES in both directions -- a code without a mutation is a reported failure"
    requirement: CAT-07
    verification:
      - kind: other
        ref: "python3 -c \"...set(MUTATIONS codes) == set(ALL_CHECK_CODES)...\""
        status: pass
    human_judgment: false
  - id: D3
    description: "The harness itself is proven fail-first: disabling check_pointer() in a scratch copy makes --mutation-test exit non-zero and print a code-specific FAIL line, not just an inverted exit status"
    requirement: EX-01
    verification:
      - kind: other
        ref: "manual reproduction command in Task 2 <verify>, output recorded verbatim below"
        status: pass
    human_judgment: false
  - id: D4
    description: "CI runs self-test, mutation-test, and the live check on every push/PR with no pip install and one job"
    requirement: LEG-03
    verification:
      - kind: other
        ref: ".github/workflows/ci.yml grep checks (pip install=0, checker invocations=3, jobs=1)"
        status: pass
    human_judgment: false
  - id: D5
    description: "Working tree and output are byte-identical / unmodified across repeated runs of all three modes"
    verification:
      - kind: other
        ref: "git status --porcelain before/after all three modes; diff of two consecutive live-run stdouts"
        status: pass
    human_judgment: false

duration: 25min
completed: 2026-09-10
status: complete
---

# Phase 1 Plan 7: Mutation-Testing Harness Summary

**A `--mutation-test` mode in `tools/check_repo.py` that injects one named defect per violation code into a throwaway copy of the real repository and proves each of the 10 checks fires, wired into CI between the self-test and the live check.**

## Performance

- **Duration:** 25 min
- **Started:** 2026-09-10 (recorded at plan start)
- **Completed:** 2026-09-10
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- Added `MUTATION_SOURCES` and `_copy_repo_subset()`, an allowlist-based copy of exactly `NUMBERING.md`, `NOTICES.md`, `README.md`, `examples/`, and `tools/` into a `tempfile.TemporaryDirectory` scratch tree — never `.git`, never `.planning`.
- Added one `_mutate_*` function per violation code (10 total, covering all codes that exist today, including `pointer-unparseable`, which did not exist when this plan was authored — see Deviations), each editing exactly one file in its own isolated scratch tree.
- Added `MUTATIONS`, an ordered registry pairing each code with a description and its mutate function, and `mutation_test()`, which runs a clean control copy first (requiring zero violations), then one isolated mutation per code, printing `mutation-test CONTROL:` / `mutation-test OK:` / `mutation-test FAIL:` / final `mutation-test PASS`/`FAILED` lines in that exact order.
- Wired `--mutation-test` into `main()` with the same exit-code contract as `--self-test` (0 on success, 1 on failure).
- Proved the harness is fail-first: injecting an early `return []` into `check_pointer()` in a scratch copy makes `--mutation-test` exit non-zero and print `mutation-test FAIL: pointer-missing` (see verbatim output below).
- Added the mutation-test command to `.github/workflows/ci.yml`'s single run block, between the self-test and the live check, with zero `pip install` lines and still exactly one job.
- Confirmed two consecutive live runs produce byte-identical stdout, and documented the `(code, subject)` sort-stability ordering rule in the module docstring's Usage block.

## Task Commits

1. **Task 1: Add a --mutation-test mode that proves every check fires against mutated production content** - `d847de5` (feat)
2. **Task 2: Prove the harness is fail-first and wire it into CI** - `b8dfcc3` (feat)

**Plan metadata:** (this commit)

## Files Created/Modified

- `tools/check_repo.py` - added `MUTATION_SOURCES`, `_copy_repo_subset()`, `_insert_table_rows_after_heading()`, ten `_mutate_*` functions, `MUTATIONS`, `mutation_test()`, the `--mutation-test` CLI flag, and a one-line output-ordering note in the docstring's Usage block.
- `.github/workflows/ci.yml` - added the mutation-test invocation between the self-test and live-check lines; renamed the step to name all three modes.

## Decisions Made

- Each mutation edits exactly one file in its own scratch tree (no shared scratch tree across mutations), trading a small amount of CI time for the guarantee that one mutation's violations can never mask another's absence — matches the plan's explicit threat register disposition (T-01-09, accepted).
- `mutation_test()` asserts `MUTATIONS` covers `ALL_CHECK_CODES` in both directions at runtime (not just via the standalone acceptance-criterion command), so a future code added without a mutation fails the harness itself, not only a separate CI check.
- The fail-first proof's injection point (`check_pointer(pointer, carriers, repo_root)`) silences both `pointer-missing` and `pointer-duplicated`, since both route through that one function. Recording only `pointer-missing FAIL` (per the plan's exact grep) is correct; `pointer-duplicated FAIL` appearing alongside it is expected and consistent, not a defect in the injection or the harness.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Covered the tenth violation code, `pointer-unparseable`, which did not exist when this plan was authored**
- **Found during:** Task 1 (read_first review of `tools/check_repo.py` as amended by 01-05/01-06)
- **Issue:** The plan's action text enumerates ten mutation targets and explicitly lists `pointer-unparseable` as one of them (mutation: "remove the `## Attribution pointer` heading line from `NOTICES.md`"), so the plan text itself already accounted for it — the plan's own `<must_haves>` and read_first notes flag this code as required coverage. No gap actually existed between plan intent and the ten codes; this entry documents that the coverage was verified against the current ten-code reality rather than assumed from the plan's original nine-code framing referenced in the run's context.
- **Fix:** Implemented `_mutate_pointer_unparseable()` and registered it in `MUTATIONS`, verified via the `set(MUTATIONS) == set(ALL_CHECK_CODES)` acceptance command.
- **Files modified:** `tools/check_repo.py`
- **Verification:** `python3 -c "...set(c.MUTATIONS codes) == set(c.ALL_CHECK_CODES)..."` exits 0; `--mutation-test` prints `mutation-test OK: pointer-unparseable ...`.
- **Committed in:** `d847de5` (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 missing-critical, resolved as already-covered).
**Impact on plan:** None on scope — the plan's own action text already named all ten codes including `pointer-unparseable`; this entry documents that the tenth code was verified live rather than silently assumed covered, per the run's explicit instruction to record it either way.

## Issues Encountered

None.

## Fail-First Proof (recorded verbatim, Task 2)

Command run: neuter `check_pointer()` with an injected early `return []` in a scratch copy of the real repository, then run `--mutation-test` against that copy.

```
mutation-test CONTROL: 0 violations on the unmutated copy
mutation-test OK: dup-id insert the same allocated-ID row twice into NUMBERING.md's Allocated IDs table
mutation-test OK: range-id insert an allocated-ID row whose PF number sits above its section's declared ceiling
mutation-test OK: revived-id insert the same ID into both the Allocated IDs table and the Deprecated IDs table
mutation-test OK: undefined-id cite a PF ID in README.md that no Allocated IDs row defines
mutation-test OK: dup-figure-key duplicate the first data row of the Canonical figures table
mutation-test OK: figure-order move the Canonical figures table's last data row to the top
mutation-test OK: unlisted-figure append a stray currency token after the Canonical figures table, the file's last section
mutation-test FAIL: pointer-missing remove the canonical pointer line from README.md
mutation-test FAIL: pointer-duplicated append a second copy of the canonical pointer line to README.md
mutation-test OK: pointer-unparseable remove the Attribution pointer heading from NOTICES.md
mutation-test FAILED: 2 codes not proven live
```

Exit code: 1 (non-zero), as required. The exact acceptance-criterion pipeline (`... | grep -q '^mutation-test FAIL: pointer-missing'`) exits 0.

Both `pointer-missing` and `pointer-duplicated` go FAIL because both checks route through the single neutered `check_pointer()` function — this is the correct, expected signal that the injection disabled the intended check family, not a defect.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- The regression class behind Phase 1's BLOCKER — a check named as covered, running in CI, that cannot fire against production content — now turns CI red the moment any check becomes inert, on every push and pull request.
- All 10 violation codes are proven live against the repository's real document shapes; `tools/check_repo.py` still imports only the Python standard library (`argparse`, `re`, `shutil`, `sys`, `tempfile`, `pathlib`); `.github/workflows/ci.yml` still has exactly one job and zero `pip install` lines.
- No blockers for Phase 2. Future phases adding a new violation code to `check_repo.py` must add a matching `_mutate_*` entry to `MUTATIONS` or `--mutation-test` (and therefore CI) fails.

---
*Phase: 01-foundations-legal-scaffolding-numbering-shared-deal*
*Completed: 2026-09-10*

## Self-Check: PASSED

- FOUND: tools/check_repo.py
- FOUND: .github/workflows/ci.yml
- FOUND: .planning/phases/01-foundations-legal-scaffolding-numbering-shared-deal/01-07-SUMMARY.md
- FOUND: commit d847de5 (Task 1)
- FOUND: commit b8dfcc3 (Task 2)
