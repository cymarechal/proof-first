---
phase: 03-completeness-audit-artifact-patterns
reviewed: 2026-09-16T00:00:00Z
depth: standard
files_reviewed: 22
files_reviewed_list:
  - .github/workflows/ci.yml
  - .gitignore
  - evals/conformance/RESULTS-mod04.md
  - evals/conformance/fixtures/A-rfp-answer.md
  - evals/conformance/fixtures/B-proposal-section.md
  - evals/conformance/fixtures/C-exec-summary.md
  - evals/conformance/fixtures/D-demo-discovery.md
  - evals/conformance/fixtures/E-ambiguous.md
  - evals/conformance/run_conformance.py
  - evals/conformance/transcripts/conformant-family-first-late-phrase.txt
  - evals/conformance/transcripts/conformant-family-first.txt
  - evals/conformance/transcripts/nonconformant-no-family-late-phrase.txt
  - evals/conformance/transcripts/nonconformant-no-family.txt
  - evals/conformance/transcripts/nonconformant-rule-before-family.txt
  - NUMBERING.md
  - README.md
  - skills/proof-first/SKILL.md
  - skills/proof-first/references/artifact-patterns.md
  - skills/proof-first/references/checklist.md
  - skills/proof-first/references/completeness-audit.md
  - skills/proof-first/references/worked-examples.md
  - tools/check_repo.py
findings:
  critical: 1
  warning: 2
  info: 1
  total: 4
status: issues_found
---

# Phase 03: Code Review Report

**Reviewed:** 2026-09-16
**Depth:** standard
**Files Reviewed:** 22
**Status:** issues_found

## Summary

This round's three prior findings (CR-01 anchored family-line window, CR-02 README pointer, WR-01
timed-out-session transcript preservation) are verified fixed and did not reintroduce regressions:

- `score_transcript()`'s 400-char window computes both the family offset and the marker offset
  against the identical `stripped` string (confirmed by direct offset arithmetic against every
  committed fixture, and by running `--self-test`, which passes all ten inline cases plus all five
  transcript fixtures).
- `run_session()`'s `TimeoutExpired` handling correctly decodes `bytes | str | None` streams
  (verified empirically on this platform: `TimeoutExpired.stdout` really is `bytes` even with
  `text=True`), writes a readable partial transcript, and re-raises unchanged so `main()`'s
  exclusion accounting is untouched. A timed-out session's on-disk artifact is never fed to
  `score_transcript()` regardless of its content, so a corrupted/partial transcript cannot silently
  become a scored verdict.
- `tools/check_repo.py --self-test`, `--mutation-test` (31/31 codes discrimination-proven), and a
  live run all pass with 0 violations at HEAD, and the new `skill-family-order-gate-missing` /
  `readme-results-pointer-missing` checks both fire correctly against their registered mutations
  and stay silent on the real, unmutated tree.
- `RESULTS-mod04.md`'s "Anchored remeasurement result (03-12)" section states the true finding
  (a 10-point *decline*, Arm A 30.0% vs Arm B 40.0%) plainly, including in `WINDOWS.md` entry 8 —
  it does not spin the decline as improvement, and every blob SHA and commit citation I
  independently re-derived via `git hash-object` / `git rev-parse` matched the file's claims
  exactly.

One live-scoped, previously-undiscovered defect was found: the instrument that produces this
project's one committed measurement can silently lose an entire in-progress run's results if the
Python process is interrupted before its loop finishes — the exact failure mode `RESULTS-mod04.md`
itself already documents having happened twice, worked around operationally (many single-session
invocations) rather than fixed in code. Two lower-severity documentation/consistency gaps are also
recorded below.

## Critical Issues

### CR-01: `run_conformance.py`'s live-mode results are held in memory and lost wholesale if the process is interrupted before the run completes

**File:** `evals/conformance/run_conformance.py:641-766` (specifically the `lines = []` accumulator at line 687 and the single deferred write at lines 761-762)

