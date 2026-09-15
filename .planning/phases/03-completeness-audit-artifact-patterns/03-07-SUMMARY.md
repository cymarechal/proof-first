---
phase: 03-completeness-audit-artifact-patterns
plan: 07
subsystem: skill-content
tags: [mod-04, artifact-family, source-labels, check-repo, gap-closure]

# Dependency graph
requires:
  - phase: 03-completeness-audit-artifact-patterns
    provides: "03-06's conformance instrument (evals/conformance/run_conformance.py), the committed measurement tool 03-08 uses against this plan's SKILL.md content change"
provides:
  - "SKILL.md: the artifact-family line redefined as an always-printed, five-value element (Write mode) and gated in the first of three self-check passes -- two levers different in kind from 03-05's restatement"
  - "artifact-patterns.md/completeness-audit.md: last source-coined label removed, standalone-audit shape statement aligned with the accepted AUD-03 criterion"
  - "tools/check_repo.py: two new discrimination-proven codes (skill-family-line-gate-missing, source-label-in-skill-content), 27 -> 29"
  - "WINDOWS.md entries 7 and 9 disposed as fixed"
affects: [03-08-plan-mod04-measurement]

# Actuals (#2632)
actuals:
  tokens: 8400
  tasks: 3
  commits: 4

tech-stack:
  added: []
  patterns:
    - "A new violation code only counts toward the discrimination-proven total once it has a registered MUTATIONS row proven silent-on-control and firing-on-mutation -- the same discipline every prior Phase 3 catalog code followed."
    - "A checker declares its ceiling in its own docstring at the moment it ships, not retrofitted later -- skill-family-line-gate-missing's docstring states outright that it cannot verify MOD-04 mechanically, only that the instruction text is present."

key-files:
  created: []
  modified:
    - skills/proof-first/SKILL.md
    - skills/proof-first/references/artifact-patterns.md
    - skills/proof-first/references/completeness-audit.md
    - tools/check_repo.py
    - .planning/WINDOWS.md

key-decisions:
  - "The Write-mode five-value list and the self-check family-line pass both spell the no-family value '**No family fits:**' byte-identical to references/artifact-patterns.md -- verified by direct grep -o comparison, not just visual inspection, since a reworded copy would stop matching both the reference file and the new check."
  - "The Business case paragraph's appositive replacement ('the person who signs') was initially split across a soft line-wrap, reproducing the exact defect class this repo's own 02-04 and 03-06 plans already hit and fixed the same way -- moved the wrap point, left the check and the wording alone."
  - "SOURCE_COINED_LABELS holds exactly 7 entries by encoding the singular/plural problem-word pair as one entry ('pain') matched with an optional trailing 's', not as two separate list entries -- keeping the acceptance criterion's '7 entries' literal while still catching 'pains'."
  - "The ordinary-English word for a measurement ('metric') is deliberately excluded from SOURCE_COINED_LABELS and proven silent via a dedicated self-test fixture, not just asserted in the docstring -- this repo's own MC-1 and PF-1 Metrics sub-block use that word legitimately."
  - "MOD-04 stays [ ] and REQUIREMENTS.md is untouched by this plan, per the plan's own objective and the project's own history of over-claiming from requirements-completed -- verified with grep -c \"^- \\[x\\].*UNVERIFIED\" returning 0."

patterns-established:
  - "A model-behaviour requirement (MOD-04) gets two independent levers in the same plan -- an always-emitted output value and a pre-return mechanical gate -- rather than a third restatement of the same instruction, because 03-05's restatement-only fix measurably failed to move the rate."

requirements-completed: []  # This plan pulls content levers only. It does not close MOD-04 or
  # any other requirement -- 03-08-PLAN.md owns running the actual conformance measurement
  # and the closure decision. REQUIREMENTS.md checkboxes are untouched by this plan
  # (grep -c "^- \[x\].*UNVERIFIED" .planning/REQUIREMENTS.md returns 0).

