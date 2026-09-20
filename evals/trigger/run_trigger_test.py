#!/usr/bin/env python3
"""Drive the trigger pressure test in `evals/pressure-tests.md` against a live harness.

What this measures, and what it does not
----------------------------------------
This runner answers exactly one question per phrasing: did the harness activate
`proof-first` on its own, from the skill's frontmatter `description` alone, with
nothing in the prompt naming the skill? It reads the answer from the session's
own event stream -- a `Skill` tool-use event whose `skill` field names
`proof-first` -- not from the prose the session produced. Reading activation out
of the prose would guess; the event stream states it.

It does not measure a trigger-reliability rate. One observation per phrasing is
one observation, not a rate, and this file never computes a percentage from
them. A measured rate across many phrasings and models is the eval harness's
job (`evals/benchmark/`), not this file's. `--repeats` (added for the CAT-10
gap-closure round) reports a `k of n` count per phrasing and, for a phrasing
with zero fires, the exact Clopper-Pearson upper bound on its true fire rate
from `stats.py` -- never a percentage. A bound at n=5 is 0.4507: a bound, not
a measured rate, and it is a statement about that one phrasing under repeated
sampling from the same harness on the same day, nothing broader.

Deliberately NOT passed to the session
--------------------------------------
`--bare`. It skips skill auto-discovery, which is the exact behaviour under
test. Letting the skill activate off its own `description` is the measurement,
not a setup detail. The cost is that the operator's own user-level
configuration under `$HOME` still loads, so other installed skills are present
in the session -- the same condition every prior live measurement in this
repository ran under, and disclosed rather than hidden.

Known ceiling, stated plainly
-----------------------------
A non-fire recorded here is a non-fire in one session against one model. It is
not proof that the description can never fire on that phrasing; `claude -p`
exposes no temperature or seed flag, so a repeat can differ. The Observed cells
this run fills carry a date and a model precisely so a later reader can tell how
old and how narrow the observation is.

Usage
-----
    python3 evals/trigger/run_trigger_test.py --self-test
    python3 evals/trigger/run_trigger_test.py --model claude-sonnet-5
"""

import argparse
import concurrent.futures
import datetime
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

import stats

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
PRESSURE_TESTS = REPO_ROOT / 'evals' / 'pressure-tests.md'
SKILL_SRC = REPO_ROOT / 'skills' / 'proof-first'
RESULTS_PATH = REPO_ROOT / 'evals' / 'trigger' / 'RESULTS-trigger.md'

SKILL_NAME = 'proof-first'
DISALLOWED_TOOLS = ['Write', 'Edit', 'Bash', 'NotebookEdit']
DEFAULT_MODEL = 'claude-sonnet-5'
DEFAULT_TIMEOUT_S = 600

# The Scope section of pressure-tests.md binds every row to one exact
# `description`, identified by the sha256 of SKILL.md's first 14 lines. An
# observation recorded against a different description is not an observation of
# these rows, so a mismatch halts rather than filling cells in.
SCOPE_HASH_LINES = 14

VERDICT_FIRED = 'fired'
VERDICT_DID_NOT_FIRE = 'did not fire'
VERDICT_UNSCOREABLE = 'unscoreable'


def scope_hash(skill_md_path):
    """sha256 of SKILL.md's first SCOPE_HASH_LINES lines, as pressure-tests.md records it."""
    text = pathlib.Path(skill_md_path).read_text(encoding='utf-8')
    head = ''.join(text.splitlines(keepends=True)[:SCOPE_HASH_LINES])
    return hashlib.sha256(head.encode('utf-8')).hexdigest()


def recorded_scope_hash(md_text):
    """Pull the sha256 the Scope section binds the rows to. None if absent.

    Scoped to the ## Scope section on purpose (02-REVIEW.md CR-01): an earlier
    form searched the whole document, so any later sha256 reference added
    anywhere in pressure-tests.md would have been adopted as the binding.
    """
    scope = re.search(r'^##\s+Scope\s*$(.*?)(?=^##\s|\Z)', md_text, re.M | re.S)
    if not scope:
        return None
    match = re.search(r'\b([0-9a-f]{64})\b', scope.group(1))
    return match.group(1) if match else None


