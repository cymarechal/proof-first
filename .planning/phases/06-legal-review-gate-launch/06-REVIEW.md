---
status: clean
phase: 06-legal-review-gate-launch
reviewed: 2026-09-21
round: gap-closure (06-06)
scope: files changed by 06-06's gap commits (d5efe4b..HEAD)
reviewer: inline (orchestrator) — the gsd-code-reviewer subagent was not dispatched
findings_total: 0
findings_open: 0
findings_fixed: 0
supersedes: 06-REVIEW.md as committed for the 06-05 round (preserved in full below)
---

# Phase 6 Code Review — gap-closure round (06-06)

**One source file changed in this round: `tools/check_repo.py`. No findings.**

Fourteen commits; thirteen touch documentation only. The single executable change adds one violation
code, `benchmark-run-claim-stale`, with its constants, its check function, its self-test fixtures and
its mutation.

## What was reviewed, and how

The review is behavioural, not a read-through. Every claim the new code's docstring makes about what
it does was put to a probe against an unmutated sibling control — red for the stated reason, green on
the control — rather than accepted from the prose.

| Claim in the docstring | Probe | Control | Mutant |
|---|---|---|---|
| Catches a regression restored **capitalised** | `No benchmark has run.` appended to the skill source | 0 | 1 ✓ |
| Catches a **derivative-only** regression the source-blind sibling would miss | lowercase claim appended to `output-styles/proof-first.md`, source untouched | 0 | 1 ✓ |
| Stays silent when the **evidence file is absent** — the sentence is then true | same capitalised mutant, `evals/benchmark/RESULTS.md` deleted | — | 0 ✓ |

The third row is the one that matters most: it is the two-sided conjunction the sibling code
established, and without it the check would fire on an honest disclosure in a tree where no benchmark
had run.

## Points considered and cleared

- **Placement in `run_derivative_checks`.** The call sits above the `numbering_path.exists()` early
  return, so it runs whether or not `NUMBERING.md` is present. Checked deliberately — the sibling
  call has the same placement and the ordering is load-bearing.
- **`BENCHMARK_CLAIM_PATHS = DERIVATIVE_PATHS + DERIVATIVE_SOURCE_NAMES`.** Both operands are tuples,
  so this concatenates to seven paths rather than doing anything surprising. Each is existence-guarded
  before it is read.
- **False-positive surface of a case-insensitive substring.** Widening the match widens what can trip
  it. The declared ceiling states the check is literal presence and nothing more, matching the
  sibling's disclosed discipline, and the corrected sentence in the tree does not contain the needle
  — `check_repo.py` reports 0 violations, which is the direct evidence.
- **Mutation co-firing.** The mutator appends to a `DERIVATIVE_SOURCE_NAMES` file, so
  `skill-derivative-stale` fires on the same mutant. This does not weaken the result:
  `mutation_test` requires only that the expected code is silent on the control and fires on its own
  mutant, and the control ran clean at 0 violations.

## Deviation from the plan, reviewed on its merits

The plan directed that the literal be added to the existing `check_derivative_comparison_claim`. The
executor made it a sibling code instead. Reviewed and **upheld**: the mutation harness maps one code
to one mutation, so a second literal folded into an existing code would have been registered without
ever being independently discrimination-proven — which is this repository's own named recurring
defect, `.planning/WINDOWS.md` id 10. The deviation serves the plan's stated intent ("prove the
addition discriminates via `--mutation-test`") better than its letter would have. It is recorded in
the commit message rather than left to be discovered.

## Gate

All ten commands from `.github/workflows/ci.yml`, after the final commit: green.
`check_repo.py --mutation-test` reports **57 codes discrimination-proven** with a clean control, up
from 56.

## The caveat, repeated rather than assumed carried over

**This review was not independent.** The agent that wrote the code also reviewed it — the exact
weakness `.planning/WINDOWS.md` id 17 measures, and which this phase's cold reads have now
demonstrated for a fifth consecutive round. The behavioural probes above are worth more than the
read-through precisely because they do not depend on the reviewer's judgement, but a clean
self-review is still weaker evidence than a clean independent one.

The round did run one thing an ordinary self-review does not: it re-read the sentences it had
*added*, not only the ones it fixed, and found two further checkably-false statements — one of its
own making. Both were corrected before the round closed. That is recorded here because the previous
round's failure was precisely this, and catching it once is not evidence the habit holds.

---

# Superseded: Phase 6 Code Review — gap-closure round (06-05)

The round-2 review above replaces this one at the same deterministic path. It is preserved in full
rather than overwritten, because the round it reviewed is the round whose defects round 2 found.

# Phase 6 Code Review — gap-closure round (06-05)

**No source file changed in this round. No findings.**

## Superseded reviews

This file replaces, at the same deterministic path, the **first-round review of 2026-09-21**
recorded in commit `fbcef01`. That round reviewed 1,504 added lines across
`tools/check_repo.py` and `evals/benchmark/run_benchmark.py` — a different file set entirely from
this one — and returned **one low-severity finding, fixed in place, verdict clean**: a dead
`markers` parameter and a redundant identical-branch ternary in `check_repo.py`'s
`_claim_readme()` self-test fixture builder.

