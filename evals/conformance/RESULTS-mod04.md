# MOD-04 Conformance Results

Generated and appended to by `evals/conformance/run_conformance.py`. Each `## Run
recorded` block below is a raw log of one invocation of that script; do not hand-edit
these blocks. This file is not itself the MOD-04 measurement, and the run below is not
that measurement either — it is the instrument's own proving run, recorded here per
`03-06-PLAN.md`'s `<output>` requirement. `03-08-PLAN.md` owns running the actual
MOD-04 measurement against a candidate fixed `SKILL.md` and reporting the numerator and
denominator that decide whether MOD-04 closes.

## Scorer anchoring correction (CR-01)

Every run block recorded in this file was produced by an unanchored scorer, and every
figure computed from those run blocks is an optimistic ceiling, not a precise
measurement. Read this before any figure below.

**The defect.** `score_transcript()`'s family search ran over the entire transcript
with no bound. `SKILL.md`'s write-mode contract requires the artifact-family line to
be the first of "exactly three parts, in order" the session outputs. Several
`FAMILY_PATTERNS` entries are ordinary English phrases — "executive summary",
"solution proposal" — that a real presales document is likely to use again later, as
an unrelated section heading or descriptive sentence, independent of whether the
mandatory opening declaration was ever written. An unbounded search cannot tell that
later, incidental occurrence apart from the required opening one.

**The direction of the bias.** Toward looking more conformant, never less. A session
that genuinely violated the rule — never declaring a family up front — could still be
scored `conformant` (or `rule-before-family`) if its drafted body happened to reuse the
same phrase anywhere downstream. The unbounded search never produces the opposite
error: it cannot turn a real declaration into a false `no-family`.

**The consequence for every figure above this section.** Both published arms —
`16/20` (80.0%) in "Arm 1 — post-03-07 skill" and `5/11` (45.5%) in "Arm 2 — paired
baseline, pre-03-07 skill" — were computed entirely from run blocks produced by this
unanchored scorer. Both rates are optimistic ceilings on the true conformance rate,
not precise measurements of it. The comparison between the two arms (45.5% → 60.0%
same-model, discussed below) is internally consistent — both sides share the same
unanchored bias — but neither individual number should be read as an exact rate.

**These figures cannot be re-scored.** `run_conformance.py`'s `--transcript-dir`
defaults to a fresh temporary directory, and no run in this file passed an explicit
`--transcript-dir` pointing into the repository — so every raw transcript that
produced every run block above was written outside the repository, to a temp
directory that no longer exists. There is no artifact left to re-run the fixed scorer
against. The figures stand as recorded, annotated as optimistic, and are not
recoverable.

**The fix.** Commit `7cde49a` (2026-09-16) bounds the family search to the transcript's
opening `FAMILY_LINE_WINDOW_CHARS` (400 characters) — the generous prefix window
where the write-mode contract actually places the family line — and computes both the
family offset and the marker offset against the same string, closing the same-defect
class this scorer had already been fixed for twice before (a nonzero-exit session
scored `no-family`; `_git_blob_sha()` reporting the wrong revision). Every run block
recorded above this section, including the two dated 2026-09-16 immediately below,
predates this fix. Any run recorded after commit `7cde49a` is anchored; anything
above it is not.

## Pre-committed disposition rule (03-12)

Committed 2026-09-16, before any session in this round has run. This section states the
rule that decides what this round's anchored measurement means, fixed in advance so the
disposition cannot be chosen after the number is known. Task 3 applies it mechanically to
`WINDOWS.md` entry 8, `REQUIREMENTS.md` `MOD-04`, and `03-UAT.md` gap G-03-2.

**Purpose.** `03-11` added a third, different-in-kind lever (an ordering gate the skill's
self-check runs against its own drafted response) after two instruction-wording-only levers
(`03-05`, `03-07`) each measured below the closure bar. Whether it worked is a fact to be
discovered, not a conclusion to be arranged.

**Arms.** Both arms are `claude-sonnet-5` only, five fixtures, two repeats each — ten
planned sessions per arm (20 planned total). Opus-5 is deliberately not run: `03-08`
measured it at 10/10 under the unanchored scorer, the entire measured residual lives in
sonnet-5, and a second ten-session arm doubles the quota exposure that interrupted `03-08`
twice. This is a disclosed scoping choice, not a silent omission, and it means neither arm
speaks to opus-5's behaviour under the anchored scorer.

- **Arm A** — the post-`03-11` skill, i.e. the repository working tree at HEAD.
  Measured `SKILL.md` blob SHA (derived now, before any session runs):
  `fadc48613f71fb29d55b42f70805225f9087a2b9`.
