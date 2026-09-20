---
phase: 02-rule-catalog-integrity-skill-md-core
plan: 11
subsystem: eval-harness
tags: [trigger-test, scope-hash, fail-closed, mutation-testing, code-review-cr-01]

# Dependency graph
requires:
  - phase: 02-10
    provides: The trigger instrument whose scope-hash guard this plan repairs, and the 02-REVIEW.md round that found the defect
provides:
  - A fail-closed scope-binding guard on the trigger instrument — an absent or unscoped binding now halts the run instead of passing silently
  - scope_binding_verdict(), a pure decision function beside resolve_out_mode(), making the guard's three states self-testable for the first time
  - A worked instance of a self-test case that passed over the very defect it was written for, caught by mutation probe and corrected
affects: [phase-06-legal-review-gate]

# Actuals (#2632)
actuals:
  tokens: 22000
  tasks: 3
  commits: 1

tech-stack:
  added: []
  patterns:
    - "Guard decisions extracted from main() into pure raise-on-refusal functions (the resolve_out_mode shape), so every branch is reachable from --self-test"
    - "A refusal case asserts on the refusal MESSAGE, not merely that an exception arrives, whenever a neighbouring branch can raise for a different reason"

key-files:
  created: []
  modified:
    - evals/trigger/run_trigger_test.py

key-decisions:
  - "Fixed rather than accepted, per the disposition decided at 02-UAT.md test 4: the patch was already written out in 02-REVIEW.md, touches no shipped skill content, and changes no published number, so there was no tradeoff to weigh against a silent measurement-integrity failure"
  - "Strengthened the absent-binding self-test case after the mutation probe showed it passing with the branch removed — the mismatch branch raises too (None != live_hash), so 'a ValueError arrived' was not evidence the absent-binding branch existed"
  - "Ran the mutation probe as a sibling copy inside evals/trigger/ rather than from the scratchpad: the first attempt went red on `ModuleNotFoundError: No module named 'stats'` and proved nothing, which is the same class of false-green/false-red the probe exists to detect"
  - "Left WR-01 (TOCTOU on the overwrite guard) untouched — a separate WARNING finding, out of this gap's scope and documented in 02-REVIEW.md"

requirements-completed: []

coverage:
  - id: D1
    description: "recorded_scope_hash() reads its 64-hex binding only from the ## Scope section, and returns None when that section is absent or holds no well-formed hash"
    requirement: "none (instrument integrity)"
    verification:
      - kind: unit
        ref: "evals/trigger/run_trigger_test.py --self-test — 4 scope-hash cases, exit 0"
        status: pass
      - kind: other
        ref: "Mutation M1 (restore the whole-document regex): self-test FAIL, 2 problems, both naming CR-01 defect (b)"
        status: pass
    human_judgment: false
  - id: D2
    description: "A run whose pressure-test document records no usable scope binding halts before opening any live session, instead of proceeding with the guard silently skipped"
    requirement: "none (instrument integrity)"
    verification:
      - kind: unit
        ref: "evals/trigger/run_trigger_test.py --self-test — 3 scope-binding-guard cases, exit 0"
        status: pass
      - kind: integration
        ref: "Live end-to-end: --tests against a copy with the binding removed, and against a copy whose only 64-hex token sits outside ## Scope. Both exit 1 with the absent-binding message; neither wrote an --out file."
        status: pass
      - kind: other
        ref: "Mutation M2 (remove the `is None` branch): self-test FAIL, 1 problem naming CR-01 defect (a)"
        status: pass
    human_judgment: false
  - id: D3
    description: "Both halt conditions are covered by self-test cases each proven red-then-green by a one-time mutation probe"
    requirement: "none (instrument integrity)"
    verification:
      - kind: other
        ref: "Four mutations run against an unmutated control that passes; M1/M2/M3 produce specific FAIL lines, M4 aborts the run. Full transcript in this SUMMARY's Mutation probe section."
        status: pass
    human_judgment: false
  - id: D4
    description: "Every published measurement survives untouched and the activation surface is unchanged"
    requirement: "none (instrument integrity)"
    verification:
      - kind: other
        ref: "git diff --stat HEAD -- evals/pressure-tests.md and -- evals/trigger/RESULTS-trigger.md both print nothing; head -14 skills/proof-first/SKILL.md | shasum -a 256 still prints d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675"
        status: pass
    human_judgment: false
  - id: D5
    description: "All nine commands declared in .github/workflows/ci.yml exit 0"
    requirement: "none (instrument integrity)"
    verification:
      - kind: other
        ref: "All nine CI commands declared in .github/workflows/ci.yml run after the change; every one exits 0"
        status: pass
    human_judgment: false
---

# Plan 02-11: Fail-closed scope-binding guard (gap G-02-4 / 02-REVIEW.md CR-01)

## What changed

Two defects in one guard in `evals/trigger/run_trigger_test.py`, both named by 02-REVIEW.md CR-01.

**(b) The binding search was unscoped.** `recorded_scope_hash()` ran `re.search(r'\b([0-9a-f]{64})\b', md_text)`
over the whole markdown document while its own docstring claimed it read "the sha256 the Scope
section binds the rows to". Any future sha256 reference added anywhere earlier in
`evals/pressure-tests.md` would have been adopted as the binding. It now matches the `## Scope`
section first and searches only inside it, returning `None` when that section is absent or holds
no well-formed hash.

