---
phase: 03-completeness-audit-artifact-patterns
plan: 05
subsystem: skill-content
tags: [agent-skills, meddicc, prose-catalog, gap-closure]

# Dependency graph
requires:
  - phase: 03-completeness-audit-artifact-patterns
    provides: 03-UAT.md's 18-session live harness pass, recording gaps G-03-2 and G-03-5
provides:
  - "SKILL.md: non-blocking source-material ask, explicit no-rule-before-family instruction"
  - "completeness-audit.md: six MC bodies rewritten in document-facing vocabulary, matching MC-11/MC-36's demonstrated pattern"
  - "REQUIREMENTS.md: honest state for AUD-01, AUD-03, MOD-03, MOD-04, MOD-05"
affects: [phase-6-legal-review, future-uat-passes]

# Actuals (#2632)
actuals:
  tokens: 4683
  tasks: 3
  commits: 3

tech-stack:
  added: []
  patterns:
    - "MC dimension bodies cite the block's own heading noun ('the person who signs', 'the person who carries this internally') rather than the frozen NUMBERING.md registry label ('economic buyer', 'champion'), following MC-11/MC-36's pre-existing pattern"

key-files:
  created: []
  modified:
    - skills/proof-first/SKILL.md
    - skills/proof-first/references/completeness-audit.md
    - .planning/REQUIREMENTS.md

key-decisions:
  - "G-03-2 fix: split Write mode's buried 'ask for it once, proceeding either way' into two sentences, and added one sentence to Your task stating no rule ID is cited before the family line, in either mode — 236-token margin absorbed 2 sentences with 46 tokens to spare (190 remaining, above the 150 floor)"
  - "G-03-5 fix: replaced source dimension labels in MC-1, MC-6, MC-16, MC-21, MC-26, MC-31 bodies and Replace-with lines with each block's own heading phrase; left NUMBERING.md's registry labels and all headings/IDs/count untouched, per WINDOWS.md entry 6's ownership"
  - "REQUIREMENTS.md: MOD-04 and AUD-01 stay [ ]/UNVERIFIED per plan prohibition, even though this plan's own live re-verification passed 5/5 — closure requires an independent Phase 3 UAT pass, not this plan's self-check"
  - "AUD-03, MOD-03, MOD-05 moved to [x] Complete: their stated closure condition (a live harness session recorded at the Phase 3 UAT pass) is met by 03-UAT.md's tests 1, 3, and 4 with zero failures"

patterns-established: []

requirements-completed: []  # MOD-04 and AUD-01 explicitly NOT marked complete per this plan's must_haves prohibitions — see key-decisions

coverage:
  - id: D1
    description: "SKILL.md's Write mode states the source-material ask never ends the turn; Your task states no rule ID is cited before the artifact family is named, in either mode"
    requirement: "MOD-04"
    verification:
      - kind: other
        ref: "python3 tools/check_repo.py (0 violations); 5 live claude -p write-mode sessions (fixtures A-E) — see Live Verification section"
        status: pass
    human_judgment: false
  - id: D2
    description: "Six MC dimension bodies in completeness-audit.md (MC-1, MC-6, MC-16, MC-21, MC-26, MC-31) use document-facing vocabulary instead of the frozen NUMBERING.md registry label"
    requirement: "AUD-01"
    verification:
      - kind: other
        ref: "grep -n 'economic buyer|champion|the paper process|buyer.s decision process' completeness-audit.md — zero hits; python3 tools/check_repo.py (0 violations)"
        status: pass
    human_judgment: true
    rationale: "Whether a document-facing phrase genuinely reads as this repo's own vocabulary (versus a paraphrase that still tracks the source too closely) is the same semantic judgment SOURCES.md states no tool in this stack performs. The two independent-subagent reads that found G-03-5 are the closest thing to that judgment available in this environment; a human read is still the formal closure condition per AUD-01's own annotation."
  - id: D3
    description: "REQUIREMENTS.md records the Phase 3 UAT's honest state: MOD-04/AUD-01 stay open with amended annotations, AUD-03/MOD-03/MOD-05 move to Complete with measured session counts"
    requirement: "N/A"
    verification:
      - kind: other
        ref: ".planning/REQUIREMENTS.md lines 34-36, 49-51 (diff in commit b590abe)"
        status: pass
    human_judgment: false

