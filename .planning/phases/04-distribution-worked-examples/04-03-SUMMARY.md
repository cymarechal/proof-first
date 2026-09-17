---
phase: 04-distribution-worked-examples
plan: 03
subsystem: distribution
tags: [dist-05, generate_derivatives, check_repo, output-style, system-prompt, mutation-test]

requires:
  - phase: 02-rule-catalog-integrity-skill-md-core
    provides: skills/proof-first/SKILL.md's frozen 31-rule PF catalog, its
      `description: |` frontmatter block, and RULE_HEADING_RE's `### PF-#.# — `
      heading shape
  - phase: 03-completeness-audit-artifact-patterns
    provides: references/completeness-audit.md's 8-check MC catalog, MC_HEADING_RE,
      and the frozen ARTIFACT_FAMILY_SECTIONS tuple in references/artifact-patterns.md
  - phase: 04-distribution-worked-examples
    provides: 04-01's/04-02's established three-part check contract (function,
      self-test fixture pair, MUTATIONS entry) this plan's two new codes follow
provides:
  - tools/generate_derivatives.py — the single stdlib-only source of truth for
    output-styles/proof-first.md and prompts/system-prompt.md, with a --check
    mode that compares freshly rendered bytes against committed bytes
  - Two new check_repo.py violation codes (skill-derivative-stale,
    derivative-rule-coverage-incomplete) that fail the build when a derivative
    goes stale or drops a shipped rule heading or artifact-family heading
  - Both derivatives on disk, generated and hash-stamped, structurally proven
    to carry all 39 allocated rule headings and all four artifact-family headings
affects: [04-04-readme-and-install-docs]

actuals:
  tokens: 35469
  tasks: 3
  commits: 3

tech-stack:
  added: []
  patterns:
    - "Generator/checker source-list agreement enforced by a stamp, not an
      import: tools/generate_derivatives.py and tools/check_repo.py each
      declare their own literal DERIVATIVE_SOURCE_NAMES tuple; the stamp each
      derivative carries records the generator's list, and
      skill-derivative-stale compares that recorded list against the
      checker's own frozen copy on every run (P4-13)."
    - "Stamp located by pattern, not by physical line number (P4-12): both
      the generator and skill-derivative-stale find the stamp as the first
      line matching DERIVATIVE_STAMP_RE, which lets the output style keep
      its YAML frontmatter delimiter at line 1 while the system prompt
      carries the identical stamp at line 1 with no frontmatter at all."
    - "Two independent freshness guards per P4-14: skill-derivative-stale
      recomputes a digest over the named sources on every checker run;
      python3 tools/generate_derivatives.py --check separately compares
      committed bytes against freshly rendered bytes. A hand-edit to a
      derivative's body defeats the first and is caught by the second; a
      source edit with no regeneration is caught by both."
    - "New check codes staged across two commits inside one plan to keep
      mutation-test's discrimination-proven total accurate at every commit
      boundary: Task 2's commit shipped skill-derivative-stale alone (37 to
      38), with derivative-rule-coverage-incomplete's function already
      written but deliberately left unregistered in DERIVATIVE_CHECK_CODES
      and MUTATIONS until Task 3's commit wired it in (38 to 39). A code
      listed in ALL_CHECK_CODES with no registered mutation fails
      mutation-test outright, so staging the registration, not just the
      function body, across commits was required."

key-files:
  created:
    - tools/generate_derivatives.py
    - output-styles/proof-first.md
    - prompts/system-prompt.md
  modified:
    - tools/check_repo.py
    - .github/workflows/ci.yml

