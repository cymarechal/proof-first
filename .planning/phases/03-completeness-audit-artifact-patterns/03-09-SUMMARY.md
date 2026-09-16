---
phase: 03-completeness-audit-artifact-patterns
plan: 09
subsystem: testing
tags: [conformance-scorer, mod-04, regex, stdlib, evals]

# Dependency graph
requires:
  - phase: 03-completeness-audit-artifact-patterns
    provides: run_conformance.py (03-06), MOD-04 measurement data (03-08)
provides:
  - An anchored score_transcript() that cannot mistake an incidental later family
    phrase for the required opening declaration (CR-01 closed)
  - A run_session() that preserves a decoded partial transcript on timeout instead
    of losing the evidence entirely (WR-01 closed)
  - A standing disclosure in RESULTS-mod04.md that every pre-fix figure is an
    unanchored, unrecoverable, optimistic ceiling
affects: [03-12 (MOD-04 remeasurement), any future run_conformance.py maintenance]

# Actuals (#2632)
actuals:
  tokens: 6300
  tasks: 2
  commits: 2

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Bound a regex search to a declared prefix window (FAMILY_LINE_WINDOW_CHARS)
       rather than searching the whole text, when the contract the search proves
       places its target at a known position"
    - "Compute two offsets being compared against the SAME stripped string, never
       one against stripped and one against the raw input"
    - "Normalise subprocess exception streams (bytes/str/None) before writing them
       to disk, since TimeoutExpired.stdout/.stderr come back as bytes even when
       the original call passed text=True"

key-files:
  created:
    - evals/conformance/transcripts/nonconformant-no-family-late-phrase.txt
    - evals/conformance/transcripts/conformant-family-first-late-phrase.txt
  modified:
    - evals/conformance/run_conformance.py
    - evals/conformance/transcripts/nonconformant-rule-before-family.txt
    - evals/conformance/RESULTS-mod04.md

key-decisions:
  - "requirements-completed left empty despite the plan frontmatter listing MOD-04 -- this plan fixes the measurement instrument and explicitly closes no requirement; MOD-04's checkbox and WINDOWS.md entry 8 are untouched by design (grep-verified 0 before final commit)."
  - "Edited the pre-existing nonconformant-rule-before-family.txt fixture (not listed in Task 1's <files>) to shorten its comment header and body so its family declaration still falls inside the new 400-char anchoring window -- required to keep the plan's own mandated 'existing fixtures keep unchanged verdicts' behavior true and the --self-test gate green."

patterns-established:
  - "A scorer's search bound should be derived from and commented against the actual contract line that motivates it (SKILL.md's write-mode ordering), not invented independently."

requirements-completed: []

coverage:
  - id: D1
    description: "score_transcript()'s family search is bounded to the transcript's opening 400 characters, and both the family and marker offsets are computed against the same stripped string, closing CR-01's false-pass path."
    requirement: "MOD-04"
    verification:
      - kind: unit
        ref: "evals/conformance/run_conformance.py self_test() cases 8 and 9 (inline, no fixture required)"
        status: pass
      - kind: unit
        ref: "evals/conformance/transcripts/nonconformant-no-family-late-phrase.txt and conformant-family-first-late-phrase.txt cross-checked via --self-test"
        status: pass
      - kind: integration
        ref: "python3 -c CR-01 discrimination probe (no-family) and over-anchoring control probe (conformant), both from the plan's <verify> block"
        status: pass
    human_judgment: false
  - id: D2
    description: "run_session() catches subprocess.TimeoutExpired, normalises bytes/str/None stdout/stderr, writes a decoded partial transcript to out_path, then re-raises unchanged so main()'s reason=timeout exclusion is untouched (WR-01 closed)."
    verification:
      - kind: unit
        ref: "evals/conformance/run_conformance.py self_test() case 10 (monkeypatched TimeoutExpired with bytes payloads)"
        status: pass
      - kind: integration
        ref: "python3 -c timeout probe from the plan's <verify> block: prints RAISED ARTIFACT DECODED"
        status: pass
    human_judgment: false
  - id: D3
    description: "RESULTS-mod04.md now carries a 'Scorer anchoring correction (CR-01)' banner ahead of every run block and a matching Caveats bullet, disclosing that every figure recorded before the fix is an optimistic, unrecoverable ceiling. No published figure changed."
    verification:
      - kind: other
        ref: "grep -c '^## Scorer anchoring correction (CR-01)' == 1; banner offset < first run-block offset; '16 of 20 scoreable sessions' count unchanged at 1; git diff shows zero deletions"
        status: pass
    human_judgment: false
  - id: D4
    description: "The project's four real gates (check_repo.py --self-test/--mutation-test/plain, run_conformance.py --self-test) all pass; MOD-04 stays [ ], WINDOWS.md entry 8 stays open, and no REQUIREMENTS.md checkbox reads [x] next to UNVERIFIED."
    verification:
      - kind: integration
        ref: "python3 tools/check_repo.py --self-test / --mutation-test (29 codes) / plain (0 violations); python3 evals/conformance/run_conformance.py --self-test; grep -c '^- \\[x\\].*UNVERIFIED' .planning/REQUIREMENTS.md == 0"
        status: pass
    human_judgment: false

