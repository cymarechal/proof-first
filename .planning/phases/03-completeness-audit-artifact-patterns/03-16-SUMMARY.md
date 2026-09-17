---
phase: 03-completeness-audit-artifact-patterns
plan: 16
subsystem: testing
tags: [self-test, mutation-testing, verification-integrity, conformance-harness, python]

# Dependency graph
requires:
  - phase: 03-13
    provides: run_matrix()/_write_result_line() per-session durability fix and behavior case 11 (the guard this plan repairs)
  - phase: 03-14
    provides: results-breakdown-count-mismatch check and 03-REVIEW.md's round-5 review that raised CR-01
  - phase: 03-15
    provides: MOD-04's v1 disposition decision (accept-and-disclose), which this plan does not reopen
provides:
  - A behavior case 11 that genuinely discriminates _write_result_line()'s flush call, proven in both directions by a one-time mutation probe
  - Corrected verification-integrity statements in run_conformance.py's docstring and RESULTS-mod04.md
  - _copy_repo_subset()'s docstring made internally consistent (IN-01)
  - README's decline named in the same term as RESULTS-mod04.md and WINDOWS.md (IN-02)
  - WINDOWS.md entry 10 tracking the defect as fixed
affects: [phase-05-eval-harness]

# Actuals (#2632) — pairs with the plan's estimate to calibrate future estimates.
actuals:
  tokens: 6350
  tasks: 3
  commits: 3

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Self-test-only call-recording proxy (_FlushTrackingHandle) with no __getattr__ delegation, so any access path other than the one under test raises loudly instead of being silently forwarded"
    - "Both-directions discrimination probe (mutate a sibling copy, assert it fails; run the real file, assert it passes) as the in-repo standard for a regression guard, mirroring tools/check_repo.py --mutation-test's CONTROL/FIRE precedent"

key-files:
  created: []
  modified:
    - evals/conformance/run_conformance.py
    - evals/conformance/RESULTS-mod04.md
    - tools/check_repo.py
    - README.md
    - .planning/WINDOWS.md

key-decisions:
  - "Rewrote case 11 to assert the exact recorded call sequence (['write', 'flush', 'write', 'flush']) rather than a positional pairing of alternating slices, because a positional pairing would silently truncate an odd-length list and miss a trailing unflushed write."
  - "Recorded WINDOWS.md entry 10 as fixed, not open, because the defect it names (case 11's non-discrimination) is genuinely closed and proven closed by this plan's both-directions probe; the narrower one-time-probe residual is disclosed inside the entry's own description rather than parked as a second open ledger item."
  - "Left .planning/REQUIREMENTS.md checkboxes for AUD-02/AUD-03/MOD-03/MOD-05/MOD-04 untouched, per the plan's explicit prohibition -- re-marking them is the verifier's task, done only once the phase verifies clean. requirements-completed below is empty for that reason, not because nothing was accomplished."

patterns-established:
  - "A regression guard for a durability property must assert the exact write/flush call sequence on a recording proxy plus a pre-close read of the artifact, not merely 'is it readable after close()' -- the latter is satisfied by any context manager's own close()-on-exit regardless of whether the guarded flush call ran at all."

requirements-completed: []