**Issue:** `main()`'s live-mode loop iterates over every `model × fixture × repeat` combination,
appending each session's result to an in-memory `lines` list (`lines.append(...)` at lines 736 and
751), and only writes that list to `RESULTS-mod04.md` once, after the *entire* loop has finished
(`with open(out_path, 'a') as f: f.writelines(lines)` at lines 761-762). Every per-session
exception handler (`TimeoutExpired`, `SessionFailedError`, `SubprocessError`/`OSError`) is scoped
to a single iteration and lets the loop continue — but nothing protects against the process itself
being killed or crashing between iterations (SIGTERM, SIGKILL, an uncaught exception type, or the
external interruption a `claude -p` subprocess call cannot itself prevent). In that case every
session that already completed and was scored in that same invocation is discarded, because it
was never durably written.

This is not hypothetical: `RESULTS-mod04.md`'s own "Combined result (03-08-PLAN.md...)" section
states plainly, "two earlier attempts at a single large invocation each lost their entire result
when the invoking process was interrupted mid-run (a Claude Code session-usage limit, then a
Claude Code session teardown)." The project's response was an *operational* workaround — driving
the matrix "as many small single-session invocations rather than one large matrix invocation" —
not a code fix. The default, documented usage pattern in this same file's own module docstring
(`python3 evals/conformance/run_conformance.py [--fixtures A,B,C] [--models MODEL,...] [--repeats
N] ...`) is still a multi-session, single-invocation call with no incremental persistence, so the
same data-loss failure is fully reproducible today against the current code, not just a historical
artifact.

For a repository whose entire premise is "measured claims must be reproducible from a committed
script" (per this project's own `CLAUDE.md`), an instrument that can silently discard already-
measured, already-scored sessions on an ordinary interruption is a correctness/data-loss defect in
the instrument itself, not merely an operational inconvenience — and it is the same class of
defect WR-01 already fixed for the *individual transcript* case (a timed-out session's own
transcript), just left open for the *aggregate results file* case.

**Fix:** Write each session's result line to `out_path` immediately after it is computed, instead
of batching every line into memory until the loop finishes. For example:

```python
out_path = pathlib.Path(args.out)
out_path.parent.mkdir(parents=True, exist_ok=True)

with open(out_path, 'a') as f:
    f.write(f'\n## Run recorded {datetime.datetime.now(datetime.timezone.utc).isoformat()}Z\n')
    f.write(f'Measured SKILL.md blob SHA: `{skill_sha}`\n')
    f.flush()

    for model in models:
        for fixture_stem in fixture_stems:
            for repeat in range(args.repeats):
                ...  # run_session(...) / exception handling unchanged
                f.write(
                    f'- {date_str} | model={model} | fixture={fixture_stem} | repeat={repeat} '
                    f'| verdict={verdict} | evidence={evidence}\n'
                )
                f.flush()

    f.write(f'\nconformant {conformant_count} of {scoreable_count} scoreable sessions\n')
    f.write(f'unscoreable {len(unscoreable_sessions)} sessions\n')
    for model, fixture_stem, repeat, reason in unscoreable_sessions:
        f.write(f'  - excluded: model={model} fixture={fixture_stem} repeat={repeat} reason={reason}\n')
```

This makes every already-scored session durable the moment it is scored, so an interruption at
session *N* of *M* loses at most the in-flight session, not the *N-1* already-completed ones — the
same guarantee WR-01 already established for a single session's own transcript, extended to the
aggregate results file that actually backs this project's published numbers.

## Warnings

### WR-01: `RESULTS-mod04.md`'s Arm A `no-family` breakdown enumerates one fewer session than its own stated count

**File:** `evals/conformance/RESULTS-mod04.md:756-757`

**Issue:** The "Anchored remeasurement result (03-12)" section states:

```
- no-family: 7 (`A-rfp-answer` x2, `C-exec-summary` x2, `D-demo-discovery` second attempt,
  `E-ambiguous` second attempt)
```

