---
phase: 04-distribution-worked-examples
plan: 07
subsystem: tooling
tags: [python, regex, mutation-testing, ci, stdlib, linting]

# Dependency graph
requires:
  - phase: 04-distribution-worked-examples (04-05, 04-06)
    provides: "Clean ✓ columns in examples/before-after.md (04-05) and skills/proof-first/references/worked-examples.md (04-06) obeying PF-4.1, narrating no rule, and inventing no count -- the base this plan's three new codes check against."
provides:
  - "example-sentence-length -- PF-4.1's 25-word ceiling enforced over both example files' ✓ columns as a build failure"
  - "before-after-spelled-count -- word-spelled counts (two through twelve) in examples/before-after.md's ✗/✓ lines fail the build, closing the word-spelled half of unlisted-figure's own disclosed bare-count hole"
  - "example-rule-narration -- an explicitly-labelled proxy for SKILL.md line 261's 'No list of applied rules follows the prose', catching a contrastive connective paired with the catalog's own rejected-alternative vocabulary"
  - "tools/check_repo.py --mutation-test now reports 44 codes discrimination-proven, up from 41"
affects: ["04-11 (phase-end verification, files the disclosed narration-by-self-reference residual)", "Phase 6 LEG-04 (legal review gate)"]

# Actuals (#2632)
actuals:
  tokens: 8949
  tasks: 3
  commits: 3

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Three-part violation-code contract (check function + self-test fixture pair + registered MUTATIONS entry) extended three more times without touching the frozen interfaces (BEFORE_AFTER_PATH, ARTIFACT_FAMILY_SECTIONS, strip_fences, split_sections, table_rows)"
    - "check_text optional kwarg on _before_after_section lets new fixtures override just the ✓ line's text while every existing call site keeps its original five-word default, unchanged"

key-files:
  created: []
  modified:
    - tools/check_repo.py
    - .planning/REQUIREMENTS.md
    - .planning/WINDOWS.md

key-decisions:
  - "Corrected the plan's own interfaces-block measurements before writing them into the shipped docstring: examples/deal-brief.md's word-spelled-cardinal count is 13 (not 12), and skills/proof-first/references/worked-examples.md's is 5 (not 3), both measured directly with the exact SPELLED_CARDINAL_RE the shipped code uses. Filed as WINDOWS.md id 14 (deviation), matching the 03-04/04-01/04-04 precedent of documenting plan-authored measurement errors rather than force-fitting shipped content to them. No scope or behavior changed -- both files remain out of before-after-spelled-count's scan regardless."
  - "Did not run requirements mark-complete for EX-02, even though gsd-tools requirements ready-ids reported it mechanically ready (04-07 is the last sibling plan declaring EX-02 in this phase). REQUIREMENTS.md's own EX-02 note explicitly states 'Do not re-mark Complete from a SUMMARY's requirements-completed field' and names five gaps (G-04-1 through G-04-5) plus two more (G-04-6/G-04-7) as the closure condition. This plan mechanizes three (G-04-1, G-04-2, G-04-4); G-04-3/G-04-5 stay disclosed semantic backstop truths and G-04-6/G-04-7 belong to 04-08/04-09/04-10, none of which have executed yet. Updated the REQUIREMENTS.md note in place to record the mechanization progress without flipping the checkbox."

requirements-completed: [EX-02]

coverage:
  - id: D1
    description: "example-sentence-length registered end to end: check function, EXAMPLE_PROSE_PATHS/PF41_WORD_CEILING constants, declared-ceiling docstring (both module-level bullet and function docstring), firing fixtures for both scan paths (examples/before-after.md and worked-examples.md), silent on the good fixture and on a root shipping neither file, registered MUTATIONS entry"
    requirement: "EX-02"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --self-test (verified-codes list contains example-sentence-length, 42 entries)"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py --mutation-test (42 codes discrimination-proven, 0 unexpected CONTROL, no FIRE-ONLY)"
        status: pass
    human_judgment: false
  - id: D2
    description: "before-after-spelled-count registered: SPELLED_CARDINAL_RE, check function scoped to examples/before-after.md's ✗/✓ lines only, two-token proper-noun exemption, declared-ceiling docstring naming both out-of-scope files and their measured counts, fixture exercising both the firing path and the exemption, registered MUTATIONS entry, and an assertion that the code stays silent on a root shipping the real examples/deal-brief.md"
    requirement: "EX-02"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --self-test (verified-codes list contains before-after-spelled-count, 43 entries)"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py --mutation-test (43 codes discrimination-proven, 0 unexpected CONTROL, no FIRE-ONLY)"
        status: pass
    human_judgment: false
  - id: D3
    description: "example-rule-narration registered as an explicitly-labelled proxy: NARRATION_CONNECTIVE_RE/NARRATION_META_TERMS/NARRATION_WINDOW_CHARS, check function scanning both example files' ✓ lines, docstring naming the self-reference narration shape it cannot detect, fixture exercising both the firing path and the deliberate silence on an unlisted term, registered MUTATIONS entry"
    requirement: "EX-02"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --self-test (verified-codes list contains example-rule-narration, 44 entries)"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py --mutation-test (44 codes discrimination-proven, 0 unexpected CONTROL, no FIRE-ONLY); python3 tools/generate_derivatives.py --check (clean)"
        status: pass
    human_judgment: true
    rationale: "example-rule-narration's own docstring discloses that it is a proxy, not a verdict, on SKILL.md line 261 -- whether the catalog's narration prohibition is genuinely upheld (beyond this one listed-connective-plus-listed-term signature) stays a human judgment carried forward as a verification: backstop truth, per this plan's must_haves."