- **Arm B** — the pre-`03-11` skill, materialised from git into a directory outside the
  repository and passed as `--skill-src`. This is the paired baseline that makes any delta
  attributable to `03-11`'s lever rather than to the anchoring change, the fixtures, or the
  harness. Source commit: `c7c1df45e5042636565747f31d4eb5c38513dbac` (the last commit before
  `03-11` Task 1 touched `skills/proof-first/SKILL.md` — confirmed via
  `git log --oneline -- skills/proof-first/SKILL.md`, where `5ce0ebb` is `03-11`'s own Task 1
  commit and `c7c1df4` is the commit immediately before it, `03-07`'s). Expected `SKILL.md`
  blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a` (this is the same blob SHA
  `03-08-PLAN.md`'s Arm 1 — post-03-07 skill — recorded above, since `03-11` is the only
  plan between `03-07` and now that has touched `SKILL.md`).

Let `N_A` / `M_A` be Arm A's conformant count over its scoreable count, and `N_B` / `M_B`
Arm B's. `0.875` is the closure bar this project has used since `03-08`, carried forward
unchanged.

| Branch | Condition | `WINDOWS` entry 8 | `REQUIREMENTS` `MOD-04` | `03-UAT` G-03-2 |
|---|---|---|---|---|
| **1 — closed** | `M_A >= 8` and `N_A == M_A` | `fixed` | `[x]`, annotation states `N_A`/`M_A`, `N_B`/`M_B`, the model id, the five fixtures, both blob SHAs, and the reproduction command | `status: resolved`, evidence block gains the anchored measurement, prior figures retained |
| **2 — improved, not closed** | `M_A >= 8`, `N_A < M_A`, `N_A/M_A >= 0.875` | stays `open`; description replaced with both anchored arms, the date, and the statement that a rate below 1.0 does not satisfy a truth that says "in every session" | stays `[ ]`, annotation states `N_A`/`M_A` and `N_B`/`M_B` alongside the prior figures | stays `partially_resolved`, evidence block gains the anchored measurement |
| **3 — moved, under the bar** | `M_A >= 8`, `M_B >= 8`, `N_A/M_A < 0.875`, and `(N_A/M_A) - (N_B/M_B) >= 0.10` | stays `open`; description replaced with both arms and the measured delta, stating that a third lever produced real movement that still did not reach the bar | stays `[ ]`, annotation states both arms and the delta | stays `partially_resolved`, evidence block records all measurements in sequence |
| **4 — did not move** | `M_A >= 8`, `M_B >= 8`, `N_A/M_A < 0.875`, and `(N_A/M_A) - (N_B/M_B) < 0.10` | `waived` via `gsd-tools windows waive 8 "<reason>"`, the reason stating the anchored rate, that three levers have now each been measured (`03-05` restatement, `03-07` family line plus presence gate, `03-11` ordering re-scan) and none reached the bar, and that the residual is accepted and disclosed rather than hidden | stays `[ ]`, annotation states both arms and records the residual as accepted-and-disclosed, explicitly NOT as satisfied | stays `partially_resolved`, evidence block records all measurements plus the acceptance |
| **5 — under-sampled** | `M_A < 8` or `M_B < 8` after the attempt cap | stays `open`; description states the achieved `M_A` and `M_B`, why the cap was hit, and that no rate is claimed at this sample size | stays `[ ]`, annotation states the attempt and the shortfall with the achieved counts | stays `partially_resolved`, evidence block records the attempt and the shortfall |
| **6 — harness unavailable** | Task 2's `<precondition>` fails | stays `open`; description gains one line naming the blocker and the date | stays `[ ]`, annotation gains one line naming the blocker | unchanged apart from a blocker line |

**Branch 4 is an acceptance of a residual, not a satisfaction of the requirement.** `MOD-04`
stays `[ ]` in every branch except 1. Waiving `WINDOWS.md` entry 8 records that the project
has looked at the number, named it, and chosen to stop spending live-session budget on it —
a decision that stays reversible by re-opening the entry.

**Attempt cap:** 30 live invocations total across both arms (20 planned plus up to 10
retries). On reaching the cap, stop and take Branch 5 with whatever `M_A` and `M_B` were
achieved.

**The rule is not revisable after the number is known.** If the measured figures land in a
way this table did not anticipate, that fact is recorded and the nearest branch is applied
as written — the branch table itself is never rewritten, no branch is added, and no
threshold is reinterpreted after seeing the data.

In every branch, `AUD-01` and `ART-01` through `ART-04` stay `[ ]` and their annotations are
touched only to keep them accurate. This plan performs no human paraphrase read.

No session in this round has yet run.

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

## Run recorded 2026-09-15T06:48:35.153909+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=0 | verdict=unscoreable | reason=timeout
- 2026-09-15 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=1 | verdict=unscoreable | reason=timeout

conformant 0 of 0 scoreable sessions
unscoreable 2 sessions
  - excluded: model=claude-sonnet-5 fixture=A-rfp-answer repeat=0 reason=timeout
  - excluded: model=claude-sonnet-5 fixture=A-rfp-answer repeat=1 reason=timeout

## Run recorded 2026-09-15T06:56:50.064544+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=0 | verdict=conformant | evidence=family 'RFP and RFI response' at offset 147, marker_at=416

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T07:40:48.427443+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=0 | verdict=rule-before-family | evidence=marker 'PF-3.3' at offset 242 precedes family 'RFP answer' at offset 519

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T07:47:20.177337+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-sonnet-5 | fixture=B-proposal-section | repeat=0 | verdict=conformant | evidence=family 'proposal section' at offset 19, marker_at=823

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T07:51:00.039326+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-sonnet-5 | fixture=B-proposal-section | repeat=0 | verdict=rule-before-family | evidence=marker 'PF-3.3' at offset 252 precedes family 'Solution proposal' at offset 639

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T07:55:46.969991+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-sonnet-5 | fixture=C-exec-summary | repeat=0 | verdict=conformant | evidence=family 'Executive summary' at offset 150, marker_at=1065

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T08:03:42.283257+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-sonnet-5 | fixture=C-exec-summary | repeat=0 | verdict=rule-before-family | evidence=marker 'PF-3.3' at offset 303 precedes family 'Executive summary' at offset 613

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T08:09:03.301640+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-sonnet-5 | fixture=D-demo-discovery | repeat=0 | verdict=conformant | evidence=family 'Demo or discovery material' at offset 181, marker_at=778

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T08:14:24.776424+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-sonnet-5 | fixture=D-demo-discovery | repeat=0 | verdict=conformant | evidence=family 'demo and discovery material' at offset 396, marker_at=689

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T08:21:29.775651+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-sonnet-5 | fixture=E-ambiguous | repeat=0 | verdict=rule-before-family | evidence=marker 'PF-3.3' at offset 306 precedes family 'No family fits' at offset 651

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T08:27:17.899623+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-sonnet-5 | fixture=E-ambiguous | repeat=0 | verdict=conformant | evidence=family 'No family fits' at offset 21, marker_at=1716

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T08:33:08.986933+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-opus-5 | fixture=A-rfp-answer | repeat=0 | verdict=conformant | evidence=family 'RFP answer' at offset 139, marker_at=408

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T08:36:53.202490+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-opus-5 | fixture=A-rfp-answer | repeat=0 | verdict=conformant | evidence=family 'RFP answer' at offset 22, marker_at=424

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T08:40:33.621118+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-opus-5 | fixture=B-proposal-section | repeat=0 | verdict=conformant | evidence=family 'Solution proposal' at offset 19, marker_at=491

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T08:44:27.370316+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-opus-5 | fixture=B-proposal-section | repeat=0 | verdict=conformant | evidence=family 'Solution proposal' at offset 19, marker_at=555

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T08:48:02.782509+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-opus-5 | fixture=C-exec-summary | repeat=0 | verdict=conformant | evidence=family 'Executive summary' at offset 19, marker_at=284

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T08:51:08.284268+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-opus-5 | fixture=C-exec-summary | repeat=0 | verdict=conformant | evidence=family 'executive summary' at offset 202, marker_at=368

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T08:56:09.984530+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-opus-5 | fixture=D-demo-discovery | repeat=0 | verdict=conformant | evidence=family 'demo and discovery material' at offset 19, marker_at=451

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T09:00:47.552431+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-opus-5 | fixture=D-demo-discovery | repeat=0 | verdict=conformant | evidence=family 'demo and discovery material' at offset 19, marker_at=563

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T09:04:53.757591+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-opus-5 | fixture=E-ambiguous | repeat=0 | verdict=conformant | evidence=family 'No family fits' at offset 2, marker_at=867

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T09:07:44.370883+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-15 | model=claude-opus-5 | fixture=E-ambiguous | repeat=0 | verdict=conformant | evidence=family 'No family fits' at offset 2, marker_at=591

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T09:13:03.455562+00:00Z -- CORRECTION: blob SHA below is wrong, see note
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`

**Correction:** this was the first attempt at the Branch-3 paired baseline, run with
`--skill-src` pointed at a materialised pre-03-07 `skills/proof-first` copy
(git-archived from commit `6f62385`, the last commit before `03-07` Task 1). The
SHA printed above is wrong -- `_git_blob_sha()` at the time this ran always computed
`git rev-parse HEAD:skills/proof-first/SKILL.md` regardless of `--skill-src`, so it
reported the repo's current (post-03-07) blob SHA even though the session actually
exercised the pre-03-07 skill. Fixed in the same commit as this annotation:
`_git_blob_sha()` now hashes the actual `SKILL.md` under `--skill-src` via
`git hash-object`, content-addressed and independent of HEAD. The correct SHA for
the skill this session actually used is `1fc1e1092941157191268a8294ab4e1edc65cdac`
(verified: `git hash-object` on the materialised copy equals
`git rev-parse 6f62385:skills/proof-first/SKILL.md`; also matches 03-06's own
instrument-proving run above, which measured the same pre-03-07 skill state).
The session itself timed out (unscoreable), so no scored verdict is affected by
this correction -- only the recorded metadata.

- 2026-09-15 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=0 | verdict=unscoreable | reason=timeout

conformant 0 of 0 scoreable sessions
unscoreable 1 sessions
  - excluded: model=claude-sonnet-5 fixture=A-rfp-answer repeat=0 reason=timeout

## Run recorded 2026-09-15T09:23:31.517609+00:00Z
Measured SKILL.md blob SHA: `1fc1e1092941157191268a8294ab4e1edc65cdac`
- 2026-09-15 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=0 | verdict=rule-before-family | evidence=marker 'PF-3.3' at offset 191 precedes family 'RFP and RFI response' at offset 565

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T09:29:13.681376+00:00Z
Measured SKILL.md blob SHA: `1fc1e1092941157191268a8294ab4e1edc65cdac`
- 2026-09-15 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=0 | verdict=rule-before-family | evidence=marker 'PF-3.3' at offset 835 precedes family 'RFP answer' at offset 1190

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T09:34:28.901660+00:00Z
Measured SKILL.md blob SHA: `1fc1e1092941157191268a8294ab4e1edc65cdac`
- 2026-09-15 | model=claude-sonnet-5 | fixture=B-proposal-section | repeat=0 | verdict=rule-before-family | evidence=marker 'PF-3.3' at offset 325 precedes family 'Solution proposal' at offset 700

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T09:39:37.650966+00:00Z
Measured SKILL.md blob SHA: `1fc1e1092941157191268a8294ab4e1edc65cdac`
- 2026-09-15 | model=claude-sonnet-5 | fixture=B-proposal-section | repeat=0 | verdict=rule-before-family | evidence=marker 'PF-3.3' at offset 293 precedes family 'proposal section' at offset 412

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T09:43:12.859666+00:00Z
Measured SKILL.md blob SHA: `1fc1e1092941157191268a8294ab4e1edc65cdac`
- 2026-09-15 | model=claude-sonnet-5 | fixture=C-exec-summary | repeat=0 | verdict=conformant | evidence=family 'executive summary' at offset 465, marker_at=840

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T09:46:26.690851+00:00Z
Measured SKILL.md blob SHA: `1fc1e1092941157191268a8294ab4e1edc65cdac`
- 2026-09-15 | model=claude-sonnet-5 | fixture=C-exec-summary | repeat=0 | verdict=rule-before-family | evidence=marker 'PF-3.3' at offset 189 precedes family 'executive summary' at offset 398

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T09:49:25.740184+00:00Z
Measured SKILL.md blob SHA: `1fc1e1092941157191268a8294ab4e1edc65cdac`
- 2026-09-15 | model=claude-sonnet-5 | fixture=D-demo-discovery | repeat=0 | verdict=conformant | evidence=family 'demo or discovery material' at offset 471, marker_at=723

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T09:53:18.150768+00:00Z
Measured SKILL.md blob SHA: `1fc1e1092941157191268a8294ab4e1edc65cdac`
- 2026-09-15 | model=claude-sonnet-5 | fixture=D-demo-discovery | repeat=0 | verdict=conformant | evidence=family 'Demo and discovery material' at offset 762, marker_at=1025

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-15T09:59:01.374030+00:00Z
Measured SKILL.md blob SHA: `1fc1e1092941157191268a8294ab4e1edc65cdac`
- 2026-09-15 | model=claude-sonnet-5 | fixture=E-ambiguous | repeat=0 | verdict=unscoreable | reason=nonzero exit 1 (empty stderr)

conformant 0 of 0 scoreable sessions
unscoreable 1 sessions
  - excluded: model=claude-sonnet-5 fixture=E-ambiguous repeat=0 reason=nonzero exit 1 (empty stderr)

## Run recorded 2026-09-16T04:16:05.262362+00:00Z
Measured SKILL.md blob SHA: `1fc1e1092941157191268a8294ab4e1edc65cdac`
- 2026-09-16 | model=claude-sonnet-5 | fixture=E-ambiguous | repeat=0 | verdict=conformant | evidence=family 'Solution proposal' at offset 196, marker_at=1666

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T04:22:16.993293+00:00Z
Measured SKILL.md blob SHA: `1fc1e1092941157191268a8294ab4e1edc65cdac`
- 2026-09-16 | model=claude-sonnet-5 | fixture=E-ambiguous | repeat=0 | verdict=conformant | evidence=family 'Solution proposal' at offset 553, marker_at=952

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Combined result (03-08-PLAN.md, computed by hand from the run blocks above)

This measurement was driven as many small single-session invocations rather than one large
matrix invocation, because two earlier attempts at a single large invocation each lost their
entire result when the invoking process was interrupted mid-run (a Claude Code session-usage
limit, then a Claude Code session teardown) -- `run_conformance.py` only appends its run block
when a whole invocation finishes, so one long invocation risks losing everything it ran. Each
block above is genuine, durable (committed the moment it landed), and traceable to its own
timestamp. This section aggregates them by hand; the arithmetic below is checkable against the
run blocks above by anyone, without re-running anything.

### Arm 1 -- post-03-07 skill (both models, the plan's required measurement)

Blob SHA `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a` (commit `4715d43`, the last commit before
this plan's own two instrument-fix commits). Aggregated from every non-invalidated run block
above whose blob SHA is `9612649e...`, EXCLUDING the block timestamped
`2026-09-15T09:13:03.455562+00:00Z` -- that block's SHA field was itself the manifestation of
the blob-SHA bug fixed in this plan (it actually exercised the pre-03-07 skill via
`--skill-src` and belongs to Arm 2 below; see the CORRECTION note on that block).

- claude-sonnet-5: 12 attempted (5 fixtures x 2 repeats = 10 planned, plus 2 extra
  `A-rfp-answer` retries after the first repeats=2 invocation timed out on both repeats), 2
  unscoreable (both `A-rfp-answer`, both `reason=timeout`, from that first invocation), 10
  scoreable: 6 conformant, 4 rule-before-family, 0 no-family.
- claude-opus-5: 5 fixtures x 2 repeats attempted = 10 attempted, 0 unscoreable, 10 scoreable:
  10 conformant, 0 rule-before-family, 0 no-family.

**conformant 16 of 20 scoreable sessions** (both models, 2 excluded as unscoreable: timeout x2)
Rate: 16/20 = 80.0%.

### Arm 2 -- paired baseline, pre-03-07 skill (claude-sonnet-5 only)

Blob SHA `1fc1e1092941157191268a8294ab4e1edc65cdac` (commit `6f62385`, the last commit before
`03-07` Task 1 -- materialised via `git archive 6f62385 skills/proof-first` into a directory
outside the repository, passed as `--skill-src`). Same fixtures, same prompt template, same
fixed instrument as Arm 1. Includes `03-06-PLAN.md`'s own instrument-proving run
(`2026-09-15T02:47:51.963922Z`) as one extra genuine `A-rfp-answer` sample -- it measured the
same skill state via the same recipe, before the returncode bug existed, and scored a normal
verdict (not the bug's failure signature), so excluding it would discard real data for no
reason.

- claude-sonnet-5 only: 13 attempted (1 extra `A-rfp-answer` sample from 03-06, plus 2 planned
  repeats each of 5 fixtures = 10, plus one retried session after the corrected-SHA timeout and
  one retried after a transient network failure -- 13 total distinct invocations), 2
  unscoreable (`A-rfp-answer repeat=0` timeout at `09:13:03`, `E-ambiguous repeat=0` nonzero
  exit at `09:59:01`, both retried successfully), 11 scoreable: 5 conformant, 6
  rule-before-family, 0 no-family.
- claude-opus-5: NOT RUN. Per coordinator direction, given real quota/interruption risk already
  encountered twice in this plan, a sonnet-5-only paired baseline was accepted as a defensible
  same-instrument comparison rather than attempting a second 10-session opus arm. This means
  Arm 1 (n=20, both models) and Arm 2 (n=11, one model) have unequal sample sizes, and Arm 2
  cannot speak to whether claude-opus-5's pre-03-07 behaviour differed from claude-sonnet-5's --
  only Arm 1 covers opus-5, and only against the post-fix skill.

**conformant 5 of 11 scoreable sessions** (claude-sonnet-5 only, 2 excluded as unscoreable:
1 timeout, 1 transient network failure)
Rate: 5/11 = 45.5%.

### What this comparison shows and does not show

Restricting Arm 1 to sonnet-5 only, for a like-for-like same-model comparison against Arm 2
(which is sonnet-5 only): 6 conformant of 10 scoreable = 60.0%. Paired against Arm 2's 5 of 11
= 45.5%, that is a same-instrument, same-model, same-fixture-set improvement of roughly 14.5
percentage points (45.5% -> 60.0%) attributable to 03-07's two levers. It is a real,
measured, non-trivial improvement -- and it still falls short of the 87.5% bar the
pre-committed decision rule uses as its closure threshold.

Comparing the FULL Arm 1 (both models, 16/20 = 80.0%) against the sonnet-only Arm 2 (5/11 =
45.5%) instead mixes a model-count difference into the comparison and must not be read as "the
fix improved things from 45.5% to 80.0%" -- that apparent 34.5-point jump is inflated by
opus-5's 10/10 perfect score, which has no pre-03-07 opus-5 baseline to compare against (opus-5
was never measured pre-03-07 in this plan; see the NOT RUN note under Arm 2 above). The
defensible same-instrument finding is the sonnet-only one: 45.5% -> 60.0%, not 45.5% -> 80.0%.

### Caveats (permanent part of this file, not trimmed once numbers looked favourable)

- Both models are Anthropic-hosted (`claude-sonnet-5`, `claude-opus-5`); this says nothing
  about a non-Anthropic harness.
- `claude -p` exposes no temperature or seed flag; this run is not deterministic and a repeat
  can differ, as several of the paired same-fixture repeats above already show (both
  conformant and non-conformant verdicts on the identical fixture and model).
- The user-level configuration under the home directory still loads, because `--bare` is
  deliberately off, matching the condition the prior 5/6 and 14/16 measurements ran under.
- This fixture set, prompt template, and scoring recipe (`evals/conformance/run_conformance.py`,
  built in `03-06-PLAN.md`) are DIFFERENT from `03-05-PLAN.md`'s UAT recipe that produced the
  5/6 and 14/16 figures cited elsewhere in this project (`WINDOWS.md` entry 8,
  `REQUIREMENTS.md` MOD-04, `03-UAT.md` gap G-03-2). The 16/20 and 5/11 figures here are NOT
  directly comparable to 5/6 or 14/16 -- different fixtures, different prompt, different
  scoring implementation. They are compared only to the pre-committed rule's 0.875 threshold
  (itself carried over from the 14/16 figure) and to each other (same-instrument paired
  design), never conflated with the older numbers as if measuring the same thing.
- Two real instrument defects were found and fixed while producing this data (both documented
  above and in `run_conformance.py`'s own commit history): a nonzero-exit `claude -p` session
  being scored as `no-family` instead of `unscoreable`, and `_git_blob_sha()` reporting the
  wrong SKILL.md revision for any `--skill-src` other than the repo's own HEAD. Both are fixed
  and self-test-covered before any of the data in this Combined Result section was collected
  under the fixed code.
- The exclusion rate itself is a caveat: Arm 1 excluded 2 of 22 attempted sessions (9.1%),
  Arm 2 excluded 2 of 13 attempted (15.4%). Every exclusion is a timeout or a transient network
  failure, none is a `claude -p` session that ran to completion and produced ambiguous output --
  see each run block's `reason=` field above for the individual cause.
- A third instrument defect was found and fixed after this data was collected (03-09-PLAN.md,
  CR-01): the family search had no bound and could mistake an incidental later phrase in
  drafted prose for the required opening declaration, biasing every figure above toward
  looking more conformant than it was. See "## Scorer anchoring correction (CR-01)" at the top
  of this file. Both figures in this section are optimistic ceilings and cannot be re-scored --
  their raw transcripts were never written into the repository and no longer exist.

## Run recorded 2026-09-16T06:23:26.865109+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=0 | verdict=unscoreable | reason=timeout

conformant 0 of 0 scoreable sessions
unscoreable 1 sessions
  - excluded: model=claude-sonnet-5 fixture=A-rfp-answer repeat=0 reason=timeout

## Run recorded 2026-09-16T06:31:45.559491+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=73, marker='PF-3.3')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T06:37:20.821712+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=636, marker='PF-1.2')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T06:42:11.983431+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=B-proposal-section | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=1013, marker='PF-2.13')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T06:48:34.377750+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=B-proposal-section | repeat=0 | verdict=unscoreable | reason=timeout

conformant 0 of 0 scoreable sessions
unscoreable 1 sessions
  - excluded: model=claude-sonnet-5 fixture=B-proposal-section repeat=0 reason=timeout

## Run recorded 2026-09-16T06:56:50.135039+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=B-proposal-section | repeat=0 | verdict=conformant | evidence=family 'Solution proposal' at offset 2 (window=400), marker_at=1604

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T07:02:46.131767+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=C-exec-summary | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=546, marker='PF-3.3')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T07:07:53.175382+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=C-exec-summary | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=460, marker='PF-3.3')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T07:14:12.088281+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=D-demo-discovery | repeat=0 | verdict=conformant | evidence=family 'Demo and discovery material' at offset 0 (window=400), marker_at=1059

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T07:21:00.546743+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=D-demo-discovery | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=1155, marker='PF-3.3')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T07:27:19.044526+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=E-ambiguous | repeat=0 | verdict=conformant | evidence=family 'No family fits' at offset 2 (window=400), marker_at=1010

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T07:33:46.055691+00:00Z
Measured SKILL.md blob SHA: `fadc48613f71fb29d55b42f70805225f9087a2b9`
- 2026-09-16 | model=claude-sonnet-5 | fixture=E-ambiguous | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=1176, marker='PF-3.3')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T07:40:29.839977+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=209, marker='PF-3.3')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T07:45:44.241555+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=0 | verdict=unscoreable | reason=timeout

