#!/usr/bin/env python3
"""Structural and textual consistency checker for this repository's registries.

This script is a structural and textual consistency check over NUMBERING.md,
examples/deal-brief.md, and NOTICES.md. It does not read framework source
material and it cannot judge whether a paraphrase reproduces proprietary
text — that judgement is Phase 6's legal review gate (LEG-04). It imports
only the Python standard library; no package-manager dependency is
introduced by this file or by the CI job that runs it.

Usage:
  python3 tools/check_repo.py                # live run against this repo
  python3 tools/check_repo.py --self-test     # run fixture-based self-tests
  python3 tools/check_repo.py --mutation-test # for each violation code, inject
                                               # one named defect into a copy of
                                               # this repository's real documents
                                               # and assert that code fires

Output ordering: the live run sorts violations on (code, subject) with
Python's stable sort over sorted() file iteration, so violations that
compare equal on that key keep their original insertion order.

Violation codes implemented in this file:
  dup-id            - an ID appears in more than one row of the Allocated
                      IDs table.
  range-id          - a PF ID sits outside its section's reserved range, or
                      an MC ID belongs to no declared MC dimension block
                      (checked per block, not against one aggregate range
                      spanning all blocks).
  revived-id        - an ID appears in both the Allocated IDs table and
                      the Deprecated IDs table.
  undefined-id      - a PF-#.# or MC-# token is cited in skills/,
                      examples/, or README.md but is absent from the
                      Allocated IDs table.
  dup-figure-key    - two rows of examples/deal-brief.md's Canonical
                      figures table share a key.
  figure-order      - the Canonical figures table's rows are not in
                      ascending key order. Ordering rule: keys are
                      compared with Python's default string ordering
                      over code points (plain `sorted()`), so two keys
                      differing only by case or by separator character
                      have a specified, reproducible position. Reports
                      the first key of the table that is not in
                      ascending order.
  unlisted-figure   - a currency amount, a percentage, or an ISO date in
                      examples/**/*.md or skills/**/*.md has no matching
                      Canonical figures row. Scan roots are examples/ and
                      skills/; evals/ is deliberately excluded because
                      Phase 5's benchmark data is not bound by the
                      Canonical figures interface. Declared ceiling (bare
                      count): this check catches currency, percentages,
                      and ISO dates only.
                      It does not catch bare counts, so a bare count
                      that drifts between examples is not detected by
                      this tool. Declared ceiling (value collision):
                      matching is by formatted value string with no binding to a canonical key,
                      so two Canonical figures rows may share one
                      formatted value, and a new fact whose formatted
                      value coincides with an unrelated canonical row's
                      value is accepted even though no row actually
                      backs that new fact. This is a limitation of this
                      tool, not a property of the data.
  pointer-missing   - a path listed in NOTICES.md under "Files required
                      to carry it" exists on disk and does not contain
                      the attribution pointer string. Declared ceiling:
                      each line of the carrier is UTF-8 decoded and
                      stripped, then compared to the canonical string
                      with Python string equality - code-point
                      equality, with no Unicode normalisation and no
                      case folding, so a visually identical line built
                      from different code points is reported as
                      missing.
  pointer-duplicated - such a path contains the attribution pointer
                      string more than once.
  pointer-unparseable - either NOTICES.md's "Attribution pointer"
                      section yields no usable pointer definition (no
                      fenced block, or an empty one), or a required
                      carrier entry is not a repository-relative path.
  license-missing   - the LICENSE file is absent from the repository
                      root, is empty, or does not begin with the string
                      "MIT License". Declared ceiling: only the first line
                      is inspected; the license body is never compared
                      against the full MIT text, so a file carrying
                      "MIT License" as its first line over a different
                      license body is accepted.
  framework-statement-missing - NOTICES.md is absent, or its
                      "Framework statements" section is missing one of the
                      three required framework subsections (Command of the
                      Message, MEDDIC/MEDDICC, or Challenger), or one of
                      those subsections is present but missing its
                      non-affiliation or trademark-rights language. The
                      check fires per-missing-framework, naming which one.
                      When NOTICES.md is absent, all three frameworks are
                      reported as missing.
"""
import argparse
import re
import shutil
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

PF_ID_RE = re.compile(r'^PF-(\d+)\.(\d+)$')
MC_ID_RE = re.compile(r'^MC-(\d+)$')
FENCE_RE = re.compile(r'```.*?```', re.S)

POINTER_SECTION = 'Attribution pointer'
CARRIERS_MARKER = 'Files required to carry it'


def strip_fences(text):
    return FENCE_RE.sub('', text)


def split_sections(text):
    """Split a Markdown document into {heading: body} by '## ' headings."""
    sections = {}
    current = None
    buf = []
    for line in text.splitlines():
        m = re.match(r'^## (.+?)\s*$', line)
        if m:
            if current is not None:
                sections[current] = '\n'.join(buf)
            current = m.group(1).strip()
            buf = []
        else:
            if current is not None:
                buf.append(line)
    if current is not None:
        sections[current] = '\n'.join(buf)
    return sections


