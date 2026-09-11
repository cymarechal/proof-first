---
phase: 02-rule-catalog-integrity-skill-md-core
plan: 06
subsystem: enforcement
tags: [check-repo, ci, frontmatter, agent-skills, mutation-test, self-test, cat-08, token-budget]

# Dependency graph
requires:
  - phase: 02-rule-catalog-integrity-skill-md-core
    provides: "02-01 through 02-05's completed 31-rule catalog, NUMBERING.md's PF-1/PF-2 sub-block tables, and skills/proof-first/SKILL.md's frontmatter, stated-count sentence, and dewrapped 368-line body"
provides:
  - "Four new frontmatter-integrity codes (frontmatter-unparseable, frontmatter-unknown-key, frontmatter-name-mismatch, frontmatter-description-invalid) enforcing the Agent Skills six-key allow-list, name==directory, and a 200-1024 character description bound (D-33), via a stdlib-only targeted parser"
  - "Two stated-count codes (catalog-count-unstated, catalog-count-mismatch) binding SKILL.md's stated rule/section count sentence to NUMBERING.md's registry (D-32)"
  - "skill-too-long: a 500-line CAT-08 gate with boundary fixtures at 500/501"
  - "PF sub-block containment enforced through the existing range-id code (D-05's Proof/Integrity boundary is now CI-checked, not just documented)"
  - "skill-token-budget-exceeded: an eighth code (authorized scope addition) enforcing CAT-08's token half via a word-count*1.3 proxy, currently and correctly firing against the real SKILL.md -- an open, tracked finding, not a defect"
  - "21 violation codes proven live via --mutation-test; 21 codes proven via --self-test; .github/workflows/ci.yml unchanged"
affects: [03]

# Actuals (#2632)
actuals:
  tokens: 12258
  tasks: 2
  commits: 2

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A targeted, stdlib-only frontmatter extractor (parse_frontmatter) mirrors parse_notices's established style: isolate a delimited block, scan column-zero keys line by line, treat a `|` block scalar and a nested map's indented lines as opaque text rather than parsing general config-format semantics -- extends this file's 'just enough parsing' precedent to a fourth document shape without adding any config-format library"
    - "A stated-count sentence anchored to a registry (COUNT_SENTENCE_RE matched byte-exactly, never fuzzily) is the same anti-hallucination mechanism as an ID allow-list, applied to a document's own self-description rather than to individual citations"
    - "A CI check that already, correctly fires against real content on day one (skill-token-budget-exceeded) requires a narrow, explicitly named and commented carve-out in the shared mutation-test CONTROL invariant (KNOWN_OPEN_VIOLATIONS) so that one honest, tracked finding does not silently mask a different, unexpected regression introduced later -- a real design tension when a new check's correct behavior is to fail on the unmutated repository"

key-files:
  modified:
    - tools/check_repo.py
    - .planning/WINDOWS.md

key-decisions:
  - "Implemented the plan's seven codes and the authorized eighth code (skill-token-budget-exceeded) as two commits rather than three: Task 1 and Task 2 are committed together (both are pure additions to the same file's existing check/mutation/self-test registries with no independently meaningful intermediate state beyond what the plan's own acceptance criteria already describe), and the authorized scope addition is committed separately so the boundary between 'the plan as written' and the user-authorized extra scope stays visible in git history."
  - "Used 'author' rather than 'compatibility' as the unknown-frontmatter-key fixture/mutation target. The plan's own action text names 'compatibility' as the unknown-key mutation, but compatibility IS one of the Agent Skills specification's six allowed keys per the plan's own interfaces table (D-33) -- this project simply omits it by convention (D-29/D-30). Following the plan literally would have made frontmatter-unknown-key's mutation and self-test fixture silently prove nothing, exactly the class of defect this whole phase exists to close. Fixed as a Rule 1 auto-fix; documented under Deviations below."
  - "skill-token-budget-exceeded estimates tokens as word_count * 1.3, calibrated against 02-RESEARCH.md's own sibling-skill measurement (simple-english/SKILL.md: 3,664 words, recorded under the ~5,000-token ceiling; 3,664 * 1.3 ~ 4,763, consistent with that recorded finding). The alternative proxy the authorized-scope text also offered (chars/4) was not chosen as the enforced check, since it would set an effectively stricter, uncalibrated ceiling for this specific file shape; chars/4's ~7,404-token estimate is reported in this SUMMARY and in WINDOWS.md as a second, cross-checking figure, not silently discarded."
  - "mutation-test's CONTROL step now tolerates exactly one named, already-true violation (skill-token-budget-exceeded, via KNOWN_OPEN_VIOLATIONS) rather than failing outright, so that CI can still assert 'no OTHER code has an unexpected violation' while the token-budget finding stays visibly reported by the live check_repo.py run and by --mutation-test's own CONTROL line. This was necessary engineering to reconcile 'the check must correctly fire against real content today' with '--mutation-test must still pass, proving 21 codes live' -- both explicit requirements of this plan and its authorized addition."
  - "Did not resolve the CAT-08 token-budget finding by re-wrapping SKILL.md, moving rule content into references/, or raising the ceiling -- per explicit instruction, the finding is reported and logged (WINDOWS.md entry 5), not silenced."

