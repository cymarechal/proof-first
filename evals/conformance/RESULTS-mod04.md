# MOD-04 Conformance Results

Generated and appended to by `evals/conformance/run_conformance.py`. Each `## Run
recorded` block below is a raw log of one invocation of that script; do not hand-edit
these blocks. This file is not itself the MOD-04 measurement, and the run below is not
that measurement either — it is the instrument's own proving run, recorded here per
`03-06-PLAN.md`'s `<output>` requirement. `03-08-PLAN.md` owns running the actual
MOD-04 measurement against a candidate fixed `SKILL.md` and reporting the numerator and
denominator that decide whether MOD-04 closes.

## Instrument-proving run (03-06-PLAN.md Task 1)

One real `claude -p` write-mode session, driven by this committed script against the
skill exactly as it was shipped at the start of this gap-closure plan (i.e. before any
edit this plan or `03-07`/`03-08` might make), from an isolated directory outside this
repository. Recorded below with its model id, fixture, verdict, and the measured
`SKILL.md` blob SHA — proving the runner drives a real session and writes a scoreable
verdict end to end, not proving a conformance rate.

The recorded verdict happened to be `rule-before-family`: `PF-3.3` was cited before the
`RFP and RFI response` family line was named. This is consistent with — and adds one
more data point to — the residual failure mode `WINDOWS.md` entry 8 already records at
roughly a 1-in-8 rate; it is not a new finding and this plan does not attempt to
interpret or close it. That is `03-08-PLAN.md`'s job.

## Run recorded 2026-09-15T02:47:51.963922Z
Measured SKILL.md blob SHA: `1fc1e1092941157191268a8294ab4e1edc65cdac`
- 2026-09-15 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=0 | verdict=rule-before-family | evidence=marker 'PF-3.3' at offset 371 precedes family 'RFP and RFI response' at offset 972

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## INVALIDATED run 2026-09-15T03:11:24.046796+00:00Z -- DO NOT use for MOD-04

This block is kept, not deleted, so the failure is auditable. It must not be used to compute
the MOD-04 rate.

**What happened:** the executor running this matrix hit its own harness usage limit partway
through the run. The 10 sonnet-5 sessions that ran before the limit hit are genuine (varied
verdicts, real byte offsets, real marker names). Every one of the 10 claude-opus-5 sessions
that follow, plus the immediately-preceding `E-ambiguous repeat=1` sonnet session, instead
carries the identical signature `verdict=no-family | evidence=no family match found
(marker_at=None, marker=None)` -- eleven sessions in a row producing byte-for-byte the same
evidence string across five different fixtures and two different models is not a plausible
live-session outcome; it is the fingerprint of one error condition scored eleven times.

**Root cause, confirmed and fixed:** `run_session()` in `evals/conformance/run_conformance.py`
captured only `result.stdout` and never inspected `result.returncode` or `result.stderr`. A
`claude -p` invocation that fails for quota/auth/any non-timeout reason had its short error
text scored by `score_transcript()` as if it were a real transcript -- no family pattern, no
rule marker, so it silently became a `no-family` verdict indistinguishable from a genuine
session that actually omitted the family line. Fixed in the commit immediately following this
one: `run_session()` now raises `SessionFailedError` on any nonzero exit, carrying the exit
code and `stderr`; the caller records it as `unscoreable` with a diagnosable reason. Covered
by a sixth offline `--self-test` case that monkeypatches `subprocess.run` to reproduce this
exact failure shape and asserts it is never scored `no-family`.

The run block below is retained verbatim as it was originally written, for audit only.

## Run recorded 2026-09-15T03:11:24.046796+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=0 | verdict=rule-before-family | evidence=marker 'PF-3.3' at offset 281 precedes family 'RFP answer' at offset 947
- 2026-09-15 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=1 | verdict=conformant | evidence=family 'RFP answer' at offset 5, marker_at=678
- 2026-09-15 | model=claude-sonnet-5 | fixture=B-proposal-section | repeat=0 | verdict=conformant | evidence=family 'Solution proposal' at offset 182, marker_at=652
- 2026-09-15 | model=claude-sonnet-5 | fixture=B-proposal-section | repeat=1 | verdict=rule-before-family | evidence=marker 'PF-3.3' at offset 188 precedes family 'Solution proposal' at offset 495
- 2026-09-15 | model=claude-sonnet-5 | fixture=C-exec-summary | repeat=0 | verdict=conformant | evidence=family 'executive summary' at offset 73, marker_at=313
- 2026-09-15 | model=claude-sonnet-5 | fixture=C-exec-summary | repeat=1 | verdict=no-family | evidence=no family match found (marker_at=240, marker='PF-1.13')
- 2026-09-15 | model=claude-sonnet-5 | fixture=D-demo-discovery | repeat=0 | verdict=unscoreable | reason=timeout
- 2026-09-15 | model=claude-sonnet-5 | fixture=D-demo-discovery | repeat=1 | verdict=conformant | evidence=family 'Demo or discovery material' at offset 805, marker_at=1019
- 2026-09-15 | model=claude-sonnet-5 | fixture=E-ambiguous | repeat=0 | verdict=conformant | evidence=family 'No family fits' at offset 277, marker_at=1161
- 2026-09-15 | model=claude-sonnet-5 | fixture=E-ambiguous | repeat=1 | verdict=no-family | evidence=no family match found (marker_at=None, marker=None)
- 2026-09-15 | model=claude-opus-5 | fixture=A-rfp-answer | repeat=0 | verdict=no-family | evidence=no family match found (marker_at=None, marker=None)
- 2026-09-15 | model=claude-opus-5 | fixture=A-rfp-answer | repeat=1 | verdict=no-family | evidence=no family match found (marker_at=None, marker=None)
- 2026-09-15 | model=claude-opus-5 | fixture=B-proposal-section | repeat=0 | verdict=no-family | evidence=no family match found (marker_at=None, marker=None)
- 2026-09-15 | model=claude-opus-5 | fixture=B-proposal-section | repeat=1 | verdict=no-family | evidence=no family match found (marker_at=None, marker=None)
- 2026-09-15 | model=claude-opus-5 | fixture=C-exec-summary | repeat=0 | verdict=no-family | evidence=no family match found (marker_at=None, marker=None)
- 2026-09-15 | model=claude-opus-5 | fixture=C-exec-summary | repeat=1 | verdict=no-family | evidence=no family match found (marker_at=None, marker=None)
- 2026-09-15 | model=claude-opus-5 | fixture=D-demo-discovery | repeat=0 | verdict=no-family | evidence=no family match found (marker_at=None, marker=None)
- 2026-09-15 | model=claude-opus-5 | fixture=D-demo-discovery | repeat=1 | verdict=no-family | evidence=no family match found (marker_at=None, marker=None)
- 2026-09-15 | model=claude-opus-5 | fixture=E-ambiguous | repeat=0 | verdict=no-family | evidence=no family match found (marker_at=None, marker=None)
- 2026-09-15 | model=claude-opus-5 | fixture=E-ambiguous | repeat=1 | verdict=no-family | evidence=no family match found (marker_at=None, marker=None)

conformant 5 of 19 scoreable sessions
unscoreable 1 sessions
  - excluded: model=claude-sonnet-5 fixture=D-demo-discovery repeat=0 reason=timeout

**End of invalidated run.** The `5 of 19` line above is the pre-fix scorer's own summary as
written and is NOT the MOD-04 measurement. 11 of the 19 "scoreable" sessions it counted are
the contaminated no-family signature described above. A new run against the fixed instrument
follows below.