def table_rows(section_text):
    """Return data rows (list of stripped cells) from the first Markdown
    table found in section_text, skipping the header and separator rows."""
    rows = []
    lines = [l for l in section_text.splitlines() if l.strip().startswith('|')]
    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if i == 0:
            continue  # header row
        if all(re.fullmatch(r':?-{1,}:?', c) for c in cells):
            continue  # separator row
        rows.append(cells)
    return rows


# ---------------------------------------------------------------------------
# NUMBERING.md
# ---------------------------------------------------------------------------

def parse_numbering(path):
    text = path.read_text(encoding='utf-8')
    sections = split_sections(text)

    pf_ranges = {}
    for row in table_rows(sections.get('PF reserved ranges', '')):
        section = row[0].strip()
        nums = re.findall(r'PF-\d+\.(\d+)', row[1])
        if len(nums) >= 2:
            pf_ranges[section] = (int(nums[0]), int(nums[-1]))

    mc_ranges = {}
    for row in table_rows(sections.get('MC reserved blocks', '')):
        dimension = row[0].strip()
        nums = [int(n) for n in re.findall(r'MC-(\d+)', row[1])]
        if len(nums) >= 2:
            mc_ranges[dimension] = (min(nums), max(nums))

    allocated = []
    for row in table_rows(sections.get('Allocated IDs', '')):
        if not row or not row[0]:
            continue
        allocated.append({
            'id': row[0].strip(),
            'title': row[1].strip() if len(row) > 1 else '',
            'defined_in': row[2].strip() if len(row) > 2 else '',
            'added_in': row[3].strip() if len(row) > 3 else '',
        })

    deprecated_ids = set()
    for row in table_rows(sections.get('Deprecated IDs', '')):
        if row and row[0]:
            deprecated_ids.add(row[0].strip())

    return {
        'pf_ranges': pf_ranges,
        'mc_ranges': mc_ranges,
        'allocated': allocated,
        'deprecated': deprecated_ids,
    }


# ---------------------------------------------------------------------------
# ID-integrity checks (D-05)
# ---------------------------------------------------------------------------

def check_dup_id(allocated):
    seen = {}
    for row in allocated:
        seen.setdefault(row['id'], []).append(row)
    violations = []
    for id_, rows in seen.items():
        if len(rows) > 1:
            violations.append((id_, f"dup-id {id_} appears in {len(rows)} rows of the Allocated IDs table"))
    return violations


def check_range_id(allocated, pf_ranges, mc_ranges):
    violations = []
    for row in allocated:
        id_ = row['id']
        m = PF_ID_RE.match(id_)
        if m:
            section = f"PF-{m.group(1)}"
            n = int(m.group(2))
            rng = pf_ranges.get(section)
            if rng is None or not (rng[0] <= n <= rng[1]):
                violations.append((id_, f"range-id {id_} sits outside section {section}'s reserved range"))
            continue
        m = MC_ID_RE.match(id_)
        if m:
            n = int(m.group(1))
            if not any(rng[0] <= n <= rng[1] for rng in mc_ranges.values()):
                violations.append((id_, f"range-id {id_} belongs to no declared MC dimension block"))
    return violations


def check_revived_id(allocated, deprecated_ids):
    violations = []
    for row in allocated:
        if row['id'] in deprecated_ids:
            violations.append((row['id'], f"revived-id {row['id']} appears in both the Allocated IDs and Deprecated IDs tables"))
    return violations


def check_undefined_id(allocated, repo_root):
    allocated_ids = {row['id'] for row in allocated}
    roots = [repo_root / 'skills', repo_root / 'examples', repo_root / 'README.md']
    files = []
    for root in roots:
        if not root.exists():
            continue
        if root.is_file():
            files.append(root)
        else:
            files.extend(sorted(root.rglob('*.md')))
    violations = []
    seen = set()
    for f in files:
        if f.name == 'NUMBERING.md':
            continue
        text = strip_fences(f.read_text(encoding='utf-8'))
        tokens = set(re.findall(r'PF-\d+\.\d+', text)) | set(re.findall(r'MC-\d+', text))
        for tok in sorted(tokens):
            key = (tok, str(f))
            if tok not in allocated_ids and key not in seen:
                seen.add(key)
                rel = f.relative_to(repo_root)
                violations.append((tok, f"undefined-id {tok} cited in {rel} but not defined in the Allocated IDs table"))
    return violations


ID_CHECK_CODES = ['dup-id', 'range-id', 'revived-id', 'undefined-id']


def run_id_checks(repo_root):
    numbering_path = repo_root / 'NUMBERING.md'
    if not numbering_path.exists():
        return []
    data = parse_numbering(numbering_path)
    violations = []
    violations += check_dup_id(data['allocated'])
    violations += check_range_id(data['allocated'], data['pf_ranges'], data['mc_ranges'])
    violations += check_revived_id(data['allocated'], data['deprecated'])
    violations += check_undefined_id(data['allocated'], repo_root)
    return violations


# ---------------------------------------------------------------------------
# examples/deal-brief.md — figure integrity (D-10)
# ---------------------------------------------------------------------------

