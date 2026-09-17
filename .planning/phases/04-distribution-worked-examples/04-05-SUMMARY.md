---
phase: 04-distribution-worked-examples
plan: 05
subsystem: examples
tags: [markdown, worked-examples, proof-first, check-repo]

# Dependency graph
requires:
  - phase: 04-distribution-worked-examples
    provides: "04-02's four document-level before/after pairs in examples/before-after.md, and 04-04's README lead-in reproducing the RFP pair verbatim"
provides:
  - "All four examples/before-after.md ✓ columns rewritten to obey PF-4.1 (25-word sentence ceiling), narrate no rule, invent no count, and demonstrate PF-1.9 and PF-3.3 in the shape those rules require"
  - "README.md's reproduced RFP pair kept byte-identical to the repaired source"
affects: ["04-07 (mechanises example-rule-narration, example-sentence-length, before-after-spelled-count on top of this repair)", "04-08 (owns README's remaining prose)", "Phase 6 LEG-04 (paraphrase-boundary and legal review gate)"]

# Actuals (#2632)
actuals:
  tokens: 9000
  tasks: 3
  commits: 3

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Sentence-ending punctuation inside a quoted passage must place the closing quote mark before the terminal period (`govern'.` not `govern.'`), or the word-count/sentence-split regex used by check_repo.py and this plan's own verify probes (`(?<=[.!?])\\s+`) fails to detect the sentence boundary and merges quoted dialogue into the following sentence."

key-files:
  created: []
  modified:
    - examples/before-after.md
    - README.md

key-decisions:
  - "Removed invented counts (four cut-over waves; three demo accounts) rather than adding rows to examples/deal-brief.md's Canonical figures table — a migration-wave count is the vendor's own solution-design choice, not a fact about the buyer's deal, and the brief's own rule is that the example bends to the brief, not the other way round."
  - "Solution proposal ✓ column recast to open on the capability ('Halverton Mutual must be able to govern every account...') with AWS Control Tower named only in the following sentence as the means — satisfies PF-1.9's 'never as the sentence's subject' by structure, verified mechanically by a first-sentence product-absence probe."
  - "PF-3.3 marker moved off the trailing quotation and onto the vendor's own sentence: Marcus Feld's discovery quote now stands alone with its attribution and no marker; 'a landing zone the team can actually govern' is retained and marked inside the demo-script sentence instead, giving the deletion test an actual term to fire against."

requirements-completed: [EX-02, DIST-06]

coverage:
  - id: D1
    description: "RFP and RFI response ✓ column split from 2 sentences (88, 16 words) to 4 sentences (max 22 words); rule-narration deleted; invented 'four sequenced waves' count removed; README's reproduced pair kept byte-identical"
    requirement: EX-02
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py (0 violations)"
        status: pass
      - kind: other
        ref: "inline probe: RFP column sentence count/max-words (Task 1 verify block)"
        status: pass
      - kind: other
        ref: "inline probe: README-vs-source drift list == [] (Task 1 verify block)"
        status: pass
    human_judgment: false
  - id: D2
    description: "Solution proposal ✓ column recast so PF-1.9 is demonstrated (capability-first, product named as the means) rather than inverted; rule-narration and the 'Two risks' count deleted; split from 3 sentences (43, 32, 58 words) to 5 (max 24 words); both PF-2.14/PF-2.17 REVIEW markers kept intact"
    requirement: EX-02
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py (0 violations)"
        status: pass
      - kind: other
        ref: "inline probe: first-sentence product-name absence == [] (Task 2 verify block)"
        status: pass
      - kind: other
        ref: "inline probe: marker counts (1x PF-2.17 REVIEW, >=1 PF-2.14 REVIEW) (Task 2 verify block)"
        status: pass
    human_judgment: true
    rationale: "G-04-3's PF-1.9 judgment (does the recast genuinely lead with the capability, or merely reorder the clause) is a semantic call the plan itself carries as a `verification: backstop` truth. The first-sentence product-absence probe is a mechanical proxy for this, not the verdict itself."
  - id: D3
    description: "Executive summary and Demo ✓ columns repaired: rule-narration and word-spelled counts removed; PF-3.3 marker re-attached from a trailing quotation onto a retained term inside the vendor's own sentence; file-wide sentence-length, cardinal-count, and narration-signature probes driven to zero across all four columns; all four gate commands (self-test, mutation-test at 41 codes, check_repo, generate_derivatives --check) still pass"
    requirement: EX-02
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --self-test && --mutation-test && (bare) (Task 3 verify block)"
        status: pass
      - kind: other
        ref: "python3 tools/generate_derivatives.py --check"
        status: pass
      - kind: other
        ref: "inline probe: file-wide 4 columns / 17 sentences / max 24 words / 0 over 25 (Task 3 verify block)"
        status: pass
      - kind: other
        ref: "inline probe: file-wide word-spelled-cardinal count == 0 (Task 3 verify block)"
        status: pass
      - kind: other
        ref: "inline probe: narration-signature probe == [] across all ✓ columns (Task 3 verify block)"
        status: pass
      - kind: other
        ref: "inline probe: PF-3.3 marker preceded by non-quote characters ('n ') (Task 3 verify block)"
        status: pass
    human_judgment: true
    rationale: "G-04-5's PF-3.3 term-attachment judgment (is the retained term one whose deletion would change technical meaning) is a semantic call carried as a `verification: backstop` truth. The preceding-character probe proves the marker moved off the quotation onto a term; it does not itself judge whether that term is load-bearing."

