---
status: partial
phase: 04-distribution-worked-examples
source: [04-VERIFICATION.md]
started: 2026-09-18T05:40:00Z
updated: 2026-09-18T11:15:00Z
---

## Current Test

[testing closed for Phase 4 — 2 items deferred to later phases]

Round 2. Test 3 re-read PASSES — G-04-3 closed. Test 4's G-04-4 is closed too,
but the same cold read found a new defect in the text the fix wrote: gap G-04-8,
open and diagnosed. Tests 1 and 2 remain blocked by design — 1 waits on a
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
result: pass
retest_round: 2
retest_verdict: pass
prior_gap_status: G-04-3 CONFIRMED FIXED
retest_detail: |
  Round-2 cold read of the REPAIRED file, under a brief widened beyond round 1 to
  add product-scope correctness and quotation fidelity, so a re-test could catch a
  NEW defect rather than only confirm the old one gone. It found none that fail
  the test.

  (a) PF-1.9 applied, not paraphrased. Line 20 opens with the capability as the
  buyer's own obligation; AWS Control Tower appears only in sentence 2 as the
  means, with "that governance" tying product back to capability.

  (b) Every product-scope claim now true AND agreeing with the brief. Control
  Tower scoped to landing-zone governance across the new account structure, EC2 to
  compute, Aurora PostgreSQL to the migrated data layer, vSphere/Oracle only as the
  850-VM and 40-instance source - all matching deal-brief.md:22. The reader checked
  what each claim ATTACHES to, which is how round 1's defect hid: "It lands on
  Amazon EC2 ... and Amazon Aurora PostgreSQL ..." takes "the estate" as its
  antecedent ("those accounts" is plural), and the "for compute" / "for the
  migrated data layer" adverbials bind each target to the right half of the estate.
  No product is credited with work it does not do.

  (c) PF-3.3 marker correct - on the unquoted phrase, not the quotation, tracing to
  deal-brief.md:70.

  (d) Quotation fidelity clean. The file's one quotation is character-identical to
  deal-brief.md:70 (only the terminal period moves outside the quote marks),
  unsplit, unmerged, right speaker, plain "He said:" with no invented second beat.

  Noted weaknesses, none failing the test:
  - PF-4.1's 25-word ceiling forces the product into a standalone sentence where it
    is unavoidably that sentence's subject (the capability sentence is 24 words),
    whereas the rule's own exhibit at worked-examples.md:32 keeps it in a
    post-semicolon clause. A tension between two rules, not a violation of either.
  - The PF-3.3 marked span is slightly wider than the verbatim term (customer said
    "we", span says "the team"), and lands on the second occurrence because the
    first sits inside the direct quote where marking would corrupt it. Correct
    behavior, imprecise span.
  - UNSOURCED DELIVERABLE, orchestrator-verified: line 27 asserts "The migration
    delivers automated failover". deal-brief.md:37 records only that failover IS
    currently manual, and :27 that Marcus Feld WANTS that ended. Neither states the
    migration delivers automation. The claim carries no evidence and no marker. It
    violates none of the three rules that pair cites (PF-0.1, PF-1.25, PF-2.11 -
    PF-2.11 covers invented metrics/baselines/numbers, and this is none of those),
    which is why the verdict is pass. Recorded because an unevidenced deliverable
    claim in the flagship example file is thematically the same class as the two
    defects just closed. Owner decision, not a gap this round.
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
result: pass
resolved_round: 3
resolution: |
  G-04-8 closed by 04-14. The false universal negative is gone from all three
  places it lived: README.md, WINDOWS.md's rendered table, and WINDOWS.md's JSON.
  Orchestrator fact-checked the replacement text against source, assertion by
  assertion - /config listing unobserved (true), repository does drive live
  sessions via run_conformance.py running headless `claude -p` (true, :216),
  the ## Status figure comes from those sessions (true), a headless session has
  no /config picker (true). Code count held at 48; a 49th code was measured,
  refused, and the refusal recorded in tools/check_repo.py's module docstring
  and WINDOWS entry 17.

  No further adversarial cold read was run on the repaired text, by the
  stopping rule the user approved on 2026-09-18: a cold-read finding blocks only
  if it is checkably false; merely improvable prose goes to backlog. Re-reading
  changed prose indefinitely is the loop that rule exists to end.
