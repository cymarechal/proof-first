# Phase 3: Completeness Audit & Artifact Patterns — Pattern Map

**Mapped:** 2026-09-11
**Scope:** MEDDICC-derived completeness audit (`MC-` namespace), artifact-family conventions for
four document types, a classification announcement, and a three-category check-mode report.
**Requirements covered:** AUD-01..03, ART-01..04, MOD-03..05

Proof First has no application code — its "files" are `SKILL.md`, `references/*.md`,
`NUMBERING.md`, and `tools/check_repo.py`. Every analog below is a real file already shipped in
Phase 2. Phase 3 is not a new shape; it is the same shapes filled with `MC-` content and one more
report category. Divergence, not novelty, is the risk this document exists to prevent.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `skills/proof-first/SKILL.md` (new `## MC-*` sections, artifact-family lines, report category) | rule catalog + prose spec | transform (Markdown → agent instructions) | `skills/proof-first/SKILL.md` (own prior `## PF-*` sections) | exact — same file, extending an established shape |
| `skills/proof-first/references/checklist.md` | index/registry (rendered doc) | CRUD (append rows) | itself, `## PF rules` table | exact — add a `## MC rules` table of the same shape |
| `skills/proof-first/references/worked-examples.md` | reference (rendered doc) | CRUD (keyed lookup by rule ID) | itself | exact — same "opens with a provenance paragraph, one `## <ID>` section per rule with ✗/✓" shape |
| New `references/completeness-audit.md` (or equivalent MC reference file) | reference (rendered doc) | CRUD + transform (dimension → check procedure) | `skills/proof-first/references/deletion-test.md` (mechanism-teaching shape), secondarily `checklist.md`/`worked-examples.md` | role-match — see §2 for which shape and why |
| `NUMBERING.md` (`MC-` Allocated IDs rows, MC dimension `Allocated`/`Next free` updates) | registry (rendered doc) | CRUD (append rows, update counters) | itself, `## Allocated IDs`, `## MC reserved blocks` sections | exact — table shape and update discipline already defined, only rows are new |
| `tools/check_repo.py` — any new mechanical check(s) for AUD/ART/MOD requirements | utility / linter check function | transform (parse → violation list) | `check_catalog_opening_rule_count` (commit `42607c4`) as the template; `check_catalog_id_drift` as the three-file cross-check template | exact — D-34 triad is mandatory and this is its freshest instance |
| `.planning/phases/03-completeness-audit-artifact-patterns/03-0X-PLAN.md` | plan file | request-response (spec → executor) | `.planning/phases/02-.../02-04-PLAN.md` (closes out a catalog, allocates final IDs, measures a ceiling) | exact |
| `.planning/phases/03-.../03-0X-SUMMARY.md` | summary file | event-driven (task completion record) | `.planning/phases/02-.../02-04-SUMMARY.md` | exact |

## Pattern Assignments

### 1. Rule anatomy in `SKILL.md` — the invariant shape every `MC-*` rule must match

Analog: `skills/proof-first/SKILL.md:53-118` (PF-0, PF-1) and `:147-190` (PF-2 Integrity rules,
the closest data-flow analog to an audit dimension — evidence-presence checking).

**Heading format** (`SKILL.md:65`, `:123`, `:147`):
```
### PF-1.1 — Name the current state in the buyer's own terms
```
`### <ID> — <imperative title>`, exactly one em-dash-separated title, en space either side. `MC-`
rules must use `### MC-<n> — <title>` — no sub-numbering (`MC-` IDs are flat integers per
`NUMBERING.md:9`, unlike `PF-<section>.<n>`).

**The subtractive/diagnostic statement** (`SKILL.md:123-125`, one paragraph, 2–4 sentences):
```
A sentence asserting something about the customer's estate, the vendor's capability, or an
outcome carries its evidence in the same sentence or the next.
```
States the failure condition in prose, never as a checklist bullet.

**The constructive half — `**Replace with:**`** (`SKILL.md:127`, `:145`, `:151`, etc.), always one
line, always bold-labelled, always naming a concrete substitution or the marker to raise instead:
```
**Replace with:** the customer's stated figure, a named artefact the reader could ask for, or a `GAP` marker.
```
Every `MC-*` rule must carry exactly one `**Replace with:**` line — this is mechanically counted
(see below).

