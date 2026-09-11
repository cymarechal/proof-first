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
  range-id          - a PF ID sits outside its section's reserved range, an
                      MC ID belongs to no declared MC dimension block
                      (checked per block, not against one aggregate range
                      spanning all blocks), or a PF ID sits inside its
                      section's reserved range but outside every sub-block
                      that section's own NUMBERING.md table declares (a
                      section declaring no sub-blocks keeps exactly the
                      section-range behaviour, unchanged). Declared ceiling:
                      when a section's sub-blocks tile its whole reserved
                      range — which both PF-1 and PF-2 currently do — this
                      test adds nothing beyond the section-range test; it
                      exists so a future narrowed or gapped sub-block table
                      is enforced rather than decorative.
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
  catalog-id-drift  - for each installed skill folder (a path matching
                      skills/*/SKILL.md), the PF subset of NUMBERING.md's
                      Allocated IDs, the SKILL.md's own rule-defining
                      headings, and references/checklist.md's listed PF
                      rows are not all equal. Fires once per divergent ID,
                      naming the files it is inconsistent between. A repo
                      with no path matching skills/*/SKILL.md yields no
                      violations. Declared ceiling: this check compares ID
                      sets only. It does not detect a rule whose title in
                      checklist.md disagrees with its title in
                      NUMBERING.md, nor a heading whose title text has
                      drifted from its registry row; and it reads only
                      paths one directory level below skills/, so a
                      SKILL.md placed anywhere else is not validated.
  frontmatter-unparseable - a skills/*/SKILL.md's frontmatter block has no
                      `---` delimited block at the file's first line, is
                      unterminated (no closing `---`), is missing one of
                      the two required keys (`name`, `description`), or
                      repeats a column-zero key. A repeated key is
                      reported rather than silently kept as a last-value-
                      wins merge — the first value is what the parser
                      keeps, but the repetition itself is the violation.
                      Declared ceiling: this parser recognises only a
                      column-zero key, a `|` block scalar, and an
                      indented nested map; a value written with any other
                      construct is read as an opaque string, never
                      individually validated.
  frontmatter-unknown-key - a skills/*/SKILL.md's frontmatter carries a
                      column-zero key outside the Agent Skills
                      specification's six-key allow-list (`name`,
                      `description`, `license`, `compatibility`,
                      `metadata`, `allowed-tools`), naming the key.
                      Declared ceiling: only the key's name is checked,
                      never the shape of its value.
  frontmatter-name-mismatch - a skills/*/SKILL.md's frontmatter `name`
                      value differs from its own parent directory name,
                      naming both. Declared ceiling: this check compares
                      `name` against the parent directory only; it does
                      not enforce the specification's own character-set
                      or length rules for `name`.
  frontmatter-description-invalid - a skills/*/SKILL.md's frontmatter
                      `description` is absent, empty after whitespace
                      collapse, shorter than 200 characters, or longer
                      than 1024 characters, naming the measured length
                      and the bound it broke. Declared ceiling: 200 is
                      this project's own chosen floor, not a
                      specification requirement; 1024 is the
                      specification's own ceiling, used here unchanged.
  catalog-count-unstated - a skills/*/SKILL.md contains no line matching
                      the frozen stated-count template ("This catalog
                      contains {N} rules in {M} numbered sections.").
                      Absence of the file is still not a violation.
                      Declared ceiling: the template is matched
                      byte-exactly, so a reworded but equivalent sentence
                      is reported as unstated rather than as a mismatch.
  catalog-count-mismatch - a skills/*/SKILL.md's stated rule count or
                      stated section count disagrees with the count of
                      PF rows (or distinct PF sections among them) in
                      NUMBERING.md's Allocated IDs table, naming both the
                      stated and the registry figures. Declared ceiling:
                      this check compares the two stated numbers against
                      the registry only — it does not detect a stated
                      total that is right while a rule body is missing
                      from the file entirely; that direction is
                      catalog-id-drift's.
  skill-too-long    - a skills/*/SKILL.md exceeds 500 lines, naming the
                      measured count and the ceiling. Silent at exactly
                      500. Declared ceiling: line count is a proxy for
                      the Agent Skills specification's approximate
                      5,000-token progressive-disclosure budget; a file
                      under 500 lines with unusually long lines can still
                      exceed that token budget, which this check cannot
                      detect on its own — skill-token-budget-exceeded is
                      the companion check for that direction.
  skill-token-budget-exceeded - a skills/*/SKILL.md's estimated token
                      count exceeds 5,000, the Agent Skills
                      specification's own approximate ceiling behind
                      CAT-08 ("under 500 lines, approximately 5,000
                      tokens"). No tokenizer is available to a standard-
                      library-only checker, so this check estimates
                      tokens as word_count * 1.3 — a word-to-token ratio
                      calibrated against this project's own sibling
                      skill (`simple-english/SKILL.md`), which
                      02-RESEARCH.md measured at 3,664 words and recorded
                      as comfortably under the same ~5,000-token ceiling;
                      3,664 * 1.3 ≈ 4,763, consistent with that recorded
                      finding. Declared ceiling: this is a word-count
                      proxy, not a real tokenizer; it counts words across
                      the whole file including its frontmatter block, not
                      the post-frontmatter body alone; and a different
                      estimator (for example characters / 4) gives a
                      materially different figure for the same file —
                      this check uses one stated estimator consistently,
                      never the more favourable of several. As of this
                      writing this code fires against this repository's
                      own skills/proof-first/SKILL.md — a known, tracked,
                      open finding against CAT-08 (see
                      .planning/WINDOWS.md), not a defect in this check.
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

SKILL_GLOB = 'skills/*/SKILL.md'


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


def parse_pf_subblocks(path):
    """Return {section: [(low, high, element_name), ...]} built from every
    '## PF-<n> sub-blocks' section, reusing split_sections/table_rows rather
    than a second table reader. A section with no such heading (PF-0, PF-3,
    PF-4, and PF-5 as of this writing) is simply absent from the returned
    mapping -- absence means "no sub-blocks declared", not a defect, and
    check_range_id below keeps exactly today's section-range-only behaviour
    for it."""
    text = path.read_text(encoding='utf-8')
    sections = split_sections(text)
    subblocks = {}
    for heading, body in sections.items():
        m = re.match(r'^(PF-\d+) sub-blocks$', heading)
        if not m:
            continue
        section = m.group(1)
        blocks = []
        for row in table_rows(body):
            if len(row) < 2:
                continue
            element_name = row[0].strip()
            nums = re.findall(r'PF-\d+\.(\d+)', row[1])
            if len(nums) >= 2:
                blocks.append((int(nums[0]), int(nums[-1]), element_name))
        if blocks:
            subblocks[section] = blocks
    return subblocks


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


def check_range_id(allocated, pf_ranges, mc_ranges, pf_subblocks=None):
    pf_subblocks = pf_subblocks or {}
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
            blocks = pf_subblocks.get(section)
            if blocks and not any(lo <= n <= hi for lo, hi, _ in blocks):
                violations.append((id_, f"range-id {id_} sits inside section {section}'s reserved range but outside every sub-block {section} declares"))
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
    pf_subblocks = parse_pf_subblocks(numbering_path)
    violations = []
    violations += check_dup_id(data['allocated'])
    violations += check_range_id(data['allocated'], data['pf_ranges'], data['mc_ranges'], pf_subblocks)
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


# ---------------------------------------------------------------------------
# skills/*/SKILL.md — frontmatter integrity (D-33)
#
# No general-purpose config-format parser exists in the standard library and
# none is added here (D-33). Only six top-level keys are ever legal, so a
# targeted extractor -- in parse_notices's style of finding a specific known
# shape line by line, not a general parser -- is sufficient.
# ---------------------------------------------------------------------------

ALLOWED_FRONTMATTER_KEYS = frozenset({
    'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools',
})
REQUIRED_FRONTMATTER_KEYS = frozenset({'name', 'description'})
DESCRIPTION_MIN = 200
DESCRIPTION_MAX = 1024
FRONTMATTER_DELIM = '---'

FRONTMATTER_KEY_RE = re.compile(r'^([A-Za-z][A-Za-z0-9_-]*):(.*)$')


def parse_frontmatter(path):
    """Parse the frontmatter block of a SKILL.md file with a targeted,
    stdlib-only extractor -- not a general-purpose parser. Returns
    (keys, problems): keys maps each column-zero key found to its value as
    a plain scalar, a `|` block scalar's joined body, or a nested map's raw
    indented text kept as an opaque string (the way parse_notices already
    keeps a fenced block's content opaque). problems is a list of
    human-readable structural defects -- no opening delimiter at the file's
    first line, no closing delimiter, or a column-zero key repeated (kept
    at its FIRST value, never silently overwritten by a later one). Key
    order carries no meaning: the parser reads keys into a mapping and
    never depends on the order they appear in."""
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    problems = []

    if not lines or lines[0].strip() != FRONTMATTER_DELIM:
        problems.append(f"no `{FRONTMATTER_DELIM}` block at the file's first line")
        return {}, problems

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == FRONTMATTER_DELIM:
            end_idx = i
            break
    if end_idx is None:
        problems.append(f"unterminated frontmatter block (no closing `{FRONTMATTER_DELIM}`)")
        return {}, problems

    keys = {}
    current_key = None
    current_lines = []

    def _flush():
        if current_key is None:
            return
        value = '\n'.join(l.strip() for l in current_lines).strip()
        if current_key in keys:
            problems.append(f"repeated top-level key '{current_key}'")
        else:
            keys[current_key] = value

    for line in lines[1:end_idx]:
        m = FRONTMATTER_KEY_RE.match(line)
        if m:
            _flush()
            current_key = m.group(1)
            rest = m.group(2).strip()
            current_lines = [rest] if rest and rest != '|' else []
        else:
            if current_key is not None:
                current_lines.append(line)
    _flush()

    missing_required = sorted(k for k in REQUIRED_FRONTMATTER_KEYS if k not in keys)
    if missing_required:
        problems.append(f"missing required key(s): {', '.join(missing_required)}")

    return keys, problems


def _collapse_whitespace(text):
    return ' '.join(text.split())


def check_frontmatter(repo_root):
    violations = []
    for skill_path in sorted(repo_root.glob(SKILL_GLOB)):
        rel = skill_path.relative_to(repo_root)
        keys, problems = parse_frontmatter(skill_path)

        for problem in problems:
            violations.append((str(rel), f"frontmatter-unparseable {rel} {problem}"))

        for key in keys:
            if key not in ALLOWED_FRONTMATTER_KEYS:
                violations.append((str(rel), f"frontmatter-unknown-key {rel} declares unknown key '{key}'"))

        if 'name' in keys:
            name_value = keys['name']
            dir_name = skill_path.parent.name
            if name_value != dir_name:
                violations.append((str(rel), f"frontmatter-name-mismatch {rel} name '{name_value}' differs from parent directory '{dir_name}'"))

        if 'description' in keys:
            description = _collapse_whitespace(keys['description'])
            desc_len = len(description)
            if desc_len == 0:
                violations.append((str(rel), f"frontmatter-description-invalid {rel} description is empty after whitespace collapse"))
            elif desc_len < DESCRIPTION_MIN:
                violations.append((str(rel), f"frontmatter-description-invalid {rel} description length {desc_len} is below the {DESCRIPTION_MIN}-character floor"))
            elif desc_len > DESCRIPTION_MAX:
                violations.append((str(rel), f"frontmatter-description-invalid {rel} description length {desc_len} exceeds the {DESCRIPTION_MAX}-character ceiling"))
    return violations


FRONTMATTER_CHECK_CODES = [
    'frontmatter-unparseable', 'frontmatter-unknown-key',
    'frontmatter-name-mismatch', 'frontmatter-description-invalid',
]


def run_frontmatter_checks(repo_root):
    return check_frontmatter(repo_root)


# ---------------------------------------------------------------------------
# Skill catalog ID-set integrity (D-32) -- closes the drift a third file
# holding PF IDs (references/checklist.md) can create: an ID registered in
# NUMBERING.md's Allocated IDs table but missing from the checklist, or a
# rule heading defined in SKILL.md with no registry row at all.
# ---------------------------------------------------------------------------

RULE_HEADING_RE = re.compile(r'^### (PF-\d+\.\d+) — ')


def parse_skill_catalog(path):
    """Return the ordered list of PF IDs a SKILL.md *defines* via its rule
    headings. This is distinct from the citation tokens check_undefined_id
    already scans for -- a heading defines a rule, a bracketed marker or a
    prose reference only cites one."""
    text = strip_fences(path.read_text(encoding='utf-8'))
    ids = []
    for line in text.splitlines():
        m = RULE_HEADING_RE.match(line)
        if m:
            ids.append(m.group(1))
    return ids


def parse_checklist(path):
    """Return the PF IDs listed in a references/checklist.md's '## PF rules'
    table, built on the same split_sections/table_rows pair every other
    parser in this file reuses rather than a second table reader."""
    text = path.read_text(encoding='utf-8')
    sections = split_sections(text)
    ids = []
    for row in table_rows(sections.get('PF rules', '')):
        if row and row[0]:
            ids.append(row[0].strip())
    return ids


def check_catalog_id_drift(allocated, repo_root):
    """Compare three sets per installed skill folder: the PF subset of
    NUMBERING.md's Allocated IDs, the SKILL.md's defined-heading IDs, and
    references/checklist.md's listed rows. Report one violation per
    divergent ID, naming the files it is inconsistent between. Absence is
    not failure: a repo with no path matching SKILL_GLOB returns no
    violations, matching this checker's established posture."""
    violations = []
    skill_paths = sorted(repo_root.glob(SKILL_GLOB))
    if not skill_paths:
        return violations

    numbering_pf_ids = {row['id'] for row in allocated if PF_ID_RE.match(row['id'])}

    for skill_path in skill_paths:
        skill_rel = skill_path.relative_to(repo_root)
        skill_ids = set(parse_skill_catalog(skill_path))

        checklist_path = skill_path.parent / 'references' / 'checklist.md'
        checklist_rel = checklist_path.relative_to(repo_root)
        checklist_ids = set(parse_checklist(checklist_path)) if checklist_path.exists() else set()

        all_ids = numbering_pf_ids | skill_ids | checklist_ids
        for id_ in sorted(all_ids):
            in_numbering = id_ in numbering_pf_ids
            in_skill = id_ in skill_ids
            in_checklist = id_ in checklist_ids
            if in_numbering and in_skill and in_checklist:
                continue
            present_in = []
            missing_from = []
            for label, present in (
                ('NUMBERING.md', in_numbering),
                (str(skill_rel), in_skill),
                (str(checklist_rel), in_checklist),
            ):
                (present_in if present else missing_from).append(label)
            violations.append((
                id_,
                f"catalog-id-drift {id_} is present in {', '.join(present_in)} "
                f"but missing from {', '.join(missing_from)}",
            ))
    return violations


# ---------------------------------------------------------------------------
# skills/*/SKILL.md — stated rule count vs registry (D-32)
# ---------------------------------------------------------------------------

COUNT_SENTENCE_RE = re.compile(r'^This catalog contains (\d+) rules in (\d+) numbered sections\.$')


def check_catalog_count(allocated, repo_root):
    """For each skill file, require exactly the frozen stated-count
    template and require its two numbers to match the registry: the count
    of PF rows in the Allocated IDs table, and the count of distinct PF
    sections among those rows. Absence of the file is not a violation."""
    violations = []
    pf_ids = {row['id'] for row in allocated if PF_ID_RE.match(row['id'])}
    registry_rule_count = len(pf_ids)
    registry_section_count = len({PF_ID_RE.match(id_).group(1) for id_ in pf_ids})

    for skill_path in sorted(repo_root.glob(SKILL_GLOB)):
        rel = skill_path.relative_to(repo_root)
        text = skill_path.read_text(encoding='utf-8')
        stated = None
        for line in text.splitlines():
            m = COUNT_SENTENCE_RE.match(line.strip())
            if m:
                stated = (int(m.group(1)), int(m.group(2)))
                break
        if stated is None:
            violations.append((str(rel), f"catalog-count-unstated {rel} contains no line matching the frozen stated-count template"))
            continue
        stated_rules, stated_sections = stated
        if stated_rules != registry_rule_count or stated_sections != registry_section_count:
            violations.append((str(rel), (
                f"catalog-count-mismatch {rel} states {stated_rules} rules in {stated_sections} numbered sections, "
                f"but the registry has {registry_rule_count} rules in {registry_section_count} numbered sections"
            )))
    return violations


# ---------------------------------------------------------------------------
# skills/*/SKILL.md — progressive-disclosure ceiling (CAT-08)
# ---------------------------------------------------------------------------

SKILL_LINE_CEILING = 500


def check_skill_too_long(repo_root):
    violations = []
    for skill_path in sorted(repo_root.glob(SKILL_GLOB)):
        rel = skill_path.relative_to(repo_root)
        line_count = len(skill_path.read_text(encoding='utf-8').splitlines())
        if line_count > SKILL_LINE_CEILING:
            violations.append((str(rel), f"skill-too-long {rel} has {line_count} lines, exceeding the {SKILL_LINE_CEILING}-line ceiling"))
    return violations


# Word-to-token ratio calibrated against the sibling skill's own measured
# shape (02-RESEARCH.md: simple-english/SKILL.md measures 3,664 words,
# recorded as comfortably under the ~5,000-token ceiling this constant also
# enforces here). See this module's docstring for the full derivation.
SKILL_TOKEN_WORDS_PER_TOKEN_RATIO = 1.3
SKILL_TOKEN_CEILING = 5000


def check_skill_token_budget(repo_root):
    """Estimate each skill file's token count as word_count * the ratio
    above and fire when the estimate exceeds SKILL_TOKEN_CEILING. See this
    module's docstring for the declared ceiling of this estimate."""
    violations = []
    for skill_path in sorted(repo_root.glob(SKILL_GLOB)):
        rel = skill_path.relative_to(repo_root)
        text = skill_path.read_text(encoding='utf-8')
        word_count = len(text.split())
        estimated_tokens = int(word_count * SKILL_TOKEN_WORDS_PER_TOKEN_RATIO)
        if estimated_tokens > SKILL_TOKEN_CEILING:
            violations.append((str(rel), (
                f"skill-token-budget-exceeded {rel} is estimated at {estimated_tokens} tokens "
                f"({word_count} words x {SKILL_TOKEN_WORDS_PER_TOKEN_RATIO}), "
                f"exceeding the {SKILL_TOKEN_CEILING}-token ceiling"
            )))
    return violations


CATALOG_CHECK_CODES = [
    'catalog-id-drift', 'catalog-count-unstated', 'catalog-count-mismatch',
    'skill-too-long', 'skill-token-budget-exceeded',
]


def run_catalog_checks(repo_root):
    numbering_path = repo_root / 'NUMBERING.md'
    if not numbering_path.exists():
        return []
    data = parse_numbering(numbering_path)
    violations = []
    violations += check_catalog_id_drift(data['allocated'], repo_root)
    violations += check_catalog_count(data['allocated'], repo_root)
    violations += check_skill_too_long(repo_root)
    violations += check_skill_token_budget(repo_root)
    return violations


ALL_CHECK_CODES = (
    ID_CHECK_CODES + FIGURE_CHECK_CODES + NOTICES_CHECK_CODES
    + LICENSE_CHECK_CODES + FRAMEWORK_CHECK_CODES + FRONTMATTER_CHECK_CODES
    + CATALOG_CHECK_CODES
)


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
    violations += run_frontmatter_checks(repo_root)
    violations += run_catalog_checks(repo_root)
    return violations


# ---------------------------------------------------------------------------
# Known, tracked, currently-open violations -- see .planning/WINDOWS.md
#
# skill-token-budget-exceeded is, as of this writing, a real and open
# finding against CAT-08: skills/proof-first/SKILL.md's own word-count
# estimate genuinely exceeds the 5,000-token ceiling this check enforces
# (see the docstring paragraph for the derivation). This is not a defect in
# the check -- the live `check_repo.py` run below still reports it in full,
# unsuppressed. The one place this constant is consulted is mutation-test's
# CONTROL step, which is otherwise a "this repository has zero violations"
# assertion; without this narrow, named allowance, adding this one already-
# true violation would make mutation-test's CONTROL step permanently red
# for a reason mutation-test itself did not introduce and cannot fix,
# masking any *different*, truly unexpected control violation introduced
# later. Every other code stays held to the original, unweakened "zero
# violations on an unmutated copy" bar.
# ---------------------------------------------------------------------------

KNOWN_OPEN_VIOLATIONS = frozenset({'skill-token-budget-exceeded'})


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


def _mutate_catalog_id_drift(root):
    path = root / 'skills' / 'proof-first' / 'references' / 'checklist.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    h_idx = next(i for i, l in enumerate(lines) if l.strip() == '## PF rules')
    i = h_idx + 1
    while not lines[i].strip().startswith('|'):
        i += 1
    first_row_idx = i + 2  # i = header row, i+1 = separator row, i+2 = first data row
    del lines[first_row_idx]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_frontmatter_unparseable(root):
    """Remove the real SKILL.md's opening '---' line, so no frontmatter
    block can be isolated at all."""
    path = root / 'skills' / 'proof-first' / 'SKILL.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    del lines[0]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_frontmatter_unknown_key(root):
    """Insert a column-zero key outside the six-key allow-list (D-33) into
    the real frontmatter. 'compatibility' is deliberately NOT used here --
    it is one of the six *allowed* keys per the Agent Skills specification
    (this project simply omits it by convention, per D-29/D-30), so
    inserting it would prove nothing about this check."""
    path = root / 'skills' / 'proof-first' / 'SKILL.md'
    text = path.read_text(encoding='utf-8')
    text = text.replace('license: MIT\n', 'license: MIT\nauthor: Mutation Author\n', 1)
    path.write_text(text, encoding='utf-8')


def _mutate_frontmatter_name_mismatch(root):
    """Change the real frontmatter's name value so it no longer equals its
    parent directory."""
    path = root / 'skills' / 'proof-first' / 'SKILL.md'
    text = path.read_text(encoding='utf-8')
    text = text.replace('name: proof-first\n', 'name: not-proof-first\n', 1)
    path.write_text(text, encoding='utf-8')


def _mutate_frontmatter_description_invalid(root):
    """Truncate the real description body (the indented lines following
    'description: |') to a few characters, well below the floor."""
    path = root / 'skills' / 'proof-first' / 'SKILL.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        if line.strip() == 'description: |':
            i += 1
            while i < len(lines) and (lines[i].startswith(' ') or lines[i].strip() == ''):
                i += 1
            out.append('  short')
            continue
        i += 1
    path.write_text('\n'.join(out) + '\n', encoding='utf-8')


def _mutate_catalog_count_unstated(root):
    """Delete the stated-count line from the real SKILL.md."""
    path = root / 'skills' / 'proof-first' / 'SKILL.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    lines = [l for l in lines if not COUNT_SENTENCE_RE.match(l.strip())]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_catalog_count_mismatch(root):
    """Change the rule-count number in the real SKILL.md's stated-count
    line so it disagrees with the registry."""
    path = root / 'skills' / 'proof-first' / 'SKILL.md'
    text = path.read_text(encoding='utf-8')
    text = text.replace(
        'This catalog contains 31 rules in 6 numbered sections.',
        'This catalog contains 30 rules in 6 numbered sections.',
        1,
    )
    path.write_text(text, encoding='utf-8')


def _mutate_skill_too_long(root):
    """Append filler lines to the real SKILL.md past its 500-line ceiling."""
    path = root / 'skills' / 'proof-first' / 'SKILL.md'
    text = path.read_text(encoding='utf-8')
    if not text.endswith('\n'):
        text += '\n'
    filler = '\n'.join(f"Filler line {i} pushing the file past its line ceiling." for i in range(200)) + '\n'
    text += filler
    path.write_text(text, encoding='utf-8')


def _mutate_skill_token_budget_exceeded(root):
    """Append filler words to the real SKILL.md, further increasing its
    estimated token count. The real file already exceeds the ceiling
    before this mutation (a known, tracked, open finding -- see
    KNOWN_OPEN_VIOLATIONS and .planning/WINDOWS.md); this mutation still
    registers a named, independent defect so the code is proven to react
    to a fresh injected change, not merely to already-present content."""
    path = root / 'skills' / 'proof-first' / 'SKILL.md'
    text = path.read_text(encoding='utf-8')
    if not text.endswith('\n'):
        text += '\n'
    text += '\n' + ' '.join(['filler'] * 2000) + '\n'
    path.write_text(text, encoding='utf-8')


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
    ('catalog-id-drift', "delete one PF data row from references/checklist.md's PF rules table", _mutate_catalog_id_drift),
    ('frontmatter-unparseable', "remove the opening '---' line from the real skills/proof-first/SKILL.md frontmatter block", _mutate_frontmatter_unparseable),
    ('frontmatter-unknown-key', "add an 'author:' key (outside the six-key allow-list) to the real skills/proof-first/SKILL.md frontmatter block", _mutate_frontmatter_unknown_key),
    ('frontmatter-name-mismatch', "change the real skills/proof-first/SKILL.md frontmatter's name value so it no longer equals its parent directory", _mutate_frontmatter_name_mismatch),
    ('frontmatter-description-invalid', "truncate the real skills/proof-first/SKILL.md frontmatter description to a few characters", _mutate_frontmatter_description_invalid),
    ('catalog-count-unstated', "delete the stated-count line from the real skills/proof-first/SKILL.md", _mutate_catalog_count_unstated),
    ('catalog-count-mismatch', "change the rule-count number in the real skills/proof-first/SKILL.md's stated-count line", _mutate_catalog_count_mismatch),
    ('skill-too-long', "append filler lines to the real skills/proof-first/SKILL.md past its 500-line ceiling", _mutate_skill_too_long),
    ('skill-token-budget-exceeded', "append filler words to the real skills/proof-first/SKILL.md, further increasing its already-over-ceiling estimated token count", _mutate_skill_token_budget_exceeded),
]


