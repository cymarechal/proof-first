---
phase: 04-distribution-worked-examples
plan: 10
subsystem: testing
tags: [check-repo, generate-derivatives, mutation-test, plugin-manifest, publish-location]

# Dependency graph
requires:
  - phase: 04-01
    provides: PUBLISH_LOCATION_CARRIERS/publish-location-drift, the plugin-manifest checks,
      and generate_derivatives.py's --check mode -- the three mechanisms this plan repairs.
  - phase: 04-03
    provides: The two-guard derivative-freshness arrangement (skill-derivative-stale's
      digest recomputation plus generate_derivatives.py --check's byte comparison) whose
      second guard's byte-comparison defect this plan fixes.
provides:
  - "_owner_segment normalises four GitHub URL forms (HTTPS, plaintext HTTP, scheme-less,
    SSH remote) before extracting the owner segment, closing WR-01's false-positive risk
    while still discriminating genuine owner disagreement"
  - "generate_derivatives.py --check compares committed bytes against freshly rendered
    bytes, not decoded text, so a CRLF-only divergence is caught rather than silently
    passing (WR-02); write_derivatives pins the output newline to LF"
  - "check_plugin_manifest_invalid and check_plugin_manifest_version fire on the
    previously-silent zero-skill and multi-skill ambiguity, naming it explicitly, instead
    of skipping the one-skill-assuming equality check (WR-03)"
affects: ["04-verify-work", "phase-05-eval-harness"]

# Actuals (#2632)
actuals:
  tokens: 6800
  tasks: 3
  commits: 3

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Tracer-first task ordering: Task 1 (the _owner_segment rewrite) proved the whole
      repair shape -- change a live shipped behaviour, disclose the new ceiling in two
      docstrings, add discrimination assertions in both directions, re-run the full gate
      at an unchanged code count -- before Tasks 2 and 3 repaired the other two warnings
      inside their own existing codes."
    - "Byte-verdict / text-report split: check_derivatives decides pass/fail from raw
      bytes but still decodes (defensively, errors='replace') for the human-readable
      first-differing-line message, so the fix does not regress the diagnostic output."

key-files:
  created: []
  modified:
    - tools/check_repo.py
    - tools/generate_derivatives.py

