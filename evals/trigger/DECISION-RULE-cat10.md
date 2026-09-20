# CAT-10 Decision Rule — committed before any session of this round runs

Committed 2026-09-20, before any session of this round has run. This file fixes the arms, the
exact intervention text, the sample floors, the attempt cap, and the branch table that decides
what the measurement means — all before a single live session opens. No number in this file is
computed from a session; none has run yet. The final line of this file, until Task 6 replaces it
with the branch selection, is the literal sentinel `RESULTS-mod04.md` uses for the same purpose:
this round has not started measuring anything.

## 1. Purpose

Requirement CAT-10 states that the SKILL.md frontmatter `description` triggers the skill reliably
on presales writing requests, acting as an explicit trigger list. Measured live on 2026-09-20, one
session per phrasing: 9 of 9 must-fire phrasings fired (correct) and 2 of 5 must-not-fire
phrasings also fired (`Build me a slide deck for the kickoff meeting.` and `Work out pricing and
sizing for a 500-seat deployment.`). Both over-firing phrasings name an exclusion already stated in
`SKILL.md`'s own `## Limits` section and in `PROJECT.md`'s Out of Scope list — text the activation
surface does not read.

The candidate fix is an exclusion clause appended to the description. Whether that clause actually
suppresses activation on the two over-firing phrasings — as opposed to doing nothing, or making
things worse — is a fact this round discovers by measurement. It is not a conclusion arranged in
advance. This file exists so the disposition is decided by a rule fixed before the numbers exist,
not by preference after seeing them.

## 2. The locked decision this round reopens

Decision D-30 (`02-CONTEXT.md:84`) fixes the `description`'s shape as a front-loaded trigger list of
roughly 400-600 characters. Decision D-29 forbids framework marks in it. Both are flagged
costly/one-way, and `03-RESEARCH.md:70` states plainly that the description's shape should not be
reopened without a fresh discuss-phase pass, because a published description propagates into
registry indexes and forks that do not re-fetch.

This round reopens D-30 and D-29's territory anyway, because the field is now measurably wrong on
its own stated purpose (CAT-10 itself), and the edit is additive rather than a rewrite:

- D-30's band is preserved. The candidate description's collapsed length is 551 characters, inside
  the 400-600 band and above `tools/check_repo.py`'s 200-character floor.
- D-29's no-framework-marks rule is preserved. The candidate text adds no Command of the Message,
  MEDDICC, or Challenger vocabulary.
- The entire inclusion half — the part that measured 9 of 9 on the must-fire rows — is untouched.
  This round appends one exclusion sentence; it does not reword, reorder, or shorten anything that
  already fires correctly.

## 3. The untested assumption (H4)

The proposed fix assumes a harness deciding activation applies a negative clause as a suppressor —
that "Not for slide decks" removes those tokens from what pulls activation toward the skill, rather
than simply adding the excluded nouns to the surface the ranker matches against. **Nothing in this
repository tests that assumption.** Call it H4.

Under the competing hypothesis H1 — that the activation decision is made on semantic similarity
between the request and the description rather than literal keyword overlap — appending exclusion
nouns to the description could plausibly *raise* similarity to the excluded prompts instead of
lowering it, because the words "slide deck" and "pricing" and "sizing" would now appear in the
description text for the first time, negated or not.

Lexical keyword pull is already refuted as the mechanism for the original over-fires: the two
phrasings that fired (`Build me a slide deck for the kickoff meeting.` and `Work out pricing and
sizing for a 500-seat deployment.`) share zero content words with the 439-character description,
while two phrasings that shared the word "write" did not fire. So the positive pull that produced
the original over-fires is unidentified, and whether a negative clause can counteract an
unidentified pull is itself unknown.

