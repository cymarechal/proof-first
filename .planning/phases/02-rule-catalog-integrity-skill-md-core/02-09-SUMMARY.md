---
phase: 02-rule-catalog-integrity-skill-md-core
plan: 09
subsystem: docs
tags: [readme, evals, gap-closure, honesty-constraint]

# Dependency graph
requires:
  - phase: 02-07
    provides: "skills/proof-first/references/worked-examples.md (option-a checkpoint answer), SKILL.md trimmed under the 5,000-token ceiling with byte-identical frontmatter"
provides:
  - "README.md Status prose that agrees with its own tree diagram and with the repository on disk (closes 02-REVIEW.md CR-03)"
  - "evals/pressure-tests.md scope note binding the 14 pending observations to a named SKILL.md description state"
affects: [phase-3-planning, phase-4-distribution, phase-5-eval-harness, phase-6-legal-gate]

# Actuals (#2632)
actuals:
  tokens: 1140
  tasks: 2
  commits: 2

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Scope note pattern: bind pending/unverifiable observations to a named source-artifact state (first line + char length + sha256) instead of duplicating the source text, so drift is detectable without a second copy to maintain"

key-files:
  created: []
  modified:
    - README.md
    - evals/pressure-tests.md

key-decisions:
  - "worked-examples.md entered README.md exactly twice (What exists today list + tree diagram), matching the file's existence on disk — the opening Status sentence names the reference files collectively rather than a third time, to satisfy the plan's own mention-count acceptance script."
  - "Did not touch evals/pressure-tests.md's must-not-fire justification paragraph (02-REVIEW.md WR-03) — out of this plan's scope by explicit instruction, left for a future plan."
  - "Did not perform either <human-check> item (WINDOWS.md ids 3 and 4) — both require actions (a semantic paraphrase-boundary read, a live harness session) this execution environment cannot perform or is not authorized to sign off on behalf of a human. Both ledger entries verified still open with null resolved_at after this plan's commits."

patterns-established:
  - "Attribution/scope notes cite a first-line fragment + character length + sha256 digest of a source block rather than reproducing the block, keeping a single source of truth."

requirements-completed: [CAT-03, CAT-04, CAT-05, CAT-10]

coverage:
  - id: D1
    description: "README.md's Status prose no longer contradicts its own tree diagram or the repository on disk; the self-contradicting 'has not been written yet' assertion is removed"
    requirement: "CAT-05"
    verification:
      - kind: other
        ref: "grep -c 'has not been written yet' README.md"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py (live check)"
        status: pass
      - kind: other
        ref: "membership script from PLAN.md <verify> (skills/proof-first/SKILL.md, both reference files, evals/pressure-tests.md all present in Status prose)"
        status: pass
    human_judgment: false
  - id: D2
    description: "README.md's target tree matches the skill folder on disk after 02-07: worked-examples.md added untagged, completeness-audit.md/artifact-patterns.md remain (planned)"
    requirement: "CAT-05"
    verification:
      - kind: other
        ref: "python3 -c mention-count parity script (worked-examples.md: 2 mentions vs file exists=2)"
        status: pass
      - kind: other
        ref: "grep -c '(planned)' README.md == 6, matching files absent from disk"
        status: pass
    human_judgment: false
  - id: D3
    description: "README.md publishes no measured claim; no-measured-claim paragraph preserved verbatim in substance; no percentage or rule-ID token introduced"
    requirement: "CAT-05"
    verification:
      - kind: other
        ref: "grep -nE '[0-9]+(\\.[0-9]+)?%' README.md (no output)"
        status: pass
      - kind: other
        ref: "rule-ID count script over Status prose == 0"
        status: pass
    human_judgment: false
  - id: D4
    description: "evals/pressure-tests.md carries a scope note binding the 14 pending observations to the SKILL.md description's first line, character length (439), and a sha256 digest of the frontmatter's first 14 lines, stating the 02-07 trim left it byte-identical and that observations must be re-run if the description changes"
    requirement: "CAT-10"
    verification:
      - kind: other
        ref: "sha256 of skills/proof-first/SKILL.md's first 14 lines (d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675) matches digest computed live in-task"
        status: pass
      - kind: other
        ref: "git diff evals/pressure-tests.md (added lines only, no table row/cell touched)"
        status: pass
    human_judgment: false
  - id: D5
    description: "No Observed/Date/Harness cell filled in; no ledger transition performed for WINDOWS.md ids 3 or 4; both human-check items (paraphrase-boundary judgment, live trigger-pressure-test run) correctly left open"
    requirement: "CAT-03"
    verification:
      - kind: other
        ref: "python3 json-extraction of WINDOWS.md ids 3/4 -> [(3,'open',None),(4,'open',None)]"
        status: pass
      - kind: other
        ref: "git diff --stat .planning/WINDOWS.md (empty)"
        status: pass
    human_judgment: true
    rationale: "The two WINDOWS.md items are human-verification items by design (a semantic paraphrase-boundary judgment and a live multi-session harness trigger test). This SUMMARY confirms they were correctly left untouched and open; closing them requires a human, not an executor, per the plan's own hard_prohibitions."

