# Phase 2: Rule Catalog & Integrity — SKILL.md Core - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-11
**Phase:** 2-Rule Catalog & Integrity — SKILL.md Core
**Areas discussed:** Rule shape & ID allocation, Persuasion preservation, Integrity refuse-vs-flag, File split & what ships now, Frontmatter description & triggers, Check-mode report format, Customer source material input contract, Write-mode output shape

Eight gray areas, 33 questions. Four were selected in the first round; the user chose to explore further and took all four remaining areas in a second round.

---

## Rule shape & ID allocation

**Q1 — How is CAT-02's subtractive/constructive pairing expressed?**

| Option | Description | Selected |
|--------|-------------|----------|
| One ID, mandatory Replace-with | Single numbered unit with a required constructive half; pairing cannot be half-read or half-cited. ~30 IDs. | ✓ |
| Two IDs per pair | Separate numbers, so deleted-but-not-replaced is its own citable violation. ~50-60 IDs against frozen ranges. | |
| Hybrid — pair only where the half stands alone | Separate IDs only where the constructive rule is independently citable. ~35-40 IDs. | |

**Notes:** The two-ID option was shown to collide with the frozen reserved ranges — `PF-3` has 10 slots and `PF-1` has 28 across seven elements, which pairing would not fit. The hybrid was rejected on the ground that "which shape does this new rule take" is a contributor judgement no check can enforce.

**Q2 — How verbose is a single rule entry, against CAT-08's ceiling?**

| Option | Description | Selected |
|--------|-------------|----------|
| Statement + Replace-with only | ~7 lines/rule; 40 rules ≈ 380 lines total. Comfortable headroom. | |
| Statement + Replace-with + one micro-example | ~14 lines/rule; forces a leaner rule count. Answers the attention-decay risk and seeds Phase 4's examples. | ✓ |
| Examples in a separate reference file | Terse SKILL.md, worked examples loaded on demand. Risks the pointer being skipped. | |

**Notes:** Selected knowing it puts the catalog over the ceiling at 30 rules, which the next question resolved.

**Q3 — How is the resulting ceiling pressure resolved?**

| Option | Description | Selected |
|--------|-------------|----------|
| Examples only where judgement is required | Micro-example on the deletion test, CotM element rules, integrity flags; bare statement on mechanical rules. ~30-35 rules. | ✓ |
| Lean catalog — fewer, denser rules | ~22-28 rules, all with examples. Some CotM sub-blocks ship with one rule or none. | |
| Full catalog, Prose Mechanics pushed to a reference | 35-45 rules, PF-4 moved out. Conflicts with CAT-06's self-containment. | |

**Notes:** The accepted cost is an authoring judgement per rule that no check can verify.

**Q4 — What does CAT-03's "exactly one opening instruction" mean structurally?**

| Option | Description | Selected |
|--------|-------------|----------|
| One rule, PF-0.1, 8 slots reserved | A single rule carries what a reframe is, must contain, and is disqualified by. | ✓ |
| One governing rule + numbered sub-conditions | PF-0.1 the instruction, PF-0.2/0.3 the disqualifiers. Citable per failure. | |
| One rule, disqualifiers inside its body as bullets | One citable ID; check mode quotes the failed bullet. | |

**Notes:** The sub-conditions option was rejected as reproducing the three-conflicting-rules problem success criterion 3 exists to prevent.

---

## Persuasion preservation

**Q1 — Where does persuasion live in the catalog?**

| Option | Description | Selected |
|--------|-------------|----------|
| Both — PF-1 structural, PF-5 protective | CotM spine carries the engine; PF-5 names devices the catalog must not strip. | ✓ |
| PF-1 spine only — persuasion is emergent | The mandatory Replace-with half is the whole mechanism. | |
| PF-5 protective rules only | Persuasion as its own concern, PF-1 purely structural. | |

**Notes:** The emergent-only option was weighed against PITFALLS Pitfall 1's named warning sign — a self-check that only subtracts — which nothing in that option structurally prevents.

**Q2 — What shape does the mandatory self-check take?**

| Option | Description | Selected |
|--------|-------------|----------|
| Two passes — subtract, then add | Pass 2 sweeps for contrast, metric with baseline, differentiator, reframe. Absences report as violations. | ✓ |
| One pass, additive rules as ordinary violations | Simpler, one mechanism. Absence competes with presence in one long list. | |
| Two passes plus a named flatness test | Adds an explicit "would an evaluator keep reading" question. | |

**Notes:** The flatness-test variant was declined as an unfalsifiable self-assessment.

**Q3 — How is confident voice reconciled with gap-marking and contractual exposure?**

