---
phase: 06-legal-review-gate-launch
status: gaps_found
score: "2/2 must-haves verified by automated means; 6 human items performed 2026-09-21 — 3 passed, 3 issues"
verified: 2026-09-21
requirements: [LEG-04, LEG-05]
verifier: inline (orchestrator) — the gsd-verifier subagent was not dispatched
automated_verified: 22
human_verification: 6
human_verification_performed: 6
human_verification_passed: 3
human_verification_issues: 3
uat_round: "/gsd-verify-work 06, 2026-09-21"
---

# Phase 6 Verification: Legal Review Gate & Launch

**Goal:** The repo is legally cleared and honestly marketed before anyone outside the project sees it.

**Verdict: both success criteria are met by every automated means available, and six deliverables
turn on judgements no tool in this stack performs. The phase is verified but not complete — it waits
on a human.**

## How this verification was run

The `gsd-verifier` subagent could not be dispatched (the Agent tool is not authorised in this
session), so verification was performed inline by the orchestrator against the live codebase, not
against the SUMMARYs' own claims. Every figure below was re-measured during this verification pass.
The caveat that applies to the code review applies here too: **an inline check by the agent that did
the work is weaker than an independent one.** That is precisely why the six human items below are
routed out rather than absorbed.

## Success Criterion 1 — VERIFIED

> A legal review gate passes before public launch, with MEDDIC-family trademark status (including
> the MEDDPICC genericness ruling) reconfirmed against current sources.

| Must-have | Evidence measured 2026-09-21 |
|---|---|
| A review gate exists and passed | `LEGAL-REVIEW.md` line 3 `Review date: 2026-09-21`, line 5 `Gate status: PASSED` |
| The gate precedes public launch | `git remote -v` is empty. Publication was deferred at the 06-04 checkpoint, so the ordering holds trivially; the machine check (a configured remote requires a passed gate) is green |
| MEDDIC-family status reconfirmed against **current** sources | The docket was re-queried live via CourtListener REST v4 during 06-02: `dateTerminated` null, most recent entry 2026-09-14. Not transcribed from the seven-day-old research note |
| The MEDDPICC genericness ruling specifically | Re-fetched from the IPWatchdog press item: ruling 2026-04-21, Reg. No. 6,489,058, registrant Darius Lahoutifard / 01 Consulting LLC, E.D. Pa., Chief Judge Wendy Beetlestone. `2:24-cv-01836` ×1, `6,489,058` ×6, `2026-04-21` ×3 in `LEGAL-REVIEW.md` |
| The register state, which research could not obtain | TSDR status view answered this time: `LIVE/REGISTRATION/Issued and Active` ×2, on a page TSDR stamped 2026-09-21 05:36:50 EDT. Recorded as an observation with no interpretation of the gap against the cancellation order |
| All three rights-holders reconfirmed and re-dated | `NOTICES.md` carries 3 `Last reviewed: 2026-09-21` lines, one per statement, all equal to the review date |
| The refusals survived the update | `no claim about the outcome of any proceeding` ×1 and `is not treated here as covering another` ×1, both still present after the MEDDIC edit |
| Every framework-derived concept traces to a source | `grep -c 'unverified' SOURCES.md` → **0**. All six rows carry a distinct absolute URL and an ISO-8601 retrieval date |
| The gate cannot be faked | `source-gate-incomplete` and `framework-statement-stale-review` both discrimination-proven against the real files |
| The record says what kind of document it is | `not legal advice` ×2 |

## Success Criterion 2 — VERIFIED

> Every claim and badge in README derives only from committed benchmark results in RESULTS.md,
> stating model versions and date.

| Must-have | Evidence measured 2026-09-21 |
|---|---|
| Claims are bounded so they can be checked strictly | Exactly one `<!-- claim-region:start -->` and one `<!-- claim-region:end -->`, start before end |
| Every claim number derives from a committed result | 16 numeric tokens in the region; **0 unsourced** against `evals/*/RESULTS*.md` |
| Every claim states model versions and date | 7 numeric paragraphs; **0 unanchored** — each carries `claude-opus-5` or `claude-sonnet-5` and an ISO-8601 date |
| The figures are the benchmark's, not hand-sums | `--report-only` regenerates `RESULTS.md` with a clean diff; pooled rows 45/1/2, 32/3/13, 7/3/38 and direction 8/1/7 are renderer-emitted |
| The pooled figure is not position-biased | `pooled_summary()` consumes `judge_summary()`'s paired output; a self-test fixture is built so the paired and per-order answers differ, and a sibling probe with an unmutated control confirms the assertion fails if the wrong path is taken |
| Badges | README contains **no Markdown images at all**. `readme-badge-unlisted` guards a two-entry allow-list admitting build status and license only |
| The result is reported, not selected | All three judged dimensions stated with equal prominence; the 38-loss persuasive-force result is in its own sentence, followed by the judge-construct-validity and baseline-prompt-parity caveats |
| Enforcement, not promise | `readme-claim-unsourced`, `readme-claim-unanchored`, `readme-badge-unlisted`, `readme-layout-tree-stale` all discrimination-proven |

## Requirement traceability

| ID | State | Evidence |
|---|---|---|
| LEG-04 | Complete | Declared by 06-01, 06-02 and 06-04; marked only after the last of the three produced a SUMMARY, via `requirements.ready-ids` |
| LEG-05 | Complete | Declared by 06-03 alone; marked on its completion |

No requirement was marked from a SUMMARY's `requirements-completed` field. A grep for `[x]` adjacent
to `UNVERIFIED` in `REQUIREMENTS.md` returns nothing.

