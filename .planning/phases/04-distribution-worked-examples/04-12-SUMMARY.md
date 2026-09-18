---
phase: 04-distribution-worked-examples
plan: 12
subsystem: docs
tags: [proof-first, examples, gap-closure, before-after, control-tower]

# Dependency graph
requires:
  - phase: 04-distribution-worked-examples
    provides: "examples/before-after.md (04-02), the deal brief and worked-examples.md exhibits it must agree with (Phase 1/2), and the 04-UAT.md cold-read that found G-04-3"
provides:
  - "A Solution proposal ✓ column whose AWS Control Tower claim is true of the product and agrees with deal-brief.md:22 and worked-examples.md:32"
  - "A Demo ✓ column that quotes Marcus Feld once, whole, verbatim against the brief, with a PF-2.14 marker that names the commitment its own sentence makes"
affects: [04-13, phase-04-end-of-phase-uat]

# Actuals (#2632) — pairs with the plan's `estimate` to calibrate future estimates.
# Same estimateTokens scale (chars/4 over the realized diff), never a harness token count.
actuals:
  tokens: 1090
  tasks: 2
  commits: 2

# Tech tracking
tech-stack:
  added: []
  patterns: []

key-files:
  created: []
  modified:
    - examples/before-after.md

key-decisions:
  - "Used the plan's own validated candidate rewrites verbatim for both columns (measured this session at [24, 11, 19, 16, 18, 21] and [13, 19, 24, 22, 24] tokens per sentence) rather than composing new wording, since the planner had already run them against a throwaway copy of the repository and confirmed 0 violations."
  - "Reworded the Demo column's PF-2.14 marker to 'confirm the written summary reaches Marcus Feld's team before that call' — names the commitment the sentence actually makes (a written follow-up summary due before the next scheduled call), not the 'delivery date' the sentence never states."

requirements-completed: []  # EX-02 intentionally NOT marked complete — see "EX-02 status" below.

coverage:
  - id: D1
    description: "Solution proposal ✓ column re-scopes AWS Control Tower's governance to the new account structure, rebuilding the estate-to-target referent chain across its own sentences, while keeping PF-1.9's capability-first first sentence and both integrity markers (PF-2.17, PF-2.14) intact."
    requirement: "EX-02"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py (0 violations); phrase-count probe (governance across the new account structure == 1, governance across Halverton == 0); sentence-split probe (6 sentences, max 24 words, 0 spelled cardinals); first-sentence product-absence probe ([]); marker/figure-count probe (PF-2.17==1, PF-2.14>=2, 850>=2, 40 Oracle Database instances>=1); Rules-applied footer grep (==1); git diff --stat scope guard (empty)"
        status: pass
    human_judgment: true
    rationale: "Product-scope truth (does AWS Control Tower actually govern what the sentence says it governs) is semantic, not mechanizable by any code in this repository — the plan itself carries this as a `verification: backstop` truth. The mechanical probes above prove the specific repair (correct phrase present once, stranded phrase absent, PF-1.9 shape intact); they are proxies for this one instance, not a verdict on the class. A technical evaluator must still confirm the fixed sentence is true of the real product."
  - id: D2
    description: "Demo and discovery material ✓ column quotes Marcus Feld's recorded utterance once, whole, and verbatim (including the em dash) against deal-brief.md:70, replacing the two-fragment 'He added:' construction; the PF-2.14 marker at the end of the column now names the commitment its own sentence makes instead of a 'delivery date' the sentence never states."
    requirement: "EX-02"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py (0 violations); utterance verbatim-match probe (True, True); demo sentence-split probe (5 sentences, max 24 words, 0 'added:' matches, 0 'delivery date' matches); marker-count probe (PF-3.3==1, PF-2.14>=2); Rules-applied footer grep (==1); full gate incl. --self-test, --mutation-test (47 codes, 0 unexpected CONTROL, no FIRE-ONLY), generate_derivatives.py --check, evals/conformance/run_conformance.py --self-test; git diff --stat scope guard (empty)"
        status: pass
    human_judgment: true
    rationale: "Whether the repaired quotation and marker read as an honest, non-reconstructed transcript is a semantic/prose-quality judgment, carried in the plan as a second `verification: backstop` truth. The mechanical probes prove verbatim fidelity and marker-text correctness; they do not certify the passage 'reads' honest to a human reader."

# Metrics
duration: 12 min
completed: 2026-09-18
status: complete
---

# Phase 4 Plan 12: Repair the Control Tower governance scope and the Demo quotation Summary

**Re-scoped `examples/before-after.md`'s Solution proposal column so AWS Control Tower's governance claim is true of the product (the new account structure, not the on-premises VMware/Oracle estate), and fixed the Demo column's fabricated two-part Feld quotation and its misdirected PF-2.14 marker — closing gap G-04-3 and its two secondary defects with no new violation code.**