def parse_tables(md_text):
    """Return [(table, phrasing, expected_fire)] for the two pressure-test tables.

    Reads the phrasings out of the document itself rather than carrying a second
    copy of them here, so the runner and the file it fills in cannot drift apart.
    """
    rows = []
    table = None
    for line in md_text.splitlines():
        heading = re.match(r'^##\s+(.*?)\s*$', line)
        if heading:
            title = heading.group(1).lower()
            if title == 'must fire':
                table = ('must-fire', True)
            elif title == 'must not fire':
                table = ('must-not-fire', False)
            else:
                table = None
            continue
        if table is None or not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 5:
            continue
        phrasing, expected = cells[0], cells[1]
        if phrasing.lower() == 'phrasing' or set(phrasing) <= set('-: '):
            continue
        rows.append((table[0], phrasing, table[1], expected))
    return rows


def detect_activation(stream_text):
    """True iff the session's own event stream shows a Skill tool-use naming proof-first.

    Reads structured events, never the model's prose: a session that merely
    talks about RFP writing has not activated the skill, and a session that
    activated it says so in a `tool_use` event whether or not the prose shows it.
    """
    for line in stream_text.splitlines():
        line = line.strip()
        if not line.startswith('{'):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        message = event.get('message')
        if not isinstance(message, dict):
            continue
        content = message.get('content')
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get('type') != 'tool_use' or block.get('name') != 'Skill':
                continue
            skill = (block.get('input') or {}).get('skill', '')
            if isinstance(skill, str) and skill.split(':')[-1] == SKILL_NAME:
                return True
    return False


def run_session(skill_src, phrasing, model, out_path, timeout_s):
    """Drive one live `claude -p` session for one phrasing in an isolated temp dir.

    Returns (verdict, note). Exactly one call site writes any given out_path --
    concurrent writers to one path is the defect that produced a false
    "duplicated sections" finding in an earlier UAT pass.

    out_path lands OUTSIDE the session's cwd on purpose: a session whose own
    transcript sits under its working directory can glob and read it mid-run,
    which contaminates the measurement with the measurement.
    """
    skill_src = pathlib.Path(skill_src)
    out_path = pathlib.Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    tmp_dir = pathlib.Path(tempfile.mkdtemp(prefix='proof-first-trigger-'))
    try:
        skill_dst = tmp_dir / '.claude' / 'skills' / SKILL_NAME
        skill_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(skill_src, skill_dst)

        argv = [
            'claude', '-p', phrasing,
            '--model', model,
            '--output-format', 'stream-json', '--verbose',
            '--disallowedTools',
        ] + DISALLOWED_TOOLS

        try:
            result = subprocess.run(
                argv,
                cwd=str(tmp_dir),
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=timeout_s,
            )
        except subprocess.TimeoutExpired:
            out_path.write_text('', encoding='utf-8')
            return VERDICT_UNSCOREABLE, 'session exceeded %ds timeout' % timeout_s

        stream = result.stdout or ''
        out_path.write_text(stream, encoding='utf-8')

        if result.returncode != 0:
            return VERDICT_UNSCOREABLE, 'session exited %d' % result.returncode
        if not stream.strip():
            return VERDICT_UNSCOREABLE, 'session produced no output'

        return (VERDICT_FIRED if detect_activation(stream) else VERDICT_DID_NOT_FIRE), ''
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


# --- repeats, overwrite guard, and labelled append blocks ------------------

def aggregate_verdicts(verdicts):
    """Reduce a list of per-repeat verdict strings to (fires, scoreable).

    An unscoreable session is excluded from both the numerator and the
    denominator -- it is never retried into a verdict and never rounded into
    one. `fires` counts VERDICT_FIRED entries; `scoreable` counts every entry
    that is not VERDICT_UNSCOREABLE.
    """
    scoreable = sum(1 for v in verdicts if v != VERDICT_UNSCOREABLE)
    fires = sum(1 for v in verdicts if v == VERDICT_FIRED)
    return fires, scoreable