def parse_deal_brief(path):
    text = path.read_text(encoding='utf-8')
    sections = split_sections(text)
    figures = []
    for row in table_rows(sections.get('Canonical figures', '')):
        if not row or not row[0]:
            continue
        figures.append({
            'key': row[0].strip(),
            'value': row[1].strip() if len(row) > 1 else '',
            'type': row[2].strip() if len(row) > 2 else '',
            'what': row[3].strip() if len(row) > 3 else '',
        })
    return figures


def check_dup_figure_key(figures):
    seen = {}
    for f in figures:
        seen.setdefault(f['key'], []).append(f)
    violations = []
    for key, rows in seen.items():
        if len(rows) > 1:
            violations.append((key, f"dup-figure-key {key} appears in {len(rows)} rows of the Canonical figures table"))
    return violations


def check_figure_order(figures):
    keys = [f['key'] for f in figures]
    if keys and keys != sorted(keys):
        return [(keys[0], "figure-order the Canonical figures table's rows are not in ascending key order")]
    return []


CURRENCY_RE = re.compile(r'\$\d[\d,]*(?:\.\d+)?[MKB]?')
PERCENT_RE = re.compile(r'\b\d+(?:\.\d+)?%')
ISO_DATE_RE = re.compile(r'\b\d{4}-\d{2}-\d{2}\b')


UNLISTED_FIGURE_SCAN_ROOTS = ('examples', 'skills')


def check_unlisted_figure(figures, repo_root):
    canonical_values = {f['value'] for f in figures}
    violations = []
    seen = set()
    files = []
    for root_name in UNLISTED_FIGURE_SCAN_ROOTS:
        root = repo_root / root_name
        if not root.exists():
            continue
        files.extend(sorted(root.rglob('*.md')))
    for f in files:
        if f.name == 'NUMBERING.md':
            continue
        text = strip_fences(f.read_text(encoding='utf-8'))
        lines = text.splitlines()
        in_canonical = False
        for line in lines:
            if re.match(r'^## Canonical figures\s*$', line):
                in_canonical = True
                continue
            # Bound the exempt region by table shape, not only by the next
            # heading: a blank/table-row line keeps it open; the first line
            # that is neither ends it and is itself scanned below.
            if in_canonical:
                stripped = line.strip()
                if stripped == '' or stripped.startswith('|'):
                    continue
                in_canonical = False
            if re.match(r'^## ', line):
                in_canonical = False
            if line.startswith('Last reviewed:'):
                continue
            tokens = CURRENCY_RE.findall(line) + PERCENT_RE.findall(line) + ISO_DATE_RE.findall(line)
            for tok in tokens:
                if tok not in canonical_values:
                    key = (tok, str(f))
                    if key not in seen:
                        seen.add(key)
                        rel = f.relative_to(repo_root)
                        violations.append((tok, f"unlisted-figure {tok} in {rel} has no matching Canonical figures row"))
    return violations


FIGURE_CHECK_CODES = ['dup-figure-key', 'figure-order', 'unlisted-figure']


def run_figure_checks(repo_root):
    brief_path = repo_root / 'examples' / 'deal-brief.md'
    if not brief_path.exists():
        return []
    figures = parse_deal_brief(brief_path)
    violations = []
    violations += check_dup_figure_key(figures)
    violations += check_figure_order(figures)
    violations += check_unlisted_figure(figures, repo_root)
    return violations


# ---------------------------------------------------------------------------
# NOTICES.md — attribution integrity (D-14)
# ---------------------------------------------------------------------------

FENCE_CONTENT_RE = re.compile(r'```[^\n]*\n(.*?)\n```', re.S)


def _carrier_is_repo_relative(carrier):
    """True unless carrier is absolute, a drive-letter path, or escapes the
    repository via a '..' path segment. A carrier failing this test is never
    opened (T-01-01: pathlib's '/' operator silently discards the base for an
    absolute right-hand side)."""
    if carrier.startswith('/') or carrier.startswith('\\'):
        return False
    if re.match(r'^[A-Za-z]:', carrier):
        return False
    parts = re.split(r'[\\/]', carrier)
    if '..' in parts:
        return False
    return True


def parse_notices(path):
    text = path.read_text(encoding='utf-8')
    sections = split_sections(text)
    body = sections.get(POINTER_SECTION, '')

    pointer = None
    m = FENCE_CONTENT_RE.search(body)
    if m:
        content = m.group(1).strip()
        if content:
            pointer = content

    carriers = []
    idx = body.find(CARRIERS_MARKER)
    if idx != -1:
        tail = body[idx:]
        for line in tail.splitlines()[1:]:
            m2 = re.match(r'^\s*[-*]\s+`?([^`\n]+?)`?\s*$', line)
            if m2:
                carriers.append(m2.group(1).strip())
            elif line.strip().startswith('#'):
                break
    return pointer, carriers


def check_pointer(pointer, carriers, repo_root):
    violations = []
    if pointer is None:
        return violations
    for carrier in carriers:
        p = repo_root / carrier
        if not p.exists():
            continue
        count = sum(1 for line in p.read_text(encoding='utf-8').splitlines() if line.strip() == pointer)
        if count == 0:
            violations.append((carrier, f"pointer-missing {carrier} does not contain the attribution pointer string"))
        elif count > 1:
            violations.append((carrier, f"pointer-duplicated {carrier} contains the attribution pointer string {count} times"))
    return violations


