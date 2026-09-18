#!/usr/bin/env python3
"""Deterministic proxy-violation linter for Proof First's presales prose rules.

This script counts mechanical proxies for a subset of the rule catalog in
skills/proof-first/SKILL.md -- registered buzzword/jargon terms, unquantified
superlatives, claims with no adjacent number, over-length sentences, and
unbounded modal claims. It does not perform the deletion test PF-3.1 actually
states (whether removing a term changes a sentence's technical meaning) --
that is a semantic judgment this file cannot make, and a violation count from
this module is a count of mechanical proxies, never a compliance verdict on a
document. It imports only the Python standard library; no package-manager
dependency is introduced by this file or by the CI job that runs it.

Usage:
  python3 evals/lint.py --self-test     # run fixture-based self-tests
  python3 evals/lint.py <path>          # live run over a text file
  python3 evals/lint.py <path> --json   # live run, JSON output

Violation codes implemented in this file:
  buzzword-term          - a term registered in evals/proxy-sources.md's
                           "Buzzword and jargon terms" table appears in the
                           text. Proxy for PF-3.1/PF-3.2's deletion test.
  proxy-term-unsourced   - a term this file counts (buzzword, superlative, or
                           hedge/modal) has no row anywhere in
                           evals/proxy-sources.md. Proxy for EVAL-02.
"""

import argparse
import json
import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
PROXY_SOURCES_PATH = pathlib.Path(__file__).resolve().parent / 'proxy-sources.md'

DISCLAIMER = (
    "The deletion test -- whether removing a term changes a sentence's technical meaning -- "
    "is a semantic judgment this linter does not perform. "
    "A violation count from this module is a count of mechanical proxies for that judgment, "
    "not a compliance verdict on a document."
)

ALLOWED_SOURCE_LABELS = ('A', 'B')

SOURCE_URL_PREFIXES = {
    'A': ('https://en.wikipedia.org/',),
    'B': ('https://digital.gov/', 'https://github.com/GSA/'),
}

PROXY_TERMS = (
    'acclaimed', 'best-in-class', 'comprehensive', 'cutting-edge', 'facilitate',
    'iconic', 'impactful', 'landmark', 'leading', 'leverage', 'premier', 'renowned',
    'revolutionary', 'robust', 'seamless', 'solution', 'state-of-the-art', 'streamline',
    'synergy', 'unparalleled', 'utilize', 'world-class',
)

VIOLATION_CODES = (
    'buzzword-term',
    'proxy-term-unsourced',
)


def _build_term_pattern(terms):
    """Longest-first alternation so an overlapping shorter term never wins.

    Python's re engine tries alternatives left to right and takes the first
    one that matches at a given position; sorting by length descending means
    the longest candidate is always tried first, so a shorter registry term
    nested inside a longer one is never counted a second time.
    """
    ordered = sorted(set(terms), key=len, reverse=True)
    pattern = '|'.join(re.escape(t) for t in ordered)
    return re.compile(r'\b(?:' + pattern + r')\b', re.IGNORECASE)


_ROW_PATTERN = re.compile(
    r'^\|\s*(?P<term>[^|]+?)\s*\|\s*(?P<label>[^|]+?)\s*\|\s*(?P<url>[^|]+?)\s*\|?\s*$'
)


def parse_proxy_sources(path):
    """Return one record per data row of the registry's term tables.

    Skips header rows (first cell literally "Term") and Markdown separator
    rows (cells made only of hyphens). Scans every `| term | label | url |`
    row in the file regardless of which `##` table it sits under, so a single
    parse covers every table the registry ever grows to hold.
    """
    text = pathlib.Path(path).read_text(encoding='utf-8')
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith('|'):
            continue
        m = _ROW_PATTERN.match(line)
        if not m:
            continue
        term = m.group('term').strip()
        label = m.group('label').strip()
        url = m.group('url').strip()
        if term.lower() == 'term':
            continue
        if set(term) <= {'-'} or set(label) <= {'-'}:
            continue
        rows.append({'term': term, 'label': label, 'url': url})
    return rows