patterns-established:
  - "Declared-ceiling docstring paragraphs now cover 8 new/extended codes in the same two-part shape (what it catches, then an explicit 'Declared ceiling:' sentence) as every pre-existing code -- 14 total 'Declared ceiling' occurrences in the module docstring."

requirements-completed: [CAT-01, CAT-08, CAT-09]

coverage:
  - id: D1
    description: "Four frontmatter-integrity codes (frontmatter-unparseable, frontmatter-unknown-key, frontmatter-name-mismatch, frontmatter-description-invalid) proven via --self-test (boundary fixtures at the 200/1024 description bounds, a reordered-but-valid fixture, a duplicate-key fixture) and via --mutation-test against the real skills/proof-first/SKILL.md"
    requirement: "CAT-09"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --self-test -- PASS, lists all 21 codes including all 4 frontmatter codes"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py --mutation-test -- PASS, 21 codes proven live, includes all 4 frontmatter codes"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py (live run) -- reports only skill-token-budget-exceeded; every frontmatter code is silent against the real skills/proof-first/SKILL.md"
        status: pass
    human_judgment: false
  - id: D2
    description: "Two stated-count codes (catalog-count-unstated, catalog-count-mismatch) bind SKILL.md's 'This catalog contains N rules in M numbered sections.' sentence to NUMBERING.md's registry in both directions (rule-count and section-count)"
    requirement: "CAT-01"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --self-test -- PASS, both codes fire on isolated fixtures and stay silent on a matching fixture"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py --mutation-test -- PASS, catalog-count-mismatch's registered mutation changes the rule-count number; the section-count direction was additionally verified by an ad hoc scratch-copy run (documented in this SUMMARY's Deviations/verification notes) confirming the same code fires"
        status: pass
    human_judgment: false
  - id: D3
    description: "skill-too-long enforces the 500-line half of CAT-08 with boundary fixtures at exactly 500 (silent) and 501 (fires); PF sub-block containment is enforced through the existing range-id code (D-05), with a gapped-fixture proof and confirmation that the real NUMBERING.md's PF-1 and PF-2 sub-block tables both fully tile their sections' reserved ranges"
    requirement: "CAT-08"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --self-test -- PASS, both boundary fixtures assert correctly; the gapped sub-block fixture fires range-id"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py (live run) -- skill-too-long and range-id are both silent against the real repository (368 lines; every PF ID sits inside its declared sub-block)"
        status: pass
    human_judgment: false
  - id: D4
    description: "skill-token-budget-exceeded (authorized scope addition): an eighth code enforcing CAT-08's token half via a word_count*1.3 proxy calibrated against the sibling skill's own measured shape, registered in MUTATIONS and proven live, and CORRECTLY firing against the real skills/proof-first/SKILL.md (estimated 6,207 tokens against the 5,000-token ceiling) -- the accepted, expected outcome per the authorized scope, not a defect"
    requirement: "CAT-08"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --self-test -- PASS, fires on a high-word-count fixture and stays silent on a low-word-count fixture"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py --mutation-test -- PASS, 21 codes proven live including skill-token-budget-exceeded; CONTROL line explicitly reports 1 known-open violation, 0 unexpected"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py (live run) -- prints exactly one line: skill-token-budget-exceeded skills/proof-first/SKILL.md is estimated at 6207 tokens (4775 words x 1.3), exceeding the 5000-token ceiling"
        status: pass
    human_judgment: true
    rationale: "Whether this finding should be resolved by trimming the 31-rule catalog's prose volume, restructuring content into references/, or accepting the ceiling as advisory for v1 is a content/scope decision this plan is explicitly barred from making (must not re-architect the catalog, must not raise the ceiling, must not re-wrap). A human (or a future planning session) must decide the remediation path; this plan's job was only to make the finding visible and CI-enforced, which it does."

