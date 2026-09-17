# Phase 4: Distribution & Worked Examples - Pattern Map

**Mapped:** 2026-09-17
**Files analyzed:** 9 (from RESEARCH.md's Wave 0 Gaps and Recommended Project Structure)
**Analogs found:** 9 / 9 (all tracked-source; verified via `git ls-files`)

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `.claude-plugin/plugin.json` | config | transform (static manifest) | `~/devoteam/.claude/plugins/marketplaces/simple-english/.claude-plugin/plugin.json` (external, read-only reference — **not a repo file to cite as an analog path**; see note below) | role-match, content-template only |
| `.claude-plugin/marketplace.json` | config | transform | same SimpleEnglish file, `marketplace.json` | role-match, content-template only |
| `output-styles/proof-first.md` | config/generated-artifact | transform (batch, generated) | none in-repo (new artifact type); nearest in-repo shape is `skills/proof-first/SKILL.md`'s frontmatter+prose shape | no exact analog — new pattern, see "No Analog Found" |
| `prompts/system-prompt.md` | config/generated-artifact | transform (batch, generated) | same — no in-repo analog | no exact analog |
| `tools/generate_derivatives.py` | utility | transform/file-I/O, batch | `tools/check_repo.py` (script conventions, stdlib-only discipline, docstring-states-ceiling convention) and `evals/conformance/run_conformance.py` (argparse/self-test/usage-doc shape) | strong role-match |
| `examples/before-after.md` | content/fixture | transform (static content) | `skills/proof-first/references/worked-examples.md` (per-rule ✗/✓ pairs — different granularity, same visual grammar) | role-match, different unit |
| `tools/check_repo.py` (modified — add 4-6 codes) | utility/config-validator | CRUD (registry consistency), request-response (CLI) | itself — extend using `check_catalog_count`/`check_mc_count` (lines 1400-1428) and `check_artifact_family_sections` (lines 1487-1544) as templates | exact — same file, established idiom |
| `README.md` (modified) | content | transform (static doc) | itself — existing Status/Install-adjacent sections | exact — same file |
| `.github/workflows/ci.yml` (possibly modified) | config | event-driven (CI trigger) | itself | exact — same file |

**Note on the plugin manifest analogs:** `~/devoteam/.claude/plugins/marketplaces/simple-english/.claude-plugin/plugin.json` and `marketplace.json` are **outside this repository** (a separate, unrelated marketplace checkout on the local machine, not a submodule or gitignored mirror of this repo's own tracked tree). The tracked-source gate does not apply to them the way it applies to intra-repo mirrors — they are simply an external reference implementation this project's own CLAUDE.md and RESEARCH.md explicitly cite as the field-shape template. There is no in-repo analog for these two files because this repo has never had a `.claude-plugin/` directory (`git ls-files -- .claude-plugin` returns nothing). Do not invent an in-repo path for them; cite the external path exactly as RESEARCH.md does, and note plainly in the plan that it is an external reference, not a repo file being modified.

## Pattern Assignments

### `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` (config, transform)

**Analog (external reference, not in-repo):** `~/devoteam/.claude/plugins/marketplaces/simple-english/.claude-plugin/{plugin,marketplace}.json`, read directly and quoted verbatim in `04-RESEARCH.md` Pattern 1 (lines 180-220 of that file).

**Template to copy field-for-field** (verified verbatim in RESEARCH.md, cross-checked against the official schema fetch):
```json
// plugin.json
{
  "name": "proof-first",
  "displayName": "Proof First",
  "description": "<from SKILL.md frontmatter description, trimmed to plugin-manifest scope>",
  "version": "0.1.0",
  "author": { "name": "<TBD>" },
  "homepage": "<placeholder — see Pitfall 4>",
  "repository": "<placeholder — see Pitfall 4>",
  "license": "MIT",
  "keywords": ["presales", "rfp", "proposal", "technical-writing"]
}
```
```json
// marketplace.json
{
  "name": "proof-first",
  "owner": { "name": "<TBD>", "url": "<placeholder>" },
  "description": "<one-line, matches plugin.json>",
  "plugins": [
    {
      "name": "proof-first",
      "source": "./",
      "displayName": "Proof First",
      "description": "...",
      "version": "0.1.0",
      "author": { "name": "<TBD>" },
      "homepage": "<placeholder>",
      "repository": "<placeholder>",
      "license": "MIT",
      "keywords": [ "..." ]
    }
  ]
}
```

**Version source of truth:** `skills/proof-first/SKILL.md` frontmatter, lines 1-14 (read this session, verbatim):
```yaml
---
name: proof-first
description: |
  Write or check RFP and RFI responses, solution proposals, executive
  summaries, and demo or discovery documents for technical presales and
  bid teams. ...
license: MIT
metadata:
  version: "0.1.0"
---
```
The version lives at `metadata.version` (a nested map key), NOT a top-level frontmatter key. `plugin.json`'s and `marketplace.json`'s plugin-entry `version` fields must equal this string exactly (`"0.1.0"` as of this session). `NUMBERING.md:143-149` (quoted below under Shared Patterns) is the authority for this obligation.

**Parsing note for the new checker code:** the repo's frontmatter parser (`parse_frontmatter()`, referenced by D-33 in `check_catalog_count`'s docstring) keeps nested-map values as opaque strings — a small, targeted regex extraction of the `metadata:` block's `version:` sub-key is needed, not a general YAML parser. `.claude-plugin/*.json` files, by contrast, are genuine JSON — use stdlib `json.loads()` directly (per RESEARCH.md's "Don't Hand-Roll" table), never a hand-rolled parser for those.

