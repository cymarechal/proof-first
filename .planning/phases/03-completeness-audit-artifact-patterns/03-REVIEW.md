---
phase: 03-completeness-audit-artifact-patterns
reviewed: 2026-09-16T00:00:00Z
depth: standard
files_reviewed: 4
files_reviewed_list:
  - evals/conformance/run_conformance.py
  - tools/check_repo.py
  - evals/conformance/RESULTS-mod04.md
  - README.md
findings:
  critical: 1
  warning: 0
  info: 2
  total: 3
status: issues_found
---

# Phase 03: Code Review Report

**Reviewed:** 2026-09-16
**Depth:** standard
**Files Reviewed:** 4
**Status:** issues_found

## Summary

This round closes all four findings from the prior `03-REVIEW.md`. Each is verified below by
reading the code directly (not by trusting the round's own claims) and, where practical, by
executing the tool and by empirically testing the boundary the fix claims to hold:

- **Prior CR-01 (deferred writes / in-memory `lines` accumulator) — genuinely closed.**
  `run_conformance.py`'s `main()` no longer accumulates a `lines` list. `run_matrix()` now writes
  and flushes each session's result line through `_write_result_line()` the moment it is scored,
  and `main()` holds the results file open for the whole run, calling `run_matrix()` with that
  live handle. `git diff 5346c19..HEAD -- evals/conformance/run_conformance.py` confirms the
  refactor is exactly scoped: `score_transcript()` (the 03-09 anchored scorer,
  `FAMILY_LINE_WINDOW_CHARS=400`) and `run_session()`'s `TimeoutExpired` catch/re-raise are
  byte-for-byte untouched. **However, see the new CR-01 finding below** — the offline self-test
  case (case 11) written to prove this durability property does not actually discriminate it.
- **Prior WR-01 (Arm A `no-family` enumeration undercounting by one) — genuinely closed.**
  `RESULTS-mod04.md:756-757` now enumerates all 7 sessions (`A-rfp-answer` x2,
  `B-proposal-section` first attempt, `C-exec-summary` x2, `D-demo-discovery` second attempt,
  `E-ambiguous` second attempt), matching the stated count. I independently summed every
  breakdown bullet in the file (Arm A conformant/no-family, Arm B conformant/no-family) against
  its own parenthetical and all six agree. `check_repo.py`'s new
  `results-breakdown-count-mismatch` check (added this round) now holds this class of defect
  mechanically rather than by hand-correction alone, and `--mutation-test` proves it fires when
  the real file's stated count is raised above its enumeration's sum.
- **Prior WR-02 (case-sensitivity asymmetry between the two family gates) — genuinely closed.**
  `check_skill_family_line_gate()` (`tools/check_repo.py:1547-1590`) now lowercases `body` and
  matches `'artifact family'` / `'no family fits'` case-insensitively, exactly mirroring its
  sibling `check_skill_family_order_gate()`. A new self-test fixture
  (`_capitalized_skill_family_gate()` / `family_capitalized_root`) asserts the line gate stays
  silent against an initial-capitals rewording that would have tripped the old case-sensitive
  code, closing the exact brittleness class the prior review named.
- **Prior IN-01 (stale `skill-token-budget-exceeded` docstring) — genuinely closed.**
  `tools/check_repo.py`'s module docstring (lines 325-328) now states the check "previously
  fired... before the 02-07/02-08 trim (see `.planning/WINDOWS.md` entry 5, status: fixed); it is
  silent against the current tree" — matching `WINDOWS.md` entry 5's actual `fixed` status and
  the live `0 violations` result.

I ran `python3 tools/check_repo.py --self-test`, `--mutation-test`, and a live run, plus
`python3 evals/conformance/run_conformance.py --self-test`; all four pass exactly as claimed
(`mutation-test PASS: 32 codes discrimination-proven`, live `0 violations`). No acceptance claim
in any of the four files rests on the nonexistent `--self-test` `(32 codes)` line the round's own
`03-15-SUMMARY.md` flags as a plan/tool discrepancy — the actual tool output
(`self-test PASS - verified violation codes: ...`) is what every reviewed file relies on.

One new, previously-undiscovered defect was found in this round's own added code: the offline
self-test case written specifically to prove CR-01's fix (durability against process
interruption) does not actually exercise the mechanism it claims to prove. See below.

