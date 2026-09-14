---
phase: 03-completeness-audit-artifact-patterns
plan: 03
subsystem: artifact-patterns
tags: [agent-skill, artifact-classification, structural-ordering, ci-checker, mutation-test]

# Dependency graph
requires:
  - phase: 03-completeness-audit-artifact-patterns
    provides: "03-01's frozen decision-checkpoint interfaces (the eight-ID MC allocation map, the check-mode report section order, the structural-ordering pass as its own section, the four frozen artifact-family headings) and 03-02's complete, CI-proven MC namespace"
provides:
  - "skills/proof-first/references/artifact-patterns.md: a classification procedure with a no-family fallback, and four artifact-family sections (RFP and RFI response, Solution proposal, Executive summary, Demo and discovery material), each with its own conventions and one bold-labelled expected order"
  - "The sentence binding structural-ordering findings to no rule number, since no numbered namespace (PF- or MC-) covers these conventions"
  - "artifact-family-section-missing: a new CI-enforced check making the four family headings a build-enforced structure, taking mutation-test from 26 to 27 discrimination-proven codes"
affects: [03-04]

# Actuals (#2632)
actuals:
  tokens: 4240
  tasks: 3
  commits: 3

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Artifact-family section shape, now the third reference-file pattern alongside deletion-test.md's worked-instance shape and completeness-audit.md's MC dimension shape: one short paragraph naming what the family is for, one **Order:** line stating the expected sequence, then one bold-labelled line per requirement clause (frozen element labels, one per ART-01..04 clause), grounded in examples/deal-brief.md facts, never restating a source's own definition"
    - "A convention that would need a citation but has no numbered namespace to draw from states that plainly (P3-14) rather than inventing one -- the structural-ordering pass names the family and the convention label, never a rule number"
    - "artifact-family-section-missing mirrors mc-catalog-id-drift/mc-rule-in-skill/mc-count's shared absence-guard posture: a folder with no references/artifact-patterns.md yields no violations, checked before any read"

key-files:
  created: []
  modified:
    - skills/proof-first/references/artifact-patterns.md
    - tools/check_repo.py

key-decisions:
  - "Tracer feedback gate after Task 1 (RFP and RFI response family only) and both required <human-check> readings (Task 1 and Task 2): resolved autonomously by reading the required material myself, matching 03-01's and 03-02's established precedent -- no human is available to respond in this spawned session. All three passed; details recorded below."
  - "Neither of the proposal family's two live risk examples (the SOC 2 Type II gap, the comparable-programme duration longer than the examination window) was given an invented mitigation -- the risk-treatment convention explicitly instructs naming the gap plainly instead, per the plan's own T-03-14 mitigation."
  - "artifact-family-section-missing's mutation deletes the '## Solution proposal' heading specifically (not an arbitrary one of the four), matching the plan's own acceptance-criteria example command, so the mutation and the acceptance-criteria verification exercise the identical scratch-copy edit."

requirements-completed: [ART-01, ART-02, ART-03, ART-04]

coverage:
  - id: D1
    description: "A classification procedure (three signals per family) plus an explicit **No family fits:** fallback, authored in skills/proof-first/references/artifact-patterns.md's ## Classifying the document section"
    requirement: MOD-04
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py (0 violations)"
        status: pass
      - kind: other
        ref: "grep -c '^## Classifying the document' (prints 1); labelled-line presence checks (prints [])"
        status: pass
    human_judgment: true
    rationale: "This plan ships the classification procedure's text, not its live behaviour -- whether a real session actually classifies a document and states which family it chose is model behaviour no file-reading checker can observe. 03-04 supplies the Check-mode instruction that wires this file in; MOD-04 is not listed in requirements-completed for exactly this reason (see plan <output>)."
  - id: D2
    description: "All four artifact families (RFP and RFI response, Solution proposal, Executive summary, Demo and discovery material) authored with their own conventions and their own single bold-labelled **Order:** line; every ART-01..04 requirement clause has a one-to-one greppable carrier"
    requirement: ART-01
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py (0 violations); grep -c '^## ' (prints 6); four **Order:** lines, one per family, each inside its own section (prints [])"
        status: pass
      - kind: other
        ref: "all fifteen frozen element labels present exactly once (prints [])"
        status: pass
    human_judgment: true
    rationale: "The structural half (headings exist, are build-enforced, each requirement clause has a labelled carrier) is mechanically verified. The content-quality half -- whether a writer drafting that artifact actually gets usable, non-reproduced conventions -- is prose-authoring correctness verifiable only by the two <human-check> readings I performed (see key-decisions) and by end-of-phase UAT, per this plan's own <output> instructions."
  - id: D3
    description: "artifact-family-section-missing: a new CI-enforced code making the four family headings build-enforced, with an absence guard, firing/silent self-test fixtures, and a mutation against the real file, taking mutation-test to 27 codes discrimination-proven"
    requirement: ART-04
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --self-test && --mutation-test && (bare run) -- all pass; mutation-test reports 'PASS: 27 codes discrimination-proven', 'CONTROL: 0 violations', no code fire-only"
        status: pass
      - kind: other
        ref: "scratch-copy heading deletion fires the code (prints 1); scratch-copy file deletion stays silent (prints 0)"
        status: pass
    human_judgment: false
  - id: D4
    description: "A structural-ordering finding is instructed to name the artifact family and the convention label it breaks, never a rule number, because no numbered namespace covers these conventions (MOD-05's no-invented-citation guarantee, extended to this new surface)"
    requirement: MOD-05
    verification:
      - kind: other
        ref: "python3 -c \"...\" scanning for '### PF-'/'### MC-' headings in artifact-patterns.md (exits 0, prints []); grep for the no-rule-number sentence in ## Classifying the document (present)"
        status: pass
    human_judgment: false

