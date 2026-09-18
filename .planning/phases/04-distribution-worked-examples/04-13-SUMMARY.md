---
phase: 04-distribution-worked-examples
plan: 13
subsystem: docs
tags: [proof-first, readme, checker, output-style, gap-closure, DIST-06]

# Dependency graph
requires:
  - phase: 04-distribution-worked-examples
    provides: "examples/before-after.md repaired by 04-12 (wave 1); 04-UAT.md's G-04-4 diagnosis of the false route-3 install claim"
provides:
  - "readme-output-style-destination-missing: a 48th discrimination-proven violation code asserting README names a destination directory for the output-style route"
  - "README's ## Install section stating the copy step, its destination, and what has not been observed for route 3, and no step for route 4"
  - "A tracked WINDOWS unrun-verify entry (id 16) for the one link this environment cannot observe: a live Claude Code session listing the copied style"
affects: [phase-04-end-of-phase-uat, phase-6-leg-04-launch-gate]

# Actuals (#2632) — pairs with the plan's `estimate` to calibrate future estimates.
# Same estimateTokens scale (chars/4 over the realized diff), never a harness token count.
actuals:
  tokens: 7161
  tasks: 3
  commits: 3

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Dedicated fixture-pair-per-code discipline (Phase 4, 04-09/04-13): a new README code gets its own _good_/_bad_ fixture pair rather than reusing an existing fixture that would incidentally trip it, closing the class CR-01/self-test-case-11 already paid for twice."

key-files:
  created: []
  modified:
    - tools/check_repo.py
    - README.md
    - .planning/WINDOWS.md

key-decisions:
  - "Refused a wider 'route is executable' code and registered only the narrow presence fact (README names a destination directory), matching the mechanisability assessment's explicit reasoning: proving route executability means observing another product's runtime, which no code in this repository can do, and a wider name would repeat the exact overstatement CR-01 already closed for marketplace.json."
  - "Matched the mutation on the shorter, project-level destination literal ('.claude/output-styles/') rather than the longer user-level form, because the user-level form contains the project-level form as a substring — matching only the longer literal would leave the project-level sentence behind and the mutation would silently not fire."
  - "Used a dedicated _good_readme_output_style()/_bad_readme_output_style()/_no_route_readme_output_style() fixture triple rather than reusing _good_readme_install()/_bad_readme_install(), both of which name the output-style path with no destination and would have proven this code incidentally rather than deliberately."
  - "Regenerated .planning/WINDOWS.md's rendered table for pre-existing entry 15 (a backslash-escaping drift unrelated to this plan, introduced before this plan started) via the module's own renderLedger(), because gsd-tools windows append refuses to write while any row disagrees with its own fenced JSON source of truth. Content and JSON untouched; this is the tool's own documented remediation path (regenerate the table), not a hand-edit."

requirements-completed: []  # DIST-06 intentionally NOT marked complete — see "DIST-06 status" below.