| Option | Description | Selected |
|--------|-------------|----------|
| Confidence is licensed by adjacent evidence | Unhedged claim requires evidence in the same or next sentence; no evidence means delete and gap-mark. | ✓ |
| Hedge ban with a marked deliberate-uncertainty escape | Permits accurate uncertainty when explicitly marked. | |
| Absolute hedge ban | No hedges ever; uncertainty expressed only as a stated gap. | |

**Notes:** The escape-hatch option was flagged as something a model would over-use.

**Q4 — How are PF-5's protective rules written so check mode can act on them?**

| Option | Description | Selected |
|--------|-------------|----------|
| Presence requirements + checker prohibitions | Positive requirement plus a matching prohibition on check mode itself. Covers both failure directions. | ✓ |
| Presence requirements only | Reports absence; nothing stops a future rule or the linter flagging a rhetorical device. | |
| Checker prohibitions only | Purely defensive; never prompts a writer to add a contrast. | |

---

## Integrity: refuse vs flag

**Q1 — Does PF-2 get carved into sub-blocks?**

| Option | Description | Selected |
|--------|-------------|----------|
| Proof / Integrity sub-blocks | PF-2.1-2.10 and PF-2.11-2.20, recorded in NUMBERING.md like PF-1's table. | ✓ |
| Three sub-blocks | Proof, Refusals, Flags — matches the requirement structure but ~6 slots each. | |
| Leave PF-2 flat | No NUMBERING.md change; least structure on the highest-stakes section. | |

**Q2 — What does write mode emit for an unsupportable claim?**

| Option | Description | Selected |
|--------|-------------|----------|
| Write the true part, mark the gap in place | Draft stays usable, omission visible where it happened. | ✓ |
| Omit the claim and list it as a gap | Prose reads clean; omission only visible in the gap list. | |
| Refuse the sentence and say why | Strongest guarantee; leaves holes in the draft. | |

**Q3 — What does the marker vocabulary look like?**

| Option | Description | Selected |
|--------|-------------|----------|
| Rule-numbered markers, inline + trailing register | `[PF-2.11 GAP: ...]` / `[PF-2.17 REVIEW (compliance): ...]` plus a collected table. | ✓ |
| Rule-numbered markers, inline only | One representation, no drift; writer scans the whole document to find what is outstanding. | |
| Category markers without rule numbers | Plain `[EVIDENCE GAP: ...]`; readable but breaks the tie to numbered rules. | |

**Notes:** The decisive point surfaced during the comparison — `check_repo.py`'s existing `undefined-id` check already scans `skills/` and `examples/` for `PF-#.#` tokens, so rule-numbered markers in worked examples are validated with no new code.

**Q4 — What happens to the register's Owner column?**

| Option | Description | Selected |
|--------|-------------|----------|
| Drop it | Register carries marker, rule, and what is needed. | ✓ |
| Keep it, populated only from named people in the source material | Evidence-backed but usually empty in real use. | |
| Keep it blank for the writer to fill | Prompts assignment without asserting one. | |

**Notes:** Raised because the preview's own `Kestrel legal` / `Kestrel delivery` values were an invented org structure — the same failure class INT-01 exists to prevent, appearing inside the table meant to police it.

**Q5 — Is a surviving marker a violation in check mode?**

| Option | Description | Selected |
|--------|-------------|----------|
| Compliant, but reported as outstanding | Distinguishes "the writer did the right thing" from "ready to send". | ✓ |
| A violation until resolved | Unambiguous; gives the same answer whether the writer was honest or careless. | |
| Ignored entirely | Markers as write-mode scaffolding; lets one ship silently. | |

---

## File split & what ships now

**Q1 — Where do the deletion test's four edge classes land?**

| Option | Description | Selected |
|--------|-------------|----------|
| Rules in SKILL.md + edge-case table in the reference | PF-3.1/3.2/3.3 plus `references/deletion-test.md`. | ✓ |
| Rules only, all in SKILL.md | Nothing can be skipped; spends PF-3's 10 slots and the line budget. | |
| One rule plus an in-SKILL.md edge-case list | Compact; exceptions not citable by check mode. | |

**Q2 — Does Phase 2 create `references/checklist.md`?**

| Option | Description | Selected |
|--------|-------------|----------|
| Yes — PF rows now, MC rows in Phase 3 | Ships with the catalog it audits; gives check mode in-folder ground truth. | ✓ |
| No — SKILL.md's rule headings are the list | Avoids a sync burden for a list the model already sees. | |
| Defer to Phase 3 with MOD-05 | Build it when the requirement lands. | |