duration: 15min
completed: 2026-09-11
status: complete
---

# Phase 02 Plan 09: Close README/Pressure-Test Documentation Gaps Summary

**Reconciled README.md's self-contradicting Status section with its own tree diagram and the repository on disk (closing 02-REVIEW.md CR-03), and added a scope note to evals/pressure-tests.md binding its 14 unfilled trigger-pressure-test observations to the exact SKILL.md description state they were authored against — without performing or faking either of the two human-verification items this plan deliberately left open.**

## Performance

- **Duration:** ~15 min
- **Tasks:** 2 (both `type="auto"`)
- **Files modified:** 2 (`README.md`, `evals/pressure-tests.md`)

## Accomplishments

- Removed the literal string `has not been written yet` from README.md and rewrote both "What exists today" and "What does not exist yet" lists to name the actual repository state: `skills/proof-first/SKILL.md`, `references/checklist.md`, `references/deletion-test.md`, `references/worked-examples.md`, and `evals/pressure-tests.md` are now listed as shipped; the no-measured-claim closing paragraph survives verbatim in substance.
- Added `references/worked-examples.md` to the target-tree diagram (untagged, matching its existence on disk); `completeness-audit.md` and `artifact-patterns.md` remain `(planned)`, unchanged.
- Added a `## Scope` section to `evals/pressure-tests.md`, immediately before the `## Must fire` table, naming the frontmatter `description`'s first line, its whitespace-collapsed character length (439), and a sha256 digest of `SKILL.md`'s first 14 lines — so a reader can verify which `description` state the 14 pending phrasings bind to without a second copy of the description text existing to drift from the frontmatter.
- Left every Observed/Date/Harness cell in `evals/pressure-tests.md` untouched (all still read `not yet observed`); left `.planning/WINDOWS.md` completely untouched — ids 3 and 4 verified still `open` with `resolved_at: null` after both commits.
- All three CI-trio commands (`--self-test`, `--mutation-test`, bare live run) pass: mutation-test now reports `mutation-test PASS: 21 codes discrimination-proven` (02-08's discrimination-proof upgrade, confirmed still holding).

## Task Commits

1. **Task 1: Make README.md agree with itself and with the repository** — `0431507` (docs) — rewrote Status prose (both lists + opening sentence), added `worked-examples.md` to the tree diagram.
2. **Task 2: Make the pending trigger observations attributable, and route both human items** — `d5bfd57` (docs) — added the `## Scope` section to `evals/pressure-tests.md`; no table content touched; no WINDOWS.md write.

**Plan metadata:** commit pending (this SUMMARY + STATE.md + ROADMAP.md + REQUIREMENTS.md).

## Files Created/Modified

- `README.md` — Status section prose rewritten to match the tree diagram and disk; tree diagram gained one untagged `references/worked-examples.md` line. No measured claim added; attribution pointer count unchanged (still exactly 1); no `PF-#.#`/`MC-#` token cited.
- `evals/pressure-tests.md` — gained a 23-line `## Scope` section between the intro paragraph and the `## Must fire` table. Zero table rows added, removed, or reworded. Zero Observed/Date/Harness cells touched.

## Decisions Made

- `worked-examples.md` mention count in README.md: exactly 2 (the "What exists today" list entry and the tree-diagram line), matching the plan's parity script (`file exists` -> expect exactly 2 mentions). The initial draft's opening Status sentence also named the file individually, producing 3 mentions against an expected 2 — corrected by generalizing that sentence to "the `skills/proof-first/` rule catalog and its reference files" instead of re-listing `worked-examples.md` a third time. No content was lost; the file is still named twice, where it matters (existence claim + tree).
- Did not touch the `evals/pressure-tests.md` must-not-fire justification paragraph — 02-REVIEW.md WR-03 is a real finding there, explicitly out of this plan's scope.
- Did not perform either `<human-check>` item. WINDOWS.md ids 3 and 4 remain `open` with `resolved_at: null`, exactly as before this plan ran.

## Deviations from Plan

### Auto-fixed / Adjusted Issues

**1. [Rule 3 - Blocking, self-corrected during task] worked-examples.md mention count overshot the plan's parity script on first draft**
- **Found during:** Task 1, immediately after the first `<verify>` pass.
- **Issue:** The initial rewrite named `worked-examples.md` in the opening Status sentence, the "What exists today" list, and the tree diagram (3 mentions), but the plan's own acceptance script requires the mention count to equal 2 (the number of times the file, which exists, is expected to appear: once in prose, once in the tree).
- **Fix:** Generalized the opening sentence to refer to "the `skills/proof-first/` rule catalog and its reference files" instead of listing `worked-examples.md` by name a third time. Content coverage (the file's existence and its role) is unchanged; the count now matches the plan's own script.
- **Files modified:** `README.md`.
- **Verification:** re-ran the parity script — prints `2 2`. Re-ran all Task 1 acceptance criteria after the fix; all pass.
- **Committed in:** `0431507` (final state only — the intermediate 3-mention draft was never committed).

**2. [Plan calibration drift — documented, not fixed] `grep -c 'not yet observed' evals/pressure-tests.md` was already 16, not 14, before this task ran**
- **Found during:** Task 2, running the plan's own `<verify>` command after adding the scope note.
- **Issue:** The plan's acceptance criterion states this grep "prints `14` — unchanged from before this task." The file's pre-existing prose (written in plan 02-05, untouched by this plan) already contains the phrase `not yet observed` twice outside the tables — once in the intro paragraph's definition of the term, once in the `## Observations` closing paragraph — so the true pre-task baseline was 16, not 14. This plan added zero occurrences (16 before, 16 after — confirmed by diffing against `git show HEAD~1`), so the actual acceptance intent ("unchanged, no cell filled in, no row added/removed") is fully met; only the plan's literal digit assumption (authored before those two extra prose mentions were counted) does not match.
- **Fix:** None applied — the file's existing prose was not in this task's scope to reword, and doing so to force the digit to 14 would have violated the plan's own instruction to leave `evals/pressure-tests.md`'s pre-existing sentences untouched outside the new scope note. Documented here instead, matching the precedent 02-07 set for plan-authoring-time vs. execution-time count drift.
- **Files modified:** none (informational only).
- **Verification:** `git diff HEAD~1 HEAD -- evals/pressure-tests.md` shows only the added `## Scope` block; `grep -c 'not yet observed'` is 16 both before and after this plan's commit.
- **Committed in:** n/a (no code change; recorded here for auditability).

---

**Total deviations:** 2 (1 self-corrected during the acceptance-criteria gate before committing, 1 plan-calibration drift documented without a file change).
**Impact on plan:** No must-have truth or prohibition was violated. The self-corrected deviation is invisible in the final commit (the 3-mention draft was never staged). The documented drift does not affect any of the plan's substantive guarantees — zero cells were filled, zero rows changed, and the file's diff is additive-only, which is what the acceptance criterion actually protects against.

## Issues Encountered

None beyond the two deviations documented above, both resolved within the task's own acceptance-criteria gate before committing.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- 02-REVIEW.md CR-03 is closed: `README.md`'s Status prose, its tree diagram, and the repository on disk now name the same set of shipped and unwritten files.
- `evals/pressure-tests.md`'s 14 pending observations are attributable to a named `description` state (first line, 439-char length, sha256 `d5dd651a...`); all 14 remain unfilled, exactly as this repository's evidence rule requires until a human actually runs them.
- `.planning/WINDOWS.md` ids 3 and 4 remain `open` with `resolved_at: null`. Both are restated below verbatim for `/gsd-verify-work` to pick up without re-reading this plan:

  **WINDOWS.md id 3 — SOURCES.md reproduction-boundary and PF-0.1 / PF-3.1 framing judgment.** Read `SOURCES.md`'s reproduction boundary and out-of-bounds list, then read the current text of `PF-0.1` (opening reframe), `PF-3.1` (deletion test), and `PF-3.3` in `skills/proof-first/SKILL.md`. Confirm no contiguous run of any framework source's own wording is reproduced, no source's ordered list appears in source order, and no source-coined term has been adopted as this repository's own label — re-run this judgment against 02-07's tightened statement text (26 of 31 rule statements were rewritten; the rule-ID list is in 02-07-SUMMARY.md). Expected: no contiguous-reproduction and no coined-term-adoption violation found. Mark WINDOWS.md id 3 fixed only after making this judgment yourself.

  **WINDOWS.md id 4 — trigger pressure-test observations (CAT-10).** Install `skills/proof-first/` into a real harness (Claude Code, Cursor, or another Agent Skills-compatible harness) and, in a fresh session per phrasing, run each of the 14 phrasings in `evals/pressure-tests.md` (9 must-fire, 5 must-not-fire). Record the observed result, date, and harness name in each row's cells. Expected: every must-fire phrasing activates the skill; every must-not-fire phrasing does not. The scope note this plan added states which `description` (byte-identical since 02-07) the phrasings bind to. Mark WINDOWS.md id 4 fixed only after recording real observations.

- Requirements CAT-03, CAT-04, CAT-05, and CAT-10 are satisfied by this plan's mechanical criteria; CAT-03/CAT-04's paraphrase-boundary substance and CAT-10's actual trigger reliability still depend on the two human-check items above, tracked in WINDOWS.md, not closed by this plan.
- No prior-phase requirement was regressed: all three CI-trio commands pass against the current tree.

---
*Phase: 02-rule-catalog-integrity-skill-md-core*
*Completed: 2026-09-11*

## Self-Check: PASSED

- FOUND: `README.md`
- FOUND: `evals/pressure-tests.md`
- FOUND: commit `0431507`
- FOUND: commit `d5bfd57`
