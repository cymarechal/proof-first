# Phase 06 Research — Legal Review Gate & Launch

> Every external fact below was fetched live during this research session on 2026-09-21 against
> working tree `82b20539844c865bd9d9d268bddf443ba04f297d`. Nothing here is recalled from training
> data. Where a lookup failed, the failure is recorded as a failure, not smoothed over.

## Summary

Phase 6 is the only phase in this project whose deliverable is a *judgement* rather than a
mechanism. Its two requirements pull in opposite directions and must not be blended:

- **LEG-04** is a gate a human passes: every framework-derived concept traces to a named, current,
  public source, and the three rights-holder statements in `NOTICES.md` are true as of the review
  date. The repository has carried six `unverified | to confirm at LEG-04` rows in `SOURCES.md`
  since 2026-09-10 and two open reproduction-boundary judgements (`WINDOWS.md` ids 3 and 6)
  explicitly routed here.
- **LEG-05** is a mechanism: no claim or badge in `README.md` may state a figure the committed
  benchmark records do not recompute to, and every such figure must carry its model strings and its
  run date.

**The single largest finding of this research session is that the blocking premise behind three
phases' worth of deferred verification has expired.** `WINDOWS.md` ids 1 and 18 and every
`to confirm at LEG-04` row in `SOURCES.md` were deferred on the stated ground that this environment
has no live network access. Measured this session: `curl https://example.com` returns HTTP 200,
`WebSearch` and `WebFetch` both return results, and the CourtListener REST API answered an
unauthenticated query about the exact litigation the roadmap names. The premise was true when
recorded and is false now. LEG-04's source confirmation is runnable work, not a human-only
checkpoint.

**The second finding is that the benchmark hands this README a real result, and it is not the
result the project wanted.** Pooled across all 48 both-orders-averaged pairs, the skill-on
condition wins 45 of 48 on evidence and 32 of 48 on clarity, and **loses 38 of 48 on persuasive
force**. That is a measured, committed, reproducible finding that sits in tension with this
project's own core value statement. LEG-05's honest discharge is to state it, not to find a
subset of the data that reads better.

## Architectural Responsibility Map

| Concern | Owner | Why here and not elsewhere |
|---|---|---|
| Does a concept trace to a real, current, public source? | `SOURCES.md` rows + a new mechanical provenance check | The rows exist; nothing reads them. A row can claim `verified` today with an empty `Where` cell and no check notices. |
| Is the rights-holder statement true today? | `NOTICES.md` framework statements + `Last reviewed` dates | `check_framework_statements` enforces only that each of the three `###` headings exists and that its section contains `Non-affiliation`, the phrase `not affiliated`, and `Rights-holder`. Read this session: it does **not** check `Paraphrase boundary`, does **not** check `Last reviewed`, and cannot know whether the named holder is still the holder. |
| Does a paraphrase reproduce proprietary expression? | A human read, recorded in a committed review artifact | `tools/check_repo.py`'s own module docstring already names this as Phase 6's job and refuses to attempt it. |
| Does a README figure recompute from committed records? | A new mechanical check over `README.md` against `evals/*/RESULTS*.md` | The existing `readme-*` codes check structure (anchors present, order, destination named). None reads a number. |
| Is the publish location real? | `publish-location-drift` (already enforces internal agreement) + a human decision | The checker proves the four occurrences agree. It cannot prove they resolve. |

## User Constraints

From `.planning/PROJECT.md` and the repository's own standing posture, restated because this phase
is the one most tempted to violate each:

1. **Measured claims or no claims.** Any headline number must be reproducible from a committed
   script. This phase writes the only claims the repository will carry, so this constraint binds
   here harder than anywhere else.
2. **Zero dependencies, stdlib-only.** Every check this phase adds runs under `python3` with no
   install step. A network call must never be a build gate — provenance is recorded at review time
   into a committed file, and the *check* reads that file offline.
3. **Paraphrase only, reproduce nothing.** This phase reads more source material than any other, so
   it is also the phase most able to contaminate the repository with a source's own wording. Source
   *titles* and *URLs* are citations, not reproductions; source *prose* does not enter the
   repository.