key-decisions:
  - "_owner_segment tries HTTPS, then plaintext HTTP, then scheme-less github.com/, then
    (via a for/else) the SSH git@github.com: form -- at most one prefix match per call,
    so an already-stripped value is never stripped twice. A trailing .git suffix is
    stripped after prefix removal, because the SSH form from `git remote -v` carries one
    and the HTTPS form usually does not; leaving it on would make the repository segment
    disagree between two forms of the same repository even once the owner agreed."
  - "The two new plugin-manifest-version-mismatch/plugin-manifest-invalid firing
    conditions attach to PLUGIN_MANIFEST_PATH as their subject, matching this checker's
    existing convention that both codes' violations are always tagged against one of the
    two manifest paths, never a skills/*/ path -- there is no single manifest file the
    ambiguity is 'about', so the plugin manifest (the one whose name/version comparison
    is now unresolvable) is the natural anchor."
  - "DIST-05 marked Complete: the mechanism (regenerate-from-SKILL.md plus a documented
    re-sync step, built in 04-03) was always present; this plan closes the one remaining
    gap in its second independent guard's own stated guarantee. Unlike DIST-01/02/06,
    nothing about DIST-05 depends on an external live-install test this environment
    cannot run, so it carries no UNVERIFIED caveat."

requirements-completed: [DIST-02, DIST-05]

coverage:
  - id: D1
    description: "_owner_segment normalises four GitHub URL forms (WR-01); publish-
      location-drift proven silent on genuine agreement across syntaxes and still firing
      on genuine disagreement; both ceilings (self-hosted host, owner-only granularity)
      disclosed in _owner_segment's own docstring and the module docstring's
      publish-location-drift bullet."
    requirement: "DIST-02"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --self-test"
        status: pass
      - kind: other
        ref: "python3 tools/check_repo.py --mutation-test"
        status: pass
      - kind: unit
        ref: "python3 -c \"...c._owner_segment(v) for v in (four URL forms)...\" -- all four reduce to 'acme'"
        status: pass
      - kind: unit
        ref: "python3 -c \"...c._owner_segment('git@github.com:other/...') == c._owner_segment('https://github.com/acme/...')\" -- prints False"
        status: pass
    human_judgment: false
  - id: D2
    description: "generate_derivatives.py --check compares bytes, not decoded text, so a
      CRLF-only divergence is caught (WR-02); write_derivatives pins newline='\\n'; the
      discrimination probe flips from True/True to True/False; module docstring states
      the guarantee actually implemented."
    requirement: "DIST-05"
    verification:
      - kind: other
        ref: "python3 tools/generate_derivatives.py --check"
        status: pass
      - kind: unit
        ref: "discrimination probe: clean copy True, CRLF-rewritten copy False"
        status: pass
      - kind: unit
        ref: "freshly written derivatives in a scratch tree contain no CRLF sequence"
        status: pass
    human_judgment: false
  - id: D3
    description: "check_plugin_manifest_invalid and check_plugin_manifest_version fire on
      the zero-skill and multi-skill ambiguity instead of silently skipping it (WR-03);
      both docstrings and both module-docstring bullets state the one-skill assumption as
      a declared ceiling; the one-skill live case proven unchanged."
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py --self-test"
        status: pass
      - kind: unit
        ref: "two-skill scratch tree: plugin-manifest-invalid fires (printed True)"
        status: pass
      - kind: unit
        ref: "one-skill scratch tree: no plugin-manifest-* violation (printed [])"
        status: pass
    human_judgment: false

duration: 15min
completed: 2026-09-17
status: complete
---

# Phase 4 Plan 10: Close G-04-7 -- normalise owner-URL comparison, byte-compare derivatives, disclose the one-skill assumption Summary

**Three latent `04-REVIEW.md` defects repaired inside existing violation codes -- a
URL-form-blind owner comparator, a text-mode-blind byte-comparison guard, and two checks
that silently skipped their own equality tests -- with the discrimination-proven total
held at exactly 47 throughout.**

## Performance

- **Duration:** 15 min
- **Completed:** 2026-09-17T10:47Z
- **Tasks:** 3
- **Files modified:** 2 (`tools/check_repo.py`, `tools/generate_derivatives.py`)

## Accomplishments

- **WR-01 (Task 1, tracer): `_owner_segment` normalised across four GitHub URL forms.**
  Before this plan, `_owner_segment` stripped one literal prefix
  (`https://github.com/`) only, so:

  | Input | Before | After |
  |---|---|---|
  | `https://github.com/acme/proof-first` | `acme` | `acme` |
  | `http://github.com/acme/proof-first` | `http://github.com` (wrong) | `acme` |
  | `github.com/acme/proof-first` | `github.com` (wrong) | `acme` |
  | `git@github.com:acme/proof-first.git` | `git@github.com:acme` (wrong) | `acme` |
  | `https://github.com/acme` (bare) | `acme` | `acme` |
  | `` (empty) | `` | `` |

  The rewrite tries HTTPS, plaintext HTTP, and scheme-less `github.com/` prefixes in
  order, falls back to the SSH `git@github.com:` prefix via a `for`/`else`, strips a
  trailing `.git` suffix after whichever prefix matched, then splits on the first
  remaining `/`. Discrimination in both directions is now self-test-proven:
  `publish-location-drift` stays silent on `plugin_mixed_url_root` (three carriers
  naming the same owner, `acme`, in three different syntaxes) and still fires on
  `plugin_mixed_url_drift_root` (the same three carriers, except the SSH-form value
  names a different owner, `other`). `_owner_segment('git@github.com:other/...') ==
  _owner_segment('https://github.com/acme/...')` prints `False` -- the normalisation did
  not collapse two genuinely different owners into one. Both `_owner_segment`'s own
  docstring and the module docstring's `publish-location-drift` bullet now state the
  four normalised forms and the remaining ceiling (no GitHub Enterprise/self-hosted-host
  recognition; owner-segment-only comparison, unchanged from before).

- **WR-02 (Task 2): `generate_derivatives.py --check` now genuinely compares bytes.**
  Before this plan, `check_derivatives` read both sides as `str`
  (`Path.read_text(encoding='utf-8')`), so Python's universal-newline translation made a
  CRLF-terminated committed file compare equal to an LF-terminated render -- the
  discrimination probe printed `True True` (clean copy passes, CRLF-rewritten copy also
  passes) instead of `True False`. The fix reads and compares raw bytes for the verdict;
  the first-differing-line report still decodes both sides (defensively, with
  `errors='replace'`) but only for the message, never for the verdict already reached
  from the bytes. `write_derivatives` now passes `newline='\n'` so the writer produces
  LF-terminated bytes on every platform -- verified by writing fresh derivatives into a
  scratch tree and confirming no `\r\n` sequence appears anywhere in either file. The
  module docstring's usage text and declared-ceiling clause (c) were already worded as
  "compares ... bytes"; that wording is now accurate rather than aspirational, and a new
  sentence names the pinned line ending.

- **WR-03 (Task 3): both plugin-manifest checks disclose and enforce their one-skill
  assumption.** `check_plugin_manifest_invalid`'s folder-name-equality check used to be
  guarded by `len(skill_dirs) == 1`, silently skipping the check for zero or multiple
  skill folders. It now fires `plugin-manifest-invalid` naming the ambiguity in either
  case, with different wording (zero: "no skills/*/SKILL.md folder exists to check it
  against"; multiple: "the name cannot be checked against a single shipped skill
  folder", naming every folder found). `check_plugin_manifest_version` used to resolve
  its single comparison value from the first skill stating a version and never checked
  whether other skills agreed; it now also fires `plugin-manifest-version-mismatch`
  naming every disagreeing skill and its version when two or more skills state
  different versions, independent of the manifest comparison. The live one-skill case
  is proven unchanged: a one-skill scratch tree raises no `plugin-manifest-*` violation
  at all (`[]`), and a two-skill scratch tree raises `plugin-manifest-invalid` (`True`).
  Both function docstrings and both module-docstring bullets now state the one-skill
  assumption as a declared ceiling, in the `range-id` bullet's established shape.