def resolve_out_mode(exists, nonempty, append, path=None):
    """Decide whether a run writes fresh or appends, and refuse a silent clobber.

    This is the accident that would otherwise destroy the 2026-09-20
    measurement: `write_results()` calls `write_text()`, which overwrites
    unconditionally. A non-empty existing `--out` without `--append` raises
    rather than silently discarding whatever measurement history is already
    there.
    """
    label = path if path else 'the --out file'
    if exists and nonempty and not append:
        raise ValueError(
            '%s already has content. Re-run with --append and --label to add a new '
            'run block without destroying it, or point --out at a different path.'
            % label
        )
    if exists and nonempty and append:
        return 'append'
    return 'write'


def scope_binding_verdict(bound_hash, live_hash, path=None):
    """Decide whether the recorded rows are provably bound to the live description.

    02-REVIEW.md CR-01: the earlier form of this check read `if bound_hash and
    bound_hash != live_hash`, which is falsy when no binding was found at all --
    so a document with a missing or malformed Scope hash ran with the guard
    silently skipped, which is the one thing this instrument must never do. An
    absent binding is a refusal, not a pass.
    """
    label = path if path else 'the --tests file'
    if bound_hash is None:
        raise ValueError(
            '%s records no sha256 under its ## Scope heading, so its rows cannot be '
            'shown to belong to the live description. Add the binding before running.'
            % label
        )
    if bound_hash != live_hash:
        raise ValueError(
            '%s binds its rows to description sha256 %s but the live SKILL.md '
            'hashes to %s. The rows must be re-authored against the new description, '
            'not filled in.' % (label, bound_hash, live_hash)
        )
    return 'bound'


def render_run_block(label, rows, counts, model='', harness_version='',
                      scope_hash_value='', repeats=1, run_date=''):
    """Render one labelled `## Run` block: a k-of-n count per row, never a percentage.

    `rows` is `[(table, phrasing, expects_fire, expected_text), ...]` as
    `parse_tables()` returns. `counts` is `[(fires, scoreable), ...]` aligned
    with `rows`, one pair per phrasing, already reduced by
    `aggregate_verdicts()`. Every zero-fire row gets its exact
    Clopper-Pearson upper bound from `stats.py`; no row anywhere gets a rate.
    """
    planned = repeats * len(rows)
    scoreable_total = sum(c[1] for c in counts)

    lines = [
        '## Run — %s' % label,
        '',
        '| Field | Value |',
        '|---|---|',
        '| Date | %s |' % run_date,
        '| Model | `%s` |' % model,
        '| Harness | `claude` %s |' % harness_version,
        '| SKILL.md description sha256 (first %d lines) | `%s` |' % (SCOPE_HASH_LINES, scope_hash_value),
        '| Repeats per phrasing | %d |' % repeats,
        '| Sessions planned | %d |' % planned,
        '| Sessions scoreable | %d |' % scoreable_total,
        '',
        '### Verdicts',
        '',
        '| Table | Phrasing | Expected | Observed | Match | Clopper-Pearson upper bound (alpha 0.05) |',
        '|---|---|---|---|---|---|',
    ]

    of_total = sn_total = mh_total = sm_total = 0
    for (table, phrasing, expects_fire, expected_text), (fires, scoreable) in zip(rows, counts):
        if expects_fire:
            mh_total += fires
            sm_total += scoreable
        else:
            of_total += fires
            sn_total += scoreable

        if scoreable == 0:
            match = 'unscoreable'
        elif expects_fire:
            match = 'yes' if fires == scoreable else 'NO'
        else:
            match = 'yes' if fires == 0 else 'NO'

        bound = '%.4f' % stats.clopper_pearson_upper(0, scoreable) if (fires == 0 and scoreable > 0) else '-'
        observed = 'fired %d of %d scoreable' % (fires, scoreable)
        lines.append('| %s | %s | %s | %s | %s | %s |' % (table, phrasing, expected_text, observed, match, bound))

    lines += [
        '',
        '### Totals',
        '',
        '- OF (over-fires, must-not-fire rows) = %d' % of_total,
        '- SN (scoreable, must-not-fire rows) = %d' % sn_total,
        '- MH (must-fire hits) = %d' % mh_total,
        '- SM (scoreable, must-fire rows) = %d' % sm_total,
    ]
    return '\n'.join(lines)


# --- self-test -------------------------------------------------------------

