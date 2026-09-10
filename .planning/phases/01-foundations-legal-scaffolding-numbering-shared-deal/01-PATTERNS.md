# Phase 1 (Gap Closure): Pattern Map

**Mapped:** 2026-09-10
**Mode:** gap_closure — single file under modification: `tools/check_repo.py`
**Files analyzed:** 1 (all gap-closure edits land in this one file; no new files)
**Analogs found:** in-file analogs only (see below) — 3 of 5 requested patterns fully present, 2 partially present, 0 fully absent

## File Classification

| File | Role | Data Flow | Closest Analog | Match Quality |
|------|------|-----------|-----------------|----------------|
| `tools/check_repo.py` (patch `parse_notices()`) | utility / parser | file-I/O, transform | `parse_numbering()` / `parse_deal_brief()` in the same file | exact (same file, same idiom family) |
| `tools/check_repo.py` (patch `check_pointer()`) | utility / validator | transform, batch | `check_undefined_id()` in the same file | exact (fail-loud counter-example) |
| `tools/check_repo.py` (patch `check_unlisted_figure()`) | utility / validator | transform, batch | itself — the `in_canonical` state-flag idiom needs a bugfix, not a new analog | n/a (self-fix) |
| `tools/check_repo.py` (add `_good_notices()`/`_bad_notices()` variants) | test fixture | batch (self-test) | `_bad_deal_brief()` / `_good_deal_brief()` in the same file | exact |

There is exactly one file in scope. All "analogs" below are other functions inside `tools/check_repo.py` itself — this is a gap-closure run, not new-file scaffolding, so cross-file analog search does not apply per the adapted instructions.

## Pattern Assignments

### 1. A parser that tolerates prose between a heading and its content

**Working analog:** `parse_deal_brief()`, `tools/check_repo.py:227-240`, built on `split_sections()` (lines 58-75) and `table_rows()` (lines 78-90).

The house pattern never anchors a regex directly to the heading line. It splits the whole document into `{heading: body}` first, then scans the *body* for whatever structure it needs (a table, in this case), tolerating arbitrary prose in between:

```python
# tools/check_repo.py:58-75 — the shared section splitter every working parser uses
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
```

```python
# tools/check_repo.py:227-240 — parse_deal_brief() consumes the body, not the raw text
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
```

`parse_numbering()` (lines 97-134) follows the identical shape: `split_sections(text)` first, then `table_rows(sections.get('PF reserved ranges', ''))` — never a regex anchored to `## PF reserved ranges\s*\n`.

**The broken counter-pattern to replace**, `parse_notices()`, `tools/check_repo.py:315-331` (specifically the pointer-extraction line 318):

```python
# BROKEN — anchors the fence directly to the heading, fails when prose sits between them
def parse_notices(path):
    text = path.read_text(encoding='utf-8')
    pointer = None
    m = re.search(r'## Attribution pointer\s*\n+```[^\n]*\n(.*?)\n```', text, re.S)
    if m:
        pointer = m.group(1).strip()
    ...
```

**Fix direction implied by the house pattern:** get `sections['Attribution pointer']` via `split_sections(text)`, then search *within that body string* for the first fenced block (a body-scoped variant of `FENCE_RE`, `tools/check_repo.py:51`: `FENCE_RE = re.compile(r'```.*?```', re.S)`), rather than anchoring the fence to the heading in one combined regex. This is a straight transplant of the `parse_deal_brief`/`parse_numbering` idiom onto `parse_notices`.

### 2. A check function that fails loud on unparseable/missing input

**Working analog:** `check_undefined_id()`, `tools/check_repo.py:180-204` — it never returns `[]` just because upstream input is sparse; absence of an allocated ID is itself the condition that produces a violation:

```python
# tools/check_repo.py:180-204
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
```