---

### `tools/check_repo.py` — new codes (utility, CRUD/registry-consistency)

**This is a single file being extended, not a new file.** Every new code must follow the exact three-part contract every existing code already uses: (1) a check function registered so `run_all_checks()` calls it, (2) a `--self-test` fixture pair (a "bad" root that must trip the code, a "good"/silent root that must not), (3) a `MUTATIONS` entry.

**Template A — stated-value-vs-registry check** (mirror for `plugin-manifest-version-mismatch`), verified verbatim at `tools/check_repo.py:1400-1428` (line range in RESEARCH.md confirmed exact on this read):
```python
COUNT_SENTENCE_RE = re.compile(r'^This catalog contains (\d+) rules in (\d+) numbered sections\.$')

def check_catalog_count(allocated, repo_root):
    """For each skill file, require exactly the frozen stated-count
    template and require its two numbers to match the registry..."""
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
```
Apply the same shape for `plugin-manifest-version-mismatch`: parse `SKILL.md`'s `metadata.version` (stated), parse `.claude-plugin/plugin.json` and `marketplace.json`'s `version` fields (registry-equivalent), compare, fire once per mismatched file naming both values. Absence of `.claude-plugin/` should not be a violation until this phase creates it (mirrors the "absence of the file is not a violation" declared-ceiling convention already used by `check_catalog_count` and `check_artifact_family_sections`).