A null result (the treatment arm's over-fire count does not improve on the control) or an inverted
result (it gets worse) is a pre-named, legitimate outcome of this round — not a sign the round was
run badly.

## 4. The arms

Both arms run the identical instrument (`evals/trigger/run_trigger_test.py` as extended by this
round's Task 2), with `--model claude-sonnet-5`, `--repeats 5`, `--jobs 3`, `--timeout 600`, all 14
pressure-test phrasings, 70 planned sessions each (140 planned total).

- **Arm B (control)** — the unchanged 439-character description as it ships today. Blob SHA
  `fadc48613f71fb29d55b42f70805225f9087a2b9`, head-14 sha256
  `d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675`. Run FIRST, while the live tree
  still carries this description, because the live tree is the only place the old description
  exists as a running instrument.
- **Arm A (treatment)** — the 551-character description with the exclusion clause appended, applied
  to the live tree by Task 4. Its nine exact lines, reproduced verbatim (lines 4-12 of
  `skills/proof-first/SKILL.md` after Task 4 lands; the first six are byte-identical to today's, the
  seventh gains a sentence, the last two are new):

```
  Write or check RFP and RFI responses, solution proposals, executive
  summaries, and demo or discovery documents for technical presales and
  bid teams. Use for a scored technical response, a customer-facing
  proposal, or a check pass over a finished draft that flags invented
  metrics, missing evidence, undisclosed customer references, competitor
  comparisons, compliance claims, and unquantified buzzwords before the
  document ships to a buyer. Not for slide decks or visual design,
  pricing, sizing, or commercial modelling, or marketing and brand
  writing.
```

  Expected head-14 sha256 (measured on a scratchpad copy during planning, a cross-check only):
  `9049c7d82fadce008b00cdf70c7dc74add0d23691c7c61b8d586740a3beb3e1e`. **The authority is the live
  recomputation in Task 4**, not this expected value — if they differ, Task 4 records the deviation
  and uses the live value, following the `03-04`/`04-01`/`04-03`/`04-04` precedent of never reshaping
  shipped content to force a plan-authored figure to reproduce.

## 5. One intervention

Removing the audience clause `for technical presales and bid teams` is H1's strongest candidate
explanation for the original over-fires and is deliberately **not** bundled into this round. A
bundled null result would be uninterpretable (which change, if either, produced it?) and a bundled
positive result could not be attributed to either change alone. This round measures exactly one
lever: appending the exclusion sentence above. Nothing else in the description's inclusion half
changes.

## 6. Statistical power

Clopper-Pearson upper bound on the true fire rate for a phrasing that records zero fires in n
sessions, alpha 0.05 (computed during planning with a stdlib `math.comb` script; these are Task 2's
self-test fixtures):

| zero fires in n sessions | Clopper-Pearson upper bound |
|---|---|
| n=1 | 0.9500 |
| n=3 | 0.6316 |
| **n=5** | **0.4507** |
| n=10 | 0.2589 |
| n=20 | 0.1391 |
| n=59 | 0.0495 |

**Chosen: n=5 per phrasing, paired, 140 planned live sessions (70 per arm).** A clean must-not-fire
row at n=5 bounds that phrasing's true fire rate at 0.4507, not at zero — that is the strongest
per-row statement this round can make, and it is the statement that must appear in the results,
never "the description no longer over-fires."

Why not n=3 (84 paired sessions, the `evals/benchmark/` in-repo precedent)? A bound of 0.6316 is
barely narrower than the n=1 bound of 0.9500 that produced the current unsatisfying state — not
enough gain to justify calling it a measurement. Why not n=10 (280 sessions)? The marginal bound
gain (0.4507 to 0.2589) does not justify doubling a quota exposure that interrupted the `03-08` run
twice.

Fisher exact two-tailed on the pooled must-not-fire 2x2 (computed during planning), showing why both
arms must run and not just the treatment:

| control fires / sessions | treatment | p |
|---|---|---|
| 2 of 25 | 0 of 25 | 0.4898 |
| 3 of 25 | 0 of 25 | 0.2347 |
| 4 of 25 | 0 of 25 | 0.1099 |
| 5 of 25 | 0 of 25 | 0.0502 |
| 10 of 25 | 0 of 25 | 0.0006 |

**Consequence, stated in advance:** even a perfect treatment sweep (zero fires on every
must-not-fire row) is not attributable to the intervention unless the control arm reproduces the
defect at 6 or more of its 25 must-not-fire sessions. Below that, the round can still report Arm A's
own measurement, but cannot claim the improvement is distinguishable from the control.

## 7. The branch table

**Counters.** For arm X and pressure-test row r: `S_X(r)` is r's scoreable session count in arm X
(unscoreable sessions excluded from numerator and denominator alike) and `F_X(r)` is the count of
those in which the skill fired. `MNF` is the 5 must-not-fire rows, `MF` the 9 must-fire rows.

- `OF_X` = sum of `F_X(r)` over MNF — over-fires, 0..25 at n=5
- `SN_X` = sum of `S_X(r)` over MNF
- `MH_X` = sum of `F_X(r)` over MF — must-fire hits, 0..45
- `SM_X` = sum of `S_X(r)` over MF
- Arm **B** = control = the unchanged 439-character description. Arm **A** = treatment = the
  551-character description above.
- `p_attr` = two-tailed Fisher exact on `[[OF_B, SN_B - OF_B], [OF_A, SN_A - OF_A]]`

**Sample floors** (80 percent of planned, expressed as counts, never as a rate of this instrument):
`SN_A >= 20`, `SN_B >= 20`, `SM_A >= 36`, `SM_B >= 36`.

**Attempt cap:** 170 live invocations total across both arms (140 planned plus up to 30 retries).

**Closure threshold:** `OF_A == 0` and `F_A(r) == S_A(r)` for every r in MF.

**Attribution threshold:** `p_attr < 0.05`. Below it, the round may still close CAT-10 on Arm A's own
measurement, but the annotation must state in as many words that the improvement is not
distinguishable from the control at this sample size.

**Branch precedence — first match wins, evaluated 6, 5, 4, 1, 2, 3.**

| Branch | Condition | `REQUIREMENTS.md` CAT-10 | `WINDOWS.md` id 24 | `02-UAT.md` G-02-2 | Shipped description |
|---|---|---|---|---|---|
| **1 — closed** | `OF_A == 0` and `F_A(r) == S_A(r)` for every r in MF | `[x]`, annotation states `OF_A/SN_A`, `OF_B/SN_B`, `MH_A/SM_A`, `MH_B/SM_B`, `p_attr`, the per-row Clopper-Pearson bound at n=5, the model, the harness, both description hashes and the reproduction command — and states attribution only if `p_attr < 0.05` | `fixed` | `status: resolved` | kept |
| **2 — improved, not closed** | `0 < OF_A < OF_B` | stays `[ ]`, annotation states both arms, `p_attr`, and that a rate above zero does not satisfy a truth that says "every must-not-fire phrasing" | stays `open`, description replaced with both arms and the delta | `partially_resolved` | kept |
| **3 — did not move, or inverted (H4 null)** | `OF_A >= OF_B` and `OF_A > 0` | stays `[ ]`, annotation records the residual as **accepted and disclosed, explicitly NOT satisfied**, states both arms, and names the next candidate lever as unfunded | `waived` via `gsd-tools windows waive 24 "<reason>"`; the reason states both arms' figures, that this was the FIRST lever against this residual, that H4 is now tested rather than assumed, that the clause is kept for surface consistency, and that the waiver is reversible by re-opening the entry | `partially_resolved` | **kept** — the clause makes the trigger surface agree with the body's Limits section, which is correct independently of any activation effect; keeping it is disclosed as "no measured activation effect at n=5" |
| **4 — must-fire regression** | any r in MF with `F_B(r) == S_B(r)` and `F_A(r) < S_A(r)` | stays `[ ]`, annotation states the regressing row, both arms, and that the clause was tested and reverted | stays `open`, description replaced with Arm B's measured pre-fix over-fire counts (a strictly better characterisation of the original defect than the n=1 observation it replaces) | `partially_resolved` | **reverted** — `git checkout <pre-Task-4 commit> -- skills/proof-first/SKILL.md .claude-plugin/plugin.json .claude-plugin/marketplace.json evals/pressure-tests.md`, then `python3 tools/generate_derivatives.py` |
| **5 — under-sampled** | any sample floor unmet after the attempt cap | stays `[ ]`, annotation states the achieved `S` counts and why the cap was hit; no bound and no `p_attr` are claimed | stays `open` with the achieved counts | `partially_resolved` | kept, disclosed as shipped-but-under-measured |
| **6 — harness unavailable** | Task 3's `<precondition>` fails | stays `[ ]`, annotation gains one line naming the blocker and the date | stays `open`, one added line | unchanged apart from a blocker line | **unchanged** — Tasks 4, 5 and 6 do not run; no description edit ships without a measurement |

**Branch 3 is an acceptance of a residual, not a satisfaction of the requirement.** CAT-10 stays
`[ ]` in every branch except 1.

**The rule is not revisable after the number is known.** If the measured figures land in a shape
this table did not anticipate, that fact is recorded and the nearest branch is applied as written —
no branch is added, no threshold reinterpreted, no row rewritten.

**Manifest decision, pre-committed.** All three `.claude-plugin` description sites gain the new
final sentence, appended to the existing first-sentence truncation. Reason: they are the
repository's public representation of the skill's scope and nothing mechanical binds them to
`SKILL.md`, so leaving them inclusion-only would ship a marketplace listing that contradicts the
skill's own stated limits. They cannot confound the measurement: `run_session()` copies only
`skills/proof-first/` into each session. Under Branch 4 they are reverted with everything else.

**Transcript-retention rule, pre-committed.** `evals/trigger/INIT-EVENTS.md` — a distillation of
every session's `system/init` event, which is what settles Q3 (what the harness actually loads at
activation) and H3 (which competing skills were candidates) — is committed unconditionally. The raw
JSONL captures are committed as `evals/trigger/transcripts-cat10.tar.gz` if `du -k` on the gzipped
tarball reports under 5120; otherwise the measured size and the local path are recorded in
`INIT-EVENTS.md` and the tarball is not committed.

---

No session in this round has yet run.
