---
phase: 02-rule-catalog-integrity-skill-md-core
reviewed: 2026-09-11T04:58:30Z
depth: standard
files_reviewed: 8
files_reviewed_list:
  - NUMBERING.md
  - README.md
  - evals/pressure-tests.md
  - skills/proof-first/SKILL.md
  - skills/proof-first/references/checklist.md
  - skills/proof-first/references/deletion-test.md
  - skills/proof-first/references/worked-examples.md
  - tools/check_repo.py
findings:
  critical: 2
  warning: 2
  info: 1
  total: 5
status: issues_found
---

# Phase 02: Code Review Report (gap-closure round)

**Reviewed:** 2026-09-11T04:58:30Z
**Depth:** standard
**Files Reviewed:** 8
**Status:** issues_found

## Summary

This is a re-review of the state after the 02-07/02-08/02-09 gap-closure round that claimed to
close CR-01, CR-02, CR-03, WR-01, WR-02 from the prior review. I re-ran all three CI gates live
(`--self-test`, `--mutation-test`, plain run) and they pass exactly as claimed (21 codes
discrimination-proven, 0 live violations). The rule catalog itself (31 rules, `NUMBERING.md`,
`checklist.md`, `worked-examples.md`) is internally consistent — every rule title, every ID, and
every next-free-ID computation cross-checks cleanly across all three files, and the 20 worked
✗/✓ pairs all resolve to real, correctly-scoped rule IDs.

However, the 02-08 fix commit (`f04e298`, "correct two overclaiming docstrings") was incomplete:
it fixed the `KNOWN_OPEN_VIOLATIONS` comment, the `_mutate_skill_token_budget_exceeded` function
docstring, and the `MUTATIONS` list description string, but missed a fourth location carrying the
exact same stale claim — the top-of-file module docstring's own `skill-token-budget-exceeded`
paragraph still asserts the check currently fires against the real `SKILL.md`, which is
demonstrably false (confirmed live: 0 violations). I also found a genuine self-contradiction in
`README.md` introduced in the same gap-closure round (worked-examples.md is listed as both
existing and not-yet-existing), a functional bug in `check_repo.py`'s `KNOWN_OPEN_VIOLATIONS`
exclusion logic that silently cannot do what its own instructing comment tells a future
maintainer to do, and a reproducible case (demonstrated live) where `mutation_test()`'s final
summary line prints a misleadingly reassuring count under a `FAILED` banner.

## Critical Issues

### CR-01: Module docstring still claims `skill-token-budget-exceeded` fires against the real SKILL.md — false, and contradicts a comment 60 lines below it in the same file

**File:** `tools/check_repo.py:200-205`
**Issue:** The `skill-token-budget-exceeded` entry in the top-of-file "Violation codes implemented
in this file" docstring ends with:

```
this check uses one stated estimator consistently,
never the more favourable of several. As of this
writing this code fires against this repository's
own skills/proof-first/SKILL.md — a known, tracked,
open finding against CAT-08 (see
.planning/WINDOWS.md), not a defect in this check.
```

