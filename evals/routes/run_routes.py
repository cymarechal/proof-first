#!/usr/bin/env python3
"""Route-equivalence measurement for Proof First's three distribution routes.

This script measures exactly one thing: whether the output style and the
pasted system prompt deliver the same discipline to a live session as the
installed skill folder does. Three arms -- skill-on, style-on, prompt-on --
receive byte-identical prompts from evals/benchmark/scenarios.json, the same
model, the same effort and the same tool restrictions, and differ only in how
the rule catalog reaches the session. It measures nothing else: no persuasion
judge runs here, no model comparison, no claim about which route writes
better prose.

Three limits on what its numbers mean, stated here rather than only in the
rendered report:

  score_transcript() is borrowed. evals/conformance/run_conformance.py
  calibrated it on that recipe's revise-a-draft prompt, and this script reuses
  it unchanged on write-from-brief prompts. A family-line verdict here is the
  same regex scorer answering a question it was not tuned for.

  --append-system-prompt-file is a proxy, not the thing. Route 4 is "paste
  this file into a harness with no skill support." No such harness is driven
  from this repository. Appending the same bytes to a headless Claude Code
  session is the closest observable stand-in, and it is a stand-in.

  A mechanical proxy count is not a compliance verdict. evals/lint.py states
  that limit in full in its own module docstring; this file reuses that
  statement rather than restating it in weaker words.

Activation, settled by measurement on 2026-09-21 before any matrix spend
(records committed under evals/routes/probe/, one session per row, all on
executive-summary-1 at claude-sonnet-5 --effort low):

  route      activated  family-line verdict
  none       False      no-family
  skill-on   True       rule-before-family
  style-on   True       conformant
  prompt-on  True       conformant

All three routes discriminate against the unrouted control on both signals,
so all three stay in ROUTES and none is dropped. The output style was proven
on the FIRST activation form tried -- STYLE_ACTIVATION_FORMS[0],
'settings-json': the style file copied into the session's
.claude/output-styles/ with a .claude/settings.json naming it. The two
fallback forms 'settings-flag' and 'settings-local-json' were never needed
and are therefore untested against a live session; they remain in the tuple
as the probe's escalation path, not as proven configurations. A headless
`claude -p` session does honour a project-scoped output style, which was
UNVERIFIED in this environment until this probe ran.

It imports only the Python standard library: argparse, datetime, importlib,
json, pathlib, re, shutil, subprocess, sys, tempfile, uuid. No
package-manager dependency is introduced by this file or by the CI job that
runs it.

Usage:
  python3 evals/routes/run_routes.py --self-test
      Offline proof of the per-route session setup, the record schema, the
      failure paths, the aggregator and the renderer. Makes no subprocess
      call and no network call; runs on a machine with no `claude` binary
      installed. This is the only mode CI runs.

  python3 evals/routes/run_routes.py --probe
      Activation probe: at most PROBE_SESSION_CAP live sessions against one
      scenario, including one unrouted control, to prove each route actually
      reaches the session before any matrix money is spent. Writes full
      records to evals/routes/probe/ and prints a discrimination table.

  python3 evals/routes/run_routes.py [--model M] [--effort LEVEL]
      [--repeats N] [--routes A,B] [--scenarios PATH] [--raw-dir PATH]
      [--timeout SECONDS] [--max-budget-usd AMOUNT]
      Live mode: drives the route x scenario x repeat matrix, one
      isolated-temp-dir `claude -p` session per cell, skipping any cell whose
      raw record already exists. Requires `claude auth status` to show
      loggedIn: true. No API key needed.

  python3 evals/routes/run_routes.py --report-only [--raw-dir PATH] [--out PATH]
      Offline recompute: reads every committed record under --raw-dir,
      recomputes every count, mean and range, and rewrites
      RESULTS-routes.md. Makes zero subprocess calls and zero network calls
      -- the self-test proves this by replacing subprocess.run with a
      function that raises.

No session driven by this file is isolated from skill, plugin and settings
discovery. That discovery machinery is exactly what all three routes depend
on, so the flag that would switch it off is never passed by any code path
here.
"""

import argparse
import datetime
import importlib.util
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import uuid

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
ROUTES_DIR = pathlib.Path(__file__).resolve().parent

# The four family names are skills/proof-first/references/artifact-patterns.md's
# own section headings. Frozen -- a fifth value or a missing one is a
# load_scenarios() error, never a silent pass-through.
FAMILIES = ('rfp-rfi', 'solution-proposal', 'executive-summary', 'demo-discovery')

# The three distribution routes this repository ships. Frozen here; Task 2's
# probe is the only thing permitted to narrow this tuple, and only by removing
# a route it could not prove was switched on.
ROUTES = ('skill-on', 'style-on', 'prompt-on')

# The unrouted baseline. It exists to prove a route was switched on, by
# showing what a session with no route installed produces on the same
# scenario. It is not a fourth distribution channel and must never appear in
# ROUTES or in the published matrix.
CONTROL_ROUTE = 'none'

DEFAULT_MODEL = 'claude-sonnet-5'
DEFAULT_EFFORT = 'low'
DEFAULT_REPEATS = 3
DISALLOWED_TOOLS = ['Write', 'Edit', 'Bash', 'NotebookEdit']
MAX_BUDGET_USD = 2
GENERATION_VERDICTS = ('generated', 'unscoreable')

# The probe's hard stop. probe_routes() refuses to drive more sessions than
# this, so the pre-authorisation spend is bounded by code and not only by the
# operator's attention.
PROBE_SESSION_CAP = 6
PROBE_SCENARIO_ID = 'executive-summary-1'

SCENARIOS_PATH = REPO_ROOT / 'evals' / 'benchmark' / 'scenarios.json'
RAW_DIR = ROUTES_DIR / 'raw'
PROBE_DIR = ROUTES_DIR / 'probe'
RESULTS_PATH = ROUTES_DIR / 'RESULTS-routes.md'

SKILL_SRC = REPO_ROOT / 'skills' / 'proof-first'
STYLE_SRC = REPO_ROOT / 'output-styles' / 'proof-first.md'
PROMPT_SRC = REPO_ROOT / 'prompts' / 'system-prompt.md'

# The activation detector. Identical to run_conformance.py's MARKER_PATTERN,
# deliberately, so the two instruments agree on what a rule marker is.
MARKER_RE = re.compile(r'\bPF-\d+\.\d+\b|\bMC-\d+\b')

# The three ways a project-scoped output style might reach a headless
# session, tried in this order by the probe. Whether any of them works is an
# open question this file does not assume the answer to.
STYLE_ACTIVATION_FORMS = ('settings-json', 'settings-flag', 'settings-local-json')
STYLE_ACTIVATION_FORM = 'settings-json'
STYLE_NAME = 'proof-first'

# Every field a route generation record must carry. self_test() asserts a
# record is never missing one of these.
GENERATION_RECORD_FIELDS = (
    'run_id', 'timestamp', 'model', 'canonical_model', 'effort', 'route',
    'family', 'scenario_id', 'scenario_prompt', 'artifact_sha', 'repeat',
    'text', 'activated', 'lint_violations', 'conformance_verdict',
    'usage', 'cost_usd', 'duration_ms', 'cli_version', 'verdict', 'reason',
)

# The file whose content each route installs, hashed into artifact_sha so a
# record says which bytes the session actually received.
ROUTE_ARTIFACT_PATH = {
    'skill-on': SKILL_SRC / 'SKILL.md',
    'style-on': STYLE_SRC,
    'prompt-on': PROMPT_SRC,
    CONTROL_ROUTE: None,
}

