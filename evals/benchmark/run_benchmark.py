#!/usr/bin/env python3
"""Skill-on/skill-off persuasion benchmark and offline aggregator for Proof First.

This script measures two things, kept structurally separate and never blended
into one figure: mechanical proxy-violation counts (computed by loading
evals/lint.py's lint() function and running it over generated text) and judged
persuasion (scored by a blind pairwise Claude judge with labels stripped). It
does not itself apply the deletion test PF-3.1 states, and a mechanical proxy
count is not a compliance verdict -- see evals/lint.py's own docstring for
that disclaimer stated in full; this file reuses it rather than restating it.

It imports only the Python standard library: argparse, datetime, json,
pathlib, re, shutil, subprocess, sys, tempfile, uuid. No package-manager
dependency is introduced by this file or by the CI job that runs it. Every
length, word count, and offset this module reports is a Python str code
point count, never a byte count or a grapheme-cluster count.

Usage:
  python3 evals/benchmark/run_benchmark.py --self-test
      Offline proof of the generation-record schema, the matrix loop, and the
      aggregator/renderer. Makes no subprocess call and no network call; runs
      on a machine with no `claude` binary installed.

  python3 evals/benchmark/run_benchmark.py [--models M,...] [--repeats N]
      [--effort LEVEL] [--scenarios PATH] [--skill-src PATH] [--raw-dir PATH]
      [--timeout SECONDS] [--max-budget-usd AMOUNT]
      Live mode: drives the full model x condition x scenario x repeat
      matrix, one isolated-temp-dir `claude -p` session per cell, skipping
      any cell whose raw record already exists. Requires `claude auth
      status` to show loggedIn: true. No API key needed.

  python3 evals/benchmark/run_benchmark.py --report-only [--raw-dir PATH] [--out PATH]
      Offline recompute: reads every committed record under --raw-dir,
      recomputes every mean and range, and rewrites RESULTS.md. Makes zero
      subprocess calls and zero network calls -- the self-test proves this by
      replacing subprocess.run with a function that raises.
"""

import argparse
import datetime
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import uuid

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
BENCHMARK_DIR = pathlib.Path(__file__).resolve().parent

# The four family names are skills/proof-first/references/artifact-patterns.md's
# own section headings (RFP and RFI response, Solution proposal, Executive
# summary, Demo and discovery material). Frozen -- a fifth value or a missing
# one is a load_scenarios() error, never a silent pass-through.
FAMILIES = ('rfp-rfi', 'solution-proposal', 'executive-summary', 'demo-discovery')
CONDITIONS = ('skill-off', 'skill-on')
DEFAULT_MODELS = ('claude-sonnet-5', 'claude-opus-5')
DEFAULT_EFFORT = 'low'
DEFAULT_REPEATS = 3
GENERATION_VERDICTS = ('generated', 'unscoreable')
DISALLOWED_TOOLS = ['Write', 'Edit', 'Bash', 'NotebookEdit']
MAX_BUDGET_USD = 2

SCENARIOS_PATH = BENCHMARK_DIR / 'scenarios.json'
RAW_DIR = BENCHMARK_DIR / 'raw'
FIXTURES_DIR = BENCHMARK_DIR / 'fixtures'
RESULTS_PATH = BENCHMARK_DIR / 'RESULTS.md'

# Tokens that would cue the skill-off condition toward this project's own
# disciplined-prose vocabulary rather than measuring default, unguided model
# behavior -- checked against every scenario prompt by self_test().
FORBIDDEN_PROMPT_TOKENS = ('PF-', 'MC-', 'proof-first', 'proof first', 'deletion test')

# Every field a generation record must carry (Decision 7's frozen schema).
# self_test() asserts a record is never missing one of these.
GENERATION_RECORD_FIELDS = (
    'run_id', 'timestamp', 'model', 'canonical_model', 'effort', 'condition',
    'family', 'scenario_id', 'scenario_prompt', 'skill_sha', 'repeat', 'text',
    'usage', 'cost_usd', 'duration_ms', 'cli_version', 'verdict', 'reason',
)


class SessionFailedError(RuntimeError):
    """Raised by run_generation() when `claude -p` exits non-zero, when its
    envelope reports `is_error: true`, or when its envelope cannot be parsed.

    Carries the exit code (or -1 for a non-exit-code failure) and a stderr /
    reason string, so the caller (run_matrix, or this file's own self-test
    acting as a single-cell caller) records a diagnosable `unscoreable`
    reason instead of scoring stdout -- which, on a non-timeout failure, is
    typically a short error string rather than real generated text -- as if
    it were real data. Copied in shape from
    evals/conformance/run_conformance.py's SessionFailedError, guarding the
    same Pitfall 1 bug class documented there in full (MOD-04's
    usage-limit-exhaustion incident, where every failed session's stdout was
    scored `no-family` instead of excluded as `unscoreable`).
    """

    def __init__(self, returncode, stderr):
        self.returncode = returncode
        self.stderr = stderr or ''
        super().__init__(f'claude -p exited {returncode}')