## Performance

- **Duration:** 12 min
- **Started:** 2026-09-18T (session start, see commit a628a8e timestamp)
- **Completed:** 2026-09-18
- **Tasks:** 2
- **Files modified:** 1 (`examples/before-after.md`)

## Accomplishments

- The Solution proposal ✓ column no longer claims AWS Control Tower governs Halverton Mutual's pre-migration VMware/Oracle estate. Sentence 2 now reads "AWS Control Tower delivers that governance across the new account structure" — the same scope stated by the two authorities it previously contradicted.
- The estate-to-target referent chain sentence 3 depended on is rebuilt as its own sentence rather than left dangling: the estate (850 VMware vSphere VMs, 40 Oracle Database instances) is reintroduced explicitly before stating it moves into the new accounts and lands on the target platforms.
- PF-1.9's capability-first first sentence ("Halverton Mutual must be able to govern every account in its new estate...") is untouched, and both integrity markers (PF-2.17 SOC 2 gap, PF-2.14 timeline-vs-comparable-programme) are untouched.
- The Demo column's fabricated two-attribution quotation ("said in discovery... He added...") is now one attribution, one quotation, reproduced character-for-character against `examples/deal-brief.md:70` including the em dash.
- The Demo column's trailing PF-2.14 marker no longer asks the reviewer to "confirm this delivery date" for a sentence that names no date — it now asks the reviewer to confirm the written follow-up summary actually reaches Marcus Feld's team before the next scheduled call, the commitment the sentence actually makes.
- The full CI gate (`check_repo.py`, `--self-test`, `--mutation-test`, `generate_derivatives.py --check`, `evals/conformance/run_conformance.py --self-test`) is green throughout, holding at 47 codes discrimination-proven — this plan registered no new violation code.

## Task Commits

Each task was committed atomically:

1. **Task 1: Re-scope the Solution proposal governance claim to the new account structure, end to end** - `a628a8e` (fix)
2. **Task 2: Quote Marcus Feld once, and make the PF-2.14 marker name the commitment its sentence makes** - `baa0395` (fix)

**Plan metadata:** (this commit)

## Files Created/Modified

- `examples/before-after.md` — Solution proposal ✓ column re-scoped (Task 1); Demo and discovery material ✓ column quotation and PF-2.14 marker repaired (Task 2). No heading, ✗ column, `Rules applied:` footer, or section order changed.

## Before/After Text — Every Sentence Changed

### Solution proposal ✓ column (Task 1)

**Before (sentences 2-4, defective):**
> AWS Control Tower delivers that governance across Halverton Mutual's on-premises estate of 850 VMware vSphere virtual machines and 40 Oracle Database instances. That estate moves onto Amazon EC2 for compute and Amazon Aurora PostgreSQL for the migrated data layer.

**After (sentences 2-4, repaired), with measured token counts:**
> AWS Control Tower delivers that governance across the new account structure. *(11 tokens)*
> Halverton Mutual's current estate of 850 VMware vSphere virtual machines and 40 Oracle Database instances moves into those accounts. *(19 tokens)*
> It lands on Amazon EC2 for compute and Amazon Aurora PostgreSQL for the migrated data layer. *(16 tokens)*

Sentence 1 (unchanged, 24 tokens): "Halverton Mutual must be able to govern every account in its new estate from one place, under guardrails the team can see and enforce."

Sentence 5 (unchanged, 18 tokens, PF-2.17 marker) and sentence 6 (unchanged, 21 tokens, PF-2.14 marker) carry both integrity markers, untouched.

Full measured token sequence for the repaired column: **[24, 11, 19, 16, 18, 21]** — matches the plan's own pre-validated candidate exactly.

### Demo and discovery material ✓ column (Task 2)

**Before (defective, two-attribution split):**
> Marcus Feld, Vice President of Infrastructure, said in discovery: 'We need a landing zone we can actually govern'. He added: 'Right now every VM is a snowflake'.

**After (repaired, single attribution, single quotation), with measured token counts:**
> Marcus Feld, Vice President of Infrastructure, named the requirement in the discovery call. *(13 tokens)*
> He said: 'We need a landing zone we can actually govern — right now every VM is a snowflake'. *(19 tokens)*

**PF-2.14 marker, before:** `[PF-2.14 REVIEW (commitment): confirm this delivery date before it is promised]`
**PF-2.14 marker, after:** `[PF-2.14 REVIEW (commitment): confirm the written summary reaches Marcus Feld's team before that call]`

Full measured token sequence for the repaired column: **[13, 19, 24, 22, 24]** — matches the plan's own pre-validated candidate exactly.

## The Three Authorities the Solution Column Now Agrees With