conformant 0 of 0 scoreable sessions
unscoreable 1 sessions
  - excluded: model=claude-sonnet-5 fixture=A-rfp-answer repeat=0 reason=timeout

## Run recorded 2026-09-16T07:53:55.751856+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=A-rfp-answer | repeat=0 | verdict=conformant | evidence=family 'RFP answer' at offset 22 (window=400), marker_at=512

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T07:58:45.274766+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=B-proposal-section | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=493, marker='PF-3.3')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T08:03:22.501771+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=B-proposal-section | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=425, marker='PF-1.2')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T08:08:55.790418+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=C-exec-summary | repeat=0 | verdict=conformant | evidence=family 'executive summary' at offset 70 (window=400), marker_at=342

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T08:13:31.662960+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=C-exec-summary | repeat=0 | verdict=conformant | evidence=family 'executive summary' at offset 73 (window=400), marker_at=234

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T08:17:21.490987+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=D-demo-discovery | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=874, marker='PF-3.3')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T08:22:45.863745+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=D-demo-discovery | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=898, marker='PF-3.3')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T08:28:18.574834+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=E-ambiguous | repeat=0 | verdict=conformant | evidence=family 'No family fits' at offset 2 (window=400), marker_at=1215

conformant 1 of 1 scoreable sessions
unscoreable 0 sessions

