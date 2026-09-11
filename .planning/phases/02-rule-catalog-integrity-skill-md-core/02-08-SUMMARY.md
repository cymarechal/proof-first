---
phase: 02-rule-catalog-integrity-skill-md-core
plan: 08
subsystem: testing
tags: [mutation-testing, ci-enforcement, integrity-tooling, self-verification]

# Dependency graph
requires:
  - phase: 02-07
    provides: "skills/proof-first/SKILL.md trimmed to 3,694 words (4,802 estimated tokens), under CAT-08's 5,000-token ceiling, making the control copy clean for skill-token-budget-exceeded"
provides:
  - "mutation_test() asserting discrimination (silent-on-control, fires-on-mutated) rather than mere post-mutation firing, for all 21 violation codes"
  - "KNOWN_OPEN_VIOLATIONS emptied to frozenset() with a comment instructing any future entry to name a (code, subject) pair"
  - "Corrected docstrings for _mutate_skill_token_budget_exceeded and frontmatter-description-invalid stating what is now true"
affects: [02-09, phase-3-planning, phase-6-legal-review]

# Actuals (#2632)
actuals:
  tokens: 2562
  tasks: 2
  commits: 2

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Discrimination-based mutation testing: hoist one control run's firing-code set out of the per-mutation loop and classify each mutation's post-fire state against it (silent-then-fires vs. already-firing), rather than asserting mere post-mutation firing"

key-files:
  created: []
  modified:
    - tools/check_repo.py

key-decisions:
  - "Reused the existing single control run as the pre-state for every mutation (one control_codes set captured once, before the per-mutation loop) rather than running a second control per mutation — the plan's own interfaces analysis established every scratch root starts from the same _copy_repo_subset of the same tree, so one run is a sound pre-state for all 21."
  - "Left mutation_test()'s KNOWN_OPEN_VIOLATIONS filter expression (matching on bare code) unchanged in Task 2, per the plan's explicit instruction — against an empty set it is already an unweakened assertion, and reshaping it now would be untested code with no live case."
  - "TDD gate for Task 1 interpreted as behavior-pinning via the plan's own <verify>/<acceptance_criteria> commands run against the unmodified file first (RED: 0 'discrimination-proven' occurrences, 1 'codes proven live' occurrence), rather than a separate committed test file — this task modifies the test harness itself (mutation_test()), so there is no separate implementation-under-test to split a test file from. See 'TDD Gate Compliance' below."

patterns-established: []

requirements-completed: [CAT-08, CAT-09]

coverage:
  - id: D1
    description: "mutation_test() classifies each of the 21 codes as discrimination-proven (silent on control, fires on mutated) or confirmed-fire-only (fires on both), never blending the two into one count"
    requirement: "CAT-08"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --mutation-test (21/21 OK, 'mutation-test PASS: 21 codes discrimination-proven', 0 blended-wording occurrences)"
        status: pass
    human_judgment: false
  - id: D2
    description: "The fire-only branch is proven reachable: a deliberately over-ceiling scratch control (not committed) produces 20 discrimination-proven + 1 confirmed-fire-only, with all_ok still True"
    requirement: "CAT-08"
    verification:
      - kind: other
        ref: "in-process mutation_test() invocation against a monkeypatched over-ceiling scratch tree (see 'Fire-Only Branch Proof' below)"
        status: pass
    human_judgment: false
  - id: D3
    description: "A no-op substitution for _mutate_skill_token_budget_exceeded now reports FAIL (not discrimination-proven), inverting 02-REVIEW.md CR-01's experiment where the same substitution reported OK/proven"
    requirement: "CAT-08"
    verification:
      - kind: other
        ref: "temporary no-op body swap, restored after the run (see 'No-Op Inversion Proof' below)"
        status: pass
    human_judgment: false
  - id: D4
    description: "KNOWN_OPEN_VIOLATIONS is exactly frozenset(), CONTROL reports 0 known-open, and the comment names WINDOWS.md id 5 as closed and instructs future entries to name a (code, subject) pair"
    requirement: "CAT-09"
    verification:
      - kind: other
        ref: "python3 -c extraction of KNOWN_OPEN_VIOLATIONS prints 'frozenset()'; mutation-test CONTROL line prints '0 known-open'"
        status: pass
    human_judgment: false
  - id: D5
    description: "frontmatter-description-invalid's docstring states its true boundary (present-but-invalid only) and names frontmatter-unparseable as owner of the absent case; confirmed against a fixture with no description key"
    requirement: "CAT-09"
    verification:
      - kind: other
        ref: "fixture SKILL.md (name + license, no description key) via check_frontmatter() — reports frontmatter-unparseable only, no frontmatter-description-invalid"
        status: pass
    human_judgment: false

