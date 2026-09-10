# Phase 2: Rule Catalog & Integrity — SKILL.md Core - Context

**Gathered:** 2026-09-11
**Status:** Ready for planning

<domain>
## Phase Boundary

Author the shipped skill's prose rule catalog and both of its modes, in the `PF-` namespace Phase 1 froze:

1. **The numbered rule catalog** — `skills/proof-first/SKILL.md`, organised on the six frozen PF sections, self-contained, under the progressive-disclosure ceiling, with valid frontmatter and a description that triggers (CAT-01, CAT-02, CAT-03, CAT-04, CAT-06, CAT-08, CAT-09, CAT-10).
2. **The integrity rules** — two refusals and four flag categories, living in their own sub-block of `PF-2` (INT-01 through INT-06).
3. **The deletion test and its provenance override** — including the customer-verbatim retention rule (CAT-04, CAT-05).
4. **Write mode and check mode** — drafting that follows the catalog, and checking that returns rule number, offending text, and a compliant rewrite (MOD-01, MOD-02).
5. **The reference files those require** — `references/deletion-test.md` and `references/checklist.md`.
6. **CI enforcement of this phase's own claims** — extending `tools/check_repo.py` so the catalog's consistency and the frontmatter's validity are checked, not asserted.

**Not in this phase:** the `MC-` completeness audit and `references/completeness-audit.md` (Phase 3); `references/artifact-patterns.md` and the four artifact-family conventions (Phase 3); three-category check output, artifact classification, and the citation guarantee — MOD-03, MOD-04, MOD-05 (Phase 3); distribution manifests, output style, system prompt, worked before/after examples (Phase 4); the linter, benchmark, and judge (Phase 5); the legal review gate and README claims (Phase 6).

</domain>

<decisions>
## Implementation Decisions

### Catalog Shape and Rule Form

- **D-01:** **One ID per rule, with a mandatory `Replace with:` half.** CAT-02's subtractive/constructive pairing is expressed inside a single numbered unit, not as two IDs. A rule cannot be authored without its constructive half, so the pairing cannot be half-read by a model or half-cited by check mode. One citation covers both directions of the fix. — **Reversibility:** one-way — splitting a rule into two IDs later renumbers nothing but changes what every published citation resolves to; merging two into one strands the retired ID under D-04 of Phase 1's deprecation-never-deletion rule.
- **D-02:** **A micro-example appears only on rules where judgement is required.** The deletion test, the Command of the Message element rules, and the integrity flags each carry one short ✗/✓ pair drawn from `examples/deal-brief.md`. Mechanical rules — sentence length, active voice, modal discipline — carry statement and `Replace with:` only. Uniform examples put the catalog over CAT-08's ceiling; no examples leaves the judgement rules to be applied inconsistently. — **Reversibility:** costly — adding or removing examples later rewrites every affected rule body and re-runs the line budget.
- **D-03:** **Target 30–35 rules in v1, with the frozen reserved ranges deliberately under-filled.** The research proposed 35–45 (`.planning/research/ARCHITECTURE.md:136`); D-02's example cost brings the workable number down. Under-filling is the intended use of the reserved ranges — a v1.1 rule takes the next free number in its section without disturbing a citation.
- **D-04:** **`PF-0` holds exactly one rule, `PF-0.1`, with its remaining 8 slots reserved.** CAT-03 and success criterion 3 require exactly one opening instruction resolved from the three frameworks' overlapping reframe concepts. "Exactly one" means one ID: `PF-0.1` carries what a reframe is, what it must contain, and what disqualifies it. Numbered sub-conditions in `PF-0` would reproduce the three-conflicting-rules problem the requirement exists to prevent. — **Reversibility:** one-way — same citation-stability contract as Phase 1's D-01.
- **D-05:** **`PF-2` is carved into named sub-blocks: `PF-2.1`–`PF-2.10` Proof, `PF-2.11`–`PF-2.20` Integrity.** Recorded in `NUMBERING.md` as a sub-block table in the same form as the existing `PF-1` table. Proof rules (attach evidence, name the source) and integrity rules (refuse, flag) are different jobs, and a rule added later to Integrity must not land next to a Proof rule. — **Reversibility:** one-way — the sub-block boundary is enforced by `tools/check_repo.py`'s `range-id` check once written, and moving it reassigns which rules are in range.