This is false. Live verification (word count 3,694 × 1.3 = 4,802 estimated tokens, under the
5,000 ceiling) confirms the check does **not** fire against the real `SKILL.md` — confirmed by
`python3 tools/check_repo.py` reporting `0 violations` and `--mutation-test` reporting `21 codes
discrimination-proven` with a clean control. The 02-08 gap-closure commit (`f04e298`, "correct two
overclaiming docstrings") explicitly fixed three other locations carrying this exact same stale
claim — `KNOWN_OPEN_VIOLATIONS`'s comment block, `_mutate_skill_token_budget_exceeded`'s own
function docstring, and the `MUTATIONS` list's description string for that code — but missed this
fourth location, which is the most prominent one (the module's own top-level docstring, the first
thing a reader or `--help` invocation sees). The result is a direct, in-file self-contradiction:
the `KNOWN_OPEN_VIOLATIONS` comment 60 lines below correctly states "that finding is now closed,"
while this docstring paragraph still says it's "a known, tracked, open finding." This is exactly
the class of overclaiming docstring this project's own constraint ("measured claims or no claims")
exists to prevent, in the one file that is the project's sole enforcement mechanism.
**Fix:**
```
this check uses one stated estimator consistently,
never the more favourable of several. As of 02-07's
trim this check stays silent against this repository's
own skills/proof-first/SKILL.md (3,694 words, an
estimated 4,802 tokens, a 198-token margin under the
5,000-token ceiling) -- see KNOWN_OPEN_VIOLATIONS'
comment for the closed .planning/WINDOWS.md finding
this check previously excused.
```

### CR-02: `README.md` states in the same section that `worked-examples.md` both exists and does not exist yet

**File:** `README.md:26,40`
**Issue:** "What exists today" (line 26) states:

> `skills/proof-first/references/worked-examples.md` — the 20 worked ✗/✓ pairs, keyed by rule ID.

"What does not exist yet" (line 40) states:

> The worked before-and-after examples.

Both lines were touched in the same commit (`0307c8a`, "docs(02-05): record the trigger
pressure-test and correct README's layout claims") — the author added the "exists today" bullet
for the new `worked-examples.md` file but did not remove or rephrase the pre-existing "does not
exist yet" bullet, which was written when neither file existed. The two bullets use near-identical
language ("worked ✗/✓ pairs" vs. "worked before-and-after examples") for what a reader would
reasonably assume is the same artifact, producing a direct self-contradiction in the repository's
own status page. This is defensible only if "the worked before-and-after examples" is meant to
refer exclusively to the still-planned `examples/before-after.md` (visible in the tree diagram
below), but the prose bullet never says so, and nothing distinguishes the two named "worked...
examples" artifacts for a reader who has not also parsed the tree diagram. For a repository whose
entire premise is measured, non-contradictory claims, this is a real defect, not a nitpick.
**Fix:**
```
- The rendered before-and-after example document (`examples/before-after.md`) —
  distinct from `references/worked-examples.md`'s per-rule ✗/✓ pairs, which already exist.
```

## Warnings

### WR-01: `KNOWN_OPEN_VIOLATIONS`'s documented `(code, subject)` tuple usage cannot work with the membership check that consumes it

**File:** `tools/check_repo.py:1061-1063,1394-1397`
**Issue:** The comment above `KNOWN_OPEN_VIOLATIONS` instructs a future maintainer:

> If a future finding needs this set populated again, name the specific `(code, subject)` pair it
> excuses -- e.g. `frozenset({('skill-token-budget-exceeded', 'skills/proof-first/SKILL.md')})` --
> never a bare code.

But the code that actually consumes this constant only ever compares a bare code string:

```python
unexpected_control_violations = [
    v for v in control_violations
    if v[1].split(' ', 1)[0] not in KNOWN_OPEN_VIOLATIONS
]
```

`v[1].split(' ', 1)[0]` is always a bare code string (e.g. `'skill-token-budget-exceeded'`).
Testing a string for membership in a `frozenset` of 2-tuples will never match — Python string
equality against a tuple is always `False`. If a future maintainer follows the comment's own
worked example verbatim, `KNOWN_OPEN_VIOLATIONS` would silently do nothing: every control
violation for that code would still be reported as "unexpected," and `mutation-test CONTROL`
would never go clean for it. This is currently dormant (the set is empty, so nothing is masked
today), but it means the specific safety property this constant exists to provide — narrow,
subject-scoped exclusion instead of a code-wide blanket exclusion — is unimplemented, not just
undocumented. The maintainer's only two live options today are "populate with the documented tuple
format and watch it silently fail to exclude anything" or "populate with a bare code string (which
the comment explicitly warns against, since it re-introduces the exact blanket-masking risk WR-01
of the prior review closed)."
**Fix:** Either implement subject-scoped matching:
```python
unexpected_control_violations = [
    v for v in control_violations
    if (v[1].split(' ', 1)[0], v[0]) not in KNOWN_OPEN_VIOLATIONS
]
```
or, if bare-code exclusion is intentionally retained for simplicity, correct the comment's worked
example to `frozenset({'skill-token-budget-exceeded'})` and drop the "(code, subject)" framing so
the documented usage matches what the code actually does.

### WR-02: `mutation_test()`'s final `FAILED` summary line can read "0 codes not discrimination-proven" while the run is genuinely failing

**File:** `tools/check_repo.py:1445-1448`
**Issue:** When `all_ok` is `False`, the run prints:

```python
failed = len(ALL_CHECK_CODES) - len(discrimination_proven) - len(fire_only)
print(f"mutation-test FAILED: {failed} codes not discrimination-proven")
```

`failed` only counts codes that ended up in neither `discrimination_proven` nor `fire_only`. A
code whose control copy is already non-clean (e.g. from unrelated repository drift — a stray
citation of an undefined ID landing in `README.md` outside this phase's changes) is correctly
classified `FIRE-ONLY` and is *not* counted in `failed`, even though the drift is exactly what
caused `all_ok = False` via the earlier `unexpected_control_violations` check. Reproduced live: I
appended one stray undefined-ID citation to a scratch copy of `README.md` and re-ran
`--mutation-test`; the run correctly exits 1, and the `CONTROL` line and the per-code `FIRE-ONLY`
line both correctly surface the drift — but the final summary line printed
`mutation-test FAILED: 0 codes not discrimination-proven`, which reads as "nothing is wrong with
discrimination" directly under a `FAILED` banner. The full detail is present elsewhere in the
output, so nothing is silently hidden, but the one-line takeaway a reader would scan for is
misleading exactly in the state-drift scenario this function's own docstring says it is designed
to "disclose rather than fail" (or here, disclose why it's failing) honestly.
**Fix:** Fold the unexpected-control-violation count into the failure summary, e.g.:
```python
if all_ok:
    ...
else:
    failed = len(ALL_CHECK_CODES) - len(discrimination_proven) - len(fire_only)
    reasons = []
    if unexpected_control_violations:
        reasons.append(f"{len(unexpected_control_violations)} unexpected control violation(s)")
    if failed:
        reasons.append(f"{failed} code(s) not discrimination-proven")
    print(f"mutation-test FAILED: {'; '.join(reasons) or 'see CONTROL/FIRE-ONLY lines above'}")
```

## Info

### IN-01: `SKILL.md`'s Write-mode register heading is stated once and never repeated where the section promises full specification

**File:** `skills/proof-first/SKILL.md:45,269`
**Issue:** Line 45 promises: "a trailing register under the heading `## Unresolved before this
document is sent`. That register's full column shape is specified in Write mode below." The Write
mode section (lines 261-276) does specify the three-column shape and shows the table, but never
repeats the heading text itself — a reader who lands on Write mode directly (having skipped the
Marker vocabulary section) will not learn the register's required heading text from Write mode
alone, only its column shape. Not a contradiction (the heading is stated once, correctly, at line
45), but the phrase "specified in Write mode below" slightly overpromises what Write mode alone
delivers.
**Fix:** Either repeat the heading text in Write mode's register paragraph, or narrow line 45's
claim to "That register's column shape is specified in Write mode below" (dropping "full").

---

_Reviewed: 2026-09-11T04:58:30Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