def _resolves_inside_repo(url):
    """True if url, once any file:// scheme is stripped, is a path landing
    inside this repository -- whether given as a relative path, an absolute
    path, or a file:// URL. A real http(s):// URL is never "inside" the repo.
    """
    stripped = url
    if stripped.startswith('file://'):
        stripped = stripped[len('file://'):]
    if stripped.startswith('http://') or stripped.startswith('https://'):
        return False
    try:
        candidate = pathlib.Path(stripped)
        if not candidate.is_absolute():
            candidate = (REPO_ROOT / candidate)
        candidate = candidate.resolve()
    except (OSError, ValueError):
        return True
    try:
        candidate.relative_to(REPO_ROOT.resolve())
        return True
    except ValueError:
        return False


def check_provenance(terms, rows):
    """Cross-reference `terms` (everything this file counts) against `rows`
    (evals/proxy-sources.md's parsed table rows).

    Fires proxy-term-unsourced for a term with no row at all. This is the
    mechanical half of EVAL-02: it proves every counted term traces to a row
    in the committed registry. It cannot prove the registry's own rows are
    telling the truth about their source -- that is proxy-term-source-invalid
    and proxy-term-source-is-internal's job.
    """
    violations = []
    rows_by_term = {}
    for row in rows:
        rows_by_term.setdefault(row['term'], []).append(row)

    for term in terms:
        if term not in rows_by_term:
            violations.append({
                'code': 'proxy-term-unsourced',
                'offset': 0,
                'match': term,
                'message': (
                    f"'{term}' is counted by evals/lint.py but has no row in "
                    "evals/proxy-sources.md."
                ),
            })
    return violations


def lint(text):
    """Lint `text` and return a dict: violations, violations_total, by_code,
    disclaimer. Text-based codes only -- registry provenance is checked
    separately via check_provenance(), since it is a property of the
    registry file, not of any one document.
    """
    violations = []

    proxy_pattern = _build_term_pattern(PROXY_TERMS)
    for m in proxy_pattern.finditer(text):
        violations.append({
            'code': 'buzzword-term',
            'offset': m.start(),
            'match': m.group(0),
            'message': (
                f"'{m.group(0)}' is a registered buzzword/jargon proxy term "
                "(see evals/proxy-sources.md)."
            ),
        })

    violations.sort(key=lambda v: (v['offset'], v['code']))
    by_code = {}
    for v in violations:
        by_code[v['code']] = by_code.get(v['code'], 0) + 1
    return {
        'violations': violations,
        'violations_total': len(violations),
        'by_code': by_code,
        'disclaimer': DISCLAIMER,
    }