coverage:
  - id: D1
    description: "readme-output-style-destination-missing exists, fires red on the shipped README.md before the repair (measured this session, quoted verbatim below), is silent after it, and is proven in both directions by a dedicated fixture pair plus a --mutation-test row against the real file."
    requirement: "DIST-06"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py (0 violations post-repair, 1 violation pre-repair with the exact quoted line); python3 tools/check_repo.py --self-test (48 codes, readme-output-style-destination-missing listed); python3 tools/check_repo.py --mutation-test (mutation-test PASS: 48 codes discrimination-proven, OK line for the new code); destination-removal probe (True); git diff --stat -- examples skills output-styles prompts (empty)"
        status: pass
    human_judgment: false
    rationale: ""
  - id: D2
    description: "README's ## Install section states route 3's copy step and destination directory, states route 4 needs no step beyond the clone, and states plainly that a live /config listing has not been observed here — replacing the false 'routes 3 and 4 work today, from a local clone' claim G-04-4 identified."
    requirement: "DIST-06"
    verification:
      - kind: other
        ref: "grep -cF '~/.claude/output-styles/' README.md == 2; grep -cF 'cp output-styles/proof-first.md' README.md == 1; grep -cF 'work today, from a local clone' README.md == 0; hand read of ## Install (verification item 7)"
        status: pass
    human_judgment: true
    rationale: "Whether a first-time evaluator actually experiences the Install section as clear and actionable is a human-judgment question the plan explicitly carries as a `verification: backstop` truth. The mechanical probes prove the specific false claim is gone and the copy step is stated; they do not certify the prose reads well to a cold reader — that is WINDOWS entry 12's residual, still open."
  - id: D3
    description: "Four README credibility defects folded in: the lead-in matches the actual vertical layout and is cut from 63 words to three short lines while keeping the deal-brief disclosure; a namespace pointer naming NUMBERING.md/checklist.md sits directly beneath the applied-rules footer; the placeholder is disclosed once (confirmed, not re-edited — Task 1 already merged it); ## Status's 18-line unbroken paragraph is broken into five paragraphs with no word changed."
    requirement: "DIST-06"
    verification:
      - kind: other
        ref: "phrase-absence probes (0,0,0 for the three retired phrasings); first-✗-line probe (13, <=20); NUMBERING.md-first-named probe (18, <=25); whitespace-normalised Status-section comparison against HEAD (True); ✗/✓/Rules-applied line membership probe against examples/before-after.md ([])"
        status: pass
    human_judgment: false
    rationale: ""
  - id: D4
    description: "One WINDOWS unrun-verify entry (id 16) tracks the last unobserved link — a live Claude Code session listing and applying the copied style — routed to Phase 6 LEG-04 alongside entries 11 and 12. Entry 12 stays open, narrowed. DIST-06 stays unchecked in REQUIREMENTS.md."
    requirement: "DIST-06"
    verification:
      - kind: other
        ref: "JSON probe: exactly one open unrun-verify entry naming 'output-style' (id 16); entry 12 status == open; grep -c '^- \\[ \\] \\*\\*DIST-06\\*\\*' REQUIREMENTS.md == 1"
        status: pass
    human_judgment: false
    rationale: ""

# Metrics
duration: 38 min
completed: 2026-09-18
status: complete
---

# Phase 4 Plan 13: Register readme-output-style-destination-missing and repair the README install claim Summary

**Closed G-04-4 by registering a 48th discrimination-proven violation code (`readme-output-style-destination-missing`) that fires when README names the output-style route but no destination directory, and by rewriting README's `## Install` section so route 3 states its copy step and route 4 states it needs none — replacing the false "routes 3 and 4 work today, from a local clone" claim.**

## Performance

- **Duration:** 38 min
- **Started:** 2026-09-18T06:08:30Z (session start; see commit 63b5dfa timestamp)
- **Completed:** 2026-09-18T06:46:58Z
- **Tasks:** 3
- **Files modified:** 3 (`tools/check_repo.py`, `README.md`, `.planning/WINDOWS.md`)

## Accomplishments

- Registered `readme-output-style-destination-missing`: fires once when README names `output-styles/proof-first.md` as a route but names neither `~/.claude/output-styles/` nor `.claude/output-styles/` — the two directories Claude Code actually scans for output styles (provenance: `04-UAT.md` test 4, orchestrator-verified).
- **Primary evidence — the exact red-half output line, measured against the shipped `README.md` before this plan's repair**, quoted verbatim:

  ```
  readme-output-style-destination-missing README.md names output-styles/proof-first.md as the output-style route but names neither directory Claude Code scans for output styles (~/.claude/output-styles/ or .claude/output-styles/)
  ```

  `python3 tools/check_repo.py` exited 1 printing exactly this line against the shipped file at HEAD — not a fixture. After the repair, the same command prints `check_repo: 0 violations`.
