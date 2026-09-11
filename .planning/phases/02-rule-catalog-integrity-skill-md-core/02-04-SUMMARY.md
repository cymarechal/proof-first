---
phase: 02-rule-catalog-integrity-skill-md-core
plan: 04
subsystem: rule-catalog
tags: [agent-skill, skill-md, rule-catalog, deletion-test, prose-mechanics, ci-checker]

# Dependency graph
requires:
  - phase: 02-rule-catalog-integrity-skill-md-core
    provides: "02-01's frozen three-file skills/proof-first/ folder, the marker grammar (GAP/REVIEW/retention), the register heading, the 31-rule ID allocation map, and catalog-id-drift; 02-02's PF-1 spine and mid-draft line-count discipline; 02-03's completed PF-2 Proof and Integrity"
provides:
  - "PF-3 completed: PF-3.2 (per-token deletion test) and PF-3.3 (customer-verbatim retention with the both-markers-fire precedence)"
  - "references/deletion-test.md completed: the per-token worked comparison, the provenance section defining supplied source material, the required two-marker worked instance, and a closing no-term-list paragraph"
  - "PF-4 — Prose mechanics (four self-contained rules: sentence length, active voice, modal discipline, one claim per sentence) and PF-5 — Consistency and voice (three protective rules, each a presence requirement plus a check-mode prohibition)"
  - "The catalog closed out: 31 rules across 6 numbered sections, every reserved range deliberately under-filled, SKILL.md measured at exactly 480 lines against CAT-08's 500-line ceiling"
affects: [02-05, 02-06]

# Actuals (#2632)
actuals:
  tokens: 3628
  tasks: 2
  commits: 2

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A marker phrase required to match a literal multi-word string (grep -F) must not be allowed to wrap across a line break in the authored prose — 'customer's term, retained' silently failed a literal grep when the line-wrap point fell between 'term,' and 'retained' despite both words being adjacent in rendered prose; fixed by moving the wrap point, not the check"
    - "A required phrase used as a grep anchor (e.g. 'Check mode never') must be verified against the *authored line breaks*, not just the rendered paragraph — the same phrase silently split across a hard line-wrap once in PF-5.3 before the wrap point was moved"
    - "Line-budget trims target replace-with clauses and connective prose first (lowest information density per line), not rule statements or worked examples — preserves judgment content while recovering the 1-2 lines needed to land exactly at a ceiling"

key-files:
  created: []
  modified:
    - skills/proof-first/SKILL.md
    - skills/proof-first/references/deletion-test.md
    - skills/proof-first/references/checklist.md
    - NUMBERING.md

key-decisions:
  - "PF-3.2's worked ✗/✓ pair uses AWS Control Tower (from the brief's target-platform list) with an 'enterprise-grade' decorative modifier, rather than reusing deletion-test.md's own Oracle Database half-empty-compound example — keeps SKILL.md's rule body and the reference file's edge-case table each demonstrating the mechanism on a distinct concrete noun."
  - "PF-3.3's two-marker worked instance (both in SKILL.md's rule body and in deletion-test.md's provenance section) pairs the retained term 'landing zone' (Marcus Feld's discovery quote) with a PF-2.14 REVIEW (commitment) flag on 'fully governed from day one' — a commitment-shaped claim, not a fabricated metric, so the two markers visibly answer different questions (vocabulary vs. truth) on the same phrase, per D-11."
  - "PF-4's four rules carry no worked example (D-02: mechanical rules get statement + Replace-with only) and state explicitly that the section depends on no other skill, tool, or standard — closing CAT-06's edge-probe item directly in the section's own opening paragraph rather than only in NUMBERING.md's Concern column."
  - "PF-5's three rules are ordered to match PF-1.5 (contrast), the buyer-priority material PF-1.25 draws on (second person), and PF-2.3/PF-2.4 (unhedged evidence) — each cross-references the rule it protects, so a reader lands on the mechanism it is guarding without re-deriving why the protective rule exists."
  - "Final line count landed at exactly 480 — the stated ceiling, not under it with margin. Trimmed two lines from PF-4's opening paragraph and PF-4.2/PF-4.3's Replace-with clauses (lowest-information-density prose) rather than shortening a rule statement or a worked example, so no rule lost content to meet the budget."

