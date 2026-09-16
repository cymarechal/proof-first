---
phase: 03-completeness-audit-artifact-patterns
plan: 10
subsystem: testing
tags: [check-repo, mutation-test, readme, cr-02, stdlib]

# Dependency graph
requires:
  - phase: 03-completeness-audit-artifact-patterns
    provides: evals/conformance/RESULTS-mod04.md (03-06..03-09), 03-REVIEW.md's CR-02 finding
provides:
  - readme-results-pointer-missing, a discrimination-proven check_repo.py code
    that fails the build if README.md ever again stops pointing at the
    committed MOD-04 measurement
  - A README.md Status section, layout tree, and inventory that are true as
    of this phase's own commits (CR-02 closed)
affects: [Phase 6 (LEG-04/LEG-05 README claim review), any future README edit]

# Actuals (#2632)
actuals:
  tokens: 3425
  tasks: 2
  commits: 2

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A repository-level documentation check (scans README.md directly, not
       gated on NUMBERING.md or a skills/*/SKILL.md path) gets its own
       README_CHECK_CODES list and run_readme_checks() function, kept out of
       CATALOG_CHECK_CODES which is reserved for skill-folder-scoped checks."
    - "A check whose target file (README.md) is absent from some self-test
       fixture roots skips silently on absence rather than firing, matching
       this checker's established posture for every other optional-file
       check (license-missing is the one deliberate exception, and it is a
       different code with a different job)."

key-files:
  created: []
  modified:
    - tools/check_repo.py
    - README.md

key-decisions:
  - "check_readme_results_pointer() returns no violation when README.md
     itself does not exist, mirroring the established pattern for optional
     files elsewhere in this checker -- the missing-file case is a
     different, unrelated failure mode this check does not own, and no
     self-test fixture root in the suite ships a bare repo with zero files."
  - "The new pointer sentence added to README's Status section in Task 1 is
     deliberately worded differently from the canonical NOTICES.md
     attribution pointer string, so pointer-missing/pointer-duplicated's
     exactly-one invariant over that separate, older pointer stays intact --
     per the plan's own assumption_delta_decision (add-alongside, not a
     merged pointer registry)."
  - "No percentage figure from RESULTS-mod04.md is reproduced in README.md.
     The Status section names the file and carries forward four of its
     caveats in prose (Anthropic-only models, no harness determinism,
     unequal arm sample sizes, the CR-01 scorer-anchoring correction) so a
     reader is warned before following the pointer, without creating a
     second place for the same number to go stale."

patterns-established:
  - "A mechanical guard (a new check_repo.py code) is added before the prose
     fix it protects, so the same claim cannot silently regress the next
     time a measurement file changes -- mirrors this phase's established
     precedent of closing defect classes, not just today's instance."

requirements-completed: []

coverage:
  - id: D1
    description: "readme-results-pointer-missing fires exactly once, naming README.md, when the literal path evals/conformance/RESULTS-mod04.md is absent from README.md; is silent when present; is registered in ALL_CHECK_CODES and self-tested in both directions; and is discrimination-proven against the real repository by --mutation-test (29 -> 30 codes)."
    requirement: "MOD-04"
    verification:
      - kind: unit
        ref: "tools/check_repo.py self_test() readme_good_root/readme_bad_root fixture pair"
        status: pass
      - kind: integration
        ref: "python3 tools/check_repo.py --self-test"
        status: pass
      - kind: integration
        ref: "python3 tools/check_repo.py --mutation-test (final line: mutation-test PASS: 30 codes discrimination-proven; readme-results-pointer-missing line reads mutation-test OK:)"
        status: pass
      - kind: integration
        ref: "python3 tools/check_repo.py (live run, plain check_repo: 0 violations)"
        status: pass
    human_judgment: false
  - id: D2
    description: "README.md's Status section, repository-layout tree, and what-exists-today/what-does-not-exist-yet lists are true as of this phase's own commits: the section names evals/conformance/RESULTS-mod04.md, carries at least three of its caveats, states no percentage, and attributes the still-unrun persuasion benchmark to Phase 5 rather than to the MOD-04 conformance measurement; the tree shows evals/conformance/ with run_conformance.py, fixtures/, transcripts/, and RESULTS-mod04.md, each marked (exists)."
    requirement: "MOD-04"
    verification:
      - kind: other
        ref: "grep -c 'evals/conformance' README.md == 4; python3 -c pointer-in-status probe from the plan's <verify> block prints POINTER_IN_STATUS"
        status: pass
      - kind: integration
        ref: "python3 tools/check_repo.py (0 violations) and --mutation-test (30 codes discrimination-proven) re-run after the README rewrite"
        status: pass
    human_judgment: false
  - id: D3
    description: "This plan closes no requirement: MOD-04 stays [ ] in REQUIREMENTS.md, WINDOWS.md entry 8 stays open, and no REQUIREMENTS.md checkbox reads [x] next to UNVERIFIED."
    verification:
      - kind: integration
        ref: "grep -c \"^- \\[x\\].*UNVERIFIED\" .planning/REQUIREMENTS.md == 0; grep -n 'MOD-04' .planning/REQUIREMENTS.md shows the line still opens with - [ ]; WINDOWS.md entry 8's status field still reads open"
        status: pass
    human_judgment: false

duration: 8min
completed: 2026-09-16
status: complete
---

# Phase 3 Plan 10: Close CR-02 — README's Status section, layout tree, and inventory are now true, guarded by a 30th discrimination-proven check

**README no longer claims "no measured claim is published in this repository yet" while `evals/conformance/RESULTS-mod04.md` sits uncited two paragraphs away — a new `readme-results-pointer-missing` check makes the regression a build failure, not just a prose fix.**

## Performance

- **Duration:** 8 min
- **Started:** 2026-09-16T05:51:32Z
- **Completed:** 2026-09-16T05:59:01Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Added `check_readme_results_pointer()` to `tools/check_repo.py`: fires `readme-results-pointer-missing` naming `README.md` when the literal path `evals/conformance/RESULTS-mod04.md` is absent from it, unconditionally (not gated on that file existing on disk). Registered in `ALL_CHECK_CODES`, self-tested in both directions via a dedicated `readme_good_root`/`readme_bad_root` fixture pair, and discrimination-proven against the real repository by `--mutation-test` — the total rose from 29 to 30 codes discrimination-proven.
- Added a minimal pointer sentence to README's Status section (Task 1) naming `evals/conformance/RESULTS-mod04.md`, distinct in wording from the canonical NOTICES.md attribution pointer so `pointer-missing`/`pointer-duplicated`'s exactly-one invariant over that separate string is untouched.
- Rewrote README's Status section (Task 2) to state the repository's actual position: one MOD-04 write-mode conformance measurement exists, reproducible from the committed `evals/conformance/run_conformance.py`, with four of its caveats carried forward in prose (Anthropic-hosted models only, no harness determinism, unequal arm sample sizes, the CR-01 scorer-anchoring correction making every pre-fix figure an optimistic, unrecoverable ceiling) — and no percentage figure reproduced in README.
- Made the forward-looking sentence specific: the skill-on/skill-off, multi-model, judge-scored persuasion benchmark this README will eventually cite is Phase 5's and has not run — distinct from the MOD-04 conformance measurement that does exist, so the two are never conflated.
- Added `evals/conformance/` to the repository-layout tree (`run_conformance.py`, `fixtures/`, `transcripts/`, `RESULTS-mod04.md`, each marked `(exists)`) and two entries to the what-exists-today list; reworded the what-does-not-exist-yet benchmark bullet to name Phase 5 specifically.

## Task Commits

1. **Task 1: Add `readme-results-pointer-missing` and prove it end-to-end from self-test through mutation-test to a green live run** - `90a6cba` (fix)
2. **Task 2: Make README's Status section, layout tree, and inventory true as of this phase's commits** - `baec853` (docs)

_Task 1 is `type="tracer"`. Its own `<verify>` (self-test, mutation-test, live run, pointer grep) was re-run end-to-end as the tracer feedback gate before Task 2 started — all passed (`HUMAN_VERIFY_MODE=end-of-phase`, no `<human-check>` in the tracer's `<verify>`, so this is the automated re-run-then-continue path, no checkpoint synthesized)._

## Files Created/Modified
- `tools/check_repo.py` - new `check_readme_results_pointer()`, `README_RESULTS_POINTER` constant, `README_CHECK_CODES`, `run_readme_checks()`, `_mutate_readme_results_pointer_missing()`, a `MUTATIONS` entry, a self-test fixture pair (`readme_good_root`/`readme_bad_root`) with matching assertions, `ALL_CHECK_CODES`/`run_all_checks()` wiring, and a Declared-ceiling docstring entry
- `README.md` - Status section rewritten (names the measurement file, carries its caveats, no percentage, attributes the persuasion benchmark to Phase 5); repository-layout tree gained `evals/conformance/` with four `(exists)`-marked entries; what-exists-today/what-does-not-exist-yet lists updated

## Decisions Made
- `check_readme_results_pointer()` returns no violation when README.md itself is absent, matching this checker's established posture for optional files elsewhere (mc-catalog-id-drift, artifact-family-section-missing, etc.) — the missing-README case is a different, unrelated failure this check does not own.
- The new Status-section pointer sentence is worded distinctly from the canonical NOTICES.md attribution pointer string, per the plan's own `assumption_delta_decision` (add-alongside): the two pointers are counted by separate codes with separate cardinality rules, and merging them into one registry would be the wrong move.
- No percentage from `RESULTS-mod04.md` is copied into README — the Status section points at the file and states its caveats in prose instead, so there is no second place for the same figure to go stale (the exact mechanism that produced CR-02).

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- CR-02 is closed: README's Status section, layout tree, and inventory are now true as of this phase's commits, and a discrimination-proven check (30th code) prevents the same claim from silently regressing.
- `MOD-04` stays `[ ]`, `WINDOWS.md` entry 8 stays `open` — this plan fixes documentation and a build guard, not the underlying MOD-04 residual (rule-before-family sessions). That closure still needs a lever other than instruction wording, per entry 8's own pre-committed rule.
- No blockers for subsequent Phase 3 plans or Phase 6's LEG-04/LEG-05 README claim review.

## Self-Check: PASSED

- `git log --oneline --all | grep -q 90a6cba` → FOUND
- `git log --oneline --all | grep -q baec853` → FOUND
- Re-ran all plan-level `<verification>` commands: `check_repo.py --self-test` → PASS (verified codes include `readme-results-pointer-missing`); `--mutation-test` → `mutation-test PASS: 30 codes discrimination-proven`; plain `check_repo.py` → `check_repo: 0 violations`; `run_conformance.py --self-test` → `self-test PASS - verdicts discriminated: conformant, no-family, rule-before-family, unscoreable`.
- `grep -c 'evals/conformance/RESULTS-mod04.md' README.md` → `1` (Task 1 gate); `grep -c 'evals/conformance' README.md` → `4` (Task 2 gate, >= 4 required).
- Pointer-in-Status probe → `POINTER_IN_STATUS`.
- `grep -c "^- \[x\].*UNVERIFIED" .planning/REQUIREMENTS.md` → `0`.
- MOD-04's REQUIREMENTS.md row still opens `- [ ]`; WINDOWS.md entry 8's status field still reads `open`.

---
*Phase: 03-completeness-audit-artifact-patterns*
*Completed: 2026-09-16*