### Persuasion Preservation

- **D-06:** **`PF-1` carries the structural persuasion engine; `PF-5` carries explicit protective rules.** The Command of the Message spine — Before/After contrast, named metrics, differentiators — is the mechanism by which specificity substitutes for adjectives (`.planning/research/PITFALLS.md:13`). `PF-5` adds a small ruleset naming devices the catalog must not strip: contrast structures, second-person address to the buyer's stated priorities, and confident unhedged claims when evidenced.
- **D-07:** **Every `PF-5` protective rule states a presence requirement and a matching prohibition on check mode itself.** Positive half: the document contains at least one explicit before/after contrast. Negative half: check mode never flags second-person address, a confident evidenced claim, or a contrast structure as a violation. "Do not flatten" is not a testable predicate; these two halves are. Covers both failure directions — a document that lost its rhetoric, and a checker that strips it.
- **D-08:** **The self-check runs two passes: subtract, then add.** Pass 1 finds violations to remove. Pass 2 is a mandatory additive sweep asking whether a contrast, a metric with a baseline, a differentiator, and a reframe are present. Missing ones are reported exactly as removals are. This makes `PITFALLS.md`'s named warning sign — a self-check that only ever finds things to delete — structurally impossible rather than discouraged.
- **D-09:** **Confidence is licensed by adjacent evidence, never by hedging.** An unhedged claim requires its evidence in the same or the next sentence. No evidence means delete and mark the gap. Hedging is never the repair for missing evidence. One rule reconciles the voice concern (models default to hedged prose), the fabrication concern (INT-01/02), and the contractual-exposure concern (`PITFALLS.md:185`).

### Integrity: Refusals and Flags

- **D-10:** **Write mode emits the true part and marks the gap where the claim would go.** Asked to write about a SOC 2 Type II report Kestrel does not hold, the sentence ships with the unverifiable claim replaced by an explicit marker. Nothing false is emitted, and nothing silently disappears — the omission is visible in place, not only in a list the reader may not reach.
- **D-11:** **Provenance never suppresses an integrity rule — both fire.** A term that is customer-verbatim *and* an unmakeable compliance claim is retained under `PF-3.3` for compliance-matrix alignment *and* carries a `REVIEW` flag. Retention is a vocabulary decision; the flag is a truth decision. The catalog states this precedence explicitly rather than leaving it to be discovered. A worked example must show two markers on one phrase.
- **D-12:** **An absence found by the additive sweep produces a gap marker like any missing evidence.** A missing differentiator is as visible as an invented metric, through the same mechanism. A thin-input draft comes back heavily marked, which is the correct signal.
- **D-13:** **`SKILL.md` carries a Limits section covering both cannot-verify and out-of-scope.** It states that the skill flags but cannot verify disclosure authorization, certification status, competitor-claim accuracy, or legal exposure; and that it does not produce slide decks, pricing, sizing, or commercial modelling, per PROJECT.md's Out of Scope. A clean check report is not legal clearance, and the skill says so.

### Marker Vocabulary

This is the phase's hardest interface. Phase 4's worked examples show it, Phase 5's linter counts it, and Phase 3's check output groups it.

- **D-14:** **Three marker types share one bracket grammar, and every marker carries the rule number that raised it.**
  - `[PF-2.11 GAP: no measured baseline for the overrun — Halverton has never instrumented it]`
  - `[PF-2.17 REVIEW (compliance): the RFP requires Type II; Kestrel's Type II observation window closes after submission]`
  - `[PF-3.3: customer's term, retained — RFP Q3]`

  Carrying the rule number is what makes `PITFALLS.md:185`'s recommendation real — check mode can cite an integrity flag exactly as it cites a prose violation. It also means `tools/check_repo.py`'s existing `undefined-id` check, which already scans `skills/` and `examples/` for `PF-#.#` tokens against `NUMBERING.md`'s Allocated IDs table, validates every marker in a worked example with no new code. — **Reversibility:** one-way — Phase 4's committed examples and Phase 5's committed generations and linter both bind to this grammar; changing it invalidates published artifacts and recorded benchmark data.