requirements-completed: [CAT-02, CAT-04, CAT-05, CAT-06]

coverage:
  - id: D1
    description: "PF-3 completed with PF-3.2 (apply the deletion test to each token of a compound term independently, so a decorative modifier riding on a real technical noun is not laundered by testing the phrase as one unit) and PF-3.3 (retain a customer-verbatim term, mark it on first occurrence only, and state that retention never suppresses an integrity flag — both markers fire on the same phrase). references/deletion-test.md completed with the per-token worked comparison, the provenance section stating what counts as supplied customer source material, the required two-marker worked instance, and a closing paragraph stating the file enumerates no banned/allowed term list."
    requirement: "CAT-04, CAT-05"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py (live run, both tasks) — check_repo: 0 violations"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test (Task 2, full CI job order) — self-test PASS, mutation-test PASS: 13 codes proven live"
        status: pass
      - kind: other
        ref: "~15 acceptance-criteria grep/awk one-liners from 02-04-PLAN.md Task 1 (heading order, Replace-with/heading counts, stated-count sentence, PF-3.3's three named conditions via 'first occurrence'/'REVIEW (' greps, the two-marker instance in deletion-test.md, the four-class table row count, NUMBERING.md/checklist.md row counts and reserved-range values, line-count ceiling)"
        status: pass
    human_judgment: true
    rationale: "SOURCES.md's reproduction boundary (no framework wording reproduced) is a semantic judgment no tool in this project's stack performs. Per workflow.human_verify_mode=end-of-phase this is harvested into the phase's UAT batch rather than halting this plan, exactly as 02-01/02-02/02-03's equivalent human-checks were deferred."
  - id: D2
    description: "PF-4 — Prose mechanics: four self-contained rules (sentence length with a stated numeric ceiling and counting unit, active voice with its one admissible exception, modal discipline distinguishing commitment- from possibility-shaped verbs, one claim per sentence), opened by a paragraph stating the section depends on no other skill, tool, or standard being installed."
    requirement: "CAT-06"
    verification:
      - kind: other
        ref: "grep -oE '^### PF-4\\.[0-9]+' skills/proof-first/SKILL.md → PF-4.1 through PF-4.4 in order"
        status: pass
      - kind: other
        ref: "awk range scan over PF-4.1 for '[0-9]+ word' → 1 (numeric ceiling + stated counting unit present)"
        status: pass
      - kind: other
        ref: "awk range scan over PF-4/PF-5 for lines starting ✗ or ✓ → 0 (no examples, per D-02's mechanical-rule criterion)"
        status: pass
    human_judgment: true
    rationale: "Whether the section 'reads as this repository's own words, not a compressed copy of an external standard's rule list' (the plan's own <human-check>) is a semantic judgment. A self-read during execution found the four rules paraphrase generic technical-writing craft (sentence length, active voice, modal verbs, single-claim sentences) with no ordered-list structure or wording traceable to any of the three anchor frameworks or to ASD-STE100 — consistent with SOURCES.md needing no new row (confirmed via `git diff --stat SOURCES.md`, no change). Formal sign-off deferred to end-of-phase UAT per workflow.human_verify_mode=end-of-phase."
  - id: D3
    description: "PF-5 — Consistency and voice: three protective rules (before/after contrast, second-person address to a stated buyer priority, unhedged evidenced claims), each stating both a presence requirement on the document and a matching prohibition on check mode itself, so neither a flattened document nor a checker that strips rhetoric can pass."
    requirement: "CAT-02"
    verification:
      - kind: other
        ref: "awk range scan over PF-5 for 'check mode never' (case-insensitive) → 3 (one per rule, both halves present in each)"
        status: pass
      - kind: other
        ref: "grep -oE '^### PF-5\\.[0-9]+' skills/proof-first/SKILL.md → PF-5.1 through PF-5.3 in order"
        status: pass
    human_judgment: false
  - id: D4
    description: "The catalog is closed out at its final stated total (31 rules in 6 numbered sections), NUMBERING.md and references/checklist.md agree with SKILL.md's defined headings, and the measured final line count is recorded rather than projected."
    requirement: "CAT-02"
    verification:
      - kind: integration
        ref: "catalog-id-drift (mutation-test, re-proven live at 31 rules) + heading/row-count checks: '### PF-' count=31, '**Replace with:**' count=31, NUMBERING.md Allocated-IDs PF rows=31, checklist.md PF rows=31, stated-count sentence present exactly once"
        status: pass
      - kind: other
        ref: "wc -l skills/proof-first/SKILL.md → 480, at CAT-08's 500-line hard ceiling and the plan's own 480-line working margin"
        status: pass
      - kind: other
        ref: "python3 one-liner confirming NUMBERING.md's Allocated IDs are in true dotted-integer ascending order (31 rows) — substituted for the plan's own `sort -c` acceptance criterion, which fails identically on byte-order grounds against content this plan did not touch (see Deviations)"
        status: pass
    human_judgment: false

