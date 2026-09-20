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
job (`evals/benchmark/`), not this file's.

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
    """Pull the sha256 the Scope section binds the rows to. None if absent."""
    match = re.search(r'\b([0-9a-f]{64})\b', md_text)
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

    for problem in failures:
        print('FAIL: %s' % problem)
    if failures:
        print('self-test FAIL: %d problem(s)' % len(failures))
        return 1
    print('self-test PASS: 3 detector cases, 2 table rows, 2 scope-hash cases')
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
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    md_text = pathlib.Path(args.tests).read_text(encoding='utf-8')
    rows = parse_tables(md_text)
    if not rows:
        print('ERROR: no pressure-test rows found in %s' % args.tests, file=sys.stderr)
        return 1

    skill_md = pathlib.Path(args.skill_src) / 'SKILL.md'
    live_hash = scope_hash(skill_md)
    bound_hash = recorded_scope_hash(md_text)
    if bound_hash and bound_hash != live_hash:
        print('ERROR: %s binds its rows to description sha256 %s but the live SKILL.md '
              'hashes to %s. The rows must be re-authored against the new description, '
              'not filled in.' % (args.tests, bound_hash, live_hash), file=sys.stderr)
        return 1

    harness_version = subprocess.run(['claude', '--version'], capture_output=True,
                                     text=True).stdout.strip() or 'unknown'
    run_date = datetime.date.today().isoformat()

    transcripts = pathlib.Path(args.transcripts) if args.transcripts \
        else pathlib.Path(tempfile.mkdtemp(prefix='proof-first-trigger-out-'))
    transcripts.mkdir(parents=True, exist_ok=True)

    print('Running %d sessions (model=%s, jobs=%d)' % (len(rows), args.model, args.jobs))

    def one(index_row):
        index, (table, phrasing, _expects, _expected_text) = index_row
        out_path = transcripts / ('%02d-%s.jsonl' % (index + 1, table))
        return run_session(args.skill_src, phrasing, args.model, out_path, args.timeout)

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(one, enumerate(rows)))

    for (table, phrasing, _e, _t), (verdict, note) in zip(rows, results):
        print('  %-14s %-72s -> %s%s' % (table, phrasing[:72], verdict,
                                         ' [%s]' % note if note else ''))

    mismatches, unscoreable = write_results(args.out, args.model, run_date, rows,
                                            results, live_hash, harness_version)
    print('Wrote %s' % args.out)
    print('Transcripts: %s' % transcripts)
    print('mismatches=%d unscoreable=%d' % (mismatches, unscoreable))
    return 0


if __name__ == '__main__':
    sys.exit(main())