coverage:
  - id: D1
    description: "SKILL.md's Write mode defines the artifact-family line as always-printed with five values including the no-family fallback, spelled byte-identical to artifact-patterns.md"
    requirement: "MOD-04"
    verification:
      - kind: other
        ref: "grep -o '\\*\\*No family fits:\\*\\*' on both files -- byte match; grep -cF 'No family fits' skills/proof-first/SKILL.md == 2"
        status: pass
    human_judgment: false
  - id: D2
    description: "Self-check before delivering gates on the family line in its first of three named passes"
    requirement: "MOD-04"
    verification:
      - kind: other
        ref: "grep -c 'three named passes' skills/proof-first/SKILL.md == 1; source read of the renumbered list"
        status: pass
    human_judgment: false
  - id: D3
    description: "SKILL.md stays under the 5000-token ceiling with margin re-measured"
    requirement: "N/A"
    verification:
      - kind: unit
        ref: "python3 -c \"...\" -- 3757 words, 4884 estimated tokens, 116-token margin"
        status: pass
    human_judgment: false
  - id: D4
    description: "Zero frozen source-coined dimension labels remain in shipped skill content"
    requirement: "N/A"
    verification:
      - kind: other
        ref: "grep -rniE over skills/ for the 7 frozen labels -- 0 hits"
        status: pass
    human_judgment: false
  - id: D5
    description: "completeness-audit.md's standalone-audit shape statement agrees with SKILL.md line 288 and the accepted AUD-03 criterion"
    requirement: "AUD-03"
    verification:
      - kind: other
        ref: "source read of 'Running the audit on its own' closing clause; forbidden-heading-at-line-start count == 0"
        status: pass
    human_judgment: false
  - id: D6
    description: "Two new violation codes wired through all seven touch points, discrimination-proven"
    requirement: "N/A"
    verification:
      - kind: unit
        ref: "python3 tools/check_repo.py --self-test (29 codes) and --mutation-test (29 discrimination-proven, CONTROL 0 unexpected)"
        status: pass
    human_judgment: false
  - id: D7
    description: "WINDOWS.md entries 7 and 9 disposed as fixed, entry 8 left untouched for 03-08"
    requirement: "N/A"
    verification:
      - kind: other
        ref: "gsd-tools windows status -- entries 7 and 9 'fixed', entry 8 'open'"
        status: pass
    human_judgment: false

duration: 25min
completed: 2026-09-15
status: complete
---

# Phase 03 Plan 07: Family-Line Levers, Last Source Label, and Two New Discrimination-Proven Codes Summary