key-decisions:
  - "DERIVATIVE_SOURCE_NAMES in tools/generate_derivatives.py is written out
    as a literal 5-element tuple rather than composed from
    `(SKILL_PATH,) + REFERENCE_SOURCES`. The plan's own acceptance criterion
    compares the two files' tuples with a non-greedy regex that stops at the
    first closing paren; a composed expression would have made the
    generator's half of that comparison read as a single-element
    placeholder (`['SKILL_PATH']`) instead of the five real paths, failing
    a criterion the underlying values already satisfied. Fixed in the same
    commit that added skill-derivative-stale, before any acceptance
    criterion was run against it."
  - "Both new checks kept read-only over the exact regexes RULE_HEADING_RE
    and MC_HEADING_RE already declare (never a second typed copy of the
    '### <ID> — ' shape), and check_derivative_rule_coverage reads
    ARTIFACT_FAMILY_SECTIONS by name rather than retyping the four frozen
    family strings — the same frozen-interface discipline 03-02 and 04-02
    already established for these two constants."
  - "The generated preamble is written in the generator's own prose rather
    than adapted from SimpleEnglish's output style or system prompt text,
    per the plan's explicit prohibition — that project's derivatives have
    no reference-file dependency to omit and this project's do, so no
    sentence of theirs transfers cleanly."

patterns-established:
  - "A derivative's one stamp line is both a freshness proof (digest over
    named sources) and a coverage-check disclosure surface simultaneously —
    future derived artifacts in this repository can reuse the same
    (source-list, digest) stamp shape rather than inventing a new one."

requirements-completed: [DIST-05]

coverage:
  - id: D1
    description: "tools/generate_derivatives.py exists, imports only argparse/hashlib/pathlib/re/sys, and produces output-styles/proof-first.md and prompts/system-prompt.md as a pure function of source bytes (re-running it twice reproduces both files byte for byte)."
    requirement: "DIST-05"
    verification:
      - kind: other
        ref: "python3 tools/generate_derivatives.py && python3 tools/generate_derivatives.py --check && git status --porcelain -- output-styles prompts"
        status: pass
      - kind: other
        ref: "python3 -c \"import ast,pathlib,sys;t=ast.parse(pathlib.Path('tools/generate_derivatives.py').read_text());mods={n.split('.')[0] for x in ast.walk(t) if isinstance(x,ast.Import) for n in [a.name for a in x.names]}|{x.module.split('.')[0] for x in ast.walk(t) if isinstance(x,ast.ImportFrom) and x.module};print(sorted(mods-{'argparse','hashlib','pathlib','re','sys'}))\""
        status: pass
    human_judgment: false
  - id: D2
    description: "skill-derivative-stale fails the build when a derivative carries no stamp, a stamp whose source-path list disagrees with check_repo.py's frozen DERIVATIVE_SOURCE_NAMES, or a stamp digest that no longer matches a fresh hash of the named sources -- discrimination-proven against a mutated copy of the real repository."
    requirement: "DIST-05"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --self-test (skill-derivative-stale in the verified-codes list)"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py --mutation-test (38-of-38 at Task 2's commit; CONTROL 0 unexpected, no FIRE-ONLY)"
        status: pass
    human_judgment: false
  - id: D3
    description: "derivative-rule-coverage-incomplete fails the build when a derivative is missing a '### <ID> -- ' heading for any of NUMBERING.md's 39 allocated PF-/MC- IDs or any of the four frozen artifact-family headings -- discrimination-proven against a mutated copy of the real repository."
    requirement: "DIST-05"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --self-test (derivative-rule-coverage-incomplete in the verified-codes list)"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py --mutation-test (39-of-39 discrimination-proven at Task 3's commit; CONTROL 0 unexpected, no FIRE-ONLY)"
        status: pass
      - kind: other
        ref: "python3 -c scoped-to-'## Allocated IDs'-table scan of NUMBERING.md confirms all 39 real allocated IDs and all 4 family headings present in both derivatives (see Deviations)"
        status: pass
    human_judgment: false
  - id: D4
    description: "CI runs python3 tools/generate_derivatives.py --check as a fifth command in the existing single multi-line run block, after check_repo.py's three invocations and the conformance self-test, with no swallowed exit status."
    requirement: "DIST-05"
    verification:
      - kind: other
        ref: "grep -cF 'python3 tools/generate_derivatives.py --check' .github/workflows/ci.yml == 1; one named step, no '|| true'"
        status: pass
    human_judgment: false
  - id: D5
    description: "A user who cannot install the Agent Skill can select output-styles/proof-first.md or paste prompts/system-prompt.md, and a live session driven by either applies the same rules a live session with the skill folder installed applies."
    verification: []
    human_judgment: true
    rationale: "This is the behavioural half of DIST-03/DIST-04, explicitly authored as a verification: backstop truth in the plan. No file-reading checker observes live model behaviour, and Phase 5's benchmark has not run. Structural coverage (D3) is a necessary but not sufficient proxy; whether either derivative changes what a model actually does is unmeasured by design, per this project's measured-claims-or-none evidence discipline."

