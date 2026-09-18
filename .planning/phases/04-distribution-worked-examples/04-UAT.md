---
status: partial
phase: 04-distribution-worked-examples
source: [04-VERIFICATION.md]
started: 2026-09-18T05:40:00Z
updated: 2026-09-18T07:25:00Z
---

## Current Test

[testing paused — 2 items outstanding]

Tests 3 and 4 are resolved: both returned issues, recorded below with gaps
G-04-3 and G-04-4. Tests 1 and 2 remain blocked by design — 1 waits on a
published repository (Phase 6, LEG-04), 2 waits on Phase 5's benchmark. Neither
is a Phase 4 code defect and neither spawns a gap.

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
result: issue
reported: "The Solution proposal check column says AWS Control Tower governs Halverton Mutual's on-premises VMware and Oracle estate, which is not a thing Control Tower does - it governs AWS accounts - so the one sentence where the product is supposed to be named as the means of delivering the capability gets the technical fact wrong, in the example file whose whole job is showing a technical evaluator that the author understands the estate."
severity: major
reader: cold first-time reader, no project context
pf19_shape_half: pass
pf33_half: pass
detail_reported: |
  The two items this test was written to check both PASSED. A third defect, not
  anticipated by the test, was found in the same sentence the PF-1.9 fix created.

  (a) PF-1.9 capability-first SHAPE: PASS. Line 20 opens "Halverton Mutual must be
  able to govern every account in its new estate from one place, under guardrails
  the team can see and enforce" - buyer is the subject, predicate is what they must
  be able to do, no product until sentence 2. A real applied rewrite grounded in
  Marcus Feld's stated need (deal-brief.md:27,70), not a paraphrase of PF-1.9's
  own wording.

  (b) PF-3.3 marker placement: PASS. At line 34 the marker sits on a term-phrase
  inside the vendor's own sentence - "a landing zone the team can actually govern
  [PF-3.3: customer's term, retained - Marcus Feld, discovery]" - not on a whole
  quotation or sentence. The term traces to Feld's verbatim words at
  deal-brief.md:70 with only the pronoun shifted. The two attributed quotations
  earlier in the line correctly carry no marker, so it fires once on first unquoted
  reuse and never repeats. Commit 8e3f7f1 made this placement deliberately; it is
  right.

  THE DEFECT - factual regression at before-after.md:20, sentence 2:
  - Text: "AWS Control Tower delivers that governance across Halverton Mutual's
    ON-PREMISES estate of 850 VMware vSphere virtual machines and 40 Oracle
    Database instances."
  - AWS Control Tower governs AWS accounts and OUs. It does not govern on-premises
    VMware VMs or Oracle instances.
  - Self-contradicting: sentence 1 of the same check column correctly scopes the
    capability to "every account in its NEW estate", and sentence 3 separately
    states that estate "moves onto Amazon EC2 ... and Amazon Aurora PostgreSQL" -
    so the governance claim is explicitly pinned to the pre-migration estate.
  - Contradicts the canonical brief: deal-brief.md:22 scopes Control Tower to
    "landing-zone governance across the new account structure".
  - Contradicts the skill's own PF-1.9 exhibit:
    skills/proof-first/references/worked-examples.md:32 reads "AWS Control Tower
    provides that governance boundary across the new account structure".
  - Introduced by the PF-1.9 fix itself. Verified by the orchestrator against git:
    f8ebf78^ read "...onto Amazon EC2 ... governed end to end by AWS Control
    Tower's account-level guardrails" - governance correctly attached to the
    target. Splitting that into three sentences to make capability lead left the
    "on-premises estate" noun phrase stranded as the object of the governance
    sentence.
  - Why this matters more than its size: this is the flagship example file, and
    the project's core value is making complex things simple without making them
    wrong. A technically false product-scope claim here is the exact failure the
    skill exists to prevent.

  Other pairs verified sound:
  - RFP/RFI check (line 13) demonstrates MC-11 - cites Q1 at 30% and keeps
    question-level weighting distinct from the three top-level rubric weights,
    the specific failure MC-11 describes (completeness-audit.md:46-56). PF-2.1
    demonstrated via the buyer's own figures (850, 40, 6-hour).
  - Executive summary check (line 27) demonstrates all three: buyer's situation
    first with no vendor or product named (PF-0.1), Diane Osoria named with her
    own stated measures (PF-1.25, deal-brief.md:26,72,77), and a GAP marker where
    the overrun baseline would be (PF-2.11, deal-brief.md:34,45).
  - Fact tracing clean: 30%, 6, 850, 40, $2,300,000, 14, 8, SOC 2 Type I/Type II
    and all five product names trace to a Canonical figures row or a named party.
    Items with no brief row are proposed-method statements, not asserted deal
    facts: "scheduled maintenance window" (:13), "guardrails the team can see and
    enforce" (:20), "an out-of-band change to any account is blocked", "written
    summary due before the next scheduled call", "the Kestrel Systems Group
    solutions architect who ran the session" (:34).

  Secondary observations (minor, not counted against the verdict):
  - The PF-2.14 marker at :34 says "confirm this delivery date" but the text it
    attaches to names no date.
  - deal-brief.md:70 records ONE Feld utterance ("We need a landing zone we can
    actually govern - right now every VM is a snowflake."). Line 34 renders it as
    two statements joined by "He added:", inventing a discourse sequence the brief
    does not record. Orchestrator confirmed against the brief.
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
result: issue
reported: "Route 3 says it 'works today, from a local clone' - but I cloned it, and output-styles/proof-first.md never shows up in /config, because a file sitting at the repo root isn't anywhere Claude Code looks for output styles. So of the two routes the README promises are usable right now, one of them doesn't actually run, and the README never tells me the step I'm missing."
severity: major
reader: cold first-time evaluator, no project context
lead_example_half: pass
detail_reported: |
  Q1 (leads with a real example) PASSED. The pair lands at lines 12-17, inside the
  first screen, reproduced verbatim from examples/before-after.md. The x column is
  a fair likeness of real bid boilerplate, not a strawman; the check column beats
  it on grounds a skeptic can verify (30% scoring weight, 850 VMs, 40 Oracle
  instances, the 6-hour settlement gate). Disclosed caveat: the after column adds
  facts the before column never had, but lines 8-10 name the shared deal brief as
  the source, so it is disclosed rather than smuggled.

  Q2 (Install actionable) FAILED, on one checkable point:
  - README line 38 states routes 3 and 4 "work today, from a local clone".
  - README lines 65-67 give route 3 in full as: the file is a Claude Code output
    style, "Select it through /config". No step sits between "the file exists in
    the clone" and "select it".
  - Claude Code discovers output styles from ~/.claude/output-styles/ or a
    project's .claude/output-styles/. A repo-root output-styles/ directory is the
    plugin-shipped location, live only once the repo is installed as a plugin.
  - Verified independently by the orchestrator: the repo has .claude/ but no
    .claude/output-styles/; output-styles/proof-first.md exists at root only; and
    grep finds no copy, symlink, or path instruction in README.md.
  - So route 3's real enabling mechanism is route 2, which the README correctly
    says does not resolve until publication. Routes 1 and 2 are both gated on the
    unpublished <owner>/<repo>, making routes 3 and 4 the entire usable install
    surface today - and one of those two is wrong as written.
  - Route 4 genuinely works: prompts/system-prompt.md is 745 lines and "paste it
    whole" is accurate.

  Secondary observations (not gaps, recorded for the owner):
  - Line 7 says the rules turned "a paragraph like the one on the left into the
    one on the right", but lines 14-15 stack vertically, x above check. There is
    no left and right. Costs trust in a document whose pitch is not saying things
    that aren't so.
  - Lines 7-10 are one 63-word sentence of abstraction between the heading and the
    example - the "tell them before showing them" move this skill exists to delete.
  - "Rules applied: PF-2.1, MC-11" at line 17 is opaque and unlinked at point of
    use; NUMBERING.md is not named until line 85.
  - Lines 34-36 and 41-42 disclose the <owner>/<repo> placeholder twice in
    near-identical words, both carrying the garbled clause "every command and
    manifest that states it is checked to agree".
  - ## Status runs lines 77-137, about a quarter of the file, with lines 114-131 a
    single unbroken 18-line paragraph. The honesty is the best thing in the
    document, but it is the third section a reader hits and denser than anything
    describing what the skill does.
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
issues: 2
pending: 0
skipped: 0
blocked: 2

## Gaps

- gap_id: G-04-3
  truth: "Each after column reads as an applied rewrite grounded in the deal brief, not a paraphrase of the rule text; PF-1.9 genuinely leads with capability; PF-3.3 marks a term, not a full quotation."
  status: failed
  reason: "Cold reader reported: examples/before-after.md:20 states AWS Control Tower delivers governance across Halverton Mutual's on-premises VMware and Oracle estate. Control Tower governs AWS accounts, not on-premises VMs. Self-contradicts sentence 1 of the same column ('every account in its new estate'), contradicts deal-brief.md:22 and worked-examples.md:32 (both scope it to 'the new account structure'), and is a regression introduced by f8ebf78's PF-1.9 recast. The two items the test was written to check — PF-1.9 capability-first shape and PF-3.3 term-level marking — both passed."
  severity: major
  test: 3
  artifacts: []
  missing: []

- gap_id: G-04-4
  truth: "A prospective evaluator understands what the skill does and how to install it within the first screen or two, with no confusion about which of the four install routes to pick."
  status: failed
  reason: "Cold reader reported: README line 38 promises routes 3 and 4 work today from a local clone, but route 3's output style is never discoverable from a bare clone - output-styles/ at repo root is the plugin-shipped location, and the plugin route is blocked on publication. No copy/symlink step is stated anywhere."
  severity: major
  test: 4
  artifacts: []
  missing: []