4. **Trademark neutrality.** `NOTICES.md` currently states that ownership in the MEDDIC family is
   contested and makes "no claim about the outcome of any proceeding." Research below shows why
   that sentence must be updated carefully rather than deleted.

## Phase Requirements

| ID | Statement | What discharges it |
|---|---|---|
| LEG-04 | A legal review gate passes before public launch, with the MEDDIC-family trademark status reconfirmed against current sources | Every `SOURCES.md` row carries a real URL and a retrieval date; the three `NOTICES.md` statements are reconfirmed and re-dated; `WINDOWS.md` ids 3 and 6 are dispositioned in a committed review record; a provenance check makes a future unsourced row a build failure |
| LEG-05 | README claims and badges derive only from committed benchmark results, with the model versions and date stated | Every numeric figure in README's claim region appears verbatim in a committed results file; every such sentence carries a model string and an ISO date; a badge policy is stated and mechanically enforced |

## The Six Decisions

### Decision 1 — The network premise has expired; re-run what it blocked

**Measured this session, not assumed:**

| Probe | Command | Observed |
|---|---|---|
| General egress | `curl -sS -o /dev/null -w '%{http_code}' https://example.com` | `200` |
| USPTO reachable | `curl ... https://tsdr.uspto.gov/` | `200` |
| Web search tool | `WebSearch` on four framework queries | results returned, four distinct queries |
| Page fetch tool | `WebFetch` on an IPWatchdog press page | full extraction returned |
| Court records API | `curl 'https://www.courtlistener.com/api/rest/v4/search/?q=MEDDICC&type=r'` | HTTP 200, 5,963 bytes, no API key required |

Four deferrals were recorded against "no live network access in this environment":
`WINDOWS.md` id 1 (Phase 1 name-collision search, since marked `fixed`), `WINDOWS.md` id 18
(`evals/benchmark/bench-deal-brief.md` name-collision search, **still open**), and every
`to confirm at LEG-04` cell in `SOURCES.md`. Per this project's own standing rule about stale
blocker premises, the reason is re-checked before the deferral is honoured. It does not hold. This
phase runs those searches.

**Ceiling to disclose:** network availability inside *this* session is not a property of the
repository. A contributor reproducing the phase two years from now may have no network, and the
sources may have moved. That is why the *output* of the network work is a committed file of URLs
and retrieval dates, and the *check* over it is offline and stdlib-only. Nothing this phase adds to
CI makes a network call.

### Decision 2 — The MEDDIC-family status, reconfirmed against primary and press sources

The roadmap criterion names "the MEDDPICC genericness ruling" specifically. Fetched this session:

| Fact | Value | Source |
|---|---|---|
| Case caption | *MEDDICC Ltd. v. 01 Consulting LLC* | CourtListener docket record |
| Docket number | 2:24-cv-01836 | CourtListener docket record |
| Court | U.S. District Court for the Eastern District of Pennsylvania | CourtListener; IPWatchdog |
| Judge | Chief Judge Wendy Beetlestone | CourtListener `assignedTo`; IPWatchdog |
| Filed | 2024-04-30 | CourtListener `dateFiled` |
| Summary-judgment ruling | 2026-04-21 | IPWatchdog press item |
| Registration at issue | No. 6,489,058 (MEDDPICC) | IPWatchdog press item |
| Registrant | Darius Lahoutifard / 01 Consulting LLC, d/b/a MEDDIC Academy | IPWatchdog press item |
| Holding | MEDDPICC is generic; USPTO directed to cancel the registration; counterclaims dismissed with prejudice | IPWatchdog press item |
| **Docket terminated?** | **No — `dateTerminated: null`** | CourtListener |
| **Most recent docket activity** | **2026-09-14, "Response in Opposition to Motion"** | CourtListener docket entries |

**The last two rows are the ones that matter for `NOTICES.md`.** A summary-judgment order directing
cancellation is not the same thing as a cancelled registration, and post-judgment motion practice
was live on this docket seven days before this research session. The repository's existing sentence
— "This repository makes no claim about the validity of any mark in this family and no claim about
the outcome of any proceeding" — is **correctly calibrated to this situation and must survive the
update**. The honest change is additive: name the proceeding and the ruling as a matter of public
record, state that the docket was still active when this review ran, and keep refusing to predict
where it lands.

