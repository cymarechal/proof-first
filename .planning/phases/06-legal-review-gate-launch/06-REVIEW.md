---
status: clean
phase: 06-legal-review-gate-launch
reviewed: 2026-09-21
round: gap-closure (06-05)
scope: files changed by 06-05's gap commits (7e2170d..HEAD)
reviewer: inline (orchestrator) — the gsd-code-reviewer subagent was not dispatched
findings_total: 0
findings_open: 0
findings_fixed: 0
supersedes: 06-REVIEW.md as committed in fbcef01
---

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