def mutation_test(repo_root):
    """Run a clean control copy, then one isolated mutation per violation
    code, and report per-code pass/fail. A code only counts as
    discrimination-proven when it was silent on the control copy and fires
    on its mutated copy -- silent-then-fires is what actually demonstrates
    the check can tell good content from bad. A code that already fires on
    the control copy cannot demonstrate that, even if it also fires after
    the mutation, so it is counted separately as confirmed-fire-only and
    never folded into the discrimination-proven total. This makes the
    tool's own printed claim state-independent: the comparison runs for
    every code regardless of whether the control happens to be clean, so a
    future drift back over a ceiling degrades what is printed instead of
    silently invalidating it. Returns True only when the control had no
    *unexpected* violations (KNOWN_OPEN_VIOLATIONS aside -- see that
    constant's own comment), every mutation fired its expected code, and
    every code in ALL_CHECK_CODES has a registered mutation. A
    confirmed-fire-only code does not by itself fail the run -- it makes
    the run disclose rather than fail."""
    all_ok = True
    discrimination_proven = set()
    fire_only = set()

    with tempfile.TemporaryDirectory(prefix='check-repo-mutation-control-') as tmp:
        control_root = Path(tmp) / 'control'
        _copy_repo_subset(repo_root, control_root)
        control_violations = run_all_checks(control_root)
        unexpected_control_violations = [
            v for v in control_violations
            if v[1].split(' ', 1)[0] not in KNOWN_OPEN_VIOLATIONS
        ]
        known_count = len(control_violations) - len(unexpected_control_violations)
        print(
            f"mutation-test CONTROL: {len(control_violations)} violations on the unmutated copy "
            f"({known_count} known-open per KNOWN_OPEN_VIOLATIONS, {len(unexpected_control_violations)} unexpected)"
        )
        if unexpected_control_violations:
            all_ok = False
        # The control copy is the identical pre-state for every mutation --
        # every scratch root below starts from the same _copy_repo_subset of
        # the same tree -- so this one control run is a sound pre-state for
        # all of them; no second control run per mutation is needed.
        control_codes = {v[1].split(' ', 1)[0] for v in control_violations}

    for code, description, mutate_fn in MUTATIONS:
        with tempfile.TemporaryDirectory(prefix=f'check-repo-mutation-{code}-') as tmp:
            scratch_root = Path(tmp) / 'scratch'
            _copy_repo_subset(repo_root, scratch_root)
            mutate_fn(scratch_root)
            violations = run_all_checks(scratch_root)
            fired = any(line.split(' ', 1)[0] == code for _, line in violations)
        if not fired:
            print(f"mutation-test FAIL: {code} {description}")
            all_ok = False
        elif code in control_codes:
            fire_only.add(code)
            print(
                f"mutation-test FIRE-ONLY: {code} {description} "
                f"(the control copy was already non-clean for this code, so this mutation "
                f"cannot demonstrate discrimination between good content and bad)"
            )
        else:
            discrimination_proven.add(code)
            print(f"mutation-test OK: {code} {description}")

    uncovered = [c for c in ALL_CHECK_CODES if c not in {m[0] for m in MUTATIONS}]
    for code in uncovered:
        print(f"mutation-test FAIL: {code} has no registered mutation")
        all_ok = False

    if all_ok:
        print(f"mutation-test PASS: {len(discrimination_proven)} codes discrimination-proven")
        if fire_only:
            print(
                f"mutation-test PASS: {len(fire_only)} codes confirmed-fire-only, not "
                f"discrimination-proven ({', '.join(sorted(fire_only))}) -- see the FIRE-ONLY "
                f"line above for each one's reason"
            )
    else:
        failed = len(ALL_CHECK_CODES) - len(discrimination_proven) - len(fire_only)
        print(f"mutation-test FAILED: {failed} codes not discrimination-proven")

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