NOTICES_CHECK_CODES = ['pointer-missing', 'pointer-duplicated', 'pointer-unparseable']


# ---------------------------------------------------------------------------
# LICENSE.md — license integrity (LEG-01)
# ---------------------------------------------------------------------------

def check_license_missing(repo_root):
    """Check that LICENSE exists at repo root, is non-empty, and begins
    with 'MIT License'."""
    violations = []
    license_path = repo_root / 'LICENSE'
    if not license_path.exists():
        violations.append(('LICENSE', "license-missing LICENSE file is absent from the repository root"))
        return violations

    text = license_path.read_text(encoding='utf-8')
    if not text:
        violations.append(('LICENSE', "license-missing LICENSE file is empty"))
        return violations

    first_line = text.split('\n')[0] if text else ''
    if not first_line.startswith('MIT License'):
        violations.append(('LICENSE', "license-missing LICENSE file does not identify itself as the MIT License"))

    return violations


LICENSE_CHECK_CODES = ['license-missing']


def run_license_checks(repo_root):
    violations = []
    violations += check_license_missing(repo_root)
    return violations


# ---------------------------------------------------------------------------
# NOTICES.md — framework statements integrity (LEG-02)
# ---------------------------------------------------------------------------

def check_framework_statements(repo_root):
    """Check that NOTICES.md carries the three required framework statements
    with their non-affiliation and trademark-rights language."""
    violations = []
    notices_path = repo_root / 'NOTICES.md'

    # Define required frameworks and their required sub-heading patterns
    frameworks = {
        'Command of the Message': ('### Command of the Message', 'Non-affiliation'),
        'MEDDIC/MEDDICC': ('### MEDDIC, MEDDICC, and related marks', 'Non-affiliation'),
        'Challenger': ('### Challenger', 'Non-affiliation'),
    }

    if not notices_path.exists():
        # If NOTICES.md is missing, all three frameworks are missing
        for framework_name in frameworks.keys():
            violations.append((framework_name, f"framework-statement-missing {framework_name} subsection is missing from NOTICES.md"))
        return violations

    text = notices_path.read_text(encoding='utf-8')

    for framework_name, (heading_pattern, required_language) in frameworks.items():
        if heading_pattern not in text:
            violations.append((framework_name, f"framework-statement-missing {framework_name} subsection is missing from NOTICES.md"))
            continue

        # Find the section for this framework
        heading_idx = text.find(heading_pattern)
        # Find the end of this section (next ### or ##)
        next_section = len(text)
        for pattern in ['### ', '## ']:
            idx = text.find('\n' + pattern, heading_idx + 1)
            if idx != -1 and idx < next_section:
                next_section = idx

        framework_section = text[heading_idx:next_section]

        # Check for non-affiliation language
        if 'Non-affiliation' not in framework_section or 'not affiliated' not in framework_section.lower():
            violations.append((framework_name, f"framework-statement-missing {framework_name} subsection missing non-affiliation language"))

        # Check for trademark/rights language
        if 'Rights-holder' not in framework_section:
            violations.append((framework_name, f"framework-statement-missing {framework_name} subsection missing trademark-rights language"))

    return violations


FRAMEWORK_CHECK_CODES = ['framework-statement-missing']


def run_framework_checks(repo_root):
    violations = []
    violations += check_framework_statements(repo_root)
    return violations


def run_notices_checks(repo_root):
    notices_path = repo_root / 'NOTICES.md'
    if not notices_path.exists():
        return []
    pointer, carriers = parse_notices(notices_path)
    if pointer is None:
        return [('NOTICES.md', "pointer-unparseable NOTICES.md's Attribution pointer section yields no usable pointer definition")]

    violations = []
    valid_carriers = []
    for carrier in carriers:
        if not _carrier_is_repo_relative(carrier):
            violations.append((carrier, f"pointer-unparseable {carrier} is a required-carrier entry that is not a repository-relative path"))
            continue
        valid_carriers.append(carrier)

    violations += check_pointer(pointer, valid_carriers, repo_root)
    return violations


ALL_CHECK_CODES = ID_CHECK_CODES + FIGURE_CHECK_CODES + NOTICES_CHECK_CODES + LICENSE_CHECK_CODES + FRAMEWORK_CHECK_CODES


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def run_all_checks(repo_root):
    violations = []
    violations += run_id_checks(repo_root)
    violations += run_figure_checks(repo_root)
    violations += run_notices_checks(repo_root)
    violations += run_license_checks(repo_root)
    violations += run_framework_checks(repo_root)
    return violations


# ---------------------------------------------------------------------------
# Mutation testing (CR-01 gap closure)
#
# The self-test above proves each check fires against a hand-built fixture.
# It cannot prove a check fires against this repository's own production
# document shapes -- that gap is exactly what let a dead check ship named as
# covered (01-VERIFICATION.md). This section injects one named defect at a
# time into a throwaway copy of the real repository files and asserts the
# matching violation code fires, closing the class rather than today's
# instances of it.
# ---------------------------------------------------------------------------

