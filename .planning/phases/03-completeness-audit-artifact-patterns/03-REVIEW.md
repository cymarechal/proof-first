---
phase: 03-completeness-audit-artifact-patterns
reviewed: 2026-09-17T00:00:00Z
depth: standard
files_reviewed: 4
files_reviewed_list:
  - evals/conformance/run_conformance.py
  - evals/conformance/RESULTS-mod04.md
  - tools/check_repo.py
  - README.md
findings:
  critical: 0
  warning: 0
  info: 1
  total: 1
status: issues_found
---

# Phase 03: Code Review Report (round 6)

**Reviewed:** 2026-09-17
**Depth:** standard
**Files Reviewed:** 4
**Status:** issues_found (1 Info, pre-existing, unrelated to this round's fix)

## Summary

This round's diff (`53ce63a`, `d744b3c`, `82535c7`, `aac27be` on top of `8ec67a0`) rewrites
`--self-test` behavior case 11 in `run_conformance.py` around a `_FlushTrackingHandle` proxy,
corrects two documents that had overclaimed the old case 11's proof, and closes two prior-round
Info findings (IN-01 in `tools/check_repo.py`, IN-02 in `README.md`).

**The central question — does the rewritten case 11 genuinely discriminate — is answered yes, by
direct reproduction, not by trusting the SUMMARY.** I copied `run_conformance.py` to a sibling
path inside `evals/conformance/`, mechanically removed the `handle.flush()` line from
`_write_result_line()`, and ran `--self-test` on the copy:

```
$ python3 evals/conformance/run_conformance_mutation_test_tmp.py --self-test
FAIL: behavior case 11 (durability on interruption) expected recorded call sequence
['write', 'flush', 'write', 'flush'], actual ['write', 'write']
exit=1
```

The unmutated original still passes cleanly:

```
$ python3 evals/conformance/run_conformance.py --self-test
self-test PASS - verdicts discriminated: conformant, no-family, rule-before-family, unscoreable
exit=0
```

Both temp files were deleted immediately after (`rm -f`, confirmed no `git status` residue). The
regression the previous two rounds found — a `KeyboardInterrupt` caught inside the same `with`
block whose own close()-on-exit flushed the file regardless of the explicit flush call — is gone.

I went one step further than the mandated reproduction and probed whether the new assertion is
merely checking that *a* call named `flush` happened, or that the call actually reached the real
handle. I mutated `_FlushTrackingHandle.flush()` to record the call but not forward it
(`return None` instead of `return self._real.flush()`) and reran `--self-test`:

```
$ python3 evals/conformance/run_conformance_proxy_test_tmp.py --self-test
FAIL: behavior case 11 (durability on interruption) expected exactly 2 "| verdict=" lines already
on disk before close, found 0: ''
exit=1
```

This confirms the second assertion (the pre-close read of the results file) is load-bearing, not
decorative: a proxy that fakes the flush without forwarding it is caught by the on-disk read, not
just by the call-sequence check. Both of case 11's two assertions are independently necessary and
both are proven to fire. Temp file deleted after, `git status --porcelain` clean.

I also reasoned through (without needing a further reproduction) the remaining sub-questions from
the review brief:

- **Proxy soundness (no `__getattr__`).** `run_matrix()` and `_write_result_line()` call only
  `.write()` and `.flush()` on the handle they're given; case 11's own harness only additionally
  reads `.calls` (an attribute the proxy defines) and separately reads the file by path (not
  through the handle). No code path today reaches any other method on the results handle, so the
  proxy's narrow interface is safe for the current call graph, exactly as its docstring claims.
- **Sequence brittleness.** The interrupt condition is `call_count_11['n'] >= 3`, not `== 3`, so a
  future bump to `repeats` would not silently produce a passing-but-meaningless test — the
  interruption still lands on the third call regardless of how many are configured, and a
  `repeats` value below 3 would fail loudly on the "expected KeyboardInterrupt, none raised"
  branch rather than passing quietly.
- **Statement correction (IN-01, `tools/check_repo.py`).** The diff changes
  `_copy_repo_subset()`'s docstring from "No existing check reads anything under `evals/`" to "No
  check other than `results-breakdown-count-mismatch` itself reads anything under `evals/`". I
  confirmed the corrected claim against the code: `check_undefined_id`'s roots are `skills/`,
  `examples/`, `README.md`; `check_unlisted_figure`'s roots are `examples/`, `skills/`; only
  `check_results_breakdown_count` reads `evals/conformance/RESULTS-mod04.md`. The correction is
  accurate, not merely different.
- **README wording (IN-02).** The diff adds "— a 10-point decline" before the existing "against a
  paired same-instrument baseline ... at 4 of 10 (40.0%)" clause. 40.0% − 30.0% = 10.0 points —
  the clause states an already-present number's arithmetic in a word, introduces no new figure,
  and changes none of the surrounding text.
- **Figure integrity.** `N_A=3, M_A=10` (30.0%), `N_B=4, M_B=10` (40.0%), delta −10.0pp, date
  2026-09-16 appear identically in `README.md`, `RESULTS-mod04.md`, `.planning/WINDOWS.md` (entry
  8, both the table row and its JSON block), `.planning/REQUIREMENTS.md` (`MOD-04`), and
  `03-UAT.md`. No drift found.
- **`check_repo.py` integrity.** Ran all three modes directly:
  `--self-test` → `self-test PASS - verified violation codes: ...` (32 codes named), exit 0;
  `--mutation-test` → `mutation-test PASS: 32 codes discrimination-proven`, exit 0; bare run →
  `check_repo: 0 violations`, exit 0. `ALL_CHECK_CODES` sums to 32 (4+3+3+1+1+1+1+4+14) matching
  the mutation-test count. The absence of a `(32 codes)` string in the self-test output line is
  expected per the review brief, not a defect.
- **Zero-dependency constraint.** Both Python files import only stdlib modules
  (`argparse`, `datetime`, `json`, `pathlib`, `re`, `shutil`, `subprocess`, `sys`, `tempfile` /
  `argparse`, `re`, `shutil`, `sys`, `tempfile`, `pathlib`). See the one Info finding below for a
  dead import inside that list.

Module docstring and `RESULTS-mod04.md`'s new `## Self-test discrimination correction (03-16)`
section were checked line by line against the code and against my own reproduction above; every
claim in both (the defect, the provenance, the fix, the residual, the figures that do not move)
matches what I independently observed. No overclaiming found this round.

## Info

### IN-03: Unused `json` import in `run_conformance.py`

**File:** `evals/conformance/run_conformance.py:55`
**Issue:** `import json` is declared (and named in the module docstring's stdlib-only list) but
`json` is never referenced anywhere in the file (`grep -n "json\."` finds no call sites). This
predates the round under review — `git diff 8ec67a0..HEAD` does not touch the import block — so
it is not a regression introduced by `03-16`, but it is present in the file as currently reviewed
and is a small piece of dead code worth clearing the next time this file is touched.
**Fix:** Remove the unused `import json` line (and its mention in the docstring's import list) in
a future edit to this file. Not urgent enough to warrant a standalone plan.

---

_Reviewed: 2026-09-17_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