_FIRED_FIXTURE = '\n'.join([
    json.dumps({'type': 'system', 'subtype': 'init', 'slash_commands': ['proof-first']}),
    json.dumps({'type': 'assistant', 'message': {'role': 'assistant', 'content': [
        {'type': 'tool_use', 'id': 't1', 'name': 'Skill',
         'input': {'skill': 'proof-first', 'args': 'RFP question 4'}}]}}),
])

# The discriminating case: the word appears all over the stream -- in the
# available-skills list and in the model's own prose -- but no Skill tool-use
# names it. A detector that grepped for the string would call this fired.
_NOT_FIRED_FIXTURE = '\n'.join([
    json.dumps({'type': 'system', 'subtype': 'init', 'slash_commands': ['proof-first']}),
    json.dumps({'type': 'assistant', 'message': {'role': 'assistant', 'content': [
        {'type': 'text', 'text': 'I could use proof-first here, but I will just write it.'}]}}),
    json.dumps({'type': 'assistant', 'message': {'role': 'assistant', 'content': [
        {'type': 'tool_use', 'id': 't2', 'name': 'Skill',
         'input': {'skill': 'simple-english'}}]}}),
])

_SELF_TEST_MD = """# heading

## Scope

bound to d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675 exactly.

## Must fire

| Phrasing | Expected | Observed | Date | Harness |
|---|---|---|---|---|
| Write our RFP answer. | Fires | not yet observed | - | - |

## Must not fire

| Phrasing | Expected | Observed | Date | Harness |
|---|---|---|---|---|
| Write launch copy. | Does not fire | not yet observed | - | - |

## Observations

nothing yet.
"""

# CR-01 defect (b): a sha256 somewhere else in the document is NOT the binding.
# This is the exact edit shape the review names as the live risk -- a later,
# unrelated hash reference added to pressure-tests.md.
_SCOPE_DECOY_MD = """# heading

Recorded elsewhere: """ + 'a' * 64 + """ (an unrelated reference, not the binding).

## Scope

no hash recorded here yet.

## Must fire

| Phrasing | Expected | Observed | Date | Harness |
|---|---|---|---|---|
| Write our RFP answer. | Fires | not yet observed | - | - |
"""

_SCOPE_WINS_MD = """# heading

Recorded elsewhere: """ + 'a' * 64 + """ (an unrelated reference, not the binding).

## Scope

bound to """ + 'b' * 64 + """ exactly.

## Must fire

| Phrasing | Expected | Observed | Date | Harness |
|---|---|---|---|---|
| Write our RFP answer. | Fires | not yet observed | - | - |
"""


