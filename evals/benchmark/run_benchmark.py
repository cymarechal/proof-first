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


# Rubric dimensions, each scored independently (Decision 5) so persuasive
# force cannot be inferred from the other two.
JUDGE_DIMENSIONS = ('evidence', 'clarity', 'persuasive_force')
JUDGE_VERDICTS = ('scored', 'unscoreable')

JUDGE_MODEL = 'claude-opus-5'
JUDGE_EFFORT = 'high'

# Every field a judgement record must carry (Decision 7's frozen schema,
# scores nested {dimension: {condition: value}} per 05-02-SUMMARY.md's
# documented refinement). self_test() asserts a record is never missing one
# of these.
JUDGEMENT_RECORD_FIELDS = (
    'run_id', 'timestamp', 'judge_model', 'judge_effort', 'scenario_id', 'model',
    'repeat', 'order', 'text_a_condition', 'text_b_condition', 'scores',
    'raw_judge_output', 'verdict', 'reason',
)

# The judge reply is validated against this schema in Python after parsing,
# regardless of what --json-schema enforced on the CLI side (T-05-13). One
# call per (pair, order) must produce scores for BOTH anonymous texts -- the
# 96-judge-call total in 05-RESEARCH.md Decision 4 (48 pairs x 2 orders) only
# balances if a single call scores both texts, not one -- so JUDGE_SCHEMA
# nests the three required 0-10 integer dimension keys under two top-level
# keys, text_a and text_b, rather than a single flat 3-key object. This is a
# documented refinement of the plan's own "JUDGE_SCHEMA ... requiring exactly
# those three keys as integers" text, read as describing the per-text leaf
# shape (each of text_a/text_b requires exactly JUDGE_DIMENSIONS as 0-10
# integers, additionalProperties false) rather than a flat top-level object,
# which cannot carry two texts' worth of scores in one call.
_JUDGE_TEXT_SCHEMA = {
    'type': 'object',
    'properties': {dim: {'type': 'integer', 'minimum': 0, 'maximum': 10} for dim in JUDGE_DIMENSIONS},
    'required': list(JUDGE_DIMENSIONS),
    'additionalProperties': False,
}
JUDGE_SCHEMA = {
    'type': 'object',
    'properties': {'text_a': _JUDGE_TEXT_SCHEMA, 'text_b': _JUDGE_TEXT_SCHEMA},
    'required': ['text_a', 'text_b'],
    'additionalProperties': False,
}

# The two figure sections a rendered report always carries, kept separate
# and never blended into one composite number (EVAL-09).
RESULTS_SECTION_HEADINGS = ('## Mechanical proxy counts', '## Judged persuasion')

# The five caveats EVAL-10 requires, named as dict keys so build_results_md()
# builds its caveats section FROM this constant -- the list this file's own
# self-test checks against cannot silently drift from what the renderer
# actually emits, because both read the same five keys.
REQUIRED_CAVEATS = (
    'position bias',
    'judge-family bias',
    'baseline prompt parity',
    'proxy provenance',
    'sample size',
    'judge construct validity',
)

CAVEAT_TEXT = {
    'position bias': (
        'Position bias: every judged pair is scored in both orders (order1/order2, with which '
        'text is labeled A and which is labeled B swapped) and the two orders are averaged per '
        'dimension before this report reads them -- that averaging is what cancels position bias, '
        'not merely a disclosure that it exists.'
    ),
    'judge-family bias': (
        'Judge-family bias: the judge is a Claude model and the texts are Claude output, so '
        'family bias is possible.'
    ),
    'baseline prompt parity': (
        'Baseline prompt parity: the skill-off condition receives a materially shorter prompt (no '
        'skill text, no explicit instruction to attach evidence or watch sentence length) than '
        'skill-on. This measures default, unguided model behavior against skill-guided behavior, '
        'not against the best a careful human prompt-writer could achieve without the skill.'
    ),
    'proxy provenance': (
        'Proxy provenance: the mechanical proxy counts above come from evals/lint.py, whose own '
        'docstring states it counts observable proxies for the rules, not the rules themselves -- '
        'a violation count is not a compliance verdict on a document.'
    ),
    'sample size': (
        f'Sample size: each cell above is measured at {DEFAULT_REPEATS} repeats. This sample size '
        'is not powered to detect statistical significance; treat differences smaller than the '
        'observed range as noise. Every mean is rounded to one decimal place using Python\'s '
        'default round-half-to-even rule; the unrounded values remain recoverable from '
        'evals/benchmark/raw/.'
    ),
    'judge construct validity': (
        'Judge construct validity: the scores under Judged persuasion are one language model\'s '
        'rating of these texts against the rubric build_judge_prompt() sends it -- a proxy for '
        'how a technical evaluator might react, not a measurement of real buyer behavior or of '
        'any commercial outcome. No human evaluator scored any of these texts, and no score here '
        'should be read as predicting one.'
    ),
}


def build_judge_prompt(text_a, text_b):
    """Build the blind pairwise judge prompt for two anonymous texts.

    Presents `text_a` and `text_b` under the anonymous labels TEXT A / TEXT B
    and asks for independent 0-10 scores on three dimensions, described in
    ordinary language rather than this project's own rule vocabulary. The
    built string must never contain a condition name ('skill-on'/
    'skill-off'), this project's name ('proof-first'/'Proof First'), or a
    PF-/MC- rule-namespace token -- self_test()'s label-stripping assertion
    scans this function's OUTPUT, not its source, so the check is against
    what the judge model actually sees.

    `text_a`/`text_b` are embedded verbatim -- the two texts reach the judge
    exactly as the generation records stored them, UTF-8 and unnormalised,
    with no transformation beyond the label-stripping this function already
    performs by never naming which condition produced which text. No
    truncation is applied here; the judge session's own timeout is the only
    length bound this module imposes.

    The persuasive_force dimension is worded to ask a question the clarity
    dimension does not (a short, active-voiced, one-claim-per-sentence text
    can still read as a checklist and score low on persuasive_force while
    scoring high on clarity) -- 05-RESEARCH.md Decision 5's own requirement.
    """
    return (
        'You are evaluating two pieces of presales writing, labeled TEXT A and TEXT B below. '
        'Score EACH text independently on three dimensions, each an integer from 0 to 10. Score '
        'each text on its own merits -- do not let one text\'s score influence the other\'s.\n\n'
        'Dimensions:\n'
        '1. evidence -- does every claim in the text carry a number, a named source, or an '
        'explicit statement that the fact is missing, with no fabricated figures, reference '
        'customers, or benchmarks. A text stating unsupported claims as plain fact scores low; a '
        'text that backs its claims or clearly states what it cannot yet prove scores high.\n'
        '2. clarity -- sentence length, active voice, and one claim per sentence. A text with '
        'long, passive, or claim-stacked sentences scores low; short, active, single-claim '
        'sentences score high.\n'
        '3. persuasive_force -- would a technical evaluator finish this text believing the '
        'author genuinely understands their specific problem, reading it as a coherent case for '
        'a decision rather than a checklist of features. Score this independently of clarity: a '
        'short, clean, well-organized text can still read as a checklist and score low here, '
        'while a text that builds a specific, situated argument can score high even with longer '
        'sentences.\n\n'
        f'TEXT A:\n{text_a}\n\n'
        f'TEXT B:\n{text_b}\n\n'
        'Reply with integer scores from 0 to 10 for both texts on all three dimensions.'
    )


def _judge_prompt_label_violations(prompt):
    """Return the list of forbidden strings found in `prompt`: a condition
    name, this project's name, or a PF-/MC- rule-namespace token.

    Checked against the string build_judge_prompt() actually returns, never
    against its source template -- exactly what self_test()'s label-
    stripping assertion requires.
    """
    forbidden_substrings = ('skill-on', 'skill-off', 'proof-first', 'proof first', 'Proof First')
    found = [token for token in forbidden_substrings if token.lower() in prompt.lower()]
    if re.search(r'\bPF-\d', prompt):
        found.append('PF-<digit>')
    if re.search(r'\bMC-\d', prompt):
        found.append('MC-<digit>')
    return found


