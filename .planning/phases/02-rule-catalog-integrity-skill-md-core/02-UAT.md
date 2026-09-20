---
status: testing
phase: 02-rule-catalog-integrity-skill-md-core
source: [02-VERIFICATION.md]
started: 2026-09-11T13:45:00Z
updated: 2026-09-20T17:30:00Z
---

## Current Test

number: 3
name: Decide whether SC1's "reliably triggering description" clause is satisfied on the measured evidence
expected: |
  A recorded decision: either (a) accept the residual as-is and record an override stating SC1 is
  met on the 9-of-9 must-fire-recall reading, with the over-fire tracked purely as CAT-10 /
  WINDOWS id 24 debt; or (b) fund the next lever (H1, the audience-clause removal — untested and
  explicitly unfunded this round) as a further gap-closure round before Phase 2 is marked complete.
awaiting: user response

## Tests

### 1. SOURCES.md paraphrase-boundary read across SKILL.md and both reference files

expected: No contiguous-reproduction or coined-term-adoption violations found. PF-0.1 and PF-3.1 framing clears assumptions A-03/A-04.
why_human: SOURCES.md states this is a semantic judgement no tool in this project's stack performs. Phase 6's LEG-04 is the formal gate. Tracked as WINDOWS.md id 3 (open).
scope_note: The 02-07 trim moved 20 worked ✗/✓ pairs into `references/worked-examples.md` and tightened 16 rule statements. Statements are in scope for this read; the frontmatter is not (byte-identical, sha256 `d5dd651a…`).
result: pass

### 2. Trigger pressure-test — run all 14 phrasings in a real harness session

expected: Every Must-fire row activates the skill; every Must-not-fire row does not. Observed/Date/Harness recorded for each.
why_human: Skill activation requires driving a live harness session this environment cannot start. Every row still reads "not yet observed". Tracked as WINDOWS.md id 4 (open). This is also the sole blocker on requirement CAT-10.
scope_note: `evals/pressure-tests.md`'s `## Scope` section binds these 14 phrasings to the SKILL.md frontmatter `description` whose first 14 lines hash to sha256 `d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675`. Confirm that hash still matches before recording observations; if it does not, the rows must be re-authored, not filled in.
hash_check: confirmed matching at UAT time (2026-09-11) — `head -14 skills/proof-first/SKILL.md | shasum -a 256` = `d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675`. The rows are runnable as written; they were not run.
result: issues
reason: "RUN 2026-09-20. All 14 phrasings were driven through live `claude -p` sessions by the committed runner `evals/trigger/run_trigger_test.py` (model claude-sonnet-5, harness claude 2.1.267), one fresh session per phrasing in a temp directory outside the repo with only skills/proof-first/ installed and no --bare. Activation was read from each session's own event stream (a Skill tool-use naming proof-first), not from its prose. 14 of 14 scoreable, 12 of 14 matched expectation. Must-fire: 9 of 9 fired. Must-not-fire: 3 of 5 stayed quiet; 2 fired that should not have — \"Build me a slide deck for the kickoff meeting.\" and \"Work out pricing and sizing for a 500-seat deployment.\" Observed/Date/Harness are now filled in for every row of evals/pressure-tests.md; full run block in evals/trigger/RESULTS-trigger.md. WINDOWS.md id 4 is closed (the test has been run). The over-fire is a new, separately tracked finding against CAT-10."
superseded_note: "The earlier `blocked` result and its stated reason — that this environment cannot start a fresh harness session — were true when written on 2026-09-11 and are no longer true. The method was proven at the Phase 3 UAT on 2026-09-14 and is now a committed, self-testing script."

### 3. Accept-or-fund decision on SC1's "reliably triggering description" clause

expected: A recorded decision — (a) accept the residual and record an override stating SC1 is met on the 9-of-9 must-fire-recall reading, with the over-fire tracked as CAT-10 / WINDOWS id 24 debt; or (b) fund the next lever (H1) as a further gap-closure round before Phase 2 is marked complete.
why_human: Whether a measured 9-of-25 over-fire count on an activation surface is acceptable to ship is a product-acceptance judgment this repository's tooling deliberately does not automate. CAT-10's decision rule adjudicates which lever wins on technical grounds (must-fire regression beats over-fire elimination); it does not adjudicate whether the residual itself is shippable.
evidence: "Arm B (shipped, unchanged 439-char description): must-not-fire 9 of 25 scoreable sessions fired; must-fire 45 of 45 fired. Arm A (tested, reverted): 0 of 25 and 40 of 45. p_attr = 0.0016. Full data: evals/trigger/RESULTS-trigger.md; rule and branch selection: evals/trigger/DECISION-RULE-cat10.md."
source: 02-VERIFICATION.md human_verification item 1
result: [pending]