retest_round: 2
retest_reported: "You tell me in the Install section that this repository never runs a live harness session - and then forty lines later you give me a measured number from ten live harness sessions. Which one is true?"
retest_severity: major
prior_gap_status: G-04-4 CONFIRMED FIXED by the same cold read - see retest_detail
retest_detail: |
  Round-2 cold read of the REPAIRED README. The original defect is closed; a new
  one, introduced by the repair, is open.

  G-04-4 CONFIRMED CLOSED. The reader checked route 3 specifically and called the
  handling "correct and unusually careful": README:45-47 states plainly that
  repo-root output-styles/ is the plugin-ship location and not a directory Claude
  Code scans, lines 76-78 give the mkdir + cp that fixes it, line 80 gives the
  project-scoped alternative, and the shipped file has valid name/description
  frontmatter so /config would in fact list it. Placeholder disclosure now
  precedes both commands that use it (README:38-41). Every path in the layout
  tree exists. Q1 (leads with a real example) passed again, with both quoted
  strings diffed verbatim against examples/before-after.md.

  NEW DEFECT - a false universal negative, introduced by this round's own fix:
  - README:83 (written by commit 63b5dfa, the G-04-4 fix) asserts: "this
    repository's own environment drives no live harness session."
  - README:111-113 describes evals/conformance/run_conformance.py as "a
    stdlib-only, self-testing scorer that drives live sessions against the
    shipped skill".
  - README:134-137 reports a measured figure from those sessions: claude-sonnet-5
    conformed in 3 of 10 scoreable sessions.
  - Orchestrator-verified in the source, not inferred from prose:
    run_conformance.py:216 builds ['claude', '-p', prompt, '--model', model,
    '--disallowedTools', ...] and :205 installs the skill into a temp
    .claude/skills/proof-first. The script drives real sessions.
  - The narrower statement that IS true: no INTERACTIVE session. The conformance
    harness runs headless `claude -p`, which has no /config picker. That
    distinction is what line 83 needed to make and did not.
  - Why this is the worst possible sentence to get wrong here: the page's own
    stated standard is "measured claims or none" (README:91, 160), and this is a
    universal negative the same page disproves forty lines later.

  Secondary observations (minor, recorded for the owner):
  - README:36 says "four install paths, one per harness class" - routes 2 and 3
    are both Claude Code, so the sentence mis-describes its own list.
  - README:149 opens a paragraph with the bare fragment "At minimum:" with no
    antecedent; reads as an editing artifact.
  - Routes 3 and 4 are described as running "from a local clone" (README:43-45),
    but no route states how to obtain the clone, and the only repository URL on
    the page is the unresolved placeholder. Read strictly, a reader with only
    this README can execute none of the four.
  - Status is ~40% of the page and puts "30.0%" on screen as the document's only
    number; lines 139-142 frame it correctly as a conformance-instrument figure,
    but a skimming evaluator walks away with "30%" attached to the skill.
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
passed: 2
issues: 0
pending: 0
skipped: 0
blocked: 2
retest_round_2: "test 3 re-read PASS (G-04-3 closed); test 4 re-read: G-04-4 closed but new gap G-04-8 opened"

## Gaps