duration: 8min
completed: 2026-09-17
status: complete
---

# Phase 4 Plan 5: Repair the worked-examples prose to obey PF-4.1 Summary

**Rewrote all four `examples/before-after.md` ✓ columns to split every sentence at or under PF-4.1's 25-word ceiling, deleted the rule-narration each column had folded into its own quoted prose, removed two invented counts never stated in the deal brief, recast the Solution proposal column so PF-1.9 leads with the capability instead of the product, and re-attached the PF-3.3 marker from a trailing quotation onto an actual retained term — while keeping the gate at 41 codes discrimination-proven throughout.**

## Performance

- **Duration:** 8 min
- **Started:** 2026-09-17T09:21:00Z
- **Completed:** 2026-09-17T09:29:09Z
- **Tasks:** 3
- **Files modified:** 2 (`examples/before-after.md`, `README.md`)

## Accomplishments

- RFP and RFI response ✓ column: split from 2 sentences (88, 16 words) to 4 (max 22 words); deleted the PF-2.1/MC-11 rule-narration; removed the invented "four sequenced waves" count; propagated the repaired line verbatim into README.
- Solution proposal ✓ column: recast to open on the capability Halverton Mutual must be able to exercise, naming AWS Control Tower afterward as the means (PF-1.9); deleted rule-narration and the "Two risks" count; split from 3 sentences (43, 32, 58 words) to 5 (max 24 words); both PF-2.14/PF-2.17 REVIEW markers preserved.
- Executive summary ✓ column: deleted the PF-0.1/PF-1.25/PF-2.11 rule-narration; split from 24/45/30 words (two over ceiling) to 24/24/17; the PF-2.11 GAP marker, Diane Osoria's two stated priorities, and the deliverable list all preserved.
- Demo and discovery material ✓ column: re-attached the PF-3.3 marker from trailing Marcus Feld's whole quotation onto the vendor-authored phrase "a landing zone the team can actually govern"; removed the invented "three representative accounts" / "any of the three accounts" count; deleted the PF-3.3/PF-2.14/MC-31 rule-narration; split from 27/55/24 words to 18/9/24/22/24.
- File-wide result: 17 sentences across all four ✓ columns, 0 over 25 words (down from 8 of 11), 0 word-spelled cardinals (down from 5), 0 narration-signature hits (down from 4 of 4 columns hit). All four gate commands unchanged at 41 codes discrimination-proven, 0 violations, 0 unexpected CONTROL.

## Task Commits

1. **Task 1: Repair the RFP and RFI response pair end to end, and propagate it into README** - `5de105d` (fix)
2. **Task 2: Recast the Solution proposal ✓ column so PF-1.9 is demonstrated rather than inverted** - `f8ebf78` (fix)
3. **Task 3: Repair the Executive summary and Demo pairs, re-attach the PF-3.3 marker to a term, and drive the file-wide measurements to zero** - `8e3f7f1` (fix)

## Files Created/Modified

- `examples/before-after.md` - All four ✓ columns rewritten (RFP and RFI response, Solution proposal, Executive summary, Demo and discovery material). No heading, ✗ column, `Rules applied:` footer, or section order changed — confirmed by `git diff` showing no `-✗`/`+✗` hunks anywhere in the file.
- `README.md` - The three reproduced RFP pair lines (✗, ✓, `Rules applied:`) kept byte-identical to the repaired source; no other line changed (`git diff --stat` reports 1 insertion / 1 deletion).

## Decisions Made