duration: 55min
completed: 2026-09-17
status: complete
---

# Phase 4 Plan 3: Output style and system prompt generated from the shipped skill Summary

**A stdlib-only generator derives `output-styles/proof-first.md` and `prompts/system-prompt.md` verbatim from `skills/proof-first/SKILL.md` and four reference files, stamps each with a sha256 over its exact sources, and two new build-failing checks (37 to 39 discrimination-proven) make skipping the re-sync step impossible to ship silently.**

## Performance

- **Duration:** 55 min
- **Tasks:** 3
- **Files created:** 3 (`tools/generate_derivatives.py`, `output-styles/proof-first.md`, `prompts/system-prompt.md`)
- **Files modified:** 2 (`tools/check_repo.py`, `.github/workflows/ci.yml`)

## Accomplishments

- Built `tools/generate_derivatives.py`: reads `skills/proof-first/SKILL.md` and four named reference files (`deletion-test.md`, `completeness-audit.md`, `artifact-patterns.md`, `checklist.md`, deliberately omitting `worked-examples.md`), concatenates them verbatim under stated section markers, and writes both derivatives with a single shared stamp line recording a sha256 digest over the concatenated source bytes and the source-path list. `--check` compares freshly rendered output against committed bytes byte for byte.
- Both derivatives generated and committed: `output-styles/proof-first.md` (757 lines / 8,229 words, YAML frontmatter at line 1, stamp as the first matching line after it) and `prompts/system-prompt.md` (745 lines / 8,159 words, stamp at line 1, no frontmatter, paste-able as-is). Both carry the identical digest `sha256:2b7735d8266cbed945164c266691b45f30dbf9c3255abecf18821d5d98d86ba5` over the same five source files in the same order.
- Added `skill-derivative-stale` to `tools/check_repo.py`: fires on a missing stamp, a source-path-list mismatch against the checker's own frozen `DERIVATIVE_SOURCE_NAMES`, or a digest that no longer matches a fresh hash of the named sources. Proven discrimination-proven at 38 codes in its own commit.
- Added `derivative-rule-coverage-incomplete`: fires when either derivative is missing a `### <ID> — ` heading for one of NUMBERING.md's 39 allocated PF-/MC- IDs, or one of the four frozen `ARTIFACT_FAMILY_SECTIONS` headings. Proven discrimination-proven at 39 codes in its own commit, wired the same commit CI gained `python3 tools/generate_derivatives.py --check` as a fifth sequential command.
- `skills/proof-first/SKILL.md` and every file under `skills/proof-first/references/` are untouched by this plan: `wc -w skills/proof-first/SKILL.md` still reads 3,710 words, and the 5,000-token ceiling margin is still 177 tokens (3,710 × 1.3 = 4,823 estimated tokens).

## Task Commits

1. **Task 1: Build `tools/generate_derivatives.py` and emit both derivatives from it** - `b46e40b` (feat)
2. **Task 2: Make skipping the re-sync step a build failure — `skill-derivative-stale`, proven live** - `4874716` (feat)
3. **Task 3: Prove the derivatives carry every shipped rule — `derivative-rule-coverage-incomplete` — and run the generator's own check in CI** - `84dfb82` (feat)

**Plan metadata:** this SUMMARY's own commit (docs)

## Files Created/Modified