The same sentence carries a second clause worth preserving: "a determination about one spelling in
the family is not treated here as covering another." The ruling addressed MEDDPICC. This repository
paraphrases concepts under the MEDDIC / MEDDICC spellings and its own namespace is `MC-`. The
clause already does the right work; the review must not quietly widen the ruling to spellings it
did not reach.

**Failed lookups, recorded as failures.** Two attempts to confirm the *register's current state*
for Reg. No. 6,489,058 returned `HTTP 503` ("The overall system is currently unavailable") and
`HTTP 403` from `tsdr.uspto.gov`, and a POST to the `tmsearch.uspto.gov` API returned
`405 MethodNotAllowed`. So this session confirmed *the ruling* from press and docket sources and
did **not** confirm *the register*. The plan treats the register check as a task with a stated
retry path and an explicit "record the failure" branch, not as a foregone conclusion.

### Decision 3 — The other two rights-holders have also moved

**Challenger.** `NOTICES.md` names "Challenger Inc. and its trademark successors." Search this
session returns that Challenger was acquired by Richardson Sales Performance in September 2024,
after an earlier period under Marlin Equity and, before that, inside CEB Inc. (acquired by Gartner
in 2017). The trailing "and its trademark successors" is why the existing statement is not false
— but a statement that is only saved by its hedge is exactly what a review gate exists to catch.
The review confirms the current holder and names it.

**Command of the Message / Force Management.** Search this session found Force Management using
`Command of the Message®` as its own mark and found no evidence of an ownership change. The
confirming source for the `SOURCES.md` row is Force Management's own public description of the
framework. No registration number was retrievable through the failing USPTO endpoints above.

**Consequence for the review's shape:** two of three framework statements need a factual update and
all three need a new `Last reviewed` date. A review that re-dates without re-reading is the failure
mode; the review record names what was checked for each, so a re-date with no evidence is visible.

### Decision 4 — `SOURCES.md` needs a check, because nothing reads it

`tools/check_repo.py` reads `NUMBERING.md`, `examples/deal-brief.md`, `NOTICES.md`, `README.md`,
`skills/`, `.claude-plugin/`, `output-styles/`, `prompts/`, and `evals/conformance/RESULTS-mod04.md`.
Grep for `SOURCES` in the checker returns only prose mentions inside other checks' messages.
`SOURCES.md` is not in `MUTATION_SOURCES` either. **The approved-source list is entirely unenforced.**

That is the gap the tracer closes, and it is the right tracer because it is the smallest slice that
crosses every layer this phase touches: a real source row, confirmed against a live source, recorded
with provenance, enforced by a new check code, discrimination-proven by the mutation harness, green
in CI.

**Precedent to copy exactly:** 03-14 added `'evals'` to `MUTATION_SOURCES` so
`results-breakdown-count-mismatch` became discrimination-proven rather than merely registered. This
phase adds `'SOURCES.md'` for the same reason and with the same comment discipline.

**What the check can and cannot do.** It can assert that a row claiming `verified` carries an
absolute `https://` URL and an ISO-8601 retrieval date in its `Where` cell, that no row is left
`unverified` once the review record declares the gate passed, and that the review record's date is
not older than the newest `Last reviewed` line it claims to cover. It **cannot** assert the URL
resolves (that is a network call, banned from CI) or that the source says what the row claims (that
is the semantic judgement `SOURCES.md` itself says no tool in this stack performs). Both ceilings
go in the docstring, the way every other ceiling in this file does.

### Decision 5 — What the benchmark actually supports, computed not recalled

Derived this session from `evals/benchmark/RESULTS.md` by summing its committed per-cell tables.
Every figure below is arithmetic over rows already in the repository — no new measurement, no new
spend.

**Mechanical proxy counts — no direction.**

| Grouping | skill-off | skill-on |
|---|---|---|
| Mean of the 16 cell means, both models | 8.21 | 7.47 |
| `claude-opus-5`, 8 cells | 10.55 | 8.43 |
| `claude-sonnet-5`, 8 cells | 5.86 | 6.53 |

Per-cell direction: skill-on is **lower in 8 of 16 cells, equal in 1, higher in 7**. The two models
move opposite ways. This is why `RESULTS.md` already says the proxy counts "do not move in one
direction" and why no headline proxy number exists to publish.