**Marker vocabulary** (`SKILL.md:33-45`): three closed bracket forms, `<rule>` token always first:
```
[<rule> GAP: what is missing]
[<rule> REVIEW (<commitment|reference|competitor|compliance>): what needs confirming]
[<rule>: customer's term, retained — source]
```
An `MC-` completeness gap (e.g. no named Economic Buyer) is diagnostically closest to
`PF-2.4`/`PF-2.13`'s `GAP` mechanism (`SKILL.md:141-145`, `:159-163`) — a missing dimension is
marked in place, not silently omitted. Reuse `[MC-<n> GAP: what is missing]` rather than inventing
a fourth bracket form; `NUMBERING.md` and the marker vocabulary section both state the vocabulary
is closed (`SKILL.md:33-45` — three forms, not four).

**Sentence discipline:** every rule body obeys the catalog's own `PF-4` rules (sentence ≤25 words,
active voice, one claim per sentence) — `SKILL.md:215-238`. A new `MC-*` rule violating its own
catalog's prose-mechanics rules is an internal inconsistency, not just a style nit.

**Mechanical enforcement of the heading/`Replace with:` pairing:** there is **no check in
`tools/check_repo.py` itself** that counts `### PF-` headings against `**Replace with:**`
occurrences — I searched (`grep -in replace tools/check_repo.py`) and found none. The count parity
is instead enforced at the **plan/task verification level**, as paired `grep` acceptance criteria,
e.g. `.planning/phases/02-.../02-04-PLAN.md:231-234`:
```
<automated>grep -c '^### PF-' skills/proof-first/SKILL.md</automated>
<fails_when>the printed number is anything other than 24</fails_when>
<automated>grep -cF '**Replace with:**' skills/proof-first/SKILL.md</automated>
<fails_when>the printed number is anything other than 24</fails_when>
```
Phase 3's plans must reproduce this exact paired-grep pattern for the `MC-*` heading count vs.
`**Replace with:**` count, scoped so it counts only the section(s) actually touched, exactly as
02-04 did for PF-3/4/5. Do not assume `check_repo.py` enforces this — it does not, today.
`check_catalog_id_drift` (`tools/check_repo.py:880-922`) is the nearest thing to a mechanical
heading-vs-registry check, but it compares heading-defined IDs against `NUMBERING.md` and
`checklist.md`, not against `**Replace with:**` counts.

---

### 2. Reference-file shape — which existing file is the right analog for the new `MC-` file

Three reference files exist, each with a distinct job:

| File | Opens with | Binds to `SKILL.md` via | Binds to `NUMBERING.md` via | Has a "does not do" section? |
|---|---|---|---|---|
| `checklist.md` | one paragraph stating it is a searchable citation index, invented-number prohibition (`checklist.md:1-8`) | `SKILL.md:50` reference pointer ("Before emitting any rule citation in check mode, read `references/checklist.md`") | explicit line: "`NUMBERING.md`... is the authoritative registry... it does not ship to an installed copy of this skill" (`checklist.md:5-8`) | no |
| `deletion-test.md` | one paragraph naming the trigger condition for opening it — "Open this file before applying PF-3.1 to a compound term..." (`deletion-test.md:1-8`) | `SKILL.md:49` reference pointer, conditional ("Before applying the deletion test to a compound term...") | none direct (it is a teaching file, not a registry) | **yes** — `## What this file does not do` (`deletion-test.md:61-67`): explicitly refuses to be a banned/allowed term list, states why (staleness, noun/modifier boundary gets it wrong both ways) |
| `worked-examples.md` | one paragraph stating its sole content type and provenance boundary — "carries the worked ✗/✓ contrast... Every fact... comes from `examples/deal-brief.md`; the rule statements... live in `SKILL.md`" (`worked-examples.md:1-6`) | implicit, one `## <rule-id>` section per rule with an example (`SKILL.md:52` pointer: "Before writing or checking a ✗/✓ contrast... read `references/worked-examples.md`") | none | no |

**Verdict for the new `MC-` reference file: model it on `deletion-test.md`, not `checklist.md` or
`worked-examples.md`.** Reasoning:
- `checklist.md` is a pure ID index (one flat table) — it is *also* needed for `MC-` IDs (a
  `## MC rules` table appended to it, same row shape: `| ID | Rule |`), but it is not where the
  audit's *procedure* (how to check each MEDDICC dimension, what counts as satisfied vs. a gap)
  belongs.
