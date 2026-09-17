---
phase: 04-distribution-worked-examples
reviewed: 2026-09-17T00:00:00Z
depth: standard
files_reviewed: 7
files_reviewed_list:
  - tools/check_repo.py
  - tools/generate_derivatives.py
  - .claude-plugin/plugin.json
  - .claude-plugin/marketplace.json
  - .github/workflows/ci.yml
  - README.md
  - examples/before-after.md
findings:
  critical: 1
  warning: 3
  info: 0
  total: 4
status: issues_found
---

# Phase 4: Code Review Report

**Reviewed:** 2026-09-17T00:00:00Z
**Depth:** standard
**Files Reviewed:** 7
**Status:** issues_found

## Summary

Reviewed the two plugin manifests, the CI workflow, the README rewrite, the new
`examples/before-after.md` worked pairs, and the nine new `check_repo.py` violation codes plus
`generate_derivatives.py`. The gate itself is genuinely strong: `--self-test`, `--mutation-test`,
a live run, and `generate_derivatives.py --check` all pass, and the mutation harness proves
discrimination for all 9 new codes (verified by re-running all four gate commands directly).

Two classes of problem survived that gate anyway. First, a literal `</content>` tag is committed
at the end of `examples/before-after.md` — a tool-output artifact that leaked into shipped,
customer-facing example content and that no check in `check_repo.py` is positioned to catch
(confirmed: `check_repo.py` still reports 0 violations with the stray line present). Second, one
of the new checks (`publish-location-drift`'s owner-segment comparison) has a real false-positive
defect: it only correctly extracts a GitHub owner from an `https://github.com/...` URL. An SSH-style
(`git@github.com:owner/repo.git`) or scheme-less (`github.com/owner/repo`) value in any carrier
would be mis-parsed and reported as disagreeing with an equivalent `https://` value naming the same
repository, even though the two point at the same place. This is dormant today only because every
carrier in this repo currently uses the same placeholder `https://github.com/<owner>/<repo>` form.

## Critical Issues

### CR-01: Stray `</content>` tag committed in shipped example file, uncaught by the gate

**File:** `examples/before-after.md:37`
**Issue:** The file's last line is the literal text `</content>` — a wrapper tag that leaked from
whatever tool produced the file (an agent-response or document-writer artifact), not part of the
"Demo and discovery material" section it trails. Confirmed present with `grep -n '</content>' examples/before-after.md`.
This file is explicitly the source the README's "Before and after" section is "reproduced from"
(README.md:19), so the defect sits directly behind a public-facing document meant to demonstrate
the skill's own quality bar — an evaluator who opens the raw file sees a broken artifact tag at
the bottom of the one file this project uses to sell itself.
It is not cosmetic-only: it also demonstrates a gap in the gate. None of the nine new Phase 4
checks (or any pre-existing check) is positioned to catch a trailing non-content line like this —
`check_before_after_families`/`check_before_after_citations` only look for required headings,
`✗`/`✓` lines, and citation tokens inside `split_sections()`'s per-heading bodies; a stray line
appended after the last section's real content is silently absorbed into that section's body and
never inspected against anything. Re-running `python3 tools/check_repo.py` with this line present
still reports `0 violations`, confirming the gate does not see it.
**Fix:** Remove the stray line.
```diff
 Rules applied: PF-3.3, PF-2.14, MC-31.
-</content>
```
Optionally, harden the gate: `check_before_after_families` (and the equivalent guard on `README.md`
and any other file assembled by a generation tool) could reject a document whose raw text (before
`strip_fences()`) contains an unmatched `<` / `</...>` tag-like token that isn't part of a fenced
code block — a cheap regex tripwire (e.g. `re.search(r'</?\w+>', text_outside_fences)`) would have
caught exactly this class of leak without becoming a general HTML/XML validator.

## Warnings

### WR-01: `publish-location-drift`'s owner-segment extraction false-positives on non-`https://` GitHub URLs

**File:** `tools/check_repo.py:2268-2278` (`_owner_segment`), used by `_publish_locations_in` at `tools/check_repo.py:2296-2320`
**Issue:** `_owner_segment` only strips a literal `'https://github.com/'` prefix; any other valid
way of writing the same repository — an SSH remote (`git@github.com:owner/repo.git`, as `git remote -v`
commonly prints) or a scheme-less form (`github.com/owner/repo`) — is left unstripped and then
split on the first `/`, producing a garbage "owner" that will never equal the owner extracted from
an `https://` carrier for the *same* repository. Verified directly:
```
>>> _owner_segment("https://github.com/acme/proof-first")
'acme'
>>> _owner_segment("git@github.com:acme/proof-first.git")
'git@github.com:acme'
>>> _owner_segment("github.com/acme/proof-first")
'github.com'
```
If a contributor ever edits `plugin.json`'s `repository` field to the SSH form (a common
copy-paste from `git remote -v`) while `marketplace.json`/README.md keep the `https://` form, this
check fires `publish-location-drift` even though every carrier names the same repository —
a false CI failure over a distinction the check's own declared ceiling never claims to make (it
promises to compare "the GitHub account/org segment," not to fail on legitimate alternate URL
syntaxes for the same segment). Currently dormant only because every existing carrier
(`plugin.json`, `marketplace.json`, `README.md`) uses the identical placeholder
`https://github.com/<owner>/<repo>` form.
**Fix:** Normalize more URL forms before comparing, e.g.:
```python
def _owner_segment(value):
    v = value.strip()
    for prefix in ('https://github.com/', 'http://github.com/', 'github.com/'):
        if v.startswith(prefix):
            v = v[len(prefix):]
            break
    else:
        m = re.match(r'^git@github\.com:(.+)$', v)
        if m:
            v = m.group(1)
    v = v.rstrip('/')
    return v.split('/', 1)[0] if v else v
```