duration: 20min
completed: 2026-09-11
status: complete
---

# Phase 02 Plan 08: Mutation-Test Discrimination and Honesty Corrections Summary

**Rewrote `mutation_test()` to assert discrimination (silent-on-control, fires-on-mutated) instead of mere post-mutation firing, emptied `KNOWN_OPEN_VIOLATIONS`, and corrected two docstrings that overclaimed what the tool proves — closing 02-REVIEW.md CR-01, CR-02, and WR-01.**

## Performance

- **Duration:** ~20 min
- **Tasks:** 2
- **Files modified:** 1 (`tools/check_repo.py`)

## Accomplishments

- `mutation_test()` now hoists the control run's firing-code set out of the `with` block and classifies each of the 21 mutations against it: silent-on-control + fires-on-mutated = **discrimination-proven**; fires-on-control + fires-on-mutated = **confirmed-fire-only**, reported separately and never folded into the proven count. No second control run per mutation was added — the existing single control run is the sound pre-state for every scratch copy.
- The blended `mutation-test PASS: 21 codes proven live` wording is gone entirely (`grep -c 'codes proven live' tools/check_repo.py` prints `0`). The new final line reads `mutation-test PASS: 21 codes discrimination-proven` against the current, under-ceiling repository state.
- `KNOWN_OPEN_VIOLATIONS` is now `frozenset()`. Its comment states `.planning/WINDOWS.md` id 5 is closed and instructs any future entry to name a specific `(code, subject)` pair rather than a bare code — closing 02-REVIEW.md WR-01's latent-risk finding by construction, not by re-scoping.
- `_mutate_skill_token_budget_exceeded`'s docstring and its `MUTATIONS` entry description no longer assert the real file is "already-over-ceiling" — both now state the control copy is under the ceiling (3,694 words / 4,802 estimated tokens, 198-token margin) and the mutation pushes it over, exactly like every other mutation (`grep -c 'already-over-ceiling' tools/check_repo.py` prints `0`).
- `frontmatter-description-invalid`'s module-docstring paragraph now states its true boundary: it fires on a present-but-invalid description only, and names `frontmatter-unparseable` as the owner of the fully-absent-key case (02-REVIEW.md CR-02). `check_frontmatter()` itself was not touched — this was a documentation-only defect.
- All three CI-trio commands (`--self-test`, `--mutation-test`, bare live run) pass; `.github/workflows/ci.yml` is byte-unchanged (`git diff --stat` empty).

## Task Commits

1. **Task 1: mutation_test asserts discrimination, not firing** — `493853d` (feat)
2. **Task 2: Empty the stale allowance and correct both overclaiming docstrings** — `f04e298` (fix)

**Plan metadata:** commit pending (this SUMMARY + STATE.md + ROADMAP.md + REQUIREMENTS.md).

## Files Created/Modified

- `tools/check_repo.py` — `mutation_test()` rewritten to classify discrimination-proven vs. confirmed-fire-only; `KNOWN_OPEN_VIOLATIONS` emptied with a rewritten comment; `_mutate_skill_token_budget_exceeded`'s docstring and `MUTATIONS` description corrected; module docstring's `frontmatter-description-invalid` paragraph corrected. No `_mutate_*` function body changed, no import added, no check function touched.

## TDD Gate Compliance

Task 1 carries `tdd="true"`, but this task's target is `mutation_test()` itself — the repository's own test harness, not application code under test. There is no separate test-file/implementation-file split available within `files_modified: tools/check_repo.py` alone (the plan scopes this file exclusively). RED/GREEN were pinned via the plan's own `<verify>`/`<acceptance_criteria>` commands, run against the unmodified file before implementation and again after:

- **RED (before any edit):** `python3 tools/check_repo.py --mutation-test | grep -c 'discrimination-proven'` printed `0`; `grep -c 'codes proven live' tools/check_repo.py` printed `1`. Both confirm the target behavior was absent.
- **GREEN (after the edit):** the same two commands printed `1` and `0` respectively (see command output below), and all other Task 1 acceptance criteria (21 `mutation-test OK` lines, CONTROL `0 unexpected`, self-test/live-check green) passed on the first implementation.

No `test(...)` commit was created separately from the `feat(...)` commit, since there is no isolated test artifact to commit ahead of the implementation in this single-file, self-verifying tool. This is a deliberate, documented deviation from the literal RED-commit-then-GREEN-commit sequence, not a skipped verification step — the behavior was demonstrably pinned both before and after.

## RED/GREEN Command Evidence