def _validate_judge_reply(raw_text):
    """Parse and validate a judge reply string against JUDGE_SCHEMA's key
    set and 0-10 integer bounds, in Python, regardless of what --json-schema
    enforced on the CLI side (T-05-13's Python-side re-validation).

    Returns (scores_by_text, None) on success, where scores_by_text is
    {'text_a': {dim: int}, 'text_b': {dim: int}} for every dim in
    JUDGE_DIMENSIONS -- or (None, reason) on any failure: unparseable JSON, a
    non-dict top level, a missing/extra text_a/text_b key, a missing/extra
    dimension key inside either (a reply missing persuasive_force names it
    in `reason` via the `missing` list), a non-integer score (bool is
    explicitly rejected even though Python's bool is an int subclass), or a
    score outside [0, 10]. Never raises -- the caller records `reason` as
    the unscoreable reason and the record contributes to no mean.
    """
    try:
        reply = json.loads(raw_text)
    except (json.JSONDecodeError, TypeError) as exc:
        return None, f'unparseable judge reply: {exc}'

    if not isinstance(reply, dict):
        return None, f'judge reply is not a JSON object: {raw_text[:200]!r}'

    if set(reply) != {'text_a', 'text_b'}:
        return None, f'judge reply top-level keys expected exactly text_a, text_b, got {sorted(reply)}'

    scores_by_text = {}
    for text_key in ('text_a', 'text_b'):
        sub = reply[text_key]
        if not isinstance(sub, dict):
            return None, f'judge reply {text_key!r} is not a JSON object'
        if set(sub) != set(JUDGE_DIMENSIONS):
            missing = [d for d in JUDGE_DIMENSIONS if d not in sub]
            extra = [k for k in sub if k not in JUDGE_DIMENSIONS]
            return None, (
                f'judge reply {text_key!r} keys do not match JUDGE_DIMENSIONS exactly '
                f'(missing={missing}, extra={extra})'
            )
        parsed = {}
        for dim in JUDGE_DIMENSIONS:
            value = sub[dim]
            if isinstance(value, bool) or not isinstance(value, int):
                return None, f'judge reply {text_key!r}.{dim} is not an integer: {value!r}'
            if not (0 <= value <= 10):
                return None, f'judge reply {text_key!r}.{dim} is out of range 0-10: {value!r}'
            parsed[dim] = value
        scores_by_text[text_key] = parsed

    return scores_by_text, None


def _unscoreable_judgement_record(judge_model, judge_effort, scenario_id, model, repeat, order,
                                   text_a_condition, text_b_condition, reason, raw_judge_output=None):
    """Build an `unscoreable` judgement record with the given `reason`.

    Used both by run_judgement() itself (a reply that parses but fails
    JUDGE_SCHEMA validation) and by run_judge_matrix() (a SessionFailedError
    from a non-zero exit, an is_error envelope, or an unparseable envelope --
    handled identically to the generation path, per this task's own
    behavior spec).
    """
    return {
        'run_id': str(uuid.uuid4()),
        'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'judge_model': judge_model,
        'judge_effort': judge_effort,
        'scenario_id': scenario_id,
        'model': model,
        'repeat': repeat,
        'order': order,
        'text_a_condition': text_a_condition,
        'text_b_condition': text_b_condition,
        'scores': None,
        'raw_judge_output': raw_judge_output,
        'verdict': 'unscoreable',
        'reason': reason,
    }