MUTATION_SOURCES = ('LICENSE', 'NUMBERING.md', 'NOTICES.md', 'README.md', 'examples', 'tools', 'skills')


def _copy_repo_subset(repo_root, dest):
    """Copy exactly MUTATION_SOURCES into dest. Never copies .git or
    .planning -- only the repository-relative paths the checker reads."""
    for name in MUTATION_SOURCES:
        src = repo_root / name
        if not src.exists():
            continue
        target = dest / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, target)
        else:
            shutil.copy2(src, target)


def _insert_table_rows_after_heading(text, heading, new_rows):
    """Insert new_rows immediately after the first Markdown table's
    separator row that follows the '## {heading}' line -- the only
    insertion point that works while a table has zero data rows."""
    lines = text.splitlines()
    heading_line = f'## {heading}'
    h_idx = next(i for i, l in enumerate(lines) if l.strip() == heading_line)
    i = h_idx + 1
    while i < len(lines) and not lines[i].strip().startswith('|'):
        i += 1
    header_idx = i
    sep_idx = header_idx + 1
    insert_at = sep_idx + 1
    out = lines[:insert_at] + list(new_rows) + lines[insert_at:]
    return '\n'.join(out) + '\n'


def _mutate_dup_id(root):
    path = root / 'NUMBERING.md'
    text = path.read_text(encoding='utf-8')
    row = '| PF-0.1 | Mutation dup row | SKILL.md | v0.0.0 |'
    text = _insert_table_rows_after_heading(text, 'Allocated IDs', [row, row])
    path.write_text(text, encoding='utf-8')


def _mutate_range_id(root):
    path = root / 'NUMBERING.md'
    text = path.read_text(encoding='utf-8')
    row = '| PF-0.99 | Mutation over-ceiling row | SKILL.md | v0.0.0 |'
    text = _insert_table_rows_after_heading(text, 'Allocated IDs', [row])
    path.write_text(text, encoding='utf-8')


def _mutate_revived_id(root):
    path = root / 'NUMBERING.md'
    text = path.read_text(encoding='utf-8')
    text = _insert_table_rows_after_heading(
        text, 'Allocated IDs', ['| PF-0.3 | Mutation revived row | SKILL.md | v0.0.0 |'])
    text = _insert_table_rows_after_heading(
        text, 'Deprecated IDs', ['| PF-0.3 | v0.0.0 | PF-0.1 |'])
    path.write_text(text, encoding='utf-8')


def _mutate_undefined_id(root):
    path = root / 'README.md'
    text = path.read_text(encoding='utf-8')
    if not text.endswith('\n'):
        text += '\n'
    text += '\nThis mutation cites PF-9.9, which no Allocated IDs row defines.\n'
    path.write_text(text, encoding='utf-8')


def _mutate_dup_figure_key(root):
    path = root / 'examples' / 'deal-brief.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    h_idx = next(i for i, l in enumerate(lines) if l.strip() == '## Canonical figures')
    i = h_idx + 1
    while not lines[i].strip().startswith('|'):
        i += 1
    first_row_idx = i + 2  # i = header row, i+1 = separator row, i+2 = first data row
    lines.insert(first_row_idx + 1, lines[first_row_idx])
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_figure_order(root):
    path = root / 'examples' / 'deal-brief.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    h_idx = next(i for i, l in enumerate(lines) if l.strip() == '## Canonical figures')
    i = h_idx + 1
    while not lines[i].strip().startswith('|'):
        i += 1
    first_row_idx = i + 2
    j = first_row_idx
    while j < len(lines) and lines[j].strip().startswith('|'):
        j += 1
    last_row_idx = j - 1
    last_row = lines.pop(last_row_idx)
    lines.insert(first_row_idx, last_row)
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_unlisted_figure(root):
    path = root / 'examples' / 'deal-brief.md'
    text = path.read_text(encoding='utf-8')
    if not text.endswith('\n'):
        text += '\n'
    text += (
        "This prose line was appended after the Canonical figures table, the "
        "file's last section, and cites $123,456,789 which matches no row.\n"
    )
    path.write_text(text, encoding='utf-8')


def _mutate_pointer_missing(root):
    pointer, _carriers = parse_notices(root / 'NOTICES.md')
    path = root / 'README.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    lines = [l for l in lines if l.strip() != pointer]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_pointer_duplicated(root):
    pointer, _carriers = parse_notices(root / 'NOTICES.md')
    path = root / 'README.md'
    text = path.read_text(encoding='utf-8')
    if not text.endswith('\n'):
        text += '\n'
    text += pointer + '\n'
    path.write_text(text, encoding='utf-8')


def _mutate_pointer_unparseable(root):
    path = root / 'NOTICES.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    lines = [l for l in lines if l.strip() != '## Attribution pointer']
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_license_missing(root):
    path = root / 'LICENSE'
    if path.exists():
        path.unlink()


def _mutate_framework_statement_missing(root):
    path = root / 'NOTICES.md'
    if path.exists():
        path.unlink()


