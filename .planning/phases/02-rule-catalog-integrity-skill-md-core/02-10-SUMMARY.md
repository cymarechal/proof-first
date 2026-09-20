---
phase: 02-rule-catalog-integrity-skill-md-core
plan: 10
subsystem: eval-harness
tags: [trigger-test, clopper-pearson, fisher-exact, skill-frontmatter, agent-skills, decision-rule]

# Dependency graph
requires:
  - phase: 02-09
    provides: Phase 02 completion-gate state and CAT-10's diagnosed root cause (DEBUG-cat10-trigger-over-fire.md)
provides:
  - A pre-committed, six-branch decision rule for reopening a locked frontmatter decision under measurement (evals/trigger/DECISION-RULE-cat10.md), reusable as a template for future D-29/D-30-class reopenings
  - A stdlib Clopper-Pearson / Fisher-exact statistics module (evals/trigger/stats.py), self-tested against externally published values
  - run_trigger_test.py --repeats/--append/--label, so the trigger instrument can run paired multi-session arms without destroying committed measurement history
  - A live-measured, real finding on CAT-10: the exclusion-clause lever eliminates the measured over-fires (p_attr=0.0016) but causes a must-fire regression, and is reverted, not shipped
affects: [phase-05-eval-harness, phase-06-legal-review-gate]

# Actuals (#2632)
actuals:
  tokens: 79000
  tasks: 6
  commits: 6

tech-stack:
  added: []
  patterns:
    - "Pre-committed branch table with a stated precedence order, committed before any measurement session runs, mirroring the evals/conformance/RESULTS-mod04.md MOD-04 precedent"
    - "Paired control/treatment arms on one instrument via a single runner's --repeats/--append/--label flags rather than two separate scripts"
    - "Counts and exact confidence bounds (Clopper-Pearson, Fisher exact) reported instead of percentages, everywhere this instrument touches"

key-files:
  created:
    - evals/trigger/DECISION-RULE-cat10.md
    - evals/trigger/stats.py
    - evals/trigger/INIT-EVENTS.md
    - evals/trigger/transcripts-cat10.tar.gz
  modified:
    - evals/trigger/run_trigger_test.py
    - evals/trigger/RESULTS-trigger.md
    - .github/workflows/ci.yml
    - .gitignore
    - .planning/REQUIREMENTS.md
    - .planning/WINDOWS.md
    - .planning/phases/02-rule-catalog-integrity-skill-md-core/02-UAT.md
    - "skills/proof-first/SKILL.md (tested with the exclusion clause, then reverted; net unchanged at HEAD)"
    - ".claude-plugin/plugin.json, .claude-plugin/marketplace.json (same: tested, reverted, net unchanged)"
    - "evals/pressure-tests.md (same: tested, reverted, net unchanged)"
    - "output-styles/proof-first.md, prompts/system-prompt.md (regenerated for the treatment description, then regenerated again after the revert; net unchanged)"

key-decisions:
  - "Applied the pre-committed decision rule's stated precedence (6, 5, 4, 1, 2, 3) exactly as written when the numbers landed in a shape that made Branch 1 (closure) and Branch 4 (must-fire regression) both technically match — Branch 4 won because it comes first in precedence, even though the over-fire elimination alone would have satisfied Branch 1"
  - "Reverted the tested treatment description rather than shipping a lever that traded one measured defect for another, per the rule's own Branch 4 disposition"
  - "Documented three plan-authored verification-script defects (git-diff header off-by-one counted three times; a pre-existing intro sentence colliding with a whole-file 'not yet observed' count; an acceptance criterion literally contradicting Task 1's own instruction to replace the sentinel line) rather than force-fitting shipped content to match them, per the 03-04/04-01/04-03/04-04 precedent"

requirements-completed: []