Note the important distinction relevant to the gap: `run_id_checks()` (line 210-220) legitimately returns `[]` when `NUMBERING.md` itself is absent from the repo (D-15's "absence is not failure" rule, `01-CONTEXT.md` specifics section, line 119 of CONTEXT.md). That is a *file-level* absence short-circuit and is correct house style (mirrored by `run_figure_checks()` line 299-303, `run_notices_checks()` line 353-358 — all three gate on `path.exists()` before parsing). The bug is different: `check_pointer()` treats a *parse failure on an existing file* the same as a file-level absence.

**Broken counter-example**, `check_pointer()`, `tools/check_repo.py:334-347` (specifically line 336-337):

```python
# BROKEN — collapses "file absent" and "file present but unparseable" into the same silent no-op
def check_pointer(pointer, carriers, repo_root):
    violations = []
    if pointer is None:
        return violations
    for carrier in carriers:
        ...
```

**Fix direction implied by the house pattern:** once `NOTICES.md` exists on disk (already gated correctly by `run_notices_checks()` line 353-356, mirroring the other two `run_*_checks` gates), a `pointer is None` result must itself become a violation tuple (e.g. a new code such as `pointer-unparseable`, following the exact tuple/string shape documented below) — not a silent `return []`. This is the fail-loud discipline `check_undefined_id` already demonstrates: existence of the input file is the only legitimate reason to skip a check family; a malformed body inside an existing file is always violation material.

### 3. The violation-emission convention

Every check function returns a list of 2-tuples: `(subject, message_string)`, where `message_string` always begins with the violation code followed by a space, then a human-readable sentence naming the offending value and its location. Examples, verbatim:

```python
# tools/check_repo.py:148, 162, 168, 176, 203, 250, 257, 292, 344, 346
violations.append((id_, f"dup-id {id_} appears in {len(rows)} rows of the Allocated IDs table"))
violations.append((id_, f"range-id {id_} sits outside section {section}'s reserved range"))
violations.append((id_, f"range-id {id_} sits outside the MC reserved range"))
violations.append((row['id'], f"revived-id {row['id']} appears in both the Allocated IDs and Deprecated IDs tables"))
violations.append((tok, f"undefined-id {tok} cited in {rel} but not defined in the Allocated IDs table"))
violations.append((key, f"dup-figure-key {key} appears in {len(rows)} rows of the Canonical figures table"))
return [(keys[0], "figure-order the Canonical figures table's rows are not in ascending key order")]
violations.append((tok, f"unlisted-figure {tok} in {rel} has no matching Canonical figures row"))
violations.append((carrier, f"pointer-missing {carrier} does not contain the attribution pointer string"))
violations.append((carrier, f"pointer-duplicated {carrier} contains the attribution pointer string {count} times"))
```

**All existing codes** (module docstring, `tools/check_repo.py:16-39`, and `ID_CHECK_CODES`/`FIGURE_CHECK_CODES`/`NOTICES_CHECK_CODES`/`ALL_CHECK_CODES` at lines 207, 296, 350, 361): `dup-id`, `range-id`, `revived-id`, `undefined-id`, `dup-figure-key`, `figure-order`, `unlisted-figure`, `pointer-missing`, `pointer-duplicated`.

**Any new code the gap-closure plan introduces** (e.g. an "unparseable pointer definition" violation) must be:
1. Added to the module docstring's code list (lines 16-39) with the same one-line style.
2. Appended to `NOTICES_CHECK_CODES` (line 350) so `ALL_CHECK_CODES` (line 361) and the self-test's coverage assertion pick it up automatically.
3. Emitted as a `(subject, f"<code> <message>")` tuple, matching the exact convention above.

**How violations reach stdout and exit status**, `main()`, `tools/check_repo.py:525-542`:

```python
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()

    if args.self_test:
        ok = self_test()
        sys.exit(0 if ok else 1)

    violations = run_all_checks(REPO_ROOT)
    violations.sort(key=lambda v: (v[1].split(' ', 1)[0], v[0]))
    if not violations:
        print("check_repo: 0 violations")
        sys.exit(0)
    for _, line in violations:
        print(line)
    sys.exit(1)
```

Sort key is `(code, subject)` — derived by splitting the message string on the first space, i.e. the code prefix convention above is load-bearing for output ordering, not just documentation. Any new violation message must keep `<code> ` as the literal first token for this sort to keep working.

### 4. The `--self-test` fixture convention

**Working analog pair:** `_bad_deal_brief()` / `_good_deal_brief()`, `tools/check_repo.py:436-452` — inline heredoc-style strings returned by zero-arg functions, one engineered to trip every code in that family, one clean:

```python
# tools/check_repo.py:436-452
def _bad_deal_brief():
    return """## Canonical figures
| Key | Value | Type | What it is |
|---|---|---|---|
| total-contract-value | $6,000,000 | currency | Total contract value |
| bidder-count | 3 | count | Number of bidders |
| bidder-count | 4 | count | Duplicate key |
"""


def _good_deal_brief():
    return """## Canonical figures
| Key | Value | Type | What it is |
|---|---|---|---|
| bidder-count | 3 | count | Number of bidders |
| total-contract-value | $6,000,000 | currency | Total contract value |
"""
```

**The fixture that must be rewritten**, `_bad_notices()` / `_good_notices()`, `tools/check_repo.py:455-479` — currently the fence sits *immediately* under the heading, which is exactly the shape production `NOTICES.md` does not have (per the gap):

```python
# tools/check_repo.py:455-479 — CURRENT (does not mirror production shape; must be rewritten)
def _bad_notices():
    return """## Attribution pointer

```
Test pointer string.
```

### Files required to carry it

- `carrier-missing.md`
- `carrier-dup.md`
"""


def _good_notices():
    return """## Attribution pointer

```
Test pointer string.
```

### Files required to carry it

- `carrier-ok.md`
"""
```

**Fix direction:** insert a prose paragraph between `## Attribution pointer` and the fence in both fixtures, mirroring real `NOTICES.md`'s shape ("The following string is the canonical, verbatim attribution pointer..." per 01-CONTEXT.md and the verification report's own description). `_bad_notices()` should additionally cover the new fail-loud case — a variant (or a third fixture function, e.g. `_bad_notices_unparseable()`) where the fence is missing entirely or malformed, so the new violation code is exercised.