## Run recorded 2026-09-16T08:33:31.569939+00:00Z
Measured SKILL.md blob SHA: `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a`
- 2026-09-16 | model=claude-sonnet-5 | fixture=E-ambiguous | repeat=0 | verdict=no-family | evidence=no family match found within the first 400 chars (marker_at=282, marker='PF-3.3')

conformant 0 of 1 scoreable sessions
unscoreable 0 sessions

## Anchored remeasurement result (03-12)

Computed by hand from the 23 run blocks appended above between the pre-committed-rule commit
`0f47e8b` and this section's own commit — re-derivable by anyone via
`git diff 0f47e8b..<this-commit> -- evals/conformance/RESULTS-mod04.md` without re-running
anything. This is the first MOD-04 measurement produced entirely under `03-09`'s anchored
scorer (`FAMILY_LINE_WINDOW_CHARS=400`, both offsets computed against the same stripped
string) — every figure below is a precise measurement, not an optimistic ceiling, unlike
every number recorded above the CR-01 banner at the top of this file.

Reproduction command (Arm A):
`python3 evals/conformance/run_conformance.py --fixtures <fixture> --models claude-sonnet-5 --repeats 1 --timeout 480 --transcript-dir <dir>`
Reproduction command (Arm B): the same command plus
`--skill-src <materialised-pre-03-11-skill-dir>`, where that directory is produced by
`git archive c7c1df45e5042636565747f31d4eb5c38513dbac skills/proof-first | tar -x -C <dir>`.