coverage:
  - id: D1
    description: "Six-branch decision rule (arms, counters, sample floors, attempt cap, closure/attribution thresholds, precedence order) committed before any session of this round ran"
    requirement: "CAT-10"
    verification:
      - kind: other
        ref: "git log --oneline (05c6d24 precedes b077b8b and d7a153c); branch-count regex probe prints 6"
        status: pass
    human_judgment: false
  - id: D2
    description: "Stdlib Clopper-Pearson/Fisher-exact stats module, self-tested against externally published values; run_trigger_test.py gains --repeats/--append/--label without touching the detector, session isolation, or scope-hash halt"
    requirement: "CAT-10"
    verification:
      - kind: unit
        ref: "evals/trigger/stats.py --self-test (15 cases, exit 0)"
        status: pass
      - kind: unit
        ref: "evals/trigger/run_trigger_test.py --self-test (3+2+2+1+4+5 cases, exit 0)"
        status: pass
    human_judgment: false
  - id: D3
    description: "Arm B (control, 439-char description) measured live at n=5: OF_B/SN_B=9/25, MH_B/SM_B=45/45"
    requirement: "CAT-10"
    verification:
      - kind: other
        ref: "70 live claude -p sessions, evals/trigger/RESULTS-trigger.md Arm B block; automated verify commands in 02-10-PLAN.md Task 3 all pass"
        status: pass
    human_judgment: false
  - id: D4
    description: "Single intervention (exclusion clause) applied to every carrier of the description string, scope hash re-authored, every Observed cell blanked before the treatment arm ran"
    requirement: "CAT-10"
    verification:
      - kind: other
        ref: "collapsed length 551 (inside D-30 band), head-14 hash 9049c7d8... matches plan's cross-check exactly, generate_derivatives.py --check exit 0, check_repo.py 0 violations"
        status: pass
    human_judgment: false
  - id: D5
    description: "Arm A (treatment, 551-char description) measured live at n=5: OF_A/SN_A=0/25 (every must-not-fire row clean), MH_A/SM_A=40/45 (one must-fire row regressed 5/5 -> 0/5)"
    requirement: "CAT-10"
    verification:
      - kind: other
        ref: "70 live claude -p sessions, evals/trigger/RESULTS-trigger.md Arm A block; automated verify commands in 02-10-PLAN.md Task 5 all pass"
        status: pass
    human_judgment: false
  - id: D6
    description: "Decision rule applied mechanically (Branch 4 selected), intervention reverted, CAT-10/WINDOWS id 24/G-02-2 re-verdicted to reflect the measurement, RESULTS-trigger.md finding states plainly that CAT-10 is not satisfied"
    requirement: "CAT-10"
    verification:
      - kind: manual_procedural
        ref: "Plan's own <manual> check: read CAT-10's annotation cold and confirm it does not read as satisfied"
        status: pass
    human_judgment: true
    rationale: "Whether the written annotation genuinely 'reads as unsatisfied' to a cold reader (the plan's own stated bar) is a prose-quality judgment; the mechanical checks (checkbox is [ ], branch count, hash reverted) all pass, but the plan explicitly names this as the check no code in this repository performs (WINDOWS.md id 17's class)."

duration: 75min
completed: 2026-09-20
status: complete
---

# Phase 2 Plan 10: CAT-10 Gap-Closure — Exclusion Clause Tested Live, Reverted on a Measured Must-Fire Regression

**A pre-committed, six-branch decision rule governed a 140-session paired experiment on the SKILL.md frontmatter `description`: the proposed exclusion clause eliminated every measured over-fire (p_attr=0.0016) but broke a legitimate must-fire request, so it was reverted rather than shipped — CAT-10 stays open, now with a real, attributable finding instead of an n=1 guess.**

## Performance

- **Duration:** ~75 min (decision-rule authoring, instrument extension, 140 live sessions across two arms, and the branch-application/revert)
- **Tasks:** 6 completed
- **Files touched:** 15 (4 created, 11 modified; 4 of the "modified" files are net-unchanged at HEAD because they were tested with the treatment description and then reverted)
- **Live invocations:** 140 of the 170-invocation cap (0 retries needed — every planned session was scoreable)

## Accomplishments