duration: 9min
completed: 2026-09-11
status: complete
---

# Phase 2 Plan 4: Deletion Test Complete, Prose Mechanics, and Consistency Protection Summary

**PF-3's per-token test and customer-verbatim retention rule, PF-4's four self-contained prose-mechanics rules, and PF-5's three presence-plus-prohibition protective rules close out the 31-rule catalog across all 6 sections, measured at exactly 480 lines against CAT-08's 500-line ceiling.**

## Performance

- **Duration:** 9 min
- **Started:** 2026-09-11T01:03:00Z
- **Completed:** 2026-09-11T01:12:00Z
- **Tasks:** 2 (both `type="auto"`)
- **Files modified:** 4

## Accomplishments

- Authored `PF-3.2` (apply the deletion test to each token of a compound term independently, so a decorative modifier riding on a real technical noun is not laundered by testing the phrase as one unit) with a worked ✗/✓ pair on an AWS Control Tower deployment.
- Authored `PF-3.3` (retain a customer-verbatim term, mark it on first occurrence only, and state that retention never suppresses an integrity flag — both markers can fire on the same phrase) with a worked instance pairing a retained "landing zone" term against a `PF-2.14 REVIEW (commitment)` flag.
- Completed `references/deletion-test.md`: a per-token worked comparison (whole-phrase test wrongly passes; token-by-token test correctly isolates the buzzword), a provenance section stating what counts as supplied customer source material (and that nothing the vendor wrote qualifies), the required two-marker worked instance, and a closing paragraph stating the file enumerates no banned/allowed term list.
- Authored `PF-4 — Prose mechanics` (four rules: sentence length with a 25-word ceiling counted as whitespace-delimited words, active voice with its one admissible exception, modal discipline distinguishing commitment- from possibility-shaped verbs, one claim per sentence), opened by a paragraph stating the section depends on no other skill, tool, or standard.
- Authored `PF-5 — Consistency and voice` (three rules: before/after contrast, second-person address to a stated buyer priority, unhedged evidenced claims), each stating both a presence requirement and a matching check-mode prohibition.
- Registered all nine new IDs in `NUMBERING.md`'s Allocated IDs table (ascending) and updated PF-3/PF-4/PF-5's reserved-range counters; added the matching nine rows to `references/checklist.md`.
- Updated the stated-count sentence twice (`22 rules in 4 numbered sections` → `24` → `31 rules in 6 numbered sections`), reaching the catalog's final value — every reserved range ships deliberately under-filled for v1.1.
- Re-ran the full CI job order (`--self-test`, `--mutation-test`, live check) after each task's growth — all 13 violation codes still proven live, 0 live violations.
- Measured the final line count at exactly 480 lines, trimming two lines of lowest-information-density prose (an opening-paragraph clause and two Replace-with lines) to land at the plan's own working margin below CAT-08's 500-line ceiling.