**Judged persuasion — three sharply different directions.** Pooled over all 48 both-orders-averaged
pairs per dimension:

| Dimension | skill-on wins | ties | skill-on losses |
|---|---|---|---|
| evidence | 45 | 1 | 2 |
| clarity | 32 | 3 | 13 |
| persuasive_force | 7 | 3 | **38** |

Split by model, the pattern is consistent rather than driven by one: opus 24/0/0 and sonnet 21/1/2
on evidence; opus 4/0/20 and sonnet 3/3/18 on persuasive force.

**This is the phase's hardest content decision and it is not close.** The project's core value is
that a technical evaluator finishes the document believing the author understands their problem.
One language model, scoring blind in both orders against a rubric that deliberately asks a
different question from clarity, rated the un-skilled draft more persuasive in 38 of 48 pairs. The
repository's own standard — measured claims or no claims, and the linter's own precedent of
publishing a null result and a decline rather than burying them — permits exactly one response:
state all three dimensions with equal prominence, in the same sentence-neighbourhood, with the
model strings and the date.

**A caveat that must travel with the persuasive-force figure, from `RESULTS.md`'s own caveats
section:** these scores are one language model's rating against the rubric `build_judge_prompt()`
sends it, no human evaluator scored any text, and the skill-off condition receives a materially
shorter prompt. The figure is real; what it measures is narrower than the word "persuasion"
suggests.

**Mechanical consequence for LEG-05.** The three pooled totals above are *my* arithmetic over
`RESULTS.md`'s committed per-cell tables. LEG-05 requires README figures to derive from committed
benchmark results. A hand-summed total in the README would be a figure no committed script
recomputes — the exact failure the requirement names. So `run_benchmark.py --report-only` must emit
the pooled totals into `RESULTS.md` itself, and README must cite that. The re-render diff
(`git diff --exit-code evals/benchmark/RESULTS.md` clean after `--report-only`) is the existing
proof mechanism and carries over unchanged.

**One trap in doing that.** `WINDOWS.md` id 20 records that `aggregate()`'s mean/range table pools
individual per-order judgement records instead of averaging each pair's two orders first, the way
`judge_summary()` / `average_orders()` does. A pooled win/tie/loss total must be built from the
*paired* path, never by re-pooling per-order records, or the new figure inherits a defect the file's
own caveat says was corrected.

### Decision 6 — What this phase must NOT claim

Named here so the plan can point at a list rather than re-derive judgement, mirroring 05-RESEARCH's
Decision 8:

1. **No legal advice, and no assertion that the repository is "legally cleared" in a sense a lawyer
   would recognise.** The gate is a documented diligence record by a non-lawyer against public
   sources. The review record says so in those words.
2. **No prediction about the MEDDICC litigation.** The docket is open. Report the ruling as a matter
   of public record and stop.
3. **No widening of the MEDDPICC holding to MEDDIC or MEDDICC.** `NOTICES.md` already forbids this
   and the review must not undo it.
4. **No claim that the skill improves persuasion.** 38 of 48 pairs say the opposite under this
   instrument.
5. **No claim that the skill reduces violations.** 8 of 16 cells lower, 7 higher, models opposite.
6. **No badge carrying a number that is not in a committed results file with its model strings and
   date beside it.**
7. **No claim that any install route has been verified until it has actually resolved.** DIST-01 and
   DIST-02 have never run end to end because no published repository exists.

## Also Researched

### The four open README-and-launch windows this phase inherits

| id | What it is | Runnable here? |
|---|---|---|
| 11 | `<owner>/<repo>` publish placeholder across two manifests and README | Needs a human decision on the real location, then mechanical substitution |
| 12 | DIST-06 README prose quality — does the lead-in read as leading with examples | Human read; no check exists or should |
| 16 | Output-style `/config` picker never observed | Needs a human on a real machine with a `/config` picker |
| 17 | No code compares two factual assertions in one document | Deliberately refused as a check; cold human read each round |
| 18 | Name-collision search for `bench-deal-brief.md`'s invented names | **Now runnable** — see Decision 1 |
| 25 | README must decide what it says on the strength of the benchmark | **This phase's LEG-05 work** — see Decision 5 |