- Committed `evals/trigger/DECISION-RULE-cat10.md` — a six-branch precedence table (evaluated 6, 5, 4, 1, 2, 3), fixed arms, fixed intervention text, sample floors, and a 170-invocation attempt cap — before any session of this round ran, mirroring the `RESULTS-mod04.md` MOD-04 precedent this project already trusts.
- Built `evals/trigger/stats.py`, a stdlib-only Clopper-Pearson upper-bound and two-tailed Fisher-exact implementation, self-tested against the exact values `DEBUG-cat10-trigger-over-fire.md` had already published (0.4507 at n=5, 0.0079 / 0.4737 / 0.0325 / 0.0031 / 0.1060 for the six Fisher cases).
- Extended `run_trigger_test.py` with `--repeats`, `--append`, and `--label`, plus an overwrite guard (`resolve_out_mode`) that refuses to clobber a non-empty results file — the exact accident that would otherwise have destroyed the 2026-09-20 measurement.
- Ran **Arm B (control)**: 70 live sessions against the unchanged 439-character description. `OF_B/SN_B = 9/25`, `MH_B/SM_B = 45/45` — the same two phrasings that fired at n=1 now fire 5/5 and 4/5 at n=5.
- Applied the single pre-committed intervention (Task 4): appended one exclusion sentence to the description, regenerated both derivatives, hand-updated both `.claude-plugin` manifests, re-authored `evals/pressure-tests.md`'s scope hash, and blanked all 14 Observed cells. Collapsed length landed at exactly 551 — inside D-30's 400-600 band — and the live head-14 hash (`9049c7d8...`) matched the plan's own cross-check value exactly, with no deviation needed.
- Ran **Arm A (treatment)**: 70 live sessions against the 551-character description. `OF_A/SN_A = 0/25` — every must-not-fire row scored zero fires — but `MH_A/SM_A = 40/45`: the must-fire row "We're putting together our bid response — write the commercial section." regressed from 5/5 (Arm B) to 0/5 (Arm A), most plausibly because the appended clause's "commercial modelling" shares the content word "commercial" with this unrelated request.
- Applied the decision rule mechanically: Fisher exact on the pooled over-fire 2x2 gives `p_attr = 0.0016` (the improvement is real and attributable), but the must-fire regression selects **Branch 4** ahead of Branch 1 in the stated precedence order. The treatment description was reverted (`git checkout` of `SKILL.md`, both manifests, and `pressure-tests.md` to the pre-Task-4 commit `b077b8b`; derivatives regenerated; head-14 hash confirmed back to `d5dd651a...`). Arm A's results and `INIT-EVENTS.md` are kept as evidence.
- Distilled every session's `system/init` event into `evals/trigger/INIT-EVENTS.md`, settling Q3 (the harness gives every session a bare skill-*name* list at activation, no description text) and confirming H3 (`simple-english:simple-english` was present as a candidate on every session, including the plain-English row) — for the first time by measurement rather than citation.

## Task Commits

1. **Task 1: Commit the decision rule** — `05c6d24` (feat)
2. **Task 2: Instrument extension (stats.py, --repeats/--append/--label)** — `9d38978` (feat)
3. **Task 3: Arm B (control) — 70 live sessions** — `b077b8b` (test)
4. **Task 4: Apply the single intervention** — `2fc7e7c` (feat) — *this is the commit Branch 4 reverts back past*
5. **Task 5: Arm A (treatment) — 70 live sessions** — `d7a153c` (test)
6. **Task 6: Apply the decision rule, revert the intervention** — `28404a5` (fix)

_No TDD gates apply — this plan is `type: execute`, not `type: tdd`._

## Files Created/Modified