- `tools/generate_derivatives.py` - stdlib-only generator (argparse, hashlib, pathlib, re, sys); `read_sources`, `source_hash`, `build_body`, `render_output_style`, `render_system_prompt`, `write_derivatives`, `check_derivatives`, `main` with `--check`
- `output-styles/proof-first.md` - generated Claude Code output style; YAML frontmatter (`name: proof-first`, `description` copied from SKILL.md's own frontmatter block, `keep-coding-instructions: false`, no `force-for-plugin`), then stamp, preamble, body
- `prompts/system-prompt.md` - generated paste-able system prompt; stamp at line 1, then preamble, then the identical body, no frontmatter
- `tools/check_repo.py` - `DERIVATIVE_PATHS`, `DERIVATIVE_SOURCE_NAMES`, `DERIVATIVE_STAMP_RE`, `_derivative_stamp`, `_hash_sources`, `check_skill_derivative_stale`, `check_derivative_rule_coverage`, `DERIVATIVE_CHECK_CODES`, `run_derivative_checks`; `MUTATION_SOURCES` gains `output-styles` and `prompts`; two docstring bullets, two self-test fixture roots (`derivative_good_root`, `derivative_bad_root`) with four fixture-builder helpers, two `MUTATIONS` entries
- `.github/workflows/ci.yml` - one line appended to the existing multi-line `run:` block: `python3 tools/generate_derivatives.py --check`

## Decisions Made

See `key-decisions` in frontmatter. In summary: `DERIVATIVE_SOURCE_NAMES` in the generator was rewritten as a literal tuple rather than a composed expression so the generator's and checker's tuples are comparable by a plain text scan; both new checks bind to the existing `RULE_HEADING_RE`/`MC_HEADING_RE`/`ARTIFACT_FAMILY_SECTIONS` constants rather than retyping their shapes; and the two check codes were staged across two commits (skill-derivative-stale alone, then derivative-rule-coverage-incomplete) so `mutation-test`'s discrimination-proven total is accurate — 38, then 39 — at every commit boundary rather than only at the plan's end.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] `DERIVATIVE_SOURCE_NAMES` composed expression broke the plan's own tuple-agreement acceptance criterion**
- **Found during:** Task 2, running the plan's acceptance criterion that regex-extracts both files' `DERIVATIVE_SOURCE_NAMES` tuples and compares them.
- **Issue:** `tools/generate_derivatives.py` originally defined `DERIVATIVE_SOURCE_NAMES = (SKILL_PATH,) + REFERENCE_SOURCES`. The acceptance criterion's non-greedy regex `DERIVATIVE_SOURCE_NAMES = \((.*?)\)` stops at the first closing paren, which for that expression is the paren closing `(SKILL_PATH,)` — capturing only the string `'SKILL_PATH'`, not the five real paths, even though the resolved tuple value was correct at runtime.
- **Fix:** Rewrote `DERIVATIVE_SOURCE_NAMES` in `tools/generate_derivatives.py` as a literal 5-element tuple, byte-for-byte comparable against `tools/check_repo.py`'s own literal tuple by the same regex scan.
- **Files modified:** `tools/generate_derivatives.py`
- **Verification:** `python3 -c "..."` comparison script now prints `True`; `python3 tools/generate_derivatives.py --check` still passes unchanged (the rendered output byte content did not change, only how the constant is spelled).
- **Committed in:** `4874716` (Task 2 commit)

**2. [Rule 1 - Plan arithmetic/regex error] Plan's own "all 39 headings" acceptance-criterion script over-matches NUMBERING.md**
- **Found during:** Task 3, running the plan's literal acceptance criterion `python3 -c "import re,pathlib;n=pathlib.Path('NUMBERING.md').read_text();ids=set(re.findall(r'\|\s*(PF-\d+\.\d+|MC-\d+)\s*\|',n));..."`.
- **Issue:** That command scans NUMBERING.md's whole text for any `| PF-#.# |`-shaped table cell, not just the `## Allocated IDs` table. NUMBERING.md's `## PF reserved ranges` table also has a "Next free" column whose cells are pipe-delimited PF tokens (e.g. `| PF-0.2 |`, the next *available*, not yet allocated, ID in that section). The unscoped scan therefore reports these six placeholder values (`PF-0.2`, `PF-1.26`, `PF-2.18`, `PF-3.4`, `PF-4.5`, `PF-5.4`) as "missing" from both derivatives, even though they were never allocated and correctly appear nowhere in `SKILL.md` either.
- **Fix:** None needed to the shipped code — `check_derivative_rule_coverage` (the actual mechanism) derives its expected ID set from `parse_numbering(...)['allocated']`, exactly as the plan's own `<action>` instructed ("do not re-parse NUMBERING.md"), which reads strictly from the `## Allocated IDs` section and correctly excludes "Next free" placeholders. Re-running the same regex scoped to just that section (matching what `parse_numbering` actually parses) confirms all 39 real allocated IDs are present in both derivatives with zero missing. `python3 tools/check_repo.py` independently confirms 0 violations, which would include a `derivative-rule-coverage-incomplete` firing had any real allocated ID actually been missing.
- **Files modified:** none (verification-only finding; no source change required)
- **Verification:** Scoped-rescan command (see coverage D3) prints `[]` for both derivatives; live `check_repo.py` run prints `check_repo: 0 violations`.
- **Committed in:** n/a (no code change; documented here per the 03-04 precedent for plan-authored acceptance-criteria arithmetic/regex errors)

