---
phase: 03-completeness-audit-artifact-patterns
plan: 08
subsystem: eval-harness
tags: [conformance, mod-04, windows-ledger, gap-closure, instrument-bugfix]

# Dependency graph
requires:
  - phase: 03-completeness-audit-artifact-patterns
    provides: "03-06's conformance instrument (evals/conformance/run_conformance.py) and 03-07's two SKILL.md levers (five-value family line, self-check gate) -- this plan measures whether those levers moved the rate and disposes of WINDOWS.md entry 8"
provides:
  - "evals/conformance/RESULTS-mod04.md: the actual post-03-07 MOD-04 measurement (16/20 scoreable, both models, five fixtures) plus a same-instrument paired baseline against the pre-03-07 skill (5/11, sonnet-5 only) and a hand-computed Combined Result section reconciling every run block"
  - "evals/conformance/run_conformance.py: two real instrument defects found and fixed -- a nonzero-exit claude -p session scored as no-family instead of unscoreable, and _git_blob_sha() always reporting the repo's HEAD blob regardless of --skill-src -- both self-test-covered"
  - "WINDOWS.md entry 8, REQUIREMENTS.md MOD-04, 03-UAT.md gap G-03-2: disposed under the plan's pre-committed Branch 3 rule, all three carrying the same 16/20 and 5/11 figures"
affects: [phase-5-eval-harness, phase-6-legal-review]

# Actuals (#2632)
actuals:
  tokens: 14392
  tasks: 2
  commits: 9

tech-stack:
  added: []
  patterns:
    - "Live-measurement durability: one claude -p session per script invocation, appended to the results file immediately, rather than one large multi-session invocation -- run_conformance.py only writes its run block when a whole invocation finishes, and two separate interruptions (a harness usage-limit reset, a session teardown) each would have silently discarded an entire in-flight matrix under the original single-invocation approach."
    - "Paired same-instrument baseline via git archive: --skill-src accepts any directory, so a prior SKILL.md revision materialised from a git commit (git archive <sha> skills/proof-first | tar -x) makes a fair apples-to-apples comparison possible without a second scoring implementation."

key-files:
  created: []
  modified:
    - evals/conformance/run_conformance.py
    - evals/conformance/RESULTS-mod04.md
    - .planning/WINDOWS.md
    - .planning/REQUIREMENTS.md
    - .planning/phases/03-completeness-audit-artifact-patterns/03-UAT.md