# Metrics
duration: 55min
completed: 2026-09-17
status: complete
---

# Phase 4 Plan 07: Mechanize the three UAT-found example defect classes Summary

**Three new discrimination-proven `check_repo.py` codes (`example-sentence-length`, `before-after-spelled-count`, `example-rule-narration`) turn `04-UAT.md`'s three mechanizable prose defects into CI build failures, moving the gate from 41 to 44 codes with zero content edits.**

## Performance

- **Duration:** 55 min
- **Started:** 2026-09-17T09:58:00Z (approx.)
- **Completed:** 2026-09-17T10:53:00Z (approx.)
- **Tasks:** 3
- **Files modified:** 1 (`tools/check_repo.py`); plus standard workflow artifacts (`REQUIREMENTS.md`, `WINDOWS.md`, `STATE.md`, `ROADMAP.md`)

## Accomplishments

- `example-sentence-length` enforces PF-4.1's 25-word ceiling over the ✓ columns of both `examples/before-after.md` and `skills/proof-first/references/worked-examples.md`, proven live against both scan paths by two dedicated fixtures.
- `before-after-spelled-count` fails the build on a word-spelled cardinal (two through twelve) in `examples/before-after.md`'s ✗/✓ lines, closing the word-spelled half of `unlisted-figure`'s own disclosed bare-count hole, with a two-token proper-noun exemption proven not to swallow genuine violations.
- `example-rule-narration` gives SKILL.md line 261's "No list of applied rules follows the prose" its first mechanical enforcement, explicitly labelled in its own docstring as a proxy — not a verdict — and naming the one narration shape (self-reference to the document's own ordering) it cannot detect.
- `python3 tools/check_repo.py --mutation-test` reports **44 codes discrimination-proven** (up from 41), `0 unexpected` on CONTROL, no FIRE-ONLY line. The live run stays `check_repo: 0 violations` and `generate_derivatives.py --check` stays clean throughout — no content in `examples/before-after.md`, `worked-examples.md`, `SKILL.md`, or `README.md` was touched.

## Task Commits

Each task was committed atomically:

1. **Task 1: Register example-sentence-length end to end — check, fixtures, mutation, 41 to 42 codes** - `840c6f5` (feat)
2. **Task 2: Register before-after-spelled-count — 42 to 43 codes** - `fd1b17b` (feat)
3. **Task 3: Register example-rule-narration as a labelled proxy — 43 to 44 codes** - `28a45ac` (feat)

**Plan metadata:** committed separately after this SUMMARY.

## Files Created/Modified

- `tools/check_repo.py` - three new check functions (`check_example_sentence_length`, `check_before_after_spelled_count`, `check_example_rule_narration`), their constants (`EXAMPLE_PROSE_PATHS`, `PF41_WORD_CEILING`, `MARKER_SPAN_RE`, `SENTENCE_SPLIT_RE`, `SPELLED_CARDINAL_RE`, `NARRATION_CONNECTIVE_RE`, `NARRATION_META_TERMS`, `NARRATION_WINDOW_CHARS`), five new fixture builders plus one optional kwarg on the existing `_before_after_section`, five new self-test roots, three new `MUTATIONS` entries, and three new module-docstring bullets. Grew from 5,274 to 5,813 lines.
- `.planning/REQUIREMENTS.md` - EX-02's note updated in place to record this plan's three-of-seven gap mechanization without flipping the checkbox (see Decisions below).
- `.planning/WINDOWS.md` - id 14 added (`deviation`, phase 04): the interfaces-block measurement correction (12→13, 3→5).

## Decisions Made

