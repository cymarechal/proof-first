---
phase: 04-distribution-worked-examples
plan: 01
subsystem: distribution
tags: [claude-code-plugin, marketplace-manifest, json, mutation-test, check_repo]

requires:
  - phase: 02-rule-catalog-integrity-skill-md-core
    provides: skills/proof-first/SKILL.md's frontmatter (name, metadata.version) as the version source of truth
  - phase: 03-completeness-audit-artifact-patterns
    provides: the stable, unedited SKILL.md this plan reads but never modifies
provides:
  - .claude-plugin/plugin.json and .claude-plugin/marketplace.json, the Claude Code plugin distribution channel's two manifests
  - Three new check_repo.py violation codes enforcing manifest validity, version binding, and publish-location consistency
  - The <owner>/<repo> placeholder mechanism 04-02/04-03/04-04 inherit with no further code change
affects: [04-04-readme-and-install-docs]

actuals:
  tokens: 7367
  tasks: 2
  commits: 2

tech-stack:
  added: []
  patterns:
    - "Stated-value-vs-registry check shape reused for plugin-manifest-version-mismatch (skill frontmatter is the source of truth, manifest states must equal it)"
    - "stdlib json.loads for genuine JSON files, kept distinct from parse_frontmatter's targeted YAML-adjacent extractor"
    - "Owner-segment normalization for publish-location-drift: every carrier position (a full owner/repo URL or a bare owner URL) is reduced to its GitHub account/org segment before comparison, so a repo-level field and an owner-only field compare at the same granularity instead of always disagreeing"

key-files:
  created:
    - .claude-plugin/plugin.json
    - .claude-plugin/marketplace.json
  modified:
    - tools/check_repo.py

key-decisions:
  - "Decision checkpoint resolved by orchestrator: adopt the proposal verbatim (plugin name and marketplace name both proof-first, marketplace source \"./\") and keep the publish-location placeholder <owner>/<repo> — the single substitution point is every homepage/repository/owner.url field in both manifests, verified identical by publish-location-drift."
  - "publish-location-drift compares GitHub owner segments, not full owner/repo strings, because owner.url structurally carries only an owner segment; comparing it against a full owner/repo string as literal text would misfire on every correctly-configured manifest. Declared as an explicit ceiling in the module docstring: a repo-name-only drift under an unchanged owner is not detected."

requirements-completed: [DIST-02]

coverage:
  - id: D1
    description: "Both plugin manifests exist, parse as JSON, restate one identical set of facts, and state the skill's frontmatter version"
    requirement: DIST-02
    verification:
      - kind: unit
        ref: "tools/check_repo.py --self-test (plugin-manifest-version-mismatch, plugin-manifest-invalid fixtures)"
        status: pass
      - kind: integration
        ref: "python3 tools/check_repo.py (live run against the real manifests)"
        status: pass
    human_judgment: false
  - id: D2
    description: "A malformed manifest, a missing required key, or a plugin name diverging from the shipped skill folder is a CI-enforced build failure"
    verification:
      - kind: unit
        ref: "tools/check_repo.py --mutation-test (plugin-manifest-invalid mutation)"
        status: pass
    human_judgment: false
  - id: D3
    description: "Every carrier stating this repository's publish location states one identical value (the frozen placeholder), so resolving the real owner/repo later is a single verified substitution"
    verification:
      - kind: unit
        ref: "tools/check_repo.py --mutation-test (publish-location-drift mutation)"
        status: pass
    human_judgment: false
  - id: D4
    description: "DIST-02's live install flow (claude plugin marketplace add + claude plugin install) actually installs the plugin from this repository"
    human_judgment: true
    rationale: "Requires a live harness and a reachable published repository; no file-reading checker observes this. Recorded as unresolved edge A4-E2 and a manual smoke test in 04-VALIDATION.md's Manual-Only table."
status: complete
duration: ~16min
completed: 2026-09-17
---

# Phase 4 Plan 1: Plugin Channel Manifests and Version/Location Enforcement Summary

**Claude Code plugin distribution wired end-to-end on one thin slice: two new `.claude-plugin/*.json` manifests bound to `SKILL.md`'s frontmatter version and to each other by three new CI-enforced `check_repo.py` codes, discrimination-proven 33 then 35, up from 32.**

## Performance

