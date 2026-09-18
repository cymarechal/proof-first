# Phase 5: Evaluation Harness - Pattern Map

**Mapped:** 2026-09-18
**Files analyzed:** 9 (new/modified paths from RESEARCH.md § Wave 0 Gaps)
**Analogs found:** 9 / 9 (all have at least a partial or external-prior-art match; none are wholly novel)

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `evals/lint.py` | utility (checker) | transform (text-in, JSON-out) | `tools/check_repo.py` (in-repo) | role-match, exact self-test idiom |
| `evals/proxy-sources.md` | config / registry | batch (static table read by checker) | `NUMBERING.md` (in-repo) | exact table-shape match |
| `evals/benchmark/run_benchmark.py` | service (orchestrator) | request-response (subprocess) + batch (aggregation) | `evals/conformance/run_conformance.py` (in-repo, primary); `run_bench.py` (external, for judge/aggregate split) | role-match, exact isolation/durability idiom; external for judge+report split |
| `evals/benchmark/scenarios.json` | config / fixture data | batch | SimpleEnglish `evals/scenarios.json` (external) | exact shape match, no in-repo analog |
| `evals/benchmark/bench-deal-brief.md` | config / fixture data | batch | `examples/deal-brief.md` (in-repo) | exact structural match, deliberately different content |
| `evals/benchmark/raw/*.json` | data (committed record) | event-driven (one file per generation/judgement event) | `evals/conformance/transcripts/*.txt` (in-repo, naming convention); SimpleEnglish `evals/raw/*.json` (external, JSON record shape) | role-match; naming from in-repo, schema from external + Decision 7 |
| `evals/benchmark/RESULTS.md` | data (generated doc) | batch (pure aggregation, no network) | `evals/conformance/RESULTS-mod04.md` (in-repo, output shape); SimpleEnglish `run_bench.py`'s `report()` (external, aggregate/report split + "Honest number warnings") | role-match; structure from in-repo, generation idiom from external |
| committed fixture JSON for `--self-test` | test (fixture) | batch | `evals/conformance/fixtures/*.md` + `run_conformance.py`'s `self_test()` monkeypatch fixtures (in-repo) | exact idiom match |
| `.github/workflows/ci.yml` (modified) | config (CI) | batch | itself, existing file | exact — append one line in existing shape |

## Pattern Assignments

### `evals/lint.py` (utility, transform)

**Analog:** `tools/check_repo.py` — **follow closely** for docstring-declared-ceiling and self-test idiom; **deviate** on scope (lint.py stays self-contained inside `evals/`, per RESEARCH.md Decision/Open-Question 2 — do not add anything to `check_repo.py` itself).

**Module docstring / declared-ceiling pattern** (`tools/check_repo.py` lines 1-19):
```python
#!/usr/bin/env python3
"""Structural and textual consistency checker for this repository's registries.

This script is a structural and textual consistency check over NUMBERING.md,
examples/deal-brief.md, and NOTICES.md. It does not read framework source
material and it cannot judge whether a paraphrase reproduces proprietary
text — that judgement is Phase 6's legal review gate (LEG-04). It imports
only the Python standard library; no package-manager dependency is
introduced by this file or by the CI job that runs it.
...
Usage:
  python3 tools/check_repo.py                # live run against this repo
  python3 tools/check_repo.py --self-test     # run fixture-based self-tests
  python3 tools/check_repo.py --mutation-test # ...
```
Copy this shape exactly for `evals/lint.py`'s own docstring, substituting the EVAL-03 disclaimer: state plainly that the deletion test is a semantic judgment the linter cannot perform, and that a violation count is not a compliance verdict — this is the same sentence-class as line 6 above ("it cannot judge whether a paraphrase reproduces proprietary text").

**CLI/argparse + exit-code pattern** (`tools/check_repo.py` lines 6865-6891):
```python
def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--mutation-test', action='store_true')
    args = parser.parse_args()

    if args.self_test:
        ok = self_test()
        sys.exit(0 if ok else 1)
    ...
    violations = run_all_checks(REPO_ROOT)
    violations.sort(key=lambda v: (v[1].split(' ', 1)[0], v[0]))
    if not violations:
        print("check_repo: 0 violations")
        sys.exit(0)
    for _, line in violations:
        print(line)
    sys.exit(1)
```
`evals/lint.py` should mirror `--self-test`'s `sys.exit(0 if ok else 1)` return-code contract exactly (CI depends on this). It does not need `--mutation-test` — RESEARCH.md does not ask for one; adding it would be scope creep beyond EVAL-01/02/03.