**How fixtures are registered and asserted**, `self_test()`, `tools/check_repo.py:482-522` (the registration block, lines 490-502, and the coverage assertion, lines 504-517):

```python
# tools/check_repo.py:490-502 — registration: write each fixture into a scratch dir tree
_write(bad_root / 'NUMBERING.md', _bad_numbering())
_write(bad_root / 'skills' / 'SKILL.md', "See PF-9.9 and MC-1 for details.\n")
_write(bad_root / 'examples' / 'deal-brief.md', _bad_deal_brief())
_write(bad_root / 'examples' / 'scenario.md', "The deal is valued at $999,999 over the term.\n")
_write(bad_root / 'NOTICES.md', _bad_notices())
_write(bad_root / 'carrier-missing.md', "This file does not carry the pointer.\n")
_write(bad_root / 'carrier-dup.md', "Test pointer string.\nSomething else.\nTest pointer string.\n")

_write(good_root / 'NUMBERING.md', _good_numbering())
_write(good_root / 'skills' / 'SKILL.md', "See PF-0.1 for details.\n")
_write(good_root / 'examples' / 'deal-brief.md', _good_deal_brief())
_write(good_root / 'NOTICES.md', _good_notices())
_write(good_root / 'carrier-ok.md', "Test pointer string.\n")
```

```python
# tools/check_repo.py:504-517 — coverage assertion: every code in ALL_CHECK_CODES must
# fire on bad_root and stay silent on good_root
bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(bad_root)}
good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(good_root)}

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
```

This is exactly the mechanism the gap exploits: a code is reported "covered" purely because it fires on `bad_root`/stays silent on `good_root`, with no check that the fixture's *document shape* matches production. The plan should treat this loop itself as correct and unchanged — the fix is entirely in making `_bad_notices()`/`_good_notices()` production-shaped, plus (if a new code is added) writing a fixture pair for it and adding the code to `ALL_CHECK_CODES` via `NOTICES_CHECK_CODES`.

### 5. The heading-scan / state-flag idiom (`in_canonical`) and its reset bug

**Location:** `check_unlisted_figure()`, `tools/check_repo.py:266-293`:

```python
# tools/check_repo.py:266-293
def check_unlisted_figure(figures, repo_root):
    canonical_values = {f['value'] for f in figures}
    examples_root = repo_root / 'examples'
    violations = []
    seen = set()
    if not examples_root.exists():
        return violations
    for f in sorted(examples_root.rglob('*.md')):
        text = strip_fences(f.read_text(encoding='utf-8'))
        lines = text.splitlines()
        in_canonical = False
        for line in lines:
            if re.match(r'^## Canonical figures\s*$', line):
                in_canonical = True
                continue
            if re.match(r'^## ', line):
                in_canonical = False
            if in_canonical or line.startswith('Last reviewed:'):
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
```