coverage:
  - id: D1
    description: "Behavior case 11 discriminates _write_result_line()'s flush call in both directions: silent against the real file, firing with a named FAIL: line against a mutated sibling copy with the flush call removed"
    verification:
      - kind: unit
        ref: "evals/conformance/run_conformance.py --self-test (behavior case 11, real file)"
        status: pass
      - kind: unit
        ref: "evals/conformance/_flush_probe_tmp.py --self-test (mutated sibling copy, run then deleted, never committed)"
        status: pass
    human_judgment: false
  - id: D2
    description: "Module docstring and RESULTS-mod04.md no longer credit case 11 with a proof it did not perform; a new dated Self-test discrimination correction (03-16) section records the defect, provenance, fix, probe, and residual"
    verification:
      - kind: other
        ref: "grep -c 'proved offline by' evals/conformance/run_conformance.py == 0; grep -c 'proves this' evals/conformance/RESULTS-mod04.md == 0; grep -c '^## Self-test discrimination correction (03-16)' evals/conformance/RESULTS-mod04.md == 1"
        status: pass
    human_judgment: false
  - id: D3
    description: "_copy_repo_subset()'s docstring no longer contradicts itself about which check reads under evals/ (IN-01); README names the 10-point movement a decline (IN-02); WINDOWS.md entry 10 tracks the defect as fixed with the ledger's table/JSON/counters in agreement"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --mutation-test (32 codes discrimination-proven, unchanged); python3 -c 'json parse .planning/WINDOWS.md' (entries=10 fixed=6 open=3 waived=1)"
        status: pass
    human_judgment: false

duration: ~25 min
completed: 2026-09-17
status: complete
---

# Phase 03 Plan 16: Self-test discrimination fix for `_write_result_line()`'s durability guard Summary

**Rewrote `evals/conformance/run_conformance.py`'s behavior case 11 to genuinely discriminate `_write_result_line()`'s flush call via a call-recording proxy handle, proved it in both directions with a one-time mutation probe, corrected the two documents that overclaimed the old test's proof, and tracked the defect fixed in `.planning/WINDOWS.md`.**

## Performance

- **Duration:** ~25 min
- **Tasks:** 3
- **Files modified:** 5 (`evals/conformance/run_conformance.py`, `evals/conformance/RESULTS-mod04.md`, `tools/check_repo.py`, `README.md`, `.planning/WINDOWS.md`)

## Accomplishments