duration: 22min
completed: 2026-09-11
status: complete
---

# Phase 2 Plan 6: Rule Catalog & Frontmatter Integrity — Eight New CI Codes, 21 Proven Live Summary

**Seven planned CI codes (frontmatter validity, stated-count/registry binding, the 500-line ceiling, PF sub-block containment) plus an eighth authorized addition enforcing CAT-08's token half — which correctly and expectedly fires against the real `skills/proof-first/SKILL.md` at an estimated 6,207 tokens against its 5,000-token ceiling, a real content-volume finding now CI-visible rather than silently unenforced.**

## Performance

- **Duration:** 22 min
- **Started:** 2026-09-11T01:26:00Z
- **Completed:** 2026-09-11T01:48:00Z
- **Tasks:** 2 (both `type="auto"`) plus 1 authorized scope addition
- **Files modified:** 2 (`tools/check_repo.py`, `.planning/WINDOWS.md`)

## Accomplishments

- **Task 1 — Frontmatter parser and its four codes:** Added `parse_frontmatter` (a targeted, stdlib-only extractor in `parse_notices`'s established style — no config-format library, per D-33), `check_frontmatter`, `ALLOWED_FRONTMATTER_KEYS`/`REQUIRED_FRONTMATTER_KEYS`/`DESCRIPTION_MIN`/`DESCRIPTION_MAX`. Four new codes: `frontmatter-unparseable` (no `---` block, unterminated block, missing required key, or repeated top-level key — the first value is kept, never silently overwritten), `frontmatter-unknown-key`, `frontmatter-name-mismatch`, `frontmatter-description-invalid` (silent at both the 200 and 1024 character bounds, firing one character past either). All four proven via hand-built self-test fixtures (including a reordered-but-valid fixture that fires nothing) and via mutation against the real `skills/proof-first/SKILL.md`.
- **Task 2 — Stated count, line ceiling, and PF sub-block containment:** Added `COUNT_SENTENCE_RE` and `check_catalog_count` (`catalog-count-unstated`, `catalog-count-mismatch`, binding SKILL.md's stated rule/section count to `NUMBERING.md`'s registry in both directions); `SKILL_LINE_CEILING = 500` and `check_skill_too_long` (`skill-too-long`, silent at exactly 500, firing at 501); `parse_pf_subblocks` and an extension to `check_range_id` enforcing D-05's Proof/Integrity sub-block boundary through the existing `range-id` code (a gapped-table self-test fixture proves it fires; the real `NUMBERING.md`'s PF-1 and PF-2 sub-block tables both fully tile their sections, so the real registry produces no violation). 20 violation codes proven live at this point; live `check_repo.py` run: `check_repo: 0 violations`.
- **Authorized scope addition — `skill-token-budget-exceeded` (CAT-08's token half):** Added `check_skill_token_budget`, estimating each `skills/*/SKILL.md`'s token count as `word_count * 1.3` — a ratio calibrated against `02-RESEARCH.md`'s own measurement of the sibling skill (`simple-english/SKILL.md`: 3,664 words, recorded comfortably under the same ~5,000-token ceiling; 3,664 × 1.3 ≈ 4,763, consistent with that finding). Registered in `MUTATIONS` and proven live. **This code correctly and expectedly fires against the real `skills/proof-first/SKILL.md`**, estimated at 6,207 tokens (4,775 words × 1.3) against the 5,000-token ceiling — a 24% overage on this estimator (a second estimator, characters ÷ 4, gives 7,404 tokens — a 48% overage; both figures are reported here and in WINDOWS.md, neither silently discarded). 21 violation codes now proven live. Per the explicit authorized-scope instruction, this finding was **not** resolved by re-wrapping SKILL.md, moving rule content to `references/`, or raising the ceiling — it is reported and logged as an open item.

## Task Commits

1. **Task 1 + Task 2: frontmatter validity, stated-count/registry binding, 500-line ceiling, PF sub-block containment** — `25421a3` (feat)
2. **Authorized scope addition: `skill-token-budget-exceeded`, CAT-08's token half** — `96e7a35` (feat)

**Plan metadata commit:** recorded below after STATE.md/ROADMAP.md/REQUIREMENTS.md updates.

## Files Created/Modified

- `tools/check_repo.py` — 8 new violation codes (7 planned + 1 authorized addition), `parse_frontmatter`/`check_frontmatter`/`FRONTMATTER_CHECK_CODES`/`run_frontmatter_checks`, `check_catalog_count`/`COUNT_SENTENCE_RE`, `check_skill_too_long`/`SKILL_LINE_CEILING`, `parse_pf_subblocks` and an extended `check_range_id`, `check_skill_token_budget`/`SKILL_TOKEN_WORDS_PER_TOKEN_RATIO`/`SKILL_TOKEN_CEILING`, `KNOWN_OPEN_VIOLATIONS`, 8 new `_mutate_*` functions and `MUTATIONS` entries, and matching self-test fixtures/assertions for every code
- `.planning/WINDOWS.md` — new open `unmet-truth` entry (id 5) recording the CAT-08 token-budget finding

## Decisions Made

See `key-decisions` in frontmatter above for full rationale. Summary:
- Task 1 and Task 2 committed together (both are additions to the same shared registries with no independently meaningful intermediate state); the authorized addition committed separately so the plan/addition boundary stays visible in git history.
- Fixed the plan's own "add a `compatibility:` key" instruction for the unknown-key mutation/fixture — `compatibility` is one of the Agent Skills specification's six *allowed* keys (per the plan's own interfaces table), so using it would have silently proven nothing. Used `author` instead.
- Chose `word_count * 1.3` as the token-budget estimator (calibrated against the sibling skill's own recorded-under-ceiling measurement), reporting `chars / 4` as a second cross-checking figure rather than the enforced metric.
- Added a narrow `KNOWN_OPEN_VIOLATIONS` allowance to `mutation_test()`'s CONTROL step so one already-true, tracked violation doesn't mask a different regression later, while every other code keeps the original unweakened "zero violations on an unmutated copy" bar.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug in the plan's own action text] `compatibility` is an allowed key, not an unknown one — used `author` instead**
- **Found during:** Task 1, writing `_mutate_frontmatter_unknown_key` and `_bad_frontmatter`
- **Issue:** The plan's Task 1 action text literally instructs "add a `compatibility:` key" as the injected defect for the `frontmatter-unknown-key` mutation. But the plan's own `<interfaces>` table lists `compatibility` as one of the Agent Skills specification's six *allowed* frontmatter keys (`license | no`, `compatibility | no | 1-500 chars free text; this project omits it`, `metadata | no`, `allowed-tools | no`) — this project simply omits it by convention (D-29/D-30), it does not forbid it. Following the plan literally made `--self-test` fail immediately: `compatibility` passed the allow-list check silently, proving nothing about `frontmatter-unknown-key`.
- **Fix:** Used `author` (a key with no meaning in the Agent Skills specification at all) as both the self-test fixture's and the mutation's injected defect, with an inline comment in the code explaining why `compatibility` was deliberately avoided.
- **Files modified:** `tools/check_repo.py`
- **Verification:** `python3 tools/check_repo.py --self-test` — PASS, `frontmatter-unknown-key` fires on the bad fixture and stays silent on every good fixture; `python3 tools/check_repo.py --mutation-test` — `mutation-test OK: frontmatter-unknown-key`.
- **Committed in:** `25421a3` (Task 1/2 commit)

---

**Total deviations:** 1 auto-fixed (1 Rule-1 bug — a plan-text/interfaces-table self-contradiction that would have shipped an inert mutation and fixture, exactly the class of defect D-34 exists to prevent).
**Impact on plan:** No scope creep. The fix changes only which literal string is injected as the "unknown key" test defect; the code, the four frontmatter codes, and every other fixture are unaffected.

### Authorized Scope Addition (not a deviation — user-approved before execution)

Per the explicit `<authorized_scope_addition>` in this execution's instructions, an eighth violation code (`skill-token-budget-exceeded`) was added beyond `02-06-PLAN.md`'s seven. This is documented as its own commit and its own coverage entry (D4) above, not folded silently into the plan's own scope. See "CAT-08 Token-Budget Open Finding" below for the required prominent report.

## CAT-08 Token-Budget Open Finding (accepted and expected)

**This is the intended, correct outcome of this plan's authorized scope addition, not a bug or a regression.**

- **Measured:** `skills/proof-first/SKILL.md` is 368 lines (well under the 500-line ceiling — `skill-too-long` is silent) but its estimated token count exceeds CAT-08's stated "~5,000 tokens" ceiling:
  - **Chosen estimator (word_count × 1.3):** 4,775 words × 1.3 ≈ **6,207 estimated tokens** — a **24%** overage.
  - **Cross-check estimator (chars ÷ 4):** 29,616 characters ÷ 4 = **7,404 estimated tokens** — a **48%** overage.
- **Why this is real, not a formatting artifact:** 02-05 already dewrapped SKILL.md's entire prose body (480 → 368 lines, zero content change) before this plan ran. The line count is comfortably under budget; the word/character volume is not. This is a genuine content-volume finding — the 31-rule catalog's prose is too large for the progressive-disclosure budget CAT-08 sets, independent of how its line breaks fall.
- **What was deliberately NOT done to make this pass:** the 500-token ceiling was not raised; SKILL.md was not re-wrapped or reformatted; no rule content was moved into `references/` (re-architecting the 31-rule catalog is a content decision affecting every rule and is out of scope for this plan).
- **Logged:** `.planning/WINDOWS.md` entry id 5 (`unmet-truth`, phase 02, open), naming the file, both estimator figures, and the remediation guidance (trim or restructure catalog content in a future plan; do not resolve by reformatting or raising the ceiling).
- **CI consequence:** the live `python3 tools/check_repo.py` run now exits 1 (one violation line) instead of 0. `--self-test` and `--mutation-test` both still exit 0 (fixture-based and mutation-based proofs are unaffected by this real-content finding; `--mutation-test`'s CONTROL step explicitly reports it as 1 known-open, 0 unexpected violation via `KNOWN_OPEN_VIOLATIONS`). This means `.github/workflows/ci.yml`'s existing three-step job (unchanged by this plan) will now go red at its third step until a future plan resolves the catalog's content volume — this is the expected, authorized consequence of implementing the token half of CAT-08 honestly.

## Issues Encountered

None beyond the deviation documented above.

## Authentication Gates

None — no external service or CLI authentication was required.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- 21 violation codes are proven live (`--self-test` and `--mutation-test` both PASS); `tools/check_repo.py` remains standard-library only (`grep -c 'yaml'` → 0); `.github/workflows/ci.yml` is unchanged (`git diff --stat` empty, 3 `check_repo.py` invocations confirmed).
- CAT-01, CAT-08, and CAT-09 are now CI-enforced, not merely documented: the stated rule/section count, the frontmatter's validity, the 500-line ceiling, PF sub-block containment, and (via the authorized addition) the token-budget half of CAT-08 all fail the build when violated, with every code's declared ceiling stated plainly in the module docstring.
- **Open blocker for a future phase or plan:** the CAT-08 token-budget finding (WINDOWS.md id 5) needs a content decision — trim the 31-rule catalog's prose volume or restructure detail into `references/` — before the live `check_repo.py` run (and therefore CI) returns to green. This is explicitly NOT this plan's decision to make.
- Phase 2's five requirements this plan covers (CAT-01, CAT-08, CAT-09) are now marked complete in REQUIREMENTS.md's traceability table; INT-01 through INT-06, MOD-01/MOD-02, and the remaining CAT-0x requirements were already complete via 02-01 through 02-05.
- No other blockers for Phase 3.

## Self-Check: PASSED

- `[ -f tools/check_repo.py ]` → FOUND
- `[ -f .planning/WINDOWS.md ]` → FOUND
- `git log --oneline --all | grep -q 25421a3` → FOUND
- `git log --oneline --all | grep -q 96e7a35` → FOUND
- `python3 tools/check_repo.py --self-test` → PASS, 21 codes verified
- `python3 tools/check_repo.py --mutation-test` → PASS, 21 codes proven live, exit 0
- `python3 tools/check_repo.py` → exit 1, prints exactly one line (`skill-token-budget-exceeded` against the real SKILL.md) — the accepted, expected outcome
- `grep -nE '^(import|from) ' tools/check_repo.py` → only stdlib modules (argparse, re, shutil, sys, tempfile, pathlib)
- `grep -c 'yaml' tools/check_repo.py` → 0
- `git diff --stat .github/workflows/ci.yml` → empty (no change)
- `grep -c 'check_repo.py' .github/workflows/ci.yml` → 3
- `python3 tools/check_repo.py --help` → exit 0, documents only `--self-test`/`--mutation-test`
- Every PF ID in the real `NUMBERING.md` sits inside its section's declared sub-block (confirmed via direct `check_range_id` call against real data — zero violations)
- `catalog-count-mismatch`'s section-count direction (not just its registered mutation's rule-count direction) independently confirmed to fire via an ad hoc scratch-copy run

---
*Phase: 02-rule-catalog-integrity-skill-md-core*
*Completed: 2026-09-11*
