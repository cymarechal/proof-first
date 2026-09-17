---
status: gaps_found
phase: 04-distribution-worked-examples
source: [04-VERIFICATION.md, 04-REVIEW.md]
started: 2026-09-17T08:21:12Z
updated: 2026-09-17T08:21:12Z
---

## Current Test

number: 0
name: all tests dispositioned
expected: |
  No test is awaiting a response. Tests 1 and 2 are deferred by design to
  Phases 6 and 5. Tests 3 and 4 were resolved by an independent adversarial
  read delegated to a subagent, per the project owner's standing instruction
  that judgment calls are delegated rather than escalated.
awaiting: none

## Tests

### 1. Live install flow resolves against a published repository
expected: `npx skills add <owner>/<repo>` and `claude plugin marketplace add <owner>/<repo> && claude plugin install proof-first@proof-first` both resolve and install.
result: blocked — deferred by design
detail: |
  This repository has no git remote and is not published, so the real owner/repo
  string does not exist. Plan 04-01 prohibited inventing it; the orchestrator
  resolved that plan's decision checkpoint by freezing a visibly-marked
  `<owner>/<repo>` placeholder, held identical across both manifests, the
  marketplace owner URL and README by `publish-location-drift`. No human can
  verify this today either. Owner: WINDOWS.md id 11, Phase 6 LEG-04.

### 2. Output style, system prompt and installed skill produce equivalent behavior
expected: All three routes apply the same rules and produce comparably disciplined output.
result: blocked — deferred by design
detail: |
  Authored in 04-03-PLAN.md as a `verification: backstop` truth precisely so no
  automated check can mark it passed. This project publishes measured claims or
  no claims, and no benchmark has run. The structural half IS proven: both
  derivatives are generator output, byte-reproducible, and carry all 31 PF- and
  8 MC- rule headings plus all four family headings. Owner: Phase 5.

### 3. Each after column demonstrates its cited rule rather than restating it
expected: Each after column reads as an applied rewrite grounded in the deal brief, not a paraphrase of the rule text.
result: FAIL
detail: |
  Resolved by an independent adversarial read (delegated subagent), then
  corroborated mechanically by the orchestrator. Four distinct defects:

  a. Rule narration inside the quoted prose, in all four pairs. Clauses such as
     "evidence a scoring committee can check against the buyer's own rubric, not
     a claim asserted without it" and "That answer stands first, before any
     account of ... platform breadth" restate the rule in the vendor's voice.
     This contradicts SKILL.md:261 ("No list of applied rules follows the
     prose") and is arguably worse than a trailing list, which is at least
     banned by name. The `Rules applied:` footer already exists outside the
     quotes and is the correct home for this rationale.

  b. PF-4.1 (25-word sentence limit) broken in 8 of 11 after-column sentences;
     longest 88 words, mean 40. The before columns break it once in 12, mean 17.
     Counted with bracketed marker spans stripped before splitting, the method
     04-07's `example-sentence-length` code applies. A first pass reported 10 of
     11 by counting markers as prose; that figure is superseded.
     Measured by the orchestrator, not asserted. On the catalog's one countable
     rule, the writing presented as correct scores worse than the writing
     presented as wrong.

  c. The solution-proposal pair inverts the rule it cites. PF-1.9 requires the
     capability stated first and the product named second, never the product as
     the sentence subject. The shipped sentence makes the architecture the
     subject and delivers the capability as a post-colon apposition, then
     announces the mapping because the sentence shape does not show it.

  d. Facts invented beyond the deal brief: "four sequenced waves" (line 13) and
     "three representative accounts" (line 34). deal-brief.md states that
     anything a later example asserts beyond its facts is an invented fact and a
     defect. These survive CI only because `unlisted-figure` covers currency,
     percent and ISO dates and does not catch word-spelled counts — a real hole
     in the checker, not just in the prose.

  Lower-cost: the PF-3.3 marker at line 34 is attached to a whole attributed
  quotation rather than to a term, so the deletion test never fires and the rule
  is demonstrated where it is not needed.

### 4. README reads well to a first-time reader
expected: A prospective evaluator understands what the skill does and how to install it within the first screen or two.
result: PASS-WITH-ISSUES
detail: |
  Macro-order is right (example before install before caveats) and the honesty
  posture is genuinely strong — the 30% conformance disclosure and the explicit
  refusal to claim behavioral equivalence should both be kept verbatim. Issues:

  a. No install command as printed is runnable. Routes 1 and 2 name the
     `<owner>/<repo>` placeholder; routes 3 and 4 work from a local clone today
     but README never says so. One sentence fixes it.
  b. The repository-layout legend explains a "planned" marker that appears zero
     times, while half the tree carries "(exists)" and the other half — including
     SKILL.md, the actual product — carries nothing, implying it does not exist.
  c. "Keeping derivatives in sync" is maintainer instruction sitting between
     Install and Status, in a reader's install path.
  d. Line 133 says "both measured models are Anthropic-hosted" but only
     claude-sonnet-5 is named in the figures above it.
  e. Lines 16-17 claim every rule exists to turn the left paragraph into the
     right one. False for PF-5.1-5.3 and PF-2.14-2.17 — an unmeasured claim
     about the repo's own rules, in a repo that bans them.
  f. Twelve lines of project description precede the first ✗.

  The showcased README example inherits defect 3a, so fixing 3 fixes part of 4.

## Summary

total: 4
passed: 0
issues: 2
pending: 0
skipped: 0
blocked: 2

## Gaps

- G-04-1: Rule narration embedded in the quoted prose of all four after columns
  in examples/before-after.md, contradicting SKILL.md:261. Relocate the rationale
  into the existing `Rules applied:` footers.
- G-04-2: PF-4.1 broken in 8 of 11 after-column sentences, bracket-stripped (max 88 words, mean
  45) while the before columns comply (1 of 12, mean 17). Split at clause
  boundaries; the split is nearly free once G-04-1's narration is deleted.
- G-04-3: examples/before-after.md line 20 inverts PF-1.9 — product as sentence
  subject, capability as apposition. Recast capability-first.
- G-04-4: "four sequenced waves" and "three representative accounts" are facts
  invented beyond examples/deal-brief.md. Either add canonical-figure rows or
  drop the counts. Additionally, `unlisted-figure` does not catch word-spelled
  counts — a new checker code is warranted so this class cannot recur silently.
- G-04-5: PF-3.3 marker attached to a whole quotation rather than to a term.
- G-04-6: README — no runnable install command is identified as runnable;
  self-contradicting layout legend; maintainer section inside the install path;
  unnamed second model at line 133; unmeasured claim about the repo's own rules
  at lines 16-17.
- G-04-7 (from 04-REVIEW.md, deferred): WR-01 `_owner_segment` mis-parses
  SSH-style and scheme-less GitHub URLs, latent until a real remote is set;
  WR-02 `generate_derivatives.py --check` docstring overclaims byte-for-byte
  comparison; WR-03 plugin-manifest checks silently assume exactly one skill
  folder without disclosing the ceiling.