duration: ~45min
completed: 2026-09-14
status: complete
---

# Phase 03 Plan 05: Close the two Phase 3 UAT gaps Summary

**Fixed the one-in-six write-mode ordering break (G-03-2) and the six-of-eight source-vocabulary leak in the completeness audit (G-03-5), then recorded REQUIREMENTS.md honestly — MOD-04 and AUD-01 stay open pending an independent UAT re-run, exactly as this plan's own prohibitions require.**

## Performance

- **Duration:** ~45 min (includes two live-harness verification passes: 5 write-mode sessions + 1 standalone audit session, run against `claude-sonnet-5`)
- **Tasks:** 3/3 completed
- **Files modified:** 3 (`SKILL.md`, `completeness-audit.md`, `REQUIREMENTS.md`)

## Accomplishments

- G-03-2 closed: `SKILL.md`'s `## Write mode` now states the source-material ask never ends the turn as its own sentence, and `## Your task` states explicitly that no rule ID is cited before the artifact family is named, in either mode. Re-verified with 5 fresh `claude -p` write-mode sessions (one per fixture family plus the ambiguous fixture) — 5/5 named the family before any rule ID appeared.
- G-03-5 closed: `completeness-audit.md`'s MC-1, MC-6, MC-16, MC-21, MC-26 and MC-31 bodies and `**Replace with:**` lines no longer use the source's own frozen dimension label ("economic buyer", "the buyer's decision process", "the paper process", "pain"/"pains", "champion") as this repository's unattributed noun — each now uses the document-facing phrase its own heading already states, matching MC-11's and MC-36's pre-existing pattern. Re-verified with a standalone completeness-audit session against `docs/B-proposal-section.md`: every MC citation used the new vocabulary, with zero leaked source labels.
- `REQUIREMENTS.md` now states the real Phase 3 UAT result rather than a rounded-up one: MOD-04 and AUD-01 keep their `[ ]`/UNVERIFIED status (their closure condition is an independent UAT pass, not this plan), while AUD-03, MOD-03 and MOD-05 move to `[x]` Complete with their measured session counts (6, 9, 18 respectively, zero failures).
- Full gate re-run clean throughout: `--self-test` (27 codes), `--mutation-test` (27 codes discrimination-proven), and the bare run (0 violations) at every checkpoint.

## Task Commits

1. **Task 1: G-03-2 — classify-before-rules order** - `3c8d7c7` (fix)
2. **Task 2: G-03-5 — stop using source dimension labels as repo nouns** - `1ef8af1` (fix)
3. **Task 3: Record state honestly** - `b590abe` (docs)

## Files Created/Modified

- `skills/proof-first/SKILL.md` - Split the buried "proceeding either way" clause into its own non-blocking sentence in `## Write mode`; added a no-rule-before-family sentence to `## Your task`
- `skills/proof-first/references/completeness-audit.md` - Replaced source dimension labels with document-facing phrases in MC-1, MC-6, MC-16, MC-21, MC-26, MC-31 bodies and `**Replace with:**` lines
- `.planning/REQUIREMENTS.md` - Amended AUD-01/MOD-04 annotations; moved AUD-03/MOD-03/MOD-05 to Complete with measured evidence; updated Traceability table

## Token Budget

`SKILL.md` measured before this plan: 3665 words, 4764 estimated tokens, 236-token margin under the 5000-token ceiling.

`SKILL.md` measured after this plan's two-sentence edit: **3700 words, 4810 estimated tokens, 190-token margin** (`python3 tools/check_repo.py` reports `skill-token-budget-exceeded` silent — 0 violations). 190 ≥ the plan's 150-token floor, so no restatement-trimming was needed to pay for the fix.