**(a) The halt failed open.** The call site read `if bound_hash and bound_hash != live_hash`, which
is falsy when `bound_hash is None` — so a document with a missing or malformed binding ran with the
guard skipped entirely and no diagnostic. The decision now lives in `scope_binding_verdict()`, a
pure raise-on-refusal function placed beside `resolve_out_mode()` (the house pattern for exactly
this shape), with three enumerated states:

| recorded binding | verdict |
|---|---|
| absent / malformed / outside `## Scope` | refuse — rows are not provably bound |
| present, differs from live | refuse — existing behaviour, message unchanged |
| present, equals live | `'bound'` |

The mismatch message is preserved verbatim; it is quoted in `evals/pressure-tests.md`'s scope note
and in `02-UAT.md` test 2.

## Nothing published moved

`evals/pressure-tests.md` holds exactly one 64-hex token, it sits under `## Scope`, and it equals
`head -14 skills/proof-first/SKILL.md | shasum -a 256`. Every figure in `RESULTS-trigger.md` was
produced under a guard that was, in fact, checking the right hash. Both files are byte-identical
after this plan, and no skill content, manifest, or derivative was touched. What changed is the
guarantee, not the data.

## Mutation probe

Required by the plan: a self-test case that still passes with the line it protects removed is not
coverage. Run as a sibling copy inside `evals/trigger/`, deleted afterwards.

| # | Mutation | Result |
|---|---|---|
| control | none | `self-test PASS` — 3 detector, 2 table rows, 4 scope-hash, 3 scope-binding-guard, 1 aggregate-verdicts, 4 overwrite-guard, 5 render-block |
| M1 | restore the whole-document regex in `recorded_scope_hash` | `self-test FAIL: 2 problem(s)` — "adopted a sha256 from outside the ## Scope section as the binding (02-REVIEW.md CR-01 defect (b))" and "did not prefer the ## Scope hash over an earlier unrelated one" |
| M2 | disable the `if bound_hash is None` branch | `self-test FAIL: 1 problem(s)` — "did not refuse via its absent-binding branch (got 'fixture.md binds its rows to description sha256 None but the live SKILL.md hashes to aaaa…')" |
| M3 | disable the mismatch branch | `self-test FAIL: 1 problem(s)` — "did not refuse a hash mismatch via its mismatch branch (got 'no refusal at all')" |
| M4 | make the happy path raise | run aborts on an uncaught `ValueError: spurious refusal` — detected, though via traceback rather than a `FAIL:` line |

### Two probe failures worth recording

**The first probe was invalid and its three greens-to-reds meant nothing.** It ran the mutant from
the scratchpad, where `import stats` cannot resolve — every mutation "failed" with
`ModuleNotFoundError: No module named 'stats'` before reaching a single assertion. Re-run as a
sibling copy inside `evals/trigger/`, with an unmutated control proving the harness itself passes
there first. A red result is only evidence when you have read *why* it is red.

**The absent-binding case was wrong on its first writing, and the probe is what caught it.** It
asserted only that `scope_binding_verdict(None, live)` raised `ValueError`. Under M2 it still
passed — with the `is None` branch removed, execution falls through to `if bound_hash != live_hash`,
`None != 'aaa…'` is true, and the mismatch branch raises instead. The case would have gone green
over the exact critical defect it was written for: the WINDOWS id 10 shape, reproduced inside the
plan that cites WINDOWS id 10 as its reason for probing. Corrected to assert on the refusal message
(`'no sha256' in str(exc)`), which the two branches do not share; the mismatch case was strengthened
the same way.

## Verification

```
python3 tools/check_repo.py --self-test                     OK
python3 tools/check_repo.py --mutation-test                 OK
python3 tools/check_repo.py                                 OK
python3 evals/conformance/run_conformance.py --self-test    OK
python3 evals/lint.py --self-test                           OK
python3 evals/benchmark/run_benchmark.py --self-test        OK
python3 evals/trigger/run_trigger_test.py --self-test       OK
python3 evals/trigger/stats.py --self-test                  OK
python3 tools/generate_derivatives.py --check               OK

head -14 skills/proof-first/SKILL.md | shasum -a 256
  d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675   (unchanged)

git diff --stat HEAD -- evals/pressure-tests.md          (no output)
git diff --stat HEAD -- evals/trigger/RESULTS-trigger.md (no output)

grep -c "def scope_binding_verdict" evals/trigger/run_trigger_test.py          1
grep -c "if bound_hash and bound_hash != live_hash" evals/trigger/...py        0
```

End-to-end halt, beyond what the plan asked for — the guard firing against the real entry point,
not only in the self-test:

```
--tests <copy with the binding removed>            -> exit 1, "records no sha256 under its ## Scope heading"
--tests <copy whose only hash sits outside Scope>  -> exit 1, same message
                                                      neither wrote an --out file
--tests evals/pressure-tests.md                    -> passes the guard, proceeds to open sessions
```

## Deviations

One, stated in the orchestrator's report as well: this plan was executed inline rather than by a
dispatched `gsd-executor`, because the session prohibited the Agent tool. Every task, verification
command, and mutation was run as written; nothing in the plan was skipped or reinterpreted.

## Out of scope, deliberately

- **WR-01** (TOCTOU on the overwrite guard), **WR-02** (duplicated total aggregation), **WR-03**
  (`--repeats` validation) — separate 02-REVIEW.md findings, untouched, still documented there.
- **WINDOWS id 24 / CAT-10** — the over-fire residual, decided separately at 02-UAT.md test 3
  (accept, route to Phase 6). This plan does not close it and does not go near the `description`.