def _git_blob_sha(skill_src):
    """Return the git blob SHA of skill_src/SKILL.md -- the actual file this
    run copies into every skill-on session, not necessarily the repo's HEAD
    version.

    Copied verbatim in shape from evals/conformance/run_conformance.py's
    _git_blob_sha(). `git hash-object` is content-addressed and needs no
    repo relationship to the target path, so it reports the correct SHA for
    a working-tree copy or any other directory shape -- unlike `git
    rev-parse HEAD:...`, which silently reports the wrong SHA for any
    materialised non-HEAD skill copy (the bug that function's own docstring
    documents fixing in this repo's history).
    """
    skill_md = pathlib.Path(skill_src) / 'SKILL.md'
    if not skill_md.exists():
        return None
    try:
        result = subprocess.run(
            ['git', 'hash-object', str(skill_md)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return None
        sha = result.stdout.strip()
        return sha if sha else None
    except (subprocess.SubprocessError, OSError):
        return None


def _write_json_atomic(path, record):
    """Write `record` to `path` as UTF-8 JSON with ensure_ascii=False.

    pathlib.Path.write_text() opens, writes, and closes in one call -- no
    separate flush helper is needed here, unlike
    evals/conformance/run_conformance.py's append-mode results handle
    (_write_result_line()), because this module writes one file per record
    rather than appending to one shared file across the whole run.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding='utf-8')


def load_scenarios(path=None):
    """Return the list of scenario dicts from `path` (default SCENARIOS_PATH).

    Raises ValueError, naming the problem, for: zero scenarios in the file, a
    duplicate `id`, a scenario missing `family`, or a `family` value outside
    the four frozen FAMILIES. Never renders an empty or malformed scenario
    file as a successful load. Does NOT check that every family is covered --
    that is a self-test-only completeness assertion over the shipped file
    (see self_test()'s family-coverage case), not a property this generic
    loader enforces on every caller (an intermediate, partially-populated
    scenarios.json -- such as the one this plan's own Task 1 ships -- is a
    legitimate input to this function).
    """
    path = pathlib.Path(path) if path is not None else SCENARIOS_PATH
    data = json.loads(path.read_text(encoding='utf-8'))
    if not data:
        raise ValueError(f'{path} contains zero scenarios')

    seen_ids = set()
    for scenario in data:
        sid = scenario.get('id')
        if not sid:
            raise ValueError(f'scenario missing id: {scenario!r}')
        if sid in seen_ids:
            raise ValueError(f'duplicate scenario id: {sid!r}')
        seen_ids.add(sid)

        family = scenario.get('family')
        if not family:
            raise ValueError(f'scenario {sid!r} is missing family')
        if family not in FAMILIES:
            raise ValueError(
                f'scenario {sid!r} has unknown family {family!r}, expected one of {FAMILIES}'
            )

    return data


def raw_path_for_generation(model, condition, scenario_id, repeat, raw_dir=None):
    """Return the frozen filename template path for a generation record.

    `scenario_id` is drawn only from the committed scenarios.json (see
    load_scenarios()); `model`/`condition` are drawn only from frozen tuples;
    `repeat` is an int. No CLI free-text value reaches this filename.
    """
    raw_dir = pathlib.Path(raw_dir) if raw_dir is not None else RAW_DIR
    return raw_dir / f'{model}__{condition}__{scenario_id}__r{repeat}.json'


def raw_path_for_judgement(model, scenario_id, repeat, order, raw_dir=None):
    """Return the frozen filename template path for a judgement record."""
    raw_dir = pathlib.Path(raw_dir) if raw_dir is not None else RAW_DIR
    return raw_dir / f'{model}__judge__{scenario_id}__r{repeat}__order{order}.json'


def _unwrap_envelope(raw_stdout):
    """Parse `raw_stdout` (claude -p --output-format json's stdout) and
    return the single result-message dict.

    Handles both CLI response shapes (Pitfall 2 in 05-RESEARCH.md): a single
    JSON object, or a JSON array of message objects (CLI >= 2.1's message-
    stream shape) where exactly one message carries `"type": "result"`.
    Raises ValueError if an array carries no such message.
    """
    env = json.loads(raw_stdout)
    if isinstance(env, list):
        for message in env:
            if isinstance(message, dict) and message.get('type') == 'result':
                return message
        raise ValueError('no message with type "result" found in envelope array')
    return env


def _unscoreable_generation_record(model, effort, condition, scenario, repeat, skill_src, reason):
    """Build an `unscoreable` generation record with the given `reason`.

    Used by the caller of run_generation() (run_matrix, or this file's own
    self-test acting as a single-cell caller) after a SessionFailedError, and
    also matches the shape run_generation() itself uses when a session
    "succeeds" (exit 0, is_error false) but returns empty or whitespace-only
    text -- either way, a failure is never written as a zero-violation
    generation (must_haves, EVAL-05 empty edge).
    """
    skill_sha = _git_blob_sha(skill_src) if condition == 'skill-on' else None
    return {
        'run_id': str(uuid.uuid4()),
        'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'model': model,
        'canonical_model': model,
        'effort': effort,
        'condition': condition,
        'family': scenario['family'],
        'scenario_id': scenario['id'],
        'scenario_prompt': scenario['prompt'],
        'skill_sha': skill_sha,
        'repeat': repeat,
        'text': '',
        'usage': {},
        'cost_usd': None,
        'duration_ms': None,
        'cli_version': None,
        'verdict': 'unscoreable',
        'reason': reason,
    }


def run_generation(model, effort, condition, scenario, repeat, skill_src, timeout_s,
                    raw_dir=None, max_budget_usd=MAX_BUDGET_USD):
    """Drive one isolated-temp-dir `claude -p` generation session, write the
    resulting record to its frozen filename template, and return
    (record, wrote_new).

    `wrote_new` is False when the cell's raw file already existed -- no
    subprocess call is made in that case, the resumability property the
    whole matrix depends on (05-RESEARCH.md's skip-if-exists pattern, copied
    from SimpleEnglish's `generate()`).

    Raises SessionFailedError on a non-zero exit, an `is_error: true`
    envelope, or an unparseable envelope. The caller (run_matrix, or this
    file's own self-test acting as a single-cell caller) is responsible for
    catching that and writing an `unscoreable` record instead of letting the
    failure propagate out of the whole run -- see
    _unscoreable_generation_record().

    A session that exits 0 with `is_error: false` but returns empty or
    whitespace-only text is NOT an error from `claude -p`'s point of view,
    so it does not raise; this function instead writes and returns a record
    with `verdict: "unscoreable"` and a reason, directly -- never a record
    with empty text left un-flagged as `generated`.
    """
    raw_dir = pathlib.Path(raw_dir) if raw_dir is not None else RAW_DIR
    path = raw_path_for_generation(model, condition, scenario['id'], repeat, raw_dir)
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8')), False

    tmp_dir = pathlib.Path(tempfile.mkdtemp(prefix='proof-first-benchmark-'))
    try:
        if condition == 'skill-on':
            skill_dst = tmp_dir / '.claude' / 'skills' / 'proof-first'
            skill_dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(skill_src, skill_dst)

        argv = [
            'claude', '-p', scenario['prompt'],
            '--model', model,
            '--effort', effort,
            '--output-format', 'json',
            '--disallowedTools', ','.join(DISALLOWED_TOOLS),
            '--max-budget-usd', str(max_budget_usd),
        ]
        result = subprocess.run(
            argv, cwd=str(tmp_dir), capture_output=True, text=True, timeout=timeout_s,
        )
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    if result.returncode != 0:
        raise SessionFailedError(result.returncode, result.stderr)

    try:
        env = _unwrap_envelope(result.stdout)
    except (json.JSONDecodeError, ValueError) as exc:
        raise SessionFailedError(-1, f'unparseable envelope: {exc}')

    if not isinstance(env, dict) or env.get('is_error'):
        detail = str(env.get('result', ''))[:300] if isinstance(env, dict) else 'malformed envelope (not a JSON object)'
        raise SessionFailedError(-1, detail)

    text = env.get('result', '') or ''
    if not text.strip():
        record = _unscoreable_generation_record(
            model, effort, condition, scenario, repeat, skill_src,
            reason='empty or whitespace-only result text',
        )
        _write_json_atomic(path, record)
        return record, True

    usage = env.get('usage', {}) or {}
    skill_sha = _git_blob_sha(skill_src) if condition == 'skill-on' else None

    record = {
        'run_id': str(uuid.uuid4()),
        'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'model': model,
        'canonical_model': env.get('canonical_model', model),
        'effort': effort,
        'condition': condition,
        'family': scenario['family'],
        'scenario_id': scenario['id'],
        'scenario_prompt': scenario['prompt'],
        'skill_sha': skill_sha,
        'repeat': repeat,
        'text': text,
        'usage': usage,
        'cost_usd': env.get('total_cost_usd', env.get('cost_usd')),
        'duration_ms': env.get('duration_ms'),
        'cli_version': env.get('cli_version'),
        'verdict': 'generated',
        'reason': None,
    }
    _write_json_atomic(path, record)
    return record, True


def _assert_family_coverage(scenarios):
    """Raise ValueError, naming the family, if any FAMILIES member has fewer
    than 2 scenarios in `scenarios`.

    This is a self-test-only completeness assertion over the shipped
    scenarios.json -- load_scenarios() itself does not enforce this (see its
    own docstring): an intermediate, partially-populated scenario file is a
    legitimate input to that generic loader, but the SHIPPED file must cover
    every family with at least 2 scenarios each.
    """
    counts = {}
    for scenario in scenarios:
        counts[scenario['family']] = counts.get(scenario['family'], 0) + 1
    under = [family for family in FAMILIES if counts.get(family, 0) < 2]
    if under:
        raise ValueError(f'family coverage incomplete, fewer than 2 scenarios: {under}')


def run_matrix(models, conditions, scenarios, repeats, skill_src, raw_dir, timeout_s,
               effort=DEFAULT_EFFORT, max_budget_usd=MAX_BUDGET_USD, generation_fn=run_generation):
    """Enumerate model x condition x scenario x repeat, in that nesting
    order, and drive one generation per cell via `generation_fn` (defaults
    to run_generation).

    Single-writer-per-path rule, in evals/conformance/run_conformance.py's
    own words: exactly one call site writes any given raw path, and this
    runner never parallelises onto a shared path.

    `generation_fn` defaults to run_generation() -- which already skips a
    cell whose raw file exists and makes no subprocess call for it -- but
    self_test() injects stubs with the identical keyword signature so the
    enumeration order, the skip-if-exists property, and the durability-on-
    interruption property are all checkable offline, with no `claude`
    binary and no network call.

    On SessionFailedError from `generation_fn`, writes an `unscoreable`
    record carrying the real reason to the cell's raw path rather than
    raising out of the loop and losing the rest of the run -- an
    interruption by any OTHER exception type (a genuine process kill, or a
    self-test-injected KeyboardInterrupt) still propagates immediately,
    leaving on disk exactly the records already written by cells before it.

    Returns the full list of (model, condition, scenario_id, repeat) tuples
    this call enumerated, in the documented deterministic order -- derived
    from the JSON array order of `scenarios` and the caller-supplied
    `models`/`conditions`/`repeats`, never from dict iteration order.
    """
    raw_dir = pathlib.Path(raw_dir) if raw_dir is not None else RAW_DIR
    todo = []
    for model in models:
        for condition in conditions:
            for scenario in scenarios:
                for repeat in range(repeats):
                    todo.append((model, condition, scenario, repeat))

    for model, condition, scenario, repeat in todo:
        try:
            generation_fn(
                model=model, effort=effort, condition=condition, scenario=scenario,
                repeat=repeat, skill_src=skill_src, timeout_s=timeout_s,
                raw_dir=raw_dir, max_budget_usd=max_budget_usd,
            )
        except SessionFailedError as exc:
            record = _unscoreable_generation_record(
                model, effort, condition, scenario, repeat, skill_src,
                reason=f'nonzero exit or is_error: returncode={exc.returncode} stderr={exc.stderr!r}',
            )
            path = raw_path_for_generation(model, condition, scenario['id'], repeat, raw_dir)
            _write_json_atomic(path, record)

    return [(model, condition, scenario['id'], repeat) for (model, condition, scenario, repeat) in todo]


def self_test():
    """Offline proof of the generation-record schema and its failure paths.
    No subprocess call, no network call; runs on a machine with no `claude`
    binary. Extended by later tasks in this plan with run_matrix(),
    load_raw_records(), aggregate(), and build_results_md() assertions.
    """
    all_ok = True
    cases_exercised = []

    fake_scenario = {
        'id': 'exec-summary-1',
        'family': 'executive-summary',
        'prompt': 'Write a two-paragraph executive summary.',
    }
    fake_skill_src = REPO_ROOT / 'skills' / 'proof-first'

    # --- load_scenarios(): duplicate id, missing family, unknown family, empty file ---
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = pathlib.Path(tmp)

        dup_path = tmp_path / 'dup.json'
        dup_path.write_text(json.dumps([
            {'id': 'x-1', 'family': 'rfp-rfi', 'prompt': 'a'},
            {'id': 'x-1', 'family': 'solution-proposal', 'prompt': 'b'},
        ]))
        try:
            load_scenarios(dup_path)
            print('FAIL: load_scenarios did not raise on duplicate id')
            all_ok = False
        except ValueError as exc:
            if 'x-1' not in str(exc):
                print(f'FAIL: duplicate-id error does not name the id: {exc}')
                all_ok = False
            else:
                cases_exercised.append('duplicate-id')

        missing_family_path = tmp_path / 'missing-family.json'
        missing_family_path.write_text(json.dumps([{'id': 'y-1', 'prompt': 'a'}]))
        try:
            load_scenarios(missing_family_path)
            print('FAIL: load_scenarios did not raise on missing family')
            all_ok = False
        except ValueError as exc:
            if 'y-1' not in str(exc):
                print(f'FAIL: missing-family error does not name the id: {exc}')
                all_ok = False
            else:
                cases_exercised.append('missing-family')

        bad_family_path = tmp_path / 'bad-family.json'
        bad_family_path.write_text(json.dumps([{'id': 'z-1', 'family': 'onboarding', 'prompt': 'a'}]))
        try:
            load_scenarios(bad_family_path)
            print('FAIL: load_scenarios did not raise on unknown family')
            all_ok = False
        except ValueError as exc:
            if 'onboarding' not in str(exc):
                print(f'FAIL: unknown-family error does not name the family: {exc}')
                all_ok = False
            else:
                cases_exercised.append('unknown-family')

        empty_path = tmp_path / 'empty.json'
        empty_path.write_text('[]')
        try:
            load_scenarios(empty_path)
            print('FAIL: load_scenarios did not raise on zero scenarios')
            all_ok = False
        except ValueError:
            cases_exercised.append('empty-scenarios-file')

    real_subprocess_run = subprocess.run

    # --- success envelope: full schema, written to the frozen filename template ---
    success_envelope = json.loads(
        (FIXTURES_DIR / 'generation-success-envelope.json').read_text(encoding='utf-8')
    )

    def _fake_success_run(argv, **kwargs):
        return subprocess.CompletedProcess(argv, returncode=0, stdout=json.dumps(success_envelope), stderr='')

    with tempfile.TemporaryDirectory() as tmp:
        raw_dir = pathlib.Path(tmp)
        subprocess.run = _fake_success_run
        try:
            record, wrote = run_generation(
                model='claude-sonnet-5', effort='low', condition='skill-off',
                scenario=fake_scenario, repeat=0, skill_src=fake_skill_src,
                timeout_s=30, raw_dir=raw_dir,
            )
        finally:
            subprocess.run = real_subprocess_run

        written_path = raw_path_for_generation('claude-sonnet-5', 'skill-off', 'exec-summary-1', 0, raw_dir)
        missing_fields = [f for f in GENERATION_RECORD_FIELDS if f not in record]
        if missing_fields:
            print(f'FAIL: success-envelope record missing fields: {missing_fields}')
            all_ok = False
        elif not wrote:
            print('FAIL: success-envelope run reported wrote=False for a fresh cell')
            all_ok = False
        elif not written_path.exists():
            print(f'FAIL: success-envelope run did not write {written_path}')
            all_ok = False
        elif record['verdict'] != 'generated':
            print(f"FAIL: success-envelope record verdict expected generated, got {record['verdict']!r}")
            all_ok = False
        else:
            cases_exercised.append('success')

        # skip-if-exists: re-running the identical cell must make zero subprocess calls.
        def _fail_if_called(argv, **kwargs):
            raise AssertionError('subprocess.run should not be called for an existing raw file')

        subprocess.run = _fail_if_called
        try:
            record2, wrote2 = run_generation(
                model='claude-sonnet-5', effort='low', condition='skill-off',
                scenario=fake_scenario, repeat=0, skill_src=fake_skill_src,
                timeout_s=30, raw_dir=raw_dir,
            )
        finally:
            subprocess.run = real_subprocess_run
        if wrote2:
            print('FAIL: re-running an existing cell reported wrote=True')
            all_ok = False
        elif record2 != record:
            print('FAIL: re-running an existing cell returned a different record')
            all_ok = False
        else:
            cases_exercised.append('skip-if-exists')

    # --- non-zero exit: raises SessionFailedError; caller records unscoreable ---
    def _fake_failed_run(argv, **kwargs):
        return subprocess.CompletedProcess(argv, returncode=1, stdout='', stderr='usage limit reached, resets 2:20pm')

    with tempfile.TemporaryDirectory() as tmp:
        raw_dir = pathlib.Path(tmp)
        subprocess.run = _fake_failed_run
        raised = None
        try:
            run_generation(
                model='claude-sonnet-5', effort='low', condition='skill-off',
                scenario=fake_scenario, repeat=1, skill_src=fake_skill_src,
                timeout_s=30, raw_dir=raw_dir,
            )
        except SessionFailedError as exc:
            raised = exc
        finally:
            subprocess.run = real_subprocess_run

        if raised is None:
            print('FAIL: non-zero exit did not raise SessionFailedError')
            all_ok = False
        else:
            unscoreable = _unscoreable_generation_record(
                'claude-sonnet-5', 'low', 'skill-off', fake_scenario, 1, fake_skill_src,
                reason=f'nonzero exit {raised.returncode}: {raised.stderr!r}',
            )
            if unscoreable['verdict'] != 'unscoreable' or not unscoreable['reason']:
                print(f'FAIL: unscoreable record malformed: {unscoreable}')
                all_ok = False
            else:
                cases_exercised.append('non-zero-exit')

    # --- is_error: true envelope: handled identically to a non-zero exit ---
    def _fake_is_error_run(argv, **kwargs):
        return subprocess.CompletedProcess(
            argv, returncode=0,
            stdout=json.dumps({'is_error': True, 'result': 'overloaded_error', 'type': 'result'}),
            stderr='',
        )

    with tempfile.TemporaryDirectory() as tmp:
        raw_dir = pathlib.Path(tmp)
        subprocess.run = _fake_is_error_run
        raised = None
        try:
            run_generation(
                model='claude-sonnet-5', effort='low', condition='skill-off',
                scenario=fake_scenario, repeat=2, skill_src=fake_skill_src,
                timeout_s=30, raw_dir=raw_dir,
            )
        except SessionFailedError as exc:
            raised = exc
        finally:
            subprocess.run = real_subprocess_run
        if raised is None:
            print('FAIL: is_error envelope did not raise SessionFailedError')
            all_ok = False
        else:
            cases_exercised.append('is-error')

    # --- array-shaped envelope (CLI >= 2.1 message-stream shape) ---
    array_envelope = [
        {'type': 'system', 'subtype': 'init'},
        dict(success_envelope, type='result'),
    ]

    def _fake_array_run(argv, **kwargs):
        return subprocess.CompletedProcess(argv, returncode=0, stdout=json.dumps(array_envelope), stderr='')

    with tempfile.TemporaryDirectory() as tmp:
        raw_dir = pathlib.Path(tmp)
        subprocess.run = _fake_array_run
        try:
            record3, _wrote3 = run_generation(
                model='claude-sonnet-5', effort='low', condition='skill-off',
                scenario=fake_scenario, repeat=3, skill_src=fake_skill_src,
                timeout_s=30, raw_dir=raw_dir,
            )
        finally:
            subprocess.run = real_subprocess_run
        if record3['verdict'] != 'generated':
            print(f"FAIL: array-envelope record verdict expected generated, got {record3['verdict']!r}")
            all_ok = False
        else:
            cases_exercised.append('array-envelope')

    # --- committed fixtures cross-check: the fixture envelope, run through
    # run_generation(), reproduces the committed example record's schema
    # (field set and verdict), proving the schema is a committed artifact
    # rather than only an inline dict. Timestamps/run_id are expected to
    # differ; those two fields are excluded from the comparison. ---
    example_record = json.loads(
        (FIXTURES_DIR / 'generation-record-example.json').read_text(encoding='utf-8')
    )
    if set(example_record) != set(GENERATION_RECORD_FIELDS):
        print(f'FAIL: committed fixture record fields do not match GENERATION_RECORD_FIELDS: {sorted(set(example_record))}')
        all_ok = False
    else:
        cases_exercised.append('committed-fixture-schema')

    # --- scenario prompts never cue the skill-off condition toward this
    # project's own rule vocabulary (leakage control, Decision 2). ---
    shipped_scenarios = load_scenarios()
    leaked = [
        (s['id'], token)
        for s in shipped_scenarios
        for token in FORBIDDEN_PROMPT_TOKENS
        if token.lower() in s['prompt'].lower()
    ]
    if leaked:
        print(f'FAIL: scenario prompt(s) leak forbidden tokens: {leaked}')
        all_ok = False
    else:
        cases_exercised.append('no-vocabulary-leakage')

    # --- bench-deal-brief.md shares no named entity with examples/deal-brief.md ---
    shared_deal_brief_entities = ('Halverton Mutual', 'Kestrel Systems Group', 'Diane Osoria', 'Marcus Feld')
    bench_deal_brief_text = (BENCHMARK_DIR / 'bench-deal-brief.md').read_text(encoding='utf-8')
    collisions = [name for name in shared_deal_brief_entities if name in bench_deal_brief_text]
    if collisions:
        print(f'FAIL: bench-deal-brief.md reuses shared-deal-brief entities: {collisions}')
        all_ok = False
    else:
        cases_exercised.append('no-entity-collision')

    # --- family-coverage assertion: the shipped scenarios.json carries
    # exactly 8 scenarios, exactly 2 per family; a negative fixture with a
    # family carrying only 1 scenario fails the same assertion, naming it. ---
    shipped_counts = {}
    for scenario in shipped_scenarios:
        shipped_counts[scenario['family']] = shipped_counts.get(scenario['family'], 0) + 1
    if len(shipped_scenarios) != 8 or set(shipped_counts.values()) != {2} or set(shipped_counts) != set(FAMILIES):
        print(f'FAIL: shipped scenarios.json family coverage wrong: {shipped_counts} (total {len(shipped_scenarios)})')
        all_ok = False
    else:
        try:
            _assert_family_coverage(shipped_scenarios)
            cases_exercised.append('family-coverage-positive')
        except ValueError as exc:
            print(f'FAIL: _assert_family_coverage raised on the shipped, fully-covered file: {exc}')
            all_ok = False

    under_covered = [s for s in shipped_scenarios if s['family'] != 'executive-summary'] + [shipped_scenarios[0]]
    try:
        _assert_family_coverage(under_covered)
        print('FAIL: _assert_family_coverage did not raise on a 1-scenario family')
        all_ok = False
    except ValueError as exc:
        if 'executive-summary' not in str(exc):
            print(f'FAIL: family-coverage error does not name the under-covered family: {exc}')
            all_ok = False
        else:
            cases_exercised.append('family-coverage-negative')

    # --- cell-enumeration assertion: the default matrix (2 models x 2
    # conditions x 8 scenarios x 3 repeats) enumerates exactly 96 cells, in
    # the documented (model, condition, scenario, repeat) nesting order --
    # the expected count is computed from the frozen tuples, never
    # hardcoded as a bare literal in the assertion message alone. ---
    expected_cell_count = len(DEFAULT_MODELS) * len(CONDITIONS) * len(shipped_scenarios) * DEFAULT_REPEATS
    expected_order = []
    for model in DEFAULT_MODELS:
        for condition in CONDITIONS:
            for scenario in shipped_scenarios:
                for repeat in range(DEFAULT_REPEATS):
                    expected_order.append((model, condition, scenario['id'], repeat))

    with tempfile.TemporaryDirectory() as tmp:
        raw_dir = pathlib.Path(tmp)
        subprocess.run = _fake_success_run
        try:
            cells = run_matrix(
                models=list(DEFAULT_MODELS), conditions=list(CONDITIONS),
                scenarios=shipped_scenarios, repeats=DEFAULT_REPEATS,
                skill_src=fake_skill_src, raw_dir=raw_dir, timeout_s=30,
            )
        finally:
            subprocess.run = real_subprocess_run

    if len(cells) != expected_cell_count:
        print(f'FAIL: run_matrix() default-matrix cell count expected {expected_cell_count}, got {len(cells)}')
        all_ok = False
    elif cells != expected_order:
        print('FAIL: run_matrix() default-matrix cell order does not match the documented nesting order')
        all_ok = False
    else:
        cases_exercised.append('cell-enumeration-96')

    # --- skip-if-exists at the run_matrix() level: a fully-populated raw
    # directory makes exactly 0 subprocess calls, asserted by a call
    # counter (not merely by run_generation()'s own single-cell property,
    # which case "skip-if-exists" above already proved). ---
    call_counter = {'n': 0}

    def _counting_run(argv, **kwargs):
        call_counter['n'] += 1
        return subprocess.CompletedProcess(argv, returncode=0, stdout=json.dumps(success_envelope), stderr='')

    small_scenarios = shipped_scenarios[:2]
    with tempfile.TemporaryDirectory() as tmp:
        raw_dir = pathlib.Path(tmp)
        subprocess.run = _fake_success_run
        try:
            run_matrix(
                models=['claude-sonnet-5'], conditions=['skill-off'],
                scenarios=small_scenarios, repeats=1,
                skill_src=fake_skill_src, raw_dir=raw_dir, timeout_s=30,
            )
        finally:
            subprocess.run = real_subprocess_run

        subprocess.run = _counting_run
        try:
            run_matrix(
                models=['claude-sonnet-5'], conditions=['skill-off'],
                scenarios=small_scenarios, repeats=1,
                skill_src=fake_skill_src, raw_dir=raw_dir, timeout_s=30,
            )
        finally:
            subprocess.run = real_subprocess_run

    if call_counter['n'] != 0:
        print(f"FAIL: run_matrix() over a fully-populated raw dir made {call_counter['n']} subprocess calls, expected 0")
        all_ok = False
    else:
        cases_exercised.append('run-matrix-skip-if-exists')

    # --- durability on interruption: a stub generation_fn that writes a
    # record for each of its first two calls and then raises
    # KeyboardInterrupt on its third leaves exactly 2 records readable on
    # disk when run_matrix() propagates that interruption -- proven by
    # reading the files back, not by inspecting an in-memory list. ---
    interrupt_state = {'n': 0}

    def _interrupt_stub(model, effort, condition, scenario, repeat, skill_src, timeout_s,
                         raw_dir, max_budget_usd):
        interrupt_state['n'] += 1
        if interrupt_state['n'] >= 3:
            raise KeyboardInterrupt('simulated interruption between cells')
        record = _unscoreable_generation_record(model, effort, condition, scenario, repeat, skill_src, reason=None)
        record['verdict'] = 'generated'
        record['text'] = 'stub generated text'
        path = raw_path_for_generation(model, condition, scenario['id'], repeat, raw_dir)
        _write_json_atomic(path, record)
        return record, True

    with tempfile.TemporaryDirectory() as tmp:
        raw_dir = pathlib.Path(tmp)
        interrupted = False
        try:
            run_matrix(
                models=['claude-sonnet-5'], conditions=['skill-off'],
                scenarios=shipped_scenarios, repeats=1,
                skill_src=fake_skill_src, raw_dir=raw_dir, timeout_s=30,
                generation_fn=_interrupt_stub,
            )
        except KeyboardInterrupt:
            interrupted = True

        written = sorted(raw_dir.glob('*.json'))
        if not interrupted:
            print('FAIL: run_matrix() durability-on-interruption expected KeyboardInterrupt, none raised')
            all_ok = False
        elif len(written) != 2:
            print(f'FAIL: run_matrix() durability-on-interruption expected exactly 2 records on disk, found {len(written)}: {written}')
            all_ok = False
        else:
            readable = [json.loads(p.read_text(encoding='utf-8')) for p in written]
            if not all(r['verdict'] == 'generated' for r in readable):
                print(f'FAIL: run_matrix() durability-on-interruption records not all generated: {readable}')
                all_ok = False
            else:
                cases_exercised.append('run-matrix-durability-on-interruption')

    if not all_ok:
        return False

    print('self-test PASS - fake-envelope cases exercised: ' + ', '.join(cases_exercised))
    return True


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--self-test', action='store_true',
                         help='Offline proof; makes no subprocess or network call.')
    parser.add_argument('--models', default=','.join(DEFAULT_MODELS),
                         help=f'Comma-separated model ids (default: {",".join(DEFAULT_MODELS)}).')
    parser.add_argument('--repeats', type=int, default=DEFAULT_REPEATS,
                         help=f'Repeats per model x condition x scenario cell (default: {DEFAULT_REPEATS}).')
    parser.add_argument('--effort', default=DEFAULT_EFFORT,
                         help=f'Reasoning effort level passed to --effort (default: {DEFAULT_EFFORT}).')
    parser.add_argument('--scenarios', default=str(SCENARIOS_PATH),
                         help='Path to the scenarios JSON file.')
    parser.add_argument('--skill-src', default='skills/proof-first',
                         help='Path to the skill directory to copy into skill-on sessions.')
    parser.add_argument('--raw-dir', default=str(RAW_DIR),
                         help='Directory for committed raw generation/judgement records.')
    parser.add_argument('--out', default=str(RESULTS_PATH),
                         help='RESULTS.md path (only used by --report-only).')
    parser.add_argument('--timeout', type=int, default=600,
                         help='Per-session timeout in seconds (default: 600).')
    parser.add_argument('--max-budget-usd', type=float, default=MAX_BUDGET_USD,
                         help=f'Per-session cost cap passed to --max-budget-usd (default: {MAX_BUDGET_USD}).')
    parser.add_argument('--report-only', action='store_true',
                         help='Offline recompute of RESULTS.md from --raw-dir; makes no subprocess call.')
    args = parser.parse_args()

    if args.self_test:
        ok = self_test()
        sys.exit(0 if ok else 1)

    print(
        'Live matrix and --report-only aggregation are not yet implemented in this plan '
        '(see 05-02-PLAN.md Tasks 2 and 3).',
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == '__main__':
    main()
