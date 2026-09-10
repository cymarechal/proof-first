---
phase: 01-foundations-legal-scaffolding-numbering-shared-deal
reviewed: 2026-09-10T07:15:29Z
depth: standard
files_reviewed: 8
files_reviewed_list:
  - .github/workflows/ci.yml
  - LICENSE
  - NOTICES.md
  - NUMBERING.md
  - README.md
  - SOURCES.md
  - examples/deal-brief.md
  - tools/check_repo.py
findings:
  critical: 1
  warning: 2
  info: 0
  total: 3
status: issues_found
---

# Phase 01: Code Review Report

**Reviewed:** 2026-09-10T07:15:29Z
**Depth:** standard
**Files Reviewed:** 8
**Status:** issues_found

## Summary

This phase's actual documents (`NOTICES.md`, `SOURCES.md`, `NUMBERING.md`, `examples/deal-brief.md`, `README.md`) are internally consistent and well-hedged: the legal statements are properly non-affiliating and paraphrase-scoped, no proprietary text or invented legal citations are present, the attribution pointer is byte-identical between `NOTICES.md` and `README.md` and appears exactly once, `NUMBERING.md`'s reserved ranges are arithmetically self-consistent, and `README.md` makes no unreproducible measured claim. CI genuinely wires `--self-test` and the live check into the build with fail-closed shell semantics.