- Removed the invented counts (the RFP column's "four sequenced waves", the Demo column's "three representative accounts") entirely rather than adding rows to `examples/deal-brief.md`'s Canonical figures table. A migration-wave count and a demo-account count are the vendor's own solution-design choices, not facts about the buyer's deal; the brief's own closing section states that anything a later example asserts beyond its stated facts is an invented fact and a defect, and the Canonical figures table is an interface Phase 5 binds to — widening it for an example's convenience would invert that dependency.
- Recast the Solution proposal opening sentence as "Halverton Mutual must be able to govern every account in its new estate from one place, under guardrails the team can see and enforce," naming AWS Control Tower only in the following sentence, so the mechanical first-sentence product-absence probe has something concrete to check against PF-1.9's "never as the sentence's subject."
- Moved the PF-3.3 marker off the trailing whole-quotation attachment and onto the vendor-authored phrase "a landing zone the team can actually govern" inside the demo-script sentence, giving the deletion test an actual retained term to fire against instead of demonstrating the rule where it isn't needed.
- Adopted a punctuation convention for quoted dialogue that ends a sentence — closing single-quote mark placed before the terminal period (`govern'.`), not after (`govern.'`) — because the file's own existing sentence-boundary regex (`(?<=[.!?])\s+`, used identically by this plan's verify probes and by `04-07`'s planned `example-sentence-length` check) only recognizes a sentence boundary when the character immediately preceding whitespace is `.`/`!`/`?`. This is the same convention the file's own pre-existing Demo column already used for its `[PF-3.3: ...]` bracket adjacency; this plan applies it consistently to the two new short quoted sentences added to that column.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] First draft of the Demo column's split quotation merged three sentences into one 51-word run**
- **Found during:** Task 3, before committing (caught by the task's own verify block, not shipped)
- **Issue:** The initial rewrite split Marcus Feld's quote into two short sentences ending `govern.'` and `snowflake.'` (period before the closing quote mark). The word-count/sentence-split regex `(?<=[.!?])\s+` requires the character immediately before whitespace to be terminal punctuation; with the quote mark trailing the period, no sentence boundary was detected, and the split script merged those two "sentences" plus the following vendor sentence into one 51-word run — failing the file-wide "0 sentences over 25 words" acceptance criterion.
- **Fix:** Swapped the punctuation order to place the closing quote mark before the terminal period (`govern'.`, `snowflake'.`), matching the convention the file's pre-existing `[PF-3.3: ...]` bracket adjacency already used. Re-ran the sentence-split probe; all 17 sentences file-wide now measure at or under 24 words.
- **Files modified:** `examples/before-after.md` (within Task 3's single edit; no separate commit — the corrected text is what Task 3's commit `8e3f7f1` contains)
- **Verification:** File-wide inline probe re-run after the fix: `4 17 24 0` (4 columns, 17 sentences, max 24 words, 0 over 25).
- **Committed in:** `8e3f7f1` (the fix was made before the task's first commit attempt; no broken version was ever committed)

---

**Total deviations:** 1 auto-fixed (1 bug, caught by the task's own verify block before any commit)
**Impact on plan:** No scope creep — the fix is a punctuation-convention correction internal to Task 3's own prose rewrite, required to satisfy that same task's stated acceptance criteria. No shipped content was ever incorrect.

## Issues Encountered

None beyond the self-caught deviation above.

## User Setup Required

None - no external service configuration required.

## Backstop Residuals (verbatim, for the phase's verification step to file in `.planning/WINDOWS.md`)

Per this plan's `<artifacts_this_phase_produces>` block, this plan closes or reclassifies no existing WINDOWS.md entry (entries 11, 12, 13 stay open and untouched), and the two residuals below are carried as `verification: backstop` truths in the plan's own `must_haves`, not mechanised here or in `04-07`. Recorded verbatim so the phase's end-of-phase verification step can file them:

1. **G-04-3 (PF-1.9 judgment):** "Each ✓ column reads as an applied rewrite a technical evaluator would accept rather than a paraphrase of the rule's own wording, and the PF-1.9 recast genuinely leads with the capability rather than merely reordering the clause." — `verification: backstop`. The mechanical half asserted here is the first-sentence product-absence probe (Task 2 verify block), which is a proxy, not a verdict, on whether the recast is genuinely capability-led rather than a superficial reorder.
2. **G-04-5 (PF-3.3 judgment):** "The PF-3.3 marker is attached to a term whose deletion would change technical meaning, not to a phrase that survives deletion intact." — `verification: backstop`. The mechanical half asserted here is the preceding-character probe (Task 3 verify block), which proves the marker moved off the quotation onto a term; it does not itself judge whether that term is load-bearing under the deletion test.

## Next Phase Readiness

- `examples/before-after.md`'s four ✓ columns are now clean prose obeying PF-4.1, narrating no rule, and inventing no count — the file `04-07` will build mechanised checks on top of (`example-rule-narration`, `example-sentence-length`, `before-after-spelled-count`) now has a clean base to check against rather than checking against writing that was itself broken.
- `README.md`'s reproduced RFP pair matches its source verbatim; `04-08`'s remaining README prose work is unaffected (no lines outside the three reproduced ones were touched).
- All four gate commands remain green at 41 codes discrimination-proven — this plan added no violation code and no new fixture root, matching its stated scope.
- G-04-3 and G-04-5 stay as disclosed, un-mechanised semantic judgments pending Phase 6's LEG-04 gate or a future plan that decides to mechanise them further; not blockers for `04-06`/`04-07`.

## Self-Check: PASSED

- `examples/before-after.md` exists on disk.
- `README.md` exists on disk.
- `.planning/phases/04-distribution-worked-examples/04-05-SUMMARY.md` exists on disk.
- Commits `5de105d`, `f8ebf78`, `8e3f7f1` all found in `git log --oneline --all`.
- All `<acceptance_criteria>` re-run per task (Tasks 1-3) and the plan-level `<verification>` block (5 checks) re-confirmed passing before this SUMMARY was written.

---
*Phase: 04-distribution-worked-examples*
*Completed: 2026-09-17*