## Gate Results (verbatim)

```
$ python3 tools/check_repo.py --self-test
self-test PASS - verified violation codes: artifact-family-section-missing, catalog-count-mismatch,
catalog-count-unstated, catalog-id-drift, catalog-opening-rule-count, dup-figure-key, dup-id,
figure-order, framework-statement-missing, frontmatter-description-invalid, frontmatter-name-mismatch,
frontmatter-unknown-key, frontmatter-unparseable, license-missing, mc-catalog-id-drift,
mc-count-mismatch, mc-count-unstated, mc-rule-in-skill, pointer-duplicated, pointer-missing,
pointer-unparseable, range-id, revived-id, skill-token-budget-exceeded, skill-too-long, undefined-id,
unlisted-figure

$ python3 tools/check_repo.py --mutation-test
[... 25 lines omitted, all OK ...]
mutation-test PASS: 27 codes discrimination-proven

$ python3 tools/check_repo.py
check_repo: 0 violations
```

All three gate commands were run fresh after each task's edits and again as a final pass after Task 3 — identical results every time.

## Live Verification

### Task 1 — 5 write-mode sessions (G-03-2 re-check)

Method: fresh isolated directory outside the repo, edited `skills/proof-first/` copied to `.claude/skills/proof-first/`, the seven pre-existing UAT fixtures copied in unmodified. Five `claude -p --model claude-sonnet-5 --disallowedTools Write Edit Bash NotebookEdit` sessions, one per fixture family plus the ambiguous fixture, prompt: `"Using proof-first, revise this draft into stronger presales prose: docs/<file>"`. Each session wrote to its own output path (no shared-file interleaving).

**Result: 5 of 5 conformed.** Every response named the artifact family (or, for the ambiguous fixture, explicitly reported spanning two families) before any `PF-` rule ID appeared, and every session drafted the revised prose in the same response as the source-material ask — none stopped to await a "proceed" reply.

| Fixture | Family stated | Any rule ID before family line | Drafted in same response |
|---|---|---|---|
| A-rfp-answer.md | RFP and RFI response | No | Yes |
| B-proposal-section.md | Proposal section | No | Yes |
| C-exec-summary.md | Executive summary | No | Yes |
| D-demo-discovery.md | Demo and discovery material | No | Yes |
| E-ambiguous.md | Reported as spanning Solution proposal + Demo and discovery (correctly not forced into one) | No | Yes |

This is an improvement over 03-UAT.md test 2's original 5/6 write-mode result, but it is **this plan's own re-verification, not an independent UAT pass** — `REQUIREMENTS.md` records MOD-04 as still requiring that independent re-run before closure, per this plan's explicit prohibition.

### Task 2 — 1 standalone completeness-audit session (G-03-5 re-check)

Method: fresh isolated directory, freshly copied edited skill (both Task 1 and Task 2 edits present), `docs/B-proposal-section.md` fixture. One `claude -p` session, prompt: `"Run the proof-first completeness audit on docs/B-proposal-section.md, on its own."`

**Result:** The session correctly cited all 8 MC dimensions with the new document-facing vocabulary — e.g. `MC-6 — Name the person who signs and the priority they stated in their own words` (used "the person who signs," never "economic buyer"), and `MC-31` (used "the person inside the buyer who carries this internally," never "champion"). Zero leaked source labels. `## Completeness gaps` and a verdict line (`0 of 8 dimensions satisfied`) both printed as the file's own instructions specify.

**Observation, not a defect in scope for this plan:** the session also printed an unrequested `## Artifact family` section before `## Completeness gaps`. `references/completeness-audit.md`'s `## Running the audit on its own` section — which this plan did not touch — says a standalone run "returns ... `## Completeness gaps` ... and nothing more." This single live sample diverges from that shape. Since only Task 2's vocabulary edits were in scope here and the "Running the audit on its own" instruction text is unchanged from before this plan, this is model-sampling variance rather than something this plan's edits caused — but it is recorded here rather than silently dropped, since it touches AUD-03 (now marked Complete based on the Phase 3 UAT's 6/6 result, which predates this observation).

