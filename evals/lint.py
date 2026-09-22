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

Three ceilings are declared here in full, in the same sentence class
tools/check_repo.py's own docstring already uses:

1. The deletion test is a semantic judgement this file does not perform.
   Whether removing a term changes the technical meaning of a sentence is
   PF-3.1's actual rule; this file counts occurrences of terms an external
   style guide names, which is a proxy for that rule and not the rule. A
   count from this file is not a compliance verdict on a document.
2. Provenance is proven outward, not inward. Every shipped term traces to
   one of two named external lists (evals/proxy-sources.md), and no term
   traces only to this repository. This does not prove a human never read
   skills/proof-first/references/worked-examples.md while choosing which
   external-list entries to ship, and it does not claim the shipped terms
   are absent from this repository's own prose: measured 2026-09-18, nine
   of eighteen candidate terms already appear in worked-examples.md or
   examples/before-after.md, the expected consequence of a skill that
   illustrates itself with the puffery it deletes.
3. Sentence segmentation is naive: a sentence is delimited by `.`, `?`, or
   `!` followed by whitespace or end of string. An abbreviation or a
   decimal point inside a sentence splits it early, which inflates the
   sentence count and deflates per-sentence word counts for the affected
   sentence and its neighbour. No stdlib-only splitter avoids this.

Longest-match counting rule: proxy terms are matched on a word-boundary
regex built from the term list sorted longest-first, so the longest term
starting at a given offset always wins and a shorter registry term nested
inside it is never counted a second time. A future term addition must not
break this ordering.

Ordering rule: `lint()` returns violations sorted on `(offset, code)`
ascending, where `offset` is the zero-based code-point index of the match in
the input text. Two violations at the same offset are ordered by code
string. This is contractual, not incidental.

Usage:
  python3 evals/lint.py --self-test     # run fixture-based self-tests
  python3 evals/lint.py <path>          # live run over a text file
  python3 evals/lint.py <path> --json   # live run, JSON output

Violation codes implemented in this file:
  buzzword-term          - a term registered in evals/proxy-sources.md's
                           "Buzzword and jargon terms" table appears in the
                           text. Proxy for PF-3.1/PF-3.2's deletion test.
                           Ceiling: a bare occurrence count, not the
                           deletion test itself (see ceiling 1 above).
  unquantified-superlative - a term registered in the registry's
                           "Superlative terms" table appears in a sentence
                           containing no digit character. Proxy for PF-3.1.
                           Ceiling: a superlative backed by a digit three
                           sentences later, not the same one, is not seen.
  claim-without-adjacent-number - a sentence contains one of the frozen
                           CLAIM_VERBS and neither a digit nor a bracketed
                           GAP/REVIEW marker in SKILL.md's marker grammar.
                           Proxy for PF-2.1. Ceiling: evidence named in
                           prose with no digit and no marker is invisible
                           to this check.
  sentence-over-ceiling  - a sentence's whitespace-split word count exceeds
                           SENTENCE_WORD_CEILING (25). Proxy for PF-4.1.
                           Ceiling: naive sentence segmentation (ceiling 3
                           above) means one mis-split sentence can under-
                           or over-count.
  unbounded-modal        - a term registered in the registry's "Hedge and
                           modal terms" table appears in a sentence with no
                           conditional cue from the frozen CONDITION_CUES.
                           Proxy for PF-4.3. Ceiling: a condition stated in
                           the previous sentence, not the same one, is not
                           seen.
  proxy-term-unsourced   - a term this file counts (buzzword, superlative, or
                           hedge/modal) has no row anywhere in
                           evals/proxy-sources.md. Proxy for EVAL-02.
                           Ceiling: proves provenance, not blind curation
                           (see ceiling 2 above).
  proxy-term-source-invalid - a registry row's label is not `A`/`B`, or its
                           URL matches no allow-listed prefix for that
                           label. Proxy for EVAL-02. Ceiling: an allow-list
                           over exactly two prefixes; a URL is judged on
                           string prefix only, never fetched or resolved
                           over the network.
  proxy-term-source-is-internal - a registry row's URL, after stripping any
                           `file://` scheme, resolves to a path inside this
                           repository, or is a relative path rather than an
                           absolute URL. Proxy for EVAL-02. Ceiling: catches
                           a path this environment can resolve; it does not
                           and cannot confirm a live http(s) URL actually
                           serves the content the registry claims (see
                           ceiling 2 above -- this linter never fetches or
                           resolves a URL, by design and regardless of what
                           network the environment has).
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

