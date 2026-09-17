---
phase: 04-distribution-worked-examples
plan: 06
subsystem: examples
tags: [markdown, worked-examples, proof-first, check-repo]

# Dependency graph
requires:
  - phase: 04-distribution-worked-examples
    provides: "04-05's repair of examples/before-after.md to the same PF-4.1 sentence-length ceiling, establishing the precedent this plan applies to the second example file"
provides:
  - "All 28 skills/proof-first/references/worked-examples.md ✓ columns obey PF-4.1's 25-word sentence ceiling — 0 over ceiling, down from 8 of 31, maximum 37"
  - "The second shipped example file worked-examples.md now clears the same bar 04-05 applied to examples/before-after.md, so 04-07's example-sentence-length code can scan both files honestly"
affects: ["04-07 (mechanises example-sentence-length and example-rule-narration across both example files without narrowing scope around a known breach)", "Phase 6 LEG-04 (paraphrase-boundary and legal review gate)"]

# Actuals (#2632)
actuals:
  tokens: 1222
  tasks: 2
  commits: 2

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "When a bracketed integrity/review marker must stay adjacent to the specific claim it flags, group unrelated facts that share only a superficial list position into one sentence and give the marker-bearing claim its own sentence, even if that means slightly reordering an enumeration (MC-21's security+legal review sentence, then a separate procurement-review sentence carrying the GAP marker) — order-in-the-source-brief is not itself a must_haves prohibition; marker-to-claim adjacency is."

key-files:
  created: []
  modified:
    - skills/proof-first/references/worked-examples.md

key-decisions:
  - "MC-21's three-review enumeration was regrouped rather than split in original order: the two reviews with stated durations (security, legal) were combined into one sentence, and the procurement review (no stated duration) was moved into its own sentence directly carrying the [MC-21 GAP: ...] marker — because the task's own instruction to 'keep the marker adjacent to the claim it replaces' could not be satisfied while also preserving the brief's security-procurement-legal listing order without exceeding 25 words in a way that separated the marker from its claim."
  - "MC-6 and MC-31's attribution-then-quotation splits use two different patterns: MC-6 keeps a short bridging clause ('She said:') before the quote to avoid an abrupt fragment, while MC-31 drops the second attribution verb entirely and lets the quotation stand alone as its own sentence (matching 04-05's precedent for Marcus Feld's quote in examples/before-after.md) — both patterns keep the quoted material character-for-character unchanged, the only must_haves requirement that constrained the choice."

requirements-completed: [EX-02]

coverage:
  - id: D1
    description: "PF-1.25 and PF-2.17 ✓ columns (Task 1, the tracer) split into two sentences each, both under 25 words; Diane Osoria's name/role/$2,300,000 figure kept in PF-1.25's first sentence, the PF-2.17 REVIEW marker kept in a single bracket pair adjacent to the observation-window claim it flags; whole-file over-ceiling count fell from 8 to 6 of 31 sentences"
    requirement: EX-02
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py (0 violations)"
        status: pass
      - kind: other
        ref: "inline probe: whole-file sentence count/max/over-25 == 28,?,37,6 (Task 1 verify block)"
        status: pass
      - kind: other
        ref: "inline probe: $2,300,000/2026-10-30/[PF-2.17 counts unchanged at 6/2/1 (Task 1 verify block)"
        status: pass
      - kind: other
        ref: "python3 tools/generate_derivatives.py --check (exit 0)"
        status: pass
    human_judgment: false
  - id: D2
    description: "Remaining six ✓ columns (MC-6, MC-11, MC-16, MC-21, MC-31, MC-36) split into two sentences each, all under 25 words; every figure (55%/25%/20%/15%/30%/62%/2026-10-30/15/10 business days) and the MC-21 GAP marker preserved; whole-file over-ceiling count driven to 0 of 39 sentences, maximum 25; all 28 ✗ columns byte-identical; gate held at 41 codes discrimination-proven"
    requirement: EX-02
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --self-test && --mutation-test && (bare) (Task 2 verify block)"
        status: pass
      - kind: other
        ref: "python3 tools/generate_derivatives.py --check (exit 0)"
        status: pass
      - kind: other
        ref: "inline probe: whole-file 28 pairs / 39 sentences / max 25 / 0 over-25 (Task 2 verify block)"
        status: pass
      - kind: other
        ref: "inline probe: 28 ✗ lines, PF-/MC- token count 43 (not lower than pre-plan) (Task 2 verify block)"
        status: pass
      - kind: other
        ref: "grep -c '2026-10-30' and grep -c '62%' unchanged at 2/2 (Task 2 verify block)"
        status: pass
      - kind: other
        ref: "git diff -- worked-examples.md: 8 changed ✓ lines total across both tasks, 0 changed ✗ lines (Task 2 verify block)"
        status: pass
    human_judgment: true
    rationale: "One of this plan's must_haves is explicitly `verification: backstop`: 'Each split ✓ column still reads as a single coherent rewrite rather than as two stapled fragments, and no split has moved a piece of evidence away from the claim it backs.' This is a semantic readability/coherence judgment no script in this repository performs. All eight mechanical checks above pass, but the coherence verdict itself is not mechanised — see Backstop Residual below."

duration: 12min
completed: 2026-09-17
status: complete
---

# Phase 4 Plan 6: Repair worked-examples.md to obey PF-4.1 Summary

