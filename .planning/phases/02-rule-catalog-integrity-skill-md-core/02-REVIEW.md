---
phase: 02-rule-catalog-integrity-skill-md-core
reviewed: 2026-09-20T00:00:00Z
depth: standard
files_reviewed: 7
files_reviewed_list:
  - evals/trigger/run_trigger_test.py
  - evals/trigger/stats.py
  - .github/workflows/ci.yml
  - .gitignore
  - evals/trigger/DECISION-RULE-cat10.md
  - evals/trigger/RESULTS-trigger.md
  - evals/trigger/INIT-EVENTS.md
findings:
  critical: 1
  warning: 3
  info: 2
  total: 6
status: issues_found
---

# Phase 02: Code Review Report (gap-closure round, plan 02-10)

**Reviewed:** 2026-09-20
**Depth:** standard
**Files Reviewed:** 7
**Status:** issues_found

## Superseded reviews

An earlier review round (2026-09-11) exists in git history for this same `02-REVIEW.md` path,
against a **different** file set (`NUMBERING.md`, `README.md`, `evals/pressure-tests.md`,
`skills/proof-first/SKILL.md`, two `references/` files, and `tools/check_repo.py`) — 5 findings
(2 critical, 2 warning, 1 info; IDs CR-01, CR-02, WR-01, WR-02). That round's record is preserved
at git commit `e950e3c` and is **not** re-litigated here. Read it with:

```
git show e950e3c:.planning/phases/02-rule-catalog-integrity-skill-md-core/02-REVIEW.md
```

This review is a fresh round, scoped only to the files plan 02-10 touched (`git diff
6ca3342..HEAD`), per the workflow's gap-closure scope note. `evals/trigger/transcripts-cat10.tar.gz`
is out of scope by explicit instruction.

## Summary

`stats.py` is new this round and is mathematically sound: both `clopper_pearson_upper` and
`fisher_exact_two_tailed` were independently re-run against the module's own inputs
(`fisher_exact_two_tailed(9, 16, 0, 25)` reproduces the `p_attr = 0.0016` cited in
`DECISION-RULE-cat10.md`; `clopper_pearson_upper(0, 5)` reproduces `0.4507`), and every number
quoted in `RESULTS-trigger.md` and `DECISION-RULE-cat10.md` was cross-checked by re-summing the
per-row `k of n` cells and matches the published `OF`/`SN`/`MH`/`SM` totals exactly. No code path
in either file emits a percentage; the self-test explicitly asserts against that
(`run_trigger_test.py:413`). The live `SKILL.md` head-14 hash on disk matches the pre-round hash
recorded as the reverted target, confirming Branch 4's revert was actually applied.

The defects found are not in the numbers already published — they are in control-flow paths the
self-tests do not exercise: a fail-open scope-hash guard, a TOCTOU window in the overwrite guard,
duplicated total-aggregation logic, and missing validation on `--repeats`.

## Critical Issues

### CR-01: Scope-hash mismatch halt fails open when no hash is recorded, and its regex is not scoped to the Scope section

**File:** `evals/trigger/run_trigger_test.py:88-91, 540-545`

**Issue:** The entire safety property this instrument depends on — "an observation recorded
against a different description is not an observation of these rows, so a mismatch halts" (the
file's own docstring, lines 70-73) — is enforced by:

```python
bound_hash = recorded_scope_hash(md_text)
if bound_hash and bound_hash != live_hash:
    print('ERROR: ...')
    return 1
```

`recorded_scope_hash` returns `None` whenever its regex (`r'\b([0-9a-f]{64})\b'`, applied to the
*whole* markdown document, not scoped to the `## Scope` heading) fails to find a 64-hex-char
token. When it returns `None`, the guard condition `bound_hash and ...` is falsy and the halt is
**silently skipped** — the script proceeds to run live sessions against `pressure-tests.md` with
no verification that the rows are bound to the live `SKILL.md` description at all. This is a
fail-open design: the safety check activates only when a hash happens to be present and
well-formed, not when the binding is absent, malformed, or (a second, independent risk) when a
different 64-hex-char token earlier in the document is picked up instead of the one under the
Scope heading. Currently `evals/pressure-tests.md` contains exactly one such token, so the defect
is latent rather than triggered — but the entire point of a pre-committed instrument surviving
future edits is that a later, unrelated edit to that file (e.g. adding another sha256 reference,
or a formatting change that breaks the regex match) must not silently disable the halt it exists
to provide. A measurement run under a silently-disabled guard is exactly the "measured claims or
no claims" failure this project is built to prevent.