- **The gate held at exactly 47 codes discrimination-proven throughout all three tasks.**
  `--self-test` (0 `FAIL:` lines), `--mutation-test` (`mutation-test PASS: 47 codes
  discrimination-proven`, `0 unexpected` on CONTROL, no `FIRE-ONLY` line, 47
  `mutation-test OK:` lines), `check_repo.py` (`check_repo: 0 violations` against the
  real repository), and `generate_derivatives.py --check` (exit 0, no derivative
  regenerated) all pass at the plan's close. No new violation code was registered; no
  `MUTATIONS` entry was added; no shipped content file (`README.md`, `examples/`,
  `skills/`, `.claude-plugin/`) changed (`git diff --stat` over all four is empty). The
  real repository's placeholder `<owner>/<repo>` publish location was not resolved or
  altered (`grep -c '<owner>/<repo>' .claude-plugin/plugin.json` still prints `2`).

## Task Commits

Each task was committed atomically:

1. **Task 1: Normalise _owner_segment across GitHub URL forms, proven silent on
   agreement and still firing on disagreement (tracer)** - `939c3a1` (fix)
2. **Task 2: Make generate_derivatives.py --check genuinely byte-comparing and pin the
   writer's line endings** - `1226ce6` (fix)
3. **Task 3: Disclose and enforce the plugin-manifest checks' one-skill assumption** -
   `2af0c67` (fix)

No separate plan-metadata commit was made for task code; this SUMMARY/STATE/ROADMAP
update is committed separately per the sequential-executor protocol.

## Files Created/Modified

- `tools/check_repo.py` - `_owner_segment` rewritten (four-URL-form normalisation,
  trailing `.git` strip); `check_plugin_manifest_invalid` and
  `check_plugin_manifest_version` extended with the multi-skill/zero-skill firing
  conditions; module docstring's `publish-location-drift`, `plugin-manifest-invalid`,
  and `plugin-manifest-version-mismatch` bullets rewritten; three new fixture builders
  (`_mixed_url_form_manifests`, `_mixed_url_form_drift_manifests`,
  `_multi_skill_manifests`); three new self-test roots
  (`plugin_mixed_url_root`, `plugin_mixed_url_drift_root`, `plugin_multiskill_root`);
  four new self-test assertions. No new violation code, no new `MUTATIONS` entry.
- `tools/generate_derivatives.py` - `check_derivatives` compares bytes for the verdict,
  decodes defensively for the line-number report only; `write_derivatives` pins
  `newline='\n'`; module docstring's usage text and declared-ceiling clause (c) confirmed
  accurate, with a new sentence naming the pinned line ending.

## Decisions Made

See `key-decisions` in the frontmatter above.

## Deviations from Plan

### Documented, Not Force-Fit

**1. [Plan-authored verify-script limitation] Task 2's own import-set verify probe
over-matches a pre-existing docstring prose line**

- **Found during:** Task 2, running the plan's own `<verify>` command
  `python3 -c "...re.findall(r'^\s*(?:import|from)\s+...', t, re.M)..."`.
- **Issue:** The probe's regex matches any line starting with `import` or `from` at
  column zero. The module docstring's opening paragraph (unedited by this plan) contains
  the prose line `from the Python standard library;` (continuing the previous line's
  "It imports only argparse, hashlib, pathlib, re, and sys"), which the regex also
  matches, printing `['argparse', 'hashlib', 'pathlib', 're', 'sys', 'the']` instead of
  the five-element list the acceptance criterion names.