- `evals/trigger/DECISION-RULE-cat10.md` — the pre-committed branch table, arms, counters, floors, attempt cap; plus Task 6's longhand branch evaluation appended in place of the `No session in this round has yet run.` sentinel
- `evals/trigger/stats.py` — `clopper_pearson_upper()` and `fisher_exact_two_tailed()`, both stdlib-only, self-tested
- `evals/trigger/run_trigger_test.py` — `--repeats`, `--append`, `--label`, `resolve_out_mode()`, `render_run_block()`, `aggregate_verdicts()`; detector/session/hash-halt logic untouched
- `evals/trigger/RESULTS-trigger.md` — gained two new `## Run` blocks (Arm B, Arm A) plus Task 6's finding statement; the original 2026-09-20 block is byte-identical throughout
- `evals/trigger/INIT-EVENTS.md` — per-arm `system/init` event distillation, settling Q3 and H3
- `evals/trigger/transcripts-cat10.tar.gz` — gzipped combined transcripts for both arms, 3988 KB (under the 5120 KB retention threshold)
- `.github/workflows/ci.yml` — added `python3 evals/trigger/stats.py --self-test` as CI's ninth command
- `.gitignore` — added `evals/trigger/transcripts/` (raw per-session JSONL, superseded by the committed tarball)
- `.planning/REQUIREMENTS.md` — CAT-10's annotation rewritten with both arms' full measurement, `p_attr`, the branch selected, and both hashes; checkbox stays `[ ]`
- `.planning/WINDOWS.md` — id 24 stays `open`, description replaced with the measured counts; two new `deviation` entries (ids 26, 27) recording the plan-authored verify-script issues below
- `.planning/phases/02-rule-catalog-integrity-skill-md-core/02-UAT.md` — gap `G-02-2` status set to `partially_resolved`, `measured:` block appended, all four original diagnosis fields retained
- `skills/proof-first/SKILL.md`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `evals/pressure-tests.md`, `output-styles/proof-first.md`, `prompts/system-prompt.md` — all tested with the treatment description (Task 4) and reverted (Task 6); net-unchanged at HEAD relative to before this plan ran

## Decisions Made

- Applied the decision rule's stated precedence order exactly as written even though the numbers landed in a shape where Branch 1 (closure) and Branch 4 (must-fire regression) both technically matched their own conditions — Branch 4 wins because it is evaluated first, per the rule committed in Task 1 before any number was known. No branch was added, reinterpreted, or reordered.
- Reverted the tested treatment rather than shipping it with a caveat, because this project's own truth for CAT-10 requires both halves (must-fire and must-not-fire) to hold, and a lever that trades one measured defect for another does not satisfy that truth under any reading.
- Documented, rather than silently worked around, three plan-authored verification-script defects (see Deviations below) — none affected the substantive measurement or its interpretation.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Plan-authored verification defect] `git diff <file> | grep -c '^-'` always over-counts by 1**
- **Found during:** Task 3 (first appended run block)
- **Issue:** The plan's own removed-lines probe (used identically in Tasks 3, 5, 6, and the plan-level `<verification>` block) counts `git diff`'s own `--- a/file` header line, which always starts with `-` regardless of whether any real content line was removed. Any successful append therefore always prints `1` (or `2` when both `DECISION-RULE-cat10.md` and `RESULTS-trigger.md` diffs are checked together), never the `0` the plan's own `<fails_when>` clause expects.
- **Fix:** None needed to shipped content — verified the substantive property with the corrected probe `git diff <file> | grep -E '^-' | grep -v '^--- '`, which printed empty (zero real removed lines) at every check point across the whole round, including `git diff HEAD~6 -- evals/trigger/RESULTS-trigger.md`.
- **Files affected:** None (verification-only; no shipped file was changed to accommodate this)
- **Verification:** Corrected probe run after Tasks 3, 5, and 6; all print empty
- **Committed in:** documented in Task 3 (`b077b8b`), Task 5 (`d7a153c`), and Task 6 (`28404a5`) commit messages