Ids 12, 16 and 17 are irreducibly human. They are the phase's manual verifications, not gaps in its
automation.

### The ledger's own rendering defect

`.planning/WINDOWS.md` frontmatter reports `total_count: 28` and the embedded JSON array holds 28
entries, but the human-readable Markdown table above it holds only 27 rows — entry 28 (the 04-15
route-equivalence null result) is present in the JSON and absent from the table. Anyone reading the
table alone under-counts the open work by one. This is a GSD tooling artifact rather than repository
content, and it is recorded here so the launch gate's ledger sweep reads the JSON, not the table.

### Current instrument state, measured this session

| Fact | Command | Observed |
|---|---|---|
| Live check | `python3 tools/check_repo.py` | `check_repo: 0 violations` |
| Mutation discrimination | `python3 tools/check_repo.py --mutation-test` | `49 codes discrimination-proven`, 8.1 s wall |
| CI surface | `.github/workflows/ci.yml` | 10 commands, all offline, all stdlib-only |
| Python | `python3 --version` | 3.13.13 |
| CLI | `claude --version` | 2.1.267 |

The mutation harness has grown from 1 second (measured before Phase 5 committed `evals/benchmark/raw/`)
to 8.1 seconds. Still an order of magnitude under the 60-second remedy threshold 05-03 set. Adding
`SOURCES.md` to `MUTATION_SOURCES` adds one small file to 50 throwaway copies; the growth is
negligible and the phase re-measures rather than assuming.

## Common Pitfalls

### Pitfall 1: Re-dating a review without re-reading

`Last reviewed: 2026-09-10` appears four times across `SOURCES.md` and `NOTICES.md`. Bumping those
dates is a one-character edit and is indistinguishable, in a diff, from a review that actually
happened. The mitigation is that the review record names what was checked for each statement and
what the check returned, so a bare re-date has nothing standing behind it.

### Pitfall 2: Letting a source URL into the repository as a reproduction

Confirming a source means recording its title, publisher, kind, URL and retrieval date. It does not
mean quoting it. The riskiest moment in this whole phase is an executor reading a framework vendor's
page in order to confirm a row and carrying a phrase from it into `SOURCES.md` or the review record.
`check_source_label_in_skill_content` guards the skill content against registry labels; nothing
guards a new file. The plan states the prohibition explicitly and the review record is read against
it.

### Pitfall 3: Publishing as a reversible act

Making the repository public is a **one-way door**. Deletion does not un-index it, un-clone it, or
un-archive it, and this repository's content includes named rights-holders and a trademark posture.
That earns a blocking decision checkpoint before the substitution task, per the default
reversibility policy.

### Pitfall 4: A CI badge read as a quality claim

A green build badge says "ten offline scripts exited zero." A reader skimming a README next to the
words "Proof First" may read it as "the claims in this document are verified." LEG-05's cleanest
discharge is a stated badge policy — which badges are allowed, what each one means, and a
mechanical check that no unlisted badge appears.

## Code Examples

### The provenance check's shape (mirrors the existing `run_*_checks` convention)

```python
SOURCES_CHECK_CODES = (
    'source-row-unconfirmed',      # Status is verified but Where has no https:// URL + ISO date
    'source-row-stale-review',     # SOURCES.md's Last reviewed predates a row's retrieval date
    'source-gate-incomplete',      # the review record declares the gate passed while a row is unverified
)
```

Registered into `ALL_CHECK_CODES`, dispatched from `run_all_checks` via `run_sources_checks`, one
`MUTATIONS` entry each so `--mutation-test` proves discrimination against the real file rather than
only against a fixture.

### The README claim check's shape

```python
README_CLAIM_CODES = (
    'readme-claim-unsourced',      # a number inside the claim region absent from any committed results file
    'readme-claim-unanchored',     # a claim sentence with no model string and no ISO date nearby
    'readme-badge-unlisted',       # a badge image whose target is not on the stated allow-list
)
```

Both groups follow the `str`-code-point, `sorted()`-stable ordering discipline the module docstring
already declares for output ordering.

## Validation Architecture

### Test Framework

