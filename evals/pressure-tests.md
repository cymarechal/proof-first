# Trigger Pressure Test

This file records whether Proof First's frontmatter `description` actually fires the skill on the
phrasings a writer would use, and stays quiet on the phrasings that sit just outside its stated
scope. Method: run each phrasing in a fresh harness session with the skill installed, with nothing
else in the prompt to bias activation, and record whether the skill activated. A must-not-fire row
is the load-bearing half of this file — a description that fires on everything is not a trigger
list, it is a catch-all, and the near-miss rows below are what tells the two apart. An Observed
cell that was not actually run is recorded as `not yet observed`, never left blank and never
claimed as a result. Trigger reliability at scale — a measured rate across many phrasings and
models — is Phase 5's eval-harness work; this file records a method and, where available, a real
observation, never an extrapolated figure.

## Scope

The 14 phrasings below were authored against, and must be run against, the frontmatter
`description` in `skills/proof-first/SKILL.md` as of the commit this note lands in. That
description's first line reads `Write or check RFP and RFI responses, solution proposals,
executive` and its whitespace-collapsed length is 551 characters — both greppable facts an
auditor can check against the live file without this note carrying a second copy of the
description text, which would only create a place for the two to silently drift apart.

**The description was narrowed by the CAT-10 gap-closure round (`02-10-PLAN.md` Task 4).** The
pre-change description (sha256 of `SKILL.md`'s first 14 lines, truncated here on purpose so this
file carries exactly one full 64-hex token — the sha256 comparison below reads the FIRST such
token in the document, and a stale full hash left anywhere above the live one would silently
rebind these rows to the retired description: `d5dd651a…`, whitespace-collapsed length 439) gained
one appended sentence — "Not for slide decks or visual design, pricing, sizing, or commercial
modelling, or marketing and brand writing." — reusing wording already agreed in `SKILL.md`'s own
`## Limits` section and `PROJECT.md`'s Out of Scope list. The live description now hashes to
`9049c7d82fadce008b00cdf70c7dc74add0d23691c7c61b8d586740a3beb3e1e`, matching the value
`evals/trigger/DECISION-RULE-cat10.md` measured on a scratchpad copy during planning; no live/plan
figure discrepancy occurred. Every observation recorded against the pre-change description was
retired from this file, not carried forward — they remain preserved in
`evals/trigger/RESULTS-trigger.md`'s original 2026-09-20 run block, which this change does not
touch.

An observation recorded in the tables below is valid only for the `description` it was run
against. If the `description` changes in a later phase, previously recorded observations must be
re-run against the new text rather than carried forward as still-current — this rewrite is that
rule being followed, not broken.

The rows below are un-run against the new description as of this commit. `evals/trigger/
DECISION-RULE-cat10.md` is the pre-committed rule that decides what this round's measurement
means; Task 5 fills every Observed cell below with Arm A's counted result.

## Must fire

Each phrasing below draws on a term the frontmatter `description` itself front-loads (RFP, RFI,
solution proposal, executive summary, demo or discovery material, presales, bid, scored technical
response), phrased the way a writer actually asks rather than as a bare keyword.

| Phrasing | Expected | Observed | Date | Harness |
|---|---|---|---|---|
| Write our response to RFP question 4 about the cut-over plan. | Fires | fired 5 of 5 scoreable | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| We got an RFI back from procurement — draft the answers. | Fires | fired 5 of 5 scoreable | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| Draft the solution proposal section for the migration approach. | Fires | fired 5 of 5 scoreable | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| I need an executive summary for the Halverton board deck. | Fires | fired 5 of 5 scoreable | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| Write the demo script for tomorrow's discovery call. | Fires | fired 5 of 5 scoreable | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| Turn these discovery notes into the after-state section of the proposal. | Fires | fired 5 of 5 scoreable | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| Help me write this presales response before it ships to the customer. | Fires | fired 5 of 5 scoreable | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| We're putting together our bid response — write the commercial section. | Fires | fired 0 of 5 scoreable | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| This is a scored technical response — write section 3 so it holds up. | Fires | fired 5 of 5 scoreable | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |

## Must not fire

Each near-miss phrasing sits just outside the skill's stated scope — PROJECT.md's Out of Scope
list and SKILL.md's own Limits section — which is exactly what makes a correct non-fire on these
rows meaningful rather than incidental.

| Phrasing | Expected | Observed | Date | Harness |
|---|---|---|---|---|
| Write launch copy for our new product announcement. | Does not fire | fired 0 of 5 scoreable | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| Build me a slide deck for the kickoff meeting. | Does not fire | fired 0 of 5 scoreable | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| Work out pricing and sizing for a 500-seat deployment. | Does not fire | fired 0 of 5 scoreable | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| Write the API reference docs for the /migrations endpoint. | Does not fire | fired 0 of 5 scoreable | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |
| Rewrite this paragraph in plain English for a general reader. | Does not fire | fired 0 of 5 scoreable | 2026-09-20 | `claude` 2.1.267 / `claude-sonnet-5` |

## Observations

**This round's method.** The CAT-10 gap-closure round (`02-10-PLAN.md`) measures whether the
appended exclusion clause changes the two over-fires the 2026-09-20 single-session run found. Two
paired arms ran on the identical instrument — `evals/trigger/run_trigger_test.py` with
`--model claude-sonnet-5 --repeats 5 --jobs 3 --timeout 600`, all 14 phrasings, 70 sessions each:
Arm B (control, the pre-change 439-character description) and Arm A (treatment, the 551-character
description the rows above now carry, measured against the hash bound in Scope). Arm B's and Arm
A's full run blocks, each with their own `k of n` counts and Clopper-Pearson bounds, are recorded
in `evals/trigger/RESULTS-trigger.md`; the 2026-09-20 single-session block above them is untouched.

**Arm A's rows above are this round's measurement of the description this file is bound to at the
commit that added this paragraph.** `OF_A = 0, SN_A = 25` (every must-not-fire row scored zero
fires) and `MH_A = 40, SM_A = 45` (one must-fire row, "We're putting together our bid response —
write the commercial section.", scored zero of five). For comparison, Arm B measured
`OF_B = 9, SN_B = 25` and `MH_B = 45, SM_B = 45`. Every zero-fire row's exact Clopper-Pearson upper
bound at n=5 is stated in `evals/trigger/RESULTS-trigger.md`'s Arm A block.

`evals/trigger/DECISION-RULE-cat10.md` — committed before either arm ran — is the authority for
what these two arms mean. **This file publishes no verdict.** The branch its six-branch table
selects, and what that means for CAT-10, is applied and written out by Task 6 in
`evals/trigger/RESULTS-trigger.md`, `.planning/REQUIREMENTS.md`, and `.planning/WINDOWS.md` id 24 —
never here.

Reproduce with:

    python3 evals/trigger/run_trigger_test.py --model claude-sonnet-5 --repeats 5 --jobs 3 \
      --timeout 600 --append --label "<arm label>" --out evals/trigger/RESULTS-trigger.md

The runner refuses to fill in any row if the live `description` no longer hashes to the value bound
in the Scope section above — an observation recorded against a different description is not an
observation of these rows.

Narrowing the description is a change to a shipped, distributed trigger surface, so it is recorded
here as a measured defect rather than patched inside the run that found it. Tracked in
`.planning/WINDOWS.md` id 24.
