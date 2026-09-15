---
phase: 03-completeness-audit-artifact-patterns
plan: 06
subsystem: eval-harness
tags: [conformance, mod-04, reproducibility, evidence]

# Dependency graph
requires:
  - phase: 03-completeness-audit-artifact-patterns
    provides: "03-05's gap-closure fix and 03-UAT.md's 18-session live harness pass that surfaced WINDOWS.md entry 8 (2/16 residual MOD-04 failures)"
provides:
  - "evals/conformance/run_conformance.py: stdlib-only scorer + live-session driver, --self-test mode proven offline"
  - "Five committed weak-draft fixtures (A-E) covering the four artifact families plus the ambiguous case"
  - "Three committed transcript fixtures proving the scorer discriminates conformant / no-family / rule-before-family from file, not just inline cases"
  - "evals/conformance/RESULTS-mod04.md: the instrument's own proving run, recorded and clearly labeled as not the MOD-04 measurement"
  - "CI line running the scorer's self-test alongside the three existing check_repo.py commands"
affects: [03-08-plan-mod04-measurement, phase-5-eval-harness]

# Actuals (#2632)
actuals:
  tokens: 7536
  tasks: 2
  commits: 2

tech-stack:
  added: []
  patterns:
    - "Conformance scorer mirrors tools/check_repo.py's self-test/mutation-test idiom: known-good and known-bad committed fixtures, a discrimination proof printed as one PASS line naming every verdict covered"
    - "Live sessions run in tempfile.mkdtemp() directories outside the repo, one writer per output path, no --bare (skill auto-discovery must stay on for the measurement to mean anything)"

key-files:
  created:
    - evals/conformance/run_conformance.py
    - evals/conformance/fixtures/A-rfp-answer.md
    - evals/conformance/fixtures/B-proposal-section.md
    - evals/conformance/fixtures/C-exec-summary.md
    - evals/conformance/fixtures/D-demo-discovery.md
    - evals/conformance/fixtures/E-ambiguous.md
    - evals/conformance/transcripts/conformant-family-first.txt
    - evals/conformance/transcripts/nonconformant-no-family.txt
    - evals/conformance/transcripts/nonconformant-rule-before-family.txt
    - evals/conformance/RESULTS-mod04.md
  modified:
    - .github/workflows/ci.yml

key-decisions:
  - "The tracer's live proving run scored rule-before-family, not conformant -- PF-3.3 was cited before the RFP and RFI response family line was named. This is not treated as a defect in the runner: it is a genuine live sample of the exact residual failure mode WINDOWS.md entry 8 already records, and this plan does not attempt to interpret or close it (03-08 owns that)."
  - "self_test() asserts all four verdicts inline first (independent of any committed transcript file), then cross-checks the three committed transcript fixtures if present. This lets Task 1's own --self-test exit 0 and name all four verdicts before Task 2 authors the transcript fixtures, while Task 2's addition still makes an edited fixture fail the same self-test."
  - "One transcript fixture (nonconformant-rule-before-family.txt) initially failed its own named property because 'Executive summary' was soft-wrapped across a line break, splitting the literal two-word match -- fixed by moving the wrap point, following this repo's own 02-04 precedent for the same class of defect (never touching the regex to work around the wrap)."
  - "datetime.datetime.utcnow() was replaced with datetime.datetime.now(datetime.timezone.utc) after the first live run printed Python's own deprecation warning -- a Rule 1 bug fix, not a deviation, since stdlib-only aging APIs are exactly the kind of blocking issue this repo's zero-dependency posture cannot route around with a newer library."

patterns-established:
  - "Conformance-instrument fixtures (fixtures/*.md) are weak drafts built only from examples/deal-brief.md and must never name their own artifact family -- enforced by both a task acceptance criterion and a CI-adjacent self-test cross-check."

requirements-completed: []  # This plan builds the measurement instrument only. It does not
  # complete MOD-04 or any other requirement -- 03-08-PLAN.md owns running the actual
  # measurement and deciding closure. REQUIREMENTS.md checkboxes are untouched by this plan.