def _good_skill():
    return "### PF-0.1 — Opening rule\n\nBody text for the opening rule.\n"


def _bad_skill():
    return "### PF-9.9 — Mutation-only rule\n\nBody text citing no registered ID.\n"


def _good_checklist():
    return """## PF rules

| ID | Rule |
|---|---|
| PF-0.1 | Opening rule |
"""


def _bad_checklist():
    return """## PF rules

| ID | Rule |
|---|---|
"""


def _good_frontmatter():
    return (
        "---\n"
        "name: good-skill\n"
        "description: |\n"
        f"  {'x' * DESCRIPTION_MIN}\n"
        "license: MIT\n"
        "metadata:\n"
        "  version: \"1.0.0\"\n"
        "---\n"
        "\n# Good skill\n\nBody text.\n"
    )


def _bad_frontmatter():
    """One root, three codes: an unknown 'author' key (not one of the six
    allowed keys -- 'compatibility' is allowed and deliberately not used
    here, see _mutate_frontmatter_unknown_key), a name that differs from
    its own directory, and a three-character description."""
    return (
        "---\n"
        "name: wrong-name\n"
        "description: hi\n"
        "author: Someone Else\n"
        "---\n"
        "\n# Bad skill\n\nBody text.\n"
    )


def _dupkey_frontmatter():
    return (
        "---\n"
        "name: dupkey-skill\n"
        "name: dupkey-skill-again\n"
        f"description: {'x' * (DESCRIPTION_MIN + 10)}\n"
        "---\n"
        "\n# Dup key skill\n\nBody text.\n"
    )


