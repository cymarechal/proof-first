---
phase: 03-completeness-audit-artifact-patterns
plan: 04
subsystem: rule-catalog
tags: [agent-skill, skill-md, check-mode, artifact-classification, token-budget, ci-checker, mutation-test]

# Dependency graph
requires:
  - phase: 03-completeness-audit-artifact-patterns
    provides: "03-01's frozen check-mode section order and four artifact-family headings, 03-02's complete eight-dimension MC namespace, and 03-03's complete artifact-patterns.md with its classification procedure and no-family fallback"
provides:
  - "SKILL.md trimmed of five named restatement regions before any addition, measured at each step, ending with a 236-token margin (up from 175 at plan entry)"
  - "Check mode's report now names four labelled sections in the frozen order (Integrity flags -> Prose violations -> Completeness gaps -> Structural ordering), each always printing, with the completeness section citing MC- numbers and the ordering section citing none"
  - "A standalone-audit instruction stating a writer can run the completeness audit alone and get the Completeness gaps verdict with no prose findings"
  - "The second Reference files pointer (references/artifact-patterns.md), completing SKILL.md's pointer coverage of all five reference files"
  - "README.md reconciled with disk: no false claim that the two Phase 3 reference files don't exist, worked-pair count corrected to 28"
  - "WINDOWS.md open entry routing the MC dimension-order paraphrase tension to Phase 6's LEG-04 gate"
  - "Provisional annotations on every Phase 3 requirement whose closure needs a live model session, in CAT-10's proven shape"
affects: [04, 05, 06]

# Actuals (#2632)
actuals:
  tokens: 5265
  tasks: 3
  commits: 3

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Trim-then-measure-then-add discipline, gated as its own acceptance criterion rather than assumed: post-trim word count checked and recorded before a single addition is authored, closing the exact ordering mistake Phase 2's 02-07 gap-closure plan had to retrofit"
    - "Mode-level instruction additions written as parallel sentences (Check mode's classification line mirrors Write mode's existing assumed-family line) rather than as a second, differently-worded convention"
    - "CAT-10's provisional-annotation shape (checkbox untouched, italic note stating implemented/unverified/why, the requirements-completed warning, a named closure condition) reproduced verbatim across nine requirements in one pass"

key-files:
  created: []
  modified:
    - skills/proof-first/SKILL.md
    - README.md
    - .planning/WINDOWS.md
    - .planning/REQUIREMENTS.md

key-decisions:
  - "Tracer feedback gate after Task 1: re-ran the automated <verify> commands and performed the <human-check> readings myself, consistent with 03-01/03-02/03-03's established precedent for spawned sessions with no human available to respond -- both passed, logged, and proceeded directly to Task 2."
  - "Post-trim measurement landed at 3539 words after the plan's own five named trim candidates (173 words), 9 words above the 3530 gate -- python's whitespace word-split counts slightly differently than the plan's prose word-count estimate. Found the additional 9+ words of restatement the plan itself flagged as the next candidate if the named list fell short: the Write-mode register illustration table's two example data rows (GAP/PF-2.11, REVIEW/PF-2.17), which demonstrate a shape the surrounding sentence and header row already fully specify. Removed the two data rows, kept the header row (the column shape stays specified), landed at 3511 words -- under the gate with no rule, Replace-with line, stated count, or distinct instruction touched."
  - "Two of the plan's own acceptance-criteria arithmetic checks did not match reality and were not force-fit: (1) Task 2's reference-files bullet-count check expects n==4, but SKILL.md already had 4 pointer bullets before this plan (03-01 added the completeness-audit.md pointer), so adding the required 5th bullet for artifact-patterns.md correctly makes 5, not 4 -- the plan's own read_first text even says 'the three existing bullets,' undercounting by one. (2) The README acceptance criterion expects the literal string 'references/completeness-audit.md' to appear >=2 times (once in the Status list, once in the layout tree), but the tree's own established format (which the plan's own action text says to preserve -- 'keeping the tree's column alignment consistent with its neighbours') lists bare filenames under a single 'references/' parent line, never repeating the parent path per child, exactly like every other reference file already in the tree. Kept both files in their correct, internally-consistent state (5 pointer bullets; 1 occurrence of the full path per file, consistent with every neighbouring entry) rather than breaking either established convention to satisfy a miscounted grep target."

requirements-completed: [MOD-03, MOD-04, MOD-05, AUD-03]