RESULTS_SECTION_HEADINGS = (
    '## Activation',
    '## Mechanical proxy counts',
    '## Family-line conformance',
    '## Honest caveats',
    '## Reproduce',
)

# The caveats this report may not ship without. build_routes_results_md()
# builds its caveats section FROM this constant, so the list the self-test
# checks against cannot drift from what the renderer emits.
REQUIRED_CAVEATS = (
    'scorer calibration',
    'trigger activation',
    'system-prompt proxy',
    'sample size',
    'interactive picker',
)

CAVEAT_TEXT = {
    'scorer calibration': (
        'Scorer calibration: the family-line verdicts come from '
        'evals/conformance/run_conformance.py\'s score_transcript(), which was calibrated on '
        'that recipe\'s revise-a-draft prompt. It is reused here, unchanged, on write-from-brief '
        'prompts. The scorer is the same; the question it is being asked is not the one it was '
        'tuned against.'
    ),
    'trigger activation': (
        'Trigger activation is not equal across arms: the skill-on arm depends on the model '
        'deciding the skill is relevant, so its result carries whatever trigger behaviour the '
        'skill description produces. The style-on and prompt-on arms are unconditionally on. '
        'Phase 2 measured and disclosed a trigger over-fire residual (CAT-10, .planning/WINDOWS.md '
        'entry 24, open); the skill-on arm here inherits it.'
    ),
    'system-prompt proxy': (
        'System-prompt proxy: route 4 is "paste this file into a harness with no skill support." '
        'No such harness is driven from this repository. The prompt-on arm appends the same bytes '
        'to a headless Claude Code session with --append-system-prompt-file, which is the closest '
        'observable stand-in and is not that harness.'
    ),
    'sample size': (
        'Sample size: one model, one effort level, and a small number of repeats per cell. This '
        'is not powered to detect statistical significance. Treat any difference smaller than the '
        'observed range as noise, and read "not distinguished" as exactly that -- not as '
        '"equivalent." Every mean is rounded to one decimal place; the unrounded values remain '
        'recoverable from evals/routes/raw/.'
    ),
    'interactive picker': (
        'Interactive picker unobserved: a headless session has no /config picker. Whether a human '
        'sees the copied output style listed there and can select it is a different question from '
        'whether the style\'s content reaches a session, and nothing here observes it '
        '(.planning/WINDOWS.md entry 16, open).'
    ),
}


class SessionFailedError(RuntimeError):
    """Raised by run_route_session() when `claude -p` exits non-zero, when
    its envelope reports `is_error: true`, or when its envelope cannot be
    parsed.

    Carries the exit code (or -1 for a non-exit-code failure) and a stderr /
    reason string, so the caller records a diagnosable `unscoreable` reason
    instead of scoring stdout -- which, on a non-timeout failure, is
    typically a short error string rather than real generated text -- as if
    it were real data. Copied in shape from
    evals/benchmark/run_benchmark.py's SessionFailedError, guarding the same
    bug class its docstring documents in full (MOD-04's
    usage-limit-exhaustion incident, where every failed session's stdout was
    scored as if it were generated text instead of excluded).
    """

    def __init__(self, returncode, stderr):
        self.returncode = returncode
        self.stderr = stderr or ''
        super().__init__(f'claude -p exited {returncode}')