### Arm A -- post-03-11 skill (the repository working tree at HEAD when this round ran)

Blob SHA `fadc48613f71fb29d55b42f70805225f9087a2b9`, model `claude-sonnet-5`, five fixtures
(A-rfp-answer, B-proposal-section, C-exec-summary, D-demo-discovery, E-ambiguous), two
repeats planned per fixture = 10 planned sessions.

12 attempted (10 planned + 2 retries after timeout exclusions), 2 unscoreable (both
`reason=timeout`: `A-rfp-answer` first attempt, `B-proposal-section` first attempt; both
retried successfully and the retries are counted below), 10 scoreable:
- conformant: 3 (`B-proposal-section` retry, `D-demo-discovery` first attempt,
  `E-ambiguous` first attempt)
- no-family: 7 (`A-rfp-answer` x2, `B-proposal-section` first attempt, `C-exec-summary` x2,
  `D-demo-discovery` second attempt, `E-ambiguous` second attempt)
- rule-before-family: 0

**N_A = 3, M_A = 10. N_A/M_A = 30.0%.**

### Arm B -- pre-03-11 skill (materialised from commit `c7c1df45e5042636565747f31d4eb5c38513dbac`, the last commit before `03-11` Task 1)

Blob SHA `9612649e49a331a65c1d8ea9cbdc5f5ea79eb92a` (the same blob `03-08-PLAN.md`'s Arm 1
already recorded as the post-03-07 skill — `03-11` is the only plan that touched
`skills/proof-first/SKILL.md` between then and this round). Same model, fixtures, and
recipe as Arm A.