- `worked-examples.md` only carries ✗/✓ contrasts keyed to an ID whose statement lives in
  `SKILL.md` — appropriate for MC rules' own ✗/✓ pairs if they get any, but not for the
  audit-procedure content (per-dimension check logic, what evidence satisfies each dimension,
  edge cases like "champion identified but not yet tested").
- `deletion-test.md` is the shape that **teaches a transferable mechanism through worked
  instances**, opens with a conditional trigger line naming exactly when to read it, and closes
  with an explicit "does not do" boundary refusing to become a static list. A MEDDICC completeness
  audit is exactly this kind of thing: "for dimension X, what present/gap looks like" is a
  procedure a model must apply to text it has never seen, not a fixed checklist of literal strings
  to grep for. The new file (e.g. `references/completeness-audit.md`) should:
  - open with a one-paragraph statement of its trigger condition ("Before running the completeness
    audit / classifying an artifact / assigning a REVIEW…", mirroring `deletion-test.md:1-8`)
  - carry one worked-pairs table or per-dimension section per MEDDICC dimension (Metric, Economic
    Buyer, Decision Criteria, Decision Process, Paper Process, Pain, Champion, Competition — the
    eight dimensions already reserved in `NUMBERING.md:64-77`), each with a **present** example, a
    **gap** example, and the verdict/why — the same three-column discipline `deletion-test.md:9-14`
    uses (Class | example | why)
  - close with a `## What this file does not do` section stating it is not a scoring rubric or a
    pass/fail gate that substitutes for human judgment — the direct MEDDICC-flavoured analog of
    `deletion-test.md:61-67`'s refusal to become a term list
  - both `checklist.md` (flat MC ID index) and this new file must exist; do not merge the audit
    procedure into `checklist.md`.

---

### 3. `NUMBERING.md` — current `MC-` namespace state (read directly, not projected)

`NUMBERING.md:64-77`, `## MC reserved blocks`:

| Dimension | Range |
|---|---|
| Metric | MC-1-MC-5 |
| Economic Buyer | MC-6-MC-10 |
| Decision Criteria | MC-11-MC-15 |
| Decision Process | MC-16-MC-20 |
| Paper Process | MC-21-MC-25 |
| Pain | MC-26-MC-30 |
| Champion | MC-31-MC-35 |
| Competition | MC-36-MC-40 |

Ceiling: `MC-40` (`NUMBERING.md:77`). Five slots per dimension, eight dimensions, uniform — no
under/over-filling asymmetry the way `PF-1`'s seven-elements-into-20-slots problem forced a
28-slot widening (`NUMBERING.md:42-49`); the planner does not need to re-litigate range width
unless a dimension is judged to need more than 5 rules.

**`## Allocated IDs` table (`NUMBERING.md:84-116`): zero `MC-*` rows exist today.** Every MC ID is
unallocated. The registry's own instruction (`NUMBERING.md:81-82`): "Phase 3 adds `MC-*` rows as
the completeness audit is written." Next free ID for a dimension with zero allocations is that
dimension's range start (`NUMBERING.md:145-149`) — e.g. next free for Metric is `MC-1`, for
Economic Buyer is `MC-6`, etc., until Phase 3 allocates.

**`## Deprecated IDs` (`NUMBERING.md:118-126`):** empty, zero rows — no MC ID has ever been
deprecated (none has even been allocated yet), so nothing to avoid reusing.

**Namespace-disjointness rule** (`NUMBERING.md:9-13`): `PF-` and `MC-` are disjoint — no ID exists
in both, and a citation is always prefixed (`MC-6`, never bare `6`). No `## PF-<n> sub-blocks`-style
per-dimension sub-block table exists yet for MC (unlike `PF-1` and `PF-2`, `NUMBERING.md:26-63`) —
`parse_pf_subblocks` (`tools/check_repo.py:311-337`) only looks for `## PF-<n> sub-blocks` headings;
there is **no equivalent MC sub-block parser**, and `check_range_id`'s MC branch
(`tools/check_repo.py:372-376`) checks only that an MC ID falls inside *some* declared MC dimension
range as a whole — it does not further constrain to a per-dimension sub-block the way `PF-1`/`PF-2`
IDs are constrained by `pf_subblocks`. If Phase 3 wants tighter within-dimension enforcement,
that is new code, not something already wired.

---

### 4. The check triad — end-to-end template from `catalog-opening-rule-count` (commit `42607c4`)

D-34 requires three parts for every check. Here is the exact template, with line references, from
the freshest instance:

**Part 1 — check function + registration + aggregator + code list.**
- Function: `check_catalog_opening_rule_count(allocated, repo_root)` at
  `tools/check_repo.py:963-992`. Signature pattern: takes the already-parsed `allocated` rows (from
  `parse_numbering`) plus `repo_root`; returns a list of `(key, message)` tuples. Message string
  format is always `"<code> <human-readable explanation citing the requirement ID>"`
  (`tools/check_repo.py:975-978`).
- Registered in the code list: `CATALOG_CHECK_CODES` (`tools/check_repo.py:1039-1043`) includes
  `'catalog-opening-rule-count'`.
- Wired into the aggregator: `run_catalog_checks(repo_root)` (`tools/check_repo.py:1045-...`) calls
  it and appends its violations, exactly as `run_id_checks` calls each of the four `ID_CHECK_CODES`
  functions in sequence (`tools/check_repo.py:418-429`).
- Rolled into `ALL_CHECK_CODES` (`tools/check_repo.py:1059-1062`), which is the master list every
  other part of the harness (self-test coverage loop, mutation coverage loop) iterates over.

**Part 2 — self-test fixtures: one that fires, one that stays silent.**
- Fixture builders: `_single_opening_rule_numbering()` / `_single_opening_rule_checklist()` (good)
  and `_multiple_opening_rules_numbering()` / `_multiple_opening_rules_checklist()` (bad) — written
  to `opening_good_root` / `opening_bad_root` inside `self_test()`
  (`tools/check_repo.py:2107-2108`, `:2212-2218`).
- Both roots run through `run_all_checks`, codes collected as sets (`tools/check_repo.py:2247-2248`).
- Explicit assertions (`tools/check_repo.py:2316-2321`):
  ```python
  if 'catalog-opening-rule-count' in opening_good_codes:
      print("FAIL: catalog-opening-rule-count fired on the known-good (exactly one PF-0) fixture")
      all_ok = False
  if 'catalog-opening-rule-count' not in opening_bad_codes:
      print("FAIL: catalog-opening-rule-count did not fire on the multiple-opening-rules fixture")
      all_ok = False
  ```
- The bad-fixture's codes are also unioned into the global `bad_codes` set
  (`tools/check_repo.py:2253-2258`) so the generic "every code must fire on some bad fixture, never
  on good_root" coverage loop (`tools/check_repo.py:2323-...`) picks it up automatically — a new MC
  check's bad fixture must be added to this union too, or the generic loop will report it as never
  observed firing.

**Part 3 — `MUTATIONS` entry proving discrimination against the real repo.**
- Mutator function: `_mutate_catalog_opening_rule_count(root)` (`tools/check_repo.py:1376-1390`) —
  takes a copied root (a working copy of the real repo tree, not a synthetic fixture), inserts one
  extra `PF-0.2` row into both `NUMBERING.md`'s `Allocated IDs` table (via the shared
  `_insert_table_rows_after_heading` helper, `tools/check_repo.py:1136-...`) and
  `references/checklist.md`'s `PF rules` table, matching the exact violation shape the check
  detects.