The five cross-referenced MOD-04 records (`RESULTS-mod04.md`, `WINDOWS.md` entry 8, `README.md`,
`REQUIREMENTS.md` MOD-04, `03-UAT.md` gap G-03-2) all carry the identical figures (Arm A 3/10 =
30.0%, Arm B paired baseline 4/10 = 40.0%, delta -10.0pp), the identical date (2026-09-16), and
the identical human-attributed provenance (the project owner, in an interactive
`/gsd-execute-phase 03 --gaps-only` session) — verified by direct comparison, no drift found.
`README.md`'s prose states both figures plainly (30.0% against a 40.0% baseline) without
spinning the decline as improvement, without omitting a denominator, and without overclaiming
significance at n=10.

## Critical Issues

### CR-01: The offline self-test case added to prove CR-01's durability fix does not actually discriminate the fix from its absence

**File:** `evals/conformance/run_conformance.py:601-668` (self-test case 11), the property it
claims to prove being `_write_result_line()` at lines 719-729

**Issue:** `_write_result_line()` is supposed to make each session's result durable against a
process interruption between sessions (the exact failure mode that has already destroyed two
real measurement runs, per `RESULTS-mod04.md`'s own "Combined result" section: "a Claude Code
session-usage limit, then a Claude Code session teardown"). The mechanism is `handle.write(text);
handle.flush()`. Self-test case 11 is supposed to prove this offline: it calls `run_matrix()`
with a stub `session_fn` that succeeds twice then raises `KeyboardInterrupt` on its third call,
and asserts the first two result lines are already present in the results file after the
`KeyboardInterrupt` propagates.

The problem: `KeyboardInterrupt` is a normal, catchable Python exception. When it propagates out
of `run_matrix()`, it also propagates out of the enclosing `with open(fake_results_path_11, 'a')
as fake_handle_11:` block in the test — and Python's `with` statement calls the file's `__exit__`
(which closes, and therefore flushes, the file) on *any* exception unwind, not only on normal
completion. This means the test would pass identically even if `_write_result_line()` never
called `.flush()` at all: the two already-written lines would still land on disk once the
`with` block's normal close-on-exception runs, with or without the explicit `flush()` call this
fix introduced.

I verified this empirically rather than by inspection alone. Removing the `handle.flush()` line
from a copy of `_write_result_line()` still produces `self-test PASS - verdicts discriminated:
conformant, no-family, rule-before-family, unscoreable` — including case 11 — with no `FAIL`
line:

```
$ python3 /tmp/run_conformance_noflush.py --self-test
self-test PASS - verdicts discriminated: conformant, no-family, rule-before-family, unscoreable
```

I also confirmed the real-world stakes directly: a genuine `SIGKILL` (which is what an external
"harness usage limit" or "session teardown" actually does to a running process — it does not run
Python's exception machinery or `with`-block cleanup at all) *does* distinguish flushed from
unflushed writes:

```
$ python3 /tmp/killtest.py /tmp/noflush.txt noflush   # write, no flush, then os.kill(self, SIGKILL)
$ wc -l < /tmp/noflush.txt
0
$ python3 /tmp/killtest.py /tmp/flush.txt flush       # write, flush(), then os.kill(self, SIGKILL)
$ wc -l < /tmp/flush.txt
1
```

So the `.flush()` call in the shipped `_write_result_line()` is doing genuinely necessary work
against the actual production threat model (a hard process kill) — but self-test case 11 uses a
soft, catchable exception that the `with`-block's own cleanup already survives on its own,
so the test cannot fail even if a future edit silently deletes the `.flush()` call and
reintroduces the exact data-loss defect this fix exists to close. This is precisely the failure
mode this project's own mutation-testing section names as the thing it exists to prevent: "a
dead check ship[ping] named as covered" (`tools/check_repo.py`'s own mutation-testing preamble,
citing `01-VERIFICATION.md`) — here reproduced in the sibling instrument's self-test rather than
in `check_repo.py` itself.

The production code is not defective today (the `.flush()` call is present and correct). This is
a verification-integrity gap: the offline proof this file's own module docstring cites
("Durability guarantee... proved offline by `--self-test` behavior case 11") is not actually
proof of the property it names, so a future regression of the exact bug that has already struck
this project twice would ship silently, with CI green.

**Fix:** Test the flush discipline directly against a call-recording stub, not against real
filesystem state that a context-manager's ordinary exception cleanup can produce on its own. For
example, replace the real `open()`/`with` around case 11's `run_matrix()` call with a thin proxy
that records call order:

```python
class _FlushTrackingHandle:
    """Wraps a real writable handle, recording write/flush call order so a
    test can assert every write is immediately followed by a flush --
    independent of whatever a context manager's own close() does on exit."""
    def __init__(self, real_handle):
        self._real = real_handle
        self.calls = []  # e.g. ['write', 'flush', 'write', 'flush', 'write']

    def write(self, text):
        self.calls.append('write')
        return self._real.write(text)

    def flush(self):
        self.calls.append('flush')
        return self._real.flush()

# ... inside case 11, before the interrupting call:
tracked_handle_11 = _FlushTrackingHandle(fake_handle_11)
run_matrix(..., handle=tracked_handle_11, session_fn=_stub_session_fn)
...
# Assert every 'write' is immediately followed by 'flush' -- the actual
# durability discipline, checkable even if run_matrix is later refactored
# to hold the file open across an uncatchable interruption where no
# context-manager __exit__ would ever run.
paired = list(zip(tracked_handle_11.calls[::2], tracked_handle_11.calls[1::2]))
if not all(pair == ('write', 'flush') for pair in paired):
    print(f'FAIL: behavior case 11 expected strict write/flush pairing, got {tracked_handle_11.calls}')
    all_ok = False
```

This makes the test fail the moment `.flush()` is removed from `_write_result_line()`,
independent of whether the interrupting exception happens to be one a `with` block's own cleanup
would have masked anyway.

## Info

### IN-01: `_copy_repo_subset()`'s comment asserts "no existing check reads anything under evals/" in the same breath as describing the check that does

**File:** `tools/check_repo.py:1869-1878`

**Issue:** The comment justifying `MUTATION_SOURCES`'s widening to include `'evals'` says: "'evals'
was added by 03-14 so the real `evals/conformance/RESULTS-mod04.md` is reachable from the
mutation harness, making `results-breakdown-count-mismatch` discrimination-proven... No existing
check reads anything under `evals/`... so widening this copy does not change what any other code
fires against." Read literally, this is self-contradictory: `check_results_breakdown_count()`
(introduced in this same round) reads exactly `evals/conformance/RESULTS-mod04.md`. The
intended meaning is almost certainly "no *other* check reads under `evals/`" (true — verified:
`check_undefined_id`'s roots are `skills/`, `examples/`, `README.md`; `check_unlisted_figure`'s
`UNLISTED_FIGURE_SCAN_ROOTS` is `('examples', 'skills')`; neither touches `evals/`), but as
written a future maintainer skimming this comment could read it as claiming the new check itself
doesn't read `evals/`, which is false.

**Fix:** Say "other" explicitly: "No check other than `results-breakdown-count-mismatch` itself
reads anything under `evals/`..."

### IN-02: README's decline is stated in full but never named as a decline

**File:** `README.md:53-56`

**Issue:** The Status section states both figures plainly and correctly — "`claude-sonnet-5`
conformed in 3 of 10 scoreable sessions (30.0%), against a paired same-instrument baseline of the
immediately prior skill version at 4 of 10 (40.0%)" — with accurate denominators, an accurate
date, and no overclaimed significance. This is not a defect: the two numbers as stated are
sufficient for any reader to compute that the newer version scored 10 points lower than its own
predecessor. It is, however, the one place in the four-record chain that never uses the word
"decline" (contrast `RESULTS-mod04.md`'s "the honest finding is a decline, not merely flat
movement" and `WINDOWS.md` entry 8's "the honest finding is a decline, not merely flat
movement"). A reader who does not do the arithmetic could parse "against a...baseline...at 4 of
10 (40.0%)" as neutral context rather than a worse result.

**Fix:** One clause would close the gap without adding a new claim, e.g.: "...a 10-point decline
against a paired same-instrument baseline of the immediately prior skill version at 4 of 10
(40.0%)."

---

_Reviewed: 2026-09-16_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