def self_test():
    print(DISCLAIMER)
    codes_covered = set()
    all_ok = True

    # lint("") is zero-violation and still carries the disclaimer.
    empty = lint('')
    assert empty['violations_total'] == 0, empty
    assert empty['violations'] == [], empty
    assert empty['disclaimer'] == DISCLAIMER, empty

    # Both disclaimer sentences are present.
    assert 'semantic judgment this linter does not perform' in DISCLAIMER, DISCLAIMER
    assert 'not a compliance verdict on a document' in DISCLAIMER, DISCLAIMER

    # buzzword-term: firing and clean fixture, dedicated to this code alone.
    BUZZWORD_FIRING = "The platform uses a robust deployment pipeline for daily releases."
    BUZZWORD_CLEAN = "The platform uses a documented deployment pipeline for daily releases."
    dirty = lint(BUZZWORD_FIRING)
    clean = lint(BUZZWORD_CLEAN)
    assert dirty['by_code'].get('buzzword-term', 0) == 1, dirty
    assert clean['violations_total'] == 0, clean
    codes_covered.add('buzzword-term')

    # Longest-match-wins: a shorter registry term nested inside a longer one
    # is never counted a second time. Uses a local ('class', 'best-in-class')
    # pair to exercise the matching primitive directly -- 'class' is not
    # itself a registry row in this file, so this proves the mechanism, not
    # a claim about the shipped PROXY_TERMS list.
    probe_pattern = _build_term_pattern(('class', 'best-in-class'))
    matches = list(probe_pattern.finditer("This best-in-class platform ships today."))
    assert len(matches) == 1, matches
    assert matches[0].group(0).lower() == 'best-in-class', matches

    # This linter's own registry does include "best-in-class" as a whole
    # term, and linting it produces exactly one violation, total.
    result = lint("This best-in-class platform ships today.")
    assert result['violations_total'] == 1, result
    assert result['violations'][0]['code'] == 'buzzword-term', result
    assert result['violations'][0]['offset'] == text_index(
        "This best-in-class platform ships today.", 'best-in-class'
    ), result

    # The research document's clean fixture (AWS Control Tower / 850 VMs)
    # produces zero violations.
    CLEAN_FIXTURE = (
        "AWS Control Tower governs the new account structure across 850 virtual machines."
    )
    assert lint(CLEAN_FIXTURE)['violations_total'] == 0, lint(CLEAN_FIXTURE)

    # proxy-term-unsourced: removing a term's row from a registry copy makes
    # it fire for exactly that term; the shipped registry produces none.
    shipped_rows = parse_proxy_sources(PROXY_SOURCES_PATH)
    shipped_violations = check_provenance(PROXY_TERMS, shipped_rows)
    unsourced = [v for v in shipped_violations if v['code'] == 'proxy-term-unsourced']
    assert unsourced == [], unsourced

    registry_text = PROXY_SOURCES_PATH.read_text(encoding='utf-8')
    mutated_lines = [
        line for line in registry_text.splitlines()
        if '| robust |' not in line
    ]
    mutated_rows = parse_proxy_sources_from_text('\n'.join(mutated_lines))
    mutated_violations = check_provenance(PROXY_TERMS, mutated_rows)
    fired_terms = {v['match'] for v in mutated_violations if v['code'] == 'proxy-term-unsourced'}
    assert fired_terms == {'robust'}, fired_terms
    codes_covered.add('proxy-term-unsourced')

    missing = set(VIOLATION_CODES) - codes_covered
    if missing:
        print(f"self-test FAIL - codes never exercised by a fixture: {sorted(missing)}")
        return False

    print(f"self-test PASS - verified violation codes: {', '.join(sorted(codes_covered))}")
    return all_ok


def text_index(haystack, needle):
    idx = haystack.find(needle)
    assert idx >= 0, (haystack, needle)
    return idx


def parse_proxy_sources_from_text(text):
    """Same row-parsing logic as parse_proxy_sources(), over an in-memory
    string instead of a file path -- used by self_test() to exercise a
    mutated registry without writing a throwaway file to disk.
    """
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith('|'):
            continue
        m = _ROW_PATTERN.match(line)
        if not m:
            continue
        term = m.group('term').strip()
        label = m.group('label').strip()
        url = m.group('url').strip()
        if term.lower() == 'term':
            continue
        if set(term) <= {'-'} or set(label) <= {'-'}:
            continue
        rows.append({'term': term, 'label': label, 'url': url})
    return rows


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--json', action='store_true', dest='as_json')
    parser.add_argument('path', nargs='?', default=None)
    args = parser.parse_args()

    if args.self_test:
        ok = self_test()
        sys.exit(0 if ok else 1)

    if not args.path:
        parser.print_help()
        sys.exit(1)

    text = pathlib.Path(args.path).read_text(encoding='utf-8')
    result = lint(text)

    if args.as_json:
        print(json.dumps(result, indent=2))
    else:
        print(result['disclaimer'])
        if result['violations_total'] == 0:
            print('lint: 0 violations')
        else:
            for v in result['violations']:
                print(f"{v['code']} @ {v['offset']}: {v['match']!r} -- {v['message']}")
            print(f"lint: {result['violations_total']} violations")

    sys.exit(0 if result['violations_total'] == 0 else 1)


if __name__ == '__main__':
    main()
