---
phase: 01-foundations-legal-scaffolding-numbering-shared-deal
reviewed: 2026-09-10T10:28:38Z
depth: standard
files_reviewed: 2
files_reviewed_list:
  - tools/check_repo.py
  - .github/workflows/ci.yml
findings:
  critical: 0
  warning: 2
  info: 2
  total: 4
status: issues_found
---

# Phase 01: Code Review Report (gap-closure re-review)

**Reviewed:** 2026-09-10T10:28:38Z
**Depth:** standard
**Files Reviewed:** 2 (`tools/check_repo.py`, `.github/workflows/ci.yml`)
**Status:** issues_found (2 warnings, 2 info — no blockers)

## Summary

This is a scoped re-review of exactly `git diff 3967b95..HEAD -- tools/check_repo.py .github/workflows/ci.yml`, covering gap-closure plans 01-05, 01-06, and 01-07. It replaces the prior `01-REVIEW.md` (git history `2b6f031`).

**Prior findings, resolved/deferred status:**

- **CR-01 (attribution-pointer dead code) — RESOLVED.** `parse_notices()` now splits the document into `{heading: body}` via `split_sections()` and searches for the fenced block inside the `## Attribution pointer` section body, matching the real `NOTICES.md` shape (heading → prose → fence). Verified against the actual `NOTICES.md`/`README.md` in this repo: `python3 tools/check_repo.py` finds the pointer, all four carrier entries parse, and the live run passes with 0 violations. A parse failure (missing/empty fence) now produces a `pointer-unparseable` violation (`tools/check_repo.py:428-432`) instead of a silent pass — the exact class of bug this phase was closing.
- **WR-01 (MC aggregate range) — RESOLVED.** `mc_ranges` is now a per-dimension `{name: (min, max)}` dict (`tools/check_repo.py:147-152`), and `check_range_id` requires membership in *some* block's range rather than one aggregate span (`tools/check_repo.py:205-209`). The self-test's `_bad_numbering()` fixture specifically exercises the gap case (`MC-6` sitting between the `Metric` block `1-5` and the `Economic Buyer` block `8-10`) and it correctly fires `range-id`. Production `NUMBERING.md`'s MC blocks are contiguous 1–40 today, so aggregate vs. per-block are behaviorally identical there — `MC-40` is confirmed still accepted (verified: live run and self-test both pass with the real file, whose ceiling is `MC-40`).
- **WR-02 (figure value-collision) — CONFIRMED DEFERRED, disclosure verified accurate.** `check_unlisted_figure` (`tools/check_repo.py:307-342`) still matches by formatted value with no key binding (`canonical_values = {f['value'] for f in figures}`, line 308). The docstring (lines 51-58) discloses this precisely, and `_good_deal_brief()`'s fixture (lines 743-754) pins the exact scenario (two rows sharing the `5%` value, then a prose line reusing `5%` for a different fact) as a demonstrated, accepted ceiling rather than an untested gap. No new finding raised here per the task's instruction not to re-litigate this deferral.

I additionally verified the two behavioral fixes and the mutation harness by direct execution rather than by reading alone:

```
python3 tools/check_repo.py            # check_repo: 0 violations, exit 0
python3 tools/check_repo.py --self-test   # PASS, all 10 codes covered
python3 tools/check_repo.py --mutation-test  # PASS, 10/10 codes proven live, control clean
git status --porcelain                 # unchanged after all three runs
```

No third-party imports were introduced (`argparse, re, shutil, sys, tempfile, pathlib` only), and `.github/workflows/ci.yml` still contains no `pip install` step — both hard constraints hold. `grep` for `repo_root /` usage confirms the unguarded-absolute-path pattern that caused the original `T-01-01` bug (`repo_root / carrier` silently discarding the base when `carrier` is absolute) exists at exactly one remaining call site (`tools/check_repo.py:412`), and that site is now gated by `_carrier_is_repo_relative()`. All other `repo_root /` joins use hardcoded literals, not document-sourced strings.

The two warnings below are residual gaps in that same carrier-path-handling code, found while specifically testing the boundaries the fix claims to close.

## Warnings

### WR-01: Carrier entry that resolves to a directory crashes the checker instead of producing a violation