- **Measurement correction over blind reproduction.** The plan's own `<interfaces>` block stated 12 word-spelled cardinals in `examples/deal-brief.md` and 3 in `worked-examples.md`. Direct measurement with the exact `SPELLED_CARDINAL_RE` the shipped code uses found 13 and 5. The shipped docstring states the corrected, verified figures. Filed as `WINDOWS.md` id 14. No scope or behavior changed — both files stay out of `before-after-spelled-count`'s scan (`examples/before-after.md` only) either way.
- **EX-02 stays unchecked despite a mechanically "ready" signal.** `gsd-tools requirements ready-ids` reports EX-02 ready to mark complete (04-07 is the last sibling plan in this phase declaring it). REQUIREMENTS.md's own EX-02 note explicitly forbids exactly this: "Do not re-mark Complete from a SUMMARY's `requirements-completed` field." Five (later expanded to seven) named UAT gaps are EX-02's actual closure condition; this plan mechanizes three (G-04-1, G-04-2, G-04-4). G-04-3/G-04-5 remain disclosed `verification: backstop` semantic judgments (already prose-repaired by 04-05, not mechanizable per this plan's own gap-coverage table), and G-04-6/G-04-7 belong to 04-08/04-09/04-10, none of which have run yet. The `requirements mark-complete` step was deliberately not invoked for EX-02 this plan; the REQUIREMENTS.md note was updated in place instead.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Documentation accuracy] Corrected two measured figures in the plan's own interfaces block before shipping them in a docstring**
- **Found during:** Task 2 (before-after-spelled-count)
- **Issue:** The plan's `<interfaces>` block stated "12 spelled cardinals were measured in [deal-brief.md's] prose" and "3 such occurrences" in worked-examples.md. Direct measurement (`python3 -c` scan with the exact `SPELLED_CARDINAL_RE` regex the shipped code uses) found 13 and 5 respectively.
- **Fix:** Wrote the corrected figures (13, 5) into `before-after-spelled-count`'s docstring (both the function-level and module-level bullets) rather than the plan's stated numbers.
- **Files modified:** `tools/check_repo.py`
- **Verification:** `python3 -c "import re; ... "` against the real `examples/deal-brief.md` and `worked-examples.md`, reproduced twice with identical results.
- **Committed in:** `fd1b17b` (Task 2 commit)

**2. [Rule 1 - Documentation accuracy] Did not act on a mechanically-ready EX-02 completion signal**
- **Found during:** Final requirements-update step
- **Issue:** `gsd-tools requirements ready-ids` reported EX-02 ready to mark complete, but REQUIREMENTS.md's own note for EX-02 explicitly forbids marking it complete from a SUMMARY's `requirements-completed` field and names a closure condition (all seven UAT gaps closed) this plan only partially satisfies (three of seven).
- **Fix:** Skipped `requirements mark-complete` for EX-02; updated the REQUIREMENTS.md note in place to record the three-gap mechanization progress, checkbox left unchecked.
- **Files modified:** `.planning/REQUIREMENTS.md`
- **Verification:** `grep -n "EX-02" .planning/REQUIREMENTS.md` shows the checkbox still `[ ]` after this plan.
- **Committed in:** plan metadata commit (this SUMMARY's own commit)

---

**Total deviations:** 2 auto-fixed (2 documentation-accuracy corrections, 0 code-behavior changes).
**Impact on plan:** Neither correction changes any check's scope, threshold, or shipped behavior — both are documentation-accuracy fixes that keep the repository's own "measured claims or no claims" standard honest about itself.

## Issues Encountered

None. All four gate commands (`--self-test`, `--mutation-test`, live run, `generate_derivatives.py --check`) passed on every task's first attempt; no retries, no node-repair invocations.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- The gate now enforces 44 discrimination-proven codes with 0 violations against the real repository. `example-rule-narration`'s disclosed blind spot (narration-by-self-reference to a document's own ordering) is carried forward as this plan's `must_haves.truths` `verification: backstop` entry — it was found once by an adversarial human-substitute read (04-UAT.md test 3) and repaired by hand in 04-05; no code in this repository detects a recurrence of that specific phrasing shape. This plan closes or reclassifies no existing `.planning/WINDOWS.md` entry for that residual; the phase's end-of-phase verification step (04-11 or equivalent) is the place to file it if it isn't already covered by the existing G-04-3/G-04-5 backstop-truth disclosures in 04-02-PLAN.md/04-05-SUMMARY.md.
- 04-08/04-09 (DIST-06) and 04-10 (DIST-02/DIST-05) are unaffected by this plan's changes and remain ready to execute independently — this plan touched no file in their `files_modified` scope.
- EX-02 stays unchecked in REQUIREMENTS.md pending G-04-3/G-04-5's semantic backstop confirmation and G-04-6/G-04-7's closure in 04-08/04-09/04-10.

## Self-Check: PASSED

- FOUND: `tools/check_repo.py`
- FOUND commit `840c6f5` (Task 1)
- FOUND commit `fd1b17b` (Task 2)
- FOUND commit `28a45ac` (Task 3)
- Re-ran all four gate commands: `--self-test` (44 verified codes), `--mutation-test` (44 codes discrimination-proven, 0 unexpected CONTROL, no FIRE-ONLY), live run (`check_repo: 0 violations`), `generate_derivatives.py --check` (exit 0)
- Re-ran every task's `<acceptance_criteria>`: all passed
- `git diff --stat` across all three task commits shows 543 insertions, 4 deletions in `tools/check_repo.py` — no existing check, fixture, assertion, or `MUTATIONS` entry removed

---
*Phase: 04-distribution-worked-examples*
*Completed: 2026-09-17*