key-decisions:
  - "Branch 3 selected mechanically, before its consequences were known: M=20>=16 and N/M=16/20=0.8<=0.875 fires the pre-committed rule's Branch 3 ('not improved') condition, which is defined against the OLD cross-instrument 0.875 figure from 03-05's UAT recipe -- not against this plan's own paired baseline."
  - "Did not force the branch-3 template's literal 'did not move it' framing when the paired baseline showed otherwise. The mechanical branch selection (stays open, [ ], partially_resolved) was honored exactly, but the WRITTEN description states the true finding: under a same-instrument, same-model comparison, 03-07's levers raised sonnet-5 conformance from 45.5% (5/11) to 60.0% (6/10) -- a real, measured improvement that still falls short of the rule's 87.5% closure bar. Silently reproducing a template phrase that contradicts measured evidence would itself be the kind of overclaim (in the opposite direction) this phase has already reverted three times."
  - "The 03:11:24 contaminated 20-session run block stays invalidated in its entirety, even though the coordinator's own analysis judged the sonnet-5 lines within it 'genuine.' Having already published that invalidation, re-admitting a favorable subset later would look exactly like the post-hoc cherry-picking the pre-committed rule exists to prevent. All of that block's data was re-collected from scratch under the fixed instrument instead."
  - "Two real instrument defects were found and fixed mid-measurement, both Rule 1 (blocking bug): (1) run_session() never inspected result.returncode or result.stderr, so a nonzero-exit claude -p invocation had its short error text scored as a real transcript, producing a false no-family verdict indistinguishable from a genuine omission -- this is exactly what corrupted the first 20-session run when the account hit a usage limit mid-run. (2) _git_blob_sha() always ran git rev-parse HEAD:skills/proof-first/SKILL.md regardless of --skill-src, so the plan's own required paired-baseline run (Branch 3) would have recorded the WRONG SKILL.md revision. Both fixed, both covered by new offline --self-test cases (7 total, up from 5), both fixed BEFORE the data used in the final disposition was collected."
  - "Opus-5 was not run for the paired baseline arm. Given two live-quota/session interruptions already encountered in this plan, a sonnet-5-only paired baseline was accepted as a defensible same-instrument comparison rather than risking a second 10-session opus arm losing data again. This means Arm 1 (post-03-07, both models, n=20) and Arm 2 (pre-03-07 baseline, sonnet-5 only, n=11) have unequal sample sizes and unequal model coverage -- disclosed explicitly in RESULTS-mod04.md, REQUIREMENTS.md, and WINDOWS.md entry 8, not silently averaged away."
  - "03-06-PLAN.md's own instrument-proving run (2026-09-15T02:47:51Z, blob 1fc1e109..., rule-before-family) was folded into the Arm 2 baseline tally as one extra genuine A-rfp-answer sample. It measured the identical pre-03-07 skill state via the identical recipe, before the returncode bug existed, and scored a normal (non-bug-signature) verdict -- discarding it would have thrown away real data for no reason."
  - "Ran the measurement as many small single-session invocations (one claude -p call per Bash tool call) rather than the plan's suggested one-shot 20-session matrix, after the first one-shot attempt's entire result was silently corrupted (usage-limit-induced no-family contamination) and a second attempt's entire result was silently lost (Claude Code session teardown mid-background-job). run_conformance.py appends its run block only at the end of a whole invocation, so any invocation spanning many sessions risks losing everything it ran; single-session invocations make every completed session durable the moment it lands, and each was committed to git immediately."

patterns-established:
  - "A live-measurement plan that risks multi-hour, multi-session execution should size its own invocations to survive interruption -- append after every unit of durable progress, not after the whole batch."

requirements-completed: []  # This plan measures and disposes; it closes no requirement.
  # MOD-04 stays [ ] under the pre-committed Branch 3 rule. AUD-02/AUD-03/MOD-03/MOD-05 were
  # already [x] before this plan and are untouched. AUD-01/ART-01..04 stay [ ], Phase 6
  # LEG-04-owned, untouched except one added sentence in ART-03's annotation (no checkbox move).
  # grep -c "^- \[x\].*UNVERIFIED" .planning/REQUIREMENTS.md returns 0.