MUTATIONS = [
    ('dup-id', "insert the same allocated-ID row twice into NUMBERING.md's Allocated IDs table", _mutate_dup_id),
    ('range-id', "insert an allocated-ID row whose PF number sits above its section's declared ceiling", _mutate_range_id),
    ('revived-id', "insert the same ID into both the Allocated IDs table and the Deprecated IDs table", _mutate_revived_id),
    ('undefined-id', "cite a PF ID in README.md that no Allocated IDs row defines", _mutate_undefined_id),
    ('dup-figure-key', "duplicate the first data row of the Canonical figures table", _mutate_dup_figure_key),
    ('figure-order', "move the Canonical figures table's last data row to the top", _mutate_figure_order),
    ('unlisted-figure', "append a stray currency token after the Canonical figures table, the file's last section", _mutate_unlisted_figure),
    ('pointer-missing', "remove the canonical pointer line from README.md", _mutate_pointer_missing),
    ('pointer-duplicated', "append a second copy of the canonical pointer line to README.md", _mutate_pointer_duplicated),
    ('pointer-unparseable', "remove the Attribution pointer heading from NOTICES.md", _mutate_pointer_unparseable),
    ('license-missing', "delete the LICENSE file from the repository root", _mutate_license_missing),
    ('framework-statement-missing', "delete the NOTICES.md file entirely from the repository root", _mutate_framework_statement_missing),
]


def mutation_test(repo_root):
    """Run a clean control copy, then one isolated mutation per violation
    code, and report per-code pass/fail. Returns True only when the control
    was clean, every mutation fired its expected code, and every code in
    ALL_CHECK_CODES has a registered mutation."""
    all_ok = True
    codes_covered = set()

    with tempfile.TemporaryDirectory(prefix='check-repo-mutation-control-') as tmp:
        control_root = Path(tmp) / 'control'
        _copy_repo_subset(repo_root, control_root)
        control_violations = run_all_checks(control_root)
        print(f"mutation-test CONTROL: {len(control_violations)} violations on the unmutated copy")
        if control_violations:
            all_ok = False

    for code, description, mutate_fn in MUTATIONS:
        with tempfile.TemporaryDirectory(prefix=f'check-repo-mutation-{code}-') as tmp:
            scratch_root = Path(tmp) / 'scratch'
            _copy_repo_subset(repo_root, scratch_root)
            mutate_fn(scratch_root)
            violations = run_all_checks(scratch_root)
            fired = any(line.split(' ', 1)[0] == code for _, line in violations)
        if fired:
            print(f"mutation-test OK: {code} {description}")
            codes_covered.add(code)
        else:
            print(f"mutation-test FAIL: {code} {description}")
            all_ok = False

    uncovered = [c for c in ALL_CHECK_CODES if c not in {m[0] for m in MUTATIONS}]
    for code in uncovered:
        print(f"mutation-test FAIL: {code} has no registered mutation")
        all_ok = False

    if all_ok:
        print(f"mutation-test PASS: {len(codes_covered)} codes proven live")
    else:
        failed = len(ALL_CHECK_CODES) - len(codes_covered)
        print(f"mutation-test FAILED: {failed} codes not proven live")

    return all_ok


# ---------------------------------------------------------------------------
# Self-test fixtures
# ---------------------------------------------------------------------------

def _write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def _bad_numbering():
    return """## PF reserved ranges
| Section | Range | Concern | Allocated | Next free |
|---|---|---|---|---|
| PF-0 | PF-0.1-PF-0.9 | Opening | 1 | PF-0.2 |
| PF-1 | PF-1.1-PF-1.4 | Structure | 0 | PF-1.1 |

## MC reserved blocks
| Dimension | Range |
|---|---|
| Metric | MC-1-MC-5 |
| Economic Buyer | MC-8-MC-10 |

## Allocated IDs
| ID | Title | Defined in | Added in |
|---|---|---|---|
| PF-0.1 | Opening rule | SKILL.md | v1.0.0 |
| PF-0.1 | Opening rule dup | SKILL.md | v1.0.0 |
| PF-1.9 | Out of range rule | SKILL.md | v1.0.0 |
| MC-6 | Gap-landing rule | SKILL.md | v1.0.0 |
| MC-99 | Out of range MC | SKILL.md | v1.0.0 |
| PF-0.5 | Revived rule | SKILL.md | v1.0.0 |

## Deprecated IDs
| ID | Deprecated in | Absorbed by |
|---|---|---|
| PF-0.5 | v1.1.0 | PF-0.1 |
"""


def _good_numbering():
    return """## PF reserved ranges
| Section | Range | Concern | Allocated | Next free |
|---|---|---|---|---|
| PF-0 | PF-0.1-PF-0.9 | Opening | 1 | PF-0.2 |
| PF-1 | PF-1.1-PF-1.4 | Structure | 0 | PF-1.1 |

## MC reserved blocks
| Dimension | Range |
|---|---|
| Metric | MC-1-MC-5 |

## Allocated IDs
| ID | Title | Defined in | Added in |
|---|---|---|---|
| PF-0.1 | Opening rule | SKILL.md | v1.0.0 |
| MC-1 | Lower boundary rule | SKILL.md | v1.0.0 |
| MC-5 | Upper boundary rule | SKILL.md | v1.0.0 |

## Deprecated IDs
| ID | Deprecated in | Absorbed by |
|---|---|---|
"""