**Fix:** Require a hash to be present and matched, and scope the regex to the `## Scope` section
rather than the whole document:

```python
def recorded_scope_hash(md_text):
    scope = re.search(r'^##\s+Scope\s*$(.*?)(?=^##\s|\Z)', md_text, re.M | re.S)
    if not scope:
        return None
    match = re.search(r'\b([0-9a-f]{64})\b', scope.group(1))
    return match.group(1) if match else None
```

```python
bound_hash = recorded_scope_hash(md_text)
if bound_hash is None:
    print('ERROR: %s has no Scope-hash binding recorded; rows cannot be trusted to be '
          'bound to the live description. Add the sha256 to the Scope section before '
          'running.' % args.tests, file=sys.stderr)
    return 1
if bound_hash != live_hash:
    print('ERROR: ...')
    return 1
```

## Warnings

### WR-01: Overwrite guard is checked once at the start of a (potentially long) run, not immediately before the write — a TOCTOU window that can still silently clobber

**File:** `evals/trigger/run_trigger_test.py:547-557, 596-620`

**Issue:** `resolve_out_mode()` is invoked once, before `harness_version` is fetched and before any
live session runs (line 549). Its own docstring calls this "the accident that would otherwise
destroy the 2026-09-20 measurement." But for a `--repeats 5` round like the one this file
documents, the gap between that check and the actual write (`write_text` at line 620, or the
`write_results()` call in the legacy branch) spans the full wall-clock time of up to 70 live
`claude -p` sessions per arm — potentially tens of minutes. If `--out` did not exist or was empty
at check time (`out_mode == 'write'`), nothing re-verifies that state immediately before the final
`pathlib.Path(args.out).write_text(block + '\n', ...)` at line 620. Content written to that path
during the run (by a concurrent process, or a human editing the file while sessions are still
in flight) is silently destroyed by that unconditional `write_text()` call, contradicting the
guard's stated purpose. The append branch (`open(args.out, 'a', ...)` at line 615-618) is not
subject to this risk since it never truncates.

**Fix:** Re-check immediately before the write, not only at the top of `main()`:

```python
if out_mode == 'write' and out_path.exists() and out_path.stat().st_size > 0:
    print('ERROR: %s gained content after this run started; re-run with --append.' % args.out,
          file=sys.stderr)
    return 1
```

### WR-02: OF/SN/MH/SM totals are computed twice, once inside `render_run_block` and once again in `main()`, from the same inputs

**File:** `evals/trigger/run_trigger_test.py:279-286` (inside `render_run_block`) and
`evals/trigger/run_trigger_test.py:622-625` (inside `main()`)

**Issue:** `render_run_block()` already computes `of_total`, `sn_total`, `mh_total`, `sm_total` and
writes them into the "### Totals" section of the persisted block (lines 279-286, 299-307). `main()`
then independently recomputes the identical four sums from the same `rows`/`counts` via a second,
differently-written expression (`sum(c[0] for r, c in zip(rows, counts) if not r[2])`, etc., lines
622-625) purely to print them to the console. The two computations happen to agree today because
both correctly key off `expects_fire`, but they are two hand-written copies of the same aggregation
with no shared source of truth — exactly the "second copy that creates a place for two numbers to
silently drift apart" pattern this project's own documentation (e.g.
`DECISION-RULE-cat10.md`'s Scope section, `INIT-EVENTS.md`'s "not reproduced a second time here")
explicitly calls out as the failure mode to avoid.

**Fix:** Have `render_run_block()` return the totals alongside the block text (or expose a small
`totals(rows, counts)` helper used by both call sites) instead of recomputing them in `main()`:

