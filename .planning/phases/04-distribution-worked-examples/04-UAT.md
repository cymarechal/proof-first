---
status: testing
phase: 04-distribution-worked-examples
source: [04-VERIFICATION.md]
started: 2026-09-18T05:40:00Z
updated: 2026-09-18T05:40:00Z
---

## Current Test

number: 3
name: Each after column demonstrates its cited rule rather than restating it
expected: |
  Each after column in examples/before-after.md reads as an applied rewrite
  grounded in the deal brief, not a paraphrase of the rule text. The PF-1.9
  recast at line 20 genuinely leads with capability; the PF-3.3 marker is
  attached to a term, not to a whole quotation.
awaiting: user response

Tests 1 and 2 are blocked by design and need no response — 1 waits on a
published repository (Phase 6, LEG-04), 2 waits on Phase 5's benchmark. Test 3
is the first item a person can actually run today; test 4 follows it.

## Tests

### 1. Live install flow resolves against a published repository
expected: `npx skills add <real-owner>/<real-repo>` and `claude plugin marketplace add <real-owner>/<real-repo> && claude plugin install proof-first@proof-first` both resolve and install, including a marketplace.json whose plugin entry is now mechanically known-complete.
result: blocked — deferred by design
detail: |
  No git remote is configured and the repository is not published, so the real
  owner/repo string does not exist. A live install is a network-and-harness
  behavior no file-reading checker can observe.

  Changed this round: CR-01's closure removed the *additional* gating reason this
  item carried in the previous round. The checker that proves marketplace.json
  well-formed no longer overstates its coverage — deleting any of the nine
  required keys from the marketplace plugin entry now fails the build. What
  remains is only the pre-existing publish-location ceiling.

  Owner: WINDOWS.md entry 11, routed to Phase 6's LEG-04 launch gate.

### 2. Output style, system prompt and installed skill produce equivalent behavior
expected: All three distribution routes apply the same rule text, the same completeness audit, and the same artifact-family conventions, producing comparably disciplined output.
result: blocked — deferred by design
detail: |
  Authored in 04-03-PLAN.md as a `verification: backstop` truth precisely so no
  automated check can mark it passed before a benchmark runs. This project
  publishes measured claims or no claims.

  The structural half IS proven and unchanged: both derivatives are generator
  output, reproduce byte-for-byte, carry the identical sha256 stamp, and cover
  all 39 rule headings plus all four family headings.

  Owner: Phase 5.

### 3. Each after column demonstrates its cited rule rather than restating it
expected: Each after column reads as an applied rewrite grounded in the deal brief, not a paraphrase of the rule text; PF-1.9 genuinely leads with capability; PF-3.3 marks a term, not a full quotation.
result: [pending]
detail: |
  Authored in 04-02-PLAN.md as a `verification: backstop` truth. Unchanged this
  round — 04-11 did not touch `examples/before-after.md`.

  The mechanical half is closed and green: rule narration, PF-4.1 sentence
  length (0 of 17 ✓ sentences over the 25-word ceiling), and invented
  word-spelled counts are all enforced by CI codes. What no code in this stack
  can judge is whether a rewrite genuinely applies its rule — specifically the
  G-04-3 PF-1.9 recast at line 20 and the G-04-5 PF-3.3 re-attachment.

  Best read by someone unfamiliar with the project.

### 4. README reads as leading with a real example and its Install section is actionable
expected: A prospective evaluator understands what the skill does and how to install it within the first screen or two, with no confusion about which of the four install routes to pick.
result: [pending]
detail: |
  DIST-06's prose-quality half. Unchanged this round — 04-11 did not touch
  `README.md`.

  The structural half is CI-enforced and green: the first ✗ line sits at line 14,
  zero `(exists)` markers remain, all four install anchors are present beneath
  `## Install`, heading order is enforced, and cross-file identity with
  `examples/before-after.md` is discrimination-proven in both directions. Whether
  the lead-in *reads* as leading with an example is not checkable by any code here.

  Owner: WINDOWS.md entry 12 (open).

## Summary

total: 4
passed: 0
issues: 0
pending: 2
skipped: 0
blocked: 2

## Gaps