**Template B — section-presence check** (mirror for `before-after-family-missing`), verified verbatim at `tools/check_repo.py:1487-1544` (line range in RESEARCH.md confirmed exact on this read):
```python
ARTIFACT_FAMILY_SECTIONS = (
    # Frozen interface (P3-11) -- do not reword, re-case, pluralise, or
    # reorder these four strings. ...
    'RFP and RFI response',
    'Solution proposal',
    'Executive summary',
    'Demo and discovery material',
)

ARTIFACT_FAMILY_REQUIREMENT = {
    'RFP and RFI response': 'ART-01',
    'Solution proposal': 'ART-02',
    'Executive summary': 'ART-03',
    'Demo and discovery material': 'ART-04',
}

def check_artifact_family_sections(repo_root):
    """For each installed skill folder ... whose references/artifact-patterns.md
    exists, require all four frozen artifact-family section headings ...
    Return no violations for a folder whose references/artifact-patterns.md
    does not exist, checked before any read -- the same declared ceiling ...
    Declared ceiling: this check is heading presence only. ..."""
    violations = []
    for skill_path in sorted(repo_root.glob(SKILL_GLOB)):
        patterns_path = skill_path.parent / 'references' / 'artifact-patterns.md'
        if not patterns_path.exists():
            continue
        rel = patterns_path.relative_to(repo_root)
        text = strip_fences(patterns_path.read_text(encoding='utf-8'))
        sections = split_sections(text)
        for heading in ARTIFACT_FAMILY_SECTIONS:
            if heading not in sections:
                requirement = ARTIFACT_FAMILY_REQUIREMENT[heading]
                violations.append((str(rel), (
                    f"artifact-family-section-missing {rel} is missing the "
                    f"required '## {heading}' section, which {requirement} requires"
                )))
    return violations
```
Apply the same shape for `before-after-family-missing`, checking `examples/before-after.md` against the SAME `ARTIFACT_FAMILY_SECTIONS` tuple — **import/reuse it, do not redeclare a second copy** (RESEARCH.md's "Don't Hand-Roll" table is explicit on this: this frozen four-string tuple is a shared interface already bound by SKILL.md's classification instruction and Phase 5's linter). `before-after-citation-missing` is a small variant: for each family section's body, require at least one `PF-\d+\.\d+` or `MC-\d+` token — reuse the same regex `check_undefined_id` already uses rather than declaring a third copy of an ID-shape regex.

**`skill-derivative-stale`** — a third variant of Template A, but with a `hashlib.sha256` recomputation instead of a stated-count parse: for each derivative file (`output-styles/proof-first.md`, `prompts/system-prompt.md`) that carries a leading HTML-comment hash stamp, recompute `hashlib.sha256` over the current concatenated bytes of `SKILL.md` + the three depended-on reference files, compare to the stamped hash, fire on mismatch or on a missing header for a file that exists.

**Self-test fixture conventions**, verified at `tools/check_repo.py:3223-3342` (function `self_test()`): each new code needs its own pair of scratch roots under a shared `tempfile.TemporaryDirectory`, e.g. `family_good_root = tmp_root / 'family_good'` / `family_bad_root = tmp_root / 'family_bad'` (exact naming style used for the sibling `artifact_good_root`/`artifact_bad_root` pair at lines 3267-3268). Write minimal fixture content with the module's `_write()` helper. The "bad" root must trip exactly the new code; the "good" root must stay silent on it (and ideally on every other code too, verified by the existing `good_root`/`good_catalog_root` composite pattern).

**`MUTATIONS` entry format**, verified at `tools/check_repo.py:2296-2329`: a 3-tuple `(code, description_string, mutate_fn)` appended to the `MUTATIONS` list, e.g.:
```python
MUTATIONS = [
    ...
    ('artifact-family-section-missing', "delete the '## Solution proposal' heading from the real skills/proof-first/references/artifact-patterns.md, leaving its body in place", _mutate_artifact_family_section_missing),
]
```
The `description` string is printed verbatim as `mutation-test OK: <code> <description>` by `mutation_test()` (lines 2332-2380+). Each `_mutate_*` function (see e.g. `_mutate_catalog_opening_rule_count` at lines ~2279-2293) takes `root: Path`, mutates a **copy** of the real repo tree (never the live repo — `_copy_repo_subset` handles the copy before any `mutate_fn` runs), and returns nothing. New mutation functions for this phase's codes should follow this exact signature and mutate a copy of the real `.claude-plugin/*.json`, `examples/before-after.md`, or derivative files once they exist.

**`KNOWN_OPEN_VIOLATIONS`** — declared at `tools/check_repo.py:1851` as `KNOWN_OPEN_VIOLATIONS = frozenset()` (currently empty — the project has zero accepted-but-unfixed violations as of this session). It is read by `mutation_test()`'s CONTROL step (lines ~2358-2366) to separate "known-open" violations from "unexpected" ones on the unmutated control copy; the printed line format is `mutation-test CONTROL: {n} violations on the unmutated copy ({known} known-open per KNOWN_OPEN_VIOLATIONS, {unexpected} unexpected)`. New codes from this phase should not need an entry here unless a plan deliberately defers fixing a real, currently-existing violation — expected outcome is it stays `frozenset()`.

**Docstring registration convention** — every implemented code is listed in the module's own top-of-file docstring under "Violation codes implemented in this file:" (`tools/check_repo.py:23` onward), one bullet per code with a one-paragraph description including its "Declared ceiling" disclosure where applicable (see the `range-id` bullet at lines 26-38 for the exact rhetorical pattern: state what the check catches, then state plainly what it does not). New codes must add their own bullet here, following this exact declared-ceiling rhetorical convention.

---

### `tools/generate_derivatives.py` (utility, transform/batch/file-I/O)

**Analog:** `tools/check_repo.py`'s own header (lines 1-22) for stdlib-only discipline and the "declares its own ceiling" convention; `evals/conformance/run_conformance.py`'s header (lines 1-40+) for argparse-driven usage-doc structure and self-test-first design.

**Header/docstring template to follow**, verified verbatim at `tools/check_repo.py:1-22`:
```python
#!/usr/bin/env python3
"""Structural and textual consistency checker for this repository's registries.

This script is a structural and textual consistency check over NUMBERING.md,
examples/deal-brief.md, and NOTICES.md. It does not read framework source
material and it cannot judge whether a paraphrase reproduces proprietary
text -- that judgement is Phase 6's legal review gate (LEG-04). It imports
only the Python standard library; no package-manager dependency is
introduced by this file or by the CI job that runs it.

Usage:
  python3 tools/check_repo.py                # live run against this repo
  python3 tools/check_repo.py --self-test     # run fixture-based self-tests
  python3 tools/check_repo.py --mutation-test # ...
"""
```
And the richer usage-doc convention from `evals/conformance/run_conformance.py:1-40`:
```python
#!/usr/bin/env python3
"""Reproducibility instrument for MOD-04's conformance rate.

This script measures exactly one thing: ... It is a regex scorer over
transcript text, not a semantic judge -- ... It does not read the drafted
prose for quality. Phase 5's evaluation harness ... owns [X]; this runner is
deliberately narrower and does not overlap with it.

It imports only the Python standard library: argparse, datetime, json,
pathlib, re, shutil, subprocess, sys, tempfile. No package-manager
dependency is introduced by this file.

Usage:
  python3 evals/conformance/run_conformance.py --self-test
      Offline proof that the scorer discriminates the three committed
      transcript fixtures correctly. ...

  python3 evals/conformance/run_conformance.py [--skill-src PATH] ...
      Live mode: ...
"""
```
**Apply this shape to `generate_derivatives.py`'s own docstring:** state its one job (mechanically derive `output-styles/proof-first.md` and `prompts/system-prompt.md` from `SKILL.md` + named reference files, stamping a `hashlib.sha256` hash), state its stdlib-only import list explicitly, and state its own declared ceiling verbatim per Pattern 4 of RESEARCH.md: "(a) the hash only proves the derivative was regenerated from *some* version of the source... (b) this mechanism proves *structural* freshness, not *behavioral* equivalence... (c) a contributor could still hand-edit a derivative file after generation..." — this three-part disclosure is the exact rhetorical convention `tools/check_repo.py`'s own docstring uses for every "Declared ceiling" note (compare the `range-id` and `unlisted-figure` bullets, lines 26-60).

**Exit-code convention:** `tools/check_repo.py` exits non-zero on any violation in a live run, `0` on a clean run or successful self-test/mutation-test (inferred from CI step ordering in `.github/workflows/ci.yml`, which runs each command bare with no `|| true`, meaning a non-zero exit fails the CI job). `generate_derivatives.py` should exit `0` on successful generation, non-zero on any read/write failure — no separate "self-test" mode is strictly required by RESEARCH.md, but CI should exercise it as a "does it run without error" smoke step per the Phase Requirements → Test Map (DIST-05 row).

---

### `examples/before-after.md` (content/fixture, transform)

**Analog:** `skills/proof-first/references/worked-examples.md`, read in full (147 lines).

**Scope-boundary note, quoted verbatim** (`skills/proof-first/references/worked-examples.md:1-7`):
> "This file carries the worked ✗/✓ contrast for each catalog rule that has one. Every fact in every example comes from `examples/deal-brief.md`. Each rule's own statement and its `**Replace with:**` line live in `SKILL.md` for the prose catalog and in `references/completeness-audit.md` for the completeness audit — this file supplies the contrast only, keyed by the ID of the rule it belongs to."

**Complete pair, quoted verbatim** (`skills/proof-first/references/worked-examples.md:9-13`):
```
## PF-0.1

✗ "Kestrel Systems Group offers a comprehensive, best-in-class cloud migration solution."
✓ "Halverton Mutual's 850-VM estate is at capacity, and its nightly settlement batch regularly overruns its required window. This proposal describes an estate the team can govern, not one it has to manage VM by VM."
```
A second pair for texture (`worked-examples.md:14-17`):
```
## PF-1.1

✗ "Halverton Mutual's infrastructure suffers from significant technical debt and sprawl."
✓ "Halverton Mutual runs its policy-administration and settlement estate on 850 VMware vSphere virtual machines and 40 Oracle Database instances, all on-premises."
```

**How `examples/before-after.md` differs (per family, not per rule):** RESEARCH.md's own recommended skeleton (already vetted against the frozen `ARTIFACT_FAMILY_SECTIONS` headings):
```markdown
# Before and After

One family-level before/after pair per artifact family this skill classifies. Every fact traces
to `examples/deal-brief.md`. Every after column cites at least one rule ID allocated in
`NUMBERING.md`.

## RFP and RFI response

✗ [non-compliant paragraph]
✓ [compliant rewrite, e.g. citing PF-2.1, MC-11]

## Solution proposal
...
## Executive summary
...
## Demo and discovery material
...
```
Every fact must trace to `examples/deal-brief.md` (the shared canonical fictional deal, same discipline `worked-examples.md` already follows), and every "after" citation must be drawn from the closed 39-ID set (31 `PF-` + 8 `MC-`) enumerated in RESEARCH.md Pattern 5 — citing anything else trips the existing `undefined-id` code.

---

### `README.md` (content, transform — modified)

**Current section order**, verified by reading the full 146-line file this session:
1. `# Proof First` (title + one-line description)
2. `## What this is`
3. `## Status` (lines 14-73) — the load-bearing measured-figure disclosure. Contains "What exists today" / "What does not exist yet" bulleted lists, the MOD-04 conformance figure with its full caveats block, and the "This is not the persuasion benchmark" paragraph.
4. `## Repository layout` (lines 75-116) — the target-tree diagram with "(planned)"/"(exists)" annotations. This is the tree RESEARCH.md quotes as already anticipating this phase's five new files.
5. `## Rule numbering`
6. `## Versioning`
7. `## License and notices` (lines 136-146) — ends with the frozen non-affiliation disclaimer paragraph.

**The section `readme-results-pointer-missing` enforces** — this is the literal path string inside `## Status`, quoted verbatim (README.md line ~35 area, within the MOD-04 paragraph):
> "Full run-by-run figures, exclusions, and caveats live in `evals/conformance/RESULTS-mod04.md` — read that file before trusting anything downstream of it..."

The mutation that proves this gate (`tools/check_repo.py:2308`): `('readme-results-pointer-missing', "delete every line of README.md containing the results-pointer path", _mutate_readme_results_pointer_missing)`. **This literal string (the path `evals/conformance/RESULTS-mod04.md` appearing in README.md) must survive verbatim through any Track D rewrite.** Do not paraphrase it away or move it into a heading-only reference — the check greps for the literal path string somewhere in the file's text (inferred from the mutation's own description: "delete every line... containing the results-pointer path").