- `examples/deal-brief.md:22` — "AWS Control Tower for landing-zone governance across the new account structure."
- `skills/proof-first/references/worked-examples.md:32` — "AWS Control Tower provides that governance boundary across the new account structure."
- `examples/before-after.md:20` sentence 1 — "every account in its new estate" (unchanged, the phrase the repaired sentence 2 now genuinely agrees with).

Hand read (verification item 7): all three name the same scope for AWS Control Tower — the new account structure — not two.

## No Violation Code Added, and Why

This plan added zero new violation codes; `--mutation-test` reports 47 codes discrimination-proven before and after, unchanged. Product-scope truth (whether a named product is claimed to do something it does not do) has no regex signature — it is a semantic judgment about what AWS Control Tower actually does, not a pattern a checker can match. A code claiming to verify it would repeat the exact overstatement CR-01 already closed once in this phase (a check that is "covered" in name but cannot fire on the defect it claims to catch). The five mechanical probes run in Task 1's `<verify>` block (positive scope-phrase count, negative stranded-scope count, first-sentence product-absence list, marker/figure-count guard, footer guard) are proxies proving this one instance was repaired correctly — they are not, and do not claim to be, a general product-scope-truth checker.

## Both `verification: backstop` Residuals (verbatim, for the phase's verification step)

1. **T-04-12-01 residual (accepted, disclosed):** "Product-scope truth has no regex signature; the mechanical halves asserted here guard this instance, not the class. Routed to the human-verification backstop rather than to a new CI code, because a code named for coverage it does not have is the CR-01 failure this phase already paid to close once."
2. **Plan `must_haves.truths` backstop statements, verbatim:**
   - "A technical evaluator reading the Solution proposal ✓ column finds no claim about what AWS Control Tower does that is false of AWS Control Tower. Product-scope truth is semantic; no code in this repository judges it."
   - "The repaired Demo column reads as one recorded utterance quoted once, not as a transcript the vendor has reconstructed."

Both stay open as human-verification items for end-of-phase UAT; nothing in this plan attempts to close them mechanically.

## Decisions Made

- Used the plan's own pre-validated candidate rewrites for both columns verbatim, since the planner had already measured them against a throwaway copy of the full repository (0 violations, exact token sequences matching this session's measurements).
- Chose "confirm the written summary reaches Marcus Feld's team before that call" for the reworded PF-2.14 marker — names the concrete commitment (written summary delivery, to Feld's team, before the next scheduled call) the sentence states, avoiding both the removed "delivery date" language (which the sentence never asserts) and any new noun not already in the sentence.

## Deviations from Plan

None - plan executed exactly as written. Both candidate rewrites in the plan's `<interfaces>` block were used verbatim (Task 1) or with only the PF-2.14 marker text composed fresh per Task 2's instruction (the plan did not supply a candidate marker wording, only the requirement that it name the sentence's real commitment).

**Total deviations:** 0
**Impact on plan:** None.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## EX-02 Status

EX-02 stays unchecked in `.planning/REQUIREMENTS.md`, per the plan's own explicit instruction. `requirements-completed` above is deliberately empty even though this plan's PLAN.md frontmatter declares `requirements: [EX-02]` — that field records implementation scope, not verification, and REQUIREMENTS.md's own EX-02 note forbids marking it Complete from a SUMMARY's `requirements-completed` field. G-04-4 (the README defects) is still open and owned by `04-13-PLAN.md`; EX-02 cannot close until all seven `04-UAT.md` gaps are closed and end-of-phase UAT re-confirms.

## Next Phase Readiness

- G-04-3 (primary defect and both secondary_defects) is closed. `examples/before-after.md`'s Solution proposal and Demo columns are both now internally consistent with `examples/deal-brief.md` and `skills/proof-first/references/worked-examples.md`.
- G-04-4 and its five README `secondary_defects` remain open, owned by `04-13-PLAN.md` (wave 2 of this gap-closure round).
- `README.md`, `skills/proof-first/references/`, and `examples/deal-brief.md` are byte-identical to their state at the start of this plan (verified: `git diff --stat` against all three prints nothing across both tasks).
- No blockers for `04-13-PLAN.md` or for end-of-phase UAT re-verification of G-04-3.

---
*Phase: 04-distribution-worked-examples*
*Completed: 2026-09-18*

## Self-Check: PASSED

- FOUND: examples/before-after.md
- FOUND: .planning/phases/04-distribution-worked-examples/04-12-SUMMARY.md
- FOUND: a628a8e (Task 1 commit)
- FOUND: baa0395 (Task 2 commit)
- All acceptance criteria for both tasks re-verified passing (see Task Commits and Accomplishments above); full plan-level `<verification>` block (7 items) re-run and passing, including the hand read against the three authorities.