11 attempted (10 planned + 1 retry after a timeout exclusion), 1 unscoreable
(`reason=timeout`, `A-rfp-answer` first attempt, retried successfully), 10 scoreable:
- conformant: 4 (`A-rfp-answer` retry, `C-exec-summary` x2, `E-ambiguous` first attempt)
- no-family: 6 (`A-rfp-answer` first attempt, `B-proposal-section` x2, `D-demo-discovery`
  x2, `E-ambiguous` second attempt)
- rule-before-family: 0

**N_B = 4, M_B = 10. N_B/M_B = 40.0%.**

### Branch selection

`M_A = 10 >= 8` and `M_B = 10 >= 8`, so neither arm is under-sampled (Branch 5 does not
fire) and the precondition passed (Branch 6 does not fire).

- Branch 1 (`M_A >= 8` and `N_A == M_A`): `3 != 10`. Does not fire.
- Branch 2 (`N_A/M_A >= 0.875`): `0.30 < 0.875`. Does not fire.
- Branch 3 (`N_A/M_A < 0.875` and `(N_A/M_A) - (N_B/M_B) >= 0.10`): `0.30 < 0.875` holds, but
  `(0.30 - 0.40) = -0.10`, which is **not** `>= 0.10`. Does not fire.
- Branch 4 (`N_A/M_A < 0.875` and `(N_A/M_A) - (N_B/M_B) < 0.10`): `0.30 < 0.875` holds, and
  `-0.10 < 0.10` holds. **Fires.**