### 4. Disposition for 02-REVIEW.md CR-01 — fail-open scope-hash guard

expected: Either a follow-up plan applies the documented fix (require a hash to be present, and scope the regex to the `## Scope` heading), or a new WINDOWS.md entry records the risk as explicitly accepted — consistent with how this same round recorded its other two findings as ids 26 and 27.
why_human: An unresolved CRITICAL code-review finding from this round currently has no disposition anywhere in the repository's tracking. It is dormant today (exactly one well-formed hash exists in evals/pressure-tests.md) but its blast radius is a future silent measurement-integrity failure — the class of failure this project's evidence discipline exists to prevent. A phase should not be marked complete with an unresolved critical finding carrying no recorded decision.
evidence: "evals/trigger/run_trigger_test.py:88-91 and 540-545. recorded_scope_hash() returns None when its whole-document regex finds no 64-hex token; the halt `if bound_hash and bound_hash != live_hash` is then silently skipped. Confirmed still present at HEAD by the verifier."
source: 02-VERIFICATION.md human_verification item 2
result: [pending]

## Summary

total: 4
passed: 1
issues: 1
pending: 2
skipped: 0
blocked: 0

## Gaps

<!-- Structured for /gsd-plan-phase --gaps. The prose statement this replaced is preserved
     verbatim as `note` below; nothing was softened, only reshaped so the planner can read it. -->