def _bad_deal_brief():
    return """## Canonical figures
| Key | Value | Type | What it is |
|---|---|---|---|
| total-contract-value | $6,000,000 | currency | Total contract value |
| bidder-count | 3 | count | Number of bidders |
| bidder-count | 4 | count | Duplicate key |

A stray figure of $999,999,999 appears after the table, with no further heading in this fixture.
"""


def _good_deal_brief():
    return """## Canonical figures
| Key | Value | Type | What it is |
|---|---|---|---|
| audit-fee-rate | 5% | percent | Fee rate charged for the audit engagement |
| bidder-count | 3 | count | Number of bidders |
| escrow-fee-rate | 5% | percent | Fee rate charged for the escrow arrangement |
| total-contract-value | $6,000,000 | currency | Total contract value |

The escrow fee rate is 5%, a value-collision fixture pinning the documented matching ceiling.
This trailing line sits after the table's last row and cites no currency, percentage, or date.
"""


def _bad_notices():
    return """## Attribution pointer

The following string is the canonical, verbatim attribution pointer. A human contributor and
`tools/check_repo.py` both read this fenced block as the single source of truth for the string.

```
Test pointer string.
```

### Files required to carry it

- `carrier-missing.md`
- `carrier-dup.md`
- `carrier-lookalike.md`
"""


def _good_notices():
    return """## Attribution pointer

The following string is the canonical, verbatim attribution pointer. A human contributor and
`tools/check_repo.py` both read this fenced block as the single source of truth for the string.

```
Test pointer string.
```

### Files required to carry it

- `carrier-ok.md`

## Framework statements

The three statements below appear in a fixed order.

### Command of the Message

**Mark:** Command of the Message

**Rights-holder:** Force Management.

**Non-affiliation:** This project is not affiliated with, endorsed by, sponsored by, or connected
to Force Management.

**Paraphrase boundary:** This repository restates concepts.

### MEDDIC, MEDDICC, and related marks

**Mark:** MEDDIC, MEDDICC, MEDDPICC.

**Rights-holder:** Multiple parties.

**Non-affiliation:** This project is not affiliated with any party claiming rights.

**Paraphrase boundary:** This repository restates concepts.

### Challenger

**Mark:** Challenger.

**Rights-holder:** Challenger Inc.

**Non-affiliation:** This project is not affiliated with Challenger Inc.

**Paraphrase boundary:** This repository restates concepts.
"""


def _unparseable_notices():
    return """## Attribution pointer

The following string is the canonical, verbatim attribution pointer, but this fixture omits the
fenced block entirely so the section yields no usable pointer definition.

### Files required to carry it

- `carrier-ok.md`
"""


def _escaping_notices():
    return """## Attribution pointer

The following string is the canonical, verbatim attribution pointer. A human contributor and
`tools/check_repo.py` both read this fenced block as the single source of truth for the string.

```
Test pointer string.
```

### Files required to carry it

- `../escaped.md`
"""


def _bad_license():
    return ""  # Empty file


def _good_license():
    return """MIT License

Copyright (c) 2026 Proof First contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
"""


def _bad_notices_frameworks():
    return """## Framework statements

The three statements below appear in a fixed order, and each carries the same four labelled
elements in the same order, so a future diff to this section shows a content change and never a
reordering.

### MEDDIC, MEDDICC, and related marks

**Mark:** MEDDIC, MEDDICC, MEDDPICC, and related marks in this family.

**Rights-holder:** Ownership of these marks is claimed by multiple parties and is contested.

**Non-affiliation:** This project is not affiliated with, endorsed by, or sponsored by any party
claiming rights in these marks.

**Paraphrase boundary:** This repository restates concepts associated with this family of marks in
its own words and reproduces no training material.

### Challenger

**Mark:** Challenger (the Challenger Sale methodology).

**Rights-holder:** Challenger Inc. and its trademark successors.

**Non-affiliation:** This project is not affiliated with, endorsed by, sponsored by, or connected
to Challenger Inc. or its trademark successors.

**Paraphrase boundary:** This repository restates concepts associated with Challenger in its own
words and reproduces no training material.
"""


def _good_notices_frameworks():
    return """## Framework statements

The three statements below appear in a fixed order, and each carries the same four labelled
elements in the same order, so a future diff to this section shows a content change and never a
reordering.

### Command of the Message

**Mark:** Command of the Message

**Rights-holder:** Force Management.

**Non-affiliation:** This project is not affiliated with, endorsed by, sponsored by, or connected
to Force Management.

**Paraphrase boundary:** This repository restates concepts associated with Command of the Message
in its own words and reproduces no training material, no course content, and no proprietary
diagram belonging to Force Management.

### MEDDIC, MEDDICC, and related marks

**Mark:** MEDDIC, MEDDICC, MEDDPICC, and related marks in this family.

**Rights-holder:** Ownership of these marks is claimed by multiple parties and is contested.

**Non-affiliation:** This project is not affiliated with, endorsed by, or sponsored by any party
claiming rights in these marks.

**Paraphrase boundary:** This repository restates concepts associated with this family of marks in
its own words and reproduces no training material, no course content, and no proprietary diagram
belonging to any claimant.

### Challenger

**Mark:** Challenger (the Challenger Sale methodology).

**Rights-holder:** Challenger Inc. and its trademark successors.

**Non-affiliation:** This project is not affiliated with, endorsed by, sponsored by, or connected
to Challenger Inc. or its trademark successors.

**Paraphrase boundary:** This repository restates concepts associated with Challenger in its own
words and reproduces no training material, no course content, and no proprietary diagram belonging
to Challenger Inc. or its trademark successors.
"""