- **Confirmed pre-existing, not introduced by this plan:** running the identical probe
  against `git show HEAD:tools/generate_derivatives.py` (the file exactly as it stood
  before this plan's first commit) reproduces the same six-element list with `'the'` as
  the sixth entry.
- **Not fixed:** per the established 03-04/04-01/04-03/04-04/WINDOWS-13 precedent, a
  plan-authored verification script's own limitation is documented rather than force-fit
  by rewording unrelated, pre-existing docstring prose. The load-bearing evidence that
  the import set is genuinely the five stated stdlib names is a direct read of the five
  real `import`/`from` statement lines at the file's end (lines 49-53:
  `argparse, hashlib, re, sys, pathlib.Path`), confirmed by `grep -n "^import \|^from
  "`.
- **Files modified:** none (documentation only: this SUMMARY and `.planning/WINDOWS.md`
  entry 15).
- **Verification:** `git show HEAD:tools/generate_derivatives.py` comparison, direct
  inspection of the five real import lines.

---

**Total deviations:** 1 documented-not-fixed (pre-existing plan-authored verify-script
limitation).
**Impact on plan:** No scope creep. The real acceptance criterion (import set is exactly
`argparse, hashlib, pathlib, re, sys`) holds; only the ad-hoc diagnostic probe's regex
has a false-positive on unrelated prose.

## Issues Encountered

None beyond the item already covered under Deviations.

## User Setup Required

None - no external service configuration required.

## WINDOWS.md -- What This Plan Closes vs. What Remains Open

Per this plan's own `<artifacts_this_phase_produces>` instruction:

**Closed by this plan:** all three `04-REVIEW.md` warnings (WR-01, WR-02, WR-03) --
G-04-7 from `04-UAT.md`. This is the phase's final gap-closure plan; `04-05` through
`04-09` closed G-04-1 through G-04-6.

**Recorded, not closed:**
- WINDOWS.md entry 15 (new, this plan): the plan-authored verify-script limitation
  documented above.
- WINDOWS.md entry 11 (`<owner>/<repo>` placeholder) stays open, explicitly untouched by
  this plan (`grep -c '<owner>/<repo>' .claude-plugin/plugin.json` unchanged at `2`),
  still routed to Phase 6's LEG-04 gate. Worth recording against it when it is finally
  closed: the owner value can now be written in any of the four normalised URL forms
  (HTTPS, plaintext HTTP, scheme-less, SSH) and `publish-location-drift` will still hold
  all carriers consistent.
- WINDOWS.md entry 12 (DIST-06's prose-quality residual) stays open, untouched -- this
  plan changed no shipped content file.

## Next Phase Readiness

- `check_repo.py` now enforces 47 discrimination-proven codes with 0 live violations and
  0 unexpected CONTROL violations; `generate_derivatives.py --check` genuinely compares
  bytes. This is the last plan in Phase 4 (`04-distribution-worked-examples`) -- all ten
  plans now have a `*-SUMMARY.md`.
- DIST-05 marked Complete (checkbox and traceability table). DIST-02 was already Complete
  from `04-01`; this plan's frontmatter re-declared it because Task 1's `_owner_segment`
  fix directly repairs the mechanism DIST-02's UNVERIFIED note references, though the
  note's live-install caveat is unchanged (still routed to Phase 6's LEG-04 gate via
  WINDOWS.md entry 11).
- No blockers. `.planning/config.json`'s `mode: yolo` and this plan's `autonomous: true`
  meant no checkpoints were encountered; the plan carried no `type="checkpoint:*"` task,
  and Task 1's tracer feedback gate re-ran its own `<verify>` end-to-end (interactive,
  `end-of-phase` mode, automated-only verify) and continued to Tasks 2-3 without a
  checkpoint, per the tracer feedback gate's row 3.
- Phase 4 is now fully executed; next step is end-of-phase verification
  (`/gsd-verify-work 04`) followed by `/gsd-plan-phase 5`.

---
*Phase: 04-distribution-worked-examples*
*Completed: 2026-09-17*

## Self-Check: PASSED

- `tools/check_repo.py` and `tools/generate_derivatives.py` exist on disk.
- SUMMARY.md exists on disk.
- Commits `939c3a1`, `1226ce6`, `2af0c67` all found in `git log --oneline --all`.
- All plan-level `<verification>` items re-run clean at close: `--self-test` (0 `FAIL:`
  lines), `--mutation-test` (`mutation-test PASS: 47 codes discrimination-proven`, `0
  unexpected` CONTROL, no `FIRE-ONLY`), `check_repo.py` (`check_repo: 0 violations`),
  `generate_derivatives.py --check` (exit 0), the four URL forms reducing to the same
  owner segment while two different owners stay different, the discrimination probe
  printing `True False`, the two-skill/one-skill scratch-tree probes printing `True`/`[]`
  respectively, and `git diff --stat` over `output-styles/ prompts/ README.md examples/
  skills/ .claude-plugin/` reporting no changed file.