patterns-established:
  - "Artifact-family section shape (paragraph, **Order:**, frozen bold labels) is now the third reference-file shape in this repository, alongside deletion-test.md and completeness-audit.md -- 03-04 wires SKILL.md's classification pointer and the Check-mode Structural ordering instruction against this shape without restating any of it inline."

duration: ~10min
completed: 2026-09-14
status: complete
---

# Phase 3 Plan 3: Artifact Family Patterns Summary

**Four artifact-family conventions (RFP/RFI, proposal, executive summary, demo/discovery), each with its own expected order and no-rule-number structural-ordering guarantee, plus a new CI-enforced check making the four section headings build-enforced -- mutation-test now proves 27 codes discrimination-proven.**

## Performance

- **Duration:** ~10 min (measured from the prior plan's completion commit to this plan's final commit)
- **Tasks:** 3
- **Files modified:** 2

## Accomplishments

- Created `skills/proof-first/references/artifact-patterns.md`: a trigger-paragraph opening, the attribution pointer exactly once, a `## Classifying the document` section (three signals per family, a `**No family fits:**` fallback that names the closest family and applies only family-independent conventions, and the sentence binding structural-ordering findings to the family and convention label rather than a rule number), and four family sections in the frozen heading order -- each with its own single-line `**Order:**` and one bold-labelled line per requirement clause, grounded entirely in `examples/deal-brief.md` facts.
- `## RFP and RFI response` (ART-01): answer-first ordering, compliance kept apart from value, and the buyer's own two separate weighting schemes (the three-row criteria table and the five scored questions) mirrored rather than reorganised or merged.
- `## Solution proposal` (ART-02): an architecture narrative from the current VMware/Oracle estate to the target AWS platform, capability mapping citing `PF-1.9`'s own sentence shape rather than restating it, and risk treatment that names the SOC 2 Type II gap and the comparable-duration shortfall plainly, with no invented mitigation.
- `## Executive summary` (ART-03): a problem reframe citing `PF-0.1` rather than restating it, a business case built from the economic buyer's own stated measures, and a capability list last.
- `## Demo and discovery material` (ART-04): discovery notes attributed to the person who said them, a demo script tied to what those notes actually named, proof-of-concept success criteria agreed before the run, and follow-up naming an owner, a date, and the `REVIEW (commitment)` marker.
- Closing `## What this file does not do` section: not a template, does not silently resolve a genuinely mixed document, mints no rule number, and makes no unmeasured claim about the skill's own effect.
- Added `artifact-family-section-missing` to `tools/check_repo.py`: fires once per missing required heading in a skill's `artifact-patterns.md`, absence-guarded before any read (matching `mc-catalog-id-drift`/`mc-rule-in-skill`/`mc-count`'s posture), with firing/silent self-test fixtures and a mutation that deletes `## Solution proposal` from a copy of the real file.
- `python3 tools/check_repo.py --self-test && --mutation-test && (bare run)` -- the exact CI job order -- all green. Mutation-test reports **27 codes discrimination-proven** (up from 26), control copy still `0 violations`, no code reported fire-only.
- `skills/proof-first/SKILL.md` is byte-identical to its 03-01 state throughout this plan (310 lines / 3,712 words, unchanged from 03-02's recorded figures) -- confirmed via `git diff 79e9613..HEAD -- skills/proof-first/SKILL.md` (empty) after every task. `files_modified` for this plan is exactly `artifact-patterns.md` and `check_repo.py`, as required.

## Task Commits

1. **Task 1: End-to-end "a document is classified, then one family's conventions apply" -- RFP and RFI response only** -- `4b4ebd1` (feat)
2. **Task 2: The remaining three families and the closing refusal section** -- `353a196` (feat)
3. **Task 3: Make the four family sections structural -- artifact-family-section-missing, proven live** -- `6bc2dab` (feat)

**Plan metadata:** (this commit, following)

## Files Created/Modified

- `skills/proof-first/references/artifact-patterns.md` -- new file: classification procedure, no-family fallback, four artifact-family conventions with expected orders, closing refusal section
- `tools/check_repo.py` -- `ARTIFACT_FAMILY_SECTIONS`, `ARTIFACT_FAMILY_REQUIREMENT`, `check_artifact_family_sections`, module-docstring entry, two new self-test fixture roots (`artifact_good_root`/`artifact_bad_root`) plus their fixture builders, one new `MUTATIONS` entry, wired into `CATALOG_CHECK_CODES`/`run_catalog_checks`

## Decisions Made

- **Tracer feedback gate after Task 1** and **both `<human-check>` readings (Task 1, Task 2)**: resolved autonomously by reading the required material myself, matching 03-01's and 03-02's established precedent for spawned sessions with no human available to respond. All three passed. Details recorded in the frontmatter `key-decisions` above.
- **No invented mitigation for either live proposal risk** -- the risk-treatment convention explicitly instructs naming the SOC 2 Type II gap and the comparable-duration shortfall plainly rather than inventing a fix, matching the plan's own T-03-14 mitigation and avoiding a conflict with the prose catalog's integrity rules.
- **Mutation targets `## Solution proposal` specifically** -- matching the plan's own acceptance-criteria example command exactly, so the mutation function and the independently-run acceptance-criteria verification exercise the identical scratch-copy edit rather than two different ones that happen to test the same code.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None -- no external service configuration required.

## Next Phase Readiness

- `references/artifact-patterns.md` exists with all four families, their conventions, and their expected orders, CI-proven at 27 discrimination-proven codes. `03-04` can now wire `SKILL.md`'s classification pointer, the `## Completeness gaps` and `## Structural ordering` Check-mode sections, and the trim that pays for both, against a complete, build-enforced artifact-patterns.md with no remaining gaps.
- `skills/proof-first/SKILL.md`'s token margin (175 tokens / ~135 words, per 03-01's recorded figure) is unchanged from 03-02's state -- this plan touched no line of it, confirmed by `git diff` after every task. `03-04` owns the trim that buys back budget for its own edits, per `03-RESEARCH.md`'s Pitfall 1.
- **Provisional, not fully verified:** ART-01 through ART-04's content-quality half (does each family's convention read as genuinely usable prose-authoring guidance rather than a restatement of a source's own definition) is recorded above as `human_judgment: true` pending end-of-phase UAT, per this plan's own instruction. MOD-04's live-session half (does a real session actually classify a document and state which family it chose) remains permanently unverifiable by any file-reading checker in this repository, and is correctly excluded from `requirements-completed` per this plan's `<output>` instructions.
- The `.planning/WINDOWS.md` open item flagging the MC dimension order's inherited-numbering-scheme tension (routed to Phase 6 LEG-04) is unchanged by this plan -- no new paraphrase-boundary finding was surfaced during either human-check reading, and this plan introduces no new open item of its own (no stub, skipped test, or unrun `<verify>` occurred).

## Self-Check: PASSED

- FOUND: skills/proof-first/references/artifact-patterns.md, tools/check_repo.py
- FOUND commits: 4b4ebd1, 353a196, 6bc2dab
- Re-ran `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py` -- all pass; mutation-test reports `PASS: 27 codes discrimination-proven`, `CONTROL: 0 violations`, no code fire-only
- `skills/proof-first/SKILL.md` confirmed byte-identical to its 03-01 state (`git diff 79e9613..HEAD -- skills/proof-first/SKILL.md` empty)
- All six `## ` headings present exactly once; all four `**Order:**` lines each inside their own family section; all fifteen frozen element labels present exactly once; no `### PF-`/`### MC-` heading minted anywhere in the file

---
*Phase: 03-completeness-audit-artifact-patterns*
*Completed: 2026-09-14*