coverage:
  - id: D1
    description: "A write-mode conformance rate for the post-03-07 skill exists over 20 scoreable sessions across both models and five fixtures, with exact numerator/denominator, exclusions, model ids, blob SHA, and reproduction command"
    requirement: "MOD-04"
    verification:
      - kind: unit
        ref: "python3 evals/conformance/run_conformance.py --self-test"
        status: pass
      - kind: other
        ref: "evals/conformance/RESULTS-mod04.md 'Combined result' section, Arm 1: conformant 16 of 20 scoreable sessions"
        status: pass
    human_judgment: false
  - id: D2
    description: "A same-instrument, same-model paired baseline against the pre-03-07 skill exists (Branch 3's own requirement), materialised from git, with its own exclusions and blob SHA"
    requirement: "MOD-04"
    verification:
      - kind: other
        ref: "evals/conformance/RESULTS-mod04.md 'Combined result' section, Arm 2: conformant 5 of 11 scoreable sessions"
        status: pass
    human_judgment: false
  - id: D3
    description: "Two real instrument defects (returncode/stderr never inspected; blob SHA ignoring --skill-src) found and fixed, each covered by a new offline --self-test case, neither touching the scoring logic (score_transcript) itself"
    requirement: "N/A"
    verification:
      - kind: unit
        ref: "python3 evals/conformance/run_conformance.py --self-test -- 7 behavior cases, verdicts discriminated: conformant, no-family, rule-before-family, unscoreable"
        status: pass
    human_judgment: false
  - id: D4
    description: "The Branch 3 disposition (mechanically selected before the number was interpreted) is applied consistently across all four trackers with the same N/M figures"
    requirement: "MOD-04"
    verification:
      - kind: other
        ref: "node gsd-tools.cjs windows status -- entry 8 open, entries 7/9 fixed; grep -cE '5/6|14/16' 03-UAT.md >= 2; grep -c 'Phase 6' REQUIREMENTS.md nonzero"
        status: pass
    human_judgment: false
  - id: D5
    description: "No checked box sits beside an UNVERIFIED annotation anywhere in REQUIREMENTS.md; AUD-01 and ART-01..04 remain [ ] and Phase-6-owned"
    requirement: "N/A"
    verification:
      - kind: other
        ref: "grep -c \"^- \\[x\\].*UNVERIFIED\" .planning/REQUIREMENTS.md == 0; grep -cE '^- \\[ \\] \\*\\*(AUD-01|ART-01|ART-02|ART-03|ART-04)\\*\\*' REQUIREMENTS.md == 5"
        status: pass
    human_judgment: false
  - id: D6
    description: "The interpretive framing of Branch 3 (honestly disclosing that the same-instrument paired comparison shows real improvement, 45.5%->60.0%, even though the rule's arithmetic trigger fired 'not improved' against a different, older baseline) is a judgment call a human should be able to reread and confirm"
    requirement: "MOD-04"
    verification: []
    human_judgment: true
    rationale: "This is a substantive interpretive choice (not reproducing a template phrase the plan itself supplied, because the evidence generated while executing that same branch contradicted it) rather than a mechanically checkable fact. A human reviewer should confirm this framing is honest and not softened in either direction before treating WINDOWS.md entry 8's new description as authoritative."

duration: "~22h elapsed wall-clock across 4 interrupted/resumed executor sessions (a harness usage-limit reset, a transient network failure, and a Claude Code session teardown each interrupted an in-flight live-measurement run); active work time was substantially less but was not separately tracked given the interruptions"
completed: 2026-09-16
status: complete
---

# Phase 3 Plan 8: MOD-04 Post-03-07 Conformance Measurement and Branch 3 Disposition Summary

**Measured the post-03-07 write-mode conformance rate at 16/20 (80.0%, both models) with a same-instrument sonnet-5-only paired baseline at 5/11 (45.5%) against the pre-03-07 skill -- a real same-model improvement of 45.5% to 60.0%, still short of the 87.5% closure bar, so MOD-04 stays `[ ]` under the plan's own pre-committed Branch 3 rule.**

## Performance

- **Duration:** ~22h elapsed wall-clock (see frontmatter `duration` for why this is not a clean "active work" figure)
- **Tasks:** 2/2 completed
- **Files modified:** 5 (1 script, 1 results file, 3 planning trackers)
- **Commits:** 9

## Accomplishments