def self_test():
    """Prove the two offline judgements discriminate, with no model call and no quota spend."""
    failures = []

    if not detect_activation(_FIRED_FIXTURE):
        failures.append('detect_activation missed a real Skill tool-use for proof-first')
    if detect_activation(_NOT_FIRED_FIXTURE):
        failures.append('detect_activation fired on a stream that only mentions proof-first')
    if detect_activation(''):
        failures.append('detect_activation fired on an empty stream')

    rows = parse_tables(_SELF_TEST_MD)
    if len(rows) != 2:
        failures.append('parse_tables read %d rows from the 2-row fixture' % len(rows))
    else:
        if rows[0] != ('must-fire', 'Write our RFP answer.', True, 'Fires'):
            failures.append('parse_tables misread the must-fire row: %r' % (rows[0],))
        if rows[1] != ('must-not-fire', 'Write launch copy.', False, 'Does not fire'):
            failures.append('parse_tables misread the must-not-fire row: %r' % (rows[1],))

    if recorded_scope_hash(_SELF_TEST_MD) != 'd5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675':
        failures.append('recorded_scope_hash did not read the bound hash out of the Scope section')
    if recorded_scope_hash('no hash here') is not None:
        failures.append('recorded_scope_hash invented a hash where none is recorded')
    if recorded_scope_hash(_SCOPE_DECOY_MD) is not None:
        failures.append('recorded_scope_hash adopted a sha256 from outside the ## Scope '
                        'section as the binding (02-REVIEW.md CR-01 defect (b))')
    if recorded_scope_hash(_SCOPE_WINS_MD) != 'b' * 64:
        failures.append('recorded_scope_hash did not prefer the ## Scope hash over an '
                        'earlier unrelated one elsewhere in the document')

    # --- scope-binding guard: an absent binding must refuse (3 cases) ---
    absent_msg = ''
    try:
        scope_binding_verdict(None, 'a' * 64, path='fixture.md')
    except ValueError as exc:
        absent_msg = str(exc)
    if 'no sha256' not in absent_msg:
        failures.append('scope_binding_verdict(None, ...) did not refuse via its absent-binding '
                        'branch (got %r) -- a document with no recorded binding would run with '
                        'the guard silently skipped (02-REVIEW.md CR-01 defect (a))'
                        % (absent_msg or 'no refusal at all'))
    mismatch_msg = ''
    try:
        scope_binding_verdict('a' * 64, 'b' * 64, path='fixture.md')
    except ValueError as exc:
        mismatch_msg = str(exc)
    if 'binds its rows' not in mismatch_msg:
        failures.append('scope_binding_verdict did not refuse a hash mismatch via its mismatch '
                        'branch (got %r) -- rows bound to a different description would be '
                        'filled in as observations' % (mismatch_msg or 'no refusal at all'))
    if scope_binding_verdict('a' * 64, 'a' * 64) != 'bound':
        failures.append('scope_binding_verdict refused a correctly bound document')

    # --- repeats aggregation (1 case) ---
    fires, scoreable = aggregate_verdicts(
        [VERDICT_FIRED, VERDICT_FIRED, VERDICT_DID_NOT_FIRE, VERDICT_UNSCOREABLE, VERDICT_FIRED])
    if (fires, scoreable) != (3, 4):
        failures.append('aggregate_verdicts(...) = (%d, %d), expected (3, 4) -- an unscoreable '
                         'session leaked into a numerator or a denominator' % (fires, scoreable))

    # --- overwrite guard (4 cases) ---
    if resolve_out_mode(False, False, False) != 'write':
        failures.append('resolve_out_mode(False, False, False) did not return "write"')
    guarded = False
    try:
        resolve_out_mode(True, True, False)
    except ValueError:
        guarded = True
    if not guarded:
        failures.append('resolve_out_mode(True, True, False) did NOT raise -- a non-empty '
                         'results file could be clobbered without --append')
    if resolve_out_mode(True, True, True) != 'append':
        failures.append('resolve_out_mode(True, True, True) did not return "append"')
    if resolve_out_mode(True, False, False) != 'write':
        failures.append('resolve_out_mode(True, False, False) did not return "write"')

    # --- render_run_block (5 cases) ---
    fixture_rows = [
        ('must-fire', 'Write our RFP answer.', True, 'Fires'),
        ('must-not-fire', 'Write launch copy.', False, 'Does not fire'),
    ]
    fixture_counts = [(5, 5), (0, 5)]
    block = render_run_block(label='self-test fixture', rows=fixture_rows, counts=fixture_counts,
                              model='claude-sonnet-5', harness_version='2.1.267 (Claude Code)',
                              scope_hash_value='deadbeef', repeats=5, run_date='2026-09-20')
    if re.findall(r'[0-9]+(?:\.[0-9]+)?%', block):
        failures.append('render_run_block emitted a percentage token, which this instrument forbids')
    if 'fired 5 of 5 scoreable' not in block:
        failures.append("render_run_block did not report the must-fire row's k-of-n count")
    if 'fired 0 of 5 scoreable' not in block:
        failures.append("render_run_block did not report the must-not-fire row's k-of-n count")
    if '0.4507' not in block:
        failures.append('render_run_block did not carry the n=5 Clopper-Pearson bound for the zero-fire row')
    if 'self-test fixture' not in block:
        failures.append("render_run_block did not carry its own label")

    for problem in failures:
        print('FAIL: %s' % problem)
    if failures:
        print('self-test FAIL: %d problem(s)' % len(failures))
        return 1
    print('self-test PASS: 3 detector cases, 2 table rows, 4 scope-hash cases, '
          '3 scope-binding-guard cases, 1 aggregate-verdicts case, 4 overwrite-guard '
          'cases, 5 render-block cases')
    return 0


# --- results ---------------------------------------------------------------