**The bug (WARNING, per verification report line 90/115):** `in_canonical` is set `True` when `## Canonical figures` is seen and only reset to `False` when a *subsequent* `## ` heading appears (line 281-282). If `## Canonical figures` is the last heading in the file, `in_canonical` stays `True` for every remaining line, including lines that fall *after* the table itself (e.g. a trailing `Last reviewed:` line is already special-cased at line 283, but any other stray prose or a second, unrelated figure appended after the table is silently skipped instead of scanned).

**No analog exists elsewhere in the file for the correct version of this idiom** — this is the only heading-scoped state-flag scan in `check_repo.py`; `split_sections()` (pattern 1 above) is the closest structurally-adjacent pattern but is a different technique (full section split, not an inline single-pass flag) and is not itself a stand-in for what a fixed `check_unlisted_figure` should do, because it discards line-level position within a section that `check_unlisted_figure` needs to preserve for accurate `line` iteration. State this to the planner explicitly: the fix here is a self-contained bugfix to the existing flag logic (e.g. bound the "in canonical table" state to line-level table-row shape — a line starting with `|` — rather than to "no `## ` heading has appeared yet since the marker," or track the table's end via blank-line/non-`|`-line termination), not a transplant from elsewhere in the file.

## Shared / House-Wide Constraints (apply to every gap-closure edit)

### Stdlib-only imports
**Source:** `tools/check_repo.py:41-45`
```python
import argparse
import re
import sys
import tempfile
from pathlib import Path
```
No third-party import may be added anywhere in `tools/`. The module docstring (lines 6-9) states this as a hard constraint tied to CI having no `pip install` step. Verified independently by the verification report ("Stdlib-only imports ... exit 0", line 85) via an `ast`-based scan — that scan is not itself present in `check_repo.py`; it appears to be a verifier-side check, not a repo artifact. **No analog exists in-repo for an import-purity self-check** — if the gap-closure plan is expected to add one, there is nothing to copy from; say so rather than invent a location.

### CI invocation — both modes must stay green
**Source:** `.github/workflows/ci.yml` (full file, 15 lines):
```yaml
name: check

on:
  push:
  pull_request:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Run checker self-test and live check
        run: |
          python3 tools/check_repo.py --self-test
          python3 tools/check_repo.py
```
Any new violation code, fixture, or parser behavior must keep `python3 tools/check_repo.py --self-test` exiting 0 (self_test() returns True, all `ALL_CHECK_CODES` covered) **and** `python3 tools/check_repo.py` exiting 0 against the real repo as shipped (i.e., once `parse_notices()`/`check_pointer()` are fixed, they must not newly flag the real, already-correct `NOTICES.md`/`README.md` pair as violating — the fix closes a false negative, it must not introduce a false positive against production content that the human-verification steps already confirmed is correct).

## No Analog Found

| Item | Reason |
|------|--------|
| A correct "in_canonical never resets at EOF" fix pattern elsewhere in the file | This is the only heading-scoped single-pass state-flag scan in `check_repo.py`; fix it in place, do not search for a transplant. |
| An import-purity self-check as a repo artifact | The verification report's "ast-based import scan" is verifier tooling, not something committed in `tools/`; if the plan wants one committed, it has no in-repo precedent to copy — flag this as new ground rather than a pattern match. |
| A new violation code for "unparseable pointer definition" | No existing code in `ALL_CHECK_CODES` covers "input file present but its required sub-structure is absent/malformed" as distinct from "row missing from a table" — `check_undefined_id`'s pattern is the closest transplant (see pattern 2) but the plan will be naming and wording a genuinely new code, not copying an existing one verbatim. |

## Metadata

**Analog search scope:** `tools/check_repo.py` (full file, 547 lines, read once, non-overlapping in-context) and `.github/workflows/ci.yml` (full file, 15 lines).
**Files scanned:** 2 (only two exist that are relevant; `git ls-files` confirms the rest of the repo per 01-CONTEXT.md's "reusable assets: none" note, since Phase 1 itself created every product file and CONTEXT.md already stated the repo was greenfield before this phase).
**Pattern extraction date:** 2026-09-10