The problem is in the enforcement layer itself. `tools/check_repo.py`'s attribution-pointer parser (`parse_notices`) cannot handle the real `NOTICES.md`'s actual prose structure (a paragraph of explanatory text sits between the `## Attribution pointer` heading and the fenced code block), so it silently fails to extract the pointer and returns zero violations regardless of what `README.md` (or any future carrier) actually contains. This was verified empirically: deleting the entire attribution pointer paragraph from a copy of `README.md` and re-running the checker's own `run_notices_checks()` against it still returns no violations. The `--self-test` fixtures for this exact check use a NOTICES.md structure (fence immediately following the heading, no intervening paragraph) that does not match production `NOTICES.md`, so this hole passes CI silently — this is exactly the class of false-negative the project's own registry-consistency goal depends on catching. This is a Critical/blocker finding because every later phase (including when the skill's `SKILL.md` and reference files are added as required carriers) trusts this checker to catch a missing or duplicated pointer, and right now it cannot.

A second, lower-severity finding: the MC ID range check validates allocated MC IDs against one aggregated `(min, max)` across all eight dimension blocks rather than each block's own reserved sub-range, unlike the PF check which is correctly scoped per section. This is currently harmless because the blocks are contiguous with no gaps, but it diverges from the tool's own docstring and from a future range-widening scenario the project's versioning rules explicitly anticipate.

## Critical Issues

### CR-01: Attribution-pointer check is silently inert against the real NOTICES.md

**File:** `tools/check_repo.py:315-331` (`parse_notices`), consumed by `check_pointer` at `tools/check_repo.py:334-347`

**Issue:** `parse_notices` extracts the canonical pointer string with:

```python
m = re.search(r'## Attribution pointer\s*\n+```[^\n]*\n(.*?)\n```', text, re.S)
```

This requires the fenced code block to begin immediately after the heading, separated only by whitespace (`\s*\n+`). The real `NOTICES.md` (lines 24-32) has an explanatory prose paragraph between the heading and the fence:

```
## Attribution pointer

The following string is the canonical, verbatim attribution pointer. A human contributor and
`tools/check_repo.py` both read this fenced block as the single source of truth for the string —
neither restates it from memory.

```
Concepts here are paraphrased from publicly described sales frameworks. ...
```
```

Because `\s*` cannot match the prose text, the regex fails to match at all, `pointer` is set to `None`, and `check_pointer` immediately returns `[]` for a `None` pointer (`tools/check_repo.py:336-337`) — meaning `pointer-missing` and `pointer-duplicated` never fire against the live repository, no matter what `README.md` or any future carrier file (e.g. `skills/proof-first/SKILL.md` once it exists) actually contains.

Verified empirically against this checkout:
- `python3 -c "import re; print(re.search(r'## Attribution pointer\s*\n+\`\`\`[^\n]*\n(.*?)\n\`\`\`', open('NOTICES.md').read(), re.S))"` → `None`.
- Running `check_repo.run_notices_checks()` against a temp copy of the repo with the entire attribution-pointer line stripped from `README.md` still returns `[]` (zero violations) — i.e. the safety net does not fire even when the exact defect it exists to catch is injected.

The `--self-test` fixtures (`_bad_notices()` / `_good_notices()`, `tools/check_repo.py:455-479`) place the fence immediately after the heading with no intervening paragraph, so they exercise a document shape that does not match production `NOTICES.md`. This is why `--self-test` reports `pointer-missing`/`pointer-duplicated` as "covered" while the live check on the real file is dead code.

**Fix:** Make the extraction tolerant of prose between the heading and the fence, and make the parser fail loudly (not silently) if it cannot find a pointer at all, since an unparseable pointer definition is itself a defect that should block CI:

```python
def parse_notices(path):
    text = path.read_text(encoding='utf-8')
    pointer = None
    section = re.search(r'## Attribution pointer\b(.*?)(?=\n## |\Z)', text, re.S)
    if section:
        fence = re.search(r'```[^\n]*\n(.*?)\n```', section.group(1), re.S)
        if fence:
            pointer = fence.group(1).strip()
    return pointer, carriers  # (carrier parsing unchanged)
```

And in `run_notices_checks`, treat a `None` pointer as a hard violation rather than an early return:

```python
def run_notices_checks(repo_root):
    notices_path = repo_root / 'NOTICES.md'
    if not notices_path.exists():
        return []
    pointer, carriers = parse_notices(notices_path)
    if pointer is None:
        return [('NOTICES.md', 'pointer-unparseable NOTICES.md defines no extractable attribution pointer fence')]
    return check_pointer(pointer, carriers, repo_root)
```

Also add a `--self-test` fixture whose `NOTICES.md` mirrors the real file's shape (heading, prose paragraph, then fence) so a future regression of this exact kind is caught by CI instead of merely by manual inspection.

## Warnings

### WR-01: MC ID range check enforces one aggregate range instead of per-dimension-block ranges

**File:** `tools/check_repo.py:97-134` (`parse_numbering`), `tools/check_repo.py:152-169` (`check_range_id`)

**Issue:** For PF IDs, `check_range_id` looks up the specific section's own `(min, max)` (`pf_ranges.get(section)`), correctly scoping the check per section. For MC IDs, `parse_numbering` instead flattens all eight dimension blocks into a single `mc_range = (min(mc_nums), max(mc_nums))` (`tools/check_repo.py:108-111`), and `check_range_id` validates every `MC-<n>` against that one aggregate range (`tools/check_repo.py:164-168`).

This currently produces correct results only because the eight MC blocks in `NUMBERING.md` are contiguous with no gaps (`MC-1-MC-5`, `MC-6-MC-10`, ..., `MC-36-MC-40`), so any ID in `[1, 40]` happens to fall inside some declared block. But this diverges from the tool's own docstring ("range-id - an allocated ID sits outside its section's **or dimension block's** reserved range", `tools/check_repo.py:19-20`) and from `NUMBERING.md`'s "Range exhaustion" section, which states dimension blocks are independently enforced. `NUMBERING.md`'s own versioning rules explicitly anticipate future range widening ("Widening a range is a major-version action recorded in this file"); if a future widening ever introduces a gap between two MC blocks (as opposed to extending the ceiling), an ID landing in that gap would be silently accepted by the aggregate-range check even though it belongs to no declared block.

**Fix:** Parse MC ranges per dimension (keyed by dimension label, mirroring `pf_ranges`) and validate each `MC-<n>` against the specific block whose range contains it, or explicitly document (and accept, in a code comment) that MC is deliberately checked only against the aggregate ceiling because blocks are guaranteed contiguous:

```python
mc_ranges = {}
for row in table_rows(sections.get('MC reserved blocks', '')):
    dim = row[0].strip()
    nums = [int(n) for n in re.findall(r'MC-(\d+)', row[1])]
    if len(nums) >= 2:
        mc_ranges[dim] = (min(nums), max(nums))
...
# in check_range_id:
if mc_ranges and not any(lo <= n <= hi for lo, hi in mc_ranges.values()):
    violations.append(...)
```

### WR-02: `unlisted-figure` check matches by raw value string, not by key/context, so a new figure can silently collide with an unrelated existing canonical value

**File:** `tools/check_repo.py:266-293` (`check_unlisted_figure`)

**Issue:** `check_unlisted_figure` builds `canonical_values = {f['value'] for f in figures}` — a flat set of value strings with no association to which key they came from — and flags a currency/percent/date token in `examples/**/*.md` only if the literal string is entirely absent from that set (`tools/check_repo.py:267, 287`). If a future edit to `examples/` introduces a genuinely new fact whose formatted value happens to equal an already-canonical value used for a *different* concept (e.g. a new "20%" figure that has nothing to do with `rfp-security-weight`, or a new "$6,000,000" cost unrelated to `total-contract-value`), the checker will treat it as already covered and report zero violations, even though no row in the Canonical figures table actually backs that new fact. This is a materially different (and undisclosed) gap from the tool's own stated "bare counts are not detected" ceiling (`tools/check_repo.py:33-34`) — that one is documented; this value-collision blind spot is not.

**Fix:** At minimum, disclose this limitation in the docstring alongside the bare-count ceiling. If stronger guarantees are wanted, require each canonical figure's value to appear in the surrounding sentence adjacent to a citation of its key (or a comment marker), or track which examples-file line consumed which canonical row so an unused/misattributed match can be flagged separately — either would move this from "any string with this value already exists somewhere" to "this specific fact is accounted for."

---

_Reviewed: 2026-09-10T07:15:29Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