**File:** `tools/check_repo.py:411-415`
**Issue:** `_carrier_is_repo_relative()` only rejects absolute paths, drive-letter paths, and `..` segments — it does not require the carrier to name a file. `check_pointer()` then does:
```python
p = repo_root / carrier
if not p.exists():
    continue
count = sum(1 for line in p.read_text(encoding='utf-8').splitlines() ...)
```
`Path.exists()` returns `True` for directories too. If a `NOTICES.md` "Files required to carry it" entry names an existing directory (e.g. `examples`, or even `.` — `_carrier_is_repo_relative('.')` returns `True` since `.` contains no `..` segment and isn't absolute, and `repo_root / '.'` is the repo root itself, which always exists), `p.read_text()` raises an unhandled `IsADirectoryError` and the entire check crashes with a traceback rather than reporting `pointer-missing`/`pointer-unparseable` or skipping gracefully. This is reachable by any future edit to `NOTICES.md`'s carrier list, not just malicious input — an easy documentation-editing mistake (someone lists a directory prefix instead of a file) turns the check itself into a CI outage instead of an actionable violation message.
**Fix:** Require `is_file()`, not just `exists()`, and treat a non-file match as a violation (or as "not repository-relative" alongside the existing `pointer-unparseable` reason):
```python
p = repo_root / carrier
if not p.is_file():
    continue
```
or, to make a directory entry loud rather than silently skipped like a genuinely-missing file:
```python
if p.exists() and not p.is_file():
    violations.append((carrier, f"pointer-unparseable {carrier} is a required-carrier entry that is not a file"))
    continue
if not p.exists():
    continue
```

### WR-02: `_carrier_is_repo_relative()` validates the path lexically, not the resolved target — a symlink can still escape the repository

**File:** `tools/check_repo.py:367-379`
**Issue:** The guard rejects `..` segments, leading `/`, `\`, and drive letters, but never resolves the path. If a carrier entry names a repository-relative path that is (or passes through) a symlink pointing outside `repo_root` — e.g. a file `link.md` committed as a symlink to `/etc/hosts`, listed in `NOTICES.md` as `- \`link.md\`` — `_carrier_is_repo_relative('link.md')` returns `True` (no `..`, not absolute), and `p = repo_root / 'link.md'` then `p.exists()` / `p.read_text()` follow the symlink and read the external target. The function's own docstring frames this as closing "T-01-01: pathlib's `/` operator silently discards the base for an absolute right-hand side" — that specific vector is closed, but the broader goal ("carrier stays inside the repository") is not fully achieved, because a lexically-relative path can still resolve outside the repo via a symlink. Concretely: a PR that adds both a symlink file and a matching `NOTICES.md` carrier entry in the same change would have the live check (and CI) read whatever the symlink points to. Impact here is bounded — `check_pointer` only counts matching lines and never echoes file content back into the check's output, so this is a denial-of-service/crash risk (e.g. a symlink to a device file or FIFO could hang `read_text()`) rather than a data-exfiltration one, and it requires a coordinated change to two files that would be visible in the same diff.
**Fix:** Resolve and contain-check instead of (or in addition to) the lexical rule:
```python
def _carrier_is_repo_relative(carrier, repo_root):
    if carrier.startswith('/') or carrier.startswith('\\'):
        return False
    if re.match(r'^[A-Za-z]:', carrier):
        return False
    parts = re.split(r'[\\/]', carrier)
    if '..' in parts:
        return False
    candidate = (repo_root / carrier)
    try:
        resolved = candidate.resolve(strict=False)
    except (OSError, ValueError):
        return False
    return resolved == repo_root or repo_root in resolved.parents
```
(This changes the function's signature; call sites in `run_notices_checks` would need `repo_root` threaded through.)

## Info

### IN-01: Dead defensive branch in `check_pointer`

**File:** `tools/check_repo.py:409-410`
**Issue:** `check_pointer(pointer, carriers, repo_root)` opens with `if pointer is None: return violations`. Its only caller, `run_notices_checks` (`tools/check_repo.py:430-432`), already returns the `pointer-unparseable` violation and never calls `check_pointer` when `pointer is None`. The branch is unreachable in the current call graph.
**Fix:** Either remove the guard (trust the caller's invariant) or add an `assert pointer is not None` to make the invariant explicit and catch future callers that don't uphold it, rather than silently returning `[]` (which would itself reintroduce a small false-green surface if a future call site forgets the precondition).

### IN-02: Mutation harness exercises only one of `pointer-unparseable`'s two trigger conditions

**File:** `tools/check_repo.py:602-606, 609-619`
**Issue:** `pointer-unparseable` fires for two distinct reasons (no usable fenced pointer, or a carrier entry that fails `_carrier_is_repo_relative`). `_mutate_pointer_unparseable` only exercises the first (removing the `## Attribution pointer` heading). The second reason (an escaping carrier entry) is covered by `self_test()`'s `_escaping_notices()` fixture instead, so the code as a whole is proven live by the combination of the two harnesses — this is not a coverage gap in the sense the phase was closing (no violation code is unproven), just an asymmetry between what each harness independently proves for a code with two branches.
**Fix:** Optional. If the mutation harness is meant to be the sole source of truth for "this code fires against real repository documents" (per its own module docstring at lines 462-470), consider adding a second `MUTATIONS` entry (e.g. `pointer-unparseable-carrier`) that injects a `../`-style entry into the real `NOTICES.md` copy, so both branches are proven against production document shape rather than one production-shape mutation plus one hand-built self-test fixture.

---

_Reviewed: 2026-09-10T10:28:38Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