def write_results(path, model, run_date, rows, results, live_hash, harness_version):
    lines = [
        '# Trigger Pressure Test — Run Results',
        '',
        'Produced by `python3 evals/trigger/run_trigger_test.py`. Each row below is one live',
        '`claude -p` session in a fresh temp directory outside this repository, with only',
        '`skills/proof-first/` copied into its `.claude/skills/`, no `--bare`, and nothing in the',
        'prompt naming the skill. The verdict is read from the session\'s own event stream (a',
        '`Skill` tool-use naming `proof-first`), not from the prose it produced.',
        '',
        '## Run',
        '',
        '| Field | Value |',
        '|---|---|',
        '| Date | %s |' % run_date,
        '| Model | `%s` |' % model,
        '| Harness | `claude` %s |' % harness_version,
        '| SKILL.md description sha256 (first %d lines) | `%s` |' % (SCOPE_HASH_LINES, live_hash),
        '| Sessions | %d |' % len(results),
        '',
        '## Verdicts',
        '',
        '| Table | Phrasing | Expected | Observed | Match |',
        '|---|---|---|---|---|',
    ]
    mismatches = 0
    unscoreable = 0
    for (table, phrasing, expects_fire, expected_text), (verdict, note) in zip(rows, results):
        if verdict == VERDICT_UNSCOREABLE:
            match = 'unscoreable'
            unscoreable += 1
        elif (verdict == VERDICT_FIRED) == expects_fire:
            match = 'yes'
        else:
            match = 'NO'
            mismatches += 1
        observed = verdict if not note else '%s (%s)' % (verdict, note)
        lines.append('| %s | %s | %s | %s | %s |' % (table, phrasing, expected_text, observed, match))

    scoreable = len(results) - unscoreable
    lines += [
        '',
        '## Totals',
        '',
        '- Sessions run: %d' % len(results),
        '- Scoreable: %d' % scoreable,
        '- Matched expectation: %d' % (scoreable - mismatches),
        '- Did not match expectation: %d' % mismatches,
        '- Unscoreable (session failed, no verdict claimed): %d' % unscoreable,
        '',
        '## Honest caveats',
        '',
        '- One session per phrasing on one Anthropic-hosted model. This is a set of single',
        '  observations, not a rate; no percentage is computed from it anywhere in this repository.',
        '- `claude -p` exposes no temperature or seed flag, so the run is not deterministic and a',
        '  repeat can differ. A non-fire here is a non-fire in this session, not a proof that the',
        '  description can never fire on that phrasing.',
        '- `--bare` is deliberately off, because skill auto-discovery is the behaviour under test.',
        '  The operator\'s user-level `$HOME` configuration therefore still loads, so other',
        '  installed skills were present in every session.',
        '- The verdicts bind to the `description` whose hash is recorded above. If that description',
        '  changes, these observations must be re-run, not carried forward.',
        '',
    ]
    pathlib.Path(path).write_text('\n'.join(lines), encoding='utf-8')
    return mismatches, unscoreable


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--self-test', action='store_true',
                        help='run the offline discrimination checks and exit (no model call)')
    parser.add_argument('--model', default=DEFAULT_MODEL)
    parser.add_argument('--skill-src', default=str(SKILL_SRC))
    parser.add_argument('--tests', default=str(PRESSURE_TESTS))
    parser.add_argument('--out', default=str(RESULTS_PATH))
    parser.add_argument('--transcripts', default=None,
                        help='directory for per-session stream captures (default: a temp dir)')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT_S)
    parser.add_argument('--jobs', type=int, default=3,
                        help='concurrent sessions; each writes its own path, never a shared one')
    parser.add_argument('--repeats', type=int, default=1,
                        help='sessions to run per phrasing, aggregated into one k-of-n row (default 1)')
    parser.add_argument('--append', action='store_true',
                        help='append a new labelled run block to --out instead of overwriting it')
    parser.add_argument('--label', default='',
                        help='label for the appended run block (required with --append)')
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    if args.append and not args.label:
        print('ERROR: --append requires --label', file=sys.stderr)
        return 1

    md_text = pathlib.Path(args.tests).read_text(encoding='utf-8')
    rows = parse_tables(md_text)
    if not rows:
        print('ERROR: no pressure-test rows found in %s' % args.tests, file=sys.stderr)
        return 1

    skill_md = pathlib.Path(args.skill_src) / 'SKILL.md'
    live_hash = scope_hash(skill_md)
    bound_hash = recorded_scope_hash(md_text)
    try:
        scope_binding_verdict(bound_hash, live_hash, path=args.tests)
    except ValueError as exc:
        print('ERROR: %s' % exc, file=sys.stderr)
        return 1

    out_path = pathlib.Path(args.out)
    try:
        out_mode = resolve_out_mode(
            exists=out_path.exists(),
            nonempty=out_path.exists() and out_path.stat().st_size > 0,
            append=args.append,
            path=str(out_path),
        )
    except ValueError as exc:
        print('ERROR: %s' % exc, file=sys.stderr)
        return 1

    harness_version = subprocess.run(['claude', '--version'], capture_output=True,
                                     text=True).stdout.strip() or 'unknown'
    run_date = datetime.date.today().isoformat()

    transcripts = pathlib.Path(args.transcripts) if args.transcripts \
        else pathlib.Path(tempfile.mkdtemp(prefix='proof-first-trigger-out-'))
    transcripts.mkdir(parents=True, exist_ok=True)

    total_sessions = len(rows) * args.repeats
    print('Running %d sessions (%d phrasings x %d repeats, model=%s, jobs=%d)'
          % (total_sessions, len(rows), args.repeats, args.model, args.jobs))

    tasks = []
    for row_index, row in enumerate(rows):
        for rep in range(args.repeats):
            tasks.append((row_index, rep, row))

    def one(task):
        row_index, rep, (table, phrasing, _expects, _expected_text) = task
        if args.repeats == 1:
            out_file = transcripts / ('%02d-%s.jsonl' % (row_index + 1, table))
        else:
            out_file = transcripts / ('%02d-%s-r%d.jsonl' % (row_index + 1, table, rep + 1))
        return row_index, run_session(args.skill_src, phrasing, args.model, out_file, args.timeout)

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        raw_results = list(pool.map(one, tasks))

    verdicts_by_row = {i: [] for i in range(len(rows))}
    for row_index, (verdict, note) in raw_results:
        verdicts_by_row[row_index].append(verdict)
        table, phrasing, _e, _t = rows[row_index]
        print('  %-14s %-60s rep -> %s%s' % (table, phrasing[:60], verdict,
                                             ' [%s]' % note if note else ''))

    counts = [aggregate_verdicts(verdicts_by_row[i]) for i in range(len(rows))]

    if args.repeats == 1 and not args.append:
        # Legacy single-session-per-row path, preserved byte-for-byte for
        # any caller that does not opt into the new --repeats/--append shape.
        results = [(verdicts_by_row[i][0], '') for i in range(len(rows))]
        mismatches, unscoreable = write_results(args.out, args.model, run_date, rows,
                                                results, live_hash, harness_version)
        print('Wrote %s' % args.out)
        print('Transcripts: %s' % transcripts)
        print('mismatches=%d unscoreable=%d' % (mismatches, unscoreable))
        return 0

    label = args.label or ('%s, %d sessions' % (args.model, total_sessions))
    block = render_run_block(
        label=label, rows=rows, counts=counts, model=args.model,
        harness_version=harness_version, scope_hash_value=live_hash,
        repeats=args.repeats, run_date=run_date,
    )

    if out_mode == 'append':
        with open(args.out, 'a', encoding='utf-8') as fh:
            fh.write('\n---\n\n')
            fh.write(block)
            fh.write('\n')
    else:
        pathlib.Path(args.out).write_text(block + '\n', encoding='utf-8')

    of_total = sum(c[0] for r, c in zip(rows, counts) if not r[2])
    sn_total = sum(c[1] for r, c in zip(rows, counts) if not r[2])
    mh_total = sum(c[0] for r, c in zip(rows, counts) if r[2])
    sm_total = sum(c[1] for r, c in zip(rows, counts) if r[2])

    print('%s %s' % ('Appended to' if out_mode == 'append' else 'Wrote', args.out))
    print('Transcripts: %s' % transcripts)
    print('OF=%d SN=%d MH=%d SM=%d' % (of_total, sn_total, mh_total, sm_total))
    return 0


if __name__ == '__main__':
    sys.exit(main())