# Registry-sourced (evals/proxy-sources.md's "Superlative terms" table),
# deliberately disjoint from PROXY_TERMS so a sentence exercising
# unquantified-superlative does not, as a side effect, also exercise
# buzzword-term -- the two codes are tested independently.
SUPERLATIVE_TERMS = (
    'exceptional', 'extraordinary', 'outstanding', 'unbeatable', 'unrivaled',
)

# Registry-sourced (evals/proxy-sources.md's "Hedge and modal terms" table).
# PF-4.3 names these three as the catalog's own possibility modals.
HEDGE_TERMS = ('could', 'may', 'might')

# Frozen here, not registry-sourced -- these are the catalog's own PF-2.1
# claim-verb vocabulary, not an externally-sourced buzzword/jargon list.
CLAIM_VERBS = (
    'reduces', 'reduce', 'improves', 'improve', 'increases', 'increase', 'delivers',
    'deliver', 'accelerates', 'accelerate', 'cuts', 'cut', 'eliminates', 'eliminate',
    'ensures', 'ensure', 'guarantees', 'guarantee',
)

# Frozen here, not registry-sourced -- these are grammatical function words,
# not an externally-sourced buzzword/jargon list.
CONDITION_CUES = ('if', 'when', 'where', 'unless', 'provided', 'subject to', 'once')

# PF-4.1's own stated ceiling.
SENTENCE_WORD_CEILING = 25

# SKILL.md lines 33-44's frozen marker grammar: "[<rule> GAP: ...]" or
# "[<rule> REVIEW (<category>): ...]". Only the GAP/REVIEW forms are
# relevant here -- the third (customer-term-retained) form marks a kept
# term, not a missing claim.
MARKER_PATTERN = re.compile(r'\[(?:PF-\d+\.\d+|MC-\d+)\s+(?:GAP|REVIEW)\b')

# Sentence boundary: '.', '?', or '!' followed by whitespace or end of
# string. See the module docstring's segmentation-ceiling paragraph.
_SENTENCE_END = re.compile(r'[.?!](?:\s+|$)')

# Every term this file counts, across all three registry-sourced lists --
# the set check_provenance() validates against evals/proxy-sources.md.
ALL_COUNTED_TERMS = tuple(sorted(set(PROXY_TERMS) | set(SUPERLATIVE_TERMS) | set(HEDGE_TERMS)))