- **The actual measurement exists.** `evals/conformance/RESULTS-mod04.md` now carries a genuine 20-session post-03-07 matrix (both models, five fixtures, two repeats: 16 conformant, 4 rule-before-family, 0 no-family, 2 timeouts excluded) and, going beyond the plan's letter, a same-instrument paired baseline against the materialised pre-03-07 skill (11 scoreable sonnet-5-only sessions: 5 conformant, 6 rule-before-family, 2 exclusions retried and resolved).
- **Two real instrument defects were found and fixed, both discovered mid-measurement.** `run_session()` never inspected `result.returncode` or `result.stderr`, so a `claude -p` invocation that failed for any non-timeout reason had its short error text scored by `score_transcript()` as a real transcript -- producing a false `no-family` verdict indistinguishable from a genuine omission. This is precisely what silently corrupted the first attempted 20-session matrix when the executing account hit a usage limit mid-run (all 10 `claude-opus-5` sessions plus one trailing sonnet session shared the exact same `no family match found (marker_at=None, marker=None)` signature). Fixed via a new `SessionFailedError`, self-test-covered. Separately, `_git_blob_sha()` always computed `git rev-parse HEAD:skills/proof-first/SKILL.md` regardless of `--skill-src` -- meaning the plan's own required Branch-3 paired baseline would have recorded the wrong `SKILL.md` revision for every baseline session. Fixed to hash the actual file under `--skill-src` via `git hash-object`, also self-test-covered.
- **The 20-session run that hit the usage limit is kept, not deleted.** It is annotated `INVALIDATED` in `RESULTS-mod04.md` with the full root-cause explanation, and every session in it was re-collected from scratch under the fixed instrument rather than salvaging any part of it.
- **Branch 3 selected mechanically and disclosed honestly.** `M=20>=16` and `N/M=16/20=0.8<=0.875` selects Branch 3 ("not improved") per the pre-committed rule -- but that condition is defined against the OLD, differently-instrumented 14/16=0.875 figure from 03-05's UAT recipe. This plan's own paired baseline (same instrument, same model, same fixtures) shows a real, measured improvement from 45.5% to 60.0% for sonnet-5. Both facts are stated plainly, side by side, in all four trackers -- the mechanical disposition (stays open, `[ ]`, `partially_resolved`) is honored exactly as written, without silently reproducing the branch template's "did not move it" phrasing where the evidence generated in the process of executing that branch says otherwise.
- **Disposition applied consistently to all four trackers.** `WINDOWS.md` entry 8 (stays `open`, description replaced), `REQUIREMENTS.md` MOD-04 (stays `[ ]`, annotation carries 5/6, 14/16, and 16/20 with model ids, blob SHAs, and the reproduction command), `03-UAT.md` gap G-03-2 (stays `partially_resolved`, evidence block gains the new measurement alongside the prior figures, none deleted). `AUD-01` and `ART-01` through `ART-04` remain untouched at `[ ]`, still Phase 6 LEG-04-owned (`ART-03` gained one sentence noting 03-07's residual-label fix, without moving its checkbox).

## Task Commits

1. **Task 1: Measure the post-edit write-mode conformance rate over at least 16 scoreable live sessions**
   - `bbb8296` (fix) -- returncode/stderr instrument bug
   - `e7dbc9b` (test) -- sonnet-5 arm of post-03-07 matrix
   - `c920486` (test) -- opus-5 A/B/C fixtures
   - `d093465` (test) -- opus-5 D/E fixtures, completing the post-03-07 matrix
   - `a5cf8d5` (fix) -- blob-SHA-from-`--skill-src` instrument bug
   - `9abf166` (test) -- baseline sonnet-5 A/B fixtures
   - `69aa171` (test) -- baseline sonnet-5 C/D fixtures, E network-failure exclusion
   - `593745a` (test) -- baseline sonnet-5 E fixture, completing the paired baseline arm
2. **Task 2: Apply the pre-committed disposition to the four records that track MOD-04**
   - `0fc0446` (docs) -- Branch 3 disposition applied to all four trackers

## Files Created/Modified

- `evals/conformance/run_conformance.py` -- `SessionFailedError`, corrected `_git_blob_sha()`, two new offline `--self-test` cases (7 total, up from 5)
- `evals/conformance/RESULTS-mod04.md` -- the invalidated-and-annotated first attempt, the full post-03-07 matrix, the paired pre-03-07 baseline, and a hand-computed "Combined result" section reconciling every run block with checkable arithmetic
- `.planning/WINDOWS.md` -- entry 8's description replaced with the new measurement and paired-baseline finding (stays `open`)
- `.planning/REQUIREMENTS.md` -- MOD-04 annotation rewritten with all three measurements; ART-03 gained one sentence
- `.planning/phases/03-completeness-audit-artifact-patterns/03-UAT.md` -- gap G-03-2's `post_fix_evidence` gained this plan's measurement, prior figures retained

## Gate Results (verbatim, run after the final commit)

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

Checkbox scan: `grep -nE '^- \[x\].*UNVERIFIED' .planning/REQUIREMENTS.md` returns nothing (0 matches).

## Decisions Made

See `key-decisions` in frontmatter for full rationale. Summary:
- Branch 3 selected by arithmetic before any interpretation (`M=20>=16`, `N/M=0.8<=0.875`).
- The written disposition states the true paired-baseline finding (45.5%->60.0% for sonnet-5) rather than reproducing the branch template's "did not move it" phrase where it would be false.
- The contaminated 20-session run stays fully invalidated; nothing from it was re-admitted even where it looked genuine.
- Two Rule 1 instrument bugs fixed mid-measurement, both self-test-covered, both fixed before the data used in the final disposition was collected.
- Opus-5 paired baseline not run (sonnet-5-only baseline accepted as defensible given repeated live-session interruption risk); disclosed as an unequal-n limitation in all four trackers.
- 03-06's own proving-run sample folded into the baseline tally as one extra genuine data point.
- Measurement driven as many small single-session invocations for durability against interruption, after two prior single-invocation attempts each lost their entire result.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] `run_session()` scored nonzero-exit `claude -p` failures as `no-family` instead of `unscoreable`**
- **Found during:** Task 1, after a background 20-session matrix run showed all 10 `claude-opus-5` sessions and one trailing sonnet session sharing the identical `no family match found (marker_at=None, marker=None)` signature -- statistically implausible as genuine independent live-session outcomes.
- **Issue:** `run_session()` returned `result.stdout` unconditionally, never checking `result.returncode` or reading `result.stderr`. A `claude -p` invocation that failed for quota/auth/any non-timeout reason had its short error text scored by `score_transcript()` as if it were a real transcript.
- **Fix:** Added `SessionFailedError`, raised on any nonzero exit, carrying the exit code and `stderr`; the caller now records it as `unscoreable` with a diagnosable reason. Covered by a new offline `--self-test` case (monkeypatched `subprocess.run`, no real `claude` or network call) proving the failure path is never scored `no-family`.
- **Files modified:** `evals/conformance/run_conformance.py`, `evals/conformance/RESULTS-mod04.md` (the contaminated block annotated `INVALIDATED`, not deleted)
- **Verification:** `python3 evals/conformance/run_conformance.py --self-test` passes (7 cases); the fix caught a genuine subsequent transient network failure correctly as `unscoreable | reason=nonzero exit 1 (empty stderr)` rather than a silent `no-family` during the actual measurement run.
- **Commit:** `bbb8296`