## Task Commits

1. **Task 1: PF-3.2 and PF-3.3, and the deletion test's four documented edge classes** — `427e09c` (feat)
2. **Task 2: PF-4's self-contained prose mechanics, PF-5's protective rules, and the final line-budget measurement** — `4720ff9` (feat)

**Plan metadata commit:** recorded below after STATE.md/ROADMAP.md/REQUIREMENTS.md updates.

## Files Created/Modified

- `skills/proof-first/SKILL.md` — completed `## PF-3`, added `## PF-4 — Prose mechanics` and `## PF-5 — Consistency and voice` (31 rules total, 373→480 lines across the two tasks)
- `skills/proof-first/references/deletion-test.md` — per-token comparison section, provenance section with the two-marker worked instance, and the no-term-list closing paragraph
- `skills/proof-first/references/checklist.md` — 9 new PF rows, ascending by ID
- `NUMBERING.md` — 9 new Allocated IDs rows, PF-3/PF-4/PF-5 reserved-range counters updated

## Decisions Made

- PF-3.2 and PF-3.3's worked examples draw on the brief's target-platform list (AWS Control Tower) and Marcus Feld's discovery quote respectively, keeping every fact traceable to `examples/deal-brief.md` — see key-decisions above for the full rationale on the two-marker instance's specific pairing (retention + `PF-2.14 REVIEW (commitment)`, not a fabricated-metric flag).
- PF-4's four rules carry no worked example (mechanical, per D-02) and state their self-containment explicitly in the section's own opening paragraph, directly answering CAT-06's "no dependency on another skill" edge-probe item.
- PF-5's three rules are each ordered to name the specific earlier rule they protect (`PF-1.5`, the buyer-priority material behind `PF-1.25`, `PF-2.3`/`PF-2.4`), so the protective rule and the mechanism it guards are cross-referenced rather than left for the reader to infer.
- The final line count was trimmed to land at exactly 480 — the plan's own stated ceiling — by shortening two low-information-density prose clauses (PF-4's opening paragraph, PF-4.2/PF-4.3's Replace-with lines), not by removing content from any rule statement or worked example.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed a line-wrap that broke two literal multi-word grep anchors**
- **Found during:** Task 1 (deletion-test.md) and Task 2 (SKILL.md PF-5.3), first acceptance-criteria pass after each
- **Issue:** The phrase `customer's term, retained` (the PF-3.3 marker's own literal text) and the phrase `Check mode never` (PF-5.3's required prohibition-half anchor) each happened to fall across an authored line-wrap boundary in my first draft — the words were adjacent in rendered prose but split by a hard newline in the source file, so a literal `grep -cF`/`grep -ciE` match against the exact string returned 0 instead of the expected ≥1.
- **Fix:** Moved the wrap point in both places so each anchor phrase sits intact on one physical line. No wording was changed, only where the line break falls.
- **Files modified:** `skills/proof-first/SKILL.md`, `skills/proof-first/references/deletion-test.md`
- **Verification:** `grep -cF "customer's term, retained" skills/proof-first/references/deletion-test.md` → `1`; `awk '/^## PF-5 —/{f=1} f' skills/proof-first/SKILL.md | grep -ciE 'check mode never'` → `3`.
- **Committed in:** `427e09c` (Task 1), `4720ff9` (Task 2) — both fixes are folded into their respective task commits, caught and corrected before either commit was made.

---

**Total deviations:** 1 auto-fixed (1 bug, applied at two line-wrap points).
**Impact on plan:** No scope creep — the fix only moved where a line break falls in already-written prose; no rule content, marker grammar, or checker code was touched.

### Acceptance-Criterion Discrepancy (verification-script bug, not an implementation defect)

**The Allocated-IDs `sort -c` ordering check fails — the same pre-existing discrepancy 02-03 already documented, unaffected by anything this plan authored.**