def run_judgement(pair, order, judge_model, judge_effort, timeout_s,
                   raw_dir=None, max_budget_usd=MAX_BUDGET_USD):
    """Drive one isolated-temp-dir `claude -p` judge session for one order of
    one (model, scenario_id, repeat) pair, write the resulting record to its
    frozen filename template, and return (record, wrote_new).

    `pair` is a dict carrying `model`, `scenario_id`, `repeat`,
    `skill_on_text`, and `skill_off_text`. `order` is 1 (TEXT A = skill-off,
    TEXT B = skill-on) or 2 (TEXT A = skill-on, TEXT B = skill-off) -- the
    both-orders swap that cancels position bias (05-RESEARCH.md Decision 5).

    Installs no skill folder into the session's temp dir, unconditionally --
    the judge must never run under the skill it is scoring (T-05-19).

    `wrote_new` is False when the cell's raw file already existed -- the same
    skip-if-exists resumability run_generation() already provides.

    Raises SessionFailedError on a non-zero exit, an `is_error: true`
    envelope, or an unparseable envelope -- exactly the generation path's own
    trigger set. The caller (run_judge_matrix, or this file's own self-test
    acting as a single-cell caller) is responsible for catching that and
    writing an `unscoreable` record instead of letting the failure propagate
    out of the whole pass.

    A reply that parses but fails JUDGE_SCHEMA validation (missing
    persuasive_force, an out-of-range or non-integer score, or a schema-
    invalid shape) does NOT raise -- exactly like run_generation()'s empty-
    text case, this function writes and returns an `unscoreable` record
    directly, with `reason` naming the validation failure.
    """
    raw_dir = pathlib.Path(raw_dir) if raw_dir is not None else RAW_DIR
    model = pair['model']
    scenario_id = pair['scenario_id']
    repeat = pair['repeat']

    path = raw_path_for_judgement(model, scenario_id, repeat, order, raw_dir)
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8')), False

    if order == 1:
        text_a_condition, text_b_condition = 'skill-off', 'skill-on'
    elif order == 2:
        text_a_condition, text_b_condition = 'skill-on', 'skill-off'
    else:
        raise ValueError(f'order must be 1 or 2, got {order!r}')

    text_a = pair['skill_off_text'] if text_a_condition == 'skill-off' else pair['skill_on_text']
    text_b = pair['skill_off_text'] if text_b_condition == 'skill-off' else pair['skill_on_text']
    prompt = build_judge_prompt(text_a, text_b)

    tmp_dir = pathlib.Path(tempfile.mkdtemp(prefix='proof-first-benchmark-judge-'))
    try:
        argv = [
            'claude', '-p', prompt,
            '--model', judge_model,
            '--effort', judge_effort,
            '--output-format', 'json',
            '--json-schema', json.dumps(JUDGE_SCHEMA),
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

    raw_judge_output = env.get('result', '') or ''
    scores_by_text, reason = _validate_judge_reply(raw_judge_output)

    record_base = {
        'run_id': str(uuid.uuid4()),
        'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'judge_model': judge_model,
        'judge_effort': judge_effort,
        'scenario_id': scenario_id,
        'model': model,
        'repeat': repeat,
        'order': order,
        'text_a_condition': text_a_condition,
        'text_b_condition': text_b_condition,
        'raw_judge_output': raw_judge_output,
    }

    if scores_by_text is None:
        record = dict(record_base, scores=None, verdict='unscoreable', reason=reason)
        _write_json_atomic(path, record)
        return record, True

    scores = {
        dim: {
            text_a_condition: scores_by_text['text_a'][dim],
            text_b_condition: scores_by_text['text_b'][dim],
        }
        for dim in JUDGE_DIMENSIONS
    }
    record = dict(record_base, scores=scores, verdict='scored', reason=None)
    _write_json_atomic(path, record)
    return record, True


def run_judge_matrix(models, scenarios, repeats, raw_dir, timeout_s, judge_model=JUDGE_MODEL,
                      judge_effort=JUDGE_EFFORT, max_budget_usd=MAX_BUDGET_USD, judgement_fn=run_judgement):
    """Enumerate model x scenario x repeat x order (1, 2), in that nesting
    order, and drive one judge call per cell via `judgement_fn` (defaults to
    run_judgement), reading each pair's skill-on/skill-off generation text
    from already-committed, `verdict == 'generated'` records under raw_dir.

    Mirrors run_matrix()'s SessionFailedError handling exactly: a raised
    SessionFailedError writes an `unscoreable` record carrying the real
    reason to the cell's raw path rather than raising out of the loop, so one
    judge-call failure never loses the rest of the pass. Any OTHER exception
    (a genuine interruption) still propagates immediately, leaving on disk
    exactly the records already written by cells before it.

    Skips a (model, scenario, repeat) triple with no matching skill-on and
    skill-off generation record on disk (or either not `verdict ==
    'generated'`) -- a missing or failed generation is not a judge failure
    and produces no judgement record at all, never a fabricated unscoreable
    one, since 05-RESEARCH.md's cost/count arithmetic already accounts for
    judge calls only over completed generation pairs.

    Returns the full list of (model, scenario_id, repeat, order) tuples this
    call enumerated, in the documented deterministic order.
    """
    raw_dir = pathlib.Path(raw_dir) if raw_dir is not None else RAW_DIR
    enumerated = []
    for model in models:
        for scenario in scenarios:
            scenario_id = scenario['id']
            for repeat in range(repeats):
                skill_on_path = raw_path_for_generation(model, 'skill-on', scenario_id, repeat, raw_dir)
                skill_off_path = raw_path_for_generation(model, 'skill-off', scenario_id, repeat, raw_dir)
                if not (skill_on_path.exists() and skill_off_path.exists()):
                    continue
                skill_on_record = json.loads(skill_on_path.read_text(encoding='utf-8'))
                skill_off_record = json.loads(skill_off_path.read_text(encoding='utf-8'))
                if skill_on_record.get('verdict') != 'generated' or skill_off_record.get('verdict') != 'generated':
                    continue
                pair = {
                    'model': model, 'scenario_id': scenario_id, 'repeat': repeat,
                    'skill_on_text': skill_on_record['text'], 'skill_off_text': skill_off_record['text'],
                }
                for order in (1, 2):
                    try:
                        judgement_fn(
                            pair=pair, order=order, judge_model=judge_model,
                            judge_effort=judge_effort, timeout_s=timeout_s,
                            raw_dir=raw_dir, max_budget_usd=max_budget_usd,
                        )
                    except SessionFailedError as exc:
                        text_a_condition, text_b_condition = (
                            ('skill-off', 'skill-on') if order == 1 else ('skill-on', 'skill-off')
                        )
                        record = _unscoreable_judgement_record(
                            judge_model, judge_effort, scenario_id, model, repeat, order,
                            text_a_condition, text_b_condition,
                            reason=f'nonzero exit or is_error: returncode={exc.returncode} stderr={exc.stderr!r}',
                        )
                        path = raw_path_for_judgement(model, scenario_id, repeat, order, raw_dir)
                        _write_json_atomic(path, record)
                    enumerated.append((model, scenario_id, repeat, order))
    return enumerated


def average_orders(order1, order2):
    """Return {dimension: {condition: averaged_score}} averaging `order1`
    and `order2`'s per-dimension per-condition scores, or None if either
    order is missing (None) or not `verdict == 'scored'`.

    A pair with only one order present -- or with an order present but not
    scored -- is excluded from the pair aggregate rather than counted at
    half weight (must_haves, EVAL-06 adjacency edge); the caller
    (judge_summary()) is responsible for counting that exclusion.

    Where the same condition scores the identical value in both orders (e.g.
    7 and 7), the average is exactly that value, 7.0 -- ordinary arithmetic,
    asserted directly by self_test().
    """
    if order1 is None or order2 is None:
        return None
    if order1.get('verdict') != 'scored' or order2.get('verdict') != 'scored':
        return None

    averaged = {}
    for dim in JUDGE_DIMENSIONS:
        averaged[dim] = {}
        for condition in ('skill-off', 'skill-on'):
            v1 = order1['scores'][dim][condition]
            v2 = order2['scores'][dim][condition]
            averaged[dim][condition] = (v1 + v2) / 2
    return averaged


def judge_summary(records):
    """Group judgement records into (model, scenario_id, repeat) pairs, run
    average_orders() over each pair's order1/order2, and tally win/tie/loss
    per dimension -- comparing the pair's averaged skill-on score against its
    averaged skill-off score, independently for each of the three
    dimensions.

    Returns:
      {
        'tallies': {(model, scenario_id): {dim: {'wins': n, 'ties': n, 'losses': n}}},
        'excluded_pairs': int,  -- pairs missing an order, or with an order
                                   present but not scored, excluded rather
                                   than counted at half weight
        'unscoreable': [{'model', 'scenario_id', 'repeat', 'order', 'reason'}, ...],
      }

    An exact tie (the two averaged condition scores equal) is counted as one
    tie and is never rounded, nudged, or tie-broken into a winner (must_haves,
    EVAL-06 adjacency edge). Rendering (build_results_md()) sorts `tallies`'
    keys itself for the model-then-scenario ascending row order -- this
    function's own dict does not need to be pre-sorted.
    """
    judgement_records = [r for r in records if 'judge_model' in r]

    by_pair = {}
    for record in judgement_records:
        key = (record['model'], record['scenario_id'], record['repeat'])
        by_pair.setdefault(key, {})[record['order']] = record

    unscoreable = [
        {
            'model': record['model'], 'scenario_id': record['scenario_id'],
            'repeat': record['repeat'], 'order': record['order'],
            'reason': record.get('reason'),
        }
        for record in judgement_records
        if record.get('verdict') != 'scored'
    ]

    tallies = {}
    excluded_pairs = 0
    for (model, scenario_id, _repeat), orders in by_pair.items():
        averaged = average_orders(orders.get(1), orders.get(2))
        if averaged is None:
            excluded_pairs += 1
            continue
        bucket = tallies.setdefault(
            (model, scenario_id), {dim: {'wins': 0, 'ties': 0, 'losses': 0} for dim in JUDGE_DIMENSIONS}
        )
        for dim in JUDGE_DIMENSIONS:
            skill_on = averaged[dim]['skill-on']
            skill_off = averaged[dim]['skill-off']
            if skill_on == skill_off:
                bucket[dim]['ties'] += 1
            elif skill_on > skill_off:
                bucket[dim]['wins'] += 1
            else:
                bucket[dim]['losses'] += 1

    return {'tallies': tallies, 'excluded_pairs': excluded_pairs, 'unscoreable': unscoreable}


def _load_lint_module():
    """Load evals/lint.py's `lint` function by reading and exec'ing its
    source, rather than importing it as a package.

    This module's own docstring states it imports only ten stdlib modules;
    a live `import lint` statement would need evals/ on sys.path as an
    importable package, which it is not, and would add a name this file's
    stdlib-only self-test (an AST-based import scan) would flag as extra,
    non-stdlib. `compile()`/`exec()` are builtins, not an import statement,
    so loading the module this way stays within the ten-module contract
    while still reusing evals/lint.py's real, committed `lint()` rather than
    reimplementing proxy-counting logic a second time in this file.
    """
    lint_path = BENCHMARK_DIR.parent / 'lint.py'
    namespace = {'__name__': 'proof_first_benchmark_lint', '__file__': str(lint_path)}
    exec(compile(lint_path.read_text(encoding='utf-8'), str(lint_path), 'exec'), namespace)
    return namespace['lint']


def load_raw_records(raw_dir=None):
    """Read every `*.json` file under `raw_dir`, in `sorted()` path order,
    and return the list of parsed records (generation and judgement records
    mixed together).

    Raises ValueError, naming the path, for an empty or unparseable file --
    never a silent skip, because a silently skipped record is a published
    number computed from less data than it claims. Returns an empty list
    for a directory that does not exist or contains no `*.json` files; the
    caller (generate_report()) is responsible for treating zero records as
    a hard failure with a named reason, not this generic reader.

    `sorted()` iteration means two directories holding the same files in a
    different filesystem creation order produce an identical record list.
    """
    raw_dir = pathlib.Path(raw_dir) if raw_dir is not None else RAW_DIR
    if not raw_dir.exists():
        return []
    records = []
    for path in sorted(raw_dir.glob('*.json')):
        text = path.read_text(encoding='utf-8')
        if not text.strip():
            raise ValueError(f'{path} is empty')
        try:
            records.append(json.loads(text))
        except json.JSONDecodeError as exc:
            raise ValueError(f'{path} is unparseable: {exc}')
    return records


def aggregate(records, lint_fn=None):
    """Pure function: turn a mixed list of raw records (generation +
    judgement) into `{'mechanical': {...}, 'judged': {...}}`, the two
    figure halves kept independent throughout and never blended into one
    number (EVAL-09).

    `mechanical` is keyed by (model, scenario_id, condition); each value
    reports `n` (the cell's actual record count, even when below 3 -- never
    silently treated as if it were 3), `mean`, `min`, `max` over the
    mechanical violation counts obtained by loading evals/lint.py's own
    `lint()` and running it on each generation's text.

    `judged` is keyed by (model, scenario_id); each value maps a condition
    ('skill-off'/'skill-on') to a per-dimension `n`/`mean`/`min`/`max` over
    that dimension's scores, pooled across every repeat and both judge
    orders (the swap that cancels position bias).

    Expects each judgement record's `scores` field nested as
    `{dimension: {condition: value}}` (e.g. `{"persuasive_force": {"skill-on":
    8, "skill-off": 5}}`) -- a documented refinement of 05-RESEARCH.md
    Decision 7's worked example, whose flat `{dimension: value}` sketch does
    not by itself say which text (A or B) a given number belongs to, which
    Decision 5's own both-orders-average-per-dimension arithmetic requires
    knowing. Every top-level field name in Decision 7's schema (run_id,
    timestamp, judge_model, judge_effort, scenario_id, model, repeat, order,
    text_a_condition, text_b_condition, scores, raw_judge_output, verdict,
    reason) is unchanged; only the internal shape of `scores`' value is
    resolved here, since a live judge-calling function is out of this
    plan's scope (05-03's to build) and this file must still be able to
    aggregate whatever schema that caller produces.

    Computes no standard deviation, no confidence interval, and no p-value:
    a sample stdev from n=3 divides by n-1=2 and is enormously unstable,
    and reporting one would look more rigorous than the data supports. This
    is deliberate at three repeats per cell, not an omission (see
    05-RESEARCH.md's "Statistical honesty for n=3").
    """
    if lint_fn is None:
        lint_fn = _load_lint_module()

    mechanical_counts = {}
    for record in records:
        if 'judge_model' in record:
            continue
        if record.get('verdict') != 'generated':
            continue
        key = (record['model'], record['scenario_id'], record['condition'])
        count = lint_fn(record['text'])['violations_total']
        mechanical_counts.setdefault(key, []).append(count)

    mechanical = {}
    for key, counts in mechanical_counts.items():
        mechanical[key] = {
            'n': len(counts),
            'mean': round(sum(counts) / len(counts), 1),
            'min': min(counts),
            'max': max(counts),
        }

    judged_scores = {}
    for record in records:
        if 'judge_model' not in record:
            continue
        if record.get('verdict') != 'scored':
            continue
        key = (record['model'], record['scenario_id'])
        bucket = judged_scores.setdefault(
            key, {'skill-on': {d: [] for d in JUDGE_DIMENSIONS}, 'skill-off': {d: [] for d in JUDGE_DIMENSIONS}}
        )
        for dim in JUDGE_DIMENSIONS:
            dim_scores = (record.get('scores') or {}).get(dim, {})
            for condition in ('skill-on', 'skill-off'):
                if condition in dim_scores:
                    bucket[condition][dim].append(dim_scores[condition])

    judged = {}
    for key, bucket in judged_scores.items():
        judged[key] = {}
        for condition in ('skill-off', 'skill-on'):
            per_dim = {}
            for dim in JUDGE_DIMENSIONS:
                scores = bucket[condition][dim]
                if not scores:
                    continue
                per_dim[dim] = {
                    'n': len(scores),
                    'mean': round(sum(scores) / len(scores), 1),
                    'min': min(scores),
                    'max': max(scores),
                }
            if per_dim:
                judged[key][condition] = per_dim

    return {'mechanical': mechanical, 'judged': judged}


def _missing_required_caveats(text, required_caveats=REQUIRED_CAVEATS):
    """Return the subset of `required_caveats` whose key does not appear
    (case-insensitively) anywhere in `text`.
    """
    lowered = text.lower()
    return [caveat for caveat in required_caveats if caveat.lower() not in lowered]


def build_results_md(aggregated, models=None, generation_count=None, as_of_date=None,
                      required_caveats=REQUIRED_CAVEATS, judge_summary_data=None):
    """Pure function: turn aggregate()'s output into the whole RESULTS.md
    document as a string. Calling this twice on identical input returns
    byte-identical strings (EVAL-12) -- there is no timestamp-at-render-time
    or randomness anywhere in this function; every date-shaped value is an
    explicit parameter.

    Emits, in this order: a headline sentence naming the tested models, the
    date, and the total generation count in the same sentence (guarding the
    overclaim 05-RESEARCH.md Decision 8 item 1 names: a percentage figure
    with no model/date/N attached); `## Mechanical proxy counts`; `##
    Judged persuasion` (per-dimension mean/range table, then a win/tie/loss
    table from `judge_summary_data`, then excluded-pair and unscoreable-
    judgement counts); `## Honest caveats`; and `## Reproduce`. The two
    figure sections are two separately headed top-level sections and are
    never blended into one composite figure anywhere in this function
    (EVAL-09) -- there is no code path here that sums or averages a
    mechanical count together with a judged score.

    `judge_summary_data` is judge_summary()'s own return shape
    (`{'tallies', 'excluded_pairs', 'unscoreable'}`) or None. The win/tie/
    loss table's rows are emitted by iterating `sorted(tallies.items())` --
    model ascending, then scenario id ascending -- regardless of the
    dict's own insertion order, so the rendered report is byte-stable
    across runs and across a shuffled input record order (must_haves,
    EVAL-06 ordering edge).

    `required_caveats` defaults to REQUIRED_CAVEATS; self_test() calls this
    with a reduced tuple to prove the caveats section is built FROM the
    constant (so the list this file's own self-test checks against cannot
    silently drift from what actually renders), never hardcoded prose.
    """
    models = models or []
    generation_count = generation_count if generation_count is not None else 0
    as_of_date = as_of_date or '(date not supplied)'

    lines = []
    lines.append(
        f"Measured {as_of_date} across {', '.join(models) if models else 'no models'} "
        f"({generation_count} generations recorded)."
    )
    lines.append('')

    lines.append(RESULTS_SECTION_HEADINGS[0])
    lines.append('')
    if not aggregated.get('mechanical'):
        lines.append('No generation records were available to compute mechanical proxy counts.')
    else:
        lines.append('| Model | Scenario | Condition | n | Mean violations | Range |')
        lines.append('|---|---|---|---|---|---|')
        for (model, scenario_id, condition), stats in sorted(aggregated['mechanical'].items()):
            lines.append(
                f"| {model} | {scenario_id} | {condition} | {stats['n']} | {stats['mean']:.1f} "
                f"| {stats['min']}-{stats['max']} |"
            )
    lines.append('')

    lines.append(RESULTS_SECTION_HEADINGS[1])
    lines.append('')
    if not aggregated.get('judged'):
        lines.append('No judgement records were available to compute judged persuasion scores.')
    else:
        lines.append('| Model | Scenario | Condition | Dimension | n | Mean | Range |')
        lines.append('|---|---|---|---|---|---|---|')
        for (model, scenario_id), by_condition in sorted(aggregated['judged'].items()):
            for condition in ('skill-off', 'skill-on'):
                for dim in JUDGE_DIMENSIONS:
                    stats = by_condition.get(condition, {}).get(dim)
                    if not stats:
                        continue
                    lines.append(
                        f"| {model} | {scenario_id} | {condition} | {dim} | {stats['n']} "
                        f"| {stats['mean']:.1f} | {stats['min']}-{stats['max']} |"
                    )
    lines.append('')

    lines.append(
        'Win/tie/loss (skill-on vs skill-off, averaged across both judge orders), rows in '
        'model-then-scenario ascending order:'
    )
    lines.append('')
    tallies = (judge_summary_data or {}).get('tallies') or {}
    if not tallies:
        lines.append('No scored judgement pairs were available to compute a win/tie/loss table.')
    else:
        lines.append('| Model | Scenario | Dimension | Wins | Ties | Losses |')
        lines.append('|---|---|---|---|---|---|')
        for (model, scenario_id), by_dim in sorted(tallies.items()):
            for dim in JUDGE_DIMENSIONS:
                tally = by_dim.get(dim, {'wins': 0, 'ties': 0, 'losses': 0})
                lines.append(
                    f"| {model} | {scenario_id} | {dim} | {tally['wins']} | {tally['ties']} "
                    f"| {tally['losses']} |"
                )
    lines.append('')

    excluded_pairs = (judge_summary_data or {}).get('excluded_pairs', 0)
    lines.append(
        f'Excluded pairs (missing an order, or an order present but not scored): {excluded_pairs}.'
    )
    lines.append('')

    unscoreable_judgements = (judge_summary_data or {}).get('unscoreable') or []
    lines.append(f'Unscoreable judgements: {len(unscoreable_judgements)}.')
    if unscoreable_judgements:
        grouped_reasons = {}
        for item in unscoreable_judgements:
            grouped_reasons.setdefault(item.get('reason'), []).append(item)
        for reason, items in sorted(grouped_reasons.items(), key=lambda kv: (kv[0] or '')):
            lines.append(f'  - {reason}: {len(items)} record(s)')
    lines.append('')

    lines.append('## Honest caveats')
    lines.append('')
    for key in required_caveats:
        lines.append(f'- {CAVEAT_TEXT[key]}')
    lines.append('')

    lines.append('## Reproduce')
    lines.append('')
    lines.append(
        '- Live (paid) run: `python3 evals/benchmark/run_benchmark.py` (requires `claude auth '
        'status` to show `loggedIn: true`).'
    )
    lines.append(
        '- Offline recompute (free, no network/model call): '
        '`python3 evals/benchmark/run_benchmark.py --report-only`.'
    )
    lines.append('')

    return '\n'.join(lines) + '\n'


def generate_report(raw_dir=None, out_path=None, models=None, generation_count=None, as_of_date=None):
    """Offline recompute: load every raw record under `raw_dir`, aggregate,
    render RESULTS.md's text, and (if `out_path` is given) write it.

    Raises ValueError, naming the reason, if `raw_dir` contains zero
    records -- an empty report is never rendered as a successful run, and
    no file is written at `out_path` in that case.

    Makes zero subprocess calls itself, and calls nothing in this module
    that does either (load_raw_records() and aggregate() are both pure
    over already-committed files); self_test()'s no-subprocess assertion
    proves this directly by replacing subprocess.run with a function that
    raises before calling this function end to end.
    """
    records = load_raw_records(raw_dir)
    if not records:
        raise ValueError(f'no raw records found under {raw_dir} -- nothing to report')

    aggregated = aggregate(records)
    judge_data = judge_summary(records)

    if models is None:
        models = sorted({r['model'] for r in records if 'model' in r and 'judge_model' not in r})
    if generation_count is None:
        generation_count = sum(1 for r in records if 'judge_model' not in r)
    if as_of_date is None:
        as_of_date = datetime.datetime.now(datetime.timezone.utc).date().isoformat()

    text = build_results_md(
        aggregated, models=models, generation_count=generation_count, as_of_date=as_of_date,
        judge_summary_data=judge_data,
    )
    if out_path is not None:
        pathlib.Path(out_path).write_text(text, encoding='utf-8')
    return text


def self_test():
    """Offline proof of the generation-record schema and its failure paths.
    No subprocess call, no network call; runs on a machine with no `claude`
    binary. Extended by later tasks in this plan with run_matrix(),
    load_raw_records(), aggregate(), and build_results_md() assertions.
    """
    all_ok = True
    cases_exercised = []

    # Snapshot RESULTS_PATH's bytes (or None) before any self-test case runs,
    # so the final assertion below can prove this function never wrote to the
    # real path -- meaningful both before 05-03's live matrix (RESULTS_PATH
    # does not exist yet) and after it (RESULTS_PATH is a real, committed
    # report generated by --report-only, which self_test() must leave alone).
    results_path_snapshot = RESULTS_PATH.read_bytes() if RESULTS_PATH.exists() else None

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

    # === The blind pairwise judge (Task 1) ===

    fake_pair = {
        'model': 'claude-sonnet-5',
        'scenario_id': 'exec-summary-1',
        'repeat': 0,
        'skill_off_text': 'AWS Control Tower governs the new account structure across 850 virtual machines.',
        'skill_on_text': 'Google Compute Engine hosts the migrated workload across 12 nodes, reducing the '
                          'annual infrastructure spend the customer named at $1,850,000.',
    }

    # --- label-stripping: the built judge prompt contains neither condition
    # name, nor this project's name, nor a PF-/MC- rule-namespace token. ---
    label_prompt = build_judge_prompt(fake_pair['skill_off_text'], fake_pair['skill_on_text'])
    label_violations = _judge_prompt_label_violations(label_prompt)
    if label_violations:
        print(f'FAIL: build_judge_prompt() leaked forbidden token(s): {label_violations}')
        all_ok = False
    else:
        cases_exercised.append('judge-prompt-label-stripping')

    judge_success_envelope = json.loads(
        (FIXTURES_DIR / 'judgement-scored-envelope.json').read_text(encoding='utf-8')
    )

    def _fake_judge_success_run(argv, **kwargs):
        return subprocess.CompletedProcess(argv, returncode=0, stdout=json.dumps(judge_success_envelope), stderr='')

    # --- well-formed reply: three integer scores per text, verdict scored,
    # every JUDGEMENT_RECORD_FIELDS key present, written to the frozen
    # filename template. ---
    with tempfile.TemporaryDirectory() as tmp:
        raw_dir = pathlib.Path(tmp)
        subprocess.run = _fake_judge_success_run
        try:
            judgement, wrote = run_judgement(
                pair=fake_pair, order=1, judge_model=JUDGE_MODEL, judge_effort=JUDGE_EFFORT,
                timeout_s=30, raw_dir=raw_dir,
            )
        finally:
            subprocess.run = real_subprocess_run

        written_judgement_path = raw_path_for_judgement('claude-sonnet-5', 'exec-summary-1', 0, 1, raw_dir)
        missing_judgement_fields = [f for f in JUDGEMENT_RECORD_FIELDS if f not in judgement]
        if missing_judgement_fields:
            print(f'FAIL: scored judgement record missing fields: {missing_judgement_fields}')
            all_ok = False
        elif not wrote:
            print('FAIL: scored judgement run reported wrote=False for a fresh cell')
            all_ok = False
        elif not written_judgement_path.exists():
            print(f'FAIL: scored judgement run did not write {written_judgement_path}')
            all_ok = False
        elif judgement['verdict'] != 'scored':
            print(f"FAIL: scored judgement verdict expected scored, got {judgement['verdict']!r}")
            all_ok = False
        elif judgement['scores'] != {
            'evidence': {'skill-off': 4, 'skill-on': 8},
            'clarity': {'skill-off': 6, 'skill-on': 7},
            'persuasive_force': {'skill-off': 3, 'skill-on': 8},
        }:
            print(f"FAIL: scored judgement scores translated incorrectly: {judgement['scores']}")
            all_ok = False
        else:
            cases_exercised.append('judge-scored')

        # skip-if-exists: re-running the identical cell must make zero subprocess calls.
        def _fail_if_judge_called(argv, **kwargs):
            raise AssertionError('subprocess.run should not be called for an existing judgement raw file')

        subprocess.run = _fail_if_judge_called
        try:
            judgement2, wrote2 = run_judgement(
                pair=fake_pair, order=1, judge_model=JUDGE_MODEL, judge_effort=JUDGE_EFFORT,
                timeout_s=30, raw_dir=raw_dir,
            )
        finally:
            subprocess.run = real_subprocess_run
        if wrote2 or judgement2 != judgement:
            print('FAIL: re-running an existing judgement cell did not skip the subprocess call')
            all_ok = False
        else:
            cases_exercised.append('judge-skip-if-exists')

    # --- reply missing persuasive_force: verdict unscoreable, reason names
    # the missing key, and the record contributes to no mean (compared
    # directly by aggregating with and without it). ---
    missing_dim_envelope = dict(
        judge_success_envelope,
        result=json.dumps({
            'text_a': {'evidence': 4, 'clarity': 6},
            'text_b': {'evidence': 8, 'clarity': 7, 'persuasive_force': 8},
        }),
    )

    def _fake_missing_dim_run(argv, **kwargs):
        return subprocess.CompletedProcess(argv, returncode=0, stdout=json.dumps(missing_dim_envelope), stderr='')

    with tempfile.TemporaryDirectory() as tmp:
        raw_dir = pathlib.Path(tmp)
        subprocess.run = _fake_missing_dim_run
        try:
            missing_dim_judgement, _wrote = run_judgement(
                pair=fake_pair, order=1, judge_model=JUDGE_MODEL, judge_effort=JUDGE_EFFORT,
                timeout_s=30, raw_dir=raw_dir,
            )
        finally:
            subprocess.run = real_subprocess_run

        if missing_dim_judgement['verdict'] != 'unscoreable' or 'persuasive_force' not in (missing_dim_judgement['reason'] or ''):
            print(f'FAIL: reply missing persuasive_force did not record unscoreable naming the key: {missing_dim_judgement}')
            all_ok = False
        else:
            # Direct with-and-without comparison: aggregate() over a scored
            # record plus this unscoreable record must equal aggregate() over
            # the scored record alone -- the unscoreable record contributes
            # zero entries to 'judged' and shifts no mean, never defaulted to
            # 0 or a midpoint (must_haves, EVAL-07 empty edge).
            agg_with_unscoreable = aggregate([judgement, missing_dim_judgement])
            agg_without_unscoreable = aggregate([judgement])
            if agg_with_unscoreable['judged'] != agg_without_unscoreable['judged']:
                print(
                    'FAIL: adding the unscoreable judgement record changed the aggregated '
                    f'judged means: with={agg_with_unscoreable["judged"]} '
                    f'without={agg_without_unscoreable["judged"]}'
                )
                all_ok = False
            else:
                cases_exercised.append('judge-missing-dimension-unscoreable')

    # --- score out of range, non-integer, and unparseable JSON: all unscoreable ---
    invalid_reply_cases = [
        ('out-of-range', json.dumps({'text_a': {'evidence': 4, 'clarity': 6, 'persuasive_force': 3},
                                      'text_b': {'evidence': 11, 'clarity': 7, 'persuasive_force': 8}})),
        ('non-integer', json.dumps({'text_a': {'evidence': 4.5, 'clarity': 6, 'persuasive_force': 3},
                                     'text_b': {'evidence': 8, 'clarity': 7, 'persuasive_force': 8}})),
        ('unparseable-json', '{not valid json'),
    ]
    invalid_cases_ok = True
    for case_name, raw_reply in invalid_reply_cases:
        scores_by_text, reason = _validate_judge_reply(raw_reply)
        if scores_by_text is not None or not reason:
            print(f'FAIL: judge reply validation case {case_name!r} did not produce (None, reason): {(scores_by_text, reason)}')
            all_ok = False
            invalid_cases_ok = False
    if invalid_cases_ok:
        cases_exercised.append('judge-reply-validation-out-of-range-non-integer-unparseable')

    # --- non-zero exit / is_error envelope: raises SessionFailedError,
    # handled identically to the generation path. ---
    def _fake_judge_failed_run(argv, **kwargs):
        return subprocess.CompletedProcess(argv, returncode=1, stdout='', stderr='usage limit reached')

    with tempfile.TemporaryDirectory() as tmp:
        raw_dir = pathlib.Path(tmp)
        subprocess.run = _fake_judge_failed_run
        raised = None
        try:
            run_judgement(
                pair=fake_pair, order=1, judge_model=JUDGE_MODEL, judge_effort=JUDGE_EFFORT,
                timeout_s=30, raw_dir=raw_dir,
            )
        except SessionFailedError as exc:
            raised = exc
        finally:
            subprocess.run = real_subprocess_run

        if raised is None:
            print('FAIL: non-zero exit from run_judgement() did not raise SessionFailedError')
            all_ok = False
        else:
            unscoreable_judgement = _unscoreable_judgement_record(
                JUDGE_MODEL, JUDGE_EFFORT, 'exec-summary-1', 'claude-sonnet-5', 0, 1,
                'skill-off', 'skill-on', reason=f'nonzero exit {raised.returncode}: {raised.stderr!r}',
            )
            if unscoreable_judgement['verdict'] != 'unscoreable' or not unscoreable_judgement['reason']:
                print(f'FAIL: unscoreable judgement record malformed: {unscoreable_judgement}')
                all_ok = False
            else:
                cases_exercised.append('judge-non-zero-exit')

    # --- run_judge_matrix(): enumerates (model, scenario, repeat, order)
    # only for pairs with both skill-on and skill-off generation records
    # already on disk, and catches SessionFailedError exactly like
    # run_matrix() does, writing an unscoreable record rather than raising. ---
    with tempfile.TemporaryDirectory() as tmp:
        raw_dir = pathlib.Path(tmp)
        gen_scenario = {'id': 'exec-summary-1', 'family': 'executive-summary', 'prompt': 'x'}
        for condition, text in (('skill-off', fake_pair['skill_off_text']), ('skill-on', fake_pair['skill_on_text'])):
            record = _unscoreable_generation_record('claude-sonnet-5', 'low', condition, gen_scenario, 0, fake_skill_src, reason=None)
            record['verdict'] = 'generated'
            record['text'] = text
            path = raw_path_for_generation('claude-sonnet-5', condition, 'exec-summary-1', 0, raw_dir)
            _write_json_atomic(path, record)

        subprocess.run = _fake_judge_failed_run
        try:
            judge_cells = run_judge_matrix(
                models=['claude-sonnet-5'], scenarios=[gen_scenario], repeats=1,
                raw_dir=raw_dir, timeout_s=30,
            )
        finally:
            subprocess.run = real_subprocess_run

        judge_written = sorted(raw_dir.glob('*__judge__*.json'))
        if judge_cells != [('claude-sonnet-5', 'exec-summary-1', 0, 1), ('claude-sonnet-5', 'exec-summary-1', 0, 2)]:
            print(f'FAIL: run_judge_matrix() enumerated unexpected cells: {judge_cells}')
            all_ok = False
        elif len(judge_written) != 2:
            print(f'FAIL: run_judge_matrix() expected 2 judgement records on a SessionFailedError, found {len(judge_written)}')
            all_ok = False
        else:
            judge_records_on_disk = [json.loads(p.read_text(encoding='utf-8')) for p in judge_written]
            if not all(r['verdict'] == 'unscoreable' for r in judge_records_on_disk):
                print(f'FAIL: run_judge_matrix() SessionFailedError records not all unscoreable: {judge_records_on_disk}')
                all_ok = False
            else:
                cases_exercised.append('run-judge-matrix-catches-session-failed')

    # --- run_judge_matrix() skips a (model, scenario, repeat) with no
    # matching generation pair on disk -- zero judge calls, zero records. ---
    with tempfile.TemporaryDirectory() as tmp:
        raw_dir = pathlib.Path(tmp)
        gen_scenario = {'id': 'exec-summary-1', 'family': 'executive-summary', 'prompt': 'x'}

        def _fail_if_judge_matrix_calls(argv, **kwargs):
            raise AssertionError('run_judge_matrix() must not call subprocess.run with no generation pair on disk')

        subprocess.run = _fail_if_judge_matrix_calls
        try:
            no_pair_cells = run_judge_matrix(
                models=['claude-sonnet-5'], scenarios=[gen_scenario], repeats=1,
                raw_dir=raw_dir, timeout_s=30,
            )
        finally:
            subprocess.run = real_subprocess_run
        if no_pair_cells:
            print(f'FAIL: run_judge_matrix() enumerated cells with no generation pair on disk: {no_pair_cells}')
            all_ok = False
        else:
            cases_exercised.append('run-judge-matrix-skips-missing-generation-pair')

    # --- average_orders(): identical 7/7 scores average to 7.0; a missing
    # order returns None (excluded, not half-weighted). ---
    order1_scored = {
        'verdict': 'scored',
        'scores': {dim: {'skill-off': 7, 'skill-on': 7} for dim in JUDGE_DIMENSIONS},
    }
    order2_scored = {
        'verdict': 'scored',
        'scores': {dim: {'skill-off': 7, 'skill-on': 7} for dim in JUDGE_DIMENSIONS},
    }
    averaged_equal = average_orders(order1_scored, order2_scored)
    if averaged_equal is None or any(
        averaged_equal[dim]['skill-off'] != 7.0 or averaged_equal[dim]['skill-on'] != 7.0
        for dim in JUDGE_DIMENSIONS
    ):
        print(f'FAIL: average_orders() of identical 7/7 scores did not yield 7.0: {averaged_equal}')
        all_ok = False
    elif average_orders(order1_scored, None) is not None:
        print('FAIL: average_orders() with a missing order did not return None')
        all_ok = False
    else:
        cases_exercised.append('average-orders-identical-and-missing-order')

    # --- judge_summary(): a genuine tie (averaged skill-on == skill-off) is
    # counted as a tie and neither a win nor a loss; a pair missing an order
    # is excluded and the exclusion is counted, read from the summary dict
    # directly, not from a log line. ---
    tie_order1 = {
        'judge_model': JUDGE_MODEL, 'model': 'claude-sonnet-5', 'scenario_id': 'exec-summary-1',
        'repeat': 0, 'order': 1, 'verdict': 'scored',
        'scores': {dim: {'skill-off': 5, 'skill-on': 5} for dim in JUDGE_DIMENSIONS},
    }
    tie_order2 = dict(tie_order1, order=2)
    lone_order1_missing_order2 = {
        'judge_model': JUDGE_MODEL, 'model': 'claude-sonnet-5', 'scenario_id': 'exec-summary-1',
        'repeat': 1, 'order': 1, 'verdict': 'scored',
        'scores': {dim: {'skill-off': 4, 'skill-on': 9} for dim in JUDGE_DIMENSIONS},
        'reason': None,
    }
    summary = judge_summary([tie_order1, tie_order2, lone_order1_missing_order2])
    tie_bucket = summary['tallies'].get(('claude-sonnet-5', 'exec-summary-1'))
    if (
        summary['excluded_pairs'] != 1
        or not tie_bucket
        or any(tie_bucket[dim] != {'wins': 0, 'ties': 1, 'losses': 0} for dim in JUDGE_DIMENSIONS)
    ):
        print(f'FAIL: judge_summary() tie/exclusion tallies wrong: {summary}')
        all_ok = False
    else:
        cases_exercised.append('judge-summary-tie-and-excluded-pair')

    # --- committed judgement fixtures: both the scored and unscoreable
    # shapes match JUDGEMENT_RECORD_FIELDS exactly, proving the schema is a
    # committed artifact, not only an inline dict. ---
    scored_fixture_record = json.loads((FIXTURES_DIR / 'judgement-record-example.json').read_text(encoding='utf-8'))
    unscoreable_fixture_record = json.loads((FIXTURES_DIR / 'judgement-unscoreable-example.json').read_text(encoding='utf-8'))
    if set(scored_fixture_record) != set(JUDGEMENT_RECORD_FIELDS) or set(unscoreable_fixture_record) != set(JUDGEMENT_RECORD_FIELDS):
        print('FAIL: committed judgement fixture(s) do not match JUDGEMENT_RECORD_FIELDS')
        all_ok = False
    else:
        cases_exercised.append('committed-judgement-fixture-schema')

    # --- load_raw_records(): empty/unparseable-file exit, sorted-order determinism ---
    with tempfile.TemporaryDirectory() as tmp:
        raw_dir = pathlib.Path(tmp)
        bad_path = raw_dir / 'a.json'
        bad_path.write_text('')
        try:
            load_raw_records(raw_dir)
            print('FAIL: load_raw_records did not raise on an empty json file')
            all_ok = False
        except ValueError as exc:
            if str(bad_path) not in str(exc):
                print(f'FAIL: load_raw_records empty-file error does not name the path: {exc}')
                all_ok = False
            else:
                cases_exercised.append('load-raw-records-empty-file')

    with tempfile.TemporaryDirectory() as tmp:
        raw_dir = pathlib.Path(tmp)
        unparseable_path = raw_dir / 'b.json'
        unparseable_path.write_text('{not valid json')
        try:
            load_raw_records(raw_dir)
            print('FAIL: load_raw_records did not raise on an unparseable json file')
            all_ok = False
        except ValueError as exc:
            if str(unparseable_path) not in str(exc):
                print(f'FAIL: load_raw_records unparseable-file error does not name the path: {exc}')
                all_ok = False
            else:
                cases_exercised.append('load-raw-records-unparseable-file')

    with tempfile.TemporaryDirectory() as tmp1, tempfile.TemporaryDirectory() as tmp2:
        dir1 = pathlib.Path(tmp1)
        dir2 = pathlib.Path(tmp2)
        payload = {'model': 'claude-sonnet-5', 'scenario_id': 'x', 'condition': 'skill-off', 'verdict': 'generated', 'text': 'a'}
        for name in ('b.json', 'a.json', 'c.json'):
            (dir1 / name).write_text(json.dumps(payload))
        for name in ('c.json', 'a.json', 'b.json'):
            (dir2 / name).write_text(json.dumps(payload))
        if load_raw_records(dir1) != load_raw_records(dir2):
            print('FAIL: load_raw_records is not creation-order-independent')
            all_ok = False
        else:
            cases_exercised.append('load-raw-records-sorted-order')

    # --- generate_report(): empty raw_dir exits without writing a file ---
    with tempfile.TemporaryDirectory() as tmp:
        empty_raw = pathlib.Path(tmp) / 'raw'
        empty_raw.mkdir()
        out_path = pathlib.Path(tmp) / 'RESULTS.md'
        raised = None
        try:
            generate_report(raw_dir=empty_raw, out_path=out_path)
        except ValueError as exc:
            raised = exc
        if raised is None:
            print('FAIL: generate_report() over an empty raw_dir did not raise')
            all_ok = False
        elif out_path.exists():
            print('FAIL: generate_report() over an empty raw_dir wrote a file despite raising')
            all_ok = False
        else:
            cases_exercised.append('generate-report-empty-dir')

    # --- aggregate(): a cell below 3 repeats reports its actual n, never a
    # silent 3, and computes no stdev/CI/p-value key anywhere in its output ---
    synthetic_records = [
        {
            'model': 'claude-sonnet-5', 'scenario_id': 'x-1', 'condition': 'skill-off',
            'verdict': 'generated',
            'text': 'AWS Control Tower governs the new account structure across 850 virtual machines.',
        },
        {
            'model': 'claude-sonnet-5', 'scenario_id': 'x-1', 'condition': 'skill-off',
            'verdict': 'generated',
            'text': 'Google Compute Engine hosts the migrated workload across 12 nodes.',
        },
    ]
    synthetic_agg = aggregate(synthetic_records)
    below_3_key = ('claude-sonnet-5', 'x-1', 'skill-off')
    below_3_stats = synthetic_agg['mechanical'].get(below_3_key)
    forbidden_stat_keys = {'stdev', 'std', 'confidence_interval', 'ci', 'p_value', 'pvalue'}
    if not below_3_stats or below_3_stats['n'] != 2:
        print(f'FAIL: aggregate() below-3-repeats cell expected n=2, got {below_3_stats}')
        all_ok = False
    elif forbidden_stat_keys & set(below_3_stats):
        print(f'FAIL: aggregate() computed a forbidden false-precision statistic: {below_3_stats}')
        all_ok = False
    else:
        cases_exercised.append('aggregate-below-3-repeats-reports-actual-n')

    # --- committed results-render fixtures: a real render carries both
    # required headings and every required caveat (REQUIRED_CAVEATS, six as
    # of the judge-construct-validity addition); two consecutive renders
    # over the same input are byte-identical; the rendered text carries no
    # p-value, confidence interval, standard deviation, or affirmative
    # "significant". ---
    fixture_raw_dir = FIXTURES_DIR / 'results-render'
    fixture_records = load_raw_records(fixture_raw_dir)
    fixture_agg = aggregate(fixture_records)
    fixture_judge_summary = judge_summary(fixture_records)
    fixture_models = sorted({r['model'] for r in fixture_records if 'judge_model' not in r})
    fixture_gen_count = sum(1 for r in fixture_records if 'judge_model' not in r)
    doc1 = build_results_md(
        fixture_agg, models=fixture_models, generation_count=fixture_gen_count, as_of_date='2026-09-18',
        judge_summary_data=fixture_judge_summary,
    )
    doc2 = build_results_md(
        fixture_agg, models=fixture_models, generation_count=fixture_gen_count, as_of_date='2026-09-18',
        judge_summary_data=fixture_judge_summary,
    )

    # --- shuffled-input ordering: a shuffled record order produces byte-
    # identical output, since build_results_md() sorts the win/tie/loss
    # table (and every other table) itself rather than relying on input or
    # dict iteration order (must_haves, EVAL-06 ordering edge). ---
    shuffled_records = list(reversed(fixture_records))
    shuffled_agg = aggregate(shuffled_records)
    shuffled_judge_summary = judge_summary(shuffled_records)
    doc_shuffled = build_results_md(
        shuffled_agg, models=fixture_models, generation_count=fixture_gen_count, as_of_date='2026-09-18',
        judge_summary_data=shuffled_judge_summary,
    )
    if doc_shuffled != doc1:
        print('FAIL: build_results_md() output differs for a shuffled input record order')
        all_ok = False
    else:
        cases_exercised.append('win-tie-loss-rows-shuffle-invariant')

    missing_headings = [h for h in RESULTS_SECTION_HEADINGS if h not in doc1]
    missing_caveats = _missing_required_caveats(doc1)
    forbidden_statistics_phrases = ('p-value', 'confidence interval', 'standard deviation', 'is significant', 'statistically significant')
    found_forbidden = [p for p in forbidden_statistics_phrases if p in doc1.lower()]

    if missing_headings:
        print(f'FAIL: rendered fixture report missing required heading(s): {missing_headings}')
        all_ok = False
    elif missing_caveats:
        print(f'FAIL: rendered fixture report missing required caveat(s): {missing_caveats}')
        all_ok = False
    elif doc1 != doc2:
        print('FAIL: build_results_md() is not byte-identical across two renders of identical input')
        all_ok = False
    elif found_forbidden:
        print(f'FAIL: rendered fixture report contains a forbidden overclaim phrase: {found_forbidden}')
        all_ok = False
    else:
        cases_exercised.append('results-render-fixture-two-headings-all-caveats-byte-identical')

    # --- per-caveat assertion: deleting each of the five caveats in turn
    # from a COPY of REQUIRED_CAVEATS (never the constant itself) makes the
    # renderer omit exactly that caveat, and _missing_required_caveats()
    # (checked against the real, full REQUIRED_CAVEATS) names it. Proves
    # the caveats section is built FROM the constant, not hardcoded prose
    # that could drift from what this file checks. ---
    per_caveat_ok = True
    for omitted in REQUIRED_CAVEATS:
        reduced = tuple(c for c in REQUIRED_CAVEATS if c != omitted)
        reduced_doc = build_results_md(fixture_agg, required_caveats=reduced)
        missing = _missing_required_caveats(reduced_doc)
        if missing != [omitted]:
            print(f'FAIL: per-caveat assertion for {omitted!r} expected missing=[{omitted!r}], got {missing}')
            all_ok = False
            per_caveat_ok = False
    if per_caveat_ok:
        cases_exercised.append('per-caveat-drift-guard')

    # --- no-subprocess assertion: the whole --report-only path (
    # load_raw_records -> aggregate -> build_results_md, via
    # generate_report()) makes zero subprocess calls, proven by replacing
    # subprocess.run with a function that raises for the duration of the
    # call. ---
    def _raise_if_called(argv, **kwargs):
        raise AssertionError('report-only path must never call subprocess.run')

    with tempfile.TemporaryDirectory() as tmp:
        out_path = pathlib.Path(tmp) / 'RESULTS.md'
        subprocess.run = _raise_if_called
        try:
            report_text = generate_report(
                raw_dir=fixture_raw_dir, out_path=out_path,
                models=fixture_models, generation_count=fixture_gen_count, as_of_date='2026-09-18',
            )
        finally:
            subprocess.run = real_subprocess_run

        if report_text != doc1:
            print('FAIL: generate_report() output does not match the equivalent direct build_results_md() render')
            all_ok = False
        elif not out_path.exists():
            print('FAIL: generate_report() with an out_path did not write RESULTS.md')
            all_ok = False
        else:
            cases_exercised.append('report-only-no-subprocess-call')

    # --- self_test() never writes to the real RESULTS_PATH -- every case
    # above renders into a temporary directory only. Before 05-03's live
    # matrix this proves RESULTS_PATH still does not exist (None == None);
    # after it, this proves self_test() left the real, committed report
    # (generated only by --report-only from real raw/ records) byte-for-byte
    # untouched. ---
    results_path_after = RESULTS_PATH.read_bytes() if RESULTS_PATH.exists() else None
    if results_path_after != results_path_snapshot:
        print(f'FAIL: {RESULTS_PATH} was modified by self_test() -- self_test() must never write the real path')
        all_ok = False
    else:
        cases_exercised.append('self-test-never-writes-real-results-path')

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
    parser.add_argument('--judge-model', default=JUDGE_MODEL,
                         help=f'Judge model id (default: {JUDGE_MODEL}).')
    parser.add_argument('--judge-effort', default=JUDGE_EFFORT,
                         help=f'Judge --effort level (default: {JUDGE_EFFORT}).')
    parser.add_argument('--report-only', action='store_true',
                         help='Offline recompute of RESULTS.md from --raw-dir; makes no subprocess call.')
    args = parser.parse_args()

    if args.self_test:
        ok = self_test()
        sys.exit(0 if ok else 1)

    if args.report_only:
        try:
            text = generate_report(raw_dir=args.raw_dir, out_path=args.out)
        except ValueError as exc:
            print(f'report-only failed: {exc}', file=sys.stderr)
            sys.exit(1)
        print(f'wrote {args.out} ({len(text)} chars)')
        sys.exit(0)

    # Live mode (05-03): drive the real model x condition x scenario x repeat
    # matrix, then the judge pass over every resulting pair, both orders.
    # Requires `claude auth status` to show loggedIn: true -- this function
    # does not check that itself (the operator-facing precondition is
    # verified once, by hand, before this command is ever invoked, per
    # 05-03-PLAN.md Task 3's own <precondition>); a session that is not
    # authenticated simply fails each call with a non-zero exit, which
    # run_matrix()/run_judge_matrix() already record as `unscoreable` rather
    # than crash the whole run.
    models = [m.strip() for m in args.models.split(',') if m.strip()]
    scenarios = load_scenarios(args.scenarios)
    conditions = list(CONDITIONS)
    expected_cells = len(models) * len(conditions) * len(scenarios) * args.repeats

    print(
        f'Running generation matrix: {len(models)} model(s) x {len(conditions)} condition(s) x '
        f'{len(scenarios)} scenario(s) x {args.repeats} repeat(s) = {expected_cells} cells '
        f'(existing raw files are skipped, not re-paid for)',
        file=sys.stderr,
    )
    run_matrix(
        models=models, conditions=conditions, scenarios=scenarios, repeats=args.repeats,
        skill_src=args.skill_src, raw_dir=args.raw_dir, timeout_s=args.timeout,
        effort=args.effort, max_budget_usd=args.max_budget_usd,
    )

    print(
        'Running judge pass over every (skill-on, skill-off) pair, both orders '
        '(existing judgement files are skipped, not re-paid for)',
        file=sys.stderr,
    )
    run_judge_matrix(
        models=models, scenarios=scenarios, repeats=args.repeats, raw_dir=args.raw_dir,
        timeout_s=args.timeout, judge_model=args.judge_model, judge_effort=args.judge_effort,
        max_budget_usd=args.max_budget_usd,
    )

    print('Live matrix complete. Run --report-only to (re)generate RESULTS.md.', file=sys.stderr)
    sys.exit(0)


if __name__ == '__main__':
    main()