**Notes:** Decided on the observation that `NUMBERING.md` never ships to an installed user, so without this file the installed skill has no in-folder list of which IDs exist.

**Q3 — How is the reference pointer written?**

| Option | Description | Selected |
|--------|-------------|----------|
| Named trigger conditions per file | States the exact situation requiring the file to be opened. | ✓ |
| General "detail lives in references/" line | Cheapest; the documented skip failure. | |
| Mandatory read on every activation | Maximum reliability; defeats progressive disclosure. | |

**Q4 — Does Phase 2 close the three-file ID drift in CI?**

| Option | Description | Selected |
|--------|-------------|----------|
| Yes — ID-set equality + stated total, with mutation tests | New codes across NUMBERING.md, SKILL.md, checklist.md. | ✓ |
| Yes, minimal — ID-set equality only | Skips the stated-total check. | |
| No — undefined-id already covers the dangerous direction | Leaves an unenforced consistency claim. | |

---

## Frontmatter description & triggers

**Q1 — Do the framework marks appear in the description?**

| Option | Description | Selected |
|--------|-------------|----------|
| No marks — artifact types and user phrasings only | Consistent with Phase 1's D-11; keeps three contested marks out of every registry index. | ✓ |
| Marks included as trigger keywords | What PITFALLS Pitfall 6 recommends; nominative fair use. | |
| Descriptive substitutes, marks in body only | Triggers on what the frameworks do rather than their names. | |

**Notes:** Decided against the research's own recommendation. The reasoning that made Phase 1 keep marks out of filenames applies harder to a `description`, which is replicated into every registry, marketplace listing, and fork. Accepted cost recorded: a user invoking a framework by name may not fire the skill.

**Q2 — How long is the description?**

| Option | Description | Selected |
|--------|-------------|----------|
| Rich trigger list, front-loaded, ~400-600 chars | Room for every artifact type and phrasing. | ✓ |
| Stay under 200 chars | Portable everywhere including a future claude.ai upload. | |
| Rich in the skill, short in the plugin manifest | Two descriptions to keep coherent. | |

**Notes:** Framed against the fact that no DIST requirement covers claude.ai upload — the targets are the skills CLI, plugin marketplace, output style, and system prompt.

**Q3 — How is CAT-10's "triggers reliably" evidenced?**

| Option | Description | Selected |
|--------|-------------|----------|
| Recorded trigger pressure-test in the repo | Phrasings that must fire and near-misses that must not, with results, date, and harness. | ✓ |
| Defer measurement to Phase 5's eval harness | Ships CAT-10 as an unevidenced claim in the meantime. | |
| Phrasing list committed now, measured in Phase 5 | Design record now, measurement later. | |

**Q4 — Does check_repo.py enforce frontmatter validity?**

| Option | Description | Selected |
|--------|-------------|----------|
| Yes — allow-list, name==dirname, length bound | Same CI-enforced posture as every other Phase 1 claim. | ✓ |
| Yes, name==dirname only | The one rule whose violation silently breaks distribution. | |
| No — rely on skills-ref locally | A local pre-release step is not enforcement. | |

---

## Check-mode report format

**Q1 — Report unit, and are categories labelled now?**

| Option | Description | Selected |
|--------|-------------|----------|
| Blocks, grouped under two labelled categories now | Prose violations / Integrity flags; Phase 3 adds a third group and changes nothing else. | ✓ |
| Blocks, flat list, categories in Phase 3 | MOD-03 would then restructure a shipped format. | |
| Markdown table, one row per violation | Compact; squeezes the rewrite, which is the content that matters most. | |

**Q2 — In what order do findings appear?**

| Option | Description | Selected |
|--------|-------------|----------|
| Integrity first, then prose in document order | Triage and workflow in one ordering. | ✓ |
| Document order throughout | One rule; puts a competitor flag below a sentence-length nit. | |
| Rule-number order | Groups like with like; bounces the writer around the document. | |

**Q3 — What does a rewrite say when the fix needs unavailable evidence?**

| Option | Description | Selected |
|--------|-------------|----------|
| Rewrite carries the marker in place | One marker vocabulary across both modes; directly pasteable. | ✓ |
| State what evidence would make a rewrite possible | Partially answers MOD-02 with a refusal. | |
| Two rewrites — marked, and claim-deleted | Doubles the length of the longest findings. | |

**Q4 — Does check mode produce a corrected document?**

| Option | Description | Selected |
|--------|-------------|----------|
| Report only | Every change stays a decision made with the rule number in view. | ✓ |
| Report, plus a corrected document on request | Second output shape to specify. | |
| Report and corrected document together | Turns a teaching tool into an autocorrect. | |

---

## Customer source material input contract