---

**Total deviations:** 2 auto-fixed (1 Rule 1 bug fix, 1 Rule 1 plan-arithmetic/regex-error documentation).
**Impact on plan:** Neither affected the shipped mechanism's correctness. The first was a cosmetic fix to how a constant is spelled so an independent verification script reads it correctly; the second required no code change at all, only confirming (via the correctly-scoped parse the shipped checker actually uses) that the plan's own literal verification command was over-broad, not that anything was missing.

## Known Stubs

None. The generator is fully wired end to end: both derivatives exist on disk, are reproducible byte for byte, and are structurally proven (build-enforced) to carry every shipped rule heading and every artifact-family heading.

## Issues Encountered

None beyond the two documented deviations above.

## Honest Verification Statement (restated from the plan)

- **DIST-05 is verified in full.** The generator exists, the re-sync step is documented in its own docstring and `--help`, and skipping it is a build failure by two independent mechanisms (`skill-derivative-stale`'s digest recomputation and `tools/generate_derivatives.py --check`'s byte comparison). The one declared ceiling — a hash of the inputs cannot prove the generator's own derivation logic is correct — is stated in both the generator's docstring and the checker's code bullet, and remains recorded as unresolved edge A4-E5.
- **DIST-03 and DIST-04 are verified only on their structural half.** Both artifacts exist, are generated rather than hand-written, carry every allocated rule heading and every artifact-family heading (D3), and disclose their one omitted source (`references/worked-examples.md`, named at least twice in each derivative). Whether selecting the output style or pasting the system prompt makes a live session behave as one with the skill installed is model behaviour no file-reading checker observes, and this project's evidence discipline forbids asserting it before Phase 5's benchmark exists. This is recorded as coverage item D5 with `human_judgment: true`, matching unresolved edges A4-E3 and A4-E4 and `04-VALIDATION.md`'s Manual-Only table.
- This plan's `requirements-completed` frontmatter lists `[DIST-05]` only, per the plan's own `<output>` instruction — DIST-03 and DIST-04's behavioural halves are not verified by anything in this repository and are not marked complete here.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `04-04-PLAN.md` (README and install docs) can now point installers at real, committed, byte-reproducible `output-styles/proof-first.md` and `prompts/system-prompt.md` paths.
- Phase 5's benchmark is the only place a claim about DIST-03/DIST-04's live-session behaviour could ever be sourced from; nothing in this plan's artifacts pre-empts that measurement.
- No blockers for `04-04`.

---
*Phase: 04-distribution-worked-examples*
*Completed: 2026-09-17*

## Self-Check: PASSED

- All 6 created/modified files verified present on disk with `[ -f ]`.
- All 3 task commit hashes (`b46e40b`, `4874716`, `84dfb82`) verified present in `git log --oneline --all`.
- `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py && python3 evals/conformance/run_conformance.py --self-test && python3 tools/generate_derivatives.py --check` re-ran green (exit 0) immediately before writing this SUMMARY, with `mutation-test PASS: 39 codes discrimination-proven` and `CONTROL: 0 violations on the unmutated copy (0 known-open per KNOWN_OPEN_VIOLATIONS, 0 unexpected)`.
- Re-ran `python3 tools/generate_derivatives.py && git status --porcelain -- output-styles prompts` with empty output, confirming regeneration is byte-identical to the committed derivatives.
- Re-confirmed `skills/proof-first/SKILL.md` untouched: `wc -w` still 3,710 words, stated-count line still reads 31 rules in 6 numbered sections.