Read it in full with:

```
git show fbcef01:.planning/phases/06-legal-review-gate-launch/06-REVIEW.md
```

Nothing in it is re-litigated here. Its finding was fixed and re-verified in that same commit, and
neither of the two files it reviewed is touched by this round.

## Scope

```
git diff --name-only 7e2170d..HEAD
```

| File | Lines | Kind |
|---|---|---|
| `README.md` | +81 / -27 | shipped prose |
| `LEGAL-REVIEW.md` | +314 / -74 | shipped prose |
| `NUMBERING.md` | +15 / -5 | shipped registry prose |
| `.planning/WINDOWS.md` | +51 / -21 | planning artefact |
| `06-05-SUMMARY.md` | +225 | planning artefact |

```
git diff --name-only 7e2170d..HEAD -- . ':!.planning/' ':!*.md'
```

Returns nothing. **No `.py`, no `.json`, no `.yml` changed.** The code-review capability's normal
remit — source files changed in the phase — is empty for this round, and the honest report of that
is this sentence rather than a re-review of code the round did not touch.

## What was reviewed instead

The round's actual risk surface is prose that makes checkable factual claims, which is the class
`.planning/WINDOWS.md` id 17 records as invisible to every check in this repository. Every factual
assertion the diff introduces was re-verified against its own source:

| Assertion introduced | Checked against | Result |
|---|---|---|
| Arm B: 45/45 must-fire, 9/25 must-not-fire, 2026-09-20, `claude-sonnet-5` | `RESULTS-trigger.md`:92-97 Totals block | matches |
| Arm B measures the shipped description | `head -14 skills/proof-first/SKILL.md \| shasum -a 256` == the hash at `RESULTS-trigger.md`:68 | byte-identical |
| Two near-miss phrasings account for all nine over-fires, at 5/5 and 4/5 | `RESULTS-trigger.md`:86-90 | matches (rows 87, 88; rows 86, 89, 90 are 0 of 5) |
| Three measured arms; routes 1 and 2 collapse | `run_routes.py`:113 `ROUTES` tuple; README:54-71 routes 1 and 2 both install the skill folder | matches |
| MOD-04's threshold is "before its first rule marker" | `run_conformance.py`:4-6 | matches |
| `scenarios.json` holds eight prompts, two per family | parsed: 8 entries, `Counter({executive-summary: 2, rfp-rfi: 2, solution-proposal: 2, demo-discovery: 2})` | matches |
| `proxy-sources.md` is the source for `lint.py`'s proxy terms | `proxy-sources.md`:3-7 | matches |
| `ci.yml` runs the checker, its two test modes, every eval self-test, and the derivative check | `ci.yml` names 6 eval scripts; `grep -rln self-test evals/` returns the same 6 | matches |
| `catalog-count-mismatch` and `readme-layout-tree-stale` exist as codes | `tools/check_repo.py` | both present |
| MEDDPPCC, and four letter-ambiguous positions | `NUMBERING.md`:64-77 | M,E,D,D,P,P,C,C; DC/DP both D, Champion/Competition both C |
| The `source-gate-incomplete` ceiling quoted verbatim | `tools/check_repo.py`:484-487 | exact |
| Ledger counts 9 fixed + 2 closed-on-reasoning + 9 waived + 9 open = 29 | `.planning/WINDOWS.md` frontmatter and its 29 JSON entries | matches |

## Findings

None.

## Considered and deliberately not flagged

- **`README.md`:126 still reads "the one canonical fictional deal every worked example cites."**
  Checked rather than assumed: this is the narrow claim the plan explicitly preserved. It is true —
  every worked example cites `examples/deal-brief.md`. The false claim was the *shipping* one at
  :7-8, and that is the one rewritten.
- **The `WINDOWS.md` table regeneration rewrote 51 lines.** Verified as a rendering change, not a
  content change: the fenced JSON is the source of truth, three reasons were reconciled INTO it
  from table-only edits, and the table was then re-rendered with `broken-windows.cjs`'s own
  escaping rule. `gsd-tools windows append` accepting the next write is the mechanical proof the
  two agree.
- **`LEGAL-REVIEW.md` is declared append-only and this round edited earlier sections.** Deliberate
  and bounded: the edits are the register corrections `06-05-PLAN.md` Task 7 commissions by line
  number, plus three heading amendments that mark superseded findings. No earlier finding was
  deleted or reworded into a different finding, and the substantive supersession is an appended
  section 4.

## Verdict

**Clean.** No source file changed, so no code defect is possible from this round; every checkable
prose assertion it introduces was verified against the file it refers to, and all ten commands
`.github/workflows/ci.yml` declares exit 0.

The caveat from the first round applies unchanged and is repeated rather than assumed carried over:
**this review was not independent.** The agent that wrote the text also checked it, which is the
exact weakness `.planning/WINDOWS.md` id 17 measures and which this round's own cold read
demonstrated for a fourth consecutive time. Treat a clean self-review as weaker evidence than a
clean independent one.