No test framework. This repository's validation is its own self-testing scripts, run by
`.github/workflows/ci.yml`. Phase 6 adds no framework and introduces no dependency.

| Property | Value |
|---|---|
| Framework | none — self-testing stdlib scripts |
| Config file | `.github/workflows/ci.yml` |
| Quick run command | `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py` |
| Full suite command | the ten commands in `.github/workflows/ci.yml`, in order |
| Estimated runtime | ~12 s (8.1 s of it is `--mutation-test`) |

### Phase Requirements → Test Map

| Requirement | What proves it | Command |
|---|---|---|
| LEG-04 — every row sourced | `source-row-unconfirmed` fires on an unsourced row and is silent on the real file | `python3 tools/check_repo.py --mutation-test` |
| LEG-04 — gate completeness | `source-gate-incomplete` fires when the review record claims a pass with a row still `unverified` | `python3 tools/check_repo.py --mutation-test` |
| LEG-04 — statements reconfirmed | `check_framework_statements` still green; a new `framework-statement-stale-review` fires when a statement carries no parseable `Last reviewed:` date or one older than the review record; review record names each holder and its confirming source | `python3 tools/check_repo.py --mutation-test` + human read |
| LEG-04 — reproduction boundary (ids 3, 6) | A recorded human judgement with reasoning, not a check | manual |
| LEG-05 — figures recompute | `git diff --exit-code evals/benchmark/RESULTS.md` clean after `--report-only`; `readme-claim-unsourced` silent | `python3 evals/benchmark/run_benchmark.py --report-only && git diff --exit-code evals/benchmark/RESULTS.md` |
| LEG-05 — anchoring | `readme-claim-unanchored` fires on a figure with no model string and no date | `python3 tools/check_repo.py --mutation-test` |
| LEG-05 — badges | `readme-badge-unlisted` fires on an off-list badge | `python3 tools/check_repo.py --mutation-test` |

### Sampling Rate

- After every task commit: `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py`
- After every plan: all ten CI commands in order
- Before verification: all ten green, and `--mutation-test` reporting every new code
  discrimination-proven

### Wave 0 Gaps

None. Every instrument this phase needs exists; the phase extends `tools/check_repo.py` and
`evals/benchmark/run_benchmark.py`, both of which ship self-tests and are already wired into CI.

## Assumptions Log

| # | Assumption | Basis | If wrong |
|---|---|---|---|
| A-01 | Network access persists for the executing session | Measured five ways this session | Tasks that need it state a "record the failure" branch; none of them is a CI gate |
| A-02 | The MEDDPICC ruling stands as of the review date | IPWatchdog + CourtListener, 2026-09-21 | The review record is dated; a later reversal invalidates the date, not the method |
| A-03 | USPTO endpoints become reachable on retry | 503 reads as transient, 403 does not | Record "register state not confirmed, endpoint returned N" — a disclosed gap, not a silent pass |
| A-04 | The operator can supply a real `<owner>/<repo>` | Nothing in the repository supplies it and no git remote is configured | The launch plan's checkpoint offers "defer publication" as a first-class option |
| A-05 | Pooled win/tie/loss is the right README figure | It is the only level at which the three dimensions differ unambiguously | Per-model tables are already committed and can be cited instead |

## Open Questions

1. **Does the USPTO register now show Reg. No. 6,489,058 as cancelled?** Not answered — both
   endpoints failed this session. Routed to a plan task with a stated failure branch.
2. **What is the real publish location?** Unanswerable from inside the repository. Routed to the
   launch checkpoint.
3. **Should `NOTICES.md` name Richardson Sales Performance as the Challenger rights-holder, or keep
   the successor hedge?** Recommendation: name it *and* keep the hedge — the hedge is what survives
   the next acquisition. Routed to the review task as a stated choice with a recorded reason.

## Environment Availability

| Capability | Available | Evidence |
|---|---|---|
| Outbound HTTPS | yes | `curl https://example.com` → 200 |
| `WebSearch` / `WebFetch` | yes | four searches and one full fetch this session |
| CourtListener REST v4, unauthenticated | yes | HTTP 200, 5,963 bytes |
| `tsdr.uspto.gov` status view | **no** | 503 and 403 on two endpoint shapes |
| `tmsearch.uspto.gov` API POST | **no** | 405 MethodNotAllowed |
| Live `claude -p` sessions | yes | CLI 2.1.267 present; Phase 5 and 04-15 both drove live matrices |
| A Claude Code `/config` picker | **no** | headless sessions have no picker — `WINDOWS.md` id 16 |