def _reordered_frontmatter():
    """The same allowed keys as _good_frontmatter, in a different order,
    still valid -- and its description is exactly DESCRIPTION_MAX
    characters, the upper boundary, which must also stay silent."""
    return (
        "---\n"
        "license: MIT\n"
        "metadata:\n"
        "  version: \"1.0.0\"\n"
        "description: |\n"
        f"  {'x' * DESCRIPTION_MAX}\n"
        "name: reordered-skill\n"
        "---\n"
        "\n# Reordered skill\n\nBody text.\n"
    )


def _overmax_frontmatter():
    """Description at DESCRIPTION_MAX + 1 -- the one character past the
    ceiling that must fire, isolated from every other frontmatter code."""
    return (
        "---\n"
        "name: overmax-skill\n"
        f"description: {'x' * (DESCRIPTION_MAX + 1)}\n"
        "---\n"
        "\n# Overmax skill\n\nBody text.\n"
    )


def _minimal_frontmatter_lines():
    """A valid, minimal frontmatter block (name equals 'proof-first',
    matching the directory every catalog/line-ceiling/token-budget fixture
    below uses) so those fixtures exercise only the one code each is built
    to test, with no incidental frontmatter-code noise."""
    return [
        '---',
        'name: proof-first',
        f"description: {'x' * DESCRIPTION_MIN}",
        '---',
        '',
    ]