**Self-test fixture pattern** (`tools/check_repo.py` lines 5807-5886, abbreviated) plus RESEARCH.md's own worked example (Code Examples § "Linter self-test pattern"):
```python
SLOP_FIXTURE = "This comprehensive, best-in-class, world-class solution delivers a robust, enterprise-grade landing zone."
CLEAN_FIXTURE = "AWS Control Tower governs the new account structure across 850 virtual machines."

def self_test():
    dirty = lint(SLOP_FIXTURE)
    clean = lint(CLEAN_FIXTURE)
    assert dirty["violations_total"] >= 4, dirty
    assert clean["violations_total"] == 0, clean
    print("self-test PASS:", dirty["violations_total"], "in slop fixture, 0 in clean")
```
`check_repo.py`'s own convention is one dedicated `*_root`/fixture pair **per violation code** inside a single `tempfile.TemporaryDirectory()` block (see the ~80 `_root` variable names at lines 5811-5886) — reuse that one-fixture-pair-per-code discipline for `evals/lint.py`'s own violation codes (`proxy-term-unsourced`, `proxy-term-source-invalid`, `proxy-term-source-is-internal`, plus the buzzword/superlative/no-adjacent-number codes), not just the two top-level fixtures shown above.

**Provenance-checker pattern (EVAL-02):** no direct in-repo analog exists (this is the one genuinely new checking behavior in the phase), but it follows the same shape as `check_repo.py`'s `undefined-id` check (an ID cited somewhere must appear in a registry table) — cross-reference `PROXY_TERMS` against rows of `evals/proxy-sources.md`, flagging any term with no row, any row with an invalid source label, or any URL resolving inside this repo. Model the violation-code naming and the "declared ceiling" comment style on `check_repo.py`'s `undefined-id`/`range-id` codes (see docstring lines 20-53 for the naming convention: lowercase-hyphenated code, one paragraph of what fires and what its ceiling is).

---

### `evals/proxy-sources.md` (config/registry, batch)

**Analog:** `NUMBERING.md` — **follow closely**.

**Table-style pattern** (`NUMBERING.md` lines 1-20):
```markdown
# NUMBERING.md

Authoritative ID registry for Proof First's two rule namespaces. This file is the single source
of truth `tools/check_repo.py` reads its ranges from — widening a range here changes enforcement
everywhere, not just in this document.

## PF reserved ranges

| Section | Range | Concern | Allocated | Next free |
|---|---|---|---|---|
| PF-0 | PF-0.1-PF-0.9 | Opening / Reframe | 1 | PF-0.2 |
```
Copy this "authoritative registry, single source of truth for a checker" framing verbatim in spirit for `evals/proxy-sources.md`'s own opening paragraph, substituting: "the single source of truth `evals/lint.py`'s provenance check reads its allow-listed terms from." Table columns per RESEARCH.md Decision 1: `| Term | Source (A or B) | URL |`, exactly two allowed source labels — this is a narrower, flatter table than `NUMBERING.md`'s multi-column ranges table, so follow the general "one authoritative table, checker-enforced" idiom, not the exact column set.

---

### `evals/benchmark/run_benchmark.py` (service, request-response + batch)