## Decisions Made

- **Token budget:** absorbed the two-sentence G-03-2 fix inside the existing 236-token margin (190 remaining afterward, above the plan's 150-token floor) — no restatement trimming was needed.
- **MC-1's `**Replace with:**` line and MC-16's/MC-21's `**Replace with:**` lines needed no edit** — they already used buyer-facing phrasing ("the buyer's own stated figure", "the submission date, the bidder count...", "each review's named owner...") with no source-label leak; only the bodies of MC-16 and MC-21 needed the fix.
- **REQUIREMENTS.md:** MOD-04 and AUD-01 deliberately kept `[ ]`/UNVERIFIED despite this plan's own passing re-verification — the plan's `must_haves.prohibitions` are explicit that their closure condition is an independent Phase 3 UAT re-run, not this plan landing. AUD-03/MOD-03/MOD-05 moved to Complete because their stated closure condition (a live session recorded at the Phase 3 UAT pass) was already met by 03-UAT.md before this plan started.

## Deviations from Plan

None — plan executed exactly as written. No Rule 1/2/3 auto-fixes were needed; the two content edits and the REQUIREMENTS.md update matched the plan's `must_haves` exactly, and all prohibitions were honored (no heading/ID/count/order changes, no `**Replace with:**` line deletions, no catalog-count changes, no `artifact-patterns.md` `**Problem reframe:**` edit, no new `WINDOWS.md` entry, no premature MOD-04/AUD-01 completion).

## Honest Note (carried from plan Task 2)

"Economic buyer" and "champion" predate the sources `SOURCES.md` lists for MC-6 and MC-31 — "economic buyer" traces to Miller Heiman's Strategic Selling (1985), and "champion" is general sales usage rather than a term coined by any of the three named frameworks. Both independent readers who surfaced G-03-5 said so themselves. Strictly, this means these two terms arguably fail `SOURCES.md`'s own "coined by a source" test for being reproduction at all. The reason they were fixed anyway is not a settled finding that a boundary was violated — it is consistency: MC-11 and MC-36 already demonstrate that this file can express every dimension in its own document-facing vocabulary, and six of eight bodies not doing what two of eight already do was the actual defect G-03-5 identified.

## Known Stubs

None.

## Threat Flags

None — this plan touched no network endpoints, auth paths, file access patterns, or schema at a trust boundary. It edited only prose inside an already-shipped skill file and a requirements-tracking markdown file.

## Issues Encountered

The first background `claude -p` loop (all 5 write-mode sessions chained in one Bash call) hit the 10-minute Bash timeout after 2 of 5 completed, leaving one output file at 0 bytes from a killed mid-write process. Recovered by deleting the truncated file and re-running each remaining session as its own Bash call (foreground where it fit under 5 minutes, backgrounded via `run_in_background` where a single session ran long — observed session durations ranged from about 1 to over 5 minutes). No output file was ever written by more than one session.

## Next Phase Readiness

- Both Phase 3 UAT gaps (G-03-2, G-03-5) are closed at the content level and re-verified by this plan's own live sessions.
- `MOD-04` and `AUD-01` remain formally open pending an independent Phase 3 UAT re-run — that re-run, not further plan work, is what would close them.
- `WINDOWS.md` entries 3 and 6 (MC block ordering, `artifact-patterns.md`'s `**Problem reframe:**` label) are untouched, as required — both remain routed to Phase 6 LEG-04.

## Self-Check: PASSED

All claimed files found on disk (`skills/proof-first/SKILL.md`, `skills/proof-first/references/completeness-audit.md`, `.planning/REQUIREMENTS.md`, this SUMMARY.md). All three claimed commit hashes (`3c8d7c7`, `1ef8af1`, `b590abe`) found in `git log`.

---
*Phase: 03-completeness-audit-artifact-patterns*
*Completed: 2026-09-14*