- Registered in `MUTATIONS` (`tools/check_repo.py:1407`):
  ```python
  ('catalog-opening-rule-count', "add a second PF-0 rule to NUMBERING.md and checklist.md, violating CAT-03's exactly-one requirement", _mutate_catalog_opening_rule_count),
  ```
  Tuple shape: `(code, human-readable description of the mutation, mutator function)`.
- `--mutation-test` copies the real repo, applies the mutator, re-runs all checks, and asserts the
  target code (and *only* checks expected to be affected) fires — proving the check discriminates
  against production content, not just synthetic fixtures (`tools/check_repo.py:1434`,
  `:1483` — `uncovered = [c for c in ALL_CHECK_CODES if c not in {m[0] for m in MUTATIONS}]`
  fails the run if any code lacks a mutation).

**Step-by-step template for a new Phase 3 check** (e.g. an `MC-` range/registry check, or an
artifact-classification-announcement check):
1. Write `check_<name>(...)` next to the other checks in its concern block (ID checks are grouped
   at `tools/check_repo.py:340-429`; catalog checks at `:843-1043`) — reuse `parse_numbering`,
   `parse_checklist`, `parse_skill_catalog`, `split_sections`, `table_rows` rather than re-parsing.
2. Add its code string to the relevant `*_CHECK_CODES` list and wire the call into that concern's
   `run_*_checks` function.