- gap_id: G-02-2
  truth: "Every Must-not-fire phrasing in evals/pressure-tests.md leaves the skill inactive."
  status: partially_resolved
  reason: "Measured 2026-09-20 by evals/trigger/run_trigger_test.py (claude-sonnet-5, claude 2.1.267, one fresh session per phrasing, verdict read from each session's own Skill tool-use event). Must-fire 9 of 9 fired. Must-not-fire 3 of 5 stayed quiet; 2 fired that should not have: \"Build me a slide deck for the kickoff meeting.\" and \"Work out pricing and sizing for a 500-seat deployment.\""
  severity: major
  test: 2
  requirement: CAT-10
  windows_id: 24
  root_cause: |
    CONFIRMED on the structural claim; INCOMPLETE on the causal one. Diagnosed by gsd-debugger
    2026-09-20, see debug_session. The orchestrator's first draft of this field asserted a
    clean causal story that the investigation partly refuted; it is corrected here rather than
    left standing.

    VERIFIED. The frontmatter `description` is a 439-character, purely inclusive string
    containing zero negation tokens (scanned). Every agreed exclusion lives somewhere the
    harness cannot read at activation time: `skills/proof-first/SKILL.md:308` (the body
    `## Limits` section) and `.planning/PROJECT.md:52-57`. Both over-firing prompts match
    those body exclusions on exact head nouns — `slide deck` against `slide decks and visual
    design`, `pricing and sizing` against `pricing calculation, sizing`. The description
    states what the skill is for and never once states what it is not for, so the must-fire
    half of the trigger list is the only half the field encodes.

    REFUTED — the differential is not explained. A third must-not-fire row, "Write launch copy
    for our new product announcement.", equally names a Limits exclusion (`marketing or brand
    writing`) and stayed quiet. The body is unread for all three alike, so absence-of-exclusion
    cannot be why two fired and one did not.

    REFUTED — lexical pull. The two prompts that fired share zero content words with the
    description. Two that did not fire share the word "write". A surface keyword-overlap
    explanation does not survive contact with the data.

    HYPOTHESIS, UNIDENTIFIED. The positive pull is therefore semantic rather than lexical, and
    which part of the description exerts it is not established. Candidate pulls named but not
    measured: the audience clause "for technical presales and bid teams", and "a customer-facing
    proposal". Whether an explicit negative clause is even honoured by the activation ranker is
    itself untested (H4 in the debug session) — a null result is a live possible outcome of the
    fix, not a sign the fix was executed badly.
  artifacts:
    - path: "skills/proof-first/SKILL.md"
      issue: "Frontmatter `description` (lines 3-10), 439 chars, inclusions only. The matching exclusions sit in the body `## Limits` section at line 308, which is never read at activation time."
    - path: "output-styles/proof-first.md"
      issue: "A real derivative — regenerated by `python3 tools/generate_derivatives.py` (OUTPUT_STYLE_PATH). Must be regenerated after any description change."
    - path: "prompts/system-prompt.md"
      issue: "The second real derivative (SYSTEM_PROMPT_PATH), omitted from this gap's first draft. Regenerated by the same command."
    - path: ".claude-plugin/plugin.json"
      issue: "CORRECTION — not generated. Carries a hand-maintained 148-character truncation of the description; tools/generate_derivatives.py never writes this file, and `python3 tools/check_repo.py` exits 0 with it stale. Nothing mechanical catches drift here, so a description change must update it by hand or consciously decide not to."
    - path: ".claude-plugin/marketplace.json"
      issue: "CORRECTION — not generated either: two more hand-maintained 148-character truncations, unenforced by check_repo.py."
    - path: "evals/pressure-tests.md"
      issue: "Its `## Scope` section binds all 14 recorded observations to the description whose first 14 lines hash to sha256 d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675 (confirmed still matching at 2026-09-20). Changing the description invalidates every Observed cell; the rows must be re-authored and re-run, never carried forward."
    - path: "evals/trigger/RESULTS-trigger.md"
      issue: "Records the same hash. A new run block is required, not an edit of the existing one."
    - path: "tools/check_repo.py"
      issue: "DESCRIPTION_MIN = 200 / DESCRIPTION_MAX = 1024 bound any new string. 200 is a floor."
  missing:
    - "Carry SKILL.md's existing Limits exclusions into the frontmatter `description` so the trigger surface states them — at minimum slide decks and visual design, pricing/sizing/commercial modelling, and marketing or brand writing. Reuse the agreed body wording; do not invent new scope."
    - "LENGTH, CORRECTED — this gap's first draft had it backwards and would have driven a plan that fails CI. `tools/check_repo.py` sets `DESCRIPTION_MIN = 200` / `DESCRIPTION_MAX = 1024`: 200 is a FLOOR, not a ceiling. Decision D-30 (02-CONTEXT.md:84) fixes the description as a front-loaded trigger list of roughly 400-600 characters and explicitly rejects 200 on the grounds that no target harness enforces it. The current string is 439 characters. Adding exclusions must land inside 400-600, keep the highest-value keywords first, and never shorten below 200."
    - "D-30 is flagged costly/one-way in 02-CONTEXT.md, and 03-RESEARCH.md:70 states the description's shape should not be reopened without a fresh discuss-phase pass. A plan that edits this field is reopening a locked decision and must say so in as many words, not slip it through as a bug fix."
    - "Change ONE thing. Do not bundle an exclusion clause with a rewrite of the inclusion half — with n small and the pull mechanism unidentified, a bundled change cannot be attributed to either intervention."
    - "Re-run `python3 tools/generate_derivatives.py` so output-styles/proof-first.md and prompts/system-prompt.md carry the new string; update the two .claude-plugin truncations by hand or record the decision not to; confirm `python3 tools/check_repo.py` still exits 0 (it does today)."
    - "ORDER MATTERS — re-author the `## Scope` hash in evals/pressure-tests.md to the new `head -14 skills/proof-first/SKILL.md | shasum -a 256` BEFORE running the test; the runner halts on a hash mismatch before it opens any session. Blank every Observed/Date/Harness cell — the old observations do not transfer."
    - "STATISTICAL POWER — n=1 per phrasing cannot close this. One quiet session bounds the fire rate only at p <= 0.95 (95% confidence); `claude -p` exposes no temperature or seed flag, so a single observation is not a rate. The re-run needs n >= 5 sessions per phrasing (p <= 0.45) and must be PAIRED against the current description, because without a pre-fix rate on the same instrument there is no denominator to show improvement against. That is 14 phrasings x 5 sessions x 2 arms = 140 live sessions. Budget it explicitly, or state a smaller n and the weaker claim it supports."
    - "Re-run `python3 evals/trigger/run_trigger_test.py` and append a NEW run block to evals/trigger/RESULTS-trigger.md — never edit the 2026-09-20 block. CAT-10 closes only on 9 of 9 must-fire AND 5 of 5 must-not-fire; a must-fire regression trades one measured defect for another and does not close it. Because H4 is untested, a re-run showing the over-fires persist is a valid measured outcome to record, not a failed plan."
    - "Record the outcome in .planning/WINDOWS.md id 24 and re-verdict CAT-10 in .planning/REQUIREMENTS.md against whatever the re-run actually measures."
  debug_session: ".planning/debug/DEBUG-cat10-trigger-over-fire.md"
  note: |
    Verbatim prose statement this entry replaces, from the 2026-09-20 UAT run:

    **CAT-10 — the `description` is measurably over-broad.** 2 of 5 near-miss phrasings activated the
    skill: a kickoff slide deck and a pricing/sizing calculation, both outside PROJECT.md's scope and
    SKILL.md's Limits section. The must-fire half of the trigger list works (9 of 9); the must-not-fire
    half does not hold. Narrowing the description changes a shipped, distributed trigger surface and
    invalidates the scope hash every recorded observation binds to, so it is recorded as a measured
    defect rather than patched inside the run that found it. Tracked in `.planning/WINDOWS.md`.
  measured: |
    CAT-10 gap-closure round (02-10-PLAN.md), a paired n=5 experiment under a six-branch decision
    rule committed BEFORE any session ran (evals/trigger/DECISION-RULE-cat10.md). Same instrument
    both arms: `run_trigger_test.py --model claude-sonnet-5 --repeats 5 --jobs 3 --timeout 600`,
    all 14 phrasings, 70 sessions per arm, 140 total (of the 170-invocation cap; no retries needed).

    Arm B (control, unchanged 439-char description, head-14 sha256 `d5dd651a…`):
    `OF_B/SN_B = 9/25` over-fires on the must-not-fire rows, `MH_B/SM_B = 45/45` must-fire hits —
    the same two phrasings that fired at n=1 (slide deck, pricing/sizing) now fire 5/5 and 4/5.

    Arm A (treatment, 551-char description with the exclusion clause this gap's `missing` field
    named, head-14 sha256 `9049c7d8…`): `OF_A/SN_A = 0/25` — every must-not-fire row scored zero
    fires, eliminating the original defect entirely on that half. But `MH_A/SM_A = 40/45`: the
    must-fire row "We're putting together our bid response — write the commercial section."
    regressed from 5/5 (Arm B) to 0/5 (Arm A) — a genuine must-fire regression, most plausibly
    because the appended clause's phrase "commercial modelling" shares the content word
    "commercial" with this unrelated, legitimate must-fire request (a hypothesis about mechanism,
    not confirmed further by this round).

    `p_attr` (Fisher exact two-tailed, `evals/trigger/stats.py`, on `[[9,16],[0,25]]`) = `0.0016` —
    the over-fire elimination is itself statistically attributable at this sample size, and is
    still not sufficient, because trading one measured defect for another does not satisfy a truth
    that says every must-not-fire phrasing AND the must-fire half both hold.

    Per the pre-committed precedence order (6, 5, 4, 1, 2, 3), the must-fire regression selects
    **Branch 4** — ahead of Branch 1, which Arm A's over-fire numbers alone would otherwise have
    selected. Branch 4's disposition: the 551-char treatment description was tested live, then
    REVERTED (`git checkout` to the pre-Task-4 commit for `SKILL.md`, both `.claude-plugin`
    manifests, and `evals/pressure-tests.md`; derivatives regenerated; `head -14` hash confirmed
    back to `d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675`). The shipped
    description is unchanged from the pre-round text. `WINDOWS.md` id 24 stays `open` with its
    description replaced by these measured counts. `REQUIREMENTS.md` CAT-10 stays `[ ]`.

    Full arm data, per-row counts, and Clopper-Pearson bounds: `evals/trigger/RESULTS-trigger.md`
    (three `## Run` blocks: the original 2026-09-20 n=1 observation, Arm B, Arm A — none edited,
    only appended to). Branch evaluation, longhand: `evals/trigger/DECISION-RULE-cat10.md`.