coverage:
  - id: D1
    description: "run_conformance.py's score_transcript() correctly discriminates conformant, no-family, rule-before-family, and unscoreable, proven offline with no model call"
    requirement: "MOD-04"
    verification:
      - kind: unit
        ref: "python3 evals/conformance/run_conformance.py --self-test"
        status: pass
    human_judgment: false
  - id: D2
    description: "One real claude -p write-mode session, driven by the committed runner against the shipped skill in an isolated directory, produced a non-empty transcript and a recorded verdict with model id and SKILL.md blob SHA"
    requirement: "MOD-04"
    verification:
      - kind: other
        ref: "evals/conformance/RESULTS-mod04.md run block dated 2026-09-15T02:47:51Z"
        status: pass
    human_judgment: false
  - id: D3
    description: "Five fixtures covering the four artifact families plus the ambiguous case are committed and none names its own family"
    requirement: "ART-01"
    verification:
      - kind: other
        ref: "grep -rEi over evals/conformance/fixtures/ for the four frozen family strings -- zero hits"
        status: pass
    human_judgment: false
  - id: D4
    description: "CI runs the scorer's self-test alongside the three existing check_repo.py commands, so the scorer cannot silently rot"
    requirement: "N/A"
    verification:
      - kind: other
        ref: ".github/workflows/ci.yml -- fourth command added to the single check job"
        status: pass
    human_judgment: false

duration: 38min
completed: 2026-09-15
status: complete
---

# Phase 03 Plan 06: Conformance Scorer and One Live MOD-04 Proving Session Summary

**Built a stdlib-only, self-testing conformance scorer and fixture set that turns 03-UAT.md's ad-hoc MOD-04 recipe into one committed command, then proved it end to end with one real `claude -p` session against the shipped skill.**

## Performance

- **Duration:** 38 min
- **Tasks:** 2/2 completed
- **Files modified:** 11 (1 new script, 9 new fixture/transcript/results files, 1 CI file)

## Accomplishments

- `evals/conformance/run_conformance.py` written as a Python 3 stdlib-only script (imports limited to `argparse`, `datetime`, `json`, `pathlib`, `re`, `shutil`, `subprocess`, `sys`, `tempfile`, mechanically verified by an AST import check). Implements `score_transcript()`, `run_session()`, `self_test()`, and `main()` exactly as specified, with `FAMILY_PATTERNS` byte-identical to `tools/check_repo.py`'s `ARTIFACT_FAMILY_SECTIONS` for the four frozen family strings, plus SKILL.md's write-mode phrasings and the `No family fits` value.
- `--self-test` proves the scorer discriminates `conformant`, `no-family`, `rule-before-family`, and `unscoreable` entirely offline (no subprocess call, no network call) via five inline behavior cases, then cross-checks the three committed transcript fixtures if present -- an edited fixture that no longer exhibits its named property now fails `--self-test`.
- Five weak-draft fixtures (`A-rfp-answer.md` through `E-ambiguous.md`), each 141-196 words, each built only from `examples/deal-brief.md`'s canonical facts, each containing unquantified or unevidenced claims, and none naming its own artifact family (mechanically verified by grep). `E-ambiguous.md` deliberately spans Solution proposal and Demo and discovery material.
- One real live `claude -p --model claude-sonnet-5` write-mode session was driven by the committed script (via its actual CLI, not a library shortcut) against the current shipped `skills/proof-first/SKILL.md`, from an isolated `tempfile.mkdtemp()` directory outside the repository. It produced a non-empty transcript and a recorded verdict, with the model id, fixture stem, and the measured SKILL.md blob SHA (`1fc1e109...`, 40 characters) all written to `evals/conformance/RESULTS-mod04.md`.
- `.github/workflows/ci.yml` gained a fourth command (`python3 evals/conformance/run_conformance.py --self-test`) in the single existing `check` job -- no matrix, no second job, no install step, no dependency.
- The `check_repo.py` baseline is untouched: 27 codes discrimination-proven, 0 violations, confirmed by a fresh `--self-test`/`--mutation-test`/bare run after every task.