3. Confirm it flows into `ALL_CHECK_CODES` (it will, automatically, via the existing concatenation
   at `tools/check_repo.py:1059-1062` and `1060` — no edit needed there unless a wholly new concern
   block is introduced, in which case add its list to the concatenation).
4. Add a good/bad fixture pair to `self_test()`, following the `opening_good_root`/`opening_bad_root`
   pattern exactly (naming convention `<concern>_good_root` / `<concern>_bad_root`), union the bad
   codes into `bad_codes`, and add explicit named assertions like `:2316-2321`.
5. Write a mutator function next to `_mutate_catalog_opening_rule_count`
   (`tools/check_repo.py:1376-1390`) that mutates a **copy of the real repo tree**, and add a
   `MUTATIONS` tuple.
6. Run `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test &&
   python3 tools/check_repo.py` — the exact CI order used throughout Phase 2
   (`.planning/phases/02-.../02-04-PLAN.md:320-325`, `:342`).

---

### 5. Existing `MC-` awareness in the checker today

- `MC_ID_RE = re.compile(r'^MC-(\d+)$')` (`tools/check_repo.py:217`) — matches a bare `MC-<n>`
  token, flat integer, no sub-numbering.
- `mc_ranges` (`tools/check_repo.py:280-285`, populated inside `parse_numbering`) — parses the
  `## MC reserved blocks` table into `{dimension_name: (min, max)}` pairs. This already reads the
  eight rows in §3 above; it needs no change to recognize the ranges — they are already declared.
- `check_range_id`'s MC branch (`tools/check_repo.py:372-376`):
  ```python
  m = MC_ID_RE.match(id_)
  if m:
      n = int(m.group(1))
      if not any(rng[0] <= n <= rng[1] for rng in mc_ranges.values()):
          violations.append((id_, f"range-id {id_} belongs to no declared MC dimension block"))
  ```
  Today this only fires for an ID that falls **outside every** declared MC range (e.g. `MC-41` or
  `MC-0`) — because zero MC rows are allocated yet, this branch never fires today. It does **not**
  currently check that an MC ID sits in the *specific* dimension range its title/content implies
  (no per-dimension sub-block containment for MC, unlike `pf_subblocks` for PF — see §3). Once
  Phase 3 allocates real `MC-*` rows, this branch starts doing real work with **no code change
  required** — it is already correct for the coarse "somewhere in some MC block" check.
- `check_undefined_id` (`tools/check_repo.py:388-412`) **already covers MC tokens**: line 405,
  ```python
  tokens = set(re.findall(r'PF-\d+\.\d+', text)) | set(re.findall(r'MC-\d+', text))
  ```
  scans `skills/`, `examples/`, and `README.md` for both PF and MC citation tokens and flags any
  token not present in `allocated_ids` (which is built from `NUMBERING.md`'s `Allocated IDs` table,
  itself namespace-agnostic — it does not filter by prefix). **No change needed here either** — as
  soon as `SKILL.md` cites an `MC-` ID, this check enforces it is registered.
- **What would need to change when `MC-` IDs are actually allocated and cited:** essentially
  nothing in the parsing/range-checking machinery — it is namespace-agnostic by construction
  (`parse_numbering`, `check_dup_id`, `check_revived_id`, `check_undefined_id` all operate on the
  generic `allocated` list without branching on prefix except where a regex must distinguish
  `PF-<n>.<n>` from `MC-<n>` shape, i.e. `check_range_id`). The one **new** enforcement surface Phase
  3 must decide whether to build is `check_catalog_id_drift`'s MC equivalent
  (`tools/check_repo.py:880-922`): today that function is hardcoded to compare `PF_ID_RE`-matched
  rows against `SKILL.md`'s `RULE_HEADING_RE = re.compile(r'^### (PF-\d+\.\d+) — ')`
  (`tools/check_repo.py:850`) and `checklist.md`'s `## PF rules` table — it has **no MC branch at
  all**. If Phase 3 wants the same three-way drift protection (registry / heading / checklist) for
  `MC-*` IDs that `PF-*` IDs already get, that is new code: a second heading regex
  (`^### (MC-\d+) — `), a second checklist-table reader for `## MC rules`, and either a parallel
  function or a generalized one. This is the single largest gap between what exists today and what
  a fully-symmetric `MC-` namespace needs.