- Proven in both directions by a dedicated fixture pair (`_good_readme_output_style()` / `_bad_readme_output_style()`) plus a third fixture (`_no_route_readme_output_style()`) proving the code stays silent when README names no output-style route at all — deliberately not reused from `_good_readme_install()`/`_bad_readme_install()`, both of which already name the output-style path with no destination and would have proven this code incidentally rather than by dedicated construction.
- Proven against the real file by a new `--mutation-test` row (`_mutate_readme_output_style_destination`) that deletes every line containing the shorter, project-level destination literal — matching the shorter literal specifically because the user-level form contains it as a substring, so a mutation matching only the longer literal would leave the project-level sentence behind and stay inert.
- Rewrote README's `## Install` preamble and route 3 block: the placeholder disclosure is now stated once (was twice, once with a clause that did not parse); route 4 states it needs no step beyond the clone; route 3 states the copy step in a fenced `mkdir -p ~/.claude/output-styles` / `cp output-styles/proof-first.md ~/.claude/output-styles/` block, names the project-scoped alternative, and states plainly that a live `/config` listing has not been observed in this environment.
- Folded in all four README `secondary_defects` from `G-04-4`: the lead-in now describes the actual vertical (draft, then rewrite) layout instead of a nonexistent left/right arrangement and is cut from one 63-word sentence to three short lines while keeping the deal-brief disclosure; a namespace pointer naming `NUMBERING.md`/`checklist.md` sits directly beneath the applied-rules footer; the placeholder disclosure is confirmed merged to one instance; `## Status`'s 18-line unbroken paragraph is now five paragraphs with no word, punctuation mark, or ordering changed (verified by whitespace-normalised comparison against HEAD).
- First `✗` line now at line 13 (down from 14, ceiling 20); `NUMBERING.md` first named at line 18 (down from 79, target ≤25).
- Filed one `unrun-verify` WINDOWS entry (id 16) for the residual: a live Claude Code session actually listing and applying the copied style is unobserved in this environment. Entry 12 stays open, narrowed. `DIST-06` stays unchecked in `REQUIREMENTS.md`.
- All four CI gate commands green throughout, holding at **48 codes discrimination-proven** (up from 47) — `mutation-test PASS: 48 codes discrimination-proven`, 0 unexpected CONTROL violations, no FIRE-ONLY line.

## Task Commits

Each task was committed atomically:

1. **Task 1: Register readme-output-style-destination-missing, prove it red on the real README, then state the copy step** - `63b5dfa` (feat)
2. **Task 2: Fold in the four README credibility defects and break the Status paragraph without changing a word** - `fea74ac` (fix)
3. **Task 3: File the one unobserved link as a tracked verification, and record what is deferred** - `2d7a0d1` (docs)

**Plan metadata:** (this commit)

## Files Created/Modified

- `tools/check_repo.py` — `README_OUTPUT_STYLE_PATH` / `README_OUTPUT_STYLE_DESTINATIONS` module constants (referenced by `README_INSTALL_ANCHORS`, replacing its inline literal); `check_readme_output_style_destination()` with a declared-ceiling docstring; dedicated `_good_readme_output_style()` / `_bad_readme_output_style()` / `_no_route_readme_output_style()` fixtures wired through all six self-test sites (root declarations, fixture writes, per-root code extraction, the `bad_codes` union, explicit directional assertions, module-docstring contract entry); `_mutate_readme_output_style_destination()` and its `MUTATIONS` row.
- `README.md` — `## Install` preamble and route 3 block rewritten (Task 1); lead-in above the before/after pair rewritten, namespace pointer added beneath the applied-rules footer, `## Status`'s single unbroken paragraph broken into five (Task 2).
- `.planning/WINDOWS.md` — one appended `unrun-verify` entry (id 16, Task 3); pre-existing entry 15's rendered table row regenerated to match its own JSON (unrelated backslash-escaping drift, content/JSON untouched — see Deviations).

## What the New Code Does Not Prove (in its own words, from the docstring)

> Declared ceiling: this check asserts the README tells a reader which directory the output-style file has to reach. It asserts nothing about whether the copy succeeds, whether Claude Code lists or applies the style, whether the stated command is correct, or whether any other route is executable — `readme-install-path-missing` owns anchor presence and nothing in this repository owns route executability. The comparison is literal substring containment with no path expansion and no filesystem access, so a README naming the directory in a different notation (a different home-directory alias, a relative path, an environment variable) is invisible to it.

A later reader should not mistake this code for an executability guarantee. It proves exactly one fact: README names a destination directory. It does not, and cannot, prove that Claude Code actually lists or applies the copied style — that residual is the one WINDOWS entry 16 (Task 3) tracks.

## Before/After — README `## Install` (Task 1)

**Before (defective preamble + route 3):**
> Proof First supports four install paths, one per harness class this project targets. The publish-location placeholder `<owner>/<repo>` below stands for wherever this repository is published; every command and manifest that states it is checked to agree.
>
> Routes 3 and 4 work today, from a local clone of this repository: `output-styles/proof-first.md` and `prompts/system-prompt.md` are committed files a reader already has once the clone exists. Routes 1 and 2 name the placeholder below and will not resolve until this repository is published. That placeholder is deliberate and disclosed, not an oversight; every command and manifest stating it is held identical by a check in this repository.
>
> **3. Output style** — `output-styles/proof-first.md` is a Claude Code output style, generated mechanically from the skill content rather than written separately. Select it through `/config`; once selected it stays on for the whole session.