## Sources

### Primary (HIGH confidence — read in full this session)

- `.planning/ROADMAP.md`, `.planning/REQUIREMENTS.md`, `.planning/STATE.md`, `.planning/WINDOWS.md`
- `README.md`, `SOURCES.md`, `NOTICES.md`, `.github/workflows/ci.yml`
- `evals/benchmark/RESULTS.md` — all committed tables, summed programmatically this session
- `tools/check_repo.py` — module docstring, `ALL_CHECK_CODES`, `MUTATION_SOURCES`,
  `_copy_repo_subset`, `KNOWN_OPEN_VIOLATIONS`, the `run_*_checks` dispatch
- `.planning/phases/05-evaluation-harness/05-03-PLAN.md` — the house plan shape this phase copies

### Secondary (MEDIUM-HIGH confidence — fetched live this session)

- CourtListener REST API v4 search, `q=MEDDICC&type=r` and a docket-scoped follow-up —
  caption, docket number, court, judge, filing date, termination state, most recent entry date
- `ipwatchdog.com/press/us-federal-court-rules-meddpicc-is-a-generic-term-orders-cancellation-of-trademark-registration/`
  — ruling date, registration number, registrant, holding, civil action number
- `WebSearch` result sets naming `meddicc.com`, `foxrothschild.com`, `prnewswire.com` and
  `meddic.academy` items corroborating the same ruling from four independent publishers
- `WebSearch` results on Challenger Inc. ownership — Richardson Sales Performance acquisition,
  September 2024; prior Marlin Equity and CEB/Gartner history
- `WebSearch` results on Force Management's public use of `Command of the Message®`

### Failed (recorded as failures, not as absence of fact)

- `tsdr.uspto.gov/statusview/sn?searchType=rn&searchText=6489058` → HTTP 503
- `tsdr.uspto.gov/statusview/rn6489058` → HTTP 403
- `tmsearch.uspto.gov/api-v1-0-0/tmsearch` POST → HTTP 405

## Metadata

- Researched: 2026-09-21
- Working tree: `82b20539844c865bd9d9d268bddf443ba04f297d`
- Researcher role performed inline by the orchestrator; `gsd-phase-researcher` was not dispatched
  because this session bans the Agent tool. Every claim above is traceable to a command or a URL in
  this document.

## RESEARCH COMPLETE

### Key Findings

1. The "no live network access" premise behind LEG-04's deferred source confirmation has expired,
   measured five ways. LEG-04 is runnable work.
2. The MEDDPICC genericness ruling is real, dated 2026-04-21, in *MEDDICC Ltd. v. 01 Consulting LLC*,
   No. 2:24-cv-01836 (E.D. Pa.) — **and the docket was still active on 2026-09-14**, so
   `NOTICES.md`'s refusal to predict an outcome must survive the update.
3. Challenger's rights-holder changed hands in September 2024 (Richardson Sales Performance);
   `NOTICES.md`'s statement is saved only by its successor hedge.
4. `SOURCES.md` is read by no check and is absent from `MUTATION_SOURCES`. The approved-source list
   is entirely unenforced — this is the tracer slice.
5. The benchmark supports exactly one honest headline, and it cuts against the project: evidence
   45-1-2, clarity 32-3-13, persuasive force **7-3-38** against the skill, pooled over 48
   both-orders-averaged pairs.
6. Any pooled figure the README states must be emitted by `--report-only` into `RESULTS.md` first,
   built from the paired averaging path, or LEG-05 is violated by the act of stating it.

### Confidence Assessment

- HIGH on the repository's own state, the benchmark arithmetic, and the checker's architecture.
- MEDIUM-HIGH on the litigation facts — four independent publishers plus the docket, but no primary
  court document fetched.
- LOW on the current USPTO register state — not confirmed; both endpoints failed.

### Ready for Planning

Yes. One tracer, two expansion plans, one launch gate carrying the human checkpoints.