- gap_id: G-04-8
  status: resolved
  resolved_by: 04-14-PLAN.md
  resolved_at: 2026-09-18
  truth: "README does not state, as fact, anything the same README disproves elsewhere on the page."
  reason_original: "Cold reader (round 2) reported: README:83 asserts 'this repository's own environment drives no live harness session', but README:111-113 describes run_conformance.py as driving live sessions and README:134-137 reports a measured figure from ten of them. Orchestrator-verified in source: run_conformance.py:216 builds a real `claude -p` invocation. Introduced by commit 63b5dfa, this round's own G-04-4 fix. The true narrower claim is that no INTERACTIVE session runs here - headless `claude -p` has no /config picker."
  severity: major
  test: 4
  regression_of: "none - new defect introduced by the G-04-4 repair"
  root_cause: "04-13 Task 1 had to state what the new check does NOT prove - the correct instinct, and the CR-01 lesson applied. Reaching for the strongest available disclaimer, it wrote a universal negative about the whole repository ('drives no live harness session') when the true scope was one narrow case (no INTERACTIVE session, so no /config picker). The repository does drive live sessions: run_conformance.py:216 builds a real `claude -p` invocation and :205 installs the skill into a temp .claude/skills/proof-first, and README:134-137 reports a measured figure from ten of them. Over-claiming a limitation is still over-claiming."
  contributing_cause: "No code can see it. tools/check_repo.py's 48 codes are per-file, per-pattern presence and drift checks; none compares two factual assertions in the same document for consistency. The gate was green across this defect, exactly as it was green across G-04-3. This is the third consecutive round in which a green gate coexisted with a false statement a cold reader caught on first pass."
  pattern_note: "Second consecutive round where the FIX introduced the next defect. f8ebf78 (PF-1.9 recast) produced G-04-3's false Control Tower scope; 63b5dfa (G-04-4 repair) produced this. Both were written while being careful, both passed the gate, both were caught only by a human-shaped read."
  artifacts:
    - path: "README.md"
      line: 83
      issue: "False universal negative; contradicts lines 111-113 and 134-137 of the same file."
  missing:
    - "Narrow README:83 to the interactive case: the conformance harness drives headless `claude -p` sessions, which have no /config picker, so the /config listing specifically is unobserved. Do not assert that no live session runs here."
    - "Consider whether a CI code can catch a self-contradicting factual claim of this shape. Assessment to make honestly: cross-sentence semantic contradiction is very likely NOT regex-checkable, and a code claiming to check it would be the CR-01 overstatement again."
  debug_session: ""

- gap_id: G-04-3
  status: resolved
  resolved_by: 04-12-PLAN.md
  resolved_at: 2026-09-18
  truth: "Each after column reads as an applied rewrite grounded in the deal brief, not a paraphrase of the rule text; PF-1.9 genuinely leads with capability; PF-3.3 marks a term, not a full quotation."
  reason: "Cold reader reported: examples/before-after.md:20 states AWS Control Tower delivers governance across Halverton Mutual's on-premises VMware and Oracle estate. Control Tower governs AWS accounts, not on-premises VMs. Self-contradicts sentence 1 of the same column ('every account in its new estate'), contradicts deal-brief.md:22 and worked-examples.md:32 (both scope it to 'the new account structure'), and is a regression introduced by f8ebf78's PF-1.9 recast. The two items the test was written to check — PF-1.9 capability-first shape and PF-3.3 term-level marking — both passed."
  severity: major
  test: 3
  root_cause: "Commit f8ebf78 recast the Solution proposal check column into three sentences so PF-1.9's capability-first requirement would be satisfied. The pre-existing single sentence correctly attached governance to the migration target ('moves ... onto Amazon EC2 ... governed end to end by AWS Control Tower's account-level guardrails'). The split left the noun phrase 'on-premises estate of 850 VMware vSphere virtual machines and 40 Oracle Database instances' stranded as the object of the new governance sentence, silently re-scoping the product claim from the post-migration account structure to the pre-migration estate. The PF-1.9 fix was verified for shape, not for the truth of the sentence it created."
  contributing_cause: "No CI code checks product-scope semantics. tools/check_repo.py's example-facing codes (example-rule-narration, example-sentence-length, before-after-spelled-count, before-after-citation-missing, before-after-family-missing) cover narration, sentence length, word-spelled counts, citations and family headings - none evaluates whether a named product is claimed to do something it does not do. The file is structurally green and substantively wrong at the same time."
  artifacts:
    - path: "examples/before-after.md"
      line: 20
      issue: "Sentence 2 claims AWS Control Tower delivers governance across the on-premises VMware/Oracle estate. Control Tower governs AWS accounts and OUs."
  authorities_contradicted:
    - "examples/deal-brief.md:22 - 'AWS Control Tower for landing-zone governance across the new account structure'"
    - "skills/proof-first/references/worked-examples.md:32 - 'AWS Control Tower provides that governance boundary across the new account structure'"
    - "examples/before-after.md:20 sentence 1 - 'every account in its new estate'"
  missing:
    - "Re-scope before-after.md:20 sentence 2 so governance attaches to the new account structure, not the on-premises estate, while preserving the capability-first order PF-1.9 requires and the PF-4.1 25-word ceiling."
    - "Re-check README.md - it reproduces the RFP/RFI pair only, so it is unaffected, but confirm cross-file identity checks still pass after the edit."
    - "Decide and record whether product-scope truth is checkable by any code in this stack. Assessment from this round: it is semantic and not regex-checkable, so it belongs in the human-verification backstop, not in a new CI code that would overstate its coverage."
  secondary_defects:
    - "examples/before-after.md:34 - the PF-2.14 marker reads 'confirm this delivery date' but the text it attaches to names no date."
    - "examples/before-after.md:34 - deal-brief.md:70 records one Feld utterance; the line renders it as two statements joined by 'He added:', inventing a discourse sequence the brief does not record."
  debug_session: ""