- **D-15:** **Output carries a trailing register listing every marker, with no Owner column.** The register is what a bid manager works from; the inline copy is what stops a marker being missed. It carries marker type, rule, and what is needed. It does **not** name an owner — the skill cannot know a customer's or a vendor's internal org, and inventing one in the very table meant to police fabrication is the failure INT-01 exists to prevent.
- **D-16:** **A retained customer term is marked on its first occurrence only.** An RFP answer mirroring the question's vocabulary would otherwise carry a marker every few sentences. Noise is bounded by the count of distinct retained terms, not by total uses.
- **D-17:** **A marker still present when check mode runs is compliant, and reported as outstanding.** Its presence means the rule was honoured — nothing was fabricated — so it is not a prose violation. It still surfaces in the register so it cannot ship unresolved. This distinguishes "the writer did the right thing" from "the document is ready to send", which a pass/fail verdict cannot.

### Modes: Write and Check

- **D-18:** **Write mode output is: one line stating the assumed artifact family, the prose, then the register. No rule trace.** The assumed-family line surfaces a correctable assumption and puts the sentence MOD-04 will formalise in Phase 3 in place now, so Phase 3 tightens an existing behaviour rather than introducing a new one. No list of applied rules — write mode writes, check mode explains, and the register already carries everything the writer must act on.
- **D-19:** **Check mode returns a report only, never a corrected document.** Every change stays a decision the writer makes with the rule number in front of them. A corrected document is the artifact a rushed writer would use, which would turn a teaching tool into an autocorrect and undercut the citations MOD-02 exists to deliver.
- **D-20:** **The report is blocks — rule ID, quoted offending text, compliant rewrite — grouped under two labelled categories now: "Prose violations" and "Integrity flags".** Phase 3's MOD-03 adds "Completeness gaps" as a third group and changes nothing else. Shipping a flat list in Phase 2 would force MOD-03 to restructure an output format Phase 4's examples were already authored against.
- **D-21:** **Ordering is integrity first, then prose in document order.** Findings that can cost a deal or create legal exposure are read first; within prose, document order lets the writer work top to bottom through their own document. `PITFALLS.md:156`'s attention-decay concern applies to a long report as much as to a long skill.
- **D-22:** **A rewrite that needs unavailable evidence carries the marker in place.** The proposed rewrite is itself compliant prose containing `[PF-2.11 GAP: ...]`. One marker vocabulary across both modes, and the rewrite is directly pasteable. MOD-02 gets a real rewrite rather than a refusal.

### Customer Source Material and Provenance

- **D-23:** **Customer source material is a named optional input the skill asks for once.** At the start of a drafting task the skill states what it can use — RFP question text, discovery notes, stated requirements — and asks for it. It proceeds either way. `PF-3.3` fires only against material actually supplied; inferring provenance from whatever the writer pasted would let the vendor's own buzzwords launder themselves as customer terms, which is exactly what `PF-3.2`'s per-token test exists to stop.
- **D-24:** **When no source material is supplied, the skill announces once that the override is inactive.** One line stating that `PF-3.3` cannot fire and terms will be judged by the deletion test alone. A writer whose RFP vocabulary gets stripped needs to know that supplying the RFP text would have prevented it.

### File Layout and Progressive Disclosure