VIOLATION_CODES = (
    'buzzword-term',
    'unquantified-superlative',
    'claim-without-adjacent-number',
    'sentence-over-ceiling',
    'unbounded-modal',
    'proxy-term-unsourced',
    'proxy-term-source-invalid',
    'proxy-term-source-is-internal',
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


def _iter_sentences(text):
    """Yield (start, end, sentence) for each sentence in `text`, with `start`
    and `end` as zero-based code-point offsets into the original text so
    per-sentence violations can report a whole-document offset.
    """
    start = 0
    for m in _SENTENCE_END.finditer(text):
        end = m.end()
        sentence = text[start:end]
        if sentence.strip():
            yield start, end, sentence
        start = end
    if start < len(text):
        tail = text[start:]
        if tail.strip():
            yield start, len(text), tail


def check_provenance(terms, rows):
    """Cross-reference `terms` (everything this file counts) against `rows`
    (evals/proxy-sources.md's parsed table rows).

    Fires proxy-term-unsourced for a term with no row at all -- the
    mechanical half of EVAL-02, proving every counted term traces to a row
    in the committed registry. Fires proxy-term-source-invalid for a row
    whose label is not `A`/`B` or whose URL matches no allow-listed prefix
    for that label, and proxy-term-source-is-internal for a row whose URL
    resolves to a path inside this repository -- both checked independently
    for every row a term has, so a row that fails both is reported by both
    (defence in depth, not a single either/or branch). This is an allow-list,
    never a deny-list: a URL that does not match an allowed prefix is
    rejected outright, so a future contributor cannot add a fourth source by
    inventing a plausible-looking domain.
    """
    violations = []
    rows_by_term = {}
    for row in rows:
        rows_by_term.setdefault(row['term'], []).append(row)

    for term in terms:
        matches = rows_by_term.get(term)
        if not matches:
            violations.append({
                'code': 'proxy-term-unsourced',
                'offset': 0,
                'match': term,
                'message': (
                    f"'{term}' is counted by evals/lint.py but has no row in "
                    "evals/proxy-sources.md."
                ),
            })
            continue

        for row in matches:
            label = row['label']
            url = row['url']
            allowed_prefixes = SOURCE_URL_PREFIXES.get(label, ())
            if label not in ALLOWED_SOURCE_LABELS or not any(
                url.startswith(p) for p in allowed_prefixes
            ):
                violations.append({
                    'code': 'proxy-term-source-invalid',
                    'offset': 0,
                    'match': term,
                    'message': (
                        f"'{term}' cites label {label!r} / url {url!r}, which is not an "
                        "allow-listed (label, URL-prefix) pair."
                    ),
                })
            if _resolves_inside_repo(url):
                violations.append({
                    'code': 'proxy-term-source-is-internal',
                    'offset': 0,
                    'match': term,
                    'message': (
                        f"'{term}' cites {url!r}, which resolves to a path inside this "
                        "repository."
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

    superlative_pattern = _build_term_pattern(SUPERLATIVE_TERMS)
    claim_pattern = _build_term_pattern(CLAIM_VERBS)
    hedge_pattern = _build_term_pattern(HEDGE_TERMS)
    condition_pattern = _build_term_pattern(CONDITION_CUES)

    for start, end, sentence in _iter_sentences(text):
        has_digit = bool(re.search(r'\d', sentence))
        has_marker = bool(MARKER_PATTERN.search(sentence))
        has_condition = bool(condition_pattern.search(sentence))

        if not has_digit:
            for m in superlative_pattern.finditer(sentence):
                violations.append({
                    'code': 'unquantified-superlative',
                    'offset': start + m.start(),
                    'match': m.group(0),
                    'message': (
                        f"'{m.group(0)}' is an unquantified superlative (PF-3.1 proxy) -- "
                        "no digit appears in its sentence."
                    ),
                })

        if not has_digit and not has_marker:
            cm = claim_pattern.search(sentence)
            if cm:
                violations.append({
                    'code': 'claim-without-adjacent-number',
                    'offset': start + cm.start(),
                    'match': cm.group(0),
                    'message': (
                        f"'{cm.group(0)}' is a claim verb (PF-2.1 proxy) with no digit or "
                        "gap/review marker in its sentence."
                    ),
                })

        word_count = len(sentence.split())
        if word_count > SENTENCE_WORD_CEILING:
            violations.append({
                'code': 'sentence-over-ceiling',
                'offset': start,
                'match': sentence.strip()[:60],
                'message': (
                    f"sentence has {word_count} words, exceeding the "
                    f"{SENTENCE_WORD_CEILING}-word ceiling (PF-4.1 proxy)."
                ),
            })

        if not has_condition:
            for m in hedge_pattern.finditer(sentence):
                violations.append({
                    'code': 'unbounded-modal',
                    'offset': start + m.start(),
                    'match': m.group(0),
                    'message': (
                        f"'{m.group(0)}' is a hedge/modal term (PF-4.3 proxy) with no "
                        "conditional cue in its sentence."
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

    # unquantified-superlative: firing and clean fixture, dedicated to this
    # code alone -- SUPERLATIVE_TERMS is disjoint from PROXY_TERMS, so
    # neither fixture also trips buzzword-term.
    SUPERLATIVE_FIRING = "This is an exceptional migration approach for the platform team."
    SUPERLATIVE_CLEAN = "This is an exceptional migration approach for the 12-person platform team."
    dirty = lint(SUPERLATIVE_FIRING)
    clean = lint(SUPERLATIVE_CLEAN)
    assert dirty['by_code'].get('unquantified-superlative', 0) == 1, dirty
    assert clean['by_code'].get('unquantified-superlative', 0) == 0, clean
    codes_covered.add('unquantified-superlative')

    # claim-without-adjacent-number: firing, digit-clean, and marker-clean.
    CLAIM_FIRING = "This upgrade reduces operational overhead for the support team."
    CLAIM_CLEAN_DIGIT = (
        "This upgrade reduces operational overhead for the support team by 12 percent."
    )
    CLAIM_CLEAN_MARKER = (
        "This upgrade reduces operational overhead for the support team "
        "[PF-2.4 GAP: baseline not yet measured]."
    )
    dirty = lint(CLAIM_FIRING)
    clean_digit = lint(CLAIM_CLEAN_DIGIT)
    clean_marker = lint(CLAIM_CLEAN_MARKER)
    assert dirty['by_code'].get('claim-without-adjacent-number', 0) == 1, dirty
    assert clean_digit['by_code'].get('claim-without-adjacent-number', 0) == 0, clean_digit
    assert clean_marker['by_code'].get('claim-without-adjacent-number', 0) == 0, clean_marker
    codes_covered.add('claim-without-adjacent-number')

    # sentence-over-ceiling: boundary asserted at both 25 (silent) and 26
    # (fires) words, word counts stated explicitly so a later edit cannot
    # silently shift the boundary.
    SENTENCE_25_WORDS = ' '.join(['token'] * 25) + '.'  # exactly 25 words -- must stay silent
    SENTENCE_26_WORDS = ' '.join(['token'] * 26) + '.'  # exactly 26 words -- must fire
    at_25 = lint(SENTENCE_25_WORDS)
    at_26 = lint(SENTENCE_26_WORDS)
    assert at_25['by_code'].get('sentence-over-ceiling', 0) == 0, at_25
    assert at_26['by_code'].get('sentence-over-ceiling', 0) == 1, at_26
    codes_covered.add('sentence-over-ceiling')

    # unbounded-modal: firing and clean (conditional-cue) fixture.
    MODAL_FIRING = "This approach might simplify onboarding for new hires."
    MODAL_CLEAN = "This approach might simplify onboarding for new hires if the pilot succeeds."
    dirty = lint(MODAL_FIRING)
    clean = lint(MODAL_CLEAN)
    assert dirty['by_code'].get('unbounded-modal', 0) == 1, dirty
    assert clean['by_code'].get('unbounded-modal', 0) == 0, clean
    codes_covered.add('unbounded-modal')

    # End-to-end: the research document's own slop/clean fixture pair.
    SLOP_FIXTURE = (
        "This comprehensive, best-in-class, world-class solution delivers a robust, "
        "enterprise-grade landing zone."
    )
    slop_result = lint(SLOP_FIXTURE)
    assert slop_result['violations_total'] >= 4, slop_result
    assert len(slop_result['by_code']) >= 2, slop_result
    assert lint(CLEAN_FIXTURE)['violations_total'] == 0, lint(CLEAN_FIXTURE)

    # proxy-term-unsourced: removing a term's row from a registry copy makes
    # it fire for exactly that term; the shipped registry produces none, for
    # every term across all three registry-sourced lists.
    shipped_rows = parse_proxy_sources(PROXY_SOURCES_PATH)
    shipped_violations = check_provenance(ALL_COUNTED_TERMS, shipped_rows)
    unsourced = [v for v in shipped_violations if v['code'] == 'proxy-term-unsourced']
    assert unsourced == [], unsourced

    registry_text = PROXY_SOURCES_PATH.read_text(encoding='utf-8')
    mutated_lines = [
        line for line in registry_text.splitlines()
        if '| robust |' not in line
    ]
    mutated_rows = parse_proxy_sources_from_text('\n'.join(mutated_lines))
    mutated_violations = check_provenance(ALL_COUNTED_TERMS, mutated_rows)
    fired_terms = {v['match'] for v in mutated_violations if v['code'] == 'proxy-term-unsourced'}
    assert fired_terms == {'robust'}, fired_terms
    codes_covered.add('proxy-term-unsourced')

    # proxy-term-source-invalid: a mutated row citing label 'C' fires; the
    # shipped registry produces none.
    shipped_invalid = [v for v in shipped_violations if v['code'] == 'proxy-term-source-invalid']
    assert shipped_invalid == [], shipped_invalid
    label_c_lines = [
        line.replace('| robust | B |', '| robust | C |', 1) if '| robust | B |' in line else line
        for line in registry_text.splitlines()
    ]
    assert label_c_lines != registry_text.splitlines(), "fixture did not mutate the robust row"
    label_c_rows = parse_proxy_sources_from_text('\n'.join(label_c_lines))
    label_c_violations = check_provenance(ALL_COUNTED_TERMS, label_c_rows)
    invalid_terms = {
        v['match'] for v in label_c_violations if v['code'] == 'proxy-term-source-invalid'
    }
    assert 'robust' in invalid_terms, invalid_terms
    codes_covered.add('proxy-term-source-invalid')

    # proxy-term-source-is-internal: a mutated row citing this repository's
    # own worked-examples.md as its URL fires -- asserted by its own
    # dedicated fixture, not inferred from the label-invalid case above,
    # even though this same fixture also fails the prefix check (defence in
    # depth, per Task 3's own instruction). The shipped registry produces
    # none.
    shipped_internal = [
        v for v in shipped_violations if v['code'] == 'proxy-term-source-is-internal'
    ]
    assert shipped_internal == [], shipped_internal
    internal_url = 'skills/proof-first/references/worked-examples.md'
    internal_lines = [
        line.replace(
            '| robust | B | https://digital.gov/guides/plain-language/principles/avoid-jargon |',
            f'| robust | B | {internal_url} |',
            1,
        )
        for line in registry_text.splitlines()
    ]
    assert internal_lines != registry_text.splitlines(), "fixture did not mutate the robust row"
    internal_rows = parse_proxy_sources_from_text('\n'.join(internal_lines))
    internal_violations = check_provenance(ALL_COUNTED_TERMS, internal_rows)
    internal_terms = {
        v['match'] for v in internal_violations if v['code'] == 'proxy-term-source-is-internal'
    }
    assert 'robust' in internal_terms, internal_terms
    codes_covered.add('proxy-term-source-is-internal')

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
