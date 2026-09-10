# Phase 2: Rule Catalog & Integrity — SKILL.md Core - Research

**Researched:** 2026-09-11
**Domain:** Authoring a numbered, self-contained Agent Skill rule catalog (Markdown + YAML frontmatter) with a stdlib-only Python CI checker extension. No new runtime code, no external services, no new packages.
**Confidence:** HIGH for repo-internal facts (numbering ranges, checker behavior, deal-brief facts — all read directly this session); HIGH for the Agent Skills frontmatter schema (carried from `.planning/research/STACK.md`, itself fetched directly from the live spec one day prior); MEDIUM for line/token-budget arithmetic (my own estimate, flagged `[ASSUMED]`); LOW/flagged-for-confirmation for anything touching the contested MEDDIC-family trademark status (out of this phase's scope but touches D-29's keyword-avoidance decision).

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CAT-01 | Numbered catalog sections follow the seven Command of the Message elements | `NUMBERING.md`'s frozen `PF-1` sub-block table (Before/After scenario, Required Capabilities, Metrics, Proof Points, Differentiators, Positive Business Outcomes) is the section spine — verified this session, quoted below |
| CAT-02 | Every subtractive rule paired with a constructive rule naming replacement evidence | D-01 locks this as one rule ID with a mandatory `Replace with:` half — see Architecture Patterns, Pattern 1 |
| CAT-03 | Exactly one opening rule resolving Before-scenario/Identify-Pain/Reframe | D-04 locks `PF-0.1` as the sole occupant of `PF-0`; see Pattern 2 |
| CAT-04 | Deletion test stated with evidence-attachment framing | D-26 locks the three-rule shape (`PF-3.1`–`PF-3.3`); see Pattern 3 |
| CAT-05 | Deletion test retains customer-verbatim terms | D-26 (`PF-3.3`), D-23/D-24 (when the override can and cannot fire); see Pattern 3 and Pitfall 2 |
| CAT-06 | Self-contained prose mechanics, no dependency on another skill | `PF-4` reserved range; ARCHITECTURE.md Pattern 2 (restate only the instrumental subset, not STE's full apparatus) |
| CAT-08 | SKILL.md under progressive-disclosure ceiling (<500 lines / ~5,000 tokens) | Line-budget arithmetic worked out below against the sibling skill's measured 329 lines / 3,664 words / 21,590 chars |
| CAT-09 | Frontmatter validates against the Agent Skills allow-list | Schema table in Standard Stack, sourced from `.planning/research/STACK.md` |
| CAT-10 | Description triggers reliably | D-29/D-30/D-31 lock the no-framework-marks, 400–600 char, pressure-test-recorded approach; see Pattern 6 |
| INT-01 | Refuse to invent metrics/references/benchmarks/certifications | D-10 (write mode marks the gap in place); `examples/deal-brief.md`'s Inconvenient facts give real refusal material |
| INT-02 | Mark an evidence gap for a human instead of filling it | D-12, D-14 (the `GAP` marker); see Pattern 4 |
| INT-03 | Flag commitment-shaped language | PITFALLS.md Pitfall 7 (the "will" contract-forming risk); part of the `PF-2.11`–`2.20` integrity sub-block |
| INT-04 | Flag undisclosed customer references | Pitfall 7; `PF-2.11`–`2.20` |
| INT-05 | Flag competitor comparisons | Pitfall 7 (Lanham Act exposure on specific competitor claims); `PF-2.11`–`2.20` |
| INT-06 | Flag compliance/certification/export claims | Pitfall 7; `examples/deal-brief.md`'s SOC 2 Type I/II gap is the ready-made worked instance |
| MOD-01 | Draft mode follows the catalog | D-18 (one-line assumed-family statement, prose, register, no rule trace) |
| MOD-02 | Check mode returns rule number, offending text, compliant rewrite | D-19, D-20, D-21, D-22 |

</phase_requirements>

## Summary

This phase has no new external dependency, no new runtime service, and no new package to vet — it is pure Markdown/YAML authoring (`skills/proof-first/SKILL.md` and two reference files) plus a stdlib-only Python extension to an already-shipped checker (`tools/check_repo.py`). The overwhelming majority of "what to build" is already decided in `02-CONTEXT.md`'s 34 numbered decisions; this research's job is to ground those decisions against the actual frozen registries (`NUMBERING.md`, `NOTICES.md`, `examples/deal-brief.md`), the actual checker code those decisions must extend, and the sibling skill's actual measured shape (not a description of it).

The single highest-leverage finding: **the progressive-disclosure ceiling (CAT-08) is genuinely tight, not a formality.** The sibling `simple-english/SKILL.md` — which needs no worked ✗/✓ examples because STE's catalog is purely mechanical — already measures 329 lines / 3,664 words / 21,590 characters (≈4,800–5,400 tokens depending on estimator) against the same ~500-line/~5,000-token ceiling. Proof First's D-02 decision requires a ✗/✓ micro-example on every judgment-carrying rule (the CotM element rules, the deletion test, the integrity flags) — plausibly 20+ of the 30–35 target rules — and each exampled rule, per the rule-shape already settled in discussion, runs ~13 lines versus ~5 for a mechanical rule with no example. The arithmetic (worked out under Architecture Patterns, Pattern 1) shows the catalog fits only if per-rule prose stays as compact as the settled shape shows and section/mode/register overhead is kept lean — this is not slack room, and the planner should budget a line-count checkpoint into the plan rather than discover the overrun after full drafting.

The second-highest-leverage finding: **`tools/check_repo.py` already does 90% of what D-32/D-33 need architecturally** — it has a working `parse_numbering`/`table_rows`/`split_sections` pattern for Markdown tables and a proven self-test + mutation-test harness (D-34's own bar). What it does not yet have is (a) any frontmatter/YAML parser (SKILL.md doesn't exist yet, so no code touches it), and (b) any check that reads SKILL.md's own rule-defining headings, not just PF-token citations. `undefined-id` already fires the moment `SKILL.md` exists and cites any `PF-#.#` — that part is free. The two genuinely new pieces of parsing this phase must write are: a minimal frontmatter key/value extractor (no PyYAML — six known keys, one of which is a block scalar and one a nested map), and a "rule-defining heading" extractor (`### PF-#.# — Title`) to compare against `NUMBERING.md`'s Allocated IDs and `references/checklist.md`'s own PF rows.

**Primary recommendation:** Draft the rule catalog and register its IDs in `NUMBERING.md` as one atomic unit (per Integration Points in `02-CONTEXT.md`), track a running line count against the ~470-line soft ceiling from the first drafted section onward (not just at the end), and write the two new `tools/check_repo.py` codes (frontmatter validity, PF-set/count equality) test-first against hand-built fixtures before pointing them at the real files — mirroring the exact self-test-then-mutation-test discipline Phase 1 already proved out.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Rule catalog content (persuasion spine, integrity, deletion test, mechanics) | Content Layer (`skills/proof-first/SKILL.md`) | Reference Layer (`references/*.md`) | The model reads SKILL.md at every activation; exhaustive/long-tail detail (deletion-test edge cases, the full PF checklist) is progressive-disclosure — loaded only on demand, per the Agent Skills three-level model |
| Marker vocabulary (`GAP`/`REVIEW`/retention markers) and the trailing register | Content Layer (inline in generated output, defined in SKILL.md) | — | This is prose the model emits, not a service; it lives entirely in the SKILL.md instruction text, never a separate runtime component |
| ID registry and range enforcement | Enforcement Layer (`NUMBERING.md` + `tools/check_repo.py`) | Content Layer (SKILL.md cites, never defines, the ranges) | `NUMBERING.md` is the single source of truth per Phase 1's D-03; SKILL.md and `references/checklist.md` are downstream consumers that must never drift from it — that drift is exactly what D-32's new checks close |
| Frontmatter validity (name/description/allow-list) | Enforcement Layer (`tools/check_repo.py`, new frontmatter parser) | Distribution Layer (the harnesses that read frontmatter at install/trigger time) | A malformed key or a `name`≠directory mismatch fails silently in a harness at install time, not at authoring time — CI is the only place this is provably caught before a user ever sees it |
| Attribution/legal posture | Legal Layer (`NOTICES.md`, checked by `pointer-missing`/`framework-statement-missing`) | Content Layer (SKILL.md is a new carrier once created) | Creating `skills/proof-first/SKILL.md` activates an existing check (`pointer-missing`) against an existing registry (`NOTICES.md`) — no new enforcement code needed here, only a new file satisfying an existing contract |

## User Constraints (from CONTEXT.md)

<user_constraints>

### Locked Decisions

**Catalog Shape and Rule Form**

- **D-01:** One ID per rule, with a mandatory `Replace with:` half. CAT-02's subtractive/constructive pairing is expressed inside a single numbered unit, not as two IDs. A rule cannot be authored without its constructive half, so the pairing cannot be half-read by a model or half-cited by check mode. One citation covers both directions of the fix. — Reversibility: one-way — splitting a rule into two IDs later renumbers nothing but changes what every published citation resolves to; merging two into one strands the retired ID under D-04 of Phase 1's deprecation-never-deletion rule.
- **D-02:** A micro-example appears only on rules where judgement is required. The deletion test, the Command of the Message element rules, and the integrity flags each carry one short ✗/✓ pair drawn from `examples/deal-brief.md`. Mechanical rules — sentence length, active voice, modal discipline — carry statement and `Replace with:` only. Uniform examples put the catalog over CAT-08's ceiling; no examples leaves the judgement rules to be applied inconsistently. — Reversibility: costly — adding or removing examples later rewrites every affected rule body and re-runs the line budget.
- **D-03:** Target 30–35 rules in v1, with the frozen reserved ranges deliberately under-filled. The research proposed 35–45 (`.planning/research/ARCHITECTURE.md:136`); D-02's example cost brings the workable number down. Under-filling is the intended use of the reserved ranges — a v1.1 rule takes the next free number in its section without disturbing a citation.
- **D-04:** `PF-0` holds exactly one rule, `PF-0.1`, with its remaining 8 slots reserved. CAT-03 and success criterion 3 require exactly one opening instruction resolved from the three frameworks' overlapping reframe concepts. "Exactly one" means one ID: `PF-0.1` carries what a reframe is, what it must contain, and what disqualifies it. Numbered sub-conditions in `PF-0` would reproduce the three-conflicting-rules problem the requirement exists to prevent. — Reversibility: one-way — same citation-stability contract as Phase 1's D-01.
- **D-05:** `PF-2` is carved into named sub-blocks: `PF-2.1`–`PF-2.10` Proof, `PF-2.11`–`PF-2.20` Integrity. Recorded in `NUMBERING.md` as a sub-block table in the same form as the existing `PF-1` table. Proof rules (attach evidence, name the source) and integrity rules (refuse, flag) are different jobs, and a rule added later to Integrity must not land next to a Proof rule. — Reversibility: one-way — the sub-block boundary is enforced by `tools/check_repo.py`'s `range-id` check once written, and moving it reassigns which rules are in range.

**Persuasion Preservation**

- **D-06:** `PF-1` carries the structural persuasion engine; `PF-5` carries explicit protective rules. The Command of the Message spine — Before/After contrast, named metrics, differentiators — is the mechanism by which specificity substitutes for adjectives (`.planning/research/PITFALLS.md:13`). `PF-5` adds a small ruleset naming devices the catalog must not strip: contrast structures, second-person address to the buyer's stated priorities, and confident unhedged claims when evidenced.
- **D-07:** Every `PF-5` protective rule states a presence requirement and a matching prohibition on check mode itself. Positive half: the document contains at least one explicit before/after contrast. Negative half: check mode never flags second-person address, a confident evidenced claim, or a contrast structure as a violation. "Do not flatten" is not a testable predicate; these two halves are. Covers both failure directions — a document that lost its rhetoric, and a checker that strips it.
- **D-08:** The self-check runs two passes: subtract, then add. Pass 1 finds violations to remove. Pass 2 is a mandatory additive sweep asking whether a contrast, a metric with a baseline, a differentiator, and a reframe are present. Missing ones are reported exactly as removals are. This makes `PITFALLS.md`'s named warning sign — a self-check that only ever finds things to delete — structurally impossible rather than discouraged.
- **D-09:** Confidence is licensed by adjacent evidence, never by hedging. An unhedged claim requires its evidence in the same or the next sentence. No evidence means delete and mark the gap. Hedging is never the repair for missing evidence. One rule reconciles the voice concern (models default to hedged prose), the fabrication concern (INT-01/02), and the contractual-exposure concern (`PITFALLS.md:185`).

**Integrity: Refusals and Flags**

- **D-10:** Write mode emits the true part and marks the gap where the claim would go. Asked to write about a SOC 2 Type II report Kestrel does not hold, the sentence ships with the unverifiable claim replaced by an explicit marker. Nothing false is emitted, and nothing silently disappears — the omission is visible in place, not only in a list the reader may not reach.
- **D-11:** Provenance never suppresses an integrity rule — both fire. A term that is customer-verbatim *and* an unmakeable compliance claim is retained under `PF-3.3` for compliance-matrix alignment *and* carries a `REVIEW` flag. Retention is a vocabulary decision; the flag is a truth decision. The catalog states this precedence explicitly rather than leaving it to be discovered. A worked example must show two markers on one phrase.
- **D-12:** An absence found by the additive sweep produces a gap marker like any missing evidence. A missing differentiator is as visible as an invented metric, through the same mechanism. A thin-input draft comes back heavily marked, which is the correct signal.
- **D-13:** `SKILL.md` carries a Limits section covering both cannot-verify and out-of-scope. It states that the skill flags but cannot verify disclosure authorization, certification status, competitor-claim accuracy, or legal exposure; and that it does not produce slide decks, pricing, sizing, or commercial modelling, per PROJECT.md's Out of Scope. A clean check report is not legal clearance, and the skill says so.

**Marker Vocabulary**

This is the phase's hardest interface. Phase 4's worked examples show it, Phase 5's linter counts it, and Phase 3's check output groups it.

- **D-14:** Three marker types share one bracket grammar, and every marker carries the rule number that raised it.
  - `[PF-2.11 GAP: no measured baseline for the overrun — Halverton has never instrumented it]`
  - `[PF-2.17 REVIEW (compliance): the RFP requires Type II; Kestrel's Type II observation window closes after submission]`
  - `[PF-3.3: customer's term, retained — RFP Q3]`

  Carrying the rule number is what makes `PITFALLS.md:185`'s recommendation real — check mode can cite an integrity flag exactly as it cites a prose violation. It also means `tools/check_repo.py`'s existing `undefined-id` check, which already scans `skills/` and `examples/` for `PF-#.#` tokens against `NUMBERING.md`'s Allocated IDs table, validates every marker in a worked example with no new code. — Reversibility: one-way — Phase 4's committed examples and Phase 5's committed generations and linter both bind to this grammar; changing it invalidates published artifacts and recorded benchmark data.
- **D-15:** Output carries a trailing register listing every marker, with no Owner column. The register is what a bid manager works from; the inline copy is what stops a marker being missed. It carries marker type, rule, and what is needed. It does **not** name an owner — the skill cannot know a customer's or a vendor's internal org, and inventing one in the very table meant to police fabrication is the failure INT-01 exists to prevent.
- **D-16:** A retained customer term is marked on its first occurrence only. An RFP answer mirroring the question's vocabulary would otherwise carry a marker every few sentences. Noise is bounded by the count of distinct retained terms, not by total uses.
- **D-17:** A marker still present when check mode runs is compliant, and reported as outstanding. Its presence means the rule was honoured — nothing was fabricated — so it is not a prose violation. It still surfaces in the register so it cannot ship unresolved. This distinguishes "the writer did the right thing" from "the document is ready to send", which a pass/fail verdict cannot.

**Modes: Write and Check**

- **D-18:** Write mode output is: one line stating the assumed artifact family, the prose, then the register. No rule trace. The assumed-family line surfaces a correctable assumption and puts the sentence MOD-04 will formalise in Phase 3 in place now, so Phase 3 tightens an existing behaviour rather than introducing a new one. No list of applied rules — write mode writes, check mode explains, and the register already carries everything the writer must act on.
- **D-19:** Check mode returns a report only, never a corrected document. Every change stays a decision the writer makes with the rule number in front of them. A corrected document is the artifact a rushed writer would use, which would turn a teaching tool into an autocorrect and undercut the citations MOD-02 exists to deliver.
- **D-20:** The report is blocks — rule ID, quoted offending text, compliant rewrite — grouped under two labelled categories now: "Prose violations" and "Integrity flags". Phase 3's MOD-03 adds "Completeness gaps" as a third group and changes nothing else. Shipping a flat list in Phase 2 would force MOD-03 to restructure an output format Phase 4's examples were already authored against.
- **D-21:** Ordering is integrity first, then prose in document order. Findings that can cost a deal or create legal exposure are read first; within prose, document order lets the writer work top to bottom through their own document. `PITFALLS.md:156`'s attention-decay concern applies to a long report as much as to a long skill.
- **D-22:** A rewrite that needs unavailable evidence carries the marker in place. The proposed rewrite is itself compliant prose containing `[PF-2.11 GAP: ...]`. One marker vocabulary across both modes, and the rewrite is directly pasteable. MOD-02 gets a real rewrite rather than a refusal.

**Customer Source Material and Provenance**

- **D-23:** Customer source material is a named optional input the skill asks for once. At the start of a drafting task the skill states what it can use — RFP question text, discovery notes, stated requirements — and asks for it. It proceeds either way. `PF-3.3` fires only against material actually supplied; inferring provenance from whatever the writer pasted would let the vendor's own buzzwords launder themselves as customer terms, which is exactly what `PF-3.2`'s per-token test exists to stop.
- **D-24:** When no source material is supplied, the skill announces once that the override is inactive. One line stating that `PF-3.3` cannot fire and terms will be judged by the deletion test alone. A writer whose RFP vocabulary gets stripped needs to know that supplying the RFP text would have prevented it.

**File Layout and Progressive Disclosure**

- **D-25:** Phase 2 ships `SKILL.md`, `references/deletion-test.md`, and `references/checklist.md` — and nothing else in the skill folder. `references/completeness-audit.md` and `references/artifact-patterns.md` are Phase 3's, and are not pre-created; Phase 1's D-15 established that empty placeholder files age badly, and `NOTICES.md`'s pointer check already skips a listed path that does not yet exist.
- **D-26:** The deletion test is three rules plus a reference table. `PF-3.1` the test itself, `PF-3.2` per-token application so a real technical noun cannot launder a decorative modifier riding on it, `PF-3.3` the provenance override for customer-verbatim terms (CAT-05). `references/deletion-test.md` carries the expanded edge-case table for the four classes `.planning/research/PITFALLS.md:38` names — connotation-only terms, customer-first terms, RFP-mandated wording, half-empty compounds. Documenting them is required: an undocumented exception looks like an inconsistently applied rule.
- **D-27:** `references/checklist.md` ships in Phase 2 with the `PF` rows; Phase 3 adds `MC` rows. `NUMBERING.md` never ships to an installed user (Phase 1's D-16), so without this file the installed skill has no in-folder list of which IDs exist, and nothing distinguishes a number the model read from a number it recalled — the failure `.planning/research/PITFALLS.md:156` documents. This is the mechanism MOD-05 will rely on in Phase 3.
- **D-28:** Every reference pointer states the named condition that requires opening the file. "Before applying `PF-3.1` to a compound term, or to any term appearing in the customer's own source material, read `references/deletion-test.md`." "Before emitting any rule citation in check mode, read `references/checklist.md`." A condition a model can match against, not an invitation it will decline — progressive disclosure only works if the pointer is specific (`.planning/research/ARCHITECTURE.md:128`).

**Frontmatter and Triggering**

- **D-29:** No framework marks appear in the frontmatter `description`. It triggers on artifact types and the phrasings a writer actually uses: RFP response, RFI, solution proposal, executive summary, demo script, discovery, presales, bid. `.planning/research/PITFALLS.md:156` recommends naming the frameworks as trigger keywords; Phase 1's D-11 established the opposite instinct for filenames because they get scraped and indexed, and a `description` is replicated harder than a filename — it lands in every registry, every marketplace listing, and every fork. Accepted cost: a user who says "check this against MEDDICC" may not fire the skill. — Reversibility: costly — a published description propagates into registry indexes and forks that do not re-fetch.
- **D-30:** The description is a front-loaded trigger list of roughly 400–600 characters. No target harness enforces 200 — the four DIST requirements name the skills CLI, the plugin marketplace, an output style, and a paste-able system prompt, not claude.ai upload. Highest-value keywords come first in case any harness truncates. Accepted cost: this closes off a claude.ai upload path without an edit, and `.planning/research/STACK.md` flags 200 as the safe figure there.
- **D-31:** A trigger pressure-test is recorded in the repo. A committed file listing natural phrasings that must fire the skill and near-miss phrasings that must not, with observed results, the date, and the harness they were run on — mirroring the sibling project's `pressure-tests.md` method. CAT-10's "triggers reliably" is only observable by running it, and this repo makes measured claims or no claims.

**CI Enforcement**

Phase 1 established that a prose-only claim which CI cannot check is the exact failure this project exists to prevent, and closed the class with a `--mutation-test` mode. Phase 2's new claims inherit that standard.

- **D-32:** New violation codes assert PF ID-set equality across `NUMBERING.md`, `SKILL.md`, and `references/checklist.md`, and assert that `SKILL.md`'s stated rule count matches the registry. The existing `undefined-id` check catches an ID cited in `skills/` that is not registered; it does not catch a registered ID missing from the checklist, nor a stated total that has drifted. The stated total is the anti-hallucination mechanism `.planning/research/ARCHITECTURE.md:155` relies on for spotting an out-of-range citation, so a wrong one is worse than none.
- **D-33:** A frontmatter check asserts the Agent Skills key allow-list, `name` equal to the parent directory name, and a non-empty `description` within the chosen bound. Stdlib parse, no dependency. `name`-vs-directory is the rule whose violation silently breaks distribution in every harness; an unknown key is the documented way a skill fails to load. `skills-ref` stays a useful local pre-release step, but a local step is not enforcement.
- **D-34:** Every new code from D-32 and D-33 is registered in `MUTATIONS` and proven to fire. A check that cannot fire is the defect Phase 1 spent three gap-closure plans closing; new checks do not get to reintroduce it.

### Claude's Discretion

- How `PF-1`'s seven Command of the Message sub-blocks are actually filled. Four slots each and a 30–35 rule total across six sections means some elements ship with one rule, and possibly one ships with none. The planner decides the distribution; leaving a sub-block empty is legitimate and is what the reserved ranges are for.
- The exact rule count inside the 30–35 band and the per-section split.
- The register's section heading wording. It becomes a stable interface for Phase 4's examples and Phase 5's linter, so pick once and record it in the plan.
- Exact keyword casing inside the D-14 bracket grammar (`GAP` / `REVIEW` / the `PF-3.3` retention form), and the parenthetical category vocabulary for `REVIEW` flags.
- Whether the new checks in D-32 and D-33 are one violation code or several, and their names.
- The trigger pressure-test file's name and location.
- Whether `SKILL.md`'s own prose is audited against its own modal rules — `.planning/research/PITFALLS.md:156` recommends applying the "should"/"may"/"might" audit to the skill's own rule text as a meta-rule. Recommended, not decided here.

### Deferred Ideas (OUT OF SCOPE)

- The `MC-` completeness audit and `references/completeness-audit.md` — Phase 3 (AUD-01 to AUD-03). Phase 2 fills no `MC-` row; `NUMBERING.md`'s MC blocks stay empty.
- `references/artifact-patterns.md` and the four artifact-family conventions — Phase 3 (ART-01 to ART-04). D-18's assumed-family line names a family but applies no family-specific template, because none exists yet.
- Three-category check output, formal artifact classification, and the citation guarantee — Phase 3 (MOD-03, MOD-04, MOD-05). D-20 and D-18 are shaped so Phase 3 extends them rather than restructuring them.
- A claude.ai upload path — closed off by D-30's description length. Reopening it needs a shortened description, not a structural change. Not a stated DIST requirement.
- Measuring trigger reliability at scale — Phase 5. D-31 commits an observed pressure-test now; turning it into a repeatable measured number belongs with the eval harness.
- The linter's buzzword proxy list — Phase 5, and it must be sourced independently of this phase's worked examples or the benchmark becomes circular. Already a standing STATE.md blocker.
- Auditing `SKILL.md`'s own prose against its own modal rules — recommended by `PITFALLS.md:156` and left to the planner's discretion above. If it becomes a checker rule rather than an authoring practice, it is a new violation code and should be scoped deliberately.
- `.planning/` framework marks in research-file headings — Phase 6 LEG-04. Untouched by this phase.

</user_constraints>

## Project Constraints (from CLAUDE.md)

`./.claude/CLAUDE.md` carries repo-wide directives that bind this phase's plan and execution, not just its content:

- **GSD workflow enforcement is mandatory.** File-changing tool calls (`Edit`, `Write`, etc.) must happen through a GSD command (`/gsd-execute-phase` for this planned phase work), not as direct ad-hoc edits.
- **No emojis** in written content unless explicitly requested — the ✗/✓ micro-example marks are not emojis and are exempt, but no other decorative unicode should appear in SKILL.md prose.
- Project stack guidance (`STACK.md`, embedded in CLAUDE.md verbatim) reconfirms: zero dependencies for the skill itself, stdlib-only Python for `tools/check_repo.py`, no `compatibility` frontmatter key, no spaCy/NLP dependency anywhere, no maintained buzzword blocklist as the mechanism (the deletion test is the mechanism; a list is only ever an eval-harness proxy, out of scope for this phase).
- `.claude/CLAUDE.md`'s embedded PROJECT.md excerpt states the constraints already carried into `02-CONTEXT.md`'s decisions (legal, dependencies, compatibility, evidence, voice) — no new constraint beyond what CONTEXT.md already encodes.

## Standard Stack

### Core

| Component | Version/Spec | Purpose | Why Standard |
|---|---|---|---|
| Agent Skills frontmatter schema | Current spec, no version number published (`agentskills.io/specification`) | `skills/proof-first/SKILL.md`'s YAML frontmatter (`name`, `description`, `license`, `metadata`) | The only cross-harness format this project targets; verified against the live spec in the prior research session `[CITED: .planning/research/STACK.md]` |
| Python 3 standard library only (`re`, `argparse`, `pathlib`, `shutil`, `tempfile`) | 3.13.13 confirmed present on this machine `[VERIFIED: python3 --version, run this session]` | Extending `tools/check_repo.py` with D-32/D-33's new checks | Matches the existing file's own stated posture (`"It imports only the Python standard library"` — `tools/check_repo.py:8-9`, read this session) and the project's zero-dependency constraint |
| git | 2.54.0 confirmed present `[VERIFIED: git --version, run this session]` | Commit, mutation-test fixture copying (uses `shutil`, not git, for scratch copies — no git dependency in the checker itself) | Standard |

### Frontmatter field allow-list (verbatim from prior-session spec fetch)

| Field | Required | Constraints |
|---|---|---|
| `name` | Yes | 1–64 chars, lowercase unicode alphanumerics and hyphens only, no leading/trailing hyphen, no `--`, **must match the parent directory name** |
| `description` | Yes | 1–1024 chars, non-empty, must describe what+when |
| `license` | No | License name or pointer to bundled license file |
| `compatibility` | No | 1–500 chars free text — **D-29/STACK.md both recommend omitting this entirely** |
| `metadata` | No | Free-form string→string map; version/standard info goes here (mirrors the sibling skill's `metadata: {version: "1.3.0", standard: ...}`) |
| `allowed-tools` | No | Space-separated string, marked experimental — not needed for a pure writing skill |

`[CITED: .planning/research/STACK.md, itself sourced from https://agentskills.io/specification]` — Any key outside this six-item list is a hard validation failure in the spec, not a soft warning. This is exactly what D-33's new frontmatter check must enforce.

### Supporting

No supporting libraries are needed. This phase adds no new package to any ecosystem.

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Hand-rolled minimal frontmatter parser (regex-based, six known keys) | PyYAML | PyYAML is a real dependency for a "zero dependencies" repo whose own STACK.md explicitly rejects adding *any* package-manager dependency for the eval harness on far weaker grounds (spaCy, textstat) than "parse six known top-level keys." Not worth it — see Don't Hand-Roll below for the narrower point this doesn't contradict. |
| `skills-ref validate` as CI enforcement | `tools/check_repo.py`'s own frontmatter check | `skills-ref` is a real, useful **local, pre-release** conformance tool (D-33 says so explicitly) but is an external Node/JS tool, not something this repo's CI can depend on without contradicting the stdlib-only CI posture. Use it as a human pre-release step, not a CI gate. |

**Installation:** None. No `npm install`, no `pip install` for this phase's deliverables.

## Package Legitimacy Audit

**N/A — this phase installs no external packages in any ecosystem.** `tools/check_repo.py` remains stdlib-only Python per the project's existing constraint and this phase's own D-33 ("Stdlib parse, no dependency"). No `npm view`/`pip index versions`/`cargo search` check applies. If a future phase proposes `skills-ref`, `textstat`, or any other package, that phase's research must run the Package Legitimacy Gate — this one does not need it.

## Architecture Patterns

### System Architecture Diagram

```
                    WRITER'S REQUEST
                          │
                          ▼
        ┌─────────────────────────────────────┐
        │  Frontmatter (name+description)      │  ← loaded at EVERY harness
        │  read by harness at skill-selection   │    turn, ~100 tokens
        │  time (not by the model's task logic) │
        └──────────────┬────────────────────────┘
                        │ (skill triggers)
                        ▼
        ┌─────────────────────────────────────┐
        │  SKILL.md body loads in full          │  ← CAT-08 ceiling:
        │  (mode selection: write vs check)     │    <500 lines/~5k tokens
        └───────┬─────────────────┬─────────────┘
                │                 │
     WRITE MODE │                 │ CHECK MODE
                ▼                 ▼
   ┌─────────────────────┐   ┌──────────────────────────┐
   │ 1. Ask once for      │   │ 1. Read existing text     │
   │    customer source   │   │ 2. Apply catalog:         │
   │    material (D-23)   │   │    subtract pass (D-08.1) │
   │ 2. Apply catalog:     │   │    additive sweep (D-08.2)│
   │    PF-0 reframe,      │   │    deletion test per-token│
   │    PF-1 CotM spine,   │   │    (references/           │
   │    PF-3 deletion test │   │     deletion-test.md,     │
   │    (per-token +       │   │     opened on the named   │
   │     provenance        │   │     condition of D-28)    │
   │     override),        │   └───────────┬───────────────┘
   │    PF-4 mechanics,    │               │
   │    PF-5 protective    │               ▼
   │    rules              │   ┌──────────────────────────┐
   │ 3. Refuse/mark         │  │ 3. Emit report, NOT a      │
   │    fabrication         │  │    rewritten document      │
   │    (PF-2 Integrity,    │  │    (D-19): blocks grouped  │
   │    D-10, D-12)         │  │    "Integrity flags" then  │
   └──────────┬─────────────┘   │    "Prose violations"      │
              │                │    (D-20/D-21), each rule  │
              ▼                │    number checked against  │
   ┌─────────────────────┐    │    references/checklist.md │
   │ 4. Output: one-line  │    │    (D-28's named condition)│
   │    assumed-family     │    └──────────────────────────┘
   │    statement, prose   │
   │    with inline        │
   │    [PF-#.# GAP/REVIEW/│
   │    retention] markers │
   │    (D-14), trailing   │
   │    register (D-15,    │
   │    no Owner column)   │
   └──────────────────────┘

              (both modes)
                        │
                        ▼
        ┌─────────────────────────────────────┐
        │  CI ENFORCEMENT (tools/check_repo.py) │
        │  undefined-id: scans skills/,          │
        │    examples/, README.md for PF-#.#     │
        │    tokens against NUMBERING.md          │
        │    — fires automatically once           │
        │    SKILL.md exists, no new code (D-14)  │
        │  NEW (D-32): PF ID-set equality across  │
        │    NUMBERING.md / SKILL.md / checklist  │
        │    .md; stated-count-vs-registry check  │
        │  NEW (D-33): frontmatter allow-list,     │
        │    name==dirname, description bound      │
        │  D-34: every new code proven live via    │
        │    --mutation-test                       │
        └─────────────────────────────────────┘
```

### Recommended Project Structure

```
skills/
└── proof-first/
    ├── SKILL.md                      # NEW this phase — catalog spine, two modes, self-check
    └── references/
        ├── deletion-test.md          # NEW this phase — D-26's edge-case table
        └── checklist.md              # NEW this phase — PF rows only (D-27); MC rows are Phase 3
                                       # (completeness-audit.md, artifact-patterns.md NOT created — D-25)
NUMBERING.md                          # EXTENDED — PF-2 sub-block table (D-05), Allocated IDs filled
tools/
└── check_repo.py                     # EXTENDED — new frontmatter parser, new PF-set/count checks
```

`[VERIFIED: README.md:47-76, read this session]` — the target tree documented there already names exactly this layout with `(planned)` markers; this phase converts three of those planned entries to real files and leaves the two Phase 3 entries (`completeness-audit.md`, `artifact-patterns.md`) untouched, per D-25.

### Pattern 1: The Line-Budget Arithmetic Behind CAT-08

**What:** SKILL.md's body is loaded in full on every activation; the Agent Skills spec sets a ~5,000-token/under-500-line ceiling `[CITED: .planning/research/STACK.md, sourced from agentskills.io/specification]`. This phase's D-02 decision (examples only on judgment-carrying rules) is the load-bearing lever that keeps the catalog under this ceiling — but the arithmetic needs to be checked explicitly, not assumed.

**Measured baseline:** `simple-english/SKILL.md` — no per-rule ✗/✓ examples at all (its worked examples are shared across whole sections, not per-rule) — measures 329 lines, 3,664 words, 21,590 characters for 53 mechanical rules across 9 table-formatted sections `[VERIFIED: wc -l -w -c run this session against the sibling skill's SKILL.md]`. At roughly 1.3 tokens/word this is ≈4,760 tokens — already close to the ceiling with a *lighter* per-rule format (table rows, not individual headed blocks) and *no* worked examples at all.

**Proof First's rule shape is heavier per rule.** The settled shape (from `02-CONTEXT.md`'s Specific Ideas, reproduced verbatim above) runs:
- **A rule WITH a ✗/✓ example** (heading, statement lines, `Replace with:` line, blank-separated ✗ line, ✓ line(s)) ≈ 12–14 lines.
- **A rule WITHOUT an example** (heading, statement, `Replace with:` line) ≈ 5–6 lines.

**Worked arithmetic `[ASSUMED — my own estimate, not verified against a drafted catalog]`:** For a 30–35 rule catalog where D-02 restricts examples to CotM element rules (`PF-1`), the deletion test (`PF-3`), and the integrity flags (a subset of `PF-2.11`–`2.20`) — plausibly 18–24 of the 30–35 rules — versus mechanical rules with no example (`PF-4`, likely some of `PF-2.1`–`2.10` Proof, `PF-0`, `PF-5` depending on planner discretion):

| Scenario | Rules w/ example | Rules w/o example | Rule-body lines | + fixed overhead* | Total |
|---|---|---|---|---|---|
| Lean (22 rules total) | 14 × 13 = 182 | 8 × 5 = 40 | 222 | ~150 | **~372** |
| Target-mid (32 rules) | 19 × 13 = 247 | 13 × 5 = 65 | 312 | ~150 | **~462** |
| Target-high (35 rules, example-heavy) | 24 × 13 = 312 | 11 × 5 = 55 | 367 | ~150 | **~517 (over ceiling)** |

*Fixed overhead ≈ frontmatter (18–22 lines) + intro/task framing/two-mode table (35–50 lines) + section headers × 6 (12–18 lines) + self-check description (D-08's two passes, 15–20 lines) + Limits section (D-13, 10–15 lines) + reference-file pointers (D-28, 6–10 lines) + Marker-vocabulary explanation (D-14/D-15, 15–20 lines).

**Conclusion:** The target-high end of D-03's 30–35 band, combined with a generous reading of "judgment-carrying," genuinely risks exceeding the ceiling. This is not a formality to check once at the end — the planner should either (a) bias the per-section rule count toward the low end of 30–35, (b) keep exampled-rule bodies tighter than the 13-line reference shape where the ✗/✓ pair can be shortened, or (c) budget an explicit mid-draft line-count checkpoint (after `PF-0`+`PF-1`+`PF-2` are drafted, before `PF-3`–`PF-5`) so an overrun is caught with sections still left to trim, not after the whole catalog is written.

**When to use:** Any time the plan proposes a specific per-section rule count, run this arithmetic against it before locking the count.

### Pattern 2: `PF-0` — The Single Resolved Opening Rule

**What:** `NUMBERING.md`'s frozen table reserves `PF-0.1`–`PF-0.9` for "Opening / Reframe" `[VERIFIED: NUMBERING.md:19, quoted: "| PF-0 | PF-0.1-PF-0.9 | Opening / Reframe | 0 | PF-0.1 |"]`. D-04 locks exactly one rule filling this range: `PF-0.1`.

**When to use:** This is the resolution point for three overlapping source concepts (Before-scenario, Identify-Pain, Reframe) named in CAT-03 — the rule must state what a reframe *is*, what it must *contain*, and what *disqualifies* it, as one indivisible instruction, not three numbered sub-conditions (which D-04 explicitly names as reproducing the exact three-conflicting-rules problem the requirement exists to prevent).

**Note on framework attribution:** Per `NOTICES.md`'s Paraphrase boundary language for Challenger `[VERIFIED: NOTICES.md:83-94, read this session]`, this rule must restate the reframe *concept* in the project's own words — no reproduced training-deck structure or phrasing — and per D-29, the rule text itself (unlike the frontmatter `description`) may still reference the general concept in plain English without needing to avoid the word "reframe," since D-29 only constrains the frontmatter field, not the rule catalog's own prose.

### Pattern 3: The Deletion Test as Three Rules Plus a Reference Table

**What:** D-26 locks this shape: `PF-3.1` (the test itself: delete the term, ask if technical meaning survives), `PF-3.2` (per-token application — a decorative modifier riding on a real technical noun does not get laundered by testing the whole phrase as one unit), `PF-3.3` (the provenance override — a term appearing verbatim in customer source material is retained and marked, not deleted).

**When to use:** `PF-3.2`'s per-token requirement directly closes PITFALLS.md's Pitfall 2 finding that "the deletion test as stated operates term-by-term... [but] compound terms where one half is real and one is air... don't get caught by a whole-term deletion check unless the rule explicitly requires testing each token independently" `[CITED: .planning/research/PITFALLS.md:45]`. `PF-3.3` directly closes the same pitfall's customer-anchored-term and RFP-mandated-wording failure classes.

**Worked instance required (D-11):** at least one example in this phase's own worked material must show a phrase carrying *both* a `[PF-3.3: ...]` retention marker *and* a `REVIEW` flag on the same phrase — proving retention (a vocabulary decision) and the integrity flag (a truth decision) compose rather than conflict. `examples/deal-brief.md`'s customer source material gives ready-made raw material for this: the discovery quote `"We need a landing zone we can actually govern"` `[VERIFIED: examples/deal-brief.md:70, quoted verbatim]` supplies a real customer-verbatim term ("landing zone") that could co-occur with an unverifiable claim about governance maturity, giving the two-marker worked example real facts to draw from rather than invented ones.

**Reference file scope (D-26):** `references/deletion-test.md` must document the four edge-case classes PITFALLS.md names — connotation-only terms, customer-first terms, RFP-mandated wording, half-empty compounds — as a *worked-pairs table* (sentence-with-term → sentence-with-term-deleted → verdict-and-why), never a verdict-only banned/allowed list. This is `ARCHITECTURE.md`'s Anti-Pattern 1 (`.planning/research/ARCHITECTURE.md:309-313`) applied directly: "Keep the deletion test as the rule... make `references/deletion-test.md` teach the mechanism through worked pairs... so a model applies the test to a term it has never seen before, not just to terms on a list."

### Pattern 4: The Marker Vocabulary as an API Contract

**What:** D-14's three marker forms (`GAP`, `REVIEW (category)`, retention) share one bracket grammar and always carry the raising rule number. Per `02-CONTEXT.md`'s Specifics section, this must be "treated as an API, not prose formatting" — Phase 4's committed examples and Phase 5's linter both parse it downstream.

**Why this matters for this phase specifically:** because every marker embeds a `PF-#.#` token, the existing `undefined-id` check `[VERIFIED: tools/check_repo.py:237-261, function check_undefined_id]` already validates every marker the moment SKILL.md and its examples exist — no new code is needed for marker validation itself, only for the two genuinely new concerns (frontmatter, PF-set/count equality). The planner should note this as a "free win" rather than scope new checker work for marker-token validity.

**One risk not covered by any existing or planned check:** the *figures* embedded inside a marker's free-text explanation (e.g., a dollar amount or date drawn from `examples/deal-brief.md`, if a worked marker cites one) are only checked by `unlisted-figure` when they appear under `examples/**/*.md` `[VERIFIED: tools/check_repo.py:323-330, "def check_unlisted_figure... examples_root = repo_root / 'examples'"]` — **not** when they appear inside `skills/proof-first/SKILL.md` itself. If this phase's worked ✗/✓ examples inside SKILL.md cite a canonical figure (as the discussion's own sample rule form does — "the 6-hour window they currently overrun"), that figure is not checker-enforced against `examples/deal-brief.md`'s Canonical figures table the way a figure inside `examples/` would be. This is flagged under Open Questions below — it is not a decided requirement (D-32/D-33 don't mention it) and the planner should decide explicitly whether to extend `unlisted-figure`'s scan roots or accept the gap for this phase.

### Pattern 5: Extending `tools/check_repo.py` for D-32/D-33 — Reusing the Existing Parse Pattern

**What already exists and should be reused, not reinvented** `[VERIFIED: tools/check_repo.py, read in full this session]`:
- `split_sections(text)` (lines 113-130) splits a Markdown doc into `{heading: body}` by `## ` headings — directly reusable for `references/checklist.md`'s own sectioning.
- `table_rows(section_text)` (lines 133-145) extracts data rows from the first Markdown table in a section, skipping header/separator rows — directly reusable for reading `checklist.md`'s PF-row table once D-27 defines its shape.
- `parse_numbering(path)` (lines 152-191) already returns `pf_ranges`, `mc_ranges`, `allocated` (list of `{id, title, defined_in, added_in}`), and `deprecated` — this is the existing source of "what IDs does `NUMBERING.md` say exist."
- The check/mutation-registration pattern: every violation code is a `(code, description, mutate_fn)` tuple in `MUTATIONS`, and `ALL_CHECK_CODES` is the union of all category-code-lists — D-34's "every new code proven to fire" bar plugs into this exact list with no new harness needed.

**What is genuinely new and must be written:**

1. **A minimal frontmatter parser** (D-33). No YAML library exists in stdlib and none should be added. Frontmatter is delimited by `---` lines at file start; for the six known keys, a targeted parser is sufficient:
   - Split on the first two `^---$` lines to isolate the frontmatter block.
   - For each of the six allowed keys, match `^key:` at column 0. `description` may use a block scalar (`description: |` followed by indented lines) — the existing `_write`/`split_sections` style of line-by-line scanning (not full YAML semantics) is the right level of complexity, matching this file's own established "just enough parsing" philosophy (see `parse_notices`'s handling of a fenced block, lines 398-420, as the closest existing precedent for "extract a specific known shape without a general-purpose parser").
   - A key at column 0 that is *not* one of the six allowed names is the `unknown-frontmatter-key` (or similarly named) violation.
   - `name` value compared against `path.parent.name` (i.e., `skills/proof-first/` → `proof-first`) for the name-vs-directory check.
   - `description` value's length checked against whatever bound the plan settles on (D-30 says ~400–600 chars target, not a hard CI-enforced ceiling — the planner should decide whether CI enforces a hard bound or only a non-empty check, since D-33 only commits to "a non-empty description within the chosen bound").

2. **A PF ID-set/count equality check** (D-32). Requires a second new extractor: rule-defining headings inside `SKILL.md` itself, distinct from rule *citations* (which `undefined-id` already catches anywhere in `skills/`). A regex like `^### (PF-\d+\.\d+)` (assuming the settled rule-shape's `### PF-1.13 — Metrics` heading form, per the Specific Ideas sample) extracts the IDs SKILL.md actually *defines*. Compare three sets: (a) `NUMBERING.md`'s Allocated IDs, (b) SKILL.md's defined-heading IDs, (c) `references/checklist.md`'s listed PF rows (via `table_rows` once its shape is settled). All three must be set-equal; a mismatch in either direction is a new violation. Separately, a stated-count assertion (e.g., a regex matching a sentence pattern the plan settles on, such as "N rules across M sections") compared against `len(allocated PF ids)`.

3. **Self-test fixtures and mutations for both**, following the existing `_bad_*()`/`_good_*()` fixture pattern (e.g., `_bad_numbering()`/`_good_numbering()` at lines 803-855) and the existing `_mutate_*()` function pattern (e.g., `_mutate_dup_id` at lines 621-626) — inject one named defect into a throwaway copy, assert the new code fires, register it in `MUTATIONS`.

**When to use:** This ordering — parser first (proven against hand-built fixtures via `--self-test`), then wired into `run_all_checks`, then a mutation registered and proven via `--mutation-test` — is the exact sequence Phase 1's own gap-closure plans (`01-05`, `01-06`, `01-07`) used to close the "check that cannot fire" defect class. Reusing that sequence is lower-risk than inventing a new verification approach for this phase's new codes.

### Pattern 6: The Description Field as a Trigger List, Not a Summary

**What:** D-29/D-30 lock a ~400–600 character, front-loaded, keyword-dense `description` naming artifact types and phrasings ("RFP response," "RFI," "solution proposal," "executive summary," "demo script," "discovery," "presales," "bid") with zero framework-name keywords.

**Why this specific tradeoff is sound, not just stated:** `[CITED: .planning/research/PITFALLS.md:169]` documents the standard failure mode — "a description written as a summary... rather than a trigger" — and separately (Pitfall 3) documents that the MEDDIC-family mark has a *documented history of enforcement against community content* (posts, videos, book listings) `[CITED: .planning/research/PITFALLS.md:71]`. D-29's choice to omit framework names from the one field that "lands in every registry, every marketplace listing, and every fork" is a defensible, though costly, precaution — it trades a real triggering benefit (a user who says "check this against MEDDICC" may not fire the skill) against a real, if diffuse, legal/replication-surface risk. This tradeoff is explicitly logged as `costly`/`one-way` in `02-CONTEXT.md` and should not be revisited mid-plan without a fresh discussion round.

**Pressure-test method (D-31):** mirror the sibling project's `pressure-tests.md` file shape — natural phrasings that must fire, near-miss phrasings that must not, observed result, date, harness. `[VERIFIED: no such file exists yet in this repo; the sibling's is at ~/devoteam/.claude/plugins/marketplaces/simple-english/evals/pressure-tests.md per the ARCHITECTURE.md system diagram, not independently re-read this session — treat the sibling's exact format as [ASSUMED] until the plan opens and reads it directly]`.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Full YAML parsing for SKILL.md frontmatter | A general-purpose YAML parser or a `pip install pyyaml` | A targeted six-key extractor (Pattern 5 above) | Only six keys are ever legal; a general parser is unneeded surface area and (if pip-installed) a real dependency this repo's own constraints reject |
| A maintained "banned buzzwords" list as the deletion test's actual mechanism | A verdict-only banned/allowed table in SKILL.md or `references/deletion-test.md` | The deletion test itself (delete-and-ask) plus worked *pairs* teaching the mechanism | `ARCHITECTURE.md` Anti-Pattern 1 and this project's own PROJECT.md already reject this explicitly; a static list is stale on arrival and gets the noun/modifier boundary wrong in both directions |
| A second numbering scheme or ad-hoc citation format for integrity flags | Inventing a distinct bracket grammar for `GAP`/`REVIEW` separate from how prose-rule citations work | D-14's single bracket grammar, reusing the existing `PF-#.#` token pattern `undefined-id` already validates | One grammar means one validation path (already built) and one thing for Phase 4/5 to parse, instead of two |
| A hand-rolled Markdown table reader for `checklist.md` | A bespoke parser distinct from what already exists | `table_rows()`/`split_sections()`, already proven against `NUMBERING.md` and `examples/deal-brief.md` | These functions already handle header/separator-row skipping and section-boundary detection correctly; a second implementation risks a second, differently-buggy edge case |

**Key insight:** Every "don't hand-roll" item above resolves to "reuse what `tools/check_repo.py` already proved out in Phase 1" or "reuse what the deletion-test's own design (a mechanism, not a list) already settled" — this phase adds no genuinely new *kind* of tooling, only new *instances* of an already-validated pattern.

## Common Pitfalls

### Pitfall 1: The catalog reads as compliance prose, not persuasive prose

**What goes wrong:** A subtractive, checkable, deletion-tested rule catalog — applied uncritically — produces correct, evidenced, dead prose. `[CITED: .planning/research/PITFALLS.md:13-35]` names this the project's central, unpatchable-later design risk.
**Why it happens:** Controlled-language rule catalogs are built for comprehension, not for persuading a skeptical, time-pressured evaluator; the two objectives pull in opposite directions unless rules explicitly preserve rhetorical structure.
**How to avoid:** D-06/D-07/D-08/D-09 are this phase's direct, already-decided countermeasures — `PF-5`'s protective rules, the mandatory two-pass self-check (subtract then add), and evidence-licensed (never hedge-licensed) confidence. The plan must actually author `PF-5` and the additive sweep, not treat them as optional polish — D-08 states this explicitly makes the failure "structurally impossible rather than discouraged," which only holds if the additive pass is actually written into the self-check instructions.
**Warning signs:** A drafted rule catalog where every worked example is a deletion with no accompanying replacement instruction; a self-check section that only lists things to remove.

### Pitfall 2: The deletion test breaks silently on connotation, customer-anchored terms, RFP wording, and half-empty compounds

**What goes wrong:** A term whose value comes from something other than denotation (customer's own vocabulary, an RFP's scored question wording, a decorative modifier riding a real noun) gets deleted by a naive whole-term test. `[CITED: .planning/research/PITFALLS.md:38-65]`
**Why it happens:** The deletion test only has access to the sentence in front of it, not the customer's document or the evaluator's rubric — provenance is external information the sentence-only test cannot see without an explicit override.
**How to avoid:** Already resolved by D-26 (`PF-3.2` per-token, `PF-3.3` provenance override) and D-23/D-24 (source material is asked for once, provenance only fires against material actually supplied). The plan must make sure `references/deletion-test.md`'s edge-case table actually covers the four named classes as worked pairs, not summary prose.
**Warning signs:** A worked RFP-response example that strips the RFP's own vocabulary from its topic sentence; a per-token test collapsed back into a whole-phrase test in the actual rule wording.

### Pitfall 3: Non-triggering, hallucinated rule numbers, and attention decay on a longer catalog than the sibling skill's

**What goes wrong:** Description-field non-triggering, later-section attention decay on a long SKILL.md, and confidently-cited rule numbers that don't exist. `[CITED: .planning/research/PITFALLS.md:156-183]`
**Why it happens:** These are documented, measured properties of how current harnesses select skills and how models process long instruction contexts — not implementation bugs.
**How to avoid:** D-29/D-30/D-31 (description as trigger list, pressure-tested) directly address non-triggering. `references/checklist.md` (D-27) and the stated-count/checkable-range mechanism (D-32) directly address hallucinated numbers — but only if SKILL.md actually states its total rule count in a form the new checker can parse (see Pattern 5's item 2). The Common Pitfalls section of the sibling's own SKILL.md models the "cite only rule numbers that exist in this file... invented rule numbers are a known failure" instruction verbatim `[VERIFIED: simple-english SKILL.md:36, quoted: "Cite only rule numbers that exist in this file. Do not cite rule numbers from memory."]` — Proof First's SKILL.md should carry an equivalent instruction extended to cover both write mode (marker rule numbers) and check mode (citation rule numbers).
**Warning signs:** No recorded baseline (no-skill) test showing what a fresh session invents when asked to cite "the Command of the Message elements" or "the MEDDICC criteria" from memory — Pitfall 6 in `PITFALLS.md` recommends running this baseline once per framework before the skill ships, though that pressure-test itself may be a Phase 4/5 concern rather than this phase's — flagged as an Open Question below.

### Pitfall 4: Domain-specific presales legal hazards treated as an afterthought

**What goes wrong:** Commitment-shaped "will" language becoming a contractual warranty, undisclosed customer references, unverified competitor comparisons (Lanham Act exposure), and unverified compliance/export claims. `[CITED: .planning/research/PITFALLS.md:185-208]`
**Why it happens:** The skill's own central mechanism — replace vague adjectives with specific, evidenced claims — is exactly what turns a soft, deniable statement into a hard, checkable, and potentially legally consequential one.
**How to avoid:** INT-03 through INT-06 require these as four distinct, numbered rules inside `PF-2.11`–`2.20`, each citable exactly like a prose violation (already the shape D-14/D-20/D-21 establish). `examples/deal-brief.md`'s Inconvenient facts section gives ready-made real material for each: the unmeasured settlement-batch overrun (INT-01/02 — no fabricated baseline), the SOC 2 Type I/Type II gap (INT-06 — compliance claim), Priya Raghunathan's stated incumbent preference (a fact the skill must not silently omit or spin), and the examination-window-vs-comparable-duration mismatch (a commitment-shaped date risk, INT-03) `[VERIFIED: examples/deal-brief.md:43-50, read this session, facts quoted in Pattern 3 above and in this session's earlier read]`.
**Warning signs:** A worked example that resolves the SOC 2 gap by simply omitting it rather than surfacing an explicit `REVIEW (compliance)` marker; an Integrity section whose language only discusses fabrication and never authorization/disclosure.

## Code Examples

### Rule shape (settled during discussion, not final wording — reproduced from `02-CONTEXT.md`'s Specifics)

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

`[VERIFIED: 02-CONTEXT.md:177-190, reproduced verbatim as the "shape to follow rather than final wording"]` — note this example cites the "6-hour window" figure, which matches `examples/deal-brief.md`'s Canonical figures row `settlement-batch-window-hours | 6 | count` `[VERIFIED: examples/deal-brief.md:120, quoted: "| settlement-batch-window-hours | 6 | count | Hours the nightly settlement batch job is required to complete within |"]` — any worked rule example the plan drafts must cite figures this way, from an existing Canonical figures row, never an invented number.

### Trailing register shape (settled during discussion)

```
## Unresolved before this document is sent

| Marker | Rule    | What is needed                                   |
|--------|---------|--------------------------------------------------|
| GAP    | PF-2.11 | A measured baseline for the settlement overrun   |
| REVIEW | PF-2.17 | Confirm the Type I framing is acceptable to send |
```

`[VERIFIED: 02-CONTEXT.md:194-201, reproduced verbatim]` — no Owner column, per D-15.

### `NUMBERING.md`'s existing `PF-1` sub-block table (the form D-05's new `PF-2` table must match)

```
| Element | Range |
|---|---|
| Before scenario | PF-1.1-PF-1.4 |
| After scenario | PF-1.5-PF-1.8 |
| Required Capabilities | PF-1.9-PF-1.12 |
| Metrics | PF-1.13-PF-1.16 |
| Proof Points | PF-1.17-PF-1.20 |
| Differentiators | PF-1.21-PF-1.24 |
| Positive Business Outcomes | PF-1.25-PF-1.28 |
```

`[VERIFIED: NUMBERING.md:32-40, quoted verbatim this session]` — D-05's new `PF-2` sub-block table (Proof `PF-2.1`–`2.10`, Integrity `PF-2.11`–`2.20`) must be added to `NUMBERING.md` in this exact two-column `| Element | Range |` shape, immediately following the existing `## PF-1 sub-blocks` section, to match the precedent `check_range_id`'s per-section (and, per D-05, per-sub-block) enforcement expects.

### Existing checker pattern to extend (frontmatter + PF-set/count checks plug in here)

```python
# tools/check_repo.py:557, existing aggregation point
ALL_CHECK_CODES = ID_CHECK_CODES + FIGURE_CHECK_CODES + NOTICES_CHECK_CODES + LICENSE_CHECK_CODES + FRAMEWORK_CHECK_CODES
# New D-32/D-33 codes join this list, e.g.:
# ALL_CHECK_CODES = ID_CHECK_CODES + FIGURE_CHECK_CODES + NOTICES_CHECK_CODES + LICENSE_CHECK_CODES + FRAMEWORK_CHECK_CODES + FRONTMATTER_CHECK_CODES + CATALOG_CONSISTENCY_CHECK_CODES

# tools/check_repo.py:564-571, existing aggregation function
def run_all_checks(repo_root):
    violations = []
    violations += run_id_checks(repo_root)
    violations += run_figure_checks(repo_root)
    violations += run_notices_checks(repo_root)
    violations += run_license_checks(repo_root)
    violations += run_framework_checks(repo_root)
    # NEW: violations += run_frontmatter_checks(repo_root)
    # NEW: violations += run_catalog_consistency_checks(repo_root)
    return violations
```

`[VERIFIED: tools/check_repo.py:557,564-571, quoted verbatim this session]` — the new `run_frontmatter_checks`/`run_catalog_consistency_checks` functions (naming per planner discretion, D-32/D-33) should follow the exact `run_*_checks(repo_root) -> list[(subject, message)]` contract every existing check function already uses, so they compose into `run_all_checks` and `main()`'s existing sort/print/exit logic with zero changes to the aggregation or CLI layer.

## State of the Art

| Old Approach (this project's own Phase 1 research proposal) | Current Approach (this phase's locked decision) | When Changed | Impact |
|---|---|---|---|
| `PF-1.20` ceiling, ~8-10 CotM rules `[CITED: .planning/research/ARCHITECTURE.md:166,172]` | `PF-1.28` ceiling, 4 slots per each of 7 CotM elements | Phase 1's 01-01 plan (already executed, per STATE.md) | This phase inherits `PF-1.28`, not the research's `PF-1.20` figure — the planner must use the frozen `NUMBERING.md` ranges, not re-derive from ARCHITECTURE.md |
| 35–45 total rule target `[CITED: .planning/research/ARCHITECTURE.md:136]` | 30–35 total rule target (D-03) | This phase's context-gathering session | D-02's per-rule example cost is the stated reason for the narrower band — see Pattern 1's arithmetic for why this matters concretely, not just as a number |
| MEDDICC as a fourth reference file alongside deletion-test/artifact-patterns/checklist (research's original recommendation) | Unchanged for Phase 2's scope — `completeness-audit.md` explicitly deferred to Phase 3 (D-25) | Roadmap phase-boundary decision, prior to this phase | Confirms this phase should not pre-create or stub that file |

**Deprecated/outdated for this phase's purposes:** ARCHITECTURE.md's `PF-1.20` figure and its 35-45 rule estimate are both superseded by frozen Phase 1 decisions and this phase's own D-03 — treat the research file's numbers as historical context only, never as the authoritative range. `NUMBERING.md` is the authoritative range in all cases, per Phase 1's own D-03 (numbering is authoritative).

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The line-budget arithmetic in Pattern 1 (per-rule line costs of ~13/~5 lines, fixed overhead of ~150 lines) | Architecture Patterns, Pattern 1 | If actual drafted prose runs longer per rule than estimated, the catalog could exceed CAT-08's ceiling without a mid-draft checkpoint catching it — mitigated by the recommended checkpoint, not eliminated by this estimate alone |
| A2 | 18–24 of the 30–35 rules will carry a ✗/✓ example under a plausible reading of D-02's "judgment-carrying" scope | Architecture Patterns, Pattern 1 | The actual split is explicit Claude's Discretion per `02-CONTEXT.md` — if the planner scopes fewer example-bearing rules, the budget is more comfortable than shown; if more (e.g., `PF-5` and `PF-0` also get examples), it is tighter |
| A3 | `PF-3.3`'s retention marker and a `REVIEW` flag can co-occur on the discovery quote "landing zone" specifically | Architecture Patterns, Pattern 3 | This is one candidate for D-11's required two-marker worked instance, not a locked choice — the plan may find a cleaner pairing elsewhere in `examples/deal-brief.md`'s material; flagged so the planner doesn't treat this specific pairing as decided |
| A4 | The sibling skill's `evals/pressure-tests.md` file shape is the right model for D-31's trigger pressure-test | Architecture Patterns, Pattern 6 | Not independently re-read this session (only referenced via prior ARCHITECTURE.md research) — the plan should open and read that file directly before committing to its exact format |
| A5 | A regex of the form `^### (PF-\d+\.\d+)` reliably extracts every rule-defining heading in a drafted SKILL.md for D-32's new check | Architecture Patterns, Pattern 5 | If the plan settles on a different heading level or format (e.g., `## PF-1.13` instead of `### PF-1.13 — Title`) the extractor regex must be adjusted accordingly — this is a design choice the plan makes, not yet fixed |

## Open Questions

1. **Does `unlisted-figure` need to scan `skills/` in addition to `examples/`?**
   - What we know: worked ✗/✓ examples inside SKILL.md will likely cite Canonical figures (per the settled rule shape's own sample, which cites the 6-hour window). `unlisted-figure` currently only scans `examples/**/*.md` `[VERIFIED: tools/check_repo.py:323-330]`.
   - What's unclear: whether this is an intentional scope boundary (SKILL.md examples are illustrative prose, not the same "every fact must trace to a row" contract `examples/` carries) or an oversight neither D-32 nor D-33 anticipated.
   - Recommendation: the planner should make an explicit call and record it — either extend `unlisted-figure`'s scan roots to include `skills/`, or explicitly note in the plan why SKILL.md's worked examples are exempt from this particular check (e.g., because `undefined-id` already covers the ID-token half of the same worked example, and the figure itself is illustrative rather than asserted-as-fact).

2. **What exact sentence pattern will SKILL.md use to state its total rule count, for D-32's stated-count check to regex against?**
   - What we know: D-32 requires the assertion to exist; ARCHITECTURE.md recommends a form like "N rules across M numbered sections."
   - What's unclear: the exact wording is Claude's Discretion, not yet fixed, and the new checker code needs a stable pattern to match.
   - Recommendation: settle the exact sentence template in the plan itself (not just "state the count somewhere"), and write the checker regex against that literal template — this mirrors how `pointer-missing` requires a byte-exact string, not a fuzzy match.

3. **Should `references/checklist.md`'s PF-row table share a header schema with `NUMBERING.md`'s Allocated IDs table, or use a narrower schema (ID + one-line description only)?**
   - What we know: D-27 requires PF rows in Phase 2, MC rows deferred to Phase 3; the file must let a model "search... for every number that is allowed to exist" per ARCHITECTURE.md Pattern 3.
   - What's unclear: whether it needs `Defined in`/`Added in` columns (mirroring `NUMBERING.md`) or just `ID | Title` for a leaner, faster-to-scan file.
   - Recommendation: keep it minimal (ID + short title, possibly + one-line summary) since its job is fast lookup/anti-hallucination, not full registry duplication — `NUMBERING.md` already owns the authoritative record (Phase 1's D-03) and never ships to an installed user, so `checklist.md` is a *derived*, lean view, not a second copy of the same table.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3 | Extending `tools/check_repo.py` | ✓ | 3.13.13 `[VERIFIED: python3 --version, run this session]` | — |
| git | Committing plan output, phase workflow | ✓ | 2.54.0 `[VERIFIED: git --version, run this session]` | — |
| Node.js / `npx skills-ref` | Optional local pre-release conformance check (not CI) | Not checked this session — not required for this phase's CI, which stays stdlib-only per D-33 | — | Skip entirely for this phase; `skills-ref` is explicitly a human pre-release step per D-33, not a build requirement |

**Missing dependencies with no fallback:** None — this phase requires nothing beyond what is already present.

**Missing dependencies with fallback:** `skills-ref` (Node-based conformance validator) is not verified present and is not needed for this phase to complete; it is an optional local step a human contributor may run before release, not a CI or planning dependency.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | `tools/check_repo.py`'s own `--self-test` / `--mutation-test` harness (no pytest/jest — this repo has no traditional test framework, by design, per STACK.md's "Repo hygiene" section: "What SimpleEnglish does *not* have... a test framework beyond the linter's own self-test") |
| Config file | none — `tools/check_repo.py` is both the checker and its own test runner |
| Quick run command | `python3 tools/check_repo.py --self-test` |
| Full suite command | `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py` (self-test, then mutation-test, then the live check — matching `.github/workflows/ci.yml`'s existing job order per the module docstring's own description) |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CAT-09 | Frontmatter validates against allow-list, `name`==dirname, non-empty description | unit (new fixture) | `python3 tools/check_repo.py --self-test` (after D-33's new fixtures are added) | ❌ Wave 0 — new fixtures + new check functions needed |
| CAT-08 | SKILL.md under progressive-disclosure ceiling | manual/scripted count | `wc -l skills/proof-first/SKILL.md` (no existing automated check enforces the line ceiling — flagged below) | ❌ — no line-count CI check exists or is required by any D-3x decision; this is a manual authoring discipline, not a CI gate, unless the plan adds one |
| CAT-01–CAT-06, INT-01–06, MOD-01/02 | Rule catalog content correctness | manual (this is prose-authoring correctness, not mechanically testable — the deletion test itself is a semantic judgment per SOURCES.md's own admission) | UAT / conversational verification against the phase's five success criteria, not a script | N/A — content quality is not unit-testable |
| D-05 | `PF-2` sub-block range enforcement, per-sub-block not aggregate | unit (extends existing `check_range_id`) | `python3 tools/check_repo.py --self-test` | ⚠️ Partially exists — `check_range_id` already handles `pf_ranges` per-section; D-05's *sub-block* (not just section) enforcement is new and needs a fixture proving a rule numbered inside `PF-2` but outside its Proof/Integrity sub-block fires |
| D-32 | PF ID-set equality + stated-count match | unit (new) | `python3 tools/check_repo.py --self-test` then `--mutation-test` | ❌ Wave 0 — new parser + new check functions + new fixtures + new mutation |
| D-33 | Frontmatter allow-list, name==dirname, description bound | unit (new) | same as above | ❌ Wave 0 — new parser + new check functions + new fixtures + new mutation |
| D-34 | Every new code proven live | mutation | `python3 tools/check_repo.py --mutation-test` | ❌ Wave 0 — new `MUTATIONS` entries for every new code from D-32/D-33 |

### Sampling Rate

- **Per task commit:** `python3 tools/check_repo.py --self-test`
- **Per wave merge:** `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py`
- **Phase gate:** Full suite green before `/gsd-verify-work`, exactly as Phase 1 already established as CI's job order.

### Wave 0 Gaps

- [ ] Frontmatter parser + `run_frontmatter_checks` + fixtures (`_bad_frontmatter()`/`_good_frontmatter()`) + one mutation per new frontmatter code — covers D-33
- [ ] PF-set/count-equality parser (rule-defining-heading extractor + checklist-row extractor) + `run_catalog_consistency_checks` + fixtures + mutations — covers D-32
- [ ] `PF-2` sub-block enforcement fixture extending `check_range_id`'s existing per-section logic to per-sub-block — covers D-05's enforcement half (the table itself is a `NUMBERING.md` content edit, not a code change)
- [ ] No automated line-count gate exists for CAT-08 — if the plan wants CI to enforce the ~500-line ceiling rather than relying on authoring discipline, that is a new, undecided check not currently scoped by any D-3x decision; otherwise, treat as a plan-level manual checkpoint (see Pattern 1's recommendation)

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | No authentication surface — this phase produces static Markdown content and a local CI script with no network/auth boundary |
| V3 Session Management | No | Not applicable — no session state anywhere in this phase's deliverables |
| V4 Access Control | No | Not applicable — a public, MIT-licensed skill file has no access-control boundary by design |
| V5 Input Validation | Yes, narrowly | `tools/check_repo.py`'s new frontmatter parser reads untrusted-shaped but locally-authored text (the repo's own `SKILL.md`) — the existing file's own defensive pattern (`_carrier_is_repo_relative`, guarding against path traversal via `..` segments or absolute paths in a parsed carrier string, `tools/check_repo.py:383-395`, read this session) is the precedent to follow: any new path-like value the frontmatter parser extracts (none currently expected — frontmatter has no path-valued fields) should be defended the same way if one is later added |
| V6 Cryptography | No | Not applicable — no cryptographic operation anywhere in this phase |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| A malformed/malicious `SKILL.md` frontmatter silently failing to load in a harness, with no local signal until a user reports it | Tampering (of trust in the artifact) / Denial of Service (of the skill's own activation) | D-33's CI-enforced allow-list + name-match + description-bound check — this is the actual security-relevant control this phase adds: catching a distribution-breaking defect before it reaches any user, not a traditional injection/auth vulnerability |
| A future contributor adding a path-like value inside frontmatter (e.g., if `allowed-tools` or a future field ever carried a file path) without path-traversal defense | Tampering (path escape reading/writing outside intended scope) | Not currently a live risk (no frontmatter field is path-valued in this phase's scope) — noted only so the existing `_carrier_is_repo_relative` pattern (`tools/check_repo.py:383-395`) is reused if this ever becomes relevant, rather than a new, weaker check being hand-rolled |
| Reproducing proprietary framework training-deck structure or phrasing inside rule prose (a content-integrity risk, not a STRIDE-classic security threat, but load-bearing for this project) | Tampering (of the project's own legal/trust posture) | `SOURCES.md`'s existing rule (paraphrase only, at the level of generality a listed public source states) — this is a human-judgment boundary Phase 6's LEG-04 gate owns, not something `tools/check_repo.py` can mechanically check (per `SOURCES.md:18-22`, read this session: "This is a semantic judgement — no tool in this project's stated stack performs it") |

## Sources

### Primary (HIGH confidence — read directly this session)

- `.planning/phases/02-rule-catalog-integrity-skill-md-core/02-CONTEXT.md` — all 34 decisions, discretion items, deferred items, canonical refs
- `.planning/REQUIREMENTS.md` — CAT/INT/MOD requirement text and traceability table
- `.planning/STATE.md` — Phase 1 completion history, standing blockers
- `.planning/ROADMAP.md` — Phase 2 goal, success criteria, phase-boundary decisions
- `NUMBERING.md` — PF reserved ranges, PF-1 sub-blocks, MC reserved blocks, Allocated/Deprecated ID tables, range-exhaustion and versioning rules
- `NOTICES.md` — attribution pointer string, framework statements (all three)
- `README.md` — target repository layout, rule-numbering summary
- `examples/deal-brief.md` — all facts, Canonical figures table, customer source material, inconvenient facts
- `SOURCES.md` — reproduction boundary, out-of-bounds material
- `tools/check_repo.py` — full file read; existing violation codes, parsing helpers, self-test and mutation-test harness
- `~/devoteam/.claude/plugins/marketplaces/simple-english/skills/simple-english/SKILL.md` — full file read + `wc -l -w -c` measurement (329 lines / 3,664 words / 21,590 chars)
- `~/devoteam/.claude/plugins/marketplaces/simple-english/skills/simple-english/references/checklist.md` — full file read (searchable-pattern shape precedent)
- `python3 --version` / `git --version` — run directly this session

### Secondary (MEDIUM confidence — cited from this project's own prior-session research, itself sourced from official docs)

- `.planning/research/ARCHITECTURE.md` — SKILL.md length/progressive-disclosure ceiling, numbering-scheme rationale, mode-axis rationale, anti-patterns — this file's own sourcing is HIGH (fetched directly from `agentskills.io` and Anthropic's own docs one day prior), carried here as CITED since not independently re-fetched this session
- `.planning/research/PITFALLS.md` — the eight named pitfalls, trademark-litigation findings, comparative-advertising legal standard — MEDIUM-HIGH per that file's own confidence rating, carried here as CITED
- `.planning/research/STACK.md` — Agent Skills frontmatter schema, distribution-channel schemas, claude.ai description-length discrepancy — HIGH per that file's own confidence rating for the frontmatter schema specifically (fetched directly from the live spec)

### Tertiary (LOW confidence — flagged, not independently verified this session)

- The sibling skill's `evals/pressure-tests.md` exact format — referenced only via `ARCHITECTURE.md`'s system diagram, not independently re-read this session; flagged as Assumption A4

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no new packages, frontmatter schema previously fetched from the live spec, stdlib-only Python confirmed present on this machine
- Architecture: HIGH for file layout and CI-extension patterns (all read directly this session); MEDIUM for the line-budget arithmetic (my own estimate against a real measured baseline, not a drafted-and-measured Proof First catalog)
- Pitfalls: HIGH — all eight sourced from a prior dedicated pitfalls-research pass, cross-referenced against this project's own frozen registries and example facts this session
- Security: MEDIUM — this phase has a genuinely small security surface (a Markdown/YAML authoring task plus a local CI script); the ASVS mapping is honest about how little of the standard set applies rather than forcing relevance

**Research date:** 2026-09-11
**Valid until:** Effectively the life of this phase's plan — nothing in this research is time-sensitive except the Agent Skills spec fetch (carried from a research pass one day prior; re-verify if the plan is executed more than ~30 days after this date) and the sibling skill's measured line count (stable unless the sibling repo is updated).