- **Duration:** ~16 min
- **Started:** 2026-09-17T06:06:00Z (approx, from STATE.md's prior session timestamp)
- **Completed:** 2026-09-17T06:21:36Z
- **Tasks:** 2 (plus one pre-resolved decision checkpoint)
- **Files modified:** 3 (2 created, 1 modified)

## Accomplishments

- Created `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` at the repository root, mirroring the real, working SimpleEnglish manifest shapes field-for-field: `name: "proof-first"` equal to the `skills/proof-first/` folder name, `source: "./"` so the harness auto-discovers `skills/*/` and (later) `output-styles/*.md` with no component-override key, and the frozen `<owner>/<repo>` placeholder in `homepage`/`repository`/`owner.url` pending the real publish location.
- Added `plugin-manifest-version-mismatch`: parses `SKILL.md`'s frontmatter `metadata.version` via a new targeted regex extractor (`_skill_metadata_version`, built on the existing `parse_frontmatter`) and compares it against both manifests' `version` fields, making NUMBERING.md's Phase-1-stated version-match obligation mechanical.
- Added `plugin-manifest-invalid`: asserts both manifests are valid JSON, carry every required key, `plugin.json`'s `name` equals the one shipped skill folder, and `marketplace.json`'s `owner`/`plugins`/`source` shape is correct.
- Added `publish-location-drift`: asserts every existing carrier of this repository's publish location (both manifests' `homepage`/`repository`/`owner.url`, and README's future install-command arguments) states the same GitHub owner segment, with the full prospective carrier list (`PUBLISH_LOCATION_CARRIERS`) already including `README.md` so `04-04` inherits enforcement with no code change.
- `.claude-plugin` added to `MUTATION_SOURCES` so the mutation-test control copy carries the new manifests — without this, both new mutations would have been silently inert (the exact trap the plan's own interfaces flagged).
- Mutation-test's discrimination-proven total moved from 32 to 33 (Task 1) then to 35 (Task 2), CONTROL still reporting 0 unexpected violations, no code reported FIRE-ONLY.

## Task Commits

1. **Task 1: End-to-end "install as a Claude Code plugin" — manifests plus the version binding, proven live** - `7f09e0d` (feat)
2. **Task 2: Close the plugin channel's two remaining enforcement gaps — `plugin-manifest-invalid` and `publish-location-drift`** - `d790b50` (feat)

**Plan metadata:** committed alongside this SUMMARY.

## Files Created/Modified

- `.claude-plugin/plugin.json` - Claude Code plugin manifest (name, version, author, license, keywords, placeholder homepage/repository)
- `.claude-plugin/marketplace.json` - Marketplace manifest with one plugin entry, `source: "./"`, restating `plugin.json`'s values
- `tools/check_repo.py` - Three new violation codes (`plugin-manifest-version-mismatch`, `plugin-manifest-invalid`, `publish-location-drift`), their check functions, self-test fixtures, and `MUTATIONS` entries; `.claude-plugin` added to `MUTATION_SOURCES`

## Decisions Made

- **Checkpoint resolution (orchestrator-supplied, per the plan's own accepted options):** adopted the proposal verbatim — `proof-first` as one identifier across the skill folder, plugin manifest, and marketplace manifest; `source: "./"`; publish location kept as the recorded placeholder `<owner>/<repo>` rather than guessed. This repository has no configured git remote (`git remote -v` prints nothing), so the real value is genuinely unknown. The single substitution point for the real value later is every `homepage`/`repository`/`owner.url` field in both manifests — `publish-location-drift` verifies they all currently agree on the placeholder, so a future substitution that misses one carrier fails the build immediately.
- **`publish-location-drift` compares GitHub owner segments, not full `owner/repo` strings.** The plan's action text describes `owner.url` as "contributing only its owner segment" to the same comparison set as `homepage`/`repository`'s full `owner/repo` values. Implemented literally (mixing full and owner-only strings in one set), this would make every correctly-configured `marketplace.json` self-report a false disagreement between its own `owner.url` (bare owner) and its own `homepage`/`repository` (full owner/repo) — breaking the plan's own required `check_repo: 0 violations` baseline. Resolved by normalizing every position (from all three carriers) down to its owner segment before comparison. This is a declared, disclosed ceiling in the module docstring: the check catches an owner-account drift; it does not catch a repository-name-only drift under an unchanged owner. Documented here as a deviation under Rule 1 (the literal reading was a bug against the plan's own stated invariant, not an ambiguity left open by design).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed a self-introduced line-wrap that split the "Declared ceiling:" anchor across two lines**
- **Found during:** Task 2, running the `Declared ceiling` count acceptance criterion
- **Issue:** The `plugin-manifest-version-mismatch` docstring bullet added in Task 1 wrapped the phrase as "...Declared\n                      ceiling: ..." — splitting the two-word anchor across a line boundary, exactly the class of authoring trap this repository's own interfaces block names as "Trap 1" (a prior instance in `02-04`).
- **Fix:** Moved the wrap point (not the wording) so "Declared ceiling:" sits entirely on one physical line, matching every other bullet's convention.
- **Files modified:** `tools/check_repo.py`
- **Verification:** `grep -c 'Declared ceiling' tools/check_repo.py` moved from 31 to 32, satisfying the acceptance criterion's "at least 32" bound.
- **Committed in:** `d790b50` (Task 2 commit)

**2. [Rule 4-adjacent design resolution, documented not escalated] `publish-location-drift`'s owner-segment normalization**
- See "Decisions Made" above. This is recorded here rather than as a Rule 4 architectural-change checkpoint because it is an implementation detail of an already-specified check (the plan names the exact code, its file list, and its behavior examples) rather than a new architectural surface; the alternative reading would have broken the plan's own explicit success criterion, so implementing the only reading consistent with that criterion is a Rule 1 bug-prevention choice, not a new decision requiring a stop.

---

**Total deviations:** 2 (1 self-caught authoring bug, 1 documented implementation-detail resolution). **Impact on plan:** Neither affects scope or requirements; both are disclosed for auditability. No scope creep.

## Issues Encountered

- The plan's own literal acceptance-criterion script for verifying version equality (`re.search(r'^version:\s*"?([^"\s]+)"?\s*$', ...split('---')[1], re.M)`) fails when run exactly as written, because it applies the anchored regex directly to the raw, still-indented frontmatter text rather than to the dedented opaque string `parse_frontmatter` produces. The actual invariant — `SKILL.md`'s `metadata.version`, `plugin.json`'s `version`, and `marketplace.json`'s plugin-entry `version` are all `"0.1.0"` — was independently verified with the same regex applied to a per-line-stripped copy of the text (matching what the shipped `_skill_metadata_version` function actually does), and holds: `True`. This is a defect in the plan's own verification script, not in the implementation; following the `03-04` precedent, it is recorded here rather than force-fit or silently worked around. Every other Task 1 and Task 2 acceptance criterion, including all three `check_repo.py --self-test`/`--mutation-test`/live-run commands, the JSON-shape criteria, and the scratch-copy mutation proof, ran and passed exactly as written.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- The plugin manifest channel (DIST-02) is structurally complete and CI-enforced: both manifests exist, parse, agree with each other and with the shipped skill's version, and carry no component-override key.
- **DIST-02 is only partially verified.** This plan verifies the structural half only (manifests exist, parse, and agree). Whether a real `claude plugin marketplace add` followed by `claude plugin install proof-first@proof-first` actually installs is a live harness-and-network behavior no file-reading checker observes — recorded as unresolved edge A4-E2, deferred to a manual smoke test in `04-VALIDATION.md`'s Manual-Only table and to end-of-phase UAT.
- **DIST-01 is not addressed by this plan's `requirements-completed`.** This plan builds the publish-location mechanism (`publish-location-drift`, the `<owner>/<repo>` placeholder) every skills-CLI install command will depend on, but the install command itself is authored in `04-04` and cannot be exercised without a published repository — recorded as unresolved edge A4-E1. `DIST-01` is intentionally omitted from this SUMMARY's `requirements-completed` field.
- The publish location is a recorded, disclosed placeholder (`<owner>/<repo>`), not a real value — `.planning/WINDOWS.md` entry 11 (new, `open`, kind `unrun-verify`) names the placeholder, its carriers, and routes closure to Phase 6's LEG-04 launch gate.
- `skills/proof-first/SKILL.md` is untouched (verified byte-identical via `git diff --stat` across both task commits showing no change to that path) — its 177-token margin remains available for `04-03`.
- Neither `output-styles/`, `prompts/`, `examples/before-after.md`, nor `tools/generate_derivatives.py` exists yet — `04-02`/`04-03` own them, matching this plan's tracer scope.
- Ready for `04-02`.

## Self-Check: PASSED

- `[ -f .claude-plugin/plugin.json ]` → FOUND
- `[ -f .claude-plugin/marketplace.json ]` → FOUND
- `git log --oneline --all | grep -q 7f09e0d` → FOUND
- `git log --oneline --all | grep -q d790b50` → FOUND
- `python3 tools/check_repo.py` → `check_repo: 0 violations`
- `python3 tools/check_repo.py --self-test` → PASS, 35 codes verified including all three new ones
- `python3 tools/check_repo.py --mutation-test` → `mutation-test PASS: 35 codes discrimination-proven`, CONTROL `0 violations ... (0 known-open ..., 0 unexpected)`, 0 FIRE-ONLY lines
- Re-ran every plan-level `<acceptance_criteria>` script from both tasks: all pass except the one script defect documented under "Issues Encountered" (the underlying invariant it was meant to check was independently confirmed true)

---
*Phase: 04-distribution-worked-examples*
*Completed: 2026-09-17*