**After (repaired):**
> Proof First supports four install paths, one per harness class this project targets.
>
> Routes 1 and 2 name the publish-location placeholder `<owner>/<repo>`, which stands for wherever this repository is published. Neither resolves until it is published. The placeholder is deliberate and disclosed: `publish-location-drift` in `tools/check_repo.py` fails the build if any command or manifest carrying it stops agreeing with the others.
>
> Route 4 runs from a local clone with no step beyond the clone: `prompts/system-prompt.md` is a committed file, and pasting it is the whole action. Route 3 runs from a local clone too, but it needs one copy step first, stated in full below. `output-styles/` at this repository's root is where a plugin ships an output style from, not a directory Claude Code scans, so the file is not offered in `/config` until it is copied to one that is.
>
> **3. Output style** — `output-styles/proof-first.md` is a Claude Code output style, generated mechanically from the skill content rather than written separately. Copy it into the directory Claude Code scans for output styles, then select it through `/config`; once selected it stays on for the whole session.
>
> ```
> mkdir -p ~/.claude/output-styles
> cp output-styles/proof-first.md ~/.claude/output-styles/
> ```
>
> Use a project's own `.claude/output-styles/` instead of `~/.claude/output-styles/` to scope the style to that project. What this repository checks is that the file exists and that this README names the directory it has to reach. That a Claude Code session then lists it in `/config` has not been observed here: this repository's own environment drives no live harness session.

## Before/After — README lead-in and Status paragraph (Task 2)

**Lead-in, before (63-word sentence, spatial description that does not match the page):**
> The rules cited below turned a paragraph like the one on the left into the one on the right: adjectives and claims of comprehensiveness replaced by the buyer's own numbers, drawn from the one shared canonical deal brief this repository ships, with each rule that drove a change named alongside it. One full pair, reproduced from `examples/before-after.md`:

**Lead-in, after (three short lines, deal-brief disclosure kept, causal claim dropped):**
> Below: an unrevised draft, then a rewrite. The rewrite's numbers come from the one shared canonical deal brief this repository ships. One full pair, reproduced from `examples/before-after.md`:

**Namespace pointer, added beneath the `Rules applied: PF-2.1, MC-11.` footer:**
> `PF-` and `MC-` are this project's two rule namespaces. `NUMBERING.md` is the registry that defines every ID; `skills/proof-first/references/checklist.md` indexes them.

**`## Status` paragraph:** the same 18 lines' words, unchanged, now broken into five paragraphs at existing sentence boundaries (verified: whitespace-normalised text of the whole `## Status` section is identical to HEAD before Task 2 — probe printed `True`).

## `--mutation-test` Final Line

```
mutation-test PASS: 48 codes discrimination-proven
```

With an `OK` line for `readme-output-style-destination-missing`, 0 unexpected CONTROL violations, and no FIRE-ONLY line.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Regenerated `.planning/WINDOWS.md`'s rendered table for pre-existing entry 15**