That parenthetical names 2 + 2 + 1 + 1 = 6 sessions, not 7. Cross-checking against the raw run
blocks between the Arm A blob SHA (`fadc48613f71fb29d55b42f70805225f9087a2b9`) at lines 565-649,
there are in fact 7 `no-family` verdicts: the two `A-rfp-answer` sessions, the two `C-exec-summary`
sessions, one `D-demo-discovery` session, one `E-ambiguous` session, **and** the `B-proposal-section`
first attempt at `2026-09-16T06:42:11.983431+00:00Z` (`verdict=no-family | evidence=no family match
found within the first 400 chars (marker_at=1013, marker='PF-2.13')`), which is omitted from the
enumeration entirely. The aggregate figures (`N_A = 3`, `M_A = 10`, `30.0%`) are correct — this is
an itemization gap, not a headline-number error — but this file explicitly frames itself as
"re-derivable by anyone... without re-running anything," and a reader manually verifying the
breakdown against the raw blocks will find the count does not add up.

**Fix:** Add the missing session to the enumeration:

```
- no-family: 7 (`A-rfp-answer` x2, `B-proposal-section` first attempt, `C-exec-summary` x2,
  `D-demo-discovery` second attempt, `E-ambiguous` second attempt)
```

### WR-02: `check_skill_family_line_gate()` and `check_skill_family_order_gate()` use inconsistent case-sensitivity for the same class of anchor match

**File:** `tools/check_repo.py:1385-1466`

**Issue:** `check_skill_family_line_gate()` (added in 03-07) matches its two anchors
case-sensitively against the raw section body:

```python
if 'artifact family' not in body:
    missing.append('the phrase naming the artifact family')
if 'No family fits' not in body:
    missing.append("the 'No family fits' value")
```

Its sibling, `check_skill_family_order_gate()` (added in 03-11, the subject of this round's
`skill-family-order-gate-missing` gap-closure), lowercases the body before matching its own two
anchors:

```python
body_lower = body.lower()
if 're-scan' not in body_lower:
    ...
if 'before any rule marker' not in body_lower:
    ...
```

Both checks exist for the identical reason (asserting SKILL.md's self-check section still states
an instruction after some future edit) and both are exercised by the review prompt's own stated
concern about "a sibling mutation matcher" breaking on a plausible rewording. As written, a future
edit that capitalizes the family-line anchor (e.g. "the line naming the Artifact Family" — a
stylistically unremarkable rewording, and one the order-gate's own case-insensitive anchors would
survive unaffected) would trip `skill-family-line-gate-missing` as a false CI failure, while the
semantically identical class of edit to the order-gate's anchors would not. This is exactly the
brittleness class the 03-11 gap closure was written to guard against for the order gate; the line
gate was left with the older, more brittle policy.

**Fix:** Lowercase `body` once in `check_skill_family_line_gate()` (matching its sibling) and
match lowercase anchors, e.g.:

```python
body_lower = body.lower()
missing = []
if 'artifact family' not in body_lower:
    missing.append('the phrase naming the artifact family')
if 'no family fits' not in body_lower:
    missing.append("the 'No family fits' value")
```

## Info

### IN-01: `tools/check_repo.py`'s module docstring claims a `skill-token-budget-exceeded` violation that no longer exists at HEAD

**File:** `tools/check_repo.py:322-328`

**Issue:** The violation-code catalog at the top of the file states: "As of this writing this code
fires against this repository's own `skills/proof-first/SKILL.md` — a known, tracked, open
finding against CAT-08 (see `.planning/WINDOWS.md`), not a defect in this check." This predates
the current phase's diff (it is present in the pre-phase-3 baseline), but it is stale relative to
the current repository state: `skills/proof-first/SKILL.md` is measured at 3,710 words / an
estimated 4,823 tokens (below the 5,000-token ceiling with a ~177-token margin), `python3
tools/check_repo.py` reports 0 violations against the live tree, and `WINDOWS.md` entry 5 itself
records this exact finding as `status: fixed` (resolved 2026-09-11, during Phase 2, before Phase 3
began). Since this file is itself a document whose accuracy the project holds to a "measured
claims or no claims" standard, this stale self-description is worth correcting even though it
predates this round's own changes and does not affect CI behavior (the docstring is prose, not
executable).

**Fix:** Update the sentence to reflect the fixed/waived status, e.g.: "This check previously fired
against this repository's own `skills/proof-first/SKILL.md` before the 02-07/02-08 trim (see
`WINDOWS.md` entry 5, `status: fixed`); it is silent against the current tree."

---

_Reviewed: 2026-09-16_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
