#!/usr/bin/env python3
"""Reproducibility instrument for MOD-04's conformance rate.

This script measures exactly one thing: whether a live write-mode session
names the artifact-family line before its first rule marker (a `PF-#.#` or
`MC-#` citation). It is a regex scorer over transcript text, not a semantic
judge — it cannot tell a family named in a heading from one named in a
sentence, and it does not read the drafted prose for quality. Phase 5's
evaluation harness (EVAL-01..12) owns prose-quality linting, the
skill-on/skill-off benchmark, and the blind pairwise judge; this runner is
deliberately narrower and does not overlap with it.

It imports only the Python standard library: argparse, datetime, json,
pathlib, re, shutil, subprocess, sys, tempfile. No package-manager
dependency is introduced by this file.

Usage:
  python3 evals/conformance/run_conformance.py --self-test
      Offline proof that the scorer discriminates the three committed
      transcript fixtures correctly. Makes no subprocess call and no
      network call; runs on a machine with no `claude` binary.

  python3 evals/conformance/run_conformance.py [--skill-src PATH]
      [--fixtures A,B,C] [--models MODEL,...] [--repeats N]
      [--transcript-dir PATH] [--out PATH] [--timeout SECONDS]
      Live mode: drives one or more real `claude -p` write-mode sessions
      against the given skill source and fixtures, scores each resulting
      transcript, and appends a run block to the results file.
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

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]

# Frozen interface: byte-identical to tools/check_repo.py's
# ARTIFACT_FAMILY_SECTIONS. A reworded copy here silently stops matching the
# same four strings that checker enforces are present in artifact-patterns.md.
FAMILY_PATTERNS = (
    re.compile(r'RFP and RFI response', re.IGNORECASE),
    re.compile(r'Solution proposal', re.IGNORECASE),
    re.compile(r'Executive summary', re.IGNORECASE),
    re.compile(r'Demo and discovery material', re.IGNORECASE),
    # SKILL.md's write-mode phrasings for the same four families.
    re.compile(r'RFP answer', re.IGNORECASE),
    re.compile(r'proposal section', re.IGNORECASE),
    re.compile(r'executive summary', re.IGNORECASE),
    re.compile(r'demo or discovery material', re.IGNORECASE),
    # The no-family value is a value of the family line, not an absence of
    # one (see 03-06-PLAN.md's <assumption_delta_decision>).
    re.compile(r'No family fits', re.IGNORECASE),
)

# The two allocated rule namespaces.
MARKER_PATTERN = re.compile(r'\bPF-\d+\.\d+\b|\bMC-\d+\b')

# Byte-identical to the prompt 03-05-SUMMARY.md's Live Verification section
# records, so this run and the prior one measure the same thing.
PROMPT_TEMPLATE = 'Using proof-first, revise this draft into stronger presales prose: docs/{fixture}'

DISALLOWED_TOOLS = ['Write', 'Edit', 'Bash', 'NotebookEdit']

VERDICTS = ('conformant', 'no-family', 'rule-before-family', 'unscoreable')

TRANSCRIPTS_DIR = pathlib.Path(__file__).resolve().parent / 'transcripts'
FIXTURES_DIR = pathlib.Path(__file__).resolve().parent / 'fixtures'


class SessionFailedError(RuntimeError):
    """Raised by run_session() when `claude -p` exits non-zero.

    Carries the exit code and stderr so the caller can record a diagnosable
    unscoreable reason instead of silently scoring stdout (which, on a
    quota/auth/other non-timeout failure, is typically a short error string
    rather than a real transcript) as if it were a normal session. Before
    this class existed, run_session() returned that error text as its
    "transcript" and the scorer legitimately found no family pattern and no
    rule marker in it, producing a false `no-family` verdict indistinguishable
    from a genuine session that omitted the family line -- see 03-08-PLAN.md's
    2026-09-15T03:11:24 run block, where all ten claude-opus-5 sessions share
    this exact signature after a usage-limit exhaustion mid-run.
    """

    def __init__(self, returncode, stderr):
        self.returncode = returncode
        self.stderr = stderr or ''
        super().__init__(f'claude -p exited {returncode}')


def score_transcript(text):
    """Return (verdict, evidence) for a live write-mode transcript's text.

    Verdicts:
      unscoreable         - text is empty (or whitespace-only).
      no-family           - no FAMILY_PATTERNS match found anywhere.
      rule-before-family  - the lowest-offset MARKER_PATTERN match starts
                             strictly before the lowest-offset family match.
      conformant          - a family match exists and no marker precedes it
                             (including the case where no marker appears at
                             all).
    """
    stripped = text.strip()
    if not stripped:
        return 'unscoreable', 'empty transcript'

    family_match = None
    family_at = None
    for pattern in FAMILY_PATTERNS:
        m = pattern.search(text)
        if m and (family_at is None or m.start() < family_at):
            family_at = m.start()
            family_match = m.group(0)

    marker_match = None
    marker_at = None
    m = MARKER_PATTERN.search(text)
    if m:
        marker_at = m.start()
        marker_match = m.group(0)

    if family_at is None:
        return 'no-family', f'no family match found (marker_at={marker_at}, marker={marker_match!r})'

    if marker_at is not None and marker_at < family_at:
        evidence = (
            f'marker {marker_match!r} at offset {marker_at} precedes '
            f'family {family_match!r} at offset {family_at}'
        )
        return 'rule-before-family', evidence

    evidence = f'family {family_match!r} at offset {family_at}, marker_at={marker_at}'
    return 'conformant', evidence


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

        docs_dir = tmp_dir / 'docs'
        docs_dir.mkdir(parents=True, exist_ok=True)
        fixture_dst = docs_dir / fixture_path.name
        shutil.copyfile(fixture_path, fixture_dst)

        prompt = PROMPT_TEMPLATE.format(fixture=fixture_path.name)

        argv = ['claude', '-p', prompt, '--model', model, '--disallowedTools'] + DISALLOWED_TOOLS

        result = subprocess.run(
            argv,
            cwd=str(tmp_dir),
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        stdout = result.stdout or ''
        stderr = result.stderr or ''

        out_path = pathlib.Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if result.returncode != 0:
            # Write both streams for audit -- a failed invocation's stdout is
            # not a transcript and must never reach score_transcript().
            out_path.write_text(
                f'[claude -p exited {result.returncode}]\n'
                f'--- stdout ---\n{stdout}\n--- stderr ---\n{stderr}\n'
            )
            raise SessionFailedError(result.returncode, stderr)

        out_path.write_text(stdout)
        return stdout
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def self_test():
    """Offline proof the scorer discriminates known verdicts. No subprocess call.

    Asserts the five inline cases from this plan's <behavior> block first --
    these need no fixture file and always run, proving all four verdict
    strings are discriminated even before evals/conformance/transcripts/ has
    any committed fixture. It then cross-checks the three committed
    transcript fixtures (conformant-family-first.txt,
    nonconformant-no-family.txt, nonconformant-rule-before-family.txt) if
    present: an absent fixture is not a failure (fixtures are authored in a
    later task), but a present one that no longer exhibits its named
    property is. A sixth case (03-08-PLAN.md) monkeypatches subprocess.run
    for one run_session() call to prove a nonzero-exit `claude -p`
    invocation raises SessionFailedError and is classified `unscoreable` by
    the caller, never scored as `no-family` against its error-text stdout --
    still no real subprocess call, no network call.
    """
    all_ok = True
    verdicts_discriminated = set()

    # Case 1: family named on the first line, PF-2.4 cited two paragraphs
    # later -> conformant.
    case1 = (
        'Artifact family: RFP and RFI response\n\n'
        'We can meet your migration timeline with confidence.\n\n'
        "This approach follows PF-2.4's proof-point discipline throughout.\n"
    )
    verdict, evidence = score_transcript(case1)
    if verdict != 'conformant':
        print(f'FAIL: behavior case 1 (family-first) expected conformant actual {verdict} ({evidence})')
        all_ok = False
    else:
        verdicts_discriminated.add(verdict)

    # Case 2: cites PF-2.17 in the first paragraph, never names any family
    # -> no-family.
    case2 = (
        'Findings: PF-2.17 flags an unproven capability claim in the second paragraph.\n'
        'No family name appears anywhere in this response.\n'
    )
    verdict, evidence = score_transcript(case2)
    if verdict != 'no-family':
        print(f'FAIL: behavior case 2 (no-family) expected no-family actual {verdict} ({evidence})')
        all_ok = False
    else:
        verdicts_discriminated.add(verdict)

    # Case 3: cites PF-1.17 in the first paragraph, names Executive summary
    # only in the fourth -> rule-before-family.
    case3 = (
        'PF-1.17 requires a quantified proof point here.\n\n'
        'Second paragraph continues the narrative.\n\n'
        'Third paragraph still without a family name.\n\n'
        'This response assumes the Executive summary family.\n'
    )
    verdict, evidence = score_transcript(case3)
    if verdict != 'rule-before-family':
        print(f'FAIL: behavior case 3 (rule-before-family) expected rule-before-family actual {verdict} ({evidence})')
        all_ok = False
    else:
        verdicts_discriminated.add(verdict)

    # Case 4: the only family statement is the no-family value, and no
    # marker precedes it -> conformant (the no-family value is a value of
    # the family line, not an absence of one).
    case4 = (
        'The document under review spans two families.\n'
        '**No family fits:** the draft mixes discovery notes with a proposal narrative.\n'
    )
    verdict, evidence = score_transcript(case4)
    if verdict != 'conformant':
        print(f'FAIL: behavior case 4 (no-family-fits value) expected conformant actual {verdict} ({evidence})')
        all_ok = False
    else:
        verdicts_discriminated.add(verdict)

    # Case 5: empty string -> unscoreable.
    verdict, evidence = score_transcript('')
    if verdict != 'unscoreable':
        print(f'FAIL: behavior case 5 (empty) expected unscoreable actual {verdict} ({evidence})')
        all_ok = False
    else:
        verdicts_discriminated.add(verdict)

    # Fixture-file cross-check: validate the three committed transcript
    # fixtures if they exist. Not present yet is not a failure.
    fixture_expectations = {
        'conformant-family-first.txt': 'conformant',
        'nonconformant-no-family.txt': 'no-family',
        'nonconformant-rule-before-family.txt': 'rule-before-family',
    }
    for filename, expected in fixture_expectations.items():
        path = TRANSCRIPTS_DIR / filename
        if not path.exists():
            continue
        text = path.read_text()
        verdict, evidence = score_transcript(text)
        if verdict != expected:
            print(f'FAIL: {filename} expected {expected} actual {verdict} ({evidence})')
            all_ok = False
        else:
            verdicts_discriminated.add(verdict)

    # Case 6: a nonzero-exit `claude -p` invocation must raise
    # SessionFailedError and never let its stdout reach score_transcript() --
    # the exact defect that produced the invalidated 2026-09-15T03:11:24 run
    # block (every claude-opus-5 session scored `no-family` instead of
    # `unscoreable` after a mid-run usage-limit exhaustion). subprocess.run is
    # monkeypatched for the duration of this one call, so this stays offline:
    # no real `claude` invocation and no network call.
    real_subprocess_run = subprocess.run

    def _fake_failed_run(argv, **kwargs):
        return subprocess.CompletedProcess(
            argv, returncode=1,
            stdout='Error: usage limit reached, resets 2:20pm',
            stderr='usage limit reached, resets 2:20pm',
        )

    fake_fixture = None
    fake_out_dir = None
    subprocess.run = _fake_failed_run
    try:
        fake_fixture = pathlib.Path(tempfile.mkstemp(suffix='.md')[1])
        fake_fixture.write_text('placeholder fixture text for self-test only')
        fake_out_dir = pathlib.Path(tempfile.mkdtemp(prefix='proof-first-conformance-selftest-'))
        fake_out_path = fake_out_dir / 'fake-session.txt'

        raised = None
        try:
            run_session(
                skill_src=REPO_ROOT / 'skills' / 'proof-first',
                fixture_path=fake_fixture,
                model='claude-sonnet-5',
                out_path=fake_out_path,
                timeout_s=5,
            )
        except SessionFailedError as exc:
            raised = exc

        if raised is None:
            print('FAIL: behavior case 6 (nonzero-exit invocation) expected SessionFailedError, none raised')
            all_ok = False
        elif raised.returncode != 1 or 'usage limit' not in raised.stderr:
            print(f'FAIL: behavior case 6 (nonzero-exit invocation) SessionFailedError fields wrong: returncode={raised.returncode!r} stderr={raised.stderr!r}')
            all_ok = False
        else:
            # Prove *why* this matters: had the buggy stdout-only path scored
            # this error text directly, it would have produced the false
            # `no-family` verdict this fix eliminates.
            would_be_verdict, _ = score_transcript(_fake_failed_run([]).stdout)
            if would_be_verdict != 'no-family':
                print(f'FAIL: behavior case 6 fixture assumption wrong: expected the pre-fix bug to produce no-family, got {would_be_verdict}')
                all_ok = False
            else:
                verdicts_discriminated.add('unscoreable')
    finally:
        subprocess.run = real_subprocess_run
        if fake_fixture is not None:
            fake_fixture.unlink(missing_ok=True)
        if fake_out_dir is not None:
            shutil.rmtree(fake_out_dir, ignore_errors=True)

    if not all_ok:
        return False

    print(
        'self-test PASS - verdicts discriminated: '
        + ', '.join(sorted(verdicts_discriminated))
    )
    return True


def _git_blob_sha(relative_path):
    try:
        result = subprocess.run(
            ['git', 'rev-parse', f'HEAD:{relative_path}'],
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


def _default_fixtures():
    if not FIXTURES_DIR.exists():
        return []
    return sorted(p.stem for p in FIXTURES_DIR.glob('*.md'))


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--self-test', action='store_true',
                         help='Offline scorer proof; makes no subprocess or network call.')
    parser.add_argument('--skill-src', default='skills/proof-first',
                         help='Path to the skill directory to copy into each session (default: skills/proof-first).')
    parser.add_argument('--fixtures', default=None,
                         help='Comma-separated fixture stems (default: all files in fixtures/).')
    parser.add_argument('--models', default='claude-sonnet-5',
                         help='Comma-separated model ids (default: claude-sonnet-5).')
    parser.add_argument('--repeats', type=int, default=1,
                         help='Number of repeats per model x fixture pair (default: 1).')
    parser.add_argument('--transcript-dir', default=None,
                         help='Directory for raw transcripts (default: a fresh temp dir -- '
                              'raw transcripts are never written into the repository).')
    parser.add_argument('--out', default=str(pathlib.Path(__file__).resolve().parent / 'RESULTS-mod04.md'),
                         help='Results file to append run blocks to.')
    parser.add_argument('--timeout', type=int, default=600,
                         help='Per-session timeout in seconds (default: 600).')
    args = parser.parse_args()

    if args.self_test:
        ok = self_test()
        sys.exit(0 if ok else 1)

    skill_src = (REPO_ROOT / args.skill_src) if not pathlib.Path(args.skill_src).is_absolute() else pathlib.Path(args.skill_src)

    if args.fixtures:
        fixture_stems = [f.strip() for f in args.fixtures.split(',') if f.strip()]
    else:
        fixture_stems = _default_fixtures()

    models = [m.strip() for m in args.models.split(',') if m.strip()]

    if args.transcript_dir:
        transcript_dir = pathlib.Path(args.transcript_dir)
    else:
        transcript_dir = pathlib.Path(tempfile.mkdtemp(prefix='proof-first-conformance-transcripts-'))
    transcript_dir.mkdir(parents=True, exist_ok=True)

    skill_sha = _git_blob_sha('skills/proof-first/SKILL.md')

    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append(f'\n## Run recorded {datetime.datetime.now(datetime.timezone.utc).isoformat()}Z\n')
    lines.append(f'Measured SKILL.md blob SHA: `{skill_sha}`\n')

    scoreable_count = 0
    conformant_count = 0
    unscoreable_sessions = []

    run_index = 0
    for model in models:
        for fixture_stem in fixture_stems:
            fixture_path = FIXTURES_DIR / f'{fixture_stem}.md'
            for repeat in range(args.repeats):
                run_index += 1
                date_str = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
                out_name = f'{model}__{fixture_stem}__r{repeat}.txt'
                session_out_path = transcript_dir / out_name

                try:
                    transcript = run_session(
                        skill_src=skill_src,
                        fixture_path=fixture_path,
                        model=model,
                        out_path=session_out_path,
                        timeout_s=args.timeout,
                    )
                    session_returncode_ok = True
                except subprocess.TimeoutExpired:
                    transcript = ''
                    session_returncode_ok = False
                    reason = 'timeout'
                except SessionFailedError as exc:
                    transcript = ''
                    session_returncode_ok = False
                    stderr_excerpt = exc.stderr.strip()
                    if len(stderr_excerpt) > 300:
                        stderr_excerpt = stderr_excerpt[:300] + '...'
                    reason = (
                        f'nonzero exit {exc.returncode}: {stderr_excerpt!r}'
                        if stderr_excerpt
                        else f'nonzero exit {exc.returncode} (empty stderr)'
                    )
                except (subprocess.SubprocessError, OSError) as exc:
                    transcript = ''
                    session_returncode_ok = False
                    reason = f'subprocess error: {exc}'

                if not session_returncode_ok:
                    unscoreable_sessions.append((model, fixture_stem, repeat, reason))
                    lines.append(
                        f'- {date_str} | model={model} | fixture={fixture_stem} | repeat={repeat} '
                        f'| verdict=unscoreable | reason={reason}\n'
                    )
                    continue

                verdict, evidence = score_transcript(transcript)

                if verdict == 'unscoreable':
                    unscoreable_sessions.append((model, fixture_stem, repeat, 'empty transcript'))
                else:
                    scoreable_count += 1
                    if verdict == 'conformant':
                        conformant_count += 1

                lines.append(
                    f'- {date_str} | model={model} | fixture={fixture_stem} | repeat={repeat} '
                    f'| verdict={verdict} | evidence={evidence}\n'
                )

    lines.append(f'\nconformant {conformant_count} of {scoreable_count} scoreable sessions\n')
    lines.append(f'unscoreable {len(unscoreable_sessions)} sessions\n')
    for model, fixture_stem, repeat, reason in unscoreable_sessions:
        lines.append(f'  - excluded: model={model} fixture={fixture_stem} repeat={repeat} reason={reason}\n')

    with open(out_path, 'a') as f:
        f.writelines(lines)

    print(f'conformant {conformant_count} of {scoreable_count} scoreable sessions')
    print(f'unscoreable {len(unscoreable_sessions)} sessions')
    sys.exit(0)


if __name__ == '__main__':
    main()