- `_FlushTrackingHandle` (a self-test-only proxy defining only `write`/`flush`, no `__getattr__`) records call order; behavior case 11 now asserts the recorded sequence is exactly `['write', 'flush', 'write', 'flush']` plus a pre-close read of the results file showing two `verdict=conformant` lines already on disk.
- Ran the discrimination probe: the real file's `--self-test` stays clean; a mutated sibling copy with the single flush call removed fails with a named `FAIL: behavior case 11` line. Both transcripts below are the plan's headline evidence.
- Corrected the module docstring's `Durability guarantee:` parenthetical and `RESULTS-mod04.md`'s `## Instrument durability fix (03-13)` section, and appended a new `## Self-test discrimination correction (03-16)` section recording the defect, both independent reproductions (03-REVIEW.md CR-01, 03-VERIFICATION.md's verifier), the fix, the probe, and the disclosed residual.
- Closed `03-REVIEW.md` IN-01 (`_copy_repo_subset()`'s self-contradictory docstring) and IN-02 (README never named the 10-point movement a decline).
- Recorded `.planning/WINDOWS.md` entry 10 (self-test non-discrimination defect) as `fixed` via the `gsd-tools windows` CLI; ledger now holds 10 entries (6 fixed, 3 open, 1 waived).

## Task Commits

Each task was committed atomically:

1. **Task 1: Make behavior case 11 fail when the flush call is removed, and prove it in both directions** — `53ce63a` (fix)
2. **Task 2: Correct the two statements that claim case 11 proved a property it did not** — `d744b3c` (docs)
3. **Task 3: Close the two consistency findings and track the defect in the ledger** — `82535c7` (fix)

## The Both-Directions Discrimination Probe — Verbatim Transcripts

Run after all three tasks landed, from the repository root.

**Real file — clean pass, no `FAIL:` line:**

```
$ python3 evals/conformance/run_conformance.py --self-test
self-test PASS - verdicts discriminated: conformant, no-family, rule-before-family, unscoreable
real_exit=0
```

**Building the mutated sibling copy (single flush statement removed):**

```
$ grep -v '^    handle\.flush()$' evals/conformance/run_conformance.py > evals/conformance/_flush_probe_tmp.py
$ python3 -c "a=len(open('evals/conformance/run_conformance.py').read().splitlines());b=len(open('evals/conformance/_flush_probe_tmp.py').read().splitlines());print('probe_delta=%d'%(a-b))"
probe_delta=1
```

**Mutated copy — non-zero exit, named `FAIL:` line for case 11:**

```
$ python3 evals/conformance/_flush_probe_tmp.py --self-test
FAIL: behavior case 11 (durability on interruption) expected recorded call sequence ['write', 'flush', 'write', 'flush'], actual ['write', 'write']
probe_exit=1
```

**Cleanup — probe copy deleted, tree clean:**

```
$ rm -f evals/conformance/_flush_probe_tmp.py
$ git status --porcelain
(no output)
```

This is exactly the plan's central success condition: deleting `handle.flush()` from `_write_result_line()` makes `--self-test` FAIL, naming case 11 — proven, not merely asserted.

## All Four CI Gate Commands (post-landing)

```
$ python3 tools/check_repo.py --self-test
self-test PASS - verified violation codes: artifact-family-section-missing, catalog-count-mismatch,
catalog-count-unstated, catalog-id-drift, catalog-opening-rule-count, dup-figure-key, dup-id,
figure-order, framework-statement-missing, frontmatter-description-invalid, frontmatter-name-mismatch,
frontmatter-unknown-key, frontmatter-unparseable, license-missing, mc-catalog-id-drift,
mc-count-mismatch, mc-count-unstated, mc-rule-in-skill, pointer-duplicated, pointer-missing,
pointer-unparseable, range-id, readme-results-pointer-missing, results-breakdown-count-mismatch,
revived-id, skill-family-line-gate-missing, skill-family-order-gate-missing,
skill-token-budget-exceeded, skill-too-long, source-label-in-skill-content, undefined-id,
unlisted-figure
exit=0

$ python3 tools/check_repo.py --mutation-test
[...32 named mutations, each "mutation-test OK: ..."...]
mutation-test PASS: 32 codes discrimination-proven
exit=0

$ python3 tools/check_repo.py
check_repo: 0 violations
exit=0

$ python3 evals/conformance/run_conformance.py --self-test
self-test PASS - verdicts discriminated: conformant, no-family, rule-before-family, unscoreable
exit=0
```

## Scope Confirmation

```
$ git diff --stat HEAD~3..HEAD
 .planning/WINDOWS.md                 |  19 ++++++-
 README.md                            |  19 ++++---
 evals/conformance/RESULTS-mod04.md   |  42 +++++++++++++-
 evals/conformance/run_conformance.py | 106 +++++++++++++++++++++++++++--------
 tools/check_repo.py                  |   9 +--
 5 files changed, 154 insertions(+), 41 deletions(-)

$ git diff HEAD~3..HEAD -- skills/ .planning/REQUIREMENTS.md .planning/phases/03-completeness-audit-artifact-patterns/03-UAT.md
(no output)

$ git diff HEAD~3..HEAD -- evals/conformance/run_conformance.py -- (hunk headers only)
@@ -32,11 +32,21 @@ Usage:                     <- docstring parenthetical (Task 2)
@@ -267,6 +277,33 @@ def _decode_stream(value):  <- new _FlushTrackingHandle class, before self_test() (Task 1)
@@ -598,16 +635,27 @@ def self_test():            <- case 11 comment + setup (Task 1)
@@ -628,7 +676,9 @@ def self_test():
@@ -637,28 +687,40 @@ def self_test():            <- case 11 assertions (Task 1)

$ git status --porcelain
(no output)
```

No hunk touches `score_transcript()`, `run_session()`, `run_matrix()`, or `_write_result_line()`. `evals/conformance/_flush_probe_tmp.py` does not exist.

## Files Created/Modified

- `evals/conformance/run_conformance.py` — added `_FlushTrackingHandle`; rewrote behavior case 11 to assert the recorded write-then-flush call sequence plus a pre-close read; corrected the module docstring's `Durability guarantee:` parenthetical
- `evals/conformance/RESULTS-mod04.md` — corrected the `**The fix.**` sentence in `## Instrument durability fix (03-13)`; appended `## Self-test discrimination correction (03-16)`
- `tools/check_repo.py` — `_copy_repo_subset()`'s docstring now names `results-breakdown-count-mismatch` as the one check reading under `evals/`, instead of asserting no check does (comment-only, `MUTATION_SOURCES` unchanged)
- `README.md` — Status paragraph now names the 10-point movement a decline; every figure preserved verbatim
- `.planning/WINDOWS.md` — new entry 10 (self-test non-discrimination defect), recorded `fixed`

## Decisions Made

- Asserted the exact recorded call sequence (`==` against the full list) rather than a positional pairing of alternating write/flush slices — the plan's `key_links` flagged that a positional pairing silently truncates an odd-length list and would miss a final unflushed write, which is precisely the failure mode this guard exists to catch.
- Recorded WINDOWS.md entry 10 as `fixed` rather than `open`: the defect it names is genuinely closed and proven closed by the both-directions probe above; the disclosed residual (no committed mutation harness for this instrument, unlike `tools/check_repo.py --mutation-test`) lives inside the entry's own description and is routed to Phase 5, not parked as a second manufactured open item.
- `requirements-completed` is empty and no `.planning/REQUIREMENTS.md` checkbox was touched, per the plan's explicit prohibition: re-marking AUD-02, AUD-03, MOD-03, and MOD-05 is the verifier's task, done only once the phase verifies clean. MOD-04 stays unchecked permanently for v1 — this plan repairs the instrument that produced MOD-04's figure, it does not satisfy the requirement.

## Deviations from Plan

None — plan executed exactly as written. All acceptance criteria and verify commands passed on the first attempt for every task; no auto-fix, blocker, or architectural deviation was required.

## Issues Encountered

None.

## Known Stubs

None.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- `03-VERIFICATION.md`'s Truth 10 is closed: the discrimination probe fires in both directions, verbatim above.
- No published MOD-04 figure moved: `N_A = 3, M_A = 10` (30.0%), `N_B = 4, M_B = 10` (40.0%), the -10.0pp delta, and `2026-09-16` are unchanged everywhere.
- `.planning/WINDOWS.md` is at 10 entries (6 fixed, 3 open, 1 waived), JSON block parses cleanly.
- `MOD-04` stays `[ ]`, permanently, for v1. Ready for `/gsd-verify-work 03` to re-check the phase's other gap-closure plans and, if clean, re-mark AUD-02/AUD-03/MOD-03/MOD-05.

## Self-Check: PASSED

- `evals/conformance/run_conformance.py` exists and contains `_FlushTrackingHandle`: confirmed (`grep -c '^class _FlushTrackingHandle'` == 1).
- `evals/conformance/RESULTS-mod04.md` contains the new section: confirmed (`grep -c '^## Self-test discrimination correction (03-16)'` == 1).
- `tools/check_repo.py` docstring corrected: confirmed (`grep -c 'No check other than'` == 1, `grep -c 'No existing check reads anything under'` == 0).
- `README.md` names the decline: confirmed (`grep -c 'decline'` == 1), all figures preserved (verified counts above).
- `.planning/WINDOWS.md` holds 10 entries, 6 fixed/3 open/1 waived, JSON parses: confirmed.
- All three task commits exist: `git log --oneline --all` shows `53ce63a`, `d744b3c`, `82535c7`.
- All four CI gate commands exit `0`: confirmed above.
- Both-directions discrimination probe fired as required: confirmed, transcripts above.
- `git status --porcelain` is clean, no probe file survives: confirmed.
- No `.planning/REQUIREMENTS.md` or `skills/` file touched: confirmed (`git diff --name-only HEAD~3..HEAD -- .planning/REQUIREMENTS.md skills/` empty).

---
*Phase: 03-completeness-audit-artifact-patterns*
*Completed: 2026-09-17*