**2. [Rule 1 - Bug] `_git_blob_sha()` always reported the repo's HEAD blob SHA, ignoring `--skill-src`**
- **Found during:** Task 1, on the first Branch-3 paired-baseline attempt -- the recorded "Measured SKILL.md blob SHA" was the post-03-07 SHA even though `--skill-src` pointed at a materialised pre-03-07 copy.
- **Issue:** `_git_blob_sha()` ran `git rev-parse HEAD:skills/proof-first/SKILL.md` unconditionally, which is correct only when `--skill-src` equals the repo's own working tree at HEAD (true of every run before this plan's own paired-baseline requirement first violated that assumption).
- **Fix:** `_git_blob_sha()` now hashes the actual `SKILL.md` under the given `skill_src` via `git hash-object`, content-addressed and independent of HEAD. Covered by a new offline `--self-test` case (monkeypatched `subprocess.run` capturing argv, no real git call) asserting the command references the given path, not a `HEAD:` rev-parse form.
- **Files modified:** `evals/conformance/run_conformance.py`, `evals/conformance/RESULTS-mod04.md` (the one affected run block, a timeout with no scored verdict, corrected in place with a note)
- **Verification:** `git hash-object` on the materialised pre-03-07 copy independently confirmed to equal `1fc1e1092941157191268a8294ab4e1edc65cdac` (matching `git rev-parse 6f62385:skills/proof-first/SKILL.md` and 03-06's own instrument-proving-run figure).
- **Commit:** `a5cf8d5`

---

**Total deviations:** 2 auto-fixed (both Rule 1, both in the measurement instrument itself, both fixed before the disposition-determining data was collected). **Impact:** Both fixes were necessary for correctness of the measurement this plan exists to produce -- an instrument that silently converts harness failures into false non-conformance verdicts, or mislabels which skill revision it measured, cannot support the pre-committed decision rule. No scope creep: the scoring logic (`score_transcript`, `FAMILY_PATTERNS`, `MARKER_PATTERN`) was never touched.

## Issues Encountered

- **Two live-measurement interruptions beyond the instrument bugs above:** a Claude Code session-usage limit reset the executor mid-matrix once, and a Claude Code session teardown discarded an entire in-flight background chunk once (the sonnet-5 arm's first background attempt never appended any run block and had to be re-run entirely as smaller invocations). Neither is a defect in this plan's own work; both are documented in `key-decisions` as the reason the measurement was ultimately driven as many small, durable, single-session invocations rather than a small number of large ones.
- **One transient network failure** (`claude -p` exited 1, empty stderr) during the baseline arm's `E-ambiguous` session -- correctly caught as `unscoreable` by the returncode fix rather than silently scored, and successfully retried after independently re-verifying connectivity.
- **One arithmetic self-correction:** an early draft of the "Combined result" write-up in `RESULTS-mod04.md` mis-stated the sonnet-only subset of the post-03-07 arm as `4 conformant of 8 scoreable = 50.0%`; re-deriving it directly from the file's own run blocks via `awk`/`grep` found the correct figure is `6 conformant of 10 scoreable = 60.0%`. Corrected before this SUMMARY was written; the corrected figure is what appears in all four trackers.

## User Setup Required

None -- no external service configuration required.

## Next Phase Readiness

- MOD-04 remains open. What would close it, given instruction-text has now been tried and measured twice (03-05, 03-07) under two different recipes and both times landed below the 87.5% bar: a lever other than instruction wording -- for example a mechanical post-generation check the skill itself runs before returning (extending the existing self-check gate from "family line present" to "family line precedes any rule marker, verified by re-scanning the drafted response"), since the two instruction-text-only levers already tried have now measured out.
- `WINDOWS.md` entry 8, `REQUIREMENTS.md` MOD-04, and `03-UAT.md` gap G-03-2 all carry the same 16/20 and 5/11 figures and the same paired-baseline finding, checkable against `evals/conformance/RESULTS-mod04.md`'s "Combined result" section without re-running anything.
- `AUD-01` and `ART-01` through `ART-04` remain Phase 6 LEG-04's to close via an actual human paraphrase-boundary read; this plan performed no such read and claims none.
- The conformance instrument (`evals/conformance/run_conformance.py`) is now more robust than at the start of this plan: it correctly distinguishes harness failure from genuine non-conformance, and correctly attributes measurements to the skill revision actually exercised -- both properties Phase 5's own eval harness work will likely want to inherit if it reuses this pattern.

## Self-Check: PASSED

All claimed files found on disk: `evals/conformance/run_conformance.py`, `evals/conformance/RESULTS-mod04.md`, `.planning/WINDOWS.md`, `.planning/REQUIREMENTS.md`, `.planning/phases/03-completeness-audit-artifact-patterns/03-UAT.md`. All nine claimed commit hashes (`bbb8296`, `e7dbc9b`, `c920486`, `d093465`, `a5cf8d5`, `9abf166`, `69aa171`, `593745a`, `0fc0446`) found in `git log`. All four gate commands re-run above with matching output. `grep -c "^- \[x\].*UNVERIFIED" .planning/REQUIREMENTS.md` returns 0. `node gsd-tools.cjs windows status` confirms entry 8 `open`, entries 7 and 9 `fixed`.

---
*Phase: 03-completeness-audit-artifact-patterns*
*Completed: 2026-09-16*