def self_test():
    codes_covered = set()
    all_ok = True
    with tempfile.TemporaryDirectory(prefix='check-repo-self-test-') as tmp:
        tmp_root = Path(tmp)
        bad_root = tmp_root / 'bad'
        good_root = tmp_root / 'good'
        unparseable_root = tmp_root / 'unparseable'
        escaping_root = tmp_root / 'escaping'
        bad_license_root = tmp_root / 'bad_license'
        bad_frameworks_root = tmp_root / 'bad_frameworks'

        _write(bad_root / 'NUMBERING.md', _bad_numbering())
        _write(bad_root / 'skills' / 'SKILL.md', "See PF-9.9 and MC-1 for details.\n")
        _write(bad_root / 'examples' / 'deal-brief.md', _bad_deal_brief())
        _write(bad_root / 'examples' / 'scenario.md', "The deal is valued at $999,999 over the term.\n")
        _write(bad_root / 'NOTICES.md', _bad_notices())
        _write(bad_root / 'carrier-missing.md', "This file does not carry the pointer.\n")
        _write(bad_root / 'carrier-dup.md', "Test pointer string.\nSomething else.\nTest pointer string.\n")
        _write(bad_root / 'carrier-lookalike.md', "Test pointer\u00a0string.\n")
        _write(bad_root / 'LICENSE', _bad_license())

        _write(good_root / 'NUMBERING.md', _good_numbering())
        _write(good_root / 'skills' / 'SKILL.md', "See PF-0.1 for details.\n")
        _write(good_root / 'examples' / 'deal-brief.md', _good_deal_brief())
        _write(good_root / 'NOTICES.md', _good_notices())
        _write(good_root / 'carrier-ok.md', "Test pointer string.\n")
        _write(good_root / 'LICENSE', _good_license())

        # Third and fourth scratch roots isolate the two `pointer-unparseable`
        # triggers so each fires alone, on its own root, and stays silent on
        # both bad_root and good_root.
        _write(unparseable_root / 'NOTICES.md', _unparseable_notices())
        _write(unparseable_root / 'carrier-ok.md', "Test pointer string.\n")
        _write(unparseable_root / 'LICENSE', _good_license())

        _write(escaping_root / 'NOTICES.md', _escaping_notices())
        _write(escaping_root / 'LICENSE', _good_license())

        # Fifth root tests license-missing
        _write(bad_license_root / 'NUMBERING.md', _good_numbering())
        _write(bad_license_root / 'NOTICES.md', _good_notices())
        _write(bad_license_root / 'carrier-ok.md', "Test pointer string.\n")
        # Deliberately omit LICENSE file

        # Sixth root tests framework-statement-missing
        _write(bad_frameworks_root / 'NUMBERING.md', _good_numbering())
        _write(bad_frameworks_root / 'NOTICES.md', _bad_notices_frameworks())
        _write(bad_frameworks_root / 'carrier-ok.md', "Test pointer string.\n")
        _write(bad_frameworks_root / 'LICENSE', _good_license())


        bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(bad_root)}
        good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(good_root)}
        unparseable_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(unparseable_root)}
        escaping_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(escaping_root)}
        bad_license_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(bad_license_root)}
        bad_frameworks_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(bad_frameworks_root)}
        # Union the third/fourth roots' codes into the bad-code set so the
        # coverage loop below needs no edit — it still just checks "did the
        # code fire on some known-bad fixture and stay silent on good_root".
        bad_codes |= unparseable_codes | escaping_codes | bad_license_codes | bad_frameworks_codes

        for code in ALL_CHECK_CODES:
            if code not in bad_codes:
                print(f"FAIL: {code} did not fire on the known-bad fixture")
                all_ok = False
                continue
            if code in good_codes:
                print(f"FAIL: {code} fired on the known-good fixture")
                all_ok = False
                continue
            codes_covered.add(code)

    if not all_ok:
        return False

    print(f"self-test PASS - verified violation codes: {', '.join(sorted(codes_covered))}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--mutation-test', action='store_true')
    args = parser.parse_args()

    if args.self_test:
        ok = self_test()
        sys.exit(0 if ok else 1)

    if args.mutation_test:
        ok = mutation_test(REPO_ROOT)
        sys.exit(0 if ok else 1)

    violations = run_all_checks(REPO_ROOT)
    violations.sort(key=lambda v: (v[1].split(' ', 1)[0], v[0]))
    if not violations:
        print("check_repo: 0 violations")
        sys.exit(0)
    for _, line in violations:
        print(line)
    sys.exit(1)


if __name__ == '__main__':
    main()