## Task Commits

1. **Task 1: End-to-end "one live write-mode session is measured by a committed script"** - `c4efe2e` (feat)
2. **Task 2: Expand to the full fixture set and wire the scorer's self-test into CI** - `978f8cb` (test)

## Files Created/Modified

- `evals/conformance/run_conformance.py` - the runner: constants, `score_transcript()`, `run_session()`, `self_test()`, `main()`
- `evals/conformance/fixtures/A-rfp-answer.md` through `E-ambiguous.md` - five weak-draft fixtures, built from `examples/deal-brief.md`
- `evals/conformance/transcripts/conformant-family-first.txt`, `nonconformant-no-family.txt`, `nonconformant-rule-before-family.txt` - three synthetic, plainly-labeled scorer fixtures
- `evals/conformance/RESULTS-mod04.md` - the instrument's own proving run, explicitly labeled as not the MOD-04 measurement
- `.github/workflows/ci.yml` - one added line, no other change

## Gate Results (verbatim)

```
$ python3 tools/check_repo.py --self-test
self-test PASS - verified violation codes: artifact-family-section-missing, catalog-count-mismatch,
catalog-count-unstated, catalog-id-drift, catalog-opening-rule-count, dup-figure-key, dup-id,
figure-order, framework-statement-missing, frontmatter-description-invalid, frontmatter-name-mismatch,
frontmatter-unknown-key, frontmatter-unparseable, license-missing, mc-catalog-id-drift,
mc-count-mismatch, mc-count-unstated, mc-rule-in-skill, pointer-duplicated, pointer-missing,
pointer-unparseable, range-id, revived-id, skill-token-budget-exceeded, skill-too-long, undefined-id,
unlisted-figure

$ python3 tools/check_repo.py --mutation-test
mutation-test PASS: 27 codes discrimination-proven

$ python3 tools/check_repo.py
check_repo: 0 violations

$ python3 evals/conformance/run_conformance.py --self-test
self-test PASS - verdicts discriminated: conformant, no-family, rule-before-family, unscoreable
```

Determinism spot-check (`python3 tools/check_repo.py` run twice, `diff -q` on the outputs): identical, no diff.

## Live Verification

One real `claude -p` write-mode session, model `claude-sonnet-5`, fixture `A-rfp-answer`, run via the committed script's own CLI (`python3 evals/conformance/run_conformance.py --skill-src skills/proof-first --fixtures A-rfp-answer --models claude-sonnet-5 --repeats 1 --out evals/conformance/RESULTS-mod04.md`), from an isolated temp directory outside this repository, with `--disallowedTools Write Edit Bash NotebookEdit` and no `--bare`.

**Result:** `rule-before-family` -- `PF-3.3` was cited at offset 371, before the `RFP and RFI response` family line at offset 972. Measured SKILL.md blob SHA: `1fc1e1092941157191268a8294ab4e1edc65cdac` (matches `git rev-parse HEAD:skills/proof-first/SKILL.md`).

This is a real, informative data point -- it happens to land in the exact residual failure mode `WINDOWS.md` entry 8 already records at roughly a 1-in-8 rate (2 of 16 post-fix sessions named no family at all; this single tracer session named no rule marker precedes the family name but does show a marker preceding it). It is recorded in `RESULTS-mod04.md` under a heading stating plainly this is the instrument's proving run, not the MOD-04 measurement. `03-08-PLAN.md` owns running the actual measurement against a candidate fix and deciding whether MOD-04 closes.

## Decisions Made