duration: 18min
completed: 2026-09-16
status: complete
---

# Phase 3 Plan 9: Anchor the MOD-04 conformance scorer's family-line search to a 400-char prefix window, and stop timed-out sessions losing their own evidence

**Closed CR-01 (unbounded family-phrase search silently inflating measured conformance) and WR-01 (a timed-out session losing all diagnostic evidence) in `run_conformance.py`, and disclosed in `RESULTS-mod04.md` that every figure recorded before the fix is an optimistic, unrecoverable ceiling.**

## Performance

- **Duration:** 18 min
- **Started:** 2026-09-16T05:40:43Z
- **Completed:** 2026-09-16T05:49:00Z
- **Tasks:** 2
- **Files modified:** 5 (2 created, 3 modified)

## Accomplishments
- `score_transcript()` now bounds its family search to `stripped[:FAMILY_LINE_WINDOW_CHARS]` (400 chars, derived from and commented against `SKILL.md`'s write-mode contract) and computes both the family and marker offsets against the same `stripped` string, so a genuine `no-family` violation can no longer be mis-scored `conformant`/`rule-before-family` just because the drafted body later reuses a common family phrase as ordinary prose.
- Two new committed transcript fixtures prove the fix discriminates in both directions: a transcript with no opening declaration but a late incidental phrase scores `no-family`; a transcript with a genuine opening declaration stays `conformant` even when the same phrase recurs later. Two matching inline `self_test()` cases (8, 9) prove the same thing even in a checkout with no fixture files.
- `run_session()` now catches `subprocess.TimeoutExpired`, normalises `bytes`/`str`/`None` stream payloads (measured directly on this platform: `TimeoutExpired.stdout`/`.stderr` come back as `bytes` even though the call passes `text=True`), writes a decoded partial transcript to `out_path`, then re-raises unchanged — `main()`'s existing `except subprocess.TimeoutExpired` clause still records `unscoreable | reason=timeout` exactly as before. `self_test()` case 10 proves this offline.
- `RESULTS-mod04.md` gained a `## Scorer anchoring correction (CR-01)` section ahead of every run block, and one new Caveats bullet, disclosing the defect, its optimistic-ceiling direction, and that the pre-fix raw transcripts were never written into the repository and cannot be recovered for re-scoring. No published figure moved.
- `self_test()` grew from 7 to 10 behavior cases (7 inline + 3 monkeypatch-style + fixture cross-checks against 5 committed transcripts), and still makes no subprocess or network call.

## Task Commits

1. **Task 1: Anchor the family-line search to the prefix window, and stop a timed-out session losing its own evidence** - `7cde49a` (fix)
2. **Task 2: Disclose in RESULTS-mod04.md that every pre-fix figure is an unanchored, unrecoverable, optimistic ceiling** - `fbe0aa6` (docs)

_Task 1 is `type="tracer"`. Its own `<verify>` (self-test, both discrimination probes, timeout probe, `check_repo.py`) was re-run end-to-end as the tracer feedback gate before Task 2 started — all passed (`HUMAN_VERIFY_MODE=end-of-phase`, no `<human-check>` in the tracer's `<verify>`, so this is the automated re-run-then-continue path, no checkpoint synthesized)._

## Files Created/Modified
- `evals/conformance/run_conformance.py` - `FAMILY_LINE_WINDOW_CHARS` constant; `score_transcript()` reworked to bound the family search and compute both offsets against `stripped`; `run_session()` timeout handling and new `_decode_stream()` helper; `self_test()` cases 8-10 and expanded `fixture_expectations`; updated module docstring ceiling paragraph
- `evals/conformance/transcripts/nonconformant-no-family-late-phrase.txt` - new CR-01 discrimination fixture (expected `no-family`)
- `evals/conformance/transcripts/conformant-family-first-late-phrase.txt` - new over-anchoring control fixture (expected `conformant`)
- `evals/conformance/transcripts/nonconformant-rule-before-family.txt` - shortened so its family declaration still falls inside the new 400-char window (see Deviations)
- `evals/conformance/RESULTS-mod04.md` - new `## Scorer anchoring correction (CR-01)` banner section and one new Caveats bullet; no existing figure or run block changed

## Decisions Made
- `requirements-completed:` left empty in this SUMMARY despite the plan's frontmatter `requirements: [MOD-04]` — this plan fixes a measurement instrument and closes no requirement by explicit design; copying `MOD-04` into `requirements-completed` here risked exactly the auto-flip regression class this repository has already reverted three times (see Deviations below).
- The 400-character window value was taken directly from `03-REVIEW.md`'s CR-01 fix proposal and the plan's own `<action>` text, not independently chosen.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Shortened the pre-existing `nonconformant-rule-before-family.txt` fixture so its family declaration stays inside the new 400-char window**
- **Found during:** Task 1, running `--self-test` after implementing the anchoring bound
- **Issue:** This fixture predates the CR-01 fix and was authored with a verbose comment header plus a long narrative body; its family phrase ("Executive summary") sat at character offset 526-573 in `stripped` text, past the new 400-char window. The plan's own `<behavior>` requires "the three already-committed fixtures keep their existing verdicts (`conformant`, `no-family`, `rule-before-family`) unchanged" — with the window correctly enforced, this fixture flipped from `rule-before-family` to `no-family`, failing `--self-test` and blocking the plan's own hard verification gate. This file was not listed in Task 1's `<files>`, but leaving it broken would have shipped a scorer that fails its own committed regression suite.
- **Fix:** Shortened the comment header and trimmed the body (kept the marker `PF-1.17` first, then the family declaration "Executive summary"), bringing the family offset down to 258 — well inside the 400-char window — while preserving the fixture's original intent (marker precedes family, `rule-before-family` verdict).
- **Files modified:** `evals/conformance/transcripts/nonconformant-rule-before-family.txt`
- **Verification:** `python3 evals/conformance/run_conformance.py --self-test` passes with all three pre-existing fixtures at their original verdicts (`conformant`, `no-family`, `rule-before-family`) plus the two new ones.
- **Committed in:** `7cde49a` (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 bug fix, forced by the plan's own acceptance criteria).
**Impact on plan:** Necessary to satisfy the plan's own `<behavior>`/`<verify>` requirements; no scope creep — only the one pre-existing fixture needed adjustment, and its tested property (marker precedes family) is unchanged.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- `run_conformance.py` is now a correctly-anchored instrument; `03-12` can remeasure MOD-04 against it without inheriting the CR-01 bias.
- `MOD-04` stays `[ ]`, `WINDOWS.md` entry 8 stays `open`, `AUD-01`/`ART-01..04` stay `[ ]` and Phase-6-owned — verified via `grep -c "^- \[x\].*UNVERIFIED" .planning/REQUIREMENTS.md` returning `0` before the final commit.
- No blockers for `03-12`.

## Self-Check: PASSED

- `[ -f evals/conformance/transcripts/nonconformant-no-family-late-phrase.txt ]` → FOUND
- `[ -f evals/conformance/transcripts/conformant-family-first-late-phrase.txt ]` → FOUND
- `git log --oneline --all | grep -q 7cde49a` → FOUND
- `git log --oneline --all | grep -q fbe0aa6` → FOUND
- Re-ran all plan-level `<verification>` commands: `check_repo.py --self-test` PASS, `--mutation-test` → `29 codes discrimination-proven`, plain `check_repo.py` → `0 violations`, `run_conformance.py --self-test` → `self-test PASS - verdicts discriminated: conformant, no-family, rule-before-family, unscoreable`.
- Re-ran both plan `<verify>` discrimination probes: CR-01 probe → `no-family`; over-anchoring control probe → `conformant`.
- Re-ran the timeout probe: `RAISED ARTIFACT DECODED`.
- `grep -c '^## Scorer anchoring correction (CR-01)'` → `1`; banner precedes `## Instrument-proving run`.
- `grep -c "^- \[x\].*UNVERIFIED" .planning/REQUIREMENTS.md` → `0`.

---
*Phase: 03-completeness-audit-artifact-patterns*
*Completed: 2026-09-16*