- gap_id: G-04-4
  status: resolved
  resolved_by: 04-13-PLAN.md
  resolved_at: 2026-09-18
  truth: "A prospective evaluator understands what the skill does and how to install it within the first screen or two, with no confusion about which of the four install routes to pick."
  reason: "Cold reader reported: README line 38 promises routes 3 and 4 work today from a local clone, but route 3's output style is never discoverable from a bare clone - output-styles/ at repo root is the plugin-shipped location, and the plugin route is blocked on publication. No copy/symlink step is stated anywhere."
  severity: major
  test: 4
  root_cause: "README.md:38 asserts routes 3 and 4 'work today, from a local clone'. Route 3's file is committed at repo-root output-styles/proof-first.md, which is the PLUGIN-ROOT discovery location - live only once the repository is installed as a plugin. Claude Code scans ~/.claude/output-styles/ and <project>/.claude/output-styles/ for a bare clone, neither of which this repository populates. README.md:65-67 gives route 3 in full as 'Select it through /config', with no step between file-exists and select. So route 3's real enabling mechanism is route 2, which the README itself correctly says will not resolve until publication."
  contributing_cause: "tools/check_repo.py's readme-install-path-missing code verifies that all four install anchors are present beneath ## Install. It verifies nothing about whether a stated route is executable. The structural half of DIST-06 is green precisely because the check measures presence, not truth - the same class of overstatement CR-01 closed for marketplace.json."
  artifacts:
    - path: "README.md"
      line: 38
      issue: "Claims routes 3 and 4 both work today from a local clone. Route 3 does not."
    - path: "README.md"
      line: 65
      issue: "Route 3 states 'Select it through /config' with no installation step; the file is not on any path Claude Code scans for a bare clone."
  verified_by_orchestrator:
    - "Repository has .claude/ containing only CLAUDE.md; no .claude/output-styles/ exists."
    - "output-styles/proof-first.md exists at repository root only; no copy or symlink elsewhere."
    - "grep over README.md finds no occurrence of ~/.claude, .claude/output-styles, cp, or symlink."
    - "output-styles/proof-first.md frontmatter carries keep-coding-instructions: false and no force-for-plugin, so nothing auto-applies it either."
  missing:
    - "State the missing step for route 3 - copy or symlink output-styles/proof-first.md into ~/.claude/output-styles/ (or the project's .claude/output-styles/) - or stop claiming route 3 works today from a bare clone. Whichever is chosen, README.md:38's 'routes 3 and 4 work today' sentence must agree with it."
    - "Consider a CI code that proves each route stated as working-today is executable from a clean clone, so this class of claim cannot go structurally green while being false."
  secondary_defects:
    - "README.md:7 says the rules turned 'a paragraph like the one on the left into the one on the right', but lines 14-15 stack vertically. There is no left and right."
    - "README.md:7-10 is one 63-word sentence of abstraction between the heading and the example - the tell-before-showing move the skill exists to delete."
    - "README.md:17 'Rules applied: PF-2.1, MC-11' is opaque and unlinked at point of use; NUMBERING.md is not named until line 85."
    - "README.md:34-36 and 41-42 disclose the <owner>/<repo> placeholder twice in near-identical words, both carrying the garbled clause 'every command and manifest that states it is checked to agree'."
    - "README.md:77-137 - ## Status is about a quarter of the file, with lines 114-131 a single unbroken 18-line paragraph, denser than anything describing what the skill does."
  debug_session: ""

