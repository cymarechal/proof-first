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