**Split all 8 over-ceiling ✓ columns in `skills/proof-first/references/worked-examples.md` (PF-1.25, PF-2.17, MC-6, MC-11, MC-16, MC-21, MC-31, MC-36) into two sentences each, driving the file's whole-file over-25-word-sentence count from 8 of 31 to 0 of 39, with every figure, marker, and ✗ column unchanged and the gate still at 41 codes discrimination-proven.**

## Performance

- **Duration:** 12 min
- **Started:** 2026-09-17T09:33:00Z
- **Completed:** 2026-09-17T09:45:00Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments

- Task 1 (tracer): split PF-1.25 and PF-2.17's ✓ columns, proving the repair path end to end — figures, the PF-2.17 REVIEW marker, and Diane Osoria's name/role all survived the split. Whole-file over-ceiling count fell 8 → 6 of 31 sentences.
- Task 2: split the remaining six MC-section ✓ columns (MC-6, MC-11, MC-16, MC-21, MC-31, MC-36), regrouping MC-21's review enumeration so its GAP marker stays adjacent to the procurement-review claim it flags. Whole-file over-ceiling count fell 6 → 0 of 39 sentences, maximum 25 words.
- All 28 ✗ columns byte-identical throughout; all 28 `PF-`/`MC-` headings, citation tokens, and figures (including `$2,300,000`, `2026-10-30`, `62%`, the five RFP percentages, and both review durations) unchanged.
- All four gate commands (`--self-test`, `--mutation-test`, bare `check_repo.py`, `generate_derivatives.py --check`) pass throughout, holding at 41 codes discrimination-proven, 0 unexpected CONTROL, no FIRE-ONLY line. This plan added no violation code and no new fixture root.

## Task Commits

1. **Task 1: Split the two PF-section sentences over the ceiling and prove the whole-file measurement moves** - `23f8c7a` (fix)
2. **Task 2: Split the remaining six MC-section sentences and drive the whole-file over-ceiling count to zero** - `badfea5` (fix)

## Files Created/Modified

- `skills/proof-first/references/worked-examples.md` - 8 of 28 ✓ columns rewritten (under headings `## PF-1.25`, `## PF-2.17`, `## MC-6`, `## MC-11`, `## MC-16`, `## MC-21`, `## MC-31`, `## MC-36`), each split into two sentences at or under 25 words. No heading, ✗ column, citation token, or pair order changed.

## Decisions Made

- MC-21's three-review enumeration regrouped (security + legal reviews into one sentence, procurement review carrying the GAP marker into its own) rather than split in the brief's original security-procurement-legal listing order, because the task's instruction to keep the marker adjacent to the claim it replaces could not be satisfied while also preserving that order under the 25-word ceiling.
- MC-6 keeps a short bridging clause ("She said:") before its quotation; MC-31 drops the second attribution verb and lets the quotation stand alone as its own sentence, matching 04-05's precedent for Marcus Feld's quote in `examples/before-after.md`. Both keep the quoted material character-for-character unchanged.
- Continuation clauses ("It is also measured on...", "It separately weights...", "That scoring happens...", "It also clears...") were used to bridge each split rather than repeating the sentence's subject, consistent with the pattern 04-05 established and had already passed acceptance criteria for the same class of edit.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Backstop Residual (verbatim, for the phase's verification step to file in `.planning/WINDOWS.md`)

Per this plan's `must_haves.truths`, one truth is explicitly `verification: backstop` and is not mechanised here or in `04-07`:

1. **Coherent-rewrite judgment:** "Each split ✓ column still reads as a single coherent rewrite rather than as two stapled fragments, and no split has moved a piece of evidence away from the claim it backs." — `verification: backstop`. All eight mechanical checks in this plan's two tasks pass (sentence-length, figure/marker/token preservation, ✗-column immutability, gate stability at 41 codes). The coherence verdict itself — whether each two-sentence split reads as a natural rewrite rather than a mechanically-severed fragment — is a semantic judgment no script in this repository performs, carried forward as a disclosed residual exactly as 04-05 carried its own G-04-3/G-04-5 residuals.

## Next Phase Readiness

- `skills/proof-first/references/worked-examples.md`'s 28 ✓ columns are now clean prose obeying PF-4.1, with 0 sentences over 25 words — the second example file `04-07`'s `example-sentence-length` code will scan now has a clean base, matching `examples/before-after.md`'s state after 04-05. `04-07` can scope its new code across both files without narrowing around a known breach.
- All four gate commands remain green at 41 codes discrimination-proven — this plan added no violation code and no new fixture root, matching its stated scope.
- The backstop coherence residual above stays a disclosed, un-mechanised semantic judgment pending Phase 6's LEG-04 gate or a future plan that decides to mechanise it further; not a blocker for `04-07`.

## Self-Check: PASSED

- `skills/proof-first/references/worked-examples.md` exists on disk and contains `## MC-36` (>= 140 lines: confirmed 147 lines).
- Commits `23f8c7a` and `badfea5` both found in `git log --oneline --all`.
- All `<acceptance_criteria>` re-run per task (Tasks 1-2) and the plan-level `<verification>` block (6 checks) re-confirmed passing before this SUMMARY was written: self-test PASS, mutation-test PASS (41 codes, 0 unexpected CONTROL, no FIRE-ONLY), check_repo 0 violations, generate_derivatives --check exit 0, whole-file probe `28 39 25 0`, git diff --stat showing 8 changed lines total.

---
*Phase: 04-distribution-worked-examples*
*Completed: 2026-09-17*