def _skill_body_at_line_count(n, extra_lines):
    """Build a full SKILL.md fixture: valid minimal frontmatter, the given
    extra content lines, then trailing blank filler lines so the file's
    total line count is exactly n."""
    lines = _minimal_frontmatter_lines() + list(extra_lines)
    filler_needed = n - len(lines)
    if filler_needed < 0:
        raise ValueError('extra_lines already exceeds the requested line count')
    lines += [''] * filler_needed
    return '\n'.join(lines) + '\n'


_LINE_CEILING_HEADING = ['### PF-0.1 — Opening rule', '', 'Body text for the opening rule.']


def _skill_at_line_count(n):
    return _skill_body_at_line_count(n, _LINE_CEILING_HEADING)


def _numbering_for_catalog_count():
    return """## PF reserved ranges
| Section | Range | Concern | Allocated | Next free |
|---|---|---|---|---|
| PF-0 | PF-0.1-PF-0.9 | Opening | 1 | PF-0.2 |
| PF-1 | PF-1.1-PF-1.4 | Structure | 2 | PF-1.3 |

## Allocated IDs
| ID | Title | Defined in | Added in |
|---|---|---|---|
| PF-0.1 | Opening rule | SKILL.md | v1.0.0 |
| PF-1.1 | Rule one | SKILL.md | v1.0.0 |
| PF-1.2 | Rule two | SKILL.md | v1.0.0 |

## Deprecated IDs
| ID | Deprecated in | Absorbed by |
|---|---|---|
"""