- **D-25:** **Phase 2 ships `SKILL.md`, `references/deletion-test.md`, and `references/checklist.md` — and nothing else in the skill folder.** `references/completeness-audit.md` and `references/artifact-patterns.md` are Phase 3's, and are not pre-created; Phase 1's D-15 established that empty placeholder files age badly, and `NOTICES.md`'s pointer check already skips a listed path that does not yet exist.
- **D-26:** **The deletion test is three rules plus a reference table.** `PF-3.1` the test itself, `PF-3.2` per-token application so a real technical noun cannot launder a decorative modifier riding on it, `PF-3.3` the provenance override for customer-verbatim terms (CAT-05). `references/deletion-test.md` carries the expanded edge-case table for the four classes `.planning/research/PITFALLS.md:38` names — connotation-only terms, customer-first terms, RFP-mandated wording, half-empty compounds. Documenting them is required: an undocumented exception looks like an inconsistently applied rule.
- **D-27:** **`references/checklist.md` ships in Phase 2 with the `PF` rows; Phase 3 adds `MC` rows.** `NUMBERING.md` never ships to an installed user (Phase 1's D-16), so without this file the installed skill has no in-folder list of which IDs exist, and nothing distinguishes a number the model read from a number it recalled — the failure `.planning/research/PITFALLS.md:156` documents. This is the mechanism MOD-05 will rely on in Phase 3.
- **D-28:** **Every reference pointer states the named condition that requires opening the file.** "Before applying `PF-3.1` to a compound term, or to any term appearing in the customer's own source material, read `references/deletion-test.md`." "Before emitting any rule citation in check mode, read `references/checklist.md`." A condition a model can match against, not an invitation it will decline — progressive disclosure only works if the pointer is specific (`.planning/research/ARCHITECTURE.md:128`).

### Frontmatter and Triggering

- **D-29:** **No framework marks appear in the frontmatter `description`.** It triggers on artifact types and the phrasings a writer actually uses: RFP response, RFI, solution proposal, executive summary, demo script, discovery, presales, bid. `.planning/research/PITFALLS.md:156` recommends naming the frameworks as trigger keywords; Phase 1's D-11 established the opposite instinct for filenames because they get scraped and indexed, and a `description` is replicated harder than a filename — it lands in every registry, every marketplace listing, and every fork. Accepted cost: a user who says "check this against MEDDICC" may not fire the skill. — **Reversibility:** costly — a published description propagates into registry indexes and forks that do not re-fetch.
- **D-30:** **The description is a front-loaded trigger list of roughly 400–600 characters.** No target harness enforces 200 — the four DIST requirements name the skills CLI, the plugin marketplace, an output style, and a paste-able system prompt, not claude.ai upload. Highest-value keywords come first in case any harness truncates. Accepted cost: this closes off a claude.ai upload path without an edit, and `.planning/research/STACK.md` flags 200 as the safe figure there.
- **D-31:** **A trigger pressure-test is recorded in the repo.** A committed file listing natural phrasings that must fire the skill and near-miss phrasings that must not, with observed results, the date, and the harness they were run on — mirroring the sibling project's `pressure-tests.md` method. CAT-10's "triggers reliably" is only observable by running it, and this repo makes measured claims or no claims.

### CI Enforcement

Phase 1 established that a prose-only claim which CI cannot check is the exact failure this project exists to prevent, and closed the class with a `--mutation-test` mode. Phase 2's new claims inherit that standard.

- **D-32:** **New violation codes assert PF ID-set equality across `NUMBERING.md`, `SKILL.md`, and `references/checklist.md`, and assert that `SKILL.md`'s stated rule count matches the registry.** The existing `undefined-id` check catches an ID cited in `skills/` that is not registered; it does not catch a registered ID missing from the checklist, nor a stated total that has drifted. The stated total is the anti-hallucination mechanism `.planning/research/ARCHITECTURE.md:155` relies on for spotting an out-of-range citation, so a wrong one is worse than none.
- **D-33:** **A frontmatter check asserts the Agent Skills key allow-list, `name` equal to the parent directory name, and a non-empty `description` within the chosen bound.** Stdlib parse, no dependency. `name`-vs-directory is the rule whose violation silently breaks distribution in every harness; an unknown key is the documented way a skill fails to load. `skills-ref` stays a useful local pre-release step, but a local step is not enforcement.
- **D-34:** **Every new code from D-32 and D-33 is registered in `MUTATIONS` and proven to fire.** A check that cannot fire is the defect Phase 1 spent three gap-closure plans closing; new checks do not get to reintroduce it.

### Claude's Discretion

- How `PF-1`'s seven Command of the Message sub-blocks are actually filled. Four slots each and a 30–35 rule total across six sections means some elements ship with one rule, and possibly one ships with none. The planner decides the distribution; leaving a sub-block empty is legitimate and is what the reserved ranges are for.
- The exact rule count inside the 30–35 band and the per-section split.
- The register's section heading wording. It becomes a stable interface for Phase 4's examples and Phase 5's linter, so pick once and record it in the plan.
- Exact keyword casing inside the D-14 bracket grammar (`GAP` / `REVIEW` / the `PF-3.3` retention form), and the parenthetical category vocabulary for `REVIEW` flags.
- Whether the new checks in D-32 and D-33 are one violation code or several, and their names.
- The trigger pressure-test file's name and location.
- Whether `SKILL.md`'s own prose is audited against its own modal rules — `.planning/research/PITFALLS.md:156` recommends applying the "should"/"may"/"might" audit to the skill's own rule text as a meta-rule. Recommended, not decided here.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project decisions and scope
- `.planning/PROJECT.md` — Core Value (persuasion that reads as marketing fails hardest), the three-framework split, the deletion-test rationale, the five constraints, and the Key Decisions table.
- `.planning/REQUIREMENTS.md` — CAT-01 to CAT-06, CAT-08 to CAT-10, INT-01 to INT-06, MOD-01, MOD-02 are this phase's. CAT-07 is Complete (Phase 1). MOD-03/04/05 are Phase 3 and must not be built here.
- `.planning/ROADMAP.md` — Phase 2's goal and its five success criteria; the Phase 2/Phase 3 boundary.
- `.planning/STATE.md` — standing blockers, including the unresolved MEDDIC-family trademark status that D-29 is decided against.
- `.planning/phases/01-foundations-legal-scaffolding-numbering-shared-deal/01-CONTEXT.md` — Phase 1's D-01 to D-17. D-01 (PF sections), D-03 (NUMBERING.md is authoritative), D-04 (deprecation never deletion), D-11 (generic filenames, marks in body only), D-14 (attribution pointer), D-15 (no placeholder files), D-16 (`skills/proof-first/`, name equals directory), D-17 (semver) all bind this phase.

### Frozen registries this phase writes into
- `NUMBERING.md` — the authoritative ID registry. Its PF reserved-range table, the `PF-1` sub-block table (the form D-05's new `PF-2` table must match), the Allocated IDs table this phase fills, the Deprecated IDs table, the range-exhaustion rule, and the next-free-ID procedure.
- `NOTICES.md` §Attribution pointer — the verbatim string `skills/proof-first/SKILL.md` must carry exactly once, and the "Files required to carry it" list naming it. Creating `SKILL.md` activates the `pointer-missing` check against it.
- `examples/deal-brief.md` — every fact any micro-example under D-02 may cite. Read `## Parties`, `## People and roles`, `## Pain points`, `## Inconvenient facts`, `## Customer source material`, and the 18-key `## Canonical figures` table. The inconvenient facts exist specifically to give INT-01 to INT-06 real material.
- `SOURCES.md` — the approved public sources every framework-derived concept must trace to, and what is out of bounds regardless of how readily a model reproduces it.

### The enforcement seam
- `tools/check_repo.py` — read the module docstring first; it lists all twelve current violation codes and their declared ceilings. `undefined-id` already scans `skills/`, `examples/`, and `README.md` for `PF-#.#` and `MC-#` tokens against the Allocated IDs table, which is what makes D-14's rule-numbered markers self-validating. `MUTATIONS` and `mutation_test()` are the contract D-34 extends.
- `.github/workflows/ci.yml` — the single job: self-test, then mutation-test, then live check.
- `README.md` §Repository layout — the documented target tree. D-25 fills three of its `(planned)` entries; the two Phase 3 reference files stay planned.

### Design research
- `.planning/research/ARCHITECTURE.md:128-137` — Pattern 1, progressive disclosure: the three-level loading model, the ~500-line / ~5,000-token ceiling behind CAT-08, and why a vague pointer gets skipped (D-28).
- `.planning/research/ARCHITECTURE.md:138-154` — Pattern 2, self-contained prose mechanics: restate only the subset instrumental to evidence-backed writing, not STE's full apparatus. Prose Mechanics must be the smallest section relative to its source scope. Carries a rule-shape example.
- `.planning/research/ARCHITECTURE.md:155-187` — Pattern 3, the numbering scheme and its anti-hallucination measures: the stated total, the cite-only-what-exists instruction, and `checklist.md`'s function (D-27, D-32).
- `.planning/research/ARCHITECTURE.md:188-203` — Pattern 4, why the mode axis is write vs. check, why strictness and artifact type were both rejected as modes, and why classification is a step rather than a mode (D-18).
- `.planning/research/ARCHITECTURE.md:307-332` — the four anti-patterns, including the verdict-only buzzword table and letting the linter imply the deletion test is mechanically verified.
- `.planning/research/PITFALLS.md:13-37` — Pitfall 1, the flatness risk. The project's central design risk and the one that cannot be patched later. Source of D-06, D-07, D-08.
- `.planning/research/PITFALLS.md:38-65` — Pitfall 2, the four classes the deletion test breaks on. Source of D-26 and the `references/deletion-test.md` edge-case table.
- `.planning/research/PITFALLS.md:156-184` — Pitfall 6, non-triggering, attention decay, soft modals, and hallucinated rule numbers. Source of D-28, D-29, D-31, and the meta-rule left to discretion.
- `.planning/research/PITFALLS.md:185-211` — Pitfall 7, the four presales hazards behind INT-03 to INT-06, and the recommendation that they be numbered rules rather than a footnote. Source of D-11, D-13, D-14.
- `.planning/research/STACK.md:1-60` — the Agent Skills frontmatter schema, the six documented keys, why `compatibility` is omitted, and the 200-vs-1024 description discrepancy D-30 resolves.

### Precedent
- `~/devoteam/.claude/plugins/marketplaces/simple-english/` — the sibling implementation, read directly. Inspect `SKILL.md`'s rule-catalog shape, its two-mode instruction, its self-check and Limits sections, and `references/checklist.md`'s anti-hallucination function. Structure and method only — copy none of its text.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `tools/check_repo.py` — 1,191 lines, stdlib only. Provides `strip_fences`, `split_sections`, `table_rows`, `parse_numbering`, and a per-code check/mutation registry pattern. D-32 and D-33's new codes extend this file rather than adding a second tool; `parse_numbering` already returns the allocated set, the deprecated set, and both range maps.
- `examples/deal-brief.md` — the complete fact set for every micro-example under D-02. Its `## Canonical figures` table is checker-enforced, so any figure a micro-example cites must already have a row.
- `NOTICES.md`'s fenced attribution-pointer block — the single source of truth for the string `SKILL.md` must carry.

### Established Patterns

- **Enforce every prose-only claim in CI, and prove the check fires.** Phase 1 shipped a check that was named as covered, ran in CI, and could not fire. The fix was `--mutation-test`: inject one named defect per violation code into a copy of the real repository and assert the code fires. D-34 continues it.
- **Declare every checker ceiling in its own docstring.** Each violation code states its real blind spots plainly. New codes inherit this.
- **Absence is not failure, only contradiction is.** The checker runs green on a repo missing the files it will eventually validate. Creating `SKILL.md` is what switches the pointer and ID checks on for it.
- **Deprecation, never deletion; ranges are hard ceilings.** An ID outside its section's reserved range is a build failure, not a judgement call.

### Integration Points

- Creating `skills/proof-first/SKILL.md` activates `pointer-missing` against it (it must carry the attribution string exactly once) and `undefined-id` against every `PF-#.#` token it contains. Authoring the catalog and registering its IDs in `NUMBERING.md` is one atomic job, not two — a plan that separates them ships a red build between commits.
- D-05 requires a new `PF-2` sub-block table in `NUMBERING.md`, and `check_range_id` must enforce it per sub-block, in the same form the existing MC per-dimension block enforcement takes (added in Phase 1's 01-06 plan).
- `references/checklist.md` becomes a third file holding PF IDs, which is what creates the drift D-32 closes.
- Phase 3 extends this phase's output shapes: a third report category (D-20), MC rows in `checklist.md` (D-27), and the formal classification behind D-18's assumed-family line.

</code_context>

<specifics>
## Specific Ideas

- The rule form settled on during discussion, as a shape to follow rather than final wording:

  ```
  ### PF-1.13 — Metrics

  Name the measure, its current baseline, and where the baseline came from.
  A metric with no baseline is a target, not a metric.

  **Replace with:** the customer's own stated figure, or an explicit gap
  marker if they have not measured it.

  ✗ "significantly faster settlement batches"
  ✓ "settlement batches complete inside the 6-hour window they currently
     overrun; Halverton has not measured the current overrun —
     [PF-2.11 GAP: baseline]"
  ```

- The trailing register's shape, with the Owner column removed per D-15:

  ```
  ## Unresolved before this document is sent

  | Marker | Rule    | What is needed                                   |
  |--------|---------|--------------------------------------------------|
  | GAP    | PF-2.11 | A measured baseline for the settlement overrun   |
  | REVIEW | PF-2.17 | Confirm the Type I framing is acceptable to send |
  ```

- Treat the D-14 bracket grammar as an API, not prose formatting — the same posture Phase 1 took toward the Canonical figures table. Phase 4's committed examples and Phase 5's linter both parse it.
- The two-marker case from D-11 needs a worked instance somewhere in this phase's own examples: a phrase carrying both `[PF-3.3: customer's term, retained]` and a `REVIEW` flag, proving provenance and integrity compose rather than conflict.
- `SKILL.md` states the total rule count and section count explicitly, so a citation outside a stated, checkable range is spottable. D-32 makes that statement enforced rather than decorative.
- The description under D-29/D-30 is the one field where keyword density matters more than prose quality — it is read by a ranker, not a person.

</specifics>

<deferred>
## Deferred Ideas

- **The `MC-` completeness audit and `references/completeness-audit.md`** — Phase 3 (AUD-01 to AUD-03). Phase 2 fills no `MC-` row; `NUMBERING.md`'s MC blocks stay empty.
- **`references/artifact-patterns.md` and the four artifact-family conventions** — Phase 3 (ART-01 to ART-04). D-18's assumed-family line names a family but applies no family-specific template, because none exists yet.
- **Three-category check output, formal artifact classification, and the citation guarantee** — Phase 3 (MOD-03, MOD-04, MOD-05). D-20 and D-18 are shaped so Phase 3 extends them rather than restructuring them.
- **A claude.ai upload path** — closed off by D-30's description length. Reopening it needs a shortened description, not a structural change. Not a stated DIST requirement.
- **Measuring trigger reliability at scale** — Phase 5. D-31 commits an observed pressure-test now; turning it into a repeatable measured number belongs with the eval harness.
- **The linter's buzzword proxy list** — Phase 5, and it must be sourced independently of this phase's worked examples or the benchmark becomes circular. Already a standing STATE.md blocker.
- **Auditing `SKILL.md`'s own prose against its own modal rules** — recommended by `PITFALLS.md:156` and left to the planner's discretion above. If it becomes a checker rule rather than an authoring practice, it is a new violation code and should be scoped deliberately.
- **`.planning/` framework marks in research-file headings** — Phase 6 LEG-04. Untouched by this phase.

</deferred>

---

*Phase: 2-Rule Catalog & Integrity — SKILL.md Core*
*Context gathered: 2026-09-11*