**Q1 — How does the skill obtain the customer's own words?**

| Option | Description | Selected |
|--------|-------------|----------|
| Named optional input the skill asks for once | States what it can use, asks once, proceeds either way. | ✓ |
| Required for the RFP/RFI family, optional elsewhere | Family classification is Phase 3, so Phase 2 would have to assume it. | |
| Infer from whatever the writer pasted | Cannot distinguish the customer's words from the writer's draft. | |

**Q2 — What happens when none is supplied?**

| Option | Description | Selected |
|--------|-------------|----------|
| Announce once that the override is inactive | Writer learns why an expected term got deleted. | ✓ |
| Degrade silently | Cleanest output, no signal. | |
| Note it in the trailing register | Read after the draft rather than before. | |

**Q3 — How is a retained customer term marked?**

| Option | Description | Selected |
|--------|-------------|----------|
| First occurrence only, same bracket vocabulary | Noise bounded by distinct terms, not total uses. | ✓ |
| Register only, no inline marks | Prose entirely clean; nothing distinguishes a retained term at the point of reading. | |
| Every occurrence marked | Maximum explicitness; a marker every few sentences in an RFP answer. | |

**Q4 — Precedence when a term is customer-verbatim and an unmakeable compliance claim?**

| Option | Description | Selected |
|--------|-------------|----------|
| Both fire — retained and flagged | Retention is a vocabulary decision, the flag is a truth decision. | ✓ |
| Integrity wins — the term is not retained | Strips the RFP's own scoring vocabulary. | |
| Provenance wins — retained, flag suppressed | Reads as asserting a certification the vendor lacks. | |

---

## Write-mode output shape

**Q1 — Does write mode state the assumed artifact family?**

| Option | Description | Selected |
|--------|-------------|----------|
| State the assumed family in one line | Surfaces a correctable assumption; Phase 3 tightens it rather than introducing it. | ✓ |
| Family-agnostic — say nothing | Honest about what Phase 2 does; Phase 3 adds a visible new behaviour. | |
| Ask the writer which family | Friction for information Phase 2 cannot act on. | |

**Q2 — Does write mode report which rules it applied?**

| Option | Description | Selected |
|--------|-------------|----------|
| No trace — document plus register is the output | Write mode writes, check mode explains. | ✓ |
| Trailing note listing rule IDs applied | Approaches "all of them" on a full draft. | |
| Only rules that visibly changed the text | A judgement the skill makes about its own work. | |

**Q3 — What happens when the additive sweep finds an element genuinely unavailable?**

| Option | Description | Selected |
|--------|-------------|----------|
| Becomes a gap marker in place | One mechanism; makes the subtraction-only failure structurally impossible. | ✓ |
| Reported in the register only | A second mechanism for the same job. | |
| Silent in write mode, surfaced in check mode | The mandatory two-pass check would only run in one mode. | |

**Q4 — Does SKILL.md carry a Limits section?**

| Option | Description | Selected |
|--------|-------------|----------|
| Yes — cannot-verify plus out-of-scope, in one section | Both halves stated once, in one findable place. | ✓ |
| Yes, cannot-verify only | Omits the deck/pricing boundary the project drew deliberately. | |
| No — state each limit on the rule that owns it | Repeated across six rules; no single place to find it. | |

---

## Claude's Discretion

- How PF-1's seven Command of the Message sub-blocks are filled given four slots each and a 30-35 rule total — leaving a sub-block empty is legitimate.
- Exact rule count within the 30-35 band and the per-section distribution.
- The register's section heading wording, which becomes a stable interface for Phase 4 and Phase 5.
- Exact keyword casing inside the marker grammar, and the parenthetical category vocabulary for REVIEW flags.
- Whether the new checker codes are one violation code or several, and their names.
- The trigger pressure-test file's name and location.
- Whether SKILL.md's own prose is audited against its own modal rules — recommended by PITFALLS Pitfall 6, not decided.

## Deferred Ideas

- The `MC-` completeness audit and `references/completeness-audit.md` — Phase 3.
- `references/artifact-patterns.md` and the four artifact-family conventions — Phase 3.
- Three-category check output, formal artifact classification, and the citation guarantee (MOD-03/04/05) — Phase 3.
- A claude.ai upload path — closed off by the description-length decision; reopening needs a shortened description, not a structural change.
- Measuring trigger reliability at scale — Phase 5.
- The linter's buzzword proxy list, which must be sourced independently of this phase's examples — Phase 5.
- Auditing SKILL.md's own prose against its own modal rules as a checker rule rather than an authoring practice.
- `.planning/` framework marks in research-file headings — Phase 6 LEG-04.