def _checklist_for_catalog_count():
    return """## PF rules

| ID | Rule |
|---|---|
| PF-0.1 | Opening rule |
| PF-1.1 | Rule one |
| PF-1.2 | Rule two |
"""


def _catalog_count_extra_lines(count_line):
    lines = [
        '### PF-0.1 — Opening rule', '', 'Body text.', '',
        '### PF-1.1 — Rule one', '', 'Body text.', '',
        '### PF-1.2 — Rule two', '', 'Body text.', '',
    ]
    if count_line is not None:
        lines.append(count_line)
    return lines


def _good_catalog_count_skill():
    return _skill_body_at_line_count(
        60, _catalog_count_extra_lines('This catalog contains 3 rules in 2 numbered sections.'))


def _unstated_count_skill():
    return _skill_body_at_line_count(60, _catalog_count_extra_lines(None))


def _mismatched_count_skill():
    return _skill_body_at_line_count(
        60, _catalog_count_extra_lines('This catalog contains 5 rules in 2 numbered sections.'))


def _subblock_numbering():
    """A PF-2 sub-block table with a deliberate gap: Proof covers
    PF-2.1-PF-2.5 and Integrity covers PF-2.15-PF-2.20, leaving
    PF-2.6-PF-2.14 declared by neither. PF-2.10 sits inside PF-2's overall
    reserved range (so the pre-existing section-range test passes) but
    lands in that gap, so only the new sub-block containment test fires --
    the same technique _bad_numbering already uses for MC dimension
    blocks."""
    return """## PF reserved ranges
| Section | Range | Concern | Allocated | Next free |
|---|---|---|---|---|
| PF-2 | PF-2.1-PF-2.20 | Proof and Integrity | 1 | PF-2.11 |

## PF-2 sub-blocks
| Element | Range |
|---|---|
| Proof | PF-2.1-PF-2.5 |
| Integrity | PF-2.15-PF-2.20 |

## Allocated IDs
| ID | Title | Defined in | Added in |
|---|---|---|---|
| PF-2.10 | Gap-landing rule | SKILL.md | v1.0.0 |

## Deprecated IDs
| ID | Deprecated in | Absorbed by |
|---|---|---|
"""