**Branch 4 selected the disposition, by the condition `(N_A/M_A) - (N_B/M_B) < 0.10` with the
computed delta of -0.10.**

### The finding this round's evidence actually shows

Branch 4's table label is "did not move." The measured delta is not zero movement — it is a
10.0-percentage-point *decline*: Arm A (post-`03-11`, with the ordering-gate lever) scored
30.0% (3/10), ten points below Arm B (pre-`03-11`, the paired same-instrument baseline) at
40.0% (4/10). Per `03-08-PLAN.md`'s precedent (honour the branch's mechanical selection,
write the true finding where the evidence contradicts the template phrase), this section
states that plainly: this round's own paired evidence does not show the ordering lever
improving conformance under the anchored scorer, and the point estimate moved in the
opposite direction from what `03-11` intended. At `n=10` per arm, a single-session swing is
roughly a 10-point shift, so this delta is well within what sampling noise alone could
produce — it is not read as proof the lever made things worse, only as proof it did not
demonstrably make things better, which is exactly what Branch 4 (not Branch 2 or 3) is for.

Zero sessions in either arm scored `rule-before-family` — every non-conformant session this
round scored `no-family` (no family phrase found anywhere in the first 400 characters at
all, not merely after a rule marker). This is a different residual shape from the
unanchored-scorer measurements above the CR-01 banner, where `rule-before-family` was the
dominant non-conformant verdict and genuine `no-family` was rare or absent. The anchored
window is doing exactly the job `03-09` built it to do: several of these `no-family`
verdicts have a `marker_at` deep in the transcript (up to offset 1176), meaning the model
did cite a rule and, in at least some of these transcripts, may have named a family
somewhere past the 400-char window — the unbounded pre-CR-01 scorer would very likely have
scored several of these `conformant` or `rule-before-family` instead. That upstream/downstream
shift in verdict composition is itself evidence of the bias CR-01 fixed, not a separate
finding needing its own disposition.