```python
def totals(rows, counts):
    of_total = sum(c[0] for r, c in zip(rows, counts) if not r[2])
    sn_total = sum(c[1] for r, c in zip(rows, counts) if not r[2])
    mh_total = sum(c[0] for r, c in zip(rows, counts) if r[2])
    sm_total = sum(c[1] for r, c in zip(rows, counts) if r[2])
    return of_total, sn_total, mh_total, sm_total
```
called once, and its result passed into `render_run_block()` as well as used for the console print.

### WR-03: `--repeats` accepts 0 or negative values with no validation, silently producing a vacuous run block

**File:** `evals/trigger/run_trigger_test.py:517-518` (`parser.add_argument('--repeats', ...)`),
used at lines 567, 573, 594-599

**Issue:** `--repeats` is declared as `type=int` with no range check. `--repeats 0` (or a negative
value) makes `range(args.repeats)` empty for every row, so `tasks = []`, no live sessions run, and
`aggregate_verdicts([])` returns `(0, 0)` for every row. The script does not error: it proceeds to
either the legacy branch (which would crash on `verdicts_by_row[i][0]` — an `IndexError` on an
empty list, since line 599 indexes element `[0]` of what is now an empty per-row list) or, if
`--append`/`repeats != 1`, silently writes/appends a "Sessions planned: 0" block with every row
marked `unscoreable`. The legacy-branch crash path is an unhandled `IndexError` with no actionable
message; the append path silently pollutes `RESULTS-trigger.md` with a content-free run block.

**Fix:**
```python
parser.add_argument('--repeats', type=int, default=1,
                    help='sessions to run per phrasing, aggregated into one k-of-n row (default 1)')
...
if args.repeats < 1:
    print('ERROR: --repeats must be >= 1', file=sys.stderr)
    return 1
```

## Info

### IN-01: `detect_activation` assumes a truthy `tool_use` `input` field is always a dict

**File:** `evals/trigger/run_trigger_test.py:151`

**Issue:** `skill = (block.get('input') or {}).get('skill', '')` guards against `input` being
absent or `None`/falsy, but not against `input` being present and non-empty but not a `dict` (e.g.
a bare string, if a future harness version or a malformed transcript line ever emits one). In that
case `.get('skill', '')` raises `AttributeError`, which is not caught anywhere between here and
`concurrent.futures.ThreadPoolExecutor.map()` in `main()` (line 585) — the exception surfaces when
the pool's results are consumed and aborts collection of the *entire* batch, discarding verdicts
for whichever other sessions in that `--repeats` batch had already completed. Given this project
runs batches of up to 70+70 live sessions per round, a single malformed event would be an expensive
way to lose an otherwise-complete measurement.

**Fix:**
```python
raw_input = block.get('input')
skill = raw_input.get('skill', '') if isinstance(raw_input, dict) else ''
```

### IN-02: The Clopper-Pearson bound column is emitted for any zero-fire row, including must-fire rows, without a note on what it means there

**File:** `evals/trigger/run_trigger_test.py:295` (`render_run_block`)

**Issue:** `bound = '%.4f' % stats.clopper_pearson_upper(0, scoreable) if (fires == 0 and
scoreable > 0) else '-'` is computed identically regardless of `expects_fire`. This is
mathematically correct (the math doesn't care which direction is "good"), and it is exactly what
produced the `0.4507` entry for the must-fire regression row in `RESULTS-trigger.md`'s Arm A block
(the "We're putting together our bid response..." row). But the column header
("Clopper-Pearson upper bound (alpha 0.05)") reads, without context, as reassurance about a low
rate — which is the wrong framing for a must-fire row where a low fire rate is the defect, not the
result being bounded away from. `DECISION-RULE-cat10.md`'s prose correctly explains this
particular row in words, but the mechanism generating the table itself carries no such
disambiguation, so a reader of a future run relying on the table alone (rather than the
accompanying prose) could misread the bound's direction of concern for a must-fire row.

**Fix:** Either suppress the bound for must-fire rows (since the interesting statistic there is the
`k of n` count itself, not an upper bound on its own failure rate) or label the column
directionally, e.g. `'%.4f (upper bound on true fire rate)' % ...` with a one-line legend noting
that for must-fire rows a *low* bound is the failure mode.

---

_Reviewed: 2026-09-20_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
