---
status: clean
phase: 06-legal-review-gate-launch
reviewed: 2026-09-21
scope: source files changed in phase 06
reviewer: inline (orchestrator) — the gsd-code-reviewer subagent was not dispatched
findings_total: 1
findings_open: 0
findings_fixed: 1
---

# Phase 6 Code Review

**One finding, fixed in place. No open findings.**

## How this review was run

The `code-review` capability is active (`workflow.code_review: true`), and its `execute:post` step
hook normally dispatches a `gsd-code-reviewer` subagent. The Agent tool is not authorised in this
session, so the review was performed inline by the orchestrator instead. This is recorded plainly
rather than as a clean run by the usual route: **an inline review by the agent that wrote the code
is weaker than an independent one**, in exactly the way `.planning/WINDOWS.md` id 17 documents for
prose. Treat the result accordingly.

## Scope

```
evals/benchmark/run_benchmark.py   +195
tools/check_repo.py              +1310
```

Two source files, 1,504 added lines across four commits (`c0fca5f`, `e2e4aa2`, `187c120`,
`1b63ece`). No other source changed; the remaining commits in the phase touch Markdown only.

## What the review leaned on

This phase's code arrives with unusually strong mechanical evidence, and the review was scoped to
what that evidence does not cover rather than repeating it:

| Evidence | Covers |
|---|---|
| `--self-test`, 56 codes | Every new code fires on its defect and is silent on its clean fixture |
| `--mutation-test`, 56 discrimination-proven, CONTROL 0 violations, no FIRE-ONLY | Every new code discriminates against this repository's **real** files, not only fixtures |
| Six sibling mutation probes, each with an unmutated control | Each new self-test assertion actually fails when its branch is disabled, with the expected message |
| AST-based stdlib check, `EXTRA []` | No dependency was introduced |
| `KNOWN_OPEN_VIOLATIONS == frozenset()` | No new code was made to pass by excusing it |
| Ten-command CI surface | Nothing regressed elsewhere |

The review therefore looked for what none of the above can see: dead code, redundant branches,
duplicated logic, and declared behaviour that no caller exercises.

## Findings

### 1. Dead parameter and redundant branch in `_claim_readme()` — **FIXED**

**File:** `tools/check_repo.py`, self-test fixture builders.
**Severity:** low. Test-helper code; no shipped check is affected.

The fixture builder was written as:

```python
def _claim_readme(region_body, tree_extra='', images='', markers=True):
    start = CLAIM_REGION_START + '\n' if markers else CLAIM_REGION_START + '\n'
    end = CLAIM_REGION_END + '\n' if markers else ''
```

Two defects in three lines. The `start` ternary has **identical branches** — it reads as though the
start marker varies with `markers` and it does not. And `markers=False`, the parameter's entire
reason for existing, was **never passed by any caller**: the unbalanced-region fixture was
hand-built inline a few lines later instead, duplicating most of the builder.

Why it matters beyond tidiness: the docstring promises a behaviour (`markers=False` omits the end
marker) that nothing exercised, so nothing would have caught it breaking. A fixture builder with an
untested mode is the same class of defect as a check with no mutation entry — registered, not
proven.

**Fix applied:** the redundant ternary is collapsed, and `claim_unbalanced_root` now calls
`_claim_readme(anchored, markers=False)` instead of hand-building a second README. The parameter is
now exercised by the `readme-claim-unsourced` unbalanced-marker assertion, which still fires.
Re-verified after the change: `--self-test` passes, `--mutation-test` reports 56 codes
discrimination-proven, `check_repo: 0 violations`.

## Considered and deliberately not flagged

- **`_framework_section()` re-implements `check_framework_statements()`'s heading-to-next-heading
  bounding rather than refactoring it into one helper both call.** Flagged as a candidate, then
  dismissed: refactoring the existing function would change a code that is already
  discrimination-proven, for no behavioural gain, in a phase whose whole point is not moving
  proven ground. A v2 cleanup, not a defect.
- **`check_readme_claim_unsourced()` re-globs and concatenates the results corpus on every call,
  and `_claim_region()` is parsed twice per run** (once per claim-region code). Measured cost:
  `--mutation-test` wall time went 8.1 s → 10.1 s across seven added codes, well under the 60-second
  remedy trigger 05-03 set. Caching would add state to a module that is deliberately stateless.
- **Substring token sourcing** (`48` is sourced by any file containing `1948`). Not a defect: it is
  a declared ceiling, stated in both the function docstring and the module docstring, and tightening
  it would need token boundaries the results files do not consistently provide.
- **`readme-badge-unlisted` cannot see a raw HTML `<img>` badge.** Declared ceiling, stated in the
  docstring, and deliberately not closed with a second regex.

## Verdict

**Clean.** One low-severity finding in test-helper code, fixed in place and re-verified. No
correctness defect found in any shipped check, and none of the seven new codes depends on an
allowance, a network call, or a non-stdlib import.

The honest caveat on this verdict is the one stated at the top: this review was not independent.