---

### 6. Plan-file shape — what Phase 3 plans must reproduce, and the threat-numbering decision

Analog: `.planning/phases/02-rule-catalog-integrity-skill-md-core/02-04-PLAN.md` (closes out a
catalog, final rule additions, allocates final IDs, measures a ceiling — the closest data-flow
match to a Phase 3 plan that finishes filling `MC-` IDs and NUMBERING rows).

**Frontmatter** (`02-04-PLAN.md:1-20`):
```yaml
phase: 02-rule-catalog-integrity-skill-md-core
plan: 04
type: execute
wave: 4
depends_on: [02-03]
files_modified: [...]
autonomous: true
requirements: [CAT-02, CAT-04, CAT-05, CAT-06]
estimate: {tokens, raw_tokens, tasks, confidence}
```
`wave:` is a required frontmatter field expressing intra-phase execution ordering, independent of
`depends_on`. Phase 3's plans must declare both.

**`must_haves` block** (`02-04-PLAN.md:22-59`): `truths` (assertable statements the finished plan
must satisfy), `prohibitions` (MUST NOT statements, often canon-inherited), `artifacts` (path +
provides + a literal `contains` string grep-checkable against the file), `key_links` (from/to file
pairs with a `via` explanation and a `pattern` regex/string that proves the link exists in text).

**Task anatomy** (`02-04-PLAN.md:172-357`): `<task type="auto">`, `<name>`, `<files>`,
`<read_first>` (bullet list of exactly which files/sections to read and why), `<action>` (prose
instructions, often naming exact heading text and exact sentence templates to reproduce
byte-for-byte, e.g. the stated-count sentence), `<verify>` with paired `<automated>`/`<fails_when>`
blocks, `<acceptance_criteria>` (a flat list of shell one-liners with expected output literally
stated), `<done>` (one-sentence completion statement).

**`<automated>` vs `<manual>`/`<human-check>` verify blocks:** `<automated>` blocks are
machine-checkable shell commands with a paired `<fails_when>` predicate (`02-04-PLAN.md:229-236`,
`:319-329`). A `<human-check>` block (`02-04-PLAN.md:330-339`) is prose describing a judgment no
tool in the stack can make — e.g. confirming prose isn't "a compressed copy of an external
standard's rule list," or that applying the whole catalog doesn't flatten the prose. Phase 3's
plans will need `<human-check>` blocks for judgment calls like "does this MC dimension's gap
language read as a genuine completeness finding vs. an invented deficiency" — model these on
`02-04-PLAN.md:330-339`'s two-numbered-question shape.

**`<threat_model>` block** (`02-04-PLAN.md:361-381`): a `## Trust Boundaries` table (Boundary |
Description) followed by `## STRIDE Threat Register` (Threat ID | Category | Component | Severity |
Disposition | Mitigation Plan).

**Threat-ID numbering scheme — explicit flag and directive:** plans `02-01` through `02-06` number
threats `T-2-NN` (verified: `02-01-PLAN.md:705-710`, `T-2-01` through `T-2-05` plus `T-2-SC`,
restarting the counter from `01` in each plan despite sharing phase `02`). Plans `02-07` through
`02-09` instead number theirs `T-02-NN` (verified: `02-07-PLAN.md:532-539`, `T-02-01` through
`T-02-07` plus `T-02-SC`). Both schemes restart their counter at `01` in every single plan file —
neither scheme is phase-wide unique. This collision is on record as having caused a real incident:
a threat-register assembly step silently missed 22 threats because two different ID shapes
(`T-2-` vs `T-02-`) were not recognized as the same namespace by whatever tooling or manual process
assembled the phase-wide register.

**Directive for Phase 3:** pick one scheme — recommend `T-03-NN` (matching the `T-02-NN` form,
zero-padded phase number, since it is the more recent and more collision-resistant of the two
patterns already in use) — and make every plan's threat IDs **phase-wide unique**, not merely
unique within their own plan file (i.e. `03-01` uses `T-03-01`..`T-03-0N`, `03-02` continues from
`T-03-0(N+1)`, rather than every plan restarting at `T-03-01`). State this scheme once, explicitly,
in whichever file plays 02-01's role of "frozen interfaces other plans in this phase must read and
comply with," and do not let any later Phase 3 plan restart the counter.