**What Track D changes:** per RESEARCH.md's Architectural Responsibility Map and Pattern set, README gets a new lead-in (before/after teaser, linking to `examples/before-after.md`) and a new `## Install` section (per-harness commands from Q6/Code Examples: `npx skills add <owner>/<repo>`, `claude plugin marketplace add <owner>/<repo> && claude plugin install proof-first@proof-first`, output-style/system-prompt paste instructions) — inserted additively, without deleting or renumbering the existing `## Status`, `## Repository layout`, `## Rule numbering`, `## Versioning`, or `## License and notices` sections. The `owner/repo` string is an unresolved placeholder (Pitfall 4) — mark it visibly, e.g. an inline HTML comment `<!-- TODO: replace owner/repo once a git remote is configured -->`, and route confirmation to a `checkpoint:human-verify` task.

---

### `.github/workflows/ci.yml` (config, event-driven — possibly modified)

**Quoted in full** (20 lines, read this session):
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
      - name: Run checker self-test, mutation test, and live check
        run: |
          python3 tools/check_repo.py --self-test
          python3 tools/check_repo.py --mutation-test
          python3 tools/check_repo.py
          python3 evals/conformance/run_conformance.py --self-test
```
**Step-naming convention:** one named step (`- name: Run checker self-test, mutation test, and live check`) runs a small multi-line `run:` block of sequential commands, rather than one step per command. **If this phase adds `generate_derivatives.py` as a CI-exercised smoke step** (per the Phase Requirements → Test Map's DIST-05 row: "exercised in CI as a 'does it run without error' smoke step"), the minimal-diff approach consistent with this file's own convention is to append one more line to the existing multi-line `run:` block (e.g. `python3 tools/generate_derivatives.py`), not a new `steps:` entry — this repo's CI surface is deliberately "one job, no matrix" per CLAUDE.md's own stated convention.

## Shared Patterns

### Stdlib-only import discipline
**Source:** `tools/check_repo.py:8-9` ("It imports only the Python standard library; no package-manager dependency is introduced by this file or by the CI job that runs it.") and `evals/conformance/run_conformance.py:17-18` ("It imports only the Python standard library: argparse, datetime, json, pathlib, re, shutil, subprocess, sys, tempfile.")
**Apply to:** `tools/generate_derivatives.py` and every new `check_repo.py` function. Only `re`, `json`, `hashlib`, `argparse`, `pathlib` (per RESEARCH.md's Standard Stack table) are needed; do not import anything else.

### Declared-ceiling disclosure convention
**Source:** every check function's docstring in `tools/check_repo.py` states plainly what it does NOT catch, e.g. `check_artifact_family_sections`'s docstring (lines 1521-1528): "Declared ceiling: this check is heading presence only. It says nothing about whether a section's content is correct or complete..."
**Apply to:** every new check function's docstring, and to `generate_derivatives.py`'s own module docstring (see Pattern 4's three-part disclosure quoted above).

### Frozen-interface reuse, never redeclare
**Source:** `ARTIFACT_FAMILY_SECTIONS` at `tools/check_repo.py:1487-1496`, with its own comment: "Frozen interface (P3-11) -- do not reword, re-case, pluralise, or reorder these four strings. SKILL.md's classification instruction, Phase 4's committed before/after examples, and Phase 5's linter all bind to them exactly as written here."
**Apply to:** `before-after-family-missing` must import this exact tuple, never redeclare a second literal list of the four family names.

### Stated-value-vs-registry check shape
**Source:** `check_catalog_count`/`check_mc_count` (`tools/check_repo.py:1400-1477`).
**Apply to:** `plugin-manifest-version-mismatch` and `skill-derivative-stale` — both are "a stated value in file A vs. a freshly recomputed value from source of truth B" checks, same control flow: parse stated value, handle "unstated" as its own violation code, compare, handle mismatch as a second violation code.

### Self-test/mutation-test three-part contract
**Source:** `self_test()` (`tools/check_repo.py:3223+`) and `MUTATIONS`/`mutation_test()` (`tools/check_repo.py:2296-2380+`).
**Apply to:** every new code this phase adds. No code is complete without (1) a bad/good fixture-root pair in `self_test()`, (2) a `MUTATIONS` tuple entry with a real mutate function operating on a copy of the live repo tree, (3) a bullet in the module's top-of-file docstring.

## No Analog Found

| File | Role | Data Flow | Reason |
|---|---|---|---|
| `output-styles/proof-first.md` | config/generated-artifact | transform, generated | No prior generated/derived Markdown artifact exists in this repo. SimpleEnglish's own equivalent file is hand-written, not generated, and explicitly identified in RESEARCH.md as NOT a template to copy prose from (Pitfall 1) — only its frontmatter shape (`keep-coding-instructions`, `force-for-plugin`) is reusable, and RESEARCH.md/CLAUDE.md already state Proof First likely wants neither field `true`. The planner should treat this as new-shape content produced mechanically by `generate_derivatives.py`, not modeled on any existing file's prose. |
| `prompts/system-prompt.md` | config/generated-artifact | transform, generated | Same reasoning as above — no in-repo analog; SimpleEnglish's version is explicitly flagged as prose-non-transferable in RESEARCH.md Pitfall 1. |

## Metadata

**Analog search scope:** `tools/check_repo.py` (full file, two targeted read passes), `tools/` directory listing, `evals/conformance/run_conformance.py` (header), `skills/proof-first/SKILL.md` (frontmatter + body opening), `skills/proof-first/references/worked-examples.md` (full file), `README.md` (full file), `NUMBERING.md` (versioning section), `.github/workflows/ci.yml` (full file), one prior-phase plan (`03-08-PLAN.md`, full file) for task/verify conventions, plus `~/devoteam/.claude/plugins/marketplaces/simple-english/` as an external (non-repo) reference cited by RESEARCH.md itself.
**Files scanned:** 9 in-repo files read in full or targeted ranges; all cited line ranges independently re-verified against the live file this session (both RESEARCH.md-claimed ranges, 1400-1428 and 1487-1544, confirmed exact).
**Tracked-source gate:** all in-repo analog paths confirmed via `git ls-files` (`.github/workflows/ci.yml`, `NUMBERING.md`, `README.md`, `evals/conformance/run_conformance.py`, `skills/proof-first/SKILL.md`, `tools/check_repo.py` — all printed, all tracked). The plugin-manifest analogs are external to this repo (a separate, unrelated local checkout) and are not gitignored mirrors of this repo's own tree, so the gate's "substitute the tracked origin" rule does not apply to them — they are cited as an external reference implementation only, per RESEARCH.md's own sourcing.
**Pattern extraction date:** 2026-09-17

## PATTERN MAPPING COMPLETE

**Phase:** 4 - Distribution & Worked Examples
**Files classified:** 9
**Analogs found:** 7 / 9 with concrete in-repo templates; 2 (the generated derivative artifacts) have no analog and are flagged as new-pattern content

### Coverage
- Files with exact analog (same file, extended): 3 (`tools/check_repo.py`, `README.md`, `.github/workflows/ci.yml`)
- Files with role-match analog: 4 (`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` — external template; `tools/generate_derivatives.py` — `tools/check_repo.py` + `run_conformance.py` header conventions; `examples/before-after.md` — `worked-examples.md` at family vs. rule granularity)
- Files with no analog: 2 (`output-styles/proof-first.md`, `prompts/system-prompt.md` — genuinely new, generated content with no in-repo precedent, and an explicit warning against copying SimpleEnglish's hand-written prose)

### Key Patterns Identified
- Every new `check_repo.py` code must follow the exact three-part contract (self-test fixture pair, `MUTATIONS` tuple entry, docstring bullet) already proven by 32 existing codes — no exceptions, no "lighter-weight" variant.
- Two check-shape templates cover all 4-5 new codes: the stated-value-vs-registry shape (`check_catalog_count`, lines 1400-1428) for `plugin-manifest-version-mismatch` and `skill-derivative-stale`; the section-presence shape (`check_artifact_family_sections`, lines 1487-1544) for `before-after-family-missing`, reusing the frozen `ARTIFACT_FAMILY_SECTIONS` tuple rather than redeclaring it.
- `SKILL.md`'s version lives at frontmatter `metadata.version` (nested key, currently `"0.1.0"`), not a top-level field — the plugin-version-match check needs a targeted extraction, not the general frontmatter parser.
- The plugin manifests have no in-repo analog; the correct template is the external, already-cross-checked SimpleEnglish reference quoted verbatim in RESEARCH.md — field-for-field copy, values changed.
- The two generated derivative artifacts must NOT be modeled on SimpleEnglish's hand-written prose (explicit Pitfall 1) — they are produced by a new stdlib-only generator script, hash-stamped, and checked for staleness; no prose-content analog exists or should be sought.

### File Created
`/Users/cymarechal/devoteam/devoteam/technical-presales/.planning/phases/04-distribution-worked-examples/04-PATTERNS.md`

### Ready for Planning
Pattern mapping complete. Planner can now reference analog patterns in PLAN.md files.