### Caveats (carried forward, plus this round's own)

- Both arms are `claude-sonnet-5` only; opus-5 was deliberately not run this round (see the
  arm definitions in `## Pre-committed disposition rule (03-12)` above) — this section says
  nothing about opus-5's behaviour under the anchored scorer.
- `claude -p` exposes no temperature or seed flag; a repeat can differ, and at `n=10` per arm
  the 10-point delta between arms is within plausible sampling noise for a true rate
  difference of zero.
- These figures are NOT directly comparable to 5/6 or 14/16 (`03-05`'s UAT recipe) or to
  16/20 and 5/11 (this same instrument, `03-08`'s measurement, BEFORE the CR-01 anchoring
  fix). All four earlier figures are optimistic ceilings from an unbounded family search;
  this round's 30.0%/40.0% are the first MOD-04 figures produced end-to-end under the
  anchored scorer and are markedly lower, consistent with CR-01's documented bias direction
  (toward looking MORE conformant, never less).
- Every exclusion in both arms was a `claude -p` timeout (`reason=timeout`); no exclusion
  this round was a nonzero exit or a network failure. Arm A's exclusion rate was 2 of 12
  attempted (16.7%); Arm B's was 1 of 11 attempted (9.1%).
- `run_conformance.py` was not modified during this measurement (verified: byte-identical to
  its state at the end of `03-09`, commit `7cde49a`, via `git diff 5ce0ebb..HEAD -- evals/conformance/run_conformance.py` producing no output).

## Instrument durability fix (03-13)

**The defect.** `main()`'s live-mode loop held every session's result in memory (an
in-memory `lines` list) and wrote the entire batch to this file only after the whole
`model x fixture x repeat` matrix finished. An interruption of the Python process between
sessions — the process killed, an uncaught exception outside the four per-session handlers,
or external teardown — silently discarded every session already scored in that same
invocation, because none of them had reached disk yet. This is the identical failure mode
the `## Combined result (03-08-PLAN.md ...)` section above already records destroying two
entire earlier measurement attempts ("a Claude Code session-usage limit, then a Claude Code
session teardown"), answered at the time by an operational workaround — driving the matrix
as many small single-session invocations rather than one large one — rather than by a fix
in the instrument itself.

**The fix.** Commit `c99a848` (2026-09-16) extracts the matrix loop into `run_matrix()`,
which writes and flushes each session's result line to the open results-file handle,
through a new `_write_result_line()` helper, at the moment that session is scored. No
result text is accumulated in memory anywhere in `main()` or `run_matrix()` any more. A new
offline self-test behavior case (case 11) proves this: it interrupts a matrix mid-run with
`KeyboardInterrupt` — an exception type outside every handler `run_matrix()` catches — and
asserts the sessions scored before the interruption are already durable on disk. The one
residual this fix does not close, and does not claim to: two `run_conformance.py`
invocations appending to this file at the same time are not guaranteed to produce
non-interleaved output. The tool makes no parallel-safety claim, and the project's
operating pattern is one foreground invocation at a time; the module docstring now states
this explicitly rather than leaving it undisclosed.

**What does not change.** Every figure recorded in this file — including the anchored
`N_A = 3, M_A = 10` (30.0%) and `N_B = 4, M_B = 10` (40.0%) figures above — was produced
under the one-invocation-per-session operating workaround, before this fix landed, and none
of them moves. This fix removes a future exposure to the failure mode that has already
struck this project twice; it does not correct, re-derive, or re-score any past number.

**The corrected enumeration.** The Arm A `no-family` breakdown above previously named six
sessions (`A-rfp-answer` x2, `C-exec-summary` x2, `D-demo-discovery` second attempt,
`E-ambiguous` second attempt) beside its own stated count of seven. The omitted session was
the `B-proposal-section` first attempt at `2026-09-16T06:42:11.983431+00:00Z`
(`verdict=no-family | evidence=no family match found within the first 400 chars
(marker_at=1013, marker='PF-2.13')`), now added to the enumeration above. The aggregate Arm
A figures (`N_A = 3, M_A = 10`, 30.0%) were correct throughout this omission and are
unaffected by this correction.