coverage:
  - id: D1
    description: "SKILL.md trimmed of five named restatement regions, measured before any addition (3712 -> 3511 words), then Check mode's classification sentence added and measured again (3548 words / 388-token margin)"
    requirement: null
    verification:
      - kind: other
        ref: "python3 -c \"...\" word-count checks at each step (post-trim 3511 <= 3530 gate; final 236 >= 150 gate)"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py (0 violations) and --self-test (all codes verified) after every edit"
        status: pass
    human_judgment: true
    rationale: "Whether the trim genuinely removed nothing but restatement, and whether the new sentences read as one coherent instruction rather than bolted-on additions, is prose-quality judgment. I performed both required <human-check> readings myself (see key-decisions) and both passed, but per this plan's own instructions this is recorded provisional pending end-of-phase UAT, not auto-passed off a self-check alone."
  - id: D2
    description: "Check mode's report names four labelled sections in the frozen order (Integrity flags, Prose violations, Completeness gaps, Structural ordering), each always printing; the completeness section cites MC- numbers, the ordering section cites no rule number"
    requirement: MOD-03
    verification:
      - kind: other
        ref: "python3 -c \"...\" section-order check (exits 0, all four present and in order); grep -c '^## ' (prints 13, none minted as a real heading)"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py --mutation-test (27 codes discrimination-proven, control 0 violations, no code fire-only)"
        status: pass
    human_judgment: true
    rationale: "This plan ships the four-section instruction text, not its live behaviour -- whether a real check-mode session actually prints four labelled sections, in that order, with a no-findings line in each empty one, is model behaviour no file-reading checker can observe. MOD-03 is listed in requirements-completed as implemented (not verified) per this plan's own <output> instructions; .planning/REQUIREMENTS.md carries the matching provisional annotation."
  - id: D3
    description: "Check mode names the artifact family it is reading the document as before reporting any finding, states the no-family-fits fallback, and points at references/artifact-patterns.md; the second Reference files pointer bullet completes coverage of all five reference files"
    requirement: MOD-04
    verification:
      - kind: other
        ref: "grep -cF 'references/artifact-patterns.md' skills/proof-first/SKILL.md (prints 2: the classification sentence and the Reference files bullet)"
        status: pass
    human_judgment: true
    rationale: "Whether a live session actually classifies a real document and states the family before applying any rule is model behaviour no file-reading checker can observe. MOD-04 is listed in requirements-completed as implemented (not verified); .planning/REQUIREMENTS.md carries the matching provisional annotation."
  - id: D4
    description: "A writer can ask for the completeness audit on its own; the standalone-run sentence states the run returns Completeness gaps and its verdict alone, with no prose findings and no rewritten document"
    requirement: AUD-03
    verification:
      - kind: other
        ref: "grep -cF 'references/completeness-audit.md' skills/proof-first/SKILL.md (prints 3: Reference files bullet, the completeness-gaps section sentence, the standalone-run sentence)"
        status: pass
    human_judgment: true
    rationale: "Whether a live session actually runs the audit alone and returns a separate verdict, with no prose findings, is model behaviour no file-reading checker can observe. AUD-03 is listed in requirements-completed as implemented (not verified); .planning/REQUIREMENTS.md carries the matching provisional annotation."
  - id: D5
    description: "Structural-ordering findings cite no rule number, because no numbered namespace covers artifact-family conventions -- MOD-05's no-invented-citation guarantee, extended to the new fourth section"
    requirement: MOD-05
    verification:
      - kind: other
        ref: "The Structural ordering sentence in SKILL.md's Check mode section explicitly states findings there cite no rule number; grep -c '^## ' unchanged at 13, confirming no PF-/MC- heading was minted"
        status: pass
    human_judgment: true
    rationale: "The shipped-file half is mechanically enforced (undefined-id, mc-catalog-id-drift, the MC count codes). Whether a live session in a fresh conversation never invents a number is permanently manual, no file-reading checker can observe it. MOD-05 was already Complete in .planning/REQUIREMENTS.md from 03-01; this plan's provisional annotation adds the live-session caveat that annotation was missing."
  - id: D6
    description: "README.md's Status list, worked-pair count, and layout tree reconciled with the repository on disk; a WINDOWS.md ledger entry routes the MC dimension-order paraphrase tension to Phase 6's LEG-04 gate; nine Phase 3 requirements carry CAT-10-shaped provisional annotations"
    requirement: null
    verification:
      - kind: other
        ref: "python3 -c \"...\" README checks (does-not-exist-yet bullet gone, worked-pair count 28==28, attribution pointer exactly 1); WINDOWS.md phase-03 row check (1 row, status open); REQUIREMENTS.md provisional-note checks (9/9 present, AUD-02 correctly absent, 12 checkbox lines unchanged)"
        status: pass
    human_judgment: false