```
== RED (before Task 1 edit) ==
$ python3 tools/check_repo.py --mutation-test | grep -c 'discrimination-proven'
0
$ grep -c 'codes proven live' tools/check_repo.py
1

== GREEN (after Task 1 edit) ==
$ python3 tools/check_repo.py --mutation-test | grep -c 'discrimination-proven'
1
$ grep -c 'codes proven live' tools/check_repo.py
0
```

## Fire-Only Branch Proof

Run in-process against a deliberately over-ceiling scratch copy (a temp directory, never committed), by monkeypatching `check_repo.REPO_ROOT` to the scratch root and invoking `mutation_test()` directly:

```
mutation-test CONTROL: 1 violations on the unmutated copy (1 known-open per KNOWN_OPEN_VIOLATIONS, 0 unexpected)
... (20 mutation-test OK lines) ...
mutation-test FIRE-ONLY: skill-token-budget-exceeded append filler words to the real skills/proof-first/SKILL.md, an under-ceiling control, pushing its estimated token count over the ceiling (the control copy was already non-clean for this code, so this mutation cannot demonstrate discrimination between good content and bad)
mutation-test PASS: 20 codes discrimination-proven
mutation-test PASS: 1 codes confirmed-fire-only, not discrimination-proven (skill-token-budget-exceeded) -- see the FIRE-ONLY line above for each one's reason
RETURN all_ok: True
```

This confirms the fire-only branch executes (not dead code) and that a confirmed-fire-only code does not by itself fail the run — `all_ok` stayed `True`.

## No-Op Inversion Proof

`_mutate_skill_token_budget_exceeded`'s body was temporarily replaced with `pass` (a pure no-op — the direct scenario 02-REVIEW.md CR-01 used to prove the pre-Task-1 code was vacuous for this one code), the mutation-test re-run, and the original body restored immediately after:

```
mutation-test FAIL: skill-token-budget-exceeded append filler words to the real skills/proof-first/SKILL.md, an under-ceiling control, pushing its estimated token count over the ceiling
mutation-test FAILED: 1 codes not discrimination-proven
```

This is the direct inverse of CR-01's result (which reported this code as `OK`/proven under the same no-op substitution): the code was never fired at all (not even fire-only), so it correctly falls into the "not fired" failure branch. After restoring the real body, `python3 tools/check_repo.py --mutation-test` again printed `mutation-test PASS: 21 codes discrimination-proven`.

## Decisions Made

See `key-decisions` in the frontmatter above:
- Single control run reused as pre-state for all 21 mutations (no doubled work).
- `KNOWN_OPEN_VIOLATIONS` filter expression in `mutation_test()` left unchanged — an empty set already makes it an unweakened assertion, and the plan explicitly instructed not to reshape it without a live case.
- TDD gate satisfied via before/after behavior-pinning against the plan's own verify commands rather than a separate committed test file, documented above.

## Deviations from Plan

None — plan executed exactly as written. The TDD-gate interpretation above is documented as a compliance note (see "TDD Gate Compliance"), not a deviation from the plan's `<action>`/`<acceptance_criteria>` content, all of which were met exactly as specified.

## Issues Encountered

None.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- 02-VERIFICATION.md gap 3 is closed: `--mutation-test`'s headline number is now discrimination-proven, not a blended firing count, and this holds independent of `skills/proof-first/SKILL.md`'s current word count — a future drift back over the token ceiling would automatically degrade the printed claim (one code moving from discrimination-proven to confirmed-fire-only) rather than silently invalidating it.
- 02-REVIEW.md CR-01 is closed: the mutation for `skill-token-budget-exceeded` is now genuinely discriminating against the current under-ceiling control, and the no-op-substitution inversion proof confirms the tool would catch a regression back to the pre-02-07 vacuous state.
- 02-REVIEW.md CR-02 is closed: the `frontmatter-description-invalid` docstring matches observed behavior, confirmed by a fixture.
- 02-REVIEW.md WR-01 is closed by construction: `KNOWN_OPEN_VIOLATIONS` is empty, and its comment prevents a future bare-code re-introduction of the same latent risk.
- All 21 violation codes remain covered — no code lost its mutation or its proof; coverage did not shrink to buy honesty.
- `.github/workflows/ci.yml` needed no change — the existing three-command job order already runs the tightened mode.
- Remaining open `.planning/WINDOWS.md` items (ids 3 and 4) are untouched by this plan and remain routed to 02-09 / end-of-phase UAT, per 02-07's own summary.

---
*Phase: 02-rule-catalog-integrity-skill-md-core*
*Completed: 2026-09-11*

## Self-Check: PASSED

- FOUND: `tools/check_repo.py` (modified, present)
- FOUND: commit `493853d`
- FOUND: commit `f04e298`