- **Verdict recorded, not interpreted:** the tracer run's `rule-before-family` verdict is reported as-is. This plan's job was to prove the instrument works end to end, not to draw a conclusion about MOD-04's closure state from a single sample.
- **self_test() design:** inline behavior cases run unconditionally (proving Task 1's own `--verify` gate before any transcript fixture exists); file-based fixture checks run only when the file is present, so Task 2's addition strengthens the same function without needing a second code path.
- **datetime.utcnow() deprecation:** fixed to timezone-aware `datetime.now(datetime.timezone.utc)` immediately after the first live run surfaced Python's own deprecation warning -- a Rule 1 fix, applied before the Task 1 commit.

## Deviations from Plan

**1. [Rule 1 - Bug] Line-wrap defect in `nonconformant-rule-before-family.txt`**
- **Found during:** Task 2, immediately after authoring the three transcript fixtures
- **Issue:** the literal two-word phrase "Executive summary" was split across a soft-wrapped line break, so `FAMILY_PATTERNS`' `Executive summary` regex (which requires a literal space) never matched, and `--self-test` reported the fixture as `no-family` instead of its named `rule-before-family`.
- **Fix:** moved the wrap point so "Executive summary" reads on one physical line; no regex or content-meaning change. This is the same class of defect this repository's own 02-04 plan hit and fixed the same way (reword the line wrap, not the check).
- **Files modified:** `evals/conformance/transcripts/nonconformant-rule-before-family.txt`
- **Verification:** `python3 evals/conformance/run_conformance.py --self-test` passes, discriminating all three transcript fixtures from file.
- **Commit:** folded into `978f8cb` (the fixture was authored and fixed within the same Task 2 commit; no separate commit needed since the defect was caught before any commit).

**2. [Rule 1 - Bug] `datetime.datetime.utcnow()` deprecation warning**
- **Found during:** Task 1, after the first live-mode CLI invocation printed Python's `DeprecationWarning`
- **Issue:** `datetime.datetime.utcnow()` is deprecated in current Python and scheduled for removal; a script meant to be reproducible for years should not carry a warning from its own stdlib on day one.
- **Fix:** replaced both call sites with `datetime.datetime.now(datetime.timezone.utc)`.
- **Files modified:** `evals/conformance/run_conformance.py`
- **Verification:** re-ran `--self-test` and the live CLI proving run; both clean, no warnings, `RESULTS-mod04.md`'s recorded run block unaffected (it was written before the fix, using the old but functionally identical timestamp call).
- **Commit:** folded into `c4efe2e` (fixed before the Task 1 commit).

**Total deviations:** 2 auto-fixed (both Rule 1). **Impact:** both are pre-commit fixes with no effect on shipped behavior or scope; neither changed any acceptance criterion's outcome.

## Threat Flags

None new beyond what `03-06-PLAN.md`'s own `<threat_model>` already registers (T-03-01 through T-03-03, all low severity, all mitigated or accepted as written in the plan). No `high` or `critical` threat is present.

## Known Stubs

None.

## Issues Encountered

None beyond the two deviations above, both resolved within the same task before its commit.

## Next Phase Readiness

- The conformance instrument is committed, self-tested, CI-enforced, and proven against one real live session.
- `03-08-PLAN.md` can now run the actual MOD-04 measurement (candidate fix, full fixture set, enough repeats to move past a single-sample result) using this exact script rather than a re-derived recipe.
- The tracer's own live result (`rule-before-family`) is one more data point consistent with `WINDOWS.md` entry 8's existing residual-failure finding; it does not change MOD-04's `[ ]` status, which remains this phase's responsibility to close via `03-08-PLAN.md`.

## Self-Check: PASSED

All claimed files found on disk: `evals/conformance/run_conformance.py`, all five `fixtures/*.md`, all three `transcripts/*.txt`, `evals/conformance/RESULTS-mod04.md`, `.github/workflows/ci.yml`. Both claimed commit hashes (`c4efe2e`, `978f8cb`) found in `git log`.

---
*Phase: 03-completeness-audit-artifact-patterns*
*Completed: 2026-09-15*