patterns-established:
  - "Trim-before-add is a task-level gate with its own measured acceptance criterion, not a discretionary step -- the exact discipline Phase 2's own 02-07 gap-closure plan had to retrofit after skipping it once."

duration: 35min
completed: 2026-09-14
status: complete
---

# Phase 3 Plan 4: SKILL.md Token Budget Trim, Check-Mode Completion, and Documentation Reconciliation Summary

**SKILL.md trimmed of five restatement regions (measured before any addition), then completed with Check mode's classification line, the third and fourth report sections, a standalone-audit instruction, and the second reference pointer, ending at a 236-token margin (up from 175); README, WINDOWS.md, and REQUIREMENTS.md reconciled with the repository as it actually is.**

## Performance

- **Duration:** ~35 min
- **Completed:** 2026-09-14
- **Tasks:** 3
- **Files modified:** 4 (skills/proof-first/SKILL.md, README.md, .planning/WINDOWS.md, .planning/REQUIREMENTS.md)

## Accomplishments

- **Trim, measured first.** Removed five named restatement regions from `SKILL.md` — the marker-vocabulary first-occurrence/both-markers-fire paragraph (superseded by `PF-3.3`'s own body), the PF-2 closing paragraph restating the four REVIEW-category mappings (each already stated in its own raising rule), two Check-mode paragraphs restating `PF-5.1`–`PF-5.3`'s own check-mode prohibitions and the `checklist.md` citation pointer already stated at the Reference files section, and the trailing sentence of the marker-vocabulary register paragraph. Measured post-trim at 3539 words, 9 words above the plan's own 3530 gate (the plan's 173-word prose estimate and Python's whitespace-split count differ slightly); found the next restatement the plan itself flagged — the Write-mode register illustration table's two example data rows, which demonstrate a shape the header row and surrounding sentence already fully specify — removed them, kept the header row, landed at 3511 words, under the gate.
- **Check mode's classification line (Task 1, tracer).** Added one sentence opening `## Check mode`, parallel to Write mode's existing assumed-family sentence: names the artifact family before reporting any finding, states the no-family-fits fallback, points at `references/artifact-patterns.md` for the procedure rather than restating it. Measured at 3548 words / ~4612 estimated tokens / 388-token margin.
- **The third and fourth report sections (Task 2).** `## Completeness gaps` (citing its own `MC-` numbers) and `## Structural ordering` (citing no rule number, because no numbered namespace covers artifact-family conventions) now print in the frozen order after `## Integrity flags` and `## Prose violations`. The existing always-print sentence was edited in place ("Both category headings" → "All four section headings") rather than duplicated. Added the standalone-audit sentence (AUD-03) and the second Reference files pointer bullet for `references/artifact-patterns.md`. Final measured state: 3665 words / ~4764 estimated tokens / **236-token margin**.
- **CI green throughout, all gates re-measured at every step, not once at the end.** `python3 tools/check_repo.py --self-test && --mutation-test && (bare run)` — the exact CI job order — passes at every commit, with `python3 tools/check_repo.py --mutation-test` reporting **27 codes discrimination-proven** (unchanged; this plan adds no new violation code, `tools/check_repo.py` untouched, confirmed by `git diff --name-only` per task).
- **README.md reconciled with disk (Task 3).** Added Status-list bullets for `references/completeness-audit.md` and `references/artifact-patterns.md`, corrected the worked-examples pair count from 20 to 28 (matching `worked-examples.md`'s actual 28 `## ` sections), removed the now-false "does not exist yet" bullet naming the two Phase 3 reference files, and dropped their `(planned)` tag in the layout tree (4 `(planned)` entries remain, all genuinely absent). No measured claim added; the attribution pointer unchanged, carried exactly once.
- **WINDOWS.md ledger entry (id 6, open).** Routes the MC dimension-order paraphrase tension to Phase 6's LEG-04 gate: the eight MC dimension names and their MC-1–MC-40 ID-range order were frozen in `NUMBERING.md`/`REQUIREMENTS.md` before Phase 3 began and match MEDDICC's own acronym order; `SOURCES.md` states a source's own ordered list reproduced in its order is reproduction and that no tool in this stack performs that judgment; Phase 3 used content levers only and did not reorder or rename anything; the judgment itself is Phase 6 LEG-04's to make.
- **Provisional annotations (Task 3).** Reproduced CAT-10's exact shape — checkbox untouched, italic note stating what is implemented, what is unverified and why, the warning against re-marking Complete from a SUMMARY's `requirements-completed` field, and a named closure condition — on `AUD-01`, `AUD-03`, `ART-01` through `ART-04`, `MOD-03`, `MOD-04`, and `MOD-05`. `AUD-02` correctly took no annotation, since both its halves are mechanically enforced.

## Task Commits

1. **Task 1: End-to-end "the budget is bought, then spent" — the trim, then the Check-mode classification line only** — `9e859b0` (feat)
2. **Task 2: The third and fourth report sections, the standalone audit, and the second reference pointer** — `1cbbed0` (feat)
3. **Task 3: Make the repository's own documentation true — README, the ledger entry, and the provisional requirement marks** — `bcac0c6` (docs)

**Plan metadata:** (this commit, following)

## Files Created/Modified

- `skills/proof-first/SKILL.md` — trimmed five restatement regions, added Check mode's classification sentence, the third/fourth report sections, the standalone-audit sentence, and the second Reference files pointer bullet
- `README.md` — Status-list bullets for the two Phase 3 reference files, corrected worked-pair count, removed the false does-not-exist bullet, dropped the two `(planned)` tags
- `.planning/WINDOWS.md` — appended open entry id 6 (unrun-verify, phase 03) routing the MC ordering tension to LEG-04
- `.planning/REQUIREMENTS.md` — appended provisional annotations to 9 requirements (AUD-01, AUD-03, ART-01–04, MOD-03, MOD-04, MOD-05)

## Decisions Made

- **Tracer feedback gate after Task 1** and both `<human-check>` readings: resolved autonomously by reading the required material myself, matching 03-01/03-02/03-03's established precedent for spawned sessions with no human available to respond. Both passed. Details in the frontmatter `key-decisions` above.
- **Post-trim gate found short by 9 words**, closed by removing the Write-mode register illustration table's two example data rows (a candidate the plan itself named as the next restatement to check), not by touching any rule, `**Replace with:**` line, the stated count, or the marker grammar.
- **Two of the plan's own acceptance-criteria arithmetic checks did not match reality** (the Task 2 reference-bullet count expected 4 but the correct count is 5; the README pointer-occurrence count expected >=2 for a file but the established tree format, which the plan's own action text says to preserve, only ever states each file's full path once). Documented as deviations below rather than force-fit by breaking an established, explicitly-preserved convention.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Plan arithmetic error] Task 2's reference-files bullet-count acceptance criterion expected 4, correct count is 5**
- **Found during:** Task 2 verification
- **Issue:** The plan's acceptance criteria include `n==4` for the number of bullets in `## Reference files`, and Task 2's own `read_first` text describes "the three existing bullets." Both undercount by one: `03-01` already added the `completeness-audit.md` pointer bullet, so `SKILL.md` had **4** existing bullets (deletion-test, checklist, worked-examples, completeness-audit) before this plan started, not 3. Adding the required 5th bullet for `references/artifact-patterns.md` (explicitly required by this plan's own `must_haves` and `key_links`) correctly makes 5.
- **Fix:** Kept the correct, complete state — 5 pointer bullets, one per each of the 5 reference files that exist on disk, verified by listing `skills/proof-first/references/`. Did not delete a bullet to force the miscounted `n==4` check to pass.
- **Files modified:** `skills/proof-first/SKILL.md`
- **Verification:** `ls skills/proof-first/references/` confirms 5 files; the Reference files section carries exactly 5 bullets, one per file, in the same named-opening-condition shape.
- **Committed in:** `1cbbed0` (Task 2 commit)

**2. [Rule 1 - Plan arithmetic error] README acceptance criterion expected >=2 occurrences of a reference file's full path, established tree format only ever states it once**
- **Found during:** Task 3 verification
- **Issue:** The plan's acceptance criteria expect `grep -cF 'references/completeness-audit.md' README.md` to print at least 2 ("once in the Status list and once in the layout tree"). The layout tree's established format (explicitly preserved per this same task's own action text: "keeping the tree's column alignment consistent with its neighbours") lists a single `references/` parent line followed by bare child filenames — exactly like `checklist.md`, `deletion-test.md`, and `worked-examples.md` already do — never repeating the full `references/` prefix per child line. The literal string therefore appears once, in the Status-list bullet, for every reference file, including the two this task added.
- **Fix:** Kept the tree in its correct, internally-consistent format (bare filenames, `(planned)` removed only from the two files that now exist) rather than breaking the established convention for two files only to inflate a grep count.
- **Files modified:** `README.md`
- **Verification:** Layout tree read end-to-end — all 5 reference files listed consistently, none carrying a repeated `references/` prefix; the same true for every pre-existing sibling entry.
- **Committed in:** `bcac0c6` (Task 3 commit)

---

**Total deviations:** 2 auto-fixed (both Rule 1 — plan-authored arithmetic errors caught by the plan's own other, more authoritative requirements: `must_haves`, `key_links`, and the explicit "keep column alignment consistent with neighbours" instruction in the same task). **Impact on plan:** Neither deviation changed scope or content quality; both resolved a hardcoded numeric check that conflicted with the plan's own descriptive instructions in the same task, in favor of the descriptive instructions and the actual, correct repository state.

## Issues Encountered

None beyond the two deviations above, both caught and resolved within the same task's verification loop before committing.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Phase 3 is content-complete: all eight MC dimensions, all four artifact families, and `SKILL.md`'s full four-section check-mode report, classification line, standalone-audit instruction, and complete reference-pointer coverage are all shipped and CI-proven at 27 discrimination-proven codes with a 236-token margin.
- `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py` — the exact CI job order — is green. `tools/check_repo.py` is byte-identical to its pre-plan state (confirmed via `git diff --name-only` per task: only `SKILL.md`, `README.md`, `.planning/WINDOWS.md`, and `.planning/REQUIREMENTS.md` changed across all three tasks).
- **Provisional, not fully verified:** every one of `AUD-01`, `AUD-03`, `ART-01` through `ART-04`, `MOD-03`, `MOD-04`, and `MOD-05` has a live-model-session or content-quality half no file-reading checker in this repository can observe, recorded above as `human_judgment: true` and annotated provisionally in `.planning/REQUIREMENTS.md`, per this plan's own instructions. `MOD-03`, `MOD-04`, `AUD-03`, and (already-Complete) `MOD-05`'s live-session half all share the same closure condition: a live harness session recorded at the Phase 3 UAT pass.
- The two pre-existing open `WINDOWS.md` entries (ids 3 and 4) are unchanged by this plan and restated below verbatim for `/gsd-verify-work`, per `02-09-SUMMARY.md`'s precedent:
  - **id 3** (phase 02, `skills/proof-first/SKILL.md`): "Tracer feedback human-check (02-01 Task 1): SOURCES.md reproduction-boundary read plus PF-0.1/PF-3.1 framing judgment (CAT-03/CAT-04 flagged assumptions A-03/A-04) - signed off at end-of-phase UAT 2026-09-11 (02-UAT.md test 1, result pass); stays open because the formal reproduction-boundary gate is Phase 6 LEG-04"
  - **id 4** (phase 02, `evals/pressure-tests.md`): "D-31 trigger pressure-test: must-fire/must-not-fire phrasings recorded with method only — this environment cannot drive a fresh harness session to install the skill and observe activation, so every Observed cell reads 'not yet observed'; a human must run each phrasing in a real harness session and fill in Observed/Date/Harness before this is fixed"
- A new open entry (id 6, phase 03) was added by this plan, routing the MC dimension-order paraphrase tension to Phase 6's LEG-04 gate — see Accomplishments above for its full statement.
- Phase 4 (distribution) and Phase 5 (eval harness) can both proceed against a complete, budget-proven `SKILL.md` with no remaining Phase 3 gaps.

## Self-Check: PASSED

- FOUND: skills/proof-first/SKILL.md, README.md, .planning/WINDOWS.md, .planning/REQUIREMENTS.md
- FOUND commits: 9e859b0, 1cbbed0, bcac0c6
- Re-ran `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py` — all pass; mutation-test reports `PASS: 27 codes discrimination-proven`, `CONTROL: 0 violations`, no code fire-only
- `skills/proof-first/SKILL.md` final measured state: 3665 words / ~4764 estimated tokens / 236-token margin (re-verified via `python3 -c "import pathlib;w=len(pathlib.Path('skills/proof-first/SKILL.md').read_text().split());print(w, int(w*1.3), 5000-int(w*1.3))"`)
- `tools/check_repo.py` confirmed untouched: `git diff 7a332d5..HEAD -- tools/check_repo.py` empty
- All invariants re-verified at HEAD: 31/31 rule/Replace-with parity, 31 rules each with exactly one constructive half, stated catalog count exactly 1, attribution pointer exactly 1, register heading exactly 1, 4 REVIEW categories, 3 marker bracket forms, 13 real headings

---
*Phase: 03-completeness-audit-artifact-patterns*
*Completed: 2026-09-14*
