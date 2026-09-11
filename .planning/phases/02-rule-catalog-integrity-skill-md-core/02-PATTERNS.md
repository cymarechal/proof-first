# Phase 2: Rule Catalog & Integrity — SKILL.md Core - Pattern Map

**Mapped:** 2026-09-11
**Files analyzed:** 6 (3 new, 3 modified)
**Analogs found:** 6 / 6 (all in-repo, git-tracked; one external precedent used for structure/method only, per D-25/canonical_refs — its text is never copied)

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog (tracked, in-repo) | Match Quality |
|---|---|---|---|---|
| `skills/proof-first/SKILL.md` (new) | config/instruction-catalog (Agent Skill) | request-response (write mode) + transform (check mode) | No in-repo analog exists yet — this is the first `SKILL.md` in the repo. Structural/method precedent (read-only, external, git-tracked in its own repo, NOT ours): `~/devoteam/.claude/plugins/marketplaces/simple-english/skills/simple-english/SKILL.md` | no-in-repo-analog — external-precedent-only |
| `skills/proof-first/references/deletion-test.md` (new) | reference/doc | transform (worked-pairs table read on demand) | Same as above — no in-repo analog; closest in-repo document shape is `NUMBERING.md`'s prose-plus-table sections | role-match (in-repo), external precedent for content shape |
| `skills/proof-first/references/checklist.md` (new) | reference/doc (machine-readable-ish index) | CRUD-like (row-per-ID registry, read-only from the skill's side) | `NUMBERING.md` (Allocated IDs table shape) — exact structural analog in-repo | exact (table shape) |
| `NUMBERING.md` (modified — new `PF-2` sub-block table, Allocated IDs rows filled) | model/registry (authoritative data file) | CRUD (append rows) | itself — extend the existing `## PF-1 sub-blocks` table pattern and `## Allocated IDs` table | exact |
| `tools/check_repo.py` (modified — new frontmatter parser + PF ID-set/count equality checks) | utility/checker (CLI, CI-invoked) | batch / transform (parse → validate → report) | itself — extend existing `check_*`/`run_*_checks`/`_mutate_*`/`_bad_*`/`_good_*` pattern already in this file | exact |
| `.github/workflows/ci.yml` (unmodified expected — verify only) | config (CI) | event-driven | itself | exact (no change needed; confirm during planning) |

## Pattern Assignments

### `skills/proof-first/SKILL.md` (config/instruction-catalog, request-response + transform)

**No in-repo analog** — this is the first file of its kind in this repository. There is nothing tracked in this repo to copy structure from; the closest thing is the external sibling skill, read only for *shape*, never for text (per `NOTICES.md`'s paraphrase-boundary posture and D-25/CLAUDE.md's zero-text-reuse constraint). Treat the excerpts below as **shape references**, not copy sources — no wording from them may appear verbatim in the new file.

**Frontmatter shape** (external precedent, `simple-english/skills/simple-english/SKILL.md` lines 1-15 — structure only, do not copy wording):
```yaml
---
name: simple-english
description: |
  Write or rewrite technical text with the rules of ... Use for
  documentation, READMEs, ... Also use when the user says "STE", ...
license: MIT
compatibility: claude-code cursor codex gemini-cli opencode
metadata:
  version: "1.3.0"
  standard: ASD-STE100 Issue 9 (2025-01-15)
---
```
Per D-29/D-33/STACK.md, Proof First's frontmatter must omit `compatibility` entirely (project decision, deviates from this precedent) and its `description` must contain zero framework-name keywords, ~400–600 chars, front-loaded on artifact types.

**Two-mode task framing** (external precedent, lines 25-36 — structure only):
```
## Your Task
1. Select the mode ...
...
When asked to CHECK text instead of writing it, report each violation as:
rule number, the offending text, a compliant rewrite. Cite only rule
numbers that exist in this file. Do not cite rule numbers from memory.
```
This "cite only rule numbers that exist in this file" instruction is the exact anti-hallucination pattern D-32/Pattern-3-of-RESEARCH requires SKILL.md to state in its own words, tied to `references/checklist.md` and the stated rule count.

**Section-per-catalog-block shape with an inline note on which rules do the work** (external precedent, lines 56-83): a `## THE RULE CATALOG` heading, a stated `N rules in M sections` count sentence, `### Section N — Name (Rules x.y-x.z)` sub-headings, table or per-rule blocks. Proof First's per-rule shape is fixed by CONTEXT.md's own Specific Ideas (not the sibling's table form) — see the settled rule shape already recorded in CONTEXT.md/RESEARCH.md's Code Examples section (reproduced there, not repeated here to avoid drift from the single source of truth).

**Self-check-before-delivery shape** (external precedent, lines 291-301): a numbered, mechanical self-check list run before output is returned. D-08's two-pass (subtract, then additive sweep) self-check replaces this with Proof First's own two-pass instruction — same *position in the document* (near the end, before output), different content.

**Limits section shape** (external precedent, line 319 heading + body pattern: states what the standard does NOT guarantee without the official dictionary). D-13's Limits section follows the same "state what this skill cannot verify, plainly, near the end" placement.

**In-repo grounding this file must satisfy on creation (exact, not precedent):**
- `NOTICES.md` lines 36-41 (`Files required to carry it`) lists `skills/proof-first/SKILL.md` — creating the file activates `tools/check_repo.py`'s `pointer-missing`/`pointer-duplicated` checks (see below) against the exact fenced string at `NOTICES.md` lines 28-31.
- Every `PF-#.#` token cited or defined in `SKILL.md` is checked by the existing `check_undefined_id` (`tools/check_repo.py:237-266`) against `NUMBERING.md`'s Allocated IDs table — no new code needed for this part.

---

### `skills/proof-first/references/deletion-test.md` (reference/doc, transform)

**No in-repo analog.** Structural precedent only: `NUMBERING.md`'s mix of explanatory prose plus a Markdown table (e.g. `## PF-1 sub-blocks`, `NUMBERING.md` lines 21-32) is the closest in-repo shape for "a named condition, explained in prose, followed by a table with fixed columns." Use this table-after-prose pattern for the four-class edge-case table D-26 requires (worked pairs: sentence-with-term → sentence-with-term-deleted → verdict-and-why), not a verdict-only banned/allowed list (explicitly rejected — see RESEARCH.md Anti-Pattern 1 / Don't Hand-Roll table).

**Source material for worked pairs:** `examples/deal-brief.md` (git-tracked, lines 1-40 read this session) — e.g. the discovery quote and the settlement-batch/SOC 2 facts are the only facts any worked pair may cite (checker-enforced for figures via `unlisted-figure`, though note the RESEARCH.md-flagged gap: that check's scan root is `examples/**/*.md`, not `skills/**/*.md`, so a figure cited inside this reference file is not currently checker-enforced — flag this to the planner as an open question, do not silently assume it is covered).

---

### `skills/proof-first/references/checklist.md` (reference/doc, CRUD-like registry)

**Analog:** `NUMBERING.md`'s `## Allocated IDs` table (`NUMBERING.md` lines 60-64):
```markdown
## Allocated IDs

Rows are kept sorted ascending by ID. Phase 2 adds `PF-*` rows as prose rules are written; Phase 3
adds `MC-*` rows as the completeness audit is written. Zero rules are allocated as of this plan.

| ID | Title | Defined in | Added in |
|---|---|---|---|
```
D-27 requires `checklist.md` to ship with PF rows only in this phase (MC rows deferred to Phase 3) — same column discipline (ID, then descriptive columns) so `tools/check_repo.py`'s existing `table_rows()`/`split_sections()` (below) can parse it with zero new generic-parsing code; only a new call site plus set-comparison logic is new (D-32).

**Reusable parsing utilities** (`tools/check_repo.py` lines 109-145, exact, copy the call pattern):
```python
def split_sections(text):
    """Split a Markdown document into {heading: body} by '## ' headings."""
    ...

def table_rows(section_text):
    """Return data rows (list of stripped cells) from the first Markdown
    table found in section_text, skipping the header and separator rows."""
    ...
```
These two functions are already proven against `NUMBERING.md` and `examples/deal-brief.md` (`parse_numbering`, `parse_deal_brief`) — reuse them verbatim for a new `parse_checklist(path)` function rather than writing a second table reader (explicit Don't-Hand-Roll item in RESEARCH.md).

---

### `NUMBERING.md` (modified — model/registry, CRUD)

**Analog:** itself. Extend the existing sub-block table pattern used for `PF-1` (lines 21-32) to add the `PF-2` sub-block table D-05 requires, in the same form:
```markdown
## PF-1 sub-blocks

`PF-1`'s reserved range (`PF-1.1`-`PF-1.28`) is carved into seven named sub-blocks, one per
Command of the Message element. A contributor adding a rule reads the element name below rather
than inferring it from a number.

| Element | Range |
|---|---|
| Before scenario | PF-1.1-PF-1.4 |
...
```
D-05's `PF-2` table needs two rows only: `Proof | PF-2.1-PF-2.10` and `Integrity | PF-2.11-PF-2.20`, headed `## PF-2 sub-blocks`, placed immediately after `## PF-1 sub-blocks` and before `## MC reserved blocks` to preserve the document's existing PF-then-MC ordering.

Then append rows to `## Allocated IDs` (lines 60-64) as rules are authored, keeping ascending-by-ID sort order (stated requirement in the section's own prose, machine-enforced nowhere currently except via manual discipline — the planner should note whether an `allocated-id-order` check is in scope, likely not per D-32's stated scope which is ID-set-equality and count, not ordering).

---

### `tools/check_repo.py` (modified — utility/checker, batch/transform)

**Analog:** itself. Three existing subsystems to mirror exactly for the two new codes (D-32 PF ID-set/count equality; D-33 frontmatter validity):

**1. Targeted "just enough" parser precedent** (`parse_notices`, lines 398-420 — exact excerpt, this is the closest existing precedent for "extract a specific known shape without a general-purpose parser," cited directly by RESEARCH.md Pattern 5):
```python
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
```
Write `parse_frontmatter(path)` in this style: split on the first two `^---$` lines, scan for the six known top-level keys at column 0, handle `description`'s optional block-scalar (`description: |` + indented continuation lines) the same way this function handles a marker-then-indented-list. No PyYAML (explicit Don't-Hand-Roll item).

**2. Check-function + violation-tuple shape** (`check_pointer`, lines 423-436, and `check_license_missing`, lines 446-464 — exact excerpts, this is the required return shape for any new check function):
```python
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
```
Every new D-32/D-33 check function must return a `list[(subject, "code-name message")]` tuple list in this exact shape — `run_all_checks` (line 564) concatenates these across all `run_*_checks` functions, and `mutation_test` (line 762+) parses the code out of the message via `line.split(' ', 1)[0]`, so the leading token of every violation message must be exactly the violation code string, unbroken.

**3. Mutation registration + fixture pattern** (`_mutate_dup_id`, lines 621-627, and the `MUTATIONS` list, lines 734-747 — exact excerpts):
```python
def _mutate_dup_id(root):
    path = root / 'NUMBERING.md'
    text = path.read_text(encoding='utf-8')
    row = '| PF-0.1 | Mutation dup row | SKILL.md | v0.0.0 |'
    text = _insert_table_rows_after_heading(text, 'Allocated IDs', [row, row])
    path.write_text(text, encoding='utf-8')
```
```python
MUTATIONS = [
    ('dup-id', "insert the same allocated-ID row twice into NUMBERING.md's Allocated IDs table", _mutate_dup_id),
    ...
]
```
D-34 requires every new D-32/D-33 code to get exactly this treatment: a `_mutate_<code>(root)` function that injects one named defect into a scratch copy, plus a `MUTATIONS` tuple registering it. `mutation_test()` (lines 750-786) already asserts every code in `ALL_CHECK_CODES` has a registered mutation and fires — extending `ALL_CHECK_CODES` (line 557, currently `ID_CHECK_CODES + FIGURE_CHECK_CODES + NOTICES_CHECK_CODES + LICENSE_CHECK_CODES + FRAMEWORK_CHECK_CODES`) with two new lists (e.g. `FRONTMATTER_CHECK_CODES`, `PF_CATALOG_CHECK_CODES`) is the wiring point — no change needed to `mutation_test` itself.

**4. Self-test fixture pattern** (`_bad_numbering`/`_good_numbering`, lines 803-857 — pattern only, not fully reproduced for length): each fixture is a `_write(path, content)` call building a minimal valid/invalid document, then `self_test()` asserts the expected violations fire/don't fire. New frontmatter and PF-set fixtures must follow this same "hand-built minimal fixture, not the real repo" discipline, run before `--mutation-test` is pointed at the real files (per RESEARCH.md Pattern 5's stated ordering: self-test first, then wire into `run_all_checks`, then mutation-register).

---

## Shared Patterns

### Violation-message shape (applies to all new checker code)
**Source:** `tools/check_repo.py` module docstring, lines 1-90 (the `Violation codes implemented in this file:` block) — every code is documented with a one-line summary plus an explicit **Declared ceiling** paragraph stating what the check does *not* catch (e.g. `unlisted-figure`'s docstring: "Declared ceiling (bare count): this check catches currency, percentages, and ISO dates only... a bare count that drifts between examples is not detected by this tool.").
**Apply to:** the two new D-32/D-33 codes — each new code must get its own paragraph in this docstring block, following the same "what it catches / what it declared-ceiling misses" two-part shape, before being wired in.

### Attribution pointer activation (applies to SKILL.md only, automatic)
**Source:** `NOTICES.md` lines 26-42 (fenced pointer string + carrier list) and `tools/check_repo.py`'s `check_pointer` (lines 423-436).
**Apply to:** `skills/proof-first/SKILL.md` must carry the exact fenced string from `NOTICES.md` lines 28-31 exactly once, verbatim, code-point-for-code-point (no Unicode normalization per the docstring's declared ceiling, lines 62-69 region). This is not optional formatting — it is a CI-enforced literal string match.

### ID citation validation (applies to SKILL.md and both reference files, automatic, no new code)
**Source:** `check_undefined_id`, `tools/check_repo.py` lines 237-266, and `undefined-id`'s docstring entry (lines 16-19).
**Apply to:** every `PF-#.#` token appearing anywhere under `skills/` (which includes both new reference files) is scanned against `NUMBERING.md`'s Allocated IDs the moment these files exist — this includes every `[PF-#.# GAP/REVIEW/...]` marker per D-14, since the marker grammar reuses the same token pattern. No new checker code is needed for marker validity itself (RESEARCH.md Pattern 4's "free win" finding).

## No Analog Found

| File | Role | Data Flow | Reason |
|---|---|---|---|
| `skills/proof-first/SKILL.md` | config/instruction-catalog | request-response + transform | First Agent-Skill file in this repository; no git-tracked in-repo predecessor exists. Use the external sibling skill (read-only, its own separate git repo) for *shape* only — RESEARCH.md's Architecture Patterns section and CONTEXT.md's Specific Ideas (settled rule shape, register shape) are the actual content source. |
| `skills/proof-first/references/deletion-test.md` | reference/doc | transform | Same reason — first reference file of its kind; content must be authored fresh per D-26 from `PITFALLS.md`'s four named edge-case classes and `examples/deal-brief.md`'s facts, not copied from any existing file. |

## Metadata

**Analog search scope:** repository root (`NUMBERING.md`, `NOTICES.md`, `SOURCES.md`, `LICENSE`, `README.md`), `tools/check_repo.py` (full file, 1191 lines, read in three non-overlapping passes), `examples/deal-brief.md` (first 40 lines), `.github/workflows/ci.yml` (existence confirmed via `git ls-files`, not opened — no change expected this phase). External precedent inspected read-only: `~/devoteam/.claude/plugins/marketplaces/simple-english/skills/simple-english/SKILL.md` (full file, 329 lines) — a separate git repository, not part of this repo's tracked tree; used strictly for structural/method comparison per the canonical_refs instruction, never as a copy source for its own text.
**Files scanned:** 9
**Pattern extraction date:** 2026-09-11