---

### 7. `SUMMARY.md` shape — and the `requirements-completed:` field's real meaning

Analog: `.planning/phases/02-rule-catalog-integrity-skill-md-core/02-04-SUMMARY.md:1-20`.

Frontmatter shape:
```yaml
phase: 02-rule-catalog-integrity-skill-md-core
plan: 04
subsystem: rule-catalog
tags: [agent-skill, skill-md, rule-catalog, deletion-test, prose-mechanics, ci-checker]
requires: [{phase, provides}]
provides: [...]
affects: [02-05, 02-06]
actuals: {tokens: ...}
requirements-completed: [CAT-02, CAT-04, CAT-05, CAT-06]
```

**`requirements-completed:` records implementation, not verification.** This is confirmed by a
real, already-recorded incident: `02-01-SUMMARY.md:47` lists `requirements-completed: [..., CAT-10,
...]`, and `.planning/REQUIREMENTS.md:21` records the fallout —
```
- [ ] **CAT-10**: ... *implementation shipped; reliability UNVERIFIED. ... Do not re-mark Complete
  from a SUMMARY's `requirements-completed` field — that field records implementation, not
  verification. Closure condition: WINDOWS.md id 4.*
```
CAT-10 was propagated as "Complete" into `.planning/REQUIREMENTS.md` on the strength of appearing
in a SUMMARY's `requirements-completed` list, before the described human/live-harness verification
had actually run. **Directive for Phase 3:** every plan's `requirements-completed:` entry for
AUD-01..03, ART-01..04, MOD-03..05 means "the code/prose for this requirement was written this
plan," never "this requirement is verified done." Any requirement whose closure depends on a
`<human-check>` or a live harness run (e.g. confirming a completeness-audit gap-finding actually
reads as genuine rather than invented, or confirming an artifact-classification line fires
correctly across real drafts) must be marked provisional in `.planning/REQUIREMENTS.md` exactly as
CAT-10 now is, pending its own named closure condition — not marked Complete off the SUMMARY field
alone.

## No Analog Found

| File | Role | Data Flow | Reason |
|---|---|---|---|
| An `MC-`-namespace equivalent of `check_catalog_id_drift` (three-way registry/heading/checklist drift check for MC IDs) | utility / linter check | transform | No existing MC-specific drift check exists; `check_catalog_id_drift` (`tools/check_repo.py:880-922`) is PF-only today (hardcoded `PF_ID_RE`/`RULE_HEADING_RE`/`## PF rules`). Build by generalizing or duplicating, per §5. |
| A per-dimension MC sub-block containment check (equivalent of `pf_subblocks` for PF-1/PF-2) | utility / linter check | transform | `parse_pf_subblocks` (`tools/check_repo.py:311-337`) only recognizes `## PF-<n> sub-blocks` headings; no MC equivalent exists. `check_range_id`'s MC branch only checks "inside *some* MC range," not "inside its *own* dimension's range." Needed only if Phase 3 decides finer-grained enforcement is worth the cost — not required by AUD-01..03 on its face. |

## Metadata

**Files read directly (not projected):** `skills/proof-first/SKILL.md` (full), `NUMBERING.md`
(full), `skills/proof-first/references/checklist.md` (full), `skills/proof-first/references/deletion-test.md`
(full), `skills/proof-first/references/worked-examples.md` (full), `tools/check_repo.py`
(targeted, lines 200-620, 833-1043, 1370-1414, 2050-2330), `.planning/phases/02-.../02-04-PLAN.md`
(full), `.planning/phases/02-.../02-04-SUMMARY.md` (frontmatter), `.planning/phases/02-.../02-01-PLAN.md`
and `02-07-PLAN.md` (threat-register tables), `.planning/REQUIREMENTS.md` (CAT-10 entry), one `git
show --stat` on commit `42607c4`.
**Analog search scope:** `skills/proof-first/`, `tools/check_repo.py`, `NUMBERING.md`,
`.planning/phases/02-rule-catalog-integrity-skill-md-core/*.md`, `.planning/REQUIREMENTS.md`.