- **Found during:** Task 3, when `gsd-tools windows append` refused to write with `WINDOWS_LEDGER_TABLE_DRIFT: Ledger table ... disagrees with the fenced JSON entries ... for row id(s): 15.`
- **Issue:** Entry 15's rendered table row used single-backslash escaping (`\s`, `\|`) where the ledger's own `renderTable()` produces double-backslash escaping (`\\s`, `\|` via the documented escape-backslash-then-pipe order). This drift pre-dates this plan — entry 15 was appended by a prior plan's execution — and is unrelated to anything this plan's tasks touch.
- **Fix:** Ran the ledger module's own `parseLedger()` then `renderLedger()` directly (not through the CLI, which validates before allowing the write) and overwrote `.planning/WINDOWS.md` with the regenerated content. This is exactly the tool's own documented remediation ("discard the table edit and re-run the command so gsd-tools regenerates the table"), applied once, mechanically, with zero change to any entry's `id`, `kind`, `description`, `status`, or any other JSON field — confirmed by diff: only the rendered table row for id 15 changed, matching its own JSON verbatim.
- **Files modified:** `.planning/WINDOWS.md` (table region only; JSON block byte-identical before and after except for the newly appended entry 16 from Task 3's own action)
- **Verification:** `git diff .planning/WINDOWS.md` before appending entry 16 showed only the table-row escaping change for id 15; `gsd-tools windows append` then succeeded on retry.
- **Committed in:** `2d7a0d1` (Task 3 commit)

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Necessary to complete Task 3's mandated tool invocation; no entry content, status, or meaning changed. No scope creep — the fix is a pure re-render of the ledger's own source of truth into its own designated presentation format.

## Issues Encountered

None beyond the one deviation above.

## User Setup Required

None — no external service configuration required.

## DIST-06 / WINDOWS Status (verbatim residuals)

- **Route executability is not mechanised and is not mechanisable here.** The registered code asserts that README names a destination directory, which is a necessary condition and the one that failed. It is not a sufficient condition and its docstring says so.
- **That a live Claude Code session lists and applies the copied style is unobserved.** Filed as new WINDOWS entry 16 (`unrun-verify`), routed to Phase 6 LEG-04 alongside entries 11 and 12.
- **WINDOWS entry 12 stays open, narrowed:** the Install section is actionable and the lead-in matches the page, but DIST-06's prose-quality judgement is still human.
- **Entries 11, 13, 14 and 15 stay open and untouched** (entry 15's *table rendering* was mechanically regenerated to match its own unchanged JSON — see Deviations; its content, status, and meaning are unchanged).
- **DIST-06 stays unchecked** in `.planning/REQUIREMENTS.md` (confirmed: `grep -c '^- \[ \] \*\*DIST-06\*\*' .planning/REQUIREMENTS.md` prints `1`).

## Deferred Item (restated verbatim from `<deferred_items>`)

| Item | Disposition | Reason |
|---|---|---|
| `README.md` — `## Status` is about a quarter of the file and is the third section a reader hits, denser than anything describing what the skill does | **Deferred**, density half closed | The eighteen-line paragraph is broken in Task 2 with no word changed, which is the half that can be proven harmless. Shortening or relocating the section means editing a measured-figure disclosure negotiated across 03-10, 03-15 and 04-08, whose content `04-UAT.md` itself calls the best thing in the document. The complaint is about position and density, not about anything being untrue, and it is not what G-04-4 failed on. It belongs to a README structure pass with its own plan and its own review of what each disclosure sentence is load-bearing for. |

Every other `secondary_defect` on both `G-04-3` and `G-04-4` was folded in: the two `examples/before-after.md` items by `04-12-PLAN.md` Task 2 (wave 1, already complete), and README items 0 through 3 by Task 2 of this plan. No secondary defect was silently dropped.

## Next Phase Readiness

- G-04-4 (primary defect and four of its five `secondary_defects`) is closed. The remaining `secondary_defects[4]` half (Status section position/density) is deferred with a stated reason, not dropped.
- Combined with 04-12 (wave 1, G-04-3), all `04-UAT.md` gaps from this gap-closure round are addressed — either closed or explicitly deferred/routed to a later gate.
- `tools/check_repo.py` now enforces 48 discrimination-proven codes; any future PR that removes README's output-style destination directory will fail CI immediately.
- No blockers for end-of-phase UAT re-verification. DIST-06 remains unchecked pending that re-verification and Phase 6's LEG-04 launch gate (route publication, live harness session).

---
*Phase: 04-distribution-worked-examples*
*Completed: 2026-09-18*

## Self-Check: PASSED

- FOUND: tools/check_repo.py
- FOUND: README.md
- FOUND: .planning/WINDOWS.md
- FOUND: .planning/phases/04-distribution-worked-examples/04-13-SUMMARY.md
- FOUND: 63b5dfa (Task 1 commit)
- FOUND: fea74ac (Task 2 commit)
- FOUND: 2d7a0d1 (Task 3 commit)
- All acceptance criteria for all three tasks re-verified passing (see Task Commits and Accomplishments above).
- Full plan-level `<verification>` block (7 items) re-run and passing: `check_repo.py` 0 violations; `--self-test` lists `readme-output-style-destination-missing` among 48 codes; `--mutation-test` prints `mutation-test PASS: 48 codes discrimination-proven` with an OK line for the new code, 0 unexpected CONTROL, no FIRE-ONLY; `generate_derivatives.py --check` exits 0 with no output; `run_conformance.py --self-test` prints `self-test PASS`; `git diff --name-only 06ebacb..HEAD` (this plan's actual base) lists exactly `tools/check_repo.py`, `README.md`, `.planning/WINDOWS.md`; hand read of `## Install` confirms a bare-clone reader can execute routes 3 and 4 and knows which link is unobserved.