def _git_blob_sha(path):
    """Return the git blob SHA of `path`, or None.

    Copied in shape from evals/benchmark/run_benchmark.py's _git_blob_sha().
    `git hash-object` is content-addressed and needs no repo relationship to
    the target path, so it reports the correct SHA for a working-tree copy --
    unlike `git rev-parse HEAD:...`, which silently reports the wrong SHA for
    any file the working tree has moved ahead of HEAD.
    """
    if path is None:
        return None
    path = pathlib.Path(path)
    if not path.exists():
        return None
    try:
        result = subprocess.run(
            ['git', 'hash-object', str(path)],
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
    """Write `record` to `path` as UTF-8 JSON with ensure_ascii=False."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding='utf-8')


def _load_module_from_path(path, module_name):
    """Load a module from an absolute path with
    importlib.util.spec_from_file_location.

    The loaded module's __name__ is `module_name`, never '__main__', so a
    loaded script's `if __name__ == "__main__"` block does not run and its
    main() is never executed by the act of loading it. Neither
    evals/lint.py nor evals/conformance/run_conformance.py performs any
    filesystem write at module level; self_test() proves that directly by
    loading the conformance module inside a temporary working directory and
    asserting nothing was created.
    """
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_lint_module():
    """Return evals/lint.py's `lint` function."""
    return _load_module_from_path(REPO_ROOT / 'evals' / 'lint.py',
                                  'proof_first_routes_lint').lint


def _load_conformance_module():
    """Return evals/conformance/run_conformance.py's `score_transcript`."""
    return _load_module_from_path(
        REPO_ROOT / 'evals' / 'conformance' / 'run_conformance.py',
        'proof_first_routes_conformance',
    ).score_transcript


def load_scenarios(path=None):
    """Return the list of scenario dicts from `path` (default
    SCENARIOS_PATH), validating ids and families.

    This file never writes that path. All three arms read the same committed
    prompts, verbatim, which is the whole reason the arms are comparable.
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


def raw_path_for_session(model, route, scenario_id, repeat, raw_dir=None):
    """Return the frozen filename template path for a route record.

    `scenario_id` is drawn only from the committed scenarios file; `model`
    and `route` come from frozen tuples or the CLI's validated subset;
    `repeat` is an int. No CLI free-text value reaches this filename.
    """
    raw_dir = pathlib.Path(raw_dir) if raw_dir is not None else RAW_DIR
    return raw_dir / f'{model}__{route}__{scenario_id}__r{repeat}.json'


def route_extra_argv(route, style_form=None, prompt_src=None):
    """Return the extra argv a route adds to the base `claude -p` call.

    skill-on and style-on add nothing in their default forms: both install
    files into the session's own project directory and let discovery find
    them. prompt-on appends the generated system prompt by absolute path.
    The settings-flag style form is the one exception -- it is a probe
    fallback, and it passes the setting inline rather than writing it.
    """
    style_form = style_form or STYLE_ACTIVATION_FORM
    prompt_src = pathlib.Path(prompt_src) if prompt_src is not None else PROMPT_SRC
    if route == 'prompt-on':
        return ['--append-system-prompt-file', str(prompt_src.resolve())]
    if route == 'style-on' and style_form == 'settings-flag':
        return ['--settings', json.dumps({'outputStyle': STYLE_NAME})]
    return []


def setup_route_dir(tmp_dir, route, style_form=None, skill_src=None, style_src=None):
    """Install whatever the route needs into the session's fresh temp dir.

    Returns the list of paths created, for the self-test to assert against.
    prompt-on and the control create nothing: prompt-on rides argv, and the
    control is the absence of a route.
    """
    tmp_dir = pathlib.Path(tmp_dir)
    style_form = style_form or STYLE_ACTIVATION_FORM
    skill_src = pathlib.Path(skill_src) if skill_src is not None else SKILL_SRC
    style_src = pathlib.Path(style_src) if style_src is not None else STYLE_SRC
    created = []

    if route == 'skill-on':
        skill_dst = tmp_dir / '.claude' / 'skills' / 'proof-first'
        skill_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(skill_src, skill_dst)
        created.append(skill_dst)
        return created

    if route == 'style-on':
        style_dst = tmp_dir / '.claude' / 'output-styles' / 'proof-first.md'
        style_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(style_src, style_dst)
        created.append(style_dst)
        if style_form == 'settings-json':
            settings = tmp_dir / '.claude' / 'settings.json'
        elif style_form == 'settings-local-json':
            settings = tmp_dir / '.claude' / 'settings.local.json'
        else:
            return created
        settings.write_text(
            json.dumps({'outputStyle': STYLE_NAME}, indent=2) + '\n', encoding='utf-8')
        created.append(settings)
        return created

    return created


def _unwrap_envelope(raw_stdout):
    """Parse `claude -p --output-format json` stdout and return the single
    result-message dict.

    Handles both CLI response shapes: a single JSON object, or a JSON array
    of message objects where exactly one carries `"type": "result"`. Raises
    ValueError if an array carries no such message.
    """
    env = json.loads(raw_stdout)
    if isinstance(env, list):
        for message in env:
            if isinstance(message, dict) and message.get('type') == 'result':
                return message
        raise ValueError('no message with type "result" found in envelope array')
    return env


def _unscoreable_record(model, effort, route, scenario, repeat, reason):
    """Build an `unscoreable` record with the given diagnosable `reason`.

    A failure is never written as a zero-violation generation. activated is
    False and both scores are None, so nothing downstream can average this
    record as if it carried text.
    """
    return {
        'run_id': str(uuid.uuid4()),
        'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'model': model,
        'canonical_model': model,
        'effort': effort,
        'route': route,
        'family': scenario['family'],
        'scenario_id': scenario['id'],
        'scenario_prompt': scenario['prompt'],
        'artifact_sha': _git_blob_sha(ROUTE_ARTIFACT_PATH.get(route)),
        'repeat': repeat,
        'text': '',
        'activated': False,
        'lint_violations': None,
        'conformance_verdict': None,
        'usage': {},
        'cost_usd': None,
        'duration_ms': None,
        'cli_version': None,
        'verdict': 'unscoreable',
        'reason': reason,
    }


def score_record(text, lint_fn=None, score_fn=None):
    """Return (activated, lint_violations, conformance_verdict) for `text`.

    activated answers a narrower question than the other two: did the rule
    catalog reach this session at all. A low violation count from a session
    that never saw a rule is not evidence that the route works, which is why
    this boolean is a separate field rather than an inference from the
    counts.
    """
    if lint_fn is None:
        lint_fn = _load_lint_module()
    if score_fn is None:
        score_fn = _load_conformance_module()
    activated = bool(MARKER_RE.search(text))
    violations = lint_fn(text)['violations_total']
    verdict, _evidence = score_fn(text)
    return activated, violations, verdict


def run_route_session(model, effort, route, scenario, repeat, timeout_s,
                      raw_dir=None, max_budget_usd=MAX_BUDGET_USD,
                      style_form=None, skill_src=None, style_src=None,
                      prompt_src=None, lint_fn=None, score_fn=None):
    """Drive one isolated-temp-dir `claude -p` session for one route cell,
    write its record to the frozen filename template, and return
    (record, wrote_new).

    `wrote_new` is False when the cell's raw file already exists -- no
    subprocess call is made in that case, which is the resumability property
    that makes an interrupted matrix cost only its remaining cells.

    Raises SessionFailedError on a non-zero exit, an `is_error: true`
    envelope, or an unparseable envelope; the caller writes an `unscoreable`
    record rather than letting the failure end the run. A session that exits
    0 with `is_error: false` but returns empty text does not raise -- this
    function writes the `unscoreable` record for it directly.

    The temp dir is removed on every path out of this function, success and
    failure alike.
    """
    raw_dir = pathlib.Path(raw_dir) if raw_dir is not None else RAW_DIR
    path = raw_path_for_session(model, route, scenario['id'], repeat, raw_dir)
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8')), False

    tmp_dir = pathlib.Path(tempfile.mkdtemp(prefix='proof-first-routes-'))
    try:
        setup_route_dir(tmp_dir, route, style_form=style_form,
                        skill_src=skill_src, style_src=style_src)
        argv = [
            'claude', '-p', scenario['prompt'],
            '--model', model,
            '--effort', effort,
            '--output-format', 'json',
            '--disallowedTools', ','.join(DISALLOWED_TOOLS),
            '--max-budget-usd', str(max_budget_usd),
        ] + route_extra_argv(route, style_form=style_form, prompt_src=prompt_src)
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
        detail = (str(env.get('result', ''))[:300] if isinstance(env, dict)
                  else 'malformed envelope (not a JSON object)')
        raise SessionFailedError(-1, detail)

    text = env.get('result', '') or ''
    if not text.strip():
        record = _unscoreable_record(
            model, effort, route, scenario, repeat,
            reason='empty or whitespace-only result text',
        )
        _write_json_atomic(path, record)
        return record, True

    activated, violations, verdict = score_record(text, lint_fn=lint_fn, score_fn=score_fn)
    record = {
        'run_id': str(uuid.uuid4()),
        'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'model': model,
        'canonical_model': env.get('canonical_model', model),
        'effort': effort,
        'route': route,
        'family': scenario['family'],
        'scenario_id': scenario['id'],
        'scenario_prompt': scenario['prompt'],
        'artifact_sha': _git_blob_sha(ROUTE_ARTIFACT_PATH.get(route)),
        'repeat': repeat,
        'text': text,
        'activated': activated,
        'lint_violations': violations,
        'conformance_verdict': verdict,
        'usage': env.get('usage', {}) or {},
        'cost_usd': env.get('total_cost_usd', env.get('cost_usd')),
        'duration_ms': env.get('duration_ms'),
        'cli_version': env.get('cli_version'),
        'verdict': 'generated',
        'reason': None,
    }
    _write_json_atomic(path, record)
    return record, True


def run_matrix(model, routes, scenarios, repeats, raw_dir, timeout_s,
               effort=DEFAULT_EFFORT, max_budget_usd=MAX_BUDGET_USD,
               session_fn=run_route_session, style_form=None):
    """Enumerate route x scenario x repeat, in that nesting order, and drive
    one session per cell.

    Single-writer-per-path: exactly one call site writes any given raw path,
    and this runner never parallelises onto a shared path. On
    SessionFailedError it writes an `unscoreable` record carrying the real
    reason and continues; any other exception propagates immediately,
    leaving on disk exactly the records written by cells before it.

    Returns the list of (route, scenario_id, repeat) tuples enumerated, in
    the deterministic order driven.
    """
    raw_dir = pathlib.Path(raw_dir)
    enumerated = []
    for route in routes:
        for scenario in scenarios:
            for repeat in range(repeats):
                enumerated.append((route, scenario['id'], repeat))
                try:
                    session_fn(
                        model=model, effort=effort, route=route, scenario=scenario,
                        repeat=repeat, timeout_s=timeout_s, raw_dir=raw_dir,
                        max_budget_usd=max_budget_usd, style_form=style_form,
                    )
                except SessionFailedError as exc:
                    record = _unscoreable_record(
                        model, effort, route, scenario, repeat,
                        reason=f'session failed (exit {exc.returncode}): {exc.stderr[:300]}',
                    )
                    _write_json_atomic(
                        raw_path_for_session(model, route, scenario['id'], repeat, raw_dir),
                        record,
                    )
    return enumerated


def load_raw_records(raw_dir=None):
    """Read every `*.json` file under `raw_dir`, in sorted path order.

    Raises ValueError, naming the path, for an empty or unparseable file --
    never a silent skip, because a silently skipped record is a published
    number computed from less data than it claims.
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


def aggregate(records, lint_fn=None, score_fn=None):
    """Pure-over-committed-files: turn raw records into the three figure
    halves, kept independent and never blended into one score.

    Every figure is recomputed from each record's own `text` rather than
    read back from the score fields the record already carries, so the
    report is a function of the committed transcripts and not of whatever
    the runner believed at write time.

    `unscoreable` records are counted per route and excluded from every
    mean. Each cell reports its actual n, never a padded one.
    """
    if lint_fn is None:
        lint_fn = _load_lint_module()
    if score_fn is None:
        score_fn = _load_conformance_module()

    activation = {}
    mechanical = {}
    conformance = {}
    unscoreable = {}
    counts = {}

    for record in records:
        route = record.get('route')
        unscoreable.setdefault(route, 0)
        counts.setdefault(route, {'activated': 0, 'n': 0, 'violations': [], 'verdicts': {}})
        if record.get('verdict') != 'generated':
            unscoreable[route] += 1
            continue
        text = record.get('text', '') or ''
        activated, violations, verdict = score_record(text, lint_fn=lint_fn, score_fn=score_fn)
        bucket = counts[route]
        bucket['n'] += 1
        bucket['activated'] += 1 if activated else 0
        bucket['violations'].append(violations)
        bucket['verdicts'][verdict] = bucket['verdicts'].get(verdict, 0) + 1

    for route, bucket in counts.items():
        activation[route] = {'n': bucket['n'], 'activated': bucket['activated']}
        if bucket['violations']:
            vals = bucket['violations']
            mechanical[route] = {
                'n': len(vals),
                'mean': round(sum(vals) / len(vals), 1),
                'min': min(vals),
                'max': max(vals),
            }
        conformance[route] = dict(bucket['verdicts'])

    return {
        'activation': activation,
        'mechanical': mechanical,
        'conformance': conformance,
        'unscoreable': unscoreable,
    }


def separation_verdict(mechanical, routes):
    """Return the one sentence the report is allowed to say about whether
    the arms differ.

    The only separation this function will assert is a non-overlapping
    observed range between two arms. Overlapping ranges at these sample
    sizes are reported as "not distinguished," which is a different claim
    from "equivalent" and is the only one the records support.
    """
    arms = [(r, mechanical[r]) for r in routes if r in mechanical]
    if len(arms) < 2:
        return ('This run carries fewer than two scoreable arms, so it makes no comparison '
                'between routes at all.')
    separated = []
    for i in range(len(arms)):
        for j in range(i + 1, len(arms)):
            a_name, a = arms[i]
            b_name, b = arms[j]
            if a['max'] < b['min']:
                separated.append(f'{a_name} entirely below {b_name}')
            elif b['max'] < a['min']:
                separated.append(f'{b_name} entirely below {a_name}')
    if not separated:
        return ('Every pair of arms has overlapping observed ranges on the mechanical proxy '
                'count, so this measurement did not distinguish the routes. That is not the '
                'same finding as equivalence, and this report does not make the stronger claim.')
    return ('Non-overlapping observed ranges on the mechanical proxy count: '
            + '; '.join(separated)
            + '. A non-overlapping range at this sample size is a signal worth recording, not '
              'a significance test.')


def _missing_required_caveats(text, required_caveats=REQUIRED_CAVEATS):
    """Return the subset of `required_caveats` whose key does not appear
    (case-insensitively) anywhere in `text`."""
    lowered = text.lower()
    return [caveat for caveat in required_caveats if caveat.lower() not in lowered]


def _as_of_date_from_records(records):
    """Derive the report's as-of date from the records' own timestamps,
    never from the render-time clock.

    Returns the single ISO date shared by every record, or
    '{earliest} to {latest}' when the run spans more than one UTC date.
    Returns None when no record carries a timestamp; the caller supplies its
    own fallback.
    """
    dates = sorted({r['timestamp'][:10] for r in records if r.get('timestamp')})
    if not dates:
        return None
    if len(dates) == 1:
        return dates[0]
    return f'{dates[0]} to {dates[-1]}'


def build_routes_results_md(aggregated, model, effort, routes, as_of_date,
                            session_count, repeats=DEFAULT_REPEATS,
                            scenario_count=None, dropped_routes=(),
                            required_caveats=REQUIRED_CAVEATS):
    """Pure function: turn aggregate()'s output into the whole
    RESULTS-routes.md document as a string.

    Calling this twice on identical input returns byte-identical strings --
    there is no clock read and no randomness anywhere in it; every
    date-shaped value is an explicit parameter.
    """
    activation = aggregated['activation']
    mechanical = aggregated['mechanical']
    conformance = aggregated['conformance']
    unscoreable = aggregated['unscoreable']
    routes = [r for r in routes]

    lines = []
    lines.append('# Route equivalence: skill folder, output style, pasted system prompt')
    lines.append('')
    lines.append(
        f'Measured {as_of_date} on {model} at --effort {effort}: {session_count} sessions across '
        f'{len(routes)} route(s) ({", ".join(routes)}), '
        f'{scenario_count if scenario_count is not None else "an unrecorded number of"} '
        f'scenario(s) x {repeats} repeats per cell.'
    )
    lines.append('')
    lines.append(separation_verdict(mechanical, routes))
    lines.append('')
    lines.append(
        'Generated by `python3 evals/routes/run_routes.py --report-only`. Every figure below '
        'recomputes from the committed records under `evals/routes/raw/`. Do not edit this file '
        'by hand.'
    )
    lines.append('')

    lines.append('## Activation')
    lines.append('')
    lines.append(
        'Did the rule catalog reach the session at all. A record is `activated` when its text '
        'carries at least one `PF-<n>.<n>` or `MC-<n>` marker. This is deliberately separate '
        'from the counts below: a low-violation session that never saw a rule is not evidence '
        'that a route works.'
    )
    lines.append('')
    lines.append('| Route | Scoreable sessions | Activated | Unscoreable |')
    lines.append('|---|---|---|---|')
    for route in routes:
        act = activation.get(route, {'n': 0, 'activated': 0})
        lines.append(
            f'| {route} | {act["n"]} | {act["activated"]} | {unscoreable.get(route, 0)} |'
        )
    lines.append('')
    if dropped_routes:
        lines.append(
            'Dropped before the matrix, for want of a demonstrated activation: '
            + ', '.join(dropped_routes)
            + '. See the probe records under `evals/routes/probe/`.'
        )
        lines.append('')

    lines.append('## Mechanical proxy counts')
    lines.append('')
    lines.append(
        'Violation counts from `evals/lint.py`\'s `lint()`, the same instrument scoring every '
        'arm. Lower is fewer proxy violations, and a proxy count is not a compliance verdict.'
    )
    lines.append('')
    lines.append('| Route | n | Mean violations | Min | Max |')
    lines.append('|---|---|---|---|---|')
    for route in routes:
        cell = mechanical.get(route)
        if cell is None:
            lines.append(f'| {route} | 0 | n/a | n/a | n/a |')
        else:
            lines.append(
                f'| {route} | {cell["n"]} | {cell["mean"]} | {cell["min"]} | {cell["max"]} |'
            )
    lines.append('')

    lines.append('## Family-line conformance')
    lines.append('')
    lines.append(
        'Verdicts from `evals/conformance/run_conformance.py`\'s `score_transcript()`: whether '
        'the artifact-family line reached the output, and whether a rule marker preceded it. '
        'Reported separately from the counts above and never blended with them into one score.'
    )
    lines.append('')
    verdict_names = sorted({v for route in routes for v in conformance.get(route, {})})
    if not verdict_names:
        verdict_names = ['conformant']
    lines.append('| Route | n | ' + ' | '.join(verdict_names) + ' |')
    lines.append('|---|---|' + '---|' * len(verdict_names))
    for route in routes:
        row = conformance.get(route, {})
        total = sum(row.values())
        cells = ' | '.join(str(row.get(v, 0)) for v in verdict_names)
        lines.append(f'| {route} | {total} | {cells} |')
    lines.append('')

    lines.append('## Honest caveats')
    lines.append('')
    for caveat in required_caveats:
        lines.append(f'- {CAVEAT_TEXT[caveat]}')
    lines.append('')

    lines.append('## Reproduce')
    lines.append('')
    lines.append('```')
    lines.append('python3 evals/routes/run_routes.py --report-only')
    lines.append('```')
    lines.append('')
    lines.append(
        'That command reads only the committed records under `evals/routes/raw/` and rewrites '
        'this file. It makes no network call and spends nothing. Re-running the live matrix '
        'costs money and is not required to check any figure above.'
    )
    lines.append('')

    return '\n'.join(lines)


def generate_report(raw_dir=None, out_path=None, model=None, effort=None,
                    routes=None, as_of_date=None, repeats=DEFAULT_REPEATS,
                    dropped_routes=()):
    """Offline recompute: load every raw record, aggregate, render, and (if
    `out_path` is given) write.

    Raises ValueError, naming the reason, when `raw_dir` holds zero records
    -- an empty report is never rendered as a successful run, and no file is
    written in that case. Makes zero subprocess calls of its own beyond the
    content-addressed `git hash-object` this path never reaches; self_test()
    proves the no-subprocess property directly by replacing subprocess.run
    with a raiser and running this function end to end.

    `as_of_date` defaults to the records' own timestamps, so re-rendering
    the same records on any later date reproduces this file byte for byte.
    """
    records = load_raw_records(raw_dir)
    if not records:
        raise ValueError(f'no raw records found under {raw_dir} -- nothing to report')

    aggregated = aggregate(records)
    if model is None:
        model = sorted({r['model'] for r in records if r.get('model')})[0]
    if effort is None:
        effort = sorted({r['effort'] for r in records if r.get('effort')})[0]
    if routes is None:
        present = {r.get('route') for r in records}
        routes = [r for r in ROUTES if r in present]
        routes += sorted(x for x in present if x not in ROUTES and x is not None)
    if as_of_date is None:
        as_of_date = _as_of_date_from_records(records)
    scenario_count = len({r.get('scenario_id') for r in records if r.get('scenario_id')})

    text = build_routes_results_md(
        aggregated, model=model, effort=effort, routes=routes, as_of_date=as_of_date,
        session_count=len(records), repeats=repeats, scenario_count=scenario_count,
        dropped_routes=dropped_routes,
    )
    if out_path is not None:
        pathlib.Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(out_path).write_text(text, encoding='utf-8')
    return text


def probe_routes(model=DEFAULT_MODEL, effort=DEFAULT_EFFORT, scenarios=None,
                 probe_dir=None, timeout_s=600, max_budget_usd=MAX_BUDGET_USD,
                 session_fn=run_route_session, scenario_id=PROBE_SCENARIO_ID):
    """Drive the activation probe: one unrouted control and one session per
    route, on a single scenario, plus at most two style-on fallback forms.

    Refuses to drive more than PROBE_SESSION_CAP sessions. Returns the list
    of records driven, in order. Every record is written to `probe_dir` in
    the full schema -- a probe that decides whether the matrix runs is
    evidence, not scratch work.
    """
    probe_dir = pathlib.Path(probe_dir) if probe_dir is not None else PROBE_DIR
    scenarios = scenarios if scenarios is not None else load_scenarios()
    scenario = next((s for s in scenarios if s['id'] == scenario_id), None)
    if scenario is None:
        raise ValueError(f'probe scenario {scenario_id!r} not found in the scenario file')

    records = []
    driven = 0

    def _drive(route, repeat, style_form):
        nonlocal driven
        if driven >= PROBE_SESSION_CAP:
            raise RuntimeError(
                f'probe session cap of {PROBE_SESSION_CAP} reached -- refusing to drive more')
        driven += 1
        try:
            record, _wrote = session_fn(
                model=model, effort=effort, route=route, scenario=scenario, repeat=repeat,
                timeout_s=timeout_s, raw_dir=probe_dir, max_budget_usd=max_budget_usd,
                style_form=style_form,
            )
        except SessionFailedError as exc:
            record = _unscoreable_record(
                model, effort, route, scenario, repeat,
                reason=f'session failed (exit {exc.returncode}): {exc.stderr[:300]}',
            )
            _write_json_atomic(
                raw_path_for_session(model, route, scenario['id'], repeat, probe_dir), record)
        records.append(record)
        return record

    _drive(CONTROL_ROUTE, 0, None)
    _drive('skill-on', 0, None)
    style_record = _drive('style-on', 0, STYLE_ACTIVATION_FORMS[0])
    _drive('prompt-on', 0, None)

    fallback_index = 1
    while (not style_record.get('activated')) and fallback_index < len(STYLE_ACTIVATION_FORMS) \
            and driven < PROBE_SESSION_CAP:
        style_record = _drive('style-on', fallback_index, STYLE_ACTIVATION_FORMS[fallback_index])
        fallback_index += 1

    return records


def discrimination_table(records):
    """Return the probe's discrimination table as a list of lines: one row
    per probe session, with the two signals the drop decision is made on."""
    lines = ['| route | activated | conformance | lint violations | cost_usd | verdict |',
             '|---|---|---|---|---|---|']
    for record in records:
        lines.append(
            f'| {record["route"]} | {record["activated"]} | {record["conformance_verdict"]} | '
            f'{record["lint_violations"]} | {record["cost_usd"]} | {record["verdict"]} |'
        )
    return lines


def self_test():
    """Offline proof of the per-route setup, the record schema, every failure
    path, the aggregator and the renderer.

    No subprocess call to `claude` and no network call; runs on a machine
    with no `claude` binary installed. Every case writes into a temporary
    directory, and the last case proves the real results path was never
    touched.
    """
    all_ok = True
    cases = []

    results_snapshot = RESULTS_PATH.read_bytes() if RESULTS_PATH.exists() else None
    raw_dir_snapshot = sorted(p.name for p in RAW_DIR.glob('*.json')) if RAW_DIR.exists() else None

    fake_scenario = {
        'id': 'executive-summary-1',
        'family': 'executive-summary',
        'prompt': 'Write a two-paragraph executive summary from this brief.',
    }

    real_subprocess_run = subprocess.run

    def _raiser(*args, **kwargs):
        raise AssertionError('subprocess.run called in a mode that must make no subprocess call')

    def _session_cwds(captured):
        """Filter a fake subprocess.run's captured cwds down to the session
        temp dirs only.

        A patched subprocess.run also intercepts _git_blob_sha()'s
        `git hash-object` call, whose cwd is REPO_ROOT -- a directory that
        always exists. Asserting temp-dir removal against that entry would
        report a surviving temp dir that was never a temp dir.
        """
        return [c for c in captured if c and pathlib.Path(c).name.startswith('proof-first-routes-')]

    # --- argv per route -------------------------------------------------
    argv_ok = True
    if route_extra_argv('skill-on'):
        print('FAIL: skill-on added extra argv')
        argv_ok = False
    if route_extra_argv('style-on'):
        print('FAIL: style-on added extra argv in its default form')
        argv_ok = False
    prompt_argv = route_extra_argv('prompt-on')
    if prompt_argv[:1] != ['--append-system-prompt-file']:
        print(f'FAIL: prompt-on argv does not start with the append flag: {prompt_argv}')
        argv_ok = False
    elif not pathlib.Path(prompt_argv[1]).is_absolute():
        print(f'FAIL: prompt-on argv path is not absolute: {prompt_argv[1]}')
        argv_ok = False
    elif not pathlib.Path(prompt_argv[1]).exists():
        print(f'FAIL: prompt-on argv path does not exist: {prompt_argv[1]}')
        argv_ok = False
    for route in ROUTES + (CONTROL_ROUTE,):
        if any('bare' == a.lstrip('-') for a in route_extra_argv(route)):
            print(f'FAIL: {route} argv carries the discovery-skipping isolation flag')
            argv_ok = False
    if argv_ok:
        cases.append('argv-per-route')
    else:
        all_ok = False

    # --- temp-dir setup per route ---------------------------------------
    setup_ok = True
    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp)
        setup_route_dir(d, 'skill-on')
        if not (d / '.claude' / 'skills' / 'proof-first' / 'SKILL.md').exists():
            print('FAIL: skill-on setup did not place SKILL.md')
            setup_ok = False
    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp)
        setup_route_dir(d, 'style-on')
        if not (d / '.claude' / 'output-styles' / 'proof-first.md').exists():
            print('FAIL: style-on setup did not place the style file')
            setup_ok = False
        settings_path = d / '.claude' / 'settings.json'
        if not settings_path.exists():
            print('FAIL: style-on setup did not write settings.json')
            setup_ok = False
        elif json.loads(settings_path.read_text())['outputStyle'] != STYLE_NAME:
            print('FAIL: style-on settings.json outputStyle is not proof-first')
            setup_ok = False
    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp)
        setup_route_dir(d, 'style-on', style_form='settings-local-json')
        if not (d / '.claude' / 'settings.local.json').exists():
            print('FAIL: style-on settings-local-json form did not write settings.local.json')
            setup_ok = False
    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp)
        setup_route_dir(d, 'prompt-on')
        if (d / '.claude').exists():
            print('FAIL: prompt-on setup created a .claude directory')
            setup_ok = False
    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp)
        setup_route_dir(d, CONTROL_ROUTE)
        if (d / '.claude').exists():
            print('FAIL: control setup created a .claude directory')
            setup_ok = False
    if setup_ok:
        cases.append('tmpdir-setup-per-route')
    else:
        all_ok = False

    # --- loading the conformance module writes nothing -------------------
    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp)
        before = sorted(p.name for p in d.iterdir())
        score_fn = _load_conformance_module()
        lint_fn = _load_lint_module()
        after = sorted(p.name for p in d.iterdir())
        if before != after:
            print('FAIL: loading the scorer modules created files')
            all_ok = False
        elif score_fn('') [0] != 'unscoreable':
            print('FAIL: loaded score_transcript does not report empty text unscoreable')
            all_ok = False
        else:
            cases.append('scorer-module-load-writes-nothing')

    # --- activation detector ---------------------------------------------
    activation_cases = [
        ('A sentence citing PF-1.9 in passing.', True),
        ('A sentence citing MC-12 in passing.', True),
        ('A sentence citing no rule at all.', False),
        ('A sentence mentioning PF with no number.', False),
    ]
    detector_ok = True
    for text, expected in activation_cases:
        if bool(MARKER_RE.search(text)) is not expected:
            print(f'FAIL: activation detector wrong for {text!r}')
            detector_ok = False
    if detector_ok:
        cases.append('activation-detector')
    else:
        all_ok = False

    # --- success path: schema, scoring, temp-dir removal -----------------
    captured_cwds = []

    def _fake_success_run(argv, **kwargs):
        captured_cwds.append(kwargs.get('cwd'))
        envelope = {
            'type': 'result',
            'is_error': False,
            'result': ('Executive summary. This response applies PF-1.9 and keeps every '
                       'sentence short.'),
            'usage': {'input_tokens': 10, 'output_tokens': 20},
            'total_cost_usd': 0.1,
            'duration_ms': 1234,
            'cli_version': '2.1.0',
        }
        return subprocess.CompletedProcess(argv, returncode=0, stdout=json.dumps(envelope), stderr='')

    with tempfile.TemporaryDirectory() as tmp:
        raw_dir = pathlib.Path(tmp)
        subprocess.run = _fake_success_run
        try:
            record, wrote = run_route_session(
                model='claude-sonnet-5', effort='low', route='skill-on',
                scenario=fake_scenario, repeat=0, timeout_s=30, raw_dir=raw_dir,
                lint_fn=lint_fn, score_fn=score_fn,
            )
        finally:
            subprocess.run = real_subprocess_run
        missing = [f for f in GENERATION_RECORD_FIELDS if f not in record]
        if missing:
            print(f'FAIL: record missing fields {missing}')
            all_ok = False
        elif not wrote:
            print('FAIL: first call did not report a new write')
            all_ok = False
        elif record['verdict'] != 'generated' or record['activated'] is not True:
            print(f'FAIL: success record verdict/activated wrong: {record["verdict"]}, {record["activated"]}')
            all_ok = False
        elif not raw_path_for_session('claude-sonnet-5', 'skill-on', 'executive-summary-1', 0, raw_dir).exists():
            print('FAIL: success record not written to the frozen filename template')
            all_ok = False
        else:
            cases.append('record-schema-complete')

        session_cwds = _session_cwds(captured_cwds)
        if session_cwds and pathlib.Path(session_cwds[0]).exists():
            print('FAIL: temp dir survived the success path')
            all_ok = False
        else:
            cases.append('tmpdir-removed-on-success')

        # --- skip-if-exists makes no subprocess call ---------------------
        subprocess.run = _raiser
        try:
            record2, wrote2 = run_route_session(
                model='claude-sonnet-5', effort='low', route='skill-on',
                scenario=fake_scenario, repeat=0, timeout_s=30, raw_dir=raw_dir,
                lint_fn=lint_fn, score_fn=score_fn,
            )
            if wrote2 or record2['run_id'] != record['run_id']:
                print('FAIL: skip-if-exists did not return the committed record untouched')
                all_ok = False
            else:
                cases.append('skip-if-exists-no-subprocess')
        except AssertionError:
            print('FAIL: skip-if-exists made a subprocess call')
            all_ok = False
        finally:
            subprocess.run = real_subprocess_run

    # --- the four unscoreable paths --------------------------------------
    def _make_fake(returncode, stdout, stderr=''):
        def _fake(argv, **kwargs):
            captured_cwds.append(kwargs.get('cwd'))
            return subprocess.CompletedProcess(argv, returncode=returncode, stdout=stdout, stderr=stderr)
        return _fake

    failure_cases = [
        ('unscoreable-non-zero-exit', _make_fake(1, '', 'boom'), True),
        ('unscoreable-is-error', _make_fake(0, json.dumps({'is_error': True, 'result': 'limit'})), True),
        ('unscoreable-unparseable-envelope', _make_fake(0, 'not json at all'), True),
        ('unscoreable-empty-text', _make_fake(0, json.dumps({'is_error': False, 'result': '   '})), False),
    ]
    for case_name, fake, expect_raise in failure_cases:
        with tempfile.TemporaryDirectory() as tmp:
            raw_dir = pathlib.Path(tmp)
            captured_cwds.clear()
            subprocess.run = fake
            raised = None
            record = None
            try:
                record, _ = run_route_session(
                    model='claude-sonnet-5', effort='low', route='prompt-on',
                    scenario=fake_scenario, repeat=0, timeout_s=30, raw_dir=raw_dir,
                    lint_fn=lint_fn, score_fn=score_fn,
                )
            except SessionFailedError as exc:
                raised = exc
            finally:
                subprocess.run = real_subprocess_run

            if expect_raise:
                if raised is None:
                    print(f'FAIL: {case_name} did not raise SessionFailedError')
                    all_ok = False
                    continue
                record = _unscoreable_record(
                    'claude-sonnet-5', 'low', 'prompt-on', fake_scenario, 0,
                    reason=f'session failed (exit {raised.returncode}): {raised.stderr[:300]}',
                )
            if record is None or record['verdict'] != 'unscoreable' or not record['reason']:
                print(f'FAIL: {case_name} did not produce an unscoreable record with a reason')
                all_ok = False
                continue
            if [f for f in GENERATION_RECORD_FIELDS if f not in record]:
                print(f'FAIL: {case_name} record is missing schema fields')
                all_ok = False
                continue
            session_cwds = _session_cwds(captured_cwds)
            if session_cwds and pathlib.Path(session_cwds[-1]).exists():
                print(f'FAIL: temp dir survived the {case_name} path')
                all_ok = False
                continue
            cases.append(case_name)
    cases.append('tmpdir-removed-on-failure')

    # --- aggregate excludes unscoreable and reports actual n --------------
    def _rec(route, text, verdict='generated', timestamp='2026-09-21T10:00:00+00:00'):
        base = _unscoreable_record('claude-sonnet-5', 'low', route, fake_scenario, 0, reason='x')
        base.update({'text': text, 'verdict': verdict, 'timestamp': timestamp,
                     'reason': None if verdict == 'generated' else 'x'})
        return base

    good = 'Executive summary. The migration applies PF-1.9. It moved 12 workloads in 6 weeks.'
    mixed = [
        _rec('skill-on', good),
        _rec('skill-on', good),
        _rec('skill-on', '', verdict='unscoreable'),
        _rec('prompt-on', good),
    ]
    agg = aggregate(mixed, lint_fn=lint_fn, score_fn=score_fn)
    if agg['mechanical']['skill-on']['n'] != 2:
        print(f'FAIL: aggregate did not report the actual n: {agg["mechanical"]["skill-on"]}')
        all_ok = False
    elif agg['unscoreable']['skill-on'] != 1:
        print('FAIL: aggregate did not count the unscoreable record')
        all_ok = False
    elif agg['activation']['skill-on']['n'] != 2:
        print('FAIL: aggregate activation n includes an unscoreable record')
        all_ok = False
    else:
        cases.append('unscoreable-excluded-from-means')

    # --- renderer: required caveats, no composite score, determinism ------
    rendered = build_routes_results_md(
        agg, model='claude-sonnet-5', effort='low', routes=['skill-on', 'prompt-on'],
        as_of_date='2026-09-21', session_count=4, repeats=3, scenario_count=1,
    )
    missing_caveats = _missing_required_caveats(rendered)
    missing_headings = [h for h in RESULTS_SECTION_HEADINGS if h not in rendered]
    if missing_caveats:
        print(f'FAIL: rendered report is missing caveats {missing_caveats}')
        all_ok = False
    elif missing_headings:
        print(f'FAIL: rendered report is missing headings {missing_headings}')
        all_ok = False
    elif 'composite' in rendered.lower() or '## Overall score' in rendered:
        print('FAIL: rendered report blends the two measures into one score')
        all_ok = False
    elif rendered != build_routes_results_md(
            agg, model='claude-sonnet-5', effort='low', routes=['skill-on', 'prompt-on'],
            as_of_date='2026-09-21', session_count=4, repeats=3, scenario_count=1):
        print('FAIL: renderer is not deterministic')
        all_ok = False
    else:
        cases.append('render-caveats-headings-deterministic')

    # --- separation verdict never says "equivalent" on overlap -----------
    overlap = {'skill-on': {'n': 3, 'mean': 4.0, 'min': 2, 'max': 6},
               'prompt-on': {'n': 3, 'mean': 5.0, 'min': 3, 'max': 7}}
    sentence = separation_verdict(overlap, ['skill-on', 'prompt-on'])
    if 'did not distinguish' not in sentence:
        print(f'FAIL: overlapping ranges did not produce a not-distinguished verdict: {sentence}')
        all_ok = False
    elif re.search(r'\bare equivalent\b', sentence):
        print('FAIL: overlapping ranges produced an equivalence claim')
        all_ok = False
    else:
        separated = separation_verdict(
            {'skill-on': {'n': 3, 'mean': 1.0, 'min': 0, 'max': 2},
             'prompt-on': {'n': 3, 'mean': 9.0, 'min': 8, 'max': 10}},
            ['skill-on', 'prompt-on'])
        if 'Non-overlapping' not in separated:
            print('FAIL: non-overlapping ranges were not reported as separated')
            all_ok = False
        else:
            cases.append('separation-verdict-discriminates')

    # --- --report-only makes no subprocess call, and is clock-independent -
    class _FrozenDatetime(datetime.datetime):
        _fake_now = None

        @classmethod
        def now(cls, tz=None):
            return cls._fake_now

    real_datetime_class = datetime.datetime
    with tempfile.TemporaryDirectory() as tmp:
        fixture_raw = pathlib.Path(tmp) / 'raw'
        fixture_raw.mkdir()
        for i, record in enumerate(mixed):
            _write_json_atomic(fixture_raw / f'rec{i}.json', record)
        out_path = pathlib.Path(tmp) / 'RESULTS-routes.md'

        subprocess.run = _raiser
        try:
            text_a = generate_report(raw_dir=fixture_raw, out_path=out_path)
            cases.append('report-only-no-subprocess-call')
        except AssertionError:
            print('FAIL: --report-only made a subprocess call')
            all_ok = False
            text_a = None
        finally:
            subprocess.run = real_subprocess_run

        if text_a is not None:
            try:
                datetime.datetime = _FrozenDatetime
                _FrozenDatetime._fake_now = real_datetime_class(2099, 1, 1, tzinfo=datetime.timezone.utc)
                clock_a = generate_report(raw_dir=fixture_raw, out_path=out_path)
                _FrozenDatetime._fake_now = real_datetime_class(2000, 6, 15, tzinfo=datetime.timezone.utc)
                clock_b = generate_report(raw_dir=fixture_raw, out_path=out_path)
            finally:
                datetime.datetime = real_datetime_class
            if clock_a != clock_b:
                print('FAIL: --report-only is not clock-independent')
                all_ok = False
            elif '2099-01-01' in clock_a or '2000-06-15' in clock_b:
                print('FAIL: --report-only rendered a render-time clock date')
                all_ok = False
            elif 'Measured 2026-09-21' not in clock_a:
                print('FAIL: --report-only did not derive the as-of date from the records')
                all_ok = False
            else:
                cases.append('render-clock-independent')

    # --- empty raw dir is a named failure, not an empty report ------------
    with tempfile.TemporaryDirectory() as tmp:
        try:
            generate_report(raw_dir=pathlib.Path(tmp) / 'nothing', out_path=None)
            print('FAIL: generate_report rendered a report from zero records')
            all_ok = False
        except ValueError:
            cases.append('empty-raw-dir-is-a-named-failure')

    # --- the probe refuses to exceed its session cap ----------------------
    drive_count = {'n': 0}

    def _counting_session(**kwargs):
        drive_count['n'] += 1
        record = _unscoreable_record(
            kwargs['model'], kwargs['effort'], kwargs['route'], kwargs['scenario'],
            kwargs['repeat'], reason='probe stub')
        record['activated'] = False
        return record, True

    with tempfile.TemporaryDirectory() as tmp:
        try:
            probe_routes(scenarios=[fake_scenario], probe_dir=pathlib.Path(tmp),
                         session_fn=_counting_session, scenario_id='executive-summary-1')
        except RuntimeError:
            pass
        if drive_count['n'] > PROBE_SESSION_CAP:
            print(f'FAIL: probe drove {drive_count["n"]} sessions, above the cap')
            all_ok = False
        else:
            cases.append('probe-session-cap-enforced')

    # --- run_matrix enumerates route x scenario x repeat, skipping nothing -
    enumerated = []

    def _enumerating_session(**kwargs):
        enumerated.append((kwargs['route'], kwargs['scenario']['id'], kwargs['repeat']))
        return {}, False

    with tempfile.TemporaryDirectory() as tmp:
        order = run_matrix(
            model='claude-sonnet-5', routes=['skill-on', 'prompt-on'],
            scenarios=[fake_scenario], repeats=2, raw_dir=pathlib.Path(tmp), timeout_s=5,
            session_fn=_enumerating_session,
        )
    expected_order = [('skill-on', 'executive-summary-1', 0), ('skill-on', 'executive-summary-1', 1),
                      ('prompt-on', 'executive-summary-1', 0), ('prompt-on', 'executive-summary-1', 1)]
    if order != expected_order or enumerated != expected_order:
        print(f'FAIL: run_matrix enumeration order wrong: {order}')
        all_ok = False
    else:
        cases.append('matrix-enumeration-order')

    # --- self_test() never wrote the real results path or raw dir ---------
    results_after = RESULTS_PATH.read_bytes() if RESULTS_PATH.exists() else None
    raw_after = sorted(p.name for p in RAW_DIR.glob('*.json')) if RAW_DIR.exists() else None
    if results_after != results_snapshot or raw_after != raw_dir_snapshot:
        print('FAIL: self_test() modified the real results path or raw directory')
        all_ok = False
    else:
        cases.append('self-test-never-writes-real-results-path')

    if not all_ok:
        return False

    print('self-test PASS - cases exercised: ' + ', '.join(cases))
    return True


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--self-test', action='store_true',
                        help='Offline proof; makes no subprocess or network call.')
    parser.add_argument('--probe', action='store_true',
                        help=f'Activation probe; at most {PROBE_SESSION_CAP} live sessions.')
    parser.add_argument('--report-only', action='store_true',
                        help='Offline recompute of RESULTS-routes.md; makes no subprocess call.')
    parser.add_argument('--model', default=DEFAULT_MODEL,
                        help=f'Model id (default: {DEFAULT_MODEL}).')
    parser.add_argument('--effort', default=DEFAULT_EFFORT,
                        help=f'Reasoning effort passed to --effort (default: {DEFAULT_EFFORT}).')
    parser.add_argument('--repeats', type=int, default=DEFAULT_REPEATS,
                        help=f'Repeats per route x scenario cell (default: {DEFAULT_REPEATS}).')
    parser.add_argument('--routes', default=','.join(ROUTES),
                        help=f'Comma-separated subset of {",".join(ROUTES)}.')
    parser.add_argument('--scenarios', default=str(SCENARIOS_PATH),
                        help='Path to the scenarios JSON file. Read, never written.')
    parser.add_argument('--raw-dir', default=str(RAW_DIR),
                        help='Directory for committed raw route records.')
    parser.add_argument('--probe-dir', default=str(PROBE_DIR),
                        help='Directory for committed probe records.')
    parser.add_argument('--out', default=str(RESULTS_PATH),
                        help='RESULTS-routes.md path (only used by --report-only).')
    parser.add_argument('--timeout', type=int, default=600,
                        help='Per-session timeout in seconds (default: 600).')
    parser.add_argument('--max-budget-usd', type=float, default=MAX_BUDGET_USD,
                        help=f'Per-session cost cap (default: {MAX_BUDGET_USD}).')
    parser.add_argument('--scenario-filter', default='',
                        help='Comma-separated scenario ids to restrict the matrix to.')
    args = parser.parse_args()

    if args.self_test:
        sys.exit(0 if self_test() else 1)

    if args.report_only:
        try:
            text = generate_report(raw_dir=args.raw_dir, out_path=args.out)
        except ValueError as exc:
            print(f'report-only failed: {exc}', file=sys.stderr)
            sys.exit(1)
        print(f'wrote {args.out} ({len(text)} chars)')
        sys.exit(0)

    if args.probe:
        scenarios = load_scenarios(args.scenarios)
        records = probe_routes(
            model=args.model, effort=args.effort, scenarios=scenarios,
            probe_dir=args.probe_dir, timeout_s=args.timeout,
            max_budget_usd=args.max_budget_usd,
        )
        for line in discrimination_table(records):
            print(line)
        total = sum((r.get('cost_usd') or 0) for r in records)
        print(f'probe sessions: {len(records)}, total cost_usd: {round(total, 4)}')
        sys.exit(0)

    routes = [r.strip() for r in args.routes.split(',') if r.strip()]
    unknown = [r for r in routes if r not in ROUTES]
    if unknown:
        print(f'unknown route(s): {unknown}; known routes are {list(ROUTES)}', file=sys.stderr)
        sys.exit(1)

    scenarios = load_scenarios(args.scenarios)
    if args.scenario_filter:
        wanted = {s.strip() for s in args.scenario_filter.split(',') if s.strip()}
        missing = wanted - {s['id'] for s in scenarios}
        if missing:
            print(f'unknown scenario id(s): {sorted(missing)}', file=sys.stderr)
            sys.exit(1)
        scenarios = [s for s in scenarios if s['id'] in wanted]

    cells = len(routes) * len(scenarios) * args.repeats
    print(
        f'Running route matrix: {len(routes)} route(s) x {len(scenarios)} scenario(s) x '
        f'{args.repeats} repeat(s) = {cells} cells (existing raw files are skipped, not re-paid '
        f'for)',
        file=sys.stderr,
    )
    run_matrix(
        model=args.model, routes=routes, scenarios=scenarios, repeats=args.repeats,
        raw_dir=args.raw_dir, timeout_s=args.timeout, effort=args.effort,
        max_budget_usd=args.max_budget_usd,
    )
    print('Live matrix complete. Run --report-only to (re)generate RESULTS-routes.md.',
          file=sys.stderr)
    sys.exit(0)


if __name__ == '__main__':
    main()