**Made the artifact-family line an always-printed, five-value SKILL.md output with a pre-return self-check gate (WINDOWS.md entry 8's lever, not its measurement); removed the last frozen source-coined label from shipped skill content and aligned the standalone-audit shape statement with the accepted AUD-03 criterion; added two new discrimination-proven check_repo.py codes, taking the mutation-proven total from 27 to 29.**

## Performance

- **Duration:** 25 min
- **Tasks:** 3/3 completed
- **Files modified:** 5

## Accomplishments

- `SKILL.md`'s `## Write mode` first sentence redefined: output is exactly three parts (family line, prose, register), and the family line always prints one of five values -- the four named families or `**No family fits:**` followed by the family-independent rules only, spelled byte-identical to `references/artifact-patterns.md`. A document the session cannot place now takes that fifth value instead of taking silence.
- `SKILL.md`'s `## Self-check before delivering` gained a third named pass: item 1 (new), the family-line pass, gates delivery on the response's first line naming the family or stating `**No family fits:**`. The pre-existing subtractive pass and additive sweep kept their bodies, renumbered 2 and 3.
- Token budget re-measured: 3700 -> 3757 words, 4810 -> 4884 estimated tokens, margin 190 -> 116 (floor 100, held).
- `artifact-patterns.md`'s `**Business case:**` paragraph: `Diane Osoria, the economic buyer` -> `Diane Osoria, the person who signs` (already used twice in the same section) -- the last frozen `NUMBERING.md` registry label used as this repository's own unattributed noun in shipped skill content, closing `WINDOWS.md` entry 9.
- `completeness-audit.md`'s `## Running the audit on its own` closing clause rewritten to state the same boundary `SKILL.md` line 288 and the `AUD-03` criterion state: no `## Integrity flags`, `## Prose violations`, or `## Structural ordering` sections, and naming the artifact family read is permitted and is not a finding -- closing `WINDOWS.md` entry 7.
- `tools/check_repo.py` gained `skill-family-line-gate-missing` (fires when a present self-check section names neither anchor; silent when the section is absent entirely -- the declared ceiling every pre-existing synthetic fixture depends on) and `source-label-in-skill-content` (scans `SKILL.md` and its `references/*.md` for `SOURCE_COINED_LABELS`, 7 frozen entries, deliberately excluding the ordinary-English word for a measurement). Both wired through all seven touch points: docstring, check function, `CATALOG_CHECK_CODES`, `run_catalog_checks`, self-test bad fixtures + assertions, and a `MUTATIONS` row.
- `--self-test` names 29 verified codes; `--mutation-test` reports `mutation-test PASS: 29 codes discrimination-proven` with `CONTROL: 0 violations ... (0 unexpected)`; the bare run still prints `check_repo: 0 violations`; `evals/conformance/run_conformance.py --self-test` is undisturbed.

## Task Commits

1. **Task 1: Make the artifact-family line unconditional in SKILL.md** - `c7c1df4` (feat)
2. **Task 2: Remove the last source label / align standalone-audit shape** - `7cac0d2` (fix)
   - WINDOWS.md entries 7/9 disposition - `ee9086e` (docs)
3. **Task 3: Two new discrimination-proven violation codes** - `ce82aac` (test)

## Files Created/Modified

- `skills/proof-first/SKILL.md` - Write mode five-value family line; three-pass self-check with the new family-line gate
- `skills/proof-first/references/artifact-patterns.md` - `economic buyer` appositive replaced with `the person who signs`
- `skills/proof-first/references/completeness-audit.md` - standalone-audit closing clause rewritten to match the accepted AUD-03 boundary
- `tools/check_repo.py` - `SOURCE_COINED_LABELS`, `check_skill_family_line_gate`, `check_source_label_in_skill_content`, two mutation functions, self-test fixtures/assertions, `MUTATIONS` rows
- `.planning/WINDOWS.md` - entries 7 and 9 marked `fixed`

## Gate Results (verbatim)

```
$ python3 tools/check_repo.py --self-test
self-test PASS - verified violation codes: artifact-family-section-missing, catalog-count-mismatch,
catalog-count-unstated, catalog-id-drift, catalog-opening-rule-count, dup-figure-key, dup-id,
figure-order, framework-statement-missing, frontmatter-description-invalid, frontmatter-name-mismatch,
frontmatter-unknown-key, frontmatter-unparseable, license-missing, mc-catalog-id-drift,
mc-count-mismatch, mc-count-unstated, mc-rule-in-skill, pointer-duplicated, pointer-missing,
pointer-unparseable, range-id, revived-id, skill-family-line-gate-missing, skill-token-budget-exceeded,
skill-too-long, source-label-in-skill-content, undefined-id, unlisted-figure

$ python3 tools/check_repo.py --mutation-test
mutation-test CONTROL: 0 violations on the unmutated copy (0 known-open per KNOWN_OPEN_VIOLATIONS, 0 unexpected)
... (29 mutation-test OK lines) ...
mutation-test PASS: 29 codes discrimination-proven

$ python3 tools/check_repo.py
check_repo: 0 violations

$ python3 evals/conformance/run_conformance.py --self-test
self-test PASS - verdicts discriminated: conformant, no-family, rule-before-family, unscoreable
```

Determinism spot-check (`python3 tools/check_repo.py` run twice, `diff -q` on the outputs): identical, no diff.

Token re-measurement (recorded numbers): pre-edit 3700 words / 4810 estimated tokens / 190-token margin; post-edit 3757 words / 4884 estimated tokens / 116-token margin.

## Decisions Made

- **Byte-identical no-family spelling:** verified with a direct `grep -o '\*\*No family fits:\*\*'` comparison against `artifact-patterns.md`, not visual inspection alone, since this string is now also a check-function anchor (`skill-family-line-gate-missing`) and a reworded copy would silently stop matching both.
- **7-entry SOURCE_COINED_LABELS:** the singular/plural problem word is one tuple entry (`'pain'`) matched with an optional trailing `s` in `_source_label_pattern`, not two separate entries -- keeps the acceptance criterion's literal "seven entries" true while still catching "pains".
- **MOD-04 stays open:** this plan pulls two content levers (Write-mode five-value promotion, self-check gate) and proves they exist; it does not run or interpret a conformance measurement. `03-08-PLAN.md` owns that.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Line-wrap defect split the appositive-replacement literal**
- **Found during:** Task 2, immediately after the first edit to `artifact-patterns.md`'s Business case paragraph
- **Issue:** `Diane Osoria, the` and `person who signs,` landed on separate physical lines after the appositive edit, splitting the literal three-word phrase `the person who signs` across the soft line-wrap boundary. `grep -c 'the person who signs'` reported 2 (the two pre-existing uses) instead of the required 3, because the third occurrence's tokens straddled two lines.
- **Fix:** Moved the wrap point so the full phrase reads on one physical line; no wording or check change. This is the same class of defect this repository's own 02-04 and 03-06 plans hit and fixed identically (reword the line wrap, never the check or the content).
- **Files modified:** `skills/proof-first/references/artifact-patterns.md`
- **Verification:** `grep -c 'the person who signs' skills/proof-first/references/artifact-patterns.md` returns 3; `grep -c 'run-rate reduction and a clean regulatory'` still returns 1 (fact preserved); `python3 tools/check_repo.py` still `0 violations`.
- **Committed in:** `7cac0d2` (fixed before the Task 2 commit; no separate commit needed).

**Total deviations:** 1 auto-fixed (Rule 1). **Impact:** pre-commit fix, no effect on shipped behavior, content, or scope; caught before any commit landed the defect.

## Threat Flags

None new beyond `03-07-PLAN.md`'s own `<threat_model>` (T-03-04 through T-03-08, all low/medium severity, all mitigated or accepted as written). No `high` or `critical` threat is present; the `security_block_on: high` gate does not fire.

## Known Stubs

None.

## Issues Encountered

None beyond the one deviation above, resolved within the same task before its commit.

## Next Phase Readiness

- Both `MOD-04` content levers (five-value family line, self-check gate) are shipped and mechanically proven present via `skill-family-line-gate-missing`.
- `03-08-PLAN.md` can now run `evals/conformance/run_conformance.py` against this plan's SKILL.md to measure whether the family-naming rate actually moved, and make the MOD-04 closure decision.
- `WINDOWS.md` entry 8 (the MOD-04 residual finding) is untouched and remains open, exactly as this plan's objective requires.
- `.planning/REQUIREMENTS.md` is untouched: `grep -c "^- \[x\].*UNVERIFIED" .planning/REQUIREMENTS.md` returns 0, and `MOD-04` reads `[ ]`.

## Self-Check: PASSED

All claimed files found on disk: `skills/proof-first/SKILL.md`, `skills/proof-first/references/artifact-patterns.md`, `skills/proof-first/references/completeness-audit.md`, `tools/check_repo.py`, `.planning/WINDOWS.md`. All four claimed commit hashes (`c7c1df4`, `7cac0d2`, `ee9086e`, `ce82aac`) found in `git log`. All plan-level `<verification>` commands re-run above with matching output. `grep -c "^- \[x\].*UNVERIFIED" .planning/REQUIREMENTS.md` returns 0.

---
*Phase: 03-completeness-audit-artifact-patterns*
*Completed: 2026-09-15*