def _token_budget_good_skill():
    return _skill_body_at_line_count(
        10, ['### PF-0.1 — Opening rule', '', 'Short body text, well under the token budget.'])


def _token_budget_bad_skill():
    filler_words = ' '.join(['word'] * 4200)
    return _skill_body_at_line_count(20, ['### PF-0.1 — Opening rule', '', filler_words])


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
        bad_catalog_root = tmp_root / 'bad_catalog'
        good_catalog_root = tmp_root / 'good_catalog'

        fm_good_root = tmp_root / 'fm_good'
        fm_bad_root = tmp_root / 'fm_bad'
        fm_dupkey_root = tmp_root / 'fm_dupkey'
        fm_reordered_root = tmp_root / 'fm_reordered'
        fm_overmax_root = tmp_root / 'fm_overmax'

        line500_root = tmp_root / 'line500'
        line501_root = tmp_root / 'line501'

        count_good_root = tmp_root / 'count_good'
        count_unstated_root = tmp_root / 'count_unstated'
        count_mismatch_root = tmp_root / 'count_mismatch'

        subblock_root = tmp_root / 'subblock'

        token_good_root = tmp_root / 'token_good'
        token_bad_root = tmp_root / 'token_bad'

        _write(bad_root / 'NUMBERING.md', _bad_numbering())
        _write(bad_root / 'skills' / 'SKILL.md', "See PF-9.9 and MC-1 for details.\n")
        _write(bad_root / 'examples' / 'deal-brief.md', _bad_deal_brief())
        _write(bad_root / 'examples' / 'scenario.md', "The deal is valued at $999,999 over the term.\n")
        _write(bad_root / 'NOTICES.md', _bad_notices())
        _write(bad_root / 'carrier-missing.md', "This file does not carry the pointer.\n")
        _write(bad_root / 'carrier-dup.md', "Test pointer string.\nSomething else.\nTest pointer string.\n")
        _write(bad_root / 'carrier-lookalike.md', "Test pointer string.\n")
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

        # Seventh/eighth roots isolate catalog-id-drift: bad_catalog_root's
        # SKILL.md defines PF-9.9 (no registry row anywhere) and its
        # checklist.md is missing PF-0.1 (registered in NUMBERING.md but
        # absent from the checklist) -- both divergence directions in one
        # fixture. good_catalog_root keeps all three files in agreement.
        _write(bad_catalog_root / 'NUMBERING.md', _good_numbering())
        _write(bad_catalog_root / 'skills' / 'proof-first' / 'SKILL.md', _bad_skill())
        _write(bad_catalog_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _bad_checklist())

        _write(good_catalog_root / 'NUMBERING.md', _good_numbering())
        _write(good_catalog_root / 'skills' / 'proof-first' / 'SKILL.md', _good_skill())
        _write(good_catalog_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _good_checklist())

        # Frontmatter fixtures (D-33): each root isolates its own code(s),
        # each written one level below skills/ so SKILL_GLOB matches.
        _write(fm_good_root / 'skills' / 'good-skill' / 'SKILL.md', _good_frontmatter())
        _write(fm_bad_root / 'skills' / 'actual-dir' / 'SKILL.md', _bad_frontmatter())
        _write(fm_dupkey_root / 'skills' / 'dupkey-skill' / 'SKILL.md', _dupkey_frontmatter())
        _write(fm_reordered_root / 'skills' / 'reordered-skill' / 'SKILL.md', _reordered_frontmatter())
        _write(fm_overmax_root / 'skills' / 'overmax-skill' / 'SKILL.md', _overmax_frontmatter())

        # Line-ceiling boundary fixtures (CAT-08): 500 lines stays silent,
        # 501 fires. Each carries a matching NUMBERING.md/checklist.md so
        # catalog-id-drift and the frontmatter codes stay silent, isolating
        # skill-too-long as the only code under test.
        _write(line500_root / 'NUMBERING.md', _good_numbering())
        _write(line500_root / 'skills' / 'proof-first' / 'SKILL.md', _skill_at_line_count(500))
        _write(line500_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _good_checklist())

        _write(line501_root / 'NUMBERING.md', _good_numbering())
        _write(line501_root / 'skills' / 'proof-first' / 'SKILL.md', _skill_at_line_count(501))
        _write(line501_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _good_checklist())

        # Stated-count fixtures (D-32): a self-contained 3-rule/2-section
        # registry, isolated from the real 31-rule catalog.
        _write(count_good_root / 'NUMBERING.md', _numbering_for_catalog_count())
        _write(count_good_root / 'skills' / 'proof-first' / 'SKILL.md', _good_catalog_count_skill())
        _write(count_good_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _checklist_for_catalog_count())

        _write(count_unstated_root / 'NUMBERING.md', _numbering_for_catalog_count())
        _write(count_unstated_root / 'skills' / 'proof-first' / 'SKILL.md', _unstated_count_skill())
        _write(count_unstated_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _checklist_for_catalog_count())

        _write(count_mismatch_root / 'NUMBERING.md', _numbering_for_catalog_count())
        _write(count_mismatch_root / 'skills' / 'proof-first' / 'SKILL.md', _mismatched_count_skill())
        _write(count_mismatch_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _checklist_for_catalog_count())

        # PF sub-block containment fixture (D-05): a gapped PF-2 sub-block
        # table with an allocated ID landing in the gap.
        _write(subblock_root / 'NUMBERING.md', _subblock_numbering())

        # Token-budget boundary fixtures (CAT-08 companion check).
        _write(token_good_root / 'NUMBERING.md', _good_numbering())
        _write(token_good_root / 'skills' / 'proof-first' / 'SKILL.md', _token_budget_good_skill())
        _write(token_good_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _good_checklist())

        _write(token_bad_root / 'NUMBERING.md', _good_numbering())
        _write(token_bad_root / 'skills' / 'proof-first' / 'SKILL.md', _token_budget_bad_skill())
        _write(token_bad_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _good_checklist())

        bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(bad_root)}
        good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(good_root)}
        unparseable_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(unparseable_root)}
        escaping_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(escaping_root)}
        bad_license_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(bad_license_root)}
        bad_frameworks_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(bad_frameworks_root)}
        bad_catalog_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(bad_catalog_root)}
        good_catalog_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(good_catalog_root)}

        fm_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(fm_good_root)}
        fm_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(fm_bad_root)}
        fm_dupkey_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(fm_dupkey_root)}
        fm_reordered_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(fm_reordered_root)}
        fm_overmax_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(fm_overmax_root)}

        line500_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(line500_root)}
        line501_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(line501_root)}

        count_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(count_good_root)}
        count_unstated_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(count_unstated_root)}
        count_mismatch_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(count_mismatch_root)}

        subblock_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(subblock_root)}

        token_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(token_good_root)}
        token_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(token_bad_root)}

        # Union the new roots' codes into the bad-code set so the coverage
        # loop below needs no edit -- it still just checks "did the code
        # fire on some known-bad fixture and stay silent on good_root".
        bad_codes |= (
            unparseable_codes | escaping_codes | bad_license_codes | bad_frameworks_codes
            | bad_catalog_codes | fm_bad_codes | fm_dupkey_codes | fm_overmax_codes
            | line501_codes | count_unstated_codes | count_mismatch_codes | subblock_codes
            | token_bad_codes
        )

        if 'catalog-id-drift' in good_catalog_codes:
            print("FAIL: catalog-id-drift fired on the known-good skill/checklist fixture")
            all_ok = False

        # Frontmatter-specific assertions.
        if FRONTMATTER_CHECK_CODES and set(FRONTMATTER_CHECK_CODES) & fm_good_codes:
            print("FAIL: a frontmatter code fired on the known-good frontmatter fixture")
            all_ok = False
        if set(FRONTMATTER_CHECK_CODES) & fm_reordered_codes:
            print("FAIL: a frontmatter code fired on the reordered-but-valid frontmatter fixture")
            all_ok = False
        if fm_bad_codes & {'frontmatter-unknown-key', 'frontmatter-name-mismatch', 'frontmatter-description-invalid'} != {
            'frontmatter-unknown-key', 'frontmatter-name-mismatch', 'frontmatter-description-invalid',
        }:
            print("FAIL: the bad frontmatter fixture did not fire all three of its expected codes")
            all_ok = False
        if 'frontmatter-unparseable' not in fm_dupkey_codes:
            print("FAIL: frontmatter-unparseable did not fire on the duplicate-key fixture")
            all_ok = False
        if 'frontmatter-description-invalid' not in fm_overmax_codes:
            print("FAIL: frontmatter-description-invalid did not fire one character past the ceiling")
            all_ok = False

        # Line-ceiling boundary assertions.
        if 'skill-too-long' in line500_codes:
            print("FAIL: skill-too-long fired at exactly the 500-line ceiling")
            all_ok = False
        if 'skill-too-long' not in line501_codes:
            print("FAIL: skill-too-long did not fire at 501 lines")
            all_ok = False

        # Stated-count assertions.
        if 'catalog-count-unstated' in count_good_codes or 'catalog-count-mismatch' in count_good_codes:
            print("FAIL: a catalog-count code fired on the known-good stated-count fixture")
            all_ok = False
        if 'catalog-count-unstated' not in count_unstated_codes:
            print("FAIL: catalog-count-unstated did not fire when the stated-count line is absent")
            all_ok = False
        if 'catalog-count-mismatch' not in count_mismatch_codes:
            print("FAIL: catalog-count-mismatch did not fire when the stated numbers disagree with the registry")
            all_ok = False

        # Sub-block containment assertion.
        if 'range-id' not in subblock_codes:
            print("FAIL: range-id did not fire for a PF ID landing in a gap between declared sub-blocks")
            all_ok = False

        # Token-budget boundary assertions.
        if 'skill-token-budget-exceeded' in token_good_codes:
            print("FAIL: skill-token-budget-exceeded fired on the known-good, low-word-count fixture")
            all_ok = False
        if 'skill-token-budget-exceeded' not in token_bad_codes:
            print("FAIL: skill-token-budget-exceeded did not fire on the high-word-count fixture")
            all_ok = False

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