## Correction Log

- 2026-09-11 — Test 2 was recorded `pass` and then corrected to `blocked` in the
  same session. The operator confirmed the 14 trigger phrasings were never run.
  A pass would have asserted CAT-10 verified on evidence that does not exist,
  while `evals/pressure-tests.md` simultaneously stated no observation had been
  made — the exact contradiction this repository's evidence rule forbids. Nothing
  was written into `evals/pressure-tests.md`. Per the workflow, a blocked test is
  a prerequisite gate rather than a code issue, so no gap was opened and no fix
  plan was spawned.

## Addendum 2026-09-20 — test 2 run

Test 2 was recorded `blocked` on 2026-09-11 with the reason that this environment could not start
a fresh harness session, install the skill, and read back whether it activated. That was accurate
when written. It stopped being accurate on 2026-09-14, when the Phase 3 UAT proved the recipe, and
Phase 5 then ran the same pattern at scale. The blocker outlived its cause.

Running it changed the verdict rather than confirming it. The must-fire half of the trigger list
holds on every one of its nine phrasings. The must-not-fire half does not: the description pulls in
a kickoff slide deck and a pricing calculation, neither of which is presales writing. That is a
worse-looking result than `blocked` and a better one to have — an unrun test had left CAT-10's
status genuinely unknown, and the half of the file built to catch an over-broad description is
exactly the half that caught one.

CAT-10 therefore does not become satisfied. It moves from unverified to measured, with a named,
reproducible defect and a command that reproduces it.
