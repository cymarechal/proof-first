---
phase: 05-evaluation-harness
reviewed: 2026-09-20T01:57:01Z
depth: standard
files_reviewed: 7
files_reviewed_list:
  - evals/lint.py
  - evals/benchmark/run_benchmark.py
  - evals/proxy-sources.md
  - evals/benchmark/scenarios.json
  - evals/benchmark/bench-deal-brief.md
  - evals/benchmark/RESULTS.md
  - .github/workflows/ci.yml
findings:
  critical: 4
  warning: 4
  info: 1
  total: 9
status: issues_found
---

# Phase 05: Code Review Report

**Reviewed:** 2026-09-20T01:57:01Z
**Depth:** standard
**Files Reviewed:** 7
**Status:** issues_found

## Summary

`evals/lint.py` is careful, well-disclaimered, and its self-test genuinely exercises every violation code and every provenance-check branch — no findings there. `evals/proxy-sources.md`, `evals/benchmark/scenarios.json`, `evals/benchmark/bench-deal-brief.md`, and `.github/workflows/ci.yml` are all internally consistent (canonical figures trace correctly, no live-model call reaches CI, no entity/vocabulary leakage found beyond what the file's own self-test already checks).

`evals/benchmark/run_benchmark.py` is where the real risk lives. Four issues there are classified Critical because they each let a number in a future `RESULTS.md` diverge from what its own prose claims, or from what an operator believes they measured — exactly the failure class this phase's own constraints (`byte-stable render`, `no silent skip`, `measured claims or no claims`) exist to prevent. None of the four manifest in the *currently committed* `RESULTS.md` (0 excluded pairs, 0 unscoreable judgements, single effort level used throughout) — that is what makes them dangerous: they are unexercised paths that will fire silently on some future live run, with no test in `self_test()` currently guarding against any of them.

## Critical Issues

### CR-01: `--report-only` is not byte-stable across days — violates the module's own documented determinism guarantee

**File:** `evals/benchmark/run_benchmark.py:1252-1253` (default computed inside `generate_report()`), invoked with no override from `main()`'s `--report-only` branch at `evals/benchmark/run_benchmark.py:2232-2239`

**Issue:** `build_results_md()` is genuinely pure and its own docstring is accurate in isolation: *"Calling this twice on identical input returns byte-identical strings ... there is no timestamp-at-render-time or randomness anywhere in this function; every date-shaped value is an explicit parameter."* But the actual CLI entry point operators use — `python3 evals/benchmark/run_benchmark.py --report-only`, exactly as documented in the module's own Usage docstring (lines 32-36) — calls `generate_report(raw_dir=args.raw_dir, out_path=args.out)` with **no `as_of_date` argument**, and there is **no `--as-of-date` flag** anywhere in `main()`'s `argparse` setup (lines 2198-2226). `generate_report()` then falls back to `datetime.datetime.now(datetime.timezone.utc).date().isoformat()` (line 1253) — a live clock read.

Consequence: running `--report-only` twice on two different days against an *unchanged* `raw/` directory produces two different `RESULTS.md` files (differing in the first line's date), even though nothing about the underlying data changed. This is precisely the failure mode the project's determinism constraint names — "Report rendering must be byte-stable ... no clock/random in the render path" — except the clock read happens one call frame above the function the docstring makes its guarantee about. The `git diff --exit-code` check mentioned as already passing only proves today's regeneration matches today's commit; it says nothing about tomorrow's regeneration of the same data.

**Fix:** Add a `--as-of-date` CLI flag (defaulting to `None`) and thread it through to `generate_report()`, or better, require the caller to pass a value explicitly derived from the *data* (e.g. the max `timestamp` across loaded records) rather than wall-clock `now()`:
```python
parser.add_argument('--as-of-date', default=None,
                     help='Pin the rendered "Measured ..." date (default: max record timestamp).')
...
if args.report_only:
    text = generate_report(raw_dir=args.raw_dir, out_path=args.out, as_of_date=args.as_of_date)
```
and in `generate_report()`, derive the fallback from data rather than `now()`:
```python
if as_of_date is None:
    as_of_date = max(r['timestamp'] for r in records if 'timestamp' in r)[:10]
```

---

### CR-02: `aggregate()`'s "Judged persuasion" means can include an un-paired, position-bias-uncorrected score, contradicting the "Honest caveats" claim

**File:** `evals/benchmark/run_benchmark.py:1048-1082` (the `judged_scores` pooling loop inside `aggregate()`), contrasted with `average_orders()` at `evals/benchmark/run_benchmark.py:849-875` and `judge_summary()` at `evals/benchmark/run_benchmark.py:878-937`; the contradicted claim is `CAVEAT_TEXT['position bias']` at `evals/benchmark/run_benchmark.py:490-495`.

**Issue:** The "Honest caveats" section states, unconditionally: *"every judged pair is scored in both orders ... and the two orders are averaged per dimension before this report reads them -- that averaging is what cancels position bias, not merely a disclosure that it exists."*

That statement is only true of the win/tie/loss table (built via `judge_summary()` → `average_orders()`, which correctly returns `None` — excluding the pair entirely, counted in `excluded_pairs` — when either order is missing or not `verdict == 'scored'`).

It is **not** true of the "Judged persuasion" mean/range table. `aggregate()`'s judged loop iterates every *individual judgement record* (one record = one order) independently:
```python
for record in records:
    if 'judge_model' not in record:
        continue
    if record.get('verdict') != 'scored':
        continue
    ...
    bucket[condition][dim].append(dim_scores[condition])
```
There is no check here that the record's sibling order (order 1 or 2 for the same `model`/`scenario_id`/`repeat`) is also present and scored. If order 1 for a pair succeeds and order 2 fails (`SessionFailedError`, or a malformed reply caught by `_validate_judge_reply`), `judge_summary()` correctly drops that entire pair from win/tie/loss (`excluded_pairs += 1`), but `aggregate()` will still pool order 1's raw, unmatched score straight into the "Judged persuasion" mean — a score that carries whatever position bias exists between labeling a text A vs. B, with no swap to cancel it. The mean/range table and the win/tie/loss table can therefore silently disagree about which pairs contributed data, and the caveat's blanket claim is false for any run where this happens. No `self_test()` case currently exercises "one order scored, sibling order for the same pair unscoreable" through `aggregate()`; the existing `judge-missing-dimension-unscoreable` self-test case uses two records with the *same* order (both `order=1`), which only proves an unscoreable record contributes nothing — it does not exercise the partial-pair case.

**Fix:** Pair orders before pooling into `judged_scores`, using the same `average_orders()` logic `judge_summary()` already has, and skip pairs where `average_orders()` returns `None`:
```python
by_pair = {}
for record in records:
    if 'judge_model' not in record:
        continue
    by_pair.setdefault((record['model'], record['scenario_id'], record['repeat']), {})[record['order']] = record

for (model, scenario_id, _repeat), orders in by_pair.items():
    averaged = average_orders(orders.get(1), orders.get(2))
    if averaged is None:
        continue
    key = (model, scenario_id)
    bucket = judged_scores.setdefault(key, {...})
    for dim in JUDGE_DIMENSIONS:
        for condition in ('skill-on', 'skill-off'):
            bucket[condition][dim].append(averaged[dim][condition])
```

---

### CR-03: `effort` and `judge_model`/`judge_effort` are not part of the raw-record resumability key or the rendered report — a re-run with different settings can silently mix configurations

**File:** `raw_path_for_generation` at `evals/benchmark/run_benchmark.py:190-198`, `raw_path_for_judgement` at `evals/benchmark/run_benchmark.py:201-204`, the `aggregate()` mechanical grouping key at `evals/benchmark/run_benchmark.py:1035`, and the whole of `build_results_md()` at `evals/benchmark/run_benchmark.py:1093-1224` (no effort/judge-model column or headline mention anywhere).

**Issue:** The frozen filename templates that back the "skip-if-exists" resumability guarantee are keyed only on `model`/`condition`/`scenario_id`/`repeat` (generation) and `model`/`scenario_id`/`repeat`/`order` (judgement). `effort` (a `--effort` CLI flag), and `judge_model`/`judge_effort` (`--judge-model`/`--judge-effort` CLI flags) are **not** part of either key.

Concretely: run the live matrix once at `--effort low` (the default), producing 96 raw files. Later, run it again at `--effort xhigh` intending to measure a different effort level. Every cell's raw file already exists from the first run, so `run_generation()`'s `if path.exists(): return ..., False` fires for all 96 cells — **zero new sessions are run**, and the operator's `--effort xhigh` invocation silently reports on `low`-effort data. The same applies to `--judge-model`/`--judge-effort` overrides against an existing `raw/`.

Worse, `build_results_md()` never surfaces which effort or judge-model/effort actually produced the numbers in the table — the headline sentence names only models and a generation count (`Measured {date} across {models} ({N} generations recorded)`), and neither results table has an effort column. So even after the fact, a reader of `RESULTS.md` has no way to detect that a mix of effort levels (or judge models) went into a mean, or even that the wrong effort was measured.

**Fix:** Include `effort` in `raw_path_for_generation`'s filename and `aggregate()`'s mechanical key; include `judge_model`/`judge_effort` in `raw_path_for_judgement`'s filename (or at minimum assert-and-fail loudly if an existing record's stored `effort`/`judge_model`/`judge_effort` field disagrees with the current invocation's arguments before treating it as reusable). Surface the effort level(s) and judge model/effort actually present in the loaded records in the headline sentence or as an explicit column, and raise if `aggregate()` observes more than one distinct effort value for a project claiming a single measured configuration.

---

### CR-04: A cell whose every generation attempt fails is silently dropped from "Mechanical proxy counts" with no disclosure — unlike the judgement path

**File:** the `mechanical_counts` loop inside `aggregate()` at `evals/benchmark/run_benchmark.py:1029-1046`, rendered at `evals/benchmark/run_benchmark.py:1137-1149`; contrast with the judgement-side disclosure at `evals/benchmark/run_benchmark.py:1196-1204`.

**Issue:** `aggregate()`'s mechanical loop only creates a `(model, scenario_id, condition)` entry in `mechanical_counts` when at least one record for that key has `verdict == 'generated'`. If *every* repeat for a given cell comes back `unscoreable` (empty text, session failure, budget cap hit, etc.), that key is never created, and `build_results_md()`'s "Mechanical proxy counts" table simply has no row for it — indistinguishable from a cell that was never in scope.

This is asymmetric with the judgement half of the same report: `judge_summary()` collects `unscoreable` judgement records regardless of grouping and `build_results_md()` explicitly renders `Unscoreable judgements: {N}` (with a reason breakdown) even when a whole pair never gets a table row. There is no equivalent `Unscoreable generations: {N}` line anywhere in `build_results_md()`. A reader cannot tell "this scenario/condition/model combination scored 0 mechanical violations because it wasn't run" from "this combination is entirely missing from the table because every attempt failed" — the two look identical (absence), and only one of them should look like anything is wrong. The project's own review-scope language calls this out directly: *"a silently dropped record means a published number computed from less data than it claims."* Here it's not one record but a whole reported cell.

**Fix:** Track and render generation-side unscoreable counts symmetrically with the judgement side:
```python
unscoreable_generations = [
    r for r in records
    if 'judge_model' not in r and r.get('verdict') != 'generated'
]
...
lines.append(f'Unscoreable generations: {len(unscoreable_generations)}.')
```
and/or emit an explicit `(n=0)` row (or a footnote naming the cell) for any `(model, condition, scenario_id)` combination expected from the matrix but absent from `mechanical_counts`.

## Warnings

### WR-01: `_write_json_atomic()` is not actually atomic — a killed process can leave a corrupt raw file that crashes the next resumed run

**File:** `evals/benchmark/run_benchmark.py:139-149`
**Issue:** The function name and its docstring ("pathlib.Path.write_text() opens, writes, and closes in one call") both imply atomicity, but the implementation is a single, non-atomic `path.write_text(...)` call — no write-to-temp-file-then-`os.replace()` pattern. For a long-running, paid, resumable matrix (the exact use case `run_matrix`'s durability documentation targets), a process kill (Ctrl-C at the wrong instant, OOM kill, machine restart) mid-write can leave a truncated/corrupt JSON file on disk. On the next invocation, `run_generation()`'s `if path.exists(): return json.loads(path.read_text(...)), False` will attempt to parse that corrupt file, raising an unhandled `json.JSONDecodeError` — a type `run_matrix`'s `except SessionFailedError:` handler does not catch — crashing the entire resumed run instead of simply regenerating that one cell.
**Fix:**
```python
def _write_json_atomic(path, record):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding='utf-8')
    tmp.replace(path)
```

### WR-02: `DISALLOWED_TOOLS` omits `WebSearch`/`WebFetch`/`Read`/`Glob`/`Grep`, contradicting the project's own documented benchmark-hygiene requirement

**File:** `evals/benchmark/run_benchmark.py:63`, used at `evals/benchmark/run_benchmark.py:294-301` (generation) and `evals/benchmark/run_benchmark.py:724-732` (judge)
**Issue:** `DISALLOWED_TOOLS = ['Write', 'Edit', 'Bash', 'NotebookEdit']`. The project's own CLAUDE.md states: *"baseline and skill conditions should not be allowed to shell out or read files — that would contaminate the comparison with tool-use variance unrelated to the skill."* As configured, a `claude -p` session in either condition can still invoke `WebSearch`/`WebFetch` (and `Read`/`Glob`/`Grep`, though there is little to read in an isolated temp dir besides the copied skill). A model that reaches for `WebSearch` mid-generation to look up real facts about the fictional deal, or about Google Cloud pricing, introduces exactly the tool-use variance the project's own stack notes flag as contamination, and does so silently — nothing in the recorded generation record or in "Honest caveats" would reveal that a session used a tool at all.
**Fix:** Add `WebSearch`, `WebFetch` (and, if the intent is truly "read no files," `Read`/`Glob`/`Grep`) to `DISALLOWED_TOOLS`, or use `--allowedTools ''`/an explicit empty allow-list for a stricter guarantee.

### WR-03: `--skill-src` default is a CWD-relative path, inconsistent with every other path-valued flag

**File:** `evals/benchmark/run_benchmark.py:2210-2211`
**Issue:** `parser.add_argument('--skill-src', default='skills/proof-first', ...)` is relative to the process's current working directory. Every other path-valued default in the same `argparse` block is absolute and anchored to `REPO_ROOT`/`BENCHMARK_DIR`: `--scenarios` defaults to `str(SCENARIOS_PATH)`, `--raw-dir` to `str(RAW_DIR)`, `--out` to `str(RESULTS_PATH)`. Invoking the documented command from anywhere other than the repo root (e.g. a CI runner with a different working directory, or a user who `cd`s into `evals/benchmark/` first) will either raise `FileNotFoundError` from `shutil.copytree(skill_src, skill_dst)` or, worse, silently resolve to an unintended directory that happens to exist at that relative path.
**Fix:** `default=str(REPO_ROOT / 'skills' / 'proof-first')`.

### WR-04: The entity-collision self-test hardcodes external names instead of reading them from their source of truth

**File:** `evals/benchmark/run_benchmark.py:1519-1527`
**Issue:** `shared_deal_brief_entities = ('Halverton Mutual', 'Kestrel Systems Group', 'Diane Osoria', 'Marcus Feld')` is a hand-copied snapshot of names that (per the code's own comment) live in `examples/deal-brief.md`. If that file is ever edited — a name changed, a name added — this check silently stops testing what it claims to test: it will neither catch a *new* collision introduced by a fresh name added to `examples/deal-brief.md`, nor notice if one of these four names is removed from that file (making the check permanently vacuous for that name). This is exactly the "test that can silently drift from what it verifies" pattern the file's own `per-caveat-drift-guard` test (further down in the same `self_test()`) is designed to avoid for `REQUIRED_CAVEATS`.
**Fix:** Parse `examples/deal-brief.md` for its named entities at self-test time (even a simple regex over a documented "Parties"-style heading) rather than hardcoding a copy.

## Info

### IN-01: Module docstring's "reuses [the disclaimer] rather than restating it" is not literally true

**File:** `evals/benchmark/run_benchmark.py:9-10`, vs. `CAVEAT_TEXT['proxy provenance']` at `evals/benchmark/run_benchmark.py:506-510`
**Issue:** The module docstring says the linter's disclaimer is reused, not restated: *"a mechanical proxy count is not a compliance verdict -- see evals/lint.py's own docstring for that disclaimer stated in full; this file reuses it rather than restating it."* In practice, `CAVEAT_TEXT['proxy provenance']` is an independently authored string with similar but not identical wording, and `lint.DISCLAIMER` is never imported or referenced by name anywhere in `run_benchmark.py`. This is a minor doc-accuracy nit, not a functional issue, but a future edit to `lint.py`'s `DISCLAIMER` wording will not propagate here despite the docstring's claim that it would.
**Fix:** Either import and interpolate `lint.DISCLAIMER` directly into `CAVEAT_TEXT['proxy provenance']` (would require a real import rather than the `exec()`-based loader, or exposing the constant via `_load_lint_module()`'s namespace), or soften the docstring's claim to "paraphrases" rather than "reuses."

---

_Reviewed: 2026-09-20T01:57:01Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