**2. [Rule 1 - Plan-authored verification defect] Task 4's whole-file "not yet observed" count collides with pre-existing prose**
- **Found during:** Task 4
- **Issue:** `evals/pressure-tests.md`'s intro paragraph (written in an earlier phase, 02-05, unrelated to this task) already contains the literal phrase "not yet observed" once as descriptive prose about the file's own convention. Task 4's own verify probe (`text.count('not yet observed')`, expecting 14) therefore reads 15, not 14.
- **Fix:** Left the pre-existing sentence untouched (out of this task's scope per the deviation-rules scope boundary) and verified the substantive property — exactly 14 table rows read `not yet observed` — with `grep -cE '^\| .* \| not yet observed \| - \| - \|$'`, which printed 14.
- **Files affected:** None
- **Verification:** Corrected probe printed 14 after Task 4 and again (via the same pattern, now with counted cells) confirmed absent after Task 5
- **Committed in:** documented in Task 4's commit message (`2fc7e7c`)

**3. [Rule 1 - Plan-authored acceptance-criteria contradiction] Task 6's "zero removed lines" criterion contradicts Task 1's own instruction**
- **Found during:** Task 6
- **Issue:** Task 6's acceptance criteria state "the branch table itself is unedited — git diff on the file shows zero removed lines," but Task 1's own action text explicitly instructs that Task 6 will "replace" the file's closing sentinel line (`No session in this round has yet run.`) with the branch evaluation — an intentional, required removal of that one line.
- **Fix:** Replaced only the sentinel line, exactly as Task 1 instructed; the six branch table rows are provably unedited (branch-count regex probe still prints 6, and the diff shows no change anywhere near the table). Documented the literal-vs-intent conflict rather than either leaving the sentinel un-replaced (violating Task 1's instruction) or silently ignoring the acceptance criterion's literal wording.
- **Files affected:** None
- **Verification:** `git diff evals/trigger/DECISION-RULE-cat10.md` shows exactly one removed line (the sentinel) and the branch-count probe still prints 6
- **Committed in:** documented in Task 6's commit message (`28404a5`)

---

**Total deviations:** 3 auto-fixed (all Rule 1, all plan-authored verification-script/acceptance-criteria defects; none required a shipped-content change). **Impact on plan:** None on substance — every deviation was a probe/wording issue in the plan itself, caught and documented per the established `03-04`/`04-01`/`04-03`/`04-04` precedent for handling plan-authored figure and script errors. All four `.planning/WINDOWS.md` prohibitions (no unscoreable-session rounding, no branch-table revision after the numbers were known, no percentage anywhere, no bundled second intervention) held throughout.

## Issues Encountered

None beyond the deviations documented above. Both live batches (70 sessions each, `--jobs 3 --timeout 600`) completed with zero unscoreable sessions and zero retries needed.

## Known Stubs

None. No hardcoded empty values, placeholder text, or unwired data sources were introduced by this plan.

## Threat Flags

None beyond what the plan's own `<threat_model>` already named (T1-T10, all mitigated as designed — see `evals/trigger/DECISION-RULE-cat10.md` and the per-task `<verify>` blocks for the mechanism each mitigation relies on).

## User Setup Required

None — no external service configuration required. This plan drove `claude -p` under the operator's existing CLI login, exactly as the prior Phase 2/3/5 live-harness measurements did.

## Next Phase Readiness

- CAT-10 stays open with a real, attributable, paired measurement (`p_attr = 0.0016` on the over-fire elimination) replacing the prior n=1 guess. `WINDOWS.md` id 24 carries the full measured characterization for whoever picks up the next lever.
- **The next candidate lever is named but not attempted**: H1's strongest candidate — removing the audience-naming clause `for technical presales and bid teams` — was deliberately kept out of this round to avoid bundling two interventions. It remains unfunded and untested.
- The instrument (`run_trigger_test.py --repeats/--append/--label`, `stats.py`) is now reusable for that next round without modification — it already supports paired arms, labelled append blocks, and exact confidence bounds.
- `evals/trigger/INIT-EVENTS.md` is the first measured (not cited) evidence in this repository of what the harness gives a session at activation time; useful context for Phase 5's eval-harness work and for any future activation-mechanism investigation.
- Task 4's commit SHA is `2fc7e7c` — the commit immediately after `b077b8b` (Task 3) and immediately before `d7a153c` (Task 5) — recorded here so a later reader can reconstruct exactly what Branch 4 reverted.

---
*Phase: 02-rule-catalog-integrity-skill-md-core*
*Completed: 2026-09-20*

## Self-Check: PASSED

- All 4 created files confirmed present on disk (`evals/trigger/DECISION-RULE-cat10.md`, `evals/trigger/stats.py`, `evals/trigger/INIT-EVENTS.md`, `evals/trigger/transcripts-cat10.tar.gz`)
- All 6 task commits confirmed in `git log --oneline --all` (`05c6d24`, `9d38978`, `b077b8b`, `2fc7e7c`, `d7a153c`, `28404a5`)
- `grep -c "^- \[x\].*UNVERIFIED" .planning/REQUIREMENTS.md` prints `0`
- Full 9-command CI sequence re-confirmed passing before this summary was written