Task 2's acceptance criteria include:
```
awk '/^## Allocated IDs/{f=1;next} /^## /{f=0} f && /^\| PF-/ {split($0,c,"|"); gsub(/ /,"",c[2]); print c[2]}' NUMBERING.md | sort -c
```
expected to exit 0. This fails with `sort: disorder: PF-1.13` — the identical first failure point 02-03's SUMMARY already documented and confirmed was present before that plan touched anything. `NUMBERING.md`'s own "sorted ascending by ID" convention treats an ID's suffix as a dotted integer pair (`PF-1.2` < `PF-1.5` < ... < `PF-1.13`), which is not the byte-order plain ASCII `sort` produces (`'1' < '2'` at the fourth character puts `PF-1.13` before `PF-1.2`). This plan's own 9 new rows (`PF-3.2`, `PF-3.3`, `PF-4.1`-`PF-4.4`, `PF-5.1`-`PF-5.3`) were placed in the same established dotted-integer ascending order as every other row — verified independently via a Python one-liner parsing each ID into `(section, n)` integer tuples and confirming all 31 rows sort ascending under that comparator (see coverage D4). No code in `tools/check_repo.py` depends on the `sort -c` byte-order shape; `parse_numbering` reads the table by row, not by verifying byte-order. This is the same class of pre-existing verification-script discrepancy 02-01 and 02-03 both documented for their own analogous checks.

## Issues Encountered

None beyond the deviation and acceptance-criterion discrepancy documented above.

## Authentication Gates

None — no external service or CLI authentication was required.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- The catalog is complete: 31 rules across 6 numbered sections (`PF-0` through `PF-5`), every reserved range deliberately under-filled for v1.1, `SKILL.md` measured at exactly 480 lines. `02-05` and `02-06` (frontmatter/CI-enforcement extensions, and the trigger pressure-test/`SOURCES.md` closure) can proceed against a stable, ID-frozen catalog.
- `SOURCES.md` required no new row — PF-4's four prose-mechanics concepts (sentence length, active voice, modal discipline, one claim per sentence) are generic technical-writing craft with no traceable origin in any of the three anchor frameworks, confirmed via `git diff --stat SOURCES.md` showing no change.
- Self-read of the plan's `<human-check>` during execution (not a formal sign-off, since `workflow.human_verify_mode=end-of-phase` defers the formal one to phase-end UAT): (1) `PF-4` and `PF-5` read as this repository's own restatement of generic prose discipline, with no ordered-list structure or wording traceable to Command of the Message, MEDDICC, Challenger, or ASD-STE100, and neither section depends on another skill being installed; (2) the catalog does not read as flat, dead prose — `PF-5`'s three rules are structural guarantees against exactly that failure, and no section consists only of removal instructions; (3) a spot-check of `SKILL.md`'s own prose against `PF-4.3`'s modal discipline found no sentence mixing a commitment-shaped and a possibility-shaped verb. Open item carried into end-of-phase UAT for an actual human sign-off, per the same deferral 02-01/02-02/02-03 used.
- No blockers for `02-05`.

## Self-Check: PASSED

- `[ -f skills/proof-first/SKILL.md ]` → FOUND
- `[ -f skills/proof-first/references/deletion-test.md ]` → FOUND
- `[ -f skills/proof-first/references/checklist.md ]` → FOUND
- `[ -f NUMBERING.md ]` → FOUND
- `git log --oneline --all | grep -q 427e09c` → FOUND
- `git log --oneline --all | grep -q 4720ff9` → FOUND
- `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py` → all green, 13 codes proven live, 0 live violations
- All Task 1 and Task 2 acceptance criteria re-run: all PASS except the pre-existing `sort -c` script discrepancy documented above (does not affect any code-enforced check)
- File-wide `### PF-` heading count (31) = `**Replace with:**` line count (31) = checklist.md PF row count (31) = NUMBERING.md Allocated IDs PF row count (31) = the stated rule count (31), across 6 numbered sections
- `wc -l skills/proof-first/SKILL.md` → 480, at CAT-08's 480-line working margin (500-line hard ceiling)

---
*Phase: 02-rule-catalog-integrity-skill-md-core*
*Completed: 2026-09-11*