### WR-02: `generate_derivatives.py --check` docstring promises byte-for-byte comparison; implementation is text-mode with newline normalization, and `write_derivatives` does not pin output newlines

**File:** `tools/generate_derivatives.py:33-37` (docstring), `:226-264` (`write_derivatives`/`check_derivatives`)
**Issue:** The module docstring states `--check` will "[r]ender both derivatives in memory and
compare them byte for byte against the committed files." The actual implementation
(`check_derivatives`, line 251) does `actual_text = path.read_text(encoding='utf-8')` and compares
it to `expected_text` (a `str`, not `bytes`) with `!=`. `Path.read_text()` uses Python's universal-newline
translation, so a committed file containing `\r\n` line endings reads back identically to one
containing `\n` — the comparison is not byte-for-byte, contrary to the docstring, and a
line-ending-only divergence would silently pass `--check`.
This is not purely theoretical: `write_derivatives` (line 234) calls
`path.write_text(text, encoding='utf-8')` with no `newline=''` argument, so on a platform where
`os.linesep` is `\r\n` (Windows), regenerating the derivatives would write `\r\n`-terminated files —
different bytes than the LF-terminated files this Linux-CI repository currently ships — while
`--check` (by the same read-side normalization) would report them as matching. This undercuts the
freshness guarantee `check_repo.py`'s `skill-derivative-stale` and this script's own `--check` are
described as providing together as "a second, independent guard" (module docstring, generate_derivatives.py:22-25):
the guard that is supposed to catch a hand-edited or platform-drifted derivative cannot see a
line-ending-only difference.
**Fix:** Either compare bytes directly, or pin the write side to `\n` so bytes stay canonical
everywhere:
```python
# check_derivatives
actual_bytes = path.read_bytes()
expected_bytes = expected_text.encode('utf-8')
if actual_bytes != expected_bytes: ...

# write_derivatives
path.write_text(text, encoding='utf-8', newline='\n')
```
Update the docstring to match whichever guarantee is actually implemented.

### WR-03: Plugin manifest checks silently assume exactly one `skills/*/SKILL.md`; multi-skill repos get weaker coverage with no violation raised

**File:** `tools/check_repo.py:2144-2149` (`check_plugin_manifest_version`), `:2218-2226` (`check_plugin_manifest_invalid`)
**Issue:** `check_plugin_manifest_version` resolves the "source of truth" skill version by iterating
`sorted(repo_root.glob(SKILL_GLOB))` and taking the *first* skill that states a
`metadata.version`, then `break`s — if a future repo state ships more than one skill folder with
different versions, only the alphabetically-first one is ever compared, and disagreement among the
skills themselves (or between the manifest and a *different* skill than the one chosen) is never
surfaced. `check_plugin_manifest_invalid`'s folder-name-equality check is guarded by
`if 'name' in plugin_data and len(skill_dirs) == 1:` (line 2219) — with zero or more than one
skill folder present, the name-equality check is skipped entirely rather than flagged as
unverifiable, so `plugin.json`'s `name` could disagree with every shipped skill folder and no
`plugin-manifest-invalid` violation would fire. Neither function's docstring discloses this
as a stated ceiling (contrast with the module's usual practice of naming exactly what a check
does not cover). Currently inert because this repository ships exactly one skill, but it is a
real blind spot in code whose stated purpose is exactly this kind of cross-file consistency
guarantee, and the repository's own stack (Agent Skills standard, marketplace `plugins: []` array)
structurally permits more than one.
**Fix:** At minimum, state the one-skill assumption as a declared ceiling in both docstrings
(matching this file's established convention elsewhere in the module), e.g. "this check compares
against the first skill folder in sorted order and is not evaluated for correctness against a
second or subsequent skill folder." Better: make `check_plugin_manifest_invalid` emit a
`plugin-manifest-invalid` violation when `len(skill_dirs) != 1` and `name` is present, naming the
ambiguity, and make `check_plugin_manifest_version` fire when more than one skill states a
version and they disagree with each other, not only against the manifest.

---

_Reviewed: 2026-09-17T00:00:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