**Analog:** `evals/conformance/run_conformance.py` — **follow closely** for isolation, durability, error handling, and CLI-arg shape; **deviate** on persistence policy (commit every raw record, vs. `run_conformance.py`'s ephemeral-by-default transcripts) and on adding a judge pass and `--report-only`, both of which have no in-repo analog and should be modeled on SimpleEnglish's `run_bench.py` instead (external prior art, explicitly named in RESEARCH.md as the improve-on/copy-from reference for exactly this split).

**Imports / module docstring convention** (`run_conformance.py` lines 1-19, paraphrased structure — read in full this session): states in its own docstring "It imports only the Python standard library: argparse, datetime, json, ..." — copy this same declared-stdlib-only opening sentence for `run_benchmark.py`.

**Isolated-session + skill-install pattern** (`run_conformance.py` lines 191-228, `run_session()`):
```python
def run_session(skill_src, fixture_path, model, out_path, timeout_s):
    """Drive one live write-mode `claude -p` session in an isolated temp dir.

    Returns the session's captured stdout (also written to out_path).
    Exactly one call site writes any given out_path -- concurrent writers to
    one path is the defect that produced a false "duplicated sections"
    finding in the first UAT pass, so this runner never parallelises onto a
    shared path.
    """
    skill_src = pathlib.Path(skill_src)
    fixture_path = pathlib.Path(fixture_path)

    tmp_dir = pathlib.Path(tempfile.mkdtemp(prefix='proof-first-conformance-'))
    try:
        skill_dst = tmp_dir / '.claude' / 'skills' / 'proof-first'
        skill_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(skill_src, skill_dst)
        ...
        argv = ['claude', '-p', prompt, '--model', model, '--disallowedTools'] + DISALLOWED_TOOLS
        out_path = pathlib.Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            result = subprocess.run(argv, cwd=str(tmp_dir), capture_output=True, text=True, timeout=timeout_s)
        ...
```
Copy this `tempfile.mkdtemp(prefix='proof-first-...')` + `shutil.copytree` skill-install pattern exactly for the skill-on generation condition; for skill-off, run the identical isolated-tmp-dir setup with no `.claude/skills/` folder created — this is RESEARCH.md's Pattern 1, already written against this exact source, and is a straight copy, not an adaptation.

**Error handling / SessionFailedError pattern** (`run_conformance.py` lines 105-123):
```python
class SessionFailedError(RuntimeError):
    """Raised by run_session() when `claude -p` exits non-zero.

    Carries the exit code and stderr so the caller can record a diagnosable
    unscoreable reason instead of silently scoring stdout (which, on a
    quota/auth/other non-timeout failure, is typically a short error string
    rather than a real transcript) as if it were a normal session.
    """
    def __init__(self, returncode, stderr):
        self.returncode = returncode
        self.stderr = stderr or ''
        super().__init__(f'claude -p exited {returncode}')
```
Copy this class verbatim in shape for `run_benchmark.py`. This directly guards Pitfall 1 in RESEARCH.md ("Scoring an error string as if it were generated text") — a documented, already-occurred bug class in this exact repo (MOD-04's usage-limit-exhaustion incident). Any non-zero exit or `is_error: true` envelope must raise this and be recorded with `verdict: "unscoreable"`, never silently lint/judge the stdout.

**VERDICTS tuple pattern** (`run_conformance.py` line 99):
```python
VERDICTS = ('conformant', 'no-family', 'rule-before-family', 'unscoreable')
```
`run_benchmark.py` needs its own such tuple for judge verdicts — at minimum `('scored', 'unscoreable')` per Decision 5 ("record the pair `verdict: 'unscoreable'`... exclude it from the mean"). Reuse the exact vocabulary discipline: a fixed tuple checked in `self_test()`, not a bare string compared ad hoc.

**Content-addressed skill-version pattern** (`run_conformance.py` lines 742-772, `_git_blob_sha`):
```python
def _git_blob_sha(skill_src):
    """Return the git blob SHA of skill_src/SKILL.md -- the actual file this
    run copies into every session, not necessarily the repo's HEAD version.
    ... `git hash-object` is content-addressed and needs no repo relationship to
    the target path, so it reports the correct SHA for a working-tree copy...
    """
    skill_md = pathlib.Path(skill_src) / 'SKILL.md'
    if not skill_md.exists():
        return None
    try:
        result = subprocess.run(['git', 'hash-object', str(skill_md)], cwd=str(REPO_ROOT),
                                 capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            return None
        sha = result.stdout.strip()
        return sha if sha else None
    except (subprocess.SubprocessError, OSError):
        return None
```
Copy verbatim as `skill_sha` for the generation record schema (Decision 7). Do not use `git rev-parse HEAD:...` — this function's own docstring documents why that was a real, fixed bug in this repo's history.

**Write-then-flush durability pattern** (`run_conformance.py` lines 781-812, `_write_result_line` / `run_matrix`):
```python
def _write_result_line(handle, text):
    """Write `text` to `handle` and flush it immediately.
    This is the single place durability is established for the results
    file... so a future edit that drops the flush is a one-line diff rather
    than a scattered one (03-REVIEW.md CR-01).
    """
    handle.write(text)
    handle.flush()
```
**Deviate here, deliberately** — per RESEARCH.md's own "Pattern 2" analysis: because `run_benchmark.py` writes one file per record (not one shared append-mode results file), `pathlib.Path.write_text()` already opens/writes/closes atomically in one call, so no separate `_write_result_line`/flush helper is needed. State this deviation inline in the new code's own comment, exactly as RESEARCH.md's Code Examples section already drafts it:
```python
def _write_json_atomic(path, record):
    path.write_text(json.dumps(record, indent=2))
    # pathlib.Path.write_text() opens, writes, and closes in one call —
    # no separate flush needed, unlike run_conformance.py's append-mode
    # results handle.
```

**CLI arg shape to copy** (`run_conformance.py` lines 881-899, `main()`'s `add_argument` calls): `--self-test`, `--skill-src` (default `skills/proof-first`), `--models` (comma-separated, default `claude-sonnet-5`), `--repeats` (int), `--transcript-dir`/`--out`, `--timeout`. `run_benchmark.py` should mirror this flag naming (`--models`, `--repeats`, `--effort`, `--raw-dir`, `--out`) plus RESEARCH.md's two new flags: `--report-only` (offline aggregation) and `--json-schema`-based judge parsing (no in-repo precedent — external only, see below).

**Judge + aggregate/report split — external prior art, no in-repo analog, follow SimpleEnglish's `run_bench.py` closely:**

Generation call pattern (`run_bench.py` lines 49-72):
```python
def call_claude(prompt, model, timeout=300, effort=DEFAULT_EFFORT):
    cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "json",
           "--disallowedTools", "Bash,Read,Write,Edit,Glob,Grep,WebFetch,WebSearch"]
    if effort:
        cmd += ["--effort", effort]
    t0 = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd="/tmp")
    if proc.returncode != 0:
        raise RuntimeError(f"{model}: {proc.stderr[:300]}")
    env = json.loads(proc.stdout)
    if isinstance(env, list):  # CLI >= 2.1 returns the message stream
        env = next(m for m in env if m.get("type") == "result")
    if env.get("is_error"):
        raise RuntimeError(f"{model}: {str(env.get('result'))[:300]}")
    usage = env.get("usage", {})
    return {"text": env.get("result", ""), "input_tokens": usage.get("input_tokens"), ...}
```
Deviate: use `run_conformance.py`'s isolated-`tempfile.mkdtemp()`-per-session cwd instead of this file's shared `cwd="/tmp"` (RESEARCH.md's explicit "Improve on" item — cheaper and cleaner, per this session's own live cost test), and use `SessionFailedError`/`unscoreable` instead of a bare `raise RuntimeError`. Keep the `isinstance(env, list)` defensive unwrap — Pitfall 2 in RESEARCH.md names this exact CLI-version-drift risk.

Baseline/skill prompt-parity pattern (`run_bench.py` lines 75-80):
```python
def build_prompt(scenario, condition, skill_text):
    if condition == "baseline":
        return scenario["prompt"]
    return ("Follow these writing instructions exactly, including the self-check step:\n\n"
            + skill_text + "\n\n---\n\nTask: " + scenario["prompt"]
            + "\n\nReturn only the final text, no rule commentary.")
```
Deviate: RESEARCH.md's Decision 3 prefers `run_conformance.py`'s skill-**folder-install** approach over this file's read-skill-text-into-prompt-string approach ("more faithful to how a real user actually invokes the skill... matching this repo's own existing (better) pattern"). Keep the parity principle (skill-off = bare `scenario["prompt"]`, unmodified) but implement skill-on via the temp-dir `.claude/skills/proof-first/` install from `run_conformance.py`, not string concatenation.

Resumable/skip-if-exists generation loop (`run_bench.py` lines 83-103, `generate()`):
```python
def generate(models, scenarios, effort):
    ...
    for i, (model, cond, sc) in enumerate(todo, 1):
        out = RAW / f"{model}__{cond}__{sc['id']}.json"
        if out.exists():
            ...
            continue
        ...
```
Copy this skip-if-exists idiom directly — RESEARCH.md names it explicitly ("lets an interrupted live run be safely re-invoked without re-paying for already-scored cells"). Adapt the filename template to Decision 7's schema (`{model}__{condition}__{scenario_id}__r{repeat}.json`).

Aggregate/report split (`run_bench.py` lines 106-137, `aggregate()`):
```python
def aggregate():
    rows = [json.loads(p.read_text()) for p in sorted(RAW.glob("*.json")) if "__judge__" not in p.name]
    ...
    (RESULTS / "results.json").write_text(json.dumps({...}, indent=2))
    return table, meta
```
Copy this "pure function over committed raw files, no subprocess/network call" shape directly for `run_benchmark.py`'s own `--report-only` path (RESEARCH.md's "Offline recompute path" section quotes this same function as the model). Deviate on two points RESEARCH.md flags explicitly: (1) never compute/print a standard deviation from n=3 — report mean + range instead; (2) never blend the mechanical-lint number and the judged-persuasion number into one composite score (EVAL-09) — this file's `aggregate()` keeps them in one `table` dict per model, which is fine internally, but the **rendered** `RESULTS.md` must split them into two separately headed sections (`## Mechanical proxy counts`, `## Judged persuasion`), unlike this file's flatter single markdown table.

Judge win/tie/loss + both-orders-swap pattern (`run_bench.py` lines 140-162, `judge_summary()`):
```python
def judge_summary():
    files = sorted(RAW.glob("*__judge__*.json"))
    per_model, wins, ties, losses = {}, 0, 0, 0
    skill_sum = base_sum = valid = recorded_effort = 0
    for p in files:
        d = json.loads(p.read_text())
        recorded_effort += "judge_effort" in d
        o1, o2 = d["order1_base_first"], d["order2_skill_first"]
        if not o1 or not o2:
            continue
        skill = (o1["b_score"] + o2["a_score"]) / 2
        base = (o1["a_score"] + o2["b_score"]) / 2
        valid += 1
        skill_sum += skill
        base_sum += base
        w = per_model.setdefault(d["model"], [0, 0, 0])
        if skill > base:
            wins += 1; w[0] += 1
        elif skill == base:
            ties += 1; w[1] += 1
        ...
```
Copy this both-orders-average-then-compare shape directly. Deviate per Decision 5: score three separate rubric dimensions (`evidence`, `clarity`, `persuasive_force`) instead of this file's single scalar score, so persuasive force cannot be inferred from the other two — average each dimension independently across the two orders, then compare on `persuasive_force` (and report all three) rather than a single blended score. Also deviate on parsing: replace this file's implicit free-text JSON parse with `--json-schema`-constrained structured output (RESEARCH.md Decision 5's named concrete improvement), removing the fragile `res["text"].strip().strip("\`json\n")` scrape SimpleEnglish uses elsewhere in the same file.

"Honest number warnings" permanent section (`run_bench.py`'s `report()`, referenced at line 220 — `"## Honest number warnings"`): copy this as a **structurally required, non-trimmable** section, per RESEARCH.md's explicit instruction — Phase 5's equivalent is EVAL-10's "honest-caveats section naming position bias, judge family bias, baseline prompt parity, proxy provenance, and sample size," five items, all five must appear verbatim-ish, checked by `self_test()`.

---

### `evals/benchmark/scenarios.json` (config, batch)

**Analog:** SimpleEnglish `evals/scenarios.json` (external; no in-repo JSON scenario file exists) — **follow closely** for shape, **deviate** on content per RESEARCH.md Decision 2 (family-tagged, plain-task-register prompts, no proof-first vocabulary, grounded in `bench-deal-brief.md` facts embedded inline).

Shape (per RESEARCH.md Decision 2, itself derived from reading SimpleEnglish's file in full):
```json
{"id": "exec-summary-1", "family": "executive-summary", "prompt": "Write a two-paragraph executive summary for X, covering Y and Z. Return only the text."}
```
8 entries required: 2 each for `rfp-rfi`, `solution-proposal`, `executive-summary`, `demo-discovery` (the four family names are `skills/proof-first/references/artifact-patterns.md`'s own headings).

---

### `evals/benchmark/bench-deal-brief.md` (config, batch)

**Analog:** `examples/deal-brief.md` (in-repo) — **follow the structural shape closely, deviate completely on content** (mandatory — RESEARCH.md Decision 2 forbids reusing Halverton Mutual's facts, to avoid EVAL-02-style circularity/memorization contamination).

**Section shape to copy** (`examples/deal-brief.md` lines 1-23):
```markdown
# Deal Brief: Cloud Migration RFP (Fictional)

Last reviewed: 2026-09-10

This brief is entirely invented for illustration; any resemblance to a real company, person, or transaction is unintended. ...

## The deal in one paragraph
...
## Parties
- **Halverton Mutual** — the buyer: ...
## Estate and target platforms
...
## People and roles
- **Diane Osoria** — Chief Financial Officer, the economic buyer. Cares about ...
## Pain points
- ...
## Timeline
```
`bench-deal-brief.md` must reuse this exact section skeleton (fictional-disclaimer line, one-paragraph deal summary, parties, technical/estate facts, named people with roles and cares, pain points, timeline) but with an entirely different fictional company, industry, dollar figures, named people, and named technical platforms — different enough that no phrase from `worked-examples.md`'s or `before-after.md`'s existing ✗/✓ pairs (all keyed to Halverton Mutual) could be reproduced verbatim by a skill-on session prompted with these new facts.

---

### `evals/benchmark/raw/*.json` (data, event-driven)

**Analog (naming convention):** `run_conformance.py`'s transcript naming, line 822: `f'{model}__{fixture_stem}__r{repeat}.txt'` — **follow closely**, adapted to Decision 7's two filename templates:
- Generations: `{model}__{condition}__{scenario_id}__r{repeat}.json`
- Judgements: `{model}__judge__{scenario_id}__r{repeat}__order{1|2}.json`

**Analog (record schema):** external — SimpleEnglish's per-record JSON dict shape (`run_bench.py` lines 64-72, `res.update(...)` at line 100) plus RESEARCH.md Decision 7's own concrete schema (already fully specified with example JSON in RESEARCH.md — copy that schema verbatim, it is not a paraphrase target).

---

### `evals/benchmark/RESULTS.md` (data, batch/generated)

**Analog:** `evals/conformance/RESULTS-mod04.md` (in-repo, output shape/voice) + SimpleEnglish `run_bench.py`'s `report()` (external, generation idiom and the "Honest number warnings" permanent section). **Follow both closely**, combined: in-repo file for house voice/citation style, external file for the generation mechanics (pure function, `--report-only`, non-trimmable caveats section).

**Structural gate (EVAL-09), no analog — genuinely new requirement, implement directly from RESEARCH.md's own spec:** two separately headed top-level sections, `## Mechanical proxy counts` and `## Judged persuasion`, never blended into one number. Model the presence-check style on `check_repo.py`'s existing `artifact-family-section-missing` code (heading-presence check) if a `results-sections-missing` self-test assertion is added.

---

### Committed fixture JSON for `run_benchmark.py`'s own `--self-test`

**Analog:** `evals/conformance/fixtures/*.md` (committed input fixtures) + `run_conformance.py`'s `self_test()` monkeypatch pattern (lines 307-680, e.g. the `_fake_failed_run` / `_fake_timeout_run` stubs at lines 485-632) — **follow closely**. `run_conformance.py`'s `self_test()` never calls a real `claude` binary; it monkeypatches `subprocess.run` with fakes that return controlled JSON/exit codes, then asserts the resulting verdict/record shape. `run_benchmark.py`'s `--self-test` should do the same: commit a handful of representative fixture generation/judgement JSON files under a self-test-only path (or inline dicts), monkeypatch `subprocess.run` to prove `--report-only` never calls it, and assert `aggregate()`/`build_results_md()` produce byte-identical output on repeat invocation (EVAL-12's exact requirement).

---

### `.github/workflows/ci.yml` (modified)

**Analog:** itself — **follow closely**, append only.

**Current full file (21 lines) — the exact shape new lines must match:**
```yaml
name: check

on:
  push:
  pull_request:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Run checker self-test, mutation test, and live check
        run: |
          python3 tools/check_repo.py --self-test
          python3 tools/check_repo.py --mutation-test
          python3 tools/check_repo.py
          python3 evals/conformance/run_conformance.py --self-test
          python3 tools/generate_derivatives.py --check
```
Add exactly two new lines inside the existing single `run: |` block, matching the existing one-command-per-line style, no new `steps:` entry, no new job, no live/paid command:
```
          python3 evals/lint.py --self-test
          python3 evals/benchmark/run_benchmark.py --self-test
```
Do **not** add a live-matrix invocation — RESEARCH.md is explicit that the paid benchmark run must never be a CI gate.

## Shared Patterns

### Stdlib-only, no third-party imports
**Source:** `tools/check_repo.py` line 8-9 ("It imports only the Python standard library... no package-manager dependency is introduced") and `run_conformance.py`'s equivalent opening sentence.
**Apply to:** `evals/lint.py`, `evals/benchmark/run_benchmark.py` — both must import only `re, json, argparse, pathlib, subprocess, tempfile, uuid, datetime, hashlib, shutil, sys` (per RESEARCH.md's Standard Stack table).

### Isolated per-session temp directory, never repo root or a shared dir
**Source:** `evals/conformance/run_conformance.py` `run_session()`, lines 203-228 (`tempfile.mkdtemp(prefix='proof-first-conformance-')`).
**Apply to:** every live generation and judge call in `run_benchmark.py`. Explicitly reject SimpleEnglish's shared `cwd="/tmp"` pattern (RESEARCH.md's own named anti-pattern).

### `SessionFailedError` / non-zero-exit and malformed-response handling → `verdict: "unscoreable"`, never scored as data
**Source:** `evals/conformance/run_conformance.py` lines 105-123 and its `VERDICTS` tuple (line 99).
**Apply to:** all subprocess calls in `run_benchmark.py` (both generation and judge). This is Pitfall 1 from RESEARCH.md, a documented past incident in this exact repo (MOD-04).

### `argv` as a list, never `shell=True` or string-interpolated commands
**Source:** `run_conformance.py`'s `subprocess.run(argv, ...)` calls throughout (e.g. line 216-228, line 760-766) — `argv` always built as a Python list.
**Apply to:** every `subprocess.run` call in `evals/lint.py` (none expected — pure text) and `run_benchmark.py` (all `claude -p` and `git hash-object` invocations). Required by RESEARCH.md's Security Domain § V5/V12 (input validation, no path/argument injection).

### Fixed filename templates keyed only to committed, non-free-text values
**Source:** `run_conformance.py` line 822 (`f'{model}__{fixture_stem}__r{repeat}.txt'`, where `fixture_stem` is drawn only from `_default_fixtures()`'s `FIXTURES_DIR.glob('*.md')`, never free-text input).
**Apply to:** `evals/benchmark/raw/*.json` filenames — `scenario_id` must be drawn only from the committed `scenarios.json`, never from any user/CLI free-text argument, per RESEARCH.md's Security Domain § V12.

### `--self-test` exit-code contract: `sys.exit(0 if ok else 1)`
**Source:** `tools/check_repo.py` lines 6872-6874 and `run_conformance.py`'s equivalent `main()` self-test branch.
**Apply to:** `evals/lint.py` and `evals/benchmark/run_benchmark.py` — both must be wired into `.github/workflows/ci.yml` on this exact contract.

### Pure aggregation with zero network/subprocess calls in offline mode
**Source:** SimpleEnglish `run_bench.py`'s `aggregate()` (lines 106-137) and RESEARCH.md's own worked `main()` example (`Code Examples § "--report-only offline aggregation entry point"`).
**Apply to:** `run_benchmark.py --report-only` — EVAL-12 requires this be provably network-free; self-test should monkeypatch `subprocess.run` to raise if called during `--report-only`, proving the offline path never shells out.

## No Analog Found

None. Every file in the Wave 0 gap list has at least a strong external-prior-art match (SimpleEnglish's harness) even where no in-repo file exists (`scenarios.json`, the judge pass, `--report-only`). The provenance-checker logic for `evals/proxy-sources.md` (EVAL-02) is the single genuinely novel piece of logic in this phase — it has no full analog anywhere, in-repo or external, but is a small, mechanical extension of `check_repo.py`'s existing `undefined-id` cross-reference idiom (see `evals/lint.py` § above).

## Metadata

**Analog search scope:** `tools/`, `evals/` (in-repo, full read of `check_repo.py` targeted sections and `run_conformance.py` in full), `examples/`, `NUMBERING.md`, `.github/workflows/ci.yml`, plus `~/devoteam/.claude/plugins/marketplaces/simple-english/evals/run_bench.py` (external prior art, targeted read of `call_claude`, `build_prompt`, `generate`, `aggregate`, `judge_summary`).
**Files scanned:** 7 in-repo, 1 external.
**Pattern extraction date:** 2026-09-18