## Gate summary

| Gate | Result |
|---|---|
| `python3 tools/check_repo.py` | `0 violations` |
| `--self-test` | PASS, 56 codes named |
| `--mutation-test` | PASS, **56 codes discrimination-proven**, CONTROL 0 violations, no FIRE-ONLY line |
| Full CI surface (10 commands) | ALL TEN PASS |
| Code review (`06-REVIEW.md`) | `status: clean` — 1 low finding, fixed in place |
| Ledger | 28 entries, **11 fixed / 9 waived / 8 open**, frontmatter matches the JSON, no open entry with an empty reason |

The seven codes this phase added took the mutation harness from **49 to 56**, at 10.1 s wall — the
repository's own integrity metric, and still far under the 60-second remedy trigger 05-03 set.

## Human verification required — 6 items

These are the deliverables their own plans classified `human_judgment: true`. None is a gap in the
work; each is a judgement `SOURCES.md` itself states no tool in this project's stack performs.

1. **Sources are in bounds and no wording was carried** (06-01 D5, 06-02 D8). Whether the six
   confirmed pages are the kind `SOURCES.md`'s "Out of bounds" section permits, and whether the
   citations stopped short of reproduction.
2. **The reproduction-boundary reasoning is sound** (06-02 D8). Whether the `WINDOWS.md` id 3 and
   id 6 dispositions engage the 2026-04-21 genericness holding correctly rather than over-reading it.
3. **`LEGAL-REVIEW.md` does not read as legal advice** (06-02 D8). It says it is not; whether it
   *reads* that way is the judgement.
4. **README's claim region reads honest, not defensive** (06-03 D7). It states 38 losses in its own
   sentence and then the caveats. Whether a first-time reader experiences that as an honest report
   of a mixed result is the question the author cannot answer about their own text.
5. **The output style appears in `/config`** (06-04 D6). NOT PERFORMED — a non-interactive session
   has no picker. `WINDOWS.md` id 16 stays open.
6. **A cold read of README** (06-04 D7). NOT PERFORMED AS A COLD READ — the agent that wrote this
   round's edits would have been the reader. A self-read with a twelve-claim mechanical
   cross-reference found nothing checkably false, and is recorded as a self-read.
   `WINDOWS.md` ids 12 and 17 stay open.

Items 5 and 6 are recorded in `LEGAL-REVIEW.md` § Human observations as explicitly not performed,
with the structural reason. That is the honest state, not a gap this phase left untried.


## Human verification — PERFORMED 2026-09-21, 3 passed / 3 issues

The six items above were performed by `/gsd-verify-work 06` and are no longer outstanding. Two of
the three reasons this file gave for not performing them had expired and were re-checked rather
than honoured: five independent headless readers supplied the "no cold reader available" half, and
an interactive Claude Code session driven in a pty supplied the "no `/config` picker" half. Results
and evidence are in `06-UAT.md`; the three failures are planned in `06-05-PLAN.md`.

| # | Item | Result |
|---|---|---|
| 1 | Six sources in bounds, nothing reproduced | **pass** — all six public, `mos.meddicc.com` correctly not cited, no run of source prose at N=6 |
| 2 | Reproduction-boundary reasoning for ids 3 and 6 | **issue (major)** — id-6's premise is false against `NUMBERING.md`; the ruling half is sound |
| 3 | LEGAL-REVIEW.md does not read as legal advice | **issue (major)** — parts of it do; the disclaimer does not reach the verdict layer |
| 4 | README claim region reads as an honest mixed result | **pass** — "not a burial, and not close to one" |
| 5 | Output style listed and selectable in `/config` | **pass** — listed as entry 7, selection persists to `settings.local.json`, two controls |
| 6 | Cold read of README | **issue (major)** — three checkably-false statements, each contradicted by a committed file |

**This changes Success Criterion 2's standing.** It was recorded VERIFIED on the reading that every
claim and badge in README derives only from committed results stating model versions and date. The
cold read found that README:231-233 asserts exactly that, universally, and that the assertion is
false — `tools/check_repo.py`:405-415's own docstring says the region is bounded "because README
legitimately carries numbers that are not measured claims." The enforced claim region is sound; the
sentence claiming the discipline extends past it is not. The criterion is not withdrawn here, but
it should not be read as covering that sentence, and `06-05-PLAN.md` Task 1 corrects it.

**All ten CI commands were green throughout** (`check_repo.py` 0 violations, `--mutation-test` 56
codes discrimination-proven, seven `evals/` self-tests and `generate_derivatives.py --check` rc=0),
which is the fourth consecutive instance of WINDOWS.md id 17's pattern.

## What is honestly still open after this phase

Eight ledger entries, each with a named owner and a closure condition: 11 (publish location,
deferred by operator decision), 12 and 17 (cold read), 16 (`/config`), and 20, 21, 22, 24 (routed to
v2). `/gsd-ship` would block on these if `workflow.windows_enforce` were on; it is off, and the
entries are the record either way.

Two items carried from 06-02 have no ledger entry and should get one before any future publish: the
exact-name collisions on **Ardent Digital** (a real trading company, cast in the brief as a displaced
incumbent and losing bidder) and **Gina Almeida** (a real associate lawyer at an insurance group,
against a brief casting her as Associate General Counsel at an insurance firm). Both are recorded in
`LEGAL-REVIEW.md` § Name collisions with a recommended rename. Not blockers while publication is
deferred; blockers before it is not.

---
*Verified: 2026-09-21*
