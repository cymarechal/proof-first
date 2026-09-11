# Phase 3: Completeness Audit & Artifact Patterns - Research

**Researched:** 2026-09-11
**Domain:** Extending an already-shipped, near-token-ceiling Agent Skill (`skills/proof-first/SKILL.md`) with a second rule namespace (`MC-`) living in a new reference file, four artifact-family pattern files, and two new classes of stdlib-only CI check (MC-namespace registry drift, structural presence). No new runtime code paradigm — this phase is Markdown authoring plus `tools/check_repo.py` extension, exactly like Phase 2, but starting from a file that has almost no headroom left.
**Confidence:** HIGH for all repo-internal facts (line/word/token counts, checker code paths, registry contents — all read or measured directly this session). MEDIUM for the paraphrase-safety judgment in Q2 (SOURCES.md itself states this is a semantic judgment no tool performs, and the actual legal verdict is Phase 6 LEG-04's). LOW/flagged where the research can only observe an inherited risk it cannot resolve (the MC dimension ordering already frozen in NUMBERING.md/REQUIREMENTS.md, discussed below).

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| AUD-01 | Document-level completeness checklist derived from MEDDICC, 8 dimensions as document questions | Q2 below — paraphrase framing pattern; NUMBERING.md's frozen `MC` blocks already name the 8 dimensions (`NUMBERING.md:66-77`) |
| AUD-02 | Checklist lives in its own reference file and its own `MC-` namespace, never blended into prose rules | Already structurally supported: `NOTICES.md:37` already lists `references/completeness-audit.md` as a required carrier; `NUMBERING.md`'s MC/PF ranges are already disjoint and enforced by `check_range_id` (`tools/check_repo.py:355-377`) |
| AUD-03 | Writer can run the audit independently and get a separate verdict | Q3/Q7 below — this is a mode-level instruction addition, largely model-behavior (see Q6) |
| ART-01–04 | Four artifact-family patterns (RFP/RFI, proposal, executive summary, demo/discovery) | Q3 below; `references/artifact-patterns.md` is the anticipated file (`NOTICES.md:38`, `README.md:41-42,61-62`) |
| MOD-03 | Check mode reports 3 labeled categories + structural ordering pass | Q4 below — Phase 2's two-category convention (`SKILL.md:284-294`) is the exact pattern to extend, per D-20's own stated intent |
| MOD-04 | Skill classifies artifact family before applying rules, states which one | Q3 below — Write mode already does half of this (`SKILL.md:263`, D-18); Check mode does not yet |
| MOD-05 | Check mode never cites a nonexistent rule number | Q5 below — `undefined-id` already covers this for both namespaces with zero new code; `catalog-id-drift`/`catalog-count` are PF-only today and need an MC-equivalent |

</phase_requirements>

## Summary

Phase 3 inherits a `SKILL.md` that is **not comfortably under its progressive-disclosure ceiling — it is nearly out of runway.** Measured this session: 309 lines / 3,694 words / an estimated 4,802 tokens against `check_skill_token_budget`'s 5,000-token ceiling (`tools/check_repo.py:1017-1036`) — a margin of **198 estimated tokens, roughly 150 words.** The line margin (191 lines to the 500-line ceiling, `tools/check_repo.py:999`) looks comfortable in isolation, but the token estimator (`word_count * 1.3`, the same estimator Phase 2's own research and `02-07`'s trim used) is the binding constraint, and it is nearly exhausted. This is the single most load-bearing finding for planning this phase: **any new instruction text placed directly in `SKILL.md` — even a short classification pointer or a third check-mode category heading — consumes real, scarce budget, and the plan should budget for a trim of existing `SKILL.md` prose to make room, not assume headroom exists.** Phase 2 already faced and solved exactly this problem once (`02-07-PLAN.md` moved the 20 worked ✗/✓ pairs to a new `references/worked-examples.md` file, cutting `SKILL.md` from 4,775 to 3,694 words) — Phase 3 should expect to need a comparable move, or at minimum a comparable trim pass, before or immediately after adding its own mode-level instructions.

The second load-bearing finding: **almost everything Phase 3 needs architecturally already exists or is already anticipated.** `NOTICES.md:34-42` already lists `skills/proof-first/references/completeness-audit.md` and `skills/proof-first/references/artifact-patterns.md` as required attribution-pointer carriers — these are not new file-layout decisions, they are already-registered obligations waiting for the files to be created. `NUMBERING.md`'s `MC reserved blocks` table (`NUMBERING.md:66-77`) already names and ranges all eight MEDDICC-derived dimensions. `SKILL.md`'s Write mode already emits an assumed-artifact-family line (`SKILL.md:263`, D-18) — Phase 3's MOD-04 work is "extend this to Check mode and give each family real conventions," not "invent classification from nothing." `check_mode`'s two-category, ordered, no-findings-line report structure (`SKILL.md:278-294`) is explicitly designed by Phase 2's D-20 to have a third category added "and changes nothing else" (`02-RESEARCH.md:98`, quoted from `02-CONTEXT.md`). And `check_undefined_id` (`tools/check_repo.py:388-412`) already scans `skills/`, `examples/`, and `README.md` for both `PF-\d+\.\d+` and `MC-\d+` tokens against `NUMBERING.md`'s Allocated IDs table — MOD-05's core citation-validity guarantee is **already live and namespace-agnostic**, and will start enforcing itself against MC citations the moment any file cites one, with zero new code.

What genuinely does not exist yet and must be built new: (1) the actual MC dimension content and the two new reference files; (2) an MC-namespace equivalent of `catalog-id-drift`/`catalog-count`, because `parse_skill_catalog`, `RULE_HEADING_RE`, `parse_checklist`, and `check_catalog_id_drift`'s `numbering_pf_ids` are all hard-coded to the `PF-` prefix and the `SKILL.md` file specifically (`tools/check_repo.py:216,850,874,892`) — none of them will ever look at `references/completeness-audit.md` or find an `MC-` heading; (3) the classification/three-category mode-level instructions in `SKILL.md` itself, which must be authored inside an almost-exhausted token budget.

**Primary recommendation:** Treat this phase as two nearly-independent tracks that share one scarce resource (`SKILL.md`'s remaining ~150 words). Track A (content): author `references/completeness-audit.md` and `references/artifact-patterns.md` as free-standing files, each carrying the attribution pointer once, with `SKILL.md` touched only by the smallest possible set of pointers. Track B (enforcement): extend `tools/check_repo.py` with an MC-equivalent of the PF drift/count checks, proven self-test-then-mutation-test exactly as Phase 2's `02-01`/`02-06`/`02-08` did for PF. Sequence a single-dimension tracer (Q7) through both tracks before bulk-authoring the remaining seven MC dimensions and four artifact families, and re-measure `SKILL.md`'s token estimate immediately after the tracer's `SKILL.md`-touching edits — before writing any more prose anywhere.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| MEDDICC-derived completeness audit content (8 MC dimensions as document questions) | Reference Layer (`references/completeness-audit.md`, new) | Enforcement Layer (`NUMBERING.md` MC ranges, already frozen) | AUD-02 requires this never blend into `SKILL.md`'s prose rules — it is progressive-disclosure content, loaded only when the audit is run, exactly like `references/deletion-test.md` today |
| Artifact-family conventions (RFP, proposal, exec summary, demo/discovery) | Reference Layer (`references/artifact-patterns.md`, new) | Content Layer (`SKILL.md`'s classification pointer) | Four families' worth of convention detail cannot fit in `SKILL.md`'s remaining ~150-word budget; `SKILL.md` states the family and points here, matching the existing `references/deletion-test.md`/`references/checklist.md` pointer pattern (`SKILL.md:47-51`) |
| Classification instruction (which family, before rules apply) | Content Layer (`SKILL.md`, extends existing Write-mode line) | Reference Layer (`artifact-patterns.md` supplies the four families' names/fallback detail) | Precedent already exists in Write mode (D-18, `SKILL.md:263`); this is a small mode-level instruction, not new rule content, and belongs where the mode instructions already live |
| Three-category + structural-ordering check-mode report | Content Layer (`SKILL.md`, extends existing two-category Check-mode text) | Reference Layer (`artifact-patterns.md` defines what "correct order" means per family) | D-20 already designed the two-category structure to take a third category with no restructuring (`SKILL.md:284`); the ordering pass's *definition* is family-specific and lives in `artifact-patterns.md`, but the *instruction to run it and report it* is a mode-level instruction in `SKILL.md` |
| MC ID registry and namespace-drift enforcement | Enforcement Layer (`NUMBERING.md` + `tools/check_repo.py`, both extended) | — | Same split Phase 2 used for PF: `NUMBERING.md` is the single source of truth (already holds the MC ranges); the checker must gain an MC-equivalent of `catalog-id-drift`/`catalog-count`, which today only look at PF (`tools/check_repo.py:216,850,874,892,938,940`, verified this session) |
| Citation-validity guarantee (MOD-05) at the shipped-file level | Enforcement Layer (`check_undefined_id`, already live) | — | Already namespace-agnostic and already scans every relevant root (`tools/check_repo.py:388-412`) — zero new code needed for this specific half of MOD-05; see Q5 |

## Package Legitimacy Audit

**N/A — this phase installs no external packages in any ecosystem.** All new content is Markdown, and all new checker code is stdlib-only Python extending `tools/check_repo.py`, matching the project's existing zero-dependency posture and Phase 2's own precedent (`02-RESEARCH.md:196-198`). No `npm view`/`pip index versions`/`cargo search` applies.

## User Constraints

No `03-CONTEXT.md` exists in `.planning/phases/03-completeness-audit-artifact-patterns/` as of this research session — `/gsd-discuss-phase` has not yet run for Phase 3. There are therefore no locked decisions, discretion areas, or deferred ideas to copy verbatim. The planner should treat every "Claude's Discretion"-shaped choice flagged below (exact MC rule wording, exact structural-ordering-pass placement, exact new-check-code naming) as open until a discuss-phase pass locks it, the same way Phase 2's `02-CONTEXT.md` locked its 34 decisions before `02-RESEARCH.md` was written. `[VERIFIED: ls .planning/phases/03-completeness-audit-artifact-patterns/ this session — directory is empty except for this file]`

## Project Constraints (from CLAUDE.md)

`./.claude/CLAUDE.md` (reproduced in this agent's system context) carries repo-wide directives binding this phase:

- **Zero dependencies. Stdlib Python 3 only.** No pip install, no test framework, no NLP library — non-negotiable, already litigated.
- **Legal paraphrase boundary.** MEDDICC, Command of the Message, and Challenger are proprietary/trademarked. Paraphrase concepts at the level of generality public sources state them; reproduce zero source text; never adopt a source-coined term as this repo's own label; never reproduce a source's ordered list in source order. `SOURCES.md` and `NOTICES.md` define the boundary (both read this session — see Q2).
- **Evidence.** Measured claims or no claims. Never assert success without a checkable verification.
- **Progressive disclosure.** `SKILL.md` under 500 lines / ~5,000 tokens, enforced by `skill-too-long` and `skill-token-budget-exceeded` (`tools/check_repo.py:1002-1036`). Currently at 309 lines / ~4,802 estimated tokens — see Summary above. This is the phase's single tightest constraint.
- **GSD workflow enforcement.** File-changing tool calls happen through a GSD command, not ad hoc.
- **No emojis** in shipped content unless explicitly requested (the ✗/✓ marks used throughout the catalog are explicitly exempted by Phase 2's own precedent, `02-RESEARCH.md:156`).

## Standard Stack

### Core

| Component | Version/Spec | Purpose | Why Standard |
|---|---|---|---|
| Python 3 standard library only (`re`, `argparse`, `pathlib`, `shutil`, `tempfile`) | 3.13.13 confirmed present `[VERIFIED: python3 --version, run this session]` | Extending `tools/check_repo.py` with MC-namespace checks | Matches the file's own stated posture (`tools/check_repo.py:8-9`) and the project's zero-dependency constraint |
| git | 2.54.0 confirmed present `[VERIFIED: git --version, run this session]` | Commit, phase workflow | Standard |
| Agent Skills frontmatter schema | Current spec, no version number (carried unchanged from Phase 2's research) | `SKILL.md`'s frontmatter is untouched by this phase unless the planner chooses to add classification/audit trigger keywords to `description` | Phase 2's D-29/D-30 already locked the description's shape; Phase 3 should not reopen that decision without a fresh discuss-phase pass, since it is flagged `costly`/`one-way` in `02-CONTEXT.md` |

### Supporting

None. This phase adds no new package to any ecosystem.

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Extending `check_catalog_id_drift`/`check_catalog_count` in place to branch on namespace | Writing wholly separate `check_mc_catalog_id_drift`/`check_mc_catalog_count` functions | Either is viable stdlib-only Python; the existing functions are already parameterized enough (`PF_ID_RE`, `RULE_HEADING_RE`, `'PF rules'` section name are all local constants/literals, not deeply threaded) that a parallel MC-flavored function reusing the same `split_sections`/`table_rows` helpers is likely *less* risky than branching one function on namespace, because a bug in a shared branch risks silently breaking the already-proven PF path — see Don't Hand-Roll below |
| A single reference file for both the MC audit and the four artifact patterns | Two separate files (`completeness-audit.md`, `artifact-patterns.md`) | `NOTICES.md:37-38` already lists them as two separate required carriers; AUD-02 explicitly requires the completeness audit to be "never blended" with anything else; keep them separate, matching what is already registered |

**Installation:** None.

## Architecture Patterns

### System Architecture Diagram

```
                         WRITER'S REQUEST
                               │
                               ▼
        ┌───────────────────────────────────────────────┐
        │  SKILL.md loads in full (~4,802 est. tokens    │
        │  today, ~150-word margin to 5,000 ceiling)      │
        └───────────────┬─────────────────────────────────┘
                         │
                         ▼
        ┌───────────────────────────────────────────────┐
        │  NEW: Classify artifact family                 │  ← MOD-04
        │  (RFP/RFI, proposal, exec summary, demo/        │    extends existing
        │  discovery, or "does not fit" fallback)          │    Write-mode line
        │  → read references/artifact-patterns.md          │    (SKILL.md:263,
        │    for the chosen family's conventions            │    D-18) to also
        └───────┬─────────────────────┬───────────────────┘    fire in Check mode
                 │                     │
      WRITE MODE │                     │ CHECK MODE
                 ▼                     ▼
   ┌───────────────────────┐   ┌────────────────────────────────┐
   │ (unchanged from        │   │ 1. Prose violations (existing) │
   │  Phase 2, now applies   │   │ 2. Integrity flags (existing)  │  ← MOD-03: 3rd
   │  the classified          │   │ 3. NEW: Completeness gaps      │    category +
   │  family's conventions)   │   │    (against references/         │    structural-
   └───────────────────────┘   │    completeness-audit.md,        │    ordering pass,
                                │    MC-# citations)                │    reusing the
                                │ 4. NEW: Structural ordering pass  │    D-20/D-21
                                │    (against the classified        │    no-findings-
                                │    family's own convention in     │    line + fixed-
                                │    artifact-patterns.md)          │    order convention
                                └───────────────┬────────────────────┘
                                                 │
                                                 ▼
        ┌───────────────────────────────────────────────────────┐
        │  CI ENFORCEMENT (tools/check_repo.py)                    │
        │  undefined-id: ALREADY namespace-agnostic (PF-#.# and     │  ← MOD-05, mostly
        │    MC-#), scans skills/, examples/, README.md — fires      │    free (Q5)
        │    against an undefined MC-# the moment one is cited,      │
        │    zero new code (tools/check_repo.py:388-412)             │
        │  NEW: MC-equivalent of catalog-id-drift/catalog-count —    │  ← genuinely new
        │    compares NUMBERING.md's MC Allocated IDs, completeness-  │    (Q5)
        │    audit.md's MC-defining headings, and checklist.md's new  │
        │    "## MC rules" section for three-way agreement            │
        │  NEW (optional, AUD-02 structural half): a check that no    │
        │    MC-# heading is ever defined inside SKILL.md itself       │
        └───────────────────────────────────────────────────────┘
```

### Recommended Project Structure

```
skills/
└── proof-first/
    ├── SKILL.md                            # EXTENDED — minimal-footprint additions only
    └── references/
        ├── deletion-test.md                 # unchanged
        ├── checklist.md                      # EXTENDED — new "## MC rules" section
        ├── worked-examples.md                # unchanged (or gains MC worked pairs — planner discretion)
        ├── completeness-audit.md             # NEW — the 8 MC dimensions, AUD-01/02
        └── artifact-patterns.md              # NEW — the 4 artifact families, ART-01–04
NUMBERING.md                                  # EXTENDED — MC Allocated IDs rows filled in
tools/
└── check_repo.py                             # EXTENDED — MC-namespace drift/count checks
```

`[VERIFIED: NOTICES.md:34-42, quoted: "- `skills/proof-first/SKILL.md`\n- `skills/proof-first/references/completeness-audit.md`\n- `skills/proof-first/references/artifact-patterns.md`\n- `README.md`\n\nA listed path that does not exist yet is skipped by the checker."]` — this exact file layout is not a new decision this research is proposing; it is an obligation already registered and waiting.

### Pattern 1: `SKILL.md`'s Token Budget Is the Binding Constraint, Not Lines

**What:** `check_skill_too_long` (`tools/check_repo.py:1002-1009`) enforces a 500-line ceiling; `check_skill_token_budget` (`tools/check_repo.py:1020-1036`) separately enforces an estimated-5,000-token ceiling using `word_count * 1.3` (`SKILL_TOKEN_WORDS_PER_TOKEN_RATIO`, `tools/check_repo.py:1016`). Both are live and both passed as of this session's baseline run (`python3 tools/check_repo.py` → `check_repo: 0 violations`, run this session).

**Measured baseline `[VERIFIED: wc -l -w -c skills/proof-first/SKILL.md, run this session: "309 3694 22902"]` and `[VERIFIED: python3 -c "..." computing word_count*1.3, run this session: "lines=309 words=3694 est_tokens=4802 ceiling=5000 margin=198"]`:**

| Metric | Value | Ceiling | Margin |
|---|---|---|---|
| Lines | 309 | 500 | 191 |
| Words | 3,694 | — | — |
| Estimated tokens (words × 1.3) | 4,802 | 5,000 | **198 tokens ≈ 150 words** |

**Why this matters concretely:** 150 words is roughly the length of two short paragraphs, or one `Reference files` pointer bullet plus one mode-instruction sentence. A naive addition of (a) a classification step naming four families with a fallback (~15-25 lines), (b) a completeness-audit pointer/mode instruction (~10-15 lines), and (c) a third check-mode category plus a structural-ordering-pass instruction (~10-15 lines) — a combined ~35-55 lines at the file's own measured ~12 words/line average (3,694 words / 309 lines ≈ 12) — is **~420-660 words, several times the remaining budget.** This is not a risk to flag for later; it is close to certain to blow the ceiling unless offset by a trim.

**Recommendation:** Budget one of two moves into the plan, decided explicitly rather than discovered at verification time:
1. **Trim first.** Re-read `SKILL.md`'s existing prose (particularly the Marker vocabulary section, `SKILL.md:33-45`, and the Check mode section, `SKILL.md:278-294`, both of which have some restatement) for words that can be cut without changing meaning, mirroring `02-07`'s dewrapping-and-tightening approach (`STATE.md:110,115` — "reclaimed 162 lines," "26-of-31 rule-statement tightening"), *before* adding new content — so the new content lands inside a re-measured, known-good margin instead of pushing an already-tight file over.
2. **Extract before adding**, the same move `02-07` made for worked examples: if the classification instruction or check-mode extension needs any illustrative detail beyond a bare pointer, put the *detail* in `references/artifact-patterns.md`/`references/completeness-audit.md` and leave only the *shortest possible imperative sentence* in `SKILL.md` (e.g., "Classify the artifact family before applying any rule; see `references/artifact-patterns.md`." rather than naming and describing all four families inline).

Either way, **re-measure `wc -l -w -c` and re-run `python3 tools/check_repo.py` after every `SKILL.md` edit**, not once at the end — this is the exact discipline `02-RESEARCH.md`'s own Pattern 1 recommended and Phase 2 needed a full gap-closure plan (`02-07`) to retrofit after not doing it continuously the first time. Do not repeat that miss.

**When to use:** Before authoring a single new line in `SKILL.md` for this phase, and after every subsequent edit to it.

### Pattern 2: Classification Already Has a Foothold — Extend, Don't Invent

**What:** Write mode already states: *"Output is exactly three parts, in order: one line naming the artifact family this response assumes (an RFP answer, a proposal section, an executive summary, or demo or discovery material), the prose itself, then the trailing register."* `[VERIFIED: SKILL.md:263, quoted verbatim]`. This is Phase 2's D-18, deliberately placed as groundwork: *"The assumed-family line surfaces a correctable assumption and puts the sentence MOD-04 will formalise in Phase 3 in place now, so Phase 3 tightens an existing behaviour rather than introducing a new one."* `[VERIFIED: 02-RESEARCH.md:96, quoted verbatim from 02-CONTEXT.md's D-18]`.

**What is missing:** Check mode (`SKILL.md:278-294`) has **no** classification statement at all today — it goes straight to "Output is a report, never a corrected document." `[VERIFIED: SKILL.md:278-294, read in full this session — no artifact-family line anywhere in this section]`. MOD-04 and Phase 3's success criterion 3 ("Skill states which artifact family it classified the document as, before applying any rules") require both modes, not just Write mode.

**Recommendation:** Add the shortest possible parallel sentence to Check mode's opening (e.g., one clause stating the classified family before "Output is a report...", mirroring Write mode's phrasing) rather than restructuring Check mode. This keeps the addition to roughly one sentence — critical given Pattern 1's budget finding.

**Fallback case (a document that fits no family):** Neither `SKILL.md` nor any existing reference file states what happens when a document does not cleanly fit one of the four families. Phase 3's classification instruction needs an explicit fallback clause (e.g., "state the closest-fitting family and note the mismatch" or "state that no family fits and apply only the prose/integrity rules"). This is genuinely new content with no existing precedent to extend — budget it as new lines, not a one-word addition.

**Where the four families' actual conventions live:** Not in `SKILL.md` at all — `references/artifact-patterns.md` (new file) is where ART-01–04's answer-first ordering, architecture-narrative-and-risk-treatment, problem-reframe-then-business-case, and discovery-to-follow-up conventions belong, following the exact "pointer in `SKILL.md`, detail in `references/`" pattern already established for the deletion test (`SKILL.md:49`, "Before applying the deletion test to a compound term... read `references/deletion-test.md`") and the checklist (`SKILL.md:50`).

### Pattern 3: The Two-Category Check-Mode Report Was Explicitly Designed to Take a Third Category

**What:** `[VERIFIED: SKILL.md:284-294, quoted verbatim]`:
> "Findings are grouped under two labelled sections in this fixed order: `## Integrity flags` first — findings that can cost a deal or create legal exposure are read before anything else.
>
> `## Prose violations` comes second. Within a group, findings run in document order... Both category headings always print. A group with nothing to report carries an explicit no-findings line rather than disappearing, so a clean document still produces a report."

Phase 2's own research recorded the design intent explicitly: *"D-20: The report is blocks... grouped under two labelled categories now: 'Prose violations' and 'Integrity flags'. Phase 3's MOD-03 adds 'Completeness gaps' as a third group and changes nothing else."* `[VERIFIED: 02-RESEARCH.md:98, quoted verbatim from 02-CONTEXT.md's D-20]`.

**Recommendation:** Add `## Completeness gaps` as a third labeled section, in the same fixed order (before/after the existing two is the planner's choice — MOD-03's own ordering rationale suggests integrity-cost-exposure findings still come first, so a natural order is Integrity flags → Completeness gaps → Prose violations, or Integrity flags → Prose violations → Completeness gaps; either is defensible, pick one and record it, mirroring how D-21 explicitly recorded the existing two-category order and its reasoning). Reuse the identical no-findings-line convention verbatim — do not invent new wording for "nothing to report here."

**The structural ordering pass is a fourth, distinct thing, not a category:** MOD-03's text is "reports prose violations, completeness gaps, and integrity flags as three separately labeled categories, **plus** a structural ordering pass" — the "plus" signals this is not a fourth category of *finding* so much as an additional *pass* the check performs (e.g., "is this RFP response's structure actually answer-first, per the classified family's convention in `artifact-patterns.md`?"). Recommend giving it its own small labeled section (e.g., `## Structural ordering`) with the same no-findings-line convention, so all four "have I checked X" outputs are visually and mechanically consistent — but this is Claude's Discretion pending a discuss-phase pass; record whichever choice is made as a locked interface, the same way D-20 was locked, because Phase 4's worked examples and Phase 5's linter will need to parse it exactly as-is.

### Pattern 4: Paraphrasing the MEDDICC-Derived Audit Safely — What Phase 2 Already Decided and What Is Inherited, Not New

**What SOURCES.md actually prohibits `[VERIFIED: SOURCES.md:11-16, quoted verbatim]`:**
> "A concept restated in this repository's own words, at a level of generality a listed source states publicly, is paraphrase. A contiguous run of a source's own wording, a source's own ordered list reproduced in its order, a source's diagram or figure, and a term coined by a source and adopted here as this repository's own label are each reproduction, and none of them ships."

**How Phase 2 handled the analogous hazard for Command of the Message:** `PF-1`'s seven sub-blocks are named "Before scenario, After scenario, Required Capabilities, Metrics, Proof Points, Differentiators, Positive Business Outcomes" `[VERIFIED: NUMBERING.md:32-40, quoted verbatim]` — generic-sounding labels for a widely-taught sales-methodology structure, not narrative descriptions of the concept. Critically, **the rule bodies never define what a "Before scenario" abstractly *is*** — they are written as direct, checkable instructions using this project's own deal-brief facts (e.g., PF-1.1: *"Describe the before state in the buyer's own words about their estate, never in the vendor's category language"* `[VERIFIED: SKILL.md:65-69]`), never as a restatement of a source's own definition or teaching material. This is the transferable pattern: **label with a generic sub-block name, then operationalize as an instruction grounded in this project's own facts — never restate the source's explanation of the concept.**

**What is already frozen and NOT this phase's decision to make:** `NUMBERING.md`'s MC dimension table already names all eight dimensions — "Metric, Economic Buyer, Decision Criteria, Decision Process, Paper Process, Pain, Champion, Competition" `[VERIFIED: NUMBERING.md:66-77, quoted verbatim]` — in exactly the order the MEDDICC/MEDDPICC acronym itself spells out (M-E-D-D-P-I-C-C, informally "Pain" for "Identify Pain"). `REQUIREMENTS.md`'s AUD-01 independently states the same eight, in the same order: *"covering metric, economic buyer, decision criteria, decision process, paper process, pain, champion, and competition"* `[VERIFIED: .planning/REQUIREMENTS.md:34, quoted verbatim]`. **Both of these were fixed before Phase 3 began** (`NUMBERING.md` at Phase 1, `REQUIREMENTS.md` at requirements-definition time) — Phase 3 cannot silently reorder or relabel the eight dimensions without contradicting two already-frozen documents.

**Why this matters for SOURCES.md's own "source's own ordered list reproduced in its order" prohibition:** the MC dimension range order **is** the MEDDICC acronym's own canonical order. This is a real, inherited paraphrase-safety tension that this research cannot resolve on the planner's behalf (SOURCES.md itself states no tool performs this judgment, and Phase 6's LEG-04 gate owns the actual verdict — `SOURCES.md:18-22`). What the planner *can* do inside this phase's scope:
- Keep the dimension **labels** as-is (already frozen, already the widely-used generic vocabulary for this methodology per `SOURCES.md`'s own public-page sources) — this is not the risky part.
- Write each dimension's actual audit **content** (the document-facing question, its rationale, its worked example) entirely in fresh, project-specific language — never restating any source's own definition of what that MEDDICC letter conceptually means, following PF-1's exact pattern above.
- Consider (flagged as an open question below, not a locked recommendation) whether `references/completeness-audit.md`'s **prose framing** of the eight dimensions needs to state explicitly that the ID-range order is a numbering-scheme artifact inherited from `NUMBERING.md`, not an assertion that this is "the" correct or original sequence — this is a defensive documentation move, not a code change, and costs no token budget in `SKILL.md` since it lives in the reference file.
- Flag this tension explicitly for Phase 6's LEG-04 gate, the same way `WINDOWS.md` id 3 already flags an open paraphrase-boundary judgment for Phase 2's PF-0.1/PF-3.1 framing (`WINDOWS.md:20`) — this phase should add its own analogous entry rather than treat the question as silently resolved.

**Worked-example material to reuse:** `examples/deal-brief.md` already contains ready-made facts mapping cleanly onto every MC dimension, letting the audit's worked examples cite real, already-canonical figures rather than inventing new ones: Diane Osoria's stated run-rate target maps to Metric/Economic Buyer (`examples/deal-brief.md:26,77`); the weighted decision-criteria table maps to Decision Criteria (`examples/deal-brief.md:81-87`); the three-review paper process maps to Paper Process (`examples/deal-brief.md:89-91`); the unmeasured settlement-batch overrun and Priya Raghunathan's stated incumbent preference map to Pain and Competition/Champion tension respectively (`examples/deal-brief.md:34,47,71`); Marcus Feld is the stated champion (`examples/deal-brief.md:27`); the three shortlisted bidders map to Competition (`examples/deal-brief.md:9`).

### Pattern 5: Extending `tools/check_repo.py` for the MC Namespace — What Is PF-Only Today

**What already exists and is namespace-agnostic (reuse, zero changes needed):**
- `check_undefined_id` (`tools/check_repo.py:388-412`) — scans `skills/` (recursively, all `.md`), `examples/`, `README.md` for `re.findall(r'PF-\d+\.\d+', text) | re.findall(r'MC-\d+', text)` and reports any token absent from `NUMBERING.md`'s Allocated IDs table. **This already covers MC.** It will start firing against a hallucinated `MC-#` citation in any shipped file the instant that file exists — no new code. `[VERIFIED: tools/check_repo.py:404-405, quoted: "tokens = set(re.findall(r'PF-\\d+\\.\\d+', text)) | set(re.findall(r'MC-\\d+', text))"]`
- `check_range_id` (`tools/check_repo.py:355-377`) — already validates any `MC-#` Allocated ID against `mc_ranges` (per-dimension-block, not one aggregate range, per Phase 1's own `01-06` gap closure). Already proven live in this session's mutation-test (`range-id` fired correctly). No change needed for MC content that respects the existing dimension blocks.
- `split_sections`/`table_rows` (`tools/check_repo.py:230-262`) — the generic Markdown table/section reader every other parser reuses. Directly reusable for a new `## MC rules` section in `checklist.md` and for a new MC-heading extractor in `completeness-audit.md`.

**What is PF-only today and will NOT see MC content unless extended `[VERIFIED: grep this session, tools/check_repo.py:216,850,874,892,938,940]`:**
- `PF_ID_RE = re.compile(r'^PF-(\d+)\.(\d+)$')` (line 216) — used by `check_catalog_id_drift`'s `numbering_pf_ids` filter (line 892) and by `check_catalog_count` (lines 938-940). An `MC-` row is silently excluded from both checks' comparisons — it is neither counted nor drift-checked by these two functions today.
- `RULE_HEADING_RE = re.compile(r'^### (PF-\d+\.\d+) — ')` (line 850) — `parse_skill_catalog` (lines 853-864) only ever looks inside the one file it's pointed at (which will always be `skills/proof-first/SKILL.md` per `check_catalog_id_drift`'s call site) for `### PF-#.# — ` headings. Since AUD-02 requires MC content to live in `completeness-audit.md`, **not** `SKILL.md`, this extractor cannot simply be reused unmodified — it needs either a parallel function pointed at `completeness-audit.md` with an `MC-\d+` heading pattern, or a generalized version taking a path and a regex as parameters.
- `parse_checklist` (`tools/check_repo.py:867-877`) — reads only `sections.get('PF rules', '')`. A parallel `## MC rules` section in `checklist.md` needs either a second call to the same function with a different section name (the function already takes a `path` parameter and internally hard-codes `'PF rules'` as the section key — this hard-code is the one line that needs a parameter, or a near-identical sibling function needs to exist), or a new function.
- `COUNT_SENTENCE_RE` / `check_catalog_count` (`tools/check_repo.py:929-960`) — matches only `"This catalog contains {N} rules in {M} numbered sections."` inside `SKILL.md`. There is no equivalent stated-count assertion for the MC checklist anywhere. If the planner wants the same anti-hallucination mechanism D-32 gave PF ("the stated total is worse wrong than absent" — `02-RESEARCH.md:124`) for MC, a new stated-count sentence template and a matching check are needed — this is optional relative to MOD-05 (which is satisfied by `undefined-id` alone) but consistent with the project's own established double-checked-registry discipline.

**Recommendation — the concrete new-code shape:** Following Phase 2's `02-01`/`02-06`/`02-08` precedent exactly (parser first, proven against hand-built fixtures via `--self-test`, then wired into `run_all_checks`, then a mutation registered and proven via `--mutation-test`):
1. A new `MC_HEADING_RE` (e.g., `^### (MC-\d+) — `) and a `parse_completeness_audit_headings(path)` function reading `references/completeness-audit.md` for MC-defining headings, mirroring `parse_skill_catalog`'s shape but pointed at a different file.
2. Either generalize `parse_checklist(path, section_name)` to take the section name as a parameter (least code churn, lowest risk to the already-proven PF path since the PF call site simply passes `'PF rules'` explicitly) or add a small sibling `parse_checklist_mc(path)` reading `'MC rules'` — either is stdlib-only and low-risk; the parameterized version is marginally preferred since it reuses one function body instead of duplicating `table_rows` plumbing (see Don't Hand-Roll below).
3. A new `check_catalog_id_drift`-equivalent (e.g., `check_mc_catalog_id_drift`) comparing three sets: (a) `NUMBERING.md`'s `MC-` Allocated IDs (already parsed by the existing `parse_numbering`, just filter on `MC_ID_RE` instead of `PF_ID_RE`), (b) `completeness-audit.md`'s MC-defining headings, (c) `checklist.md`'s new `## MC rules` rows. Same "present in some, missing from others" violation shape as the existing PF version.
4. Optionally, an MC stated-count check mirroring `catalog-count-unstated`/`catalog-count-mismatch`, if the planner wants the identical anti-hallucination redundancy PF has.
5. New self-test fixtures (`_bad_mc_catalog()`-style, mirroring `_bad_catalog_root`/`_good_catalog_root` at `tools/check_repo.py:2149-2160`) and new `MUTATIONS` entries, following D-34's three-part contract exactly: check wired into `run_all_checks`/`ALL_CHECK_CODES`, firing-and-silent self-test fixtures, and a mutation proving discrimination (silent on control, fires on mutated) per `mutation_test`'s own discrimination-proof bar (`tools/check_repo.py:1419-1500`, already proven this session: 22/22 codes discrimination-proven, 0 fire-only).

**AUD-02's structural half (optional but cheap):** a check could assert no `### MC-\d+ — ` heading is ever defined inside `SKILL.md` itself (i.e., `parse_skill_catalog`'s existing regex, re-run, should find zero MC-shaped headings in `SKILL.md`) — directly enforcing "never blended into the prose rules" as a build failure, not just a documentation convention. Low cost (a few lines, reuses existing extraction), high signal.

### Pattern 6: The Tracer Slice, Mirroring `02-01`'s Shape

`02-01-PLAN.md` proved the whole PF pipeline with three rules (`PF-0.1`, `PF-2.11`, `PF-3.1`) authored end-to-end — registered in `NUMBERING.md`, indexed in `checklist.md`, and with `catalog-id-drift` proven live — **before** the remaining 28 rules were bulk-authored (`ROADMAP.md`, Phase 2 Wave 1 description). The equivalent thinnest slice for Phase 3 (see Q7 for full reasoning): **one MC dimension, end-to-end, through both tracks (content + enforcement), before authoring the other seven.**

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| A second Markdown table/section reader for `completeness-audit.md`/the new `## MC rules` section | A bespoke parser distinct from what exists | `split_sections()`/`table_rows()`, already proven against `NUMBERING.md`, `examples/deal-brief.md`, and `checklist.md`'s `## PF rules` table | These functions already handle header/separator-row skipping and section-boundary detection correctly across four existing call sites; a fifth, differently-written reader risks a fifth, differently-buggy edge case |
| Two entirely independent PF and MC drift-check code paths with duplicated logic | Copy-pasting `check_catalog_id_drift` wholesale and search-replacing `PF`→`MC` | Parameterize the shared shape (a `(numbering_ids, definer_ids, checklist_ids)` three-way-set-diff helper) so PF and MC call the same comparison logic with different inputs | Reduces the chance that a future rule (e.g., "must be present in numbering AND definer AND checklist") gets fixed in one namespace's copy and silently drifts from the other's, the same "one grammar, one validation path" principle D-14 already established for the marker vocabulary |
| A maintained banned/allowed list of "safe" MEDDICC-derived phrasings as the paraphrase-safety mechanism | A verdict-only word list in `completeness-audit.md` | The same deletion-test-style discipline already used for PF-3 — ground every MC rule's actual audit question in this project's own deal-brief facts and its own words, never in a source's phrasing, checked at authoring time by a human against `SOURCES.md`, not by a checkable list | `SOURCES.md:18-22` explicitly states this is a semantic judgment no tool performs; a list would be exactly the "stale on arrival, wrong in both directions" anti-pattern `ARCHITECTURE.md` and this project's own `STACK.md` already reject for the buzzword problem — the same reasoning transfers |

**Key insight:** Every new piece of code this phase needs is a same-shaped sibling of something Phase 2 already built and proved — a second `parse_*`/`check_*`/`MUTATIONS`-entry triple, not a new kind of tool. The risk in this phase is budget and content-quality (paraphrase judgment), not engineering novelty.

## Common Pitfalls

### Pitfall 1: Treating `SKILL.md`'s remaining headroom as "enough" without re-measuring

**What goes wrong:** A plan drafts the classification instruction, the completeness-audit pointer, and the three-category/structural-ordering-pass check-mode extension all before running `wc`/`check_repo.py` again, discovers the ceiling is blown only at phase-verification time, and needs its own `02-07`-style emergency trim plan.
**Why it happens:** The line margin (191 lines) looks comfortable; the token margin (≈150 words) does not, and only the token estimator is checked by `skill-token-budget-exceeded`. A planner working from line count alone will misjudge how much room actually exists.
**How to avoid:** Pattern 1's explicit measure-after-every-edit discipline. Treat "re-run `python3 tools/check_repo.py` and `wc -l -w -c skills/proof-first/SKILL.md`" as a task-level verification step, not a phase-end one.
**Warning signs:** A drafted `SKILL.md` diff that adds more than ~10-15 lines in one task without an accompanying word-count check.

### Pitfall 2: Reordering or relabeling the MC dimensions to "fix" the paraphrase concern, silently contradicting two frozen documents

**What goes wrong:** A planner or executor, noticing Pattern 4's ordering tension, tries to resolve it unilaterally by reordering the MC dimension blocks in `NUMBERING.md` or renaming a dimension — which contradicts `REQUIREMENTS.md`'s AUD-01 wording (already using the same 8 names in the same order) and breaks `NUMBERING.md`'s own "range exhaustion... a build failure, not a judgement call" posture (`NUMBERING.md:127-133`) if IDs already allocated against the old order need renumbering.
**Why it happens:** The tension is real and this research cannot fully resolve it (see Pattern 4) — a planner under pressure to "just make it safe" may reach for the wrong lever.
**How to avoid:** Do not touch `NUMBERING.md`'s MC dimension names or order. The paraphrase-safety lever available to this phase is *content* (the actual audit question wording, framing, and worked examples), not the dimension labels or their ID-range order, both of which are frozen inputs from before this phase. Flag the tension explicitly (a new `WINDOWS.md` entry, mirroring id 3) rather than attempting a structural fix.
**Warning signs:** Any plan task that edits `NUMBERING.md`'s existing `MC reserved blocks` table's row order or names, rather than only filling in previously-empty Allocated ID rows within the existing ranges.

### Pitfall 3: Assuming MOD-05 is "done" once `undefined-id` covers citations, without closing the MC drift gap

**What goes wrong:** A plan reads that `check_undefined_id` already handles MC tokens (true, see Q5) and concludes no new checker work is needed for MOD-05 — but a Allocated ID in `NUMBERING.md` with no matching heading in `completeness-audit.md` (or vice versa) will not be caught by `undefined-id` at all (that check only looks for citation tokens in prose, not for definitional agreement across the three registry-adjacent files) — reintroducing exactly the "check that cannot fire" defect class Phase 1 spent three gap-closure plans closing for PF.
**Why it happens:** `undefined-id`'s scope (citation validity) and `catalog-id-drift`'s scope (definitional three-way agreement) are easy to conflate; Phase 2's own research made the same distinction explicit for PF and this phase must make it explicit for MC too.
**How to avoid:** Build the MC-equivalent drift check (Pattern 5) as its own deliverable, not as an assumed side effect of `undefined-id` already existing.
**Warning signs:** A plan whose verification section cites only `undefined-id`/`--mutation-test`'s existing PF-focused entries as proof of MOD-05 coverage, with no new fixture or mutation naming the MC namespace specifically.

### Pitfall 4: Confusing MOD-03/MOD-04's "shipped-file" half with their "live model behavior" half

**What goes wrong:** A plan claims MOD-03/MOD-04 are "verified" because `tools/check_repo.py` passes, when the actual requirement — does a live check-mode session really print three labeled sections and a structural-ordering-pass, does a live session really state the classified family before applying rules — is model behavior no static file-reading checker can observe.
**Why it happens:** `tools/check_repo.py` only reads committed repository files; it never invokes the skill or reads a model's live output. This is the same class of gap Phase 2 already hit for MOD-01/MOD-02 (`02-RESEARCH.md`'s own Validation Architecture table: "manual (this is prose-authoring correctness, not mechanically testable... UAT / conversational verification against the phase's five success criteria, not a script)").
**How to avoid:** State plainly in the plan (see Q6 below) which half of each requirement is CI-checkable (existence/structure of the shipped instruction text and reference files) and which half is permanently manual/UAT, following Phase 2's own precedent of ending with `nyquist_compliant: false` for the model-behavior half rather than promising verification that cannot be delivered.
**Warning signs:** A plan's Definition of Done listing MOD-03/MOD-04 as "automated" with no accompanying UAT/conversational-verification step.

## Code Examples

### Existing Write-mode classification line (the pattern Check mode's new line should mirror)

```
# Source: skills/proof-first/SKILL.md:263 — read this session
Output is exactly three parts, in order: one line naming the artifact family this
response assumes (an RFP answer, a proposal section, an executive summary, or demo
or discovery material), the prose itself, then the trailing register.
```

### Existing two-category Check-mode report structure (the pattern the third category must match)

```
# Source: skills/proof-first/SKILL.md:284-294 — read this session, quoted verbatim
Findings are grouped under two labelled sections in this fixed order:
`## Integrity flags` first — findings that can cost a deal or create legal exposure
are read before anything else.

`## Prose violations` comes second. Within a group, findings run in document order...

Both category headings always print. A group with nothing to report carries an
explicit no-findings line rather than disappearing, so a clean document still
produces a report.
```

### Existing `undefined-id` check — already namespace-agnostic, zero new code needed for citation validity

```python
# Source: tools/check_repo.py:388-412, read in full this session
def check_undefined_id(allocated, repo_root):
    allocated_ids = {row['id'] for row in allocated}
    roots = [repo_root / 'skills', repo_root / 'examples', repo_root / 'README.md']
    ...
    for f in files:
        if f.name == 'NUMBERING.md':
            continue
        text = strip_fences(f.read_text(encoding='utf-8'))
        tokens = set(re.findall(r'PF-\d+\.\d+', text)) | set(re.findall(r'MC-\d+', text))
        for tok in sorted(tokens):
            key = (tok, str(f))
            if tok not in allocated_ids and key not in seen:
                ...
```

### Existing PF-only drift check — the shape a new MC-equivalent must mirror, with the hard-coded PF filter to generalize

```python
# Source: tools/check_repo.py:850,867-877,892, read in full this session
RULE_HEADING_RE = re.compile(r'^### (PF-\d+\.\d+) — ')   # PF-only; needs an MC sibling

def parse_checklist(path):
    """Return the PF IDs listed in a references/checklist.md's '## PF rules'
    table..."""
    ...
    for row in table_rows(sections.get('PF rules', '')):   # hard-coded section name
        ...

def check_catalog_id_drift(allocated, repo_root):
    ...
    numbering_pf_ids = {row['id'] for row in allocated if PF_ID_RE.match(row['id'])}  # PF-only filter
```

### `NUMBERING.md`'s frozen MC dimension blocks (input this phase fills, does not redesign)

```
# Source: NUMBERING.md:66-77, read this session, quoted verbatim
| Dimension | Range |
|---|---|
| Metric | MC-1-MC-5 |
| Economic Buyer | MC-6-MC-10 |
| Decision Criteria | MC-11-MC-15 |
| Decision Process | MC-16-MC-20 |
| Paper Process | MC-21-MC-25 |
| Pain | MC-26-MC-30 |
| Champion | MC-31-MC-35 |
| Competition | MC-36-MC-40 |

Ceiling: `MC-40`.
```

## State of the Art

| Old Approach (Phase 2's shipped state) | Current Approach (this phase must build) | When Changed | Impact |
|---|---|---|---|
| `SKILL.md` has comfortable-looking headroom (368 lines mid-Phase-2, before `02-07`'s trim) | `SKILL.md` at 309 lines / ~4,802 est. tokens, ~150-word margin, *after* `02-07`'s trim already extracted worked examples to their own file | `02-07` (Phase 2 gap closure) | There is no more "extract the worked examples" lever left to pull if the token budget is exceeded again — the next lever is trimming existing prose itself, a materially harder move than moving already-separable content to a reference file |
| Two labeled check-mode categories (`Integrity flags`, `Prose violations`), designed explicitly to take a third | Three categories + a structural ordering pass | This phase (MOD-03) | D-20 already anticipated this; no restructuring needed, only careful reuse of the existing no-findings-line convention |
| `catalog-id-drift`/`catalog-count` cover only the PF namespace | Must cover MC too, or MOD-05's definitional-drift half (as opposed to its citation-validity half, already covered) has a silent gap | This phase | The exact "check that cannot fire" defect class Phase 1 spent three gap-closure plans closing for PF must not be reintroduced for MC |

**Deprecated/outdated for this phase's purposes:** None — this phase's dependencies (Phase 1's registries, Phase 2's checker and catalog) are all current and unchanged since the baseline measured this session.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The ~12-words/line, ~35-55-line estimate for a naive classification+audit+three-category addition to `SKILL.md` | Pattern 1 | If the planner's actual drafted addition is shorter (a bare one-sentence pointer per concern) the budget concern is less severe than stated; if longer (inline family descriptions, inline MC dimension summaries) it is worse — this is a planning estimate, not a locked number |
| A2 | Structural ordering pass should get its own labeled section (`## Structural ordering`) rather than folding into one of the three named categories | Pattern 3 | This is explicitly flagged as Claude's Discretion pending a discuss-phase pass; if a future `03-CONTEXT.md` locks a different shape, this recommendation should be discarded, not treated as already decided |
| A3 | The paraphrase-safety recommendation in Pattern 4 (keep frozen labels/order, ground content in project-specific facts, flag the ordering tension for LEG-04) is the correct mitigation, not a definitive legal clearance | Pattern 4 | `SOURCES.md` itself states this judgment belongs to a human, ultimately Phase 6's LEG-04 gate — this research's recommendation reduces risk but does not resolve it; treating it as resolved would be the exact "asserted rather than checkable" failure this project exists to prevent |
| A4 | Parameterizing `parse_checklist(path, section_name)` is lower-risk than a separate sibling function, for the MC checklist reader | Pattern 5 | If the planner finds the parameterization touches the already-proven PF call site in a way that risks regressing it, a sibling function (more code, zero shared-path risk) is the safer fallback — flagged as a design choice, not a must |

## Open Questions

1. **Does the MC dimension order (frozen in `NUMBERING.md` and `REQUIREMENTS.md`, matching MEDDICC's own canonical acronym order) constitute a "source's own ordered list reproduced in its order" under `SOURCES.md`'s reproduction rule?**
   - What we know: the labels and the order both predate this phase (Phase 1's `NUMBERING.md`, requirements-definition-time `REQUIREMENTS.md`); `SOURCES.md` states this is a semantic judgment no tool performs, owned by Phase 6's LEG-04 gate.
   - What's unclear: whether an ID-range numbering-scheme order (an engineering necessity — MC-1 through MC-40 needs *some* sequence) is the same kind of "ordered list" SOURCES.md means, versus a narrative list an author chose freely.
   - Recommendation: do not attempt to resolve this inside Phase 3's plan. Add a new `WINDOWS.md` entry (mirroring id 3's shape) flagging it explicitly for LEG-04, and consider (at zero token cost, since it lives in a reference file, not `SKILL.md`) a defensive sentence in `completeness-audit.md` noting the ID order is inherited numbering-scheme structure, not an assertion of "the" canonical sequence.

2. **Should the structural-ordering pass be its own labeled report section, or folded into one of the three named categories?**
   - What we know: MOD-03's wording treats it as separate from the three categories ("...as three separately labeled categories, plus a structural ordering pass").
   - What's unclear: exact placement/heading wording is unlocked (no `03-CONTEXT.md` exists yet).
   - Recommendation: treat as a discuss-phase decision; this research's Pattern 3 recommendation (own labeled section, same no-findings-line convention) is a starting proposal, not a locked interface.

3. **Should the MC checklist gain its own stated-count anti-hallucination sentence (mirroring `SKILL.md`'s "This catalog contains N rules in M numbered sections")?**
   - What we know: MOD-05's core requirement (never cite a nonexistent number) is already satisfied by `undefined-id` alone, with no stated-count mechanism required.
   - What's unclear: whether the project wants the same redundant double-check D-32 gave PF ("a wrong stated total is worse than none," `02-RESEARCH.md:124`) applied symmetrically to MC, purely for consistency/robustness, or whether that is scope the planner should decline as unnecessary for this phase.
   - Recommendation: optional; flag for the planner's discretion rather than requiring it, since MOD-05 itself does not depend on it.

4. **Does `references/worked-examples.md` need MC-namespace worked pairs, mirroring the 20 PF ones it currently holds?**
   - What we know: `worked-examples.md` currently carries only PF pairs (`skills/proof-first/references/worked-examples.md`, 106 lines, read this session — no MC content). D-02's judgment-carrying-rules-only example policy was a Phase 2 decision about the PF catalog specifically; whether the same policy should extend to MC dimensions (which are inherently judgment calls — "does this document name a champion" is not mechanical) is not yet decided.
   - What's unclear: whether adding MC worked pairs to this file risks the same token-budget pressure if the file itself is ever inlined, though currently it is a reference file, not part of `SKILL.md`'s own budget, so the risk is lower here than for `SKILL.md` itself.
   - Recommendation: likely yes, given MC dimensions are exactly the kind of judgment call D-02's original rationale (examples "only on rules where judgement is required") would extend to — but this is new scope beyond a literal reading of AUD-01–03, and should be confirmed in a discuss-phase pass rather than assumed.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3 | Extending `tools/check_repo.py` | ✓ | 3.13.13 `[VERIFIED: python3 --version, run this session]` | — |
| git | Committing plan output, phase workflow | ✓ | 2.54.0 `[VERIFIED: git --version, run this session]` | — |

**Missing dependencies with no fallback:** None.
**Missing dependencies with fallback:** None — this phase requires nothing beyond what Phase 1/2 already established as present.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | `tools/check_repo.py`'s own `--self-test`/`--mutation-test` harness (no pytest/jest, by design — same as Phase 2) |
| Config file | none |
| Quick run command | `python3 tools/check_repo.py --self-test` |
| Full suite command | `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py` |

**Baseline recorded this session `[VERIFIED: all three commands run this session against the current repo]`:**
```
$ python3 tools/check_repo.py --self-test
self-test PASS - verified violation codes: catalog-count-mismatch, catalog-count-unstated,
catalog-id-drift, catalog-opening-rule-count, dup-figure-key, dup-id, figure-order,
framework-statement-missing, frontmatter-description-invalid, frontmatter-name-mismatch,
frontmatter-unknown-key, frontmatter-unparseable, license-missing, pointer-duplicated,
pointer-missing, pointer-unparseable, range-id, revived-id, skill-token-budget-exceeded,
skill-too-long, undefined-id, unlisted-figure
(exit 0)

$ python3 tools/check_repo.py --mutation-test
mutation-test CONTROL: 0 violations on the unmutated copy (0 known-open per KNOWN_OPEN_VIOLATIONS, 0 unexpected)
[... 22 "mutation-test OK" lines, one per code ...]
mutation-test PASS: 22 codes discrimination-proven
(exit 0)

$ python3 tools/check_repo.py
check_repo: 0 violations
(exit 0)
```

This is the exact baseline Phase 3 must not regress. Any new check added by this phase should raise the discrimination-proven count above 22, never leave it lower, and the CONTROL line must keep reading "0 unexpected."

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| AUD-01 | Content quality of the 8 MC dimension questions | manual (prose-authoring correctness — same class as Phase 2's CAT-01–06) | UAT / conversational verification | N/A — not unit-testable |
| AUD-01 (structural half) | `completeness-audit.md` exists, has exactly 8 MC-defining headings matching `NUMBERING.md`'s 8 allocated dimension rows | unit (new) | `python3 tools/check_repo.py --self-test` (after new fixtures) | ❌ Wave 0 — new parser + check + fixtures needed |
| AUD-02 | Own reference file, own namespace, never blended into prose rules | unit (mostly existing: `range-id`/`dup-id`/`revived-id` already enforce namespace disjointness; new: no MC heading inside `SKILL.md`) | `python3 tools/check_repo.py --self-test` | ⚠️ Partially exists (namespace disjointness) — MC-in-SKILL.md exclusion check is new |
| AUD-03 | Writer can run the audit independently and get a separate verdict | manual (model behavior — does a live session actually produce a standalone MC verdict on request) | UAT / conversational verification | N/A |
| ART-01–04 | Content quality of the four family conventions | manual (same class as AUD-01's content half) | UAT / conversational verification | N/A |
| ART-01–04 (structural half) | `artifact-patterns.md` exists, has four required family sections | unit (new, optional) | `python3 tools/check_repo.py --self-test` (if the planner adds this check) | ❌ Wave 0, if scoped |
| MOD-03 | Live check-mode output actually shows 3 labeled categories + structural-ordering pass | manual (model behavior) | UAT / conversational verification | N/A |
| MOD-03 (shipped-instruction half) | `SKILL.md` actually contains the three-category + ordering-pass instruction text | unit (grep-style, could piggyback on `catalog-count`-style literal-string check if the planner wants one) | Not currently scoped as a distinct check; optional | ❌ if scoped |
| MOD-04 | Live classification behavior in both modes | manual (model behavior) | UAT / conversational verification | N/A |
| MOD-05 | Shipped files never cite a nonexistent PF/MC number | unit (mostly existing) | `python3 tools/check_repo.py` (`undefined-id`, already live for both namespaces) | ✅ for citation validity; ❌ Wave 0 for MC-equivalent of `catalog-id-drift`/`catalog-count` (definitional agreement) |
| MOD-05 | Live check-mode session never hallucinates a number in a fresh conversation | manual (model behavior — no static checker can observe a future live session) | UAT / conversational verification | N/A — permanently manual, same as CAT-10's trigger-reliability half |

**As with Phase 2, expect the model-behavior half of every requirement in this table (AUD-01/03 content and independence, ART-01–04 content, MOD-03/04's live behavior, MOD-05's live-session half) to remain permanently `nyquist_compliant: false`** — no file-reading checker can assert what a live model session does. The planner should state this plainly in the plan's Definition of Done, exactly as `02-RESEARCH.md`'s own Validation Architecture table already did for CAT-01–06/INT-01–06/MOD-01/02, rather than promise verification this phase cannot deliver.

### Sampling Rate

- **Per task commit:** `python3 tools/check_repo.py --self-test`
- **Per wave merge:** `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py`
- **Phase gate:** Full suite green before `/gsd-verify-work`, plus a UAT pass covering the model-behavior requirements table above (mirroring Phase 2's `02-UAT.md` precedent).

### Wave 0 Gaps

- [ ] `references/completeness-audit.md` — does not exist yet (new file, first Phase 3 content deliverable)
- [ ] `references/artifact-patterns.md` — does not exist yet (new file)
- [ ] `NUMBERING.md`'s MC Allocated IDs rows — table exists with zero MC rows filled in today (`[VERIFIED: NUMBERING.md's Allocated IDs table, lines 84-116, read this session — contains only PF-prefixed rows]`)
- [ ] `checklist.md`'s `## MC rules` section — does not exist yet (currently only `## PF rules`, `[VERIFIED: skills/proof-first/references/checklist.md, read in full this session — single section]`)
- [ ] MC-namespace parser/check/fixtures/mutation quartet in `tools/check_repo.py` — does not exist yet (Pattern 5)
- [ ] `SKILL.md`'s Check-mode classification line, third check-mode category, and structural-ordering-pass instruction — none exist yet (Patterns 2/3)
- [ ] `SKILL.md`'s remaining token budget re-measurement checkpoint — no automated gate enforces "re-measure after every edit," this is a plan-level discipline, not a CI check (mirrors Phase 2's own unresolved gap noted in `02-RESEARCH.md`'s Wave 0 Gaps: "No automated line-count gate exists for CAT-08... otherwise, treat as a plan-level manual checkpoint")

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | No authentication surface — static Markdown content and a local CI script |
| V3 Session Management | No | Not applicable |
| V4 Access Control | No | Not applicable — public MIT-licensed content |
| V5 Input Validation | Yes, narrowly | Same as Phase 2's finding: the new MC-namespace parser reads locally-authored, repo-owned Markdown, not untrusted external input. Reuse `_carrier_is_repo_relative`-style path-traversal defense (`tools/check_repo.py:543-555`) only if a future field ever carries a path value — not currently applicable to any MC-related field |
| V6 Cryptography | No | Not applicable |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| An `MC-` ID allocated in `NUMBERING.md` with no matching definition anywhere, silently drifting (the "check that cannot fire" class) | Tampering (of the registry's own claimed guarantee) | The new MC-equivalent of `catalog-id-drift`, proven via self-test + mutation-test, exactly mirroring Phase 1/2's precedent for PF |
| Reproducing a MEDDICC source's own definition text or ordered list inside `completeness-audit.md` | Tampering (of the project's legal/trust posture) | `SOURCES.md`'s existing paraphrase rule — a human-judgment boundary this phase's authors must apply directly (Pattern 4), with the residual ordering tension routed explicitly to Phase 6 LEG-04 rather than silently accepted |
| `SKILL.md` silently exceeding its token budget after this phase's edits, only discovered at a later CI run or at verification time | Denial of Service (of the skill's own progressive-disclosure contract, and of harnesses that truncate long instruction files) | Pattern 1's re-measure-after-every-edit discipline; `skill-token-budget-exceeded` is already a live, proven CI gate (confirmed in this session's baseline) that will catch a regression at the next `python3 tools/check_repo.py` run regardless — but discovering it after full drafting (Phase 2's own near-miss) costs a whole extra gap-closure plan |

## Sources

### Primary (HIGH confidence — read or measured directly this session)

- `skills/proof-first/SKILL.md` — full file read; measured `wc -l -w -c` (309/3694/22902) and computed token estimate (4802/5000, margin 198)
- `skills/proof-first/references/checklist.md`, `deletion-test.md`, `worked-examples.md` — full files read
- `examples/deal-brief.md` — full file read, including Canonical figures table
- `NUMBERING.md` — full file read, including frozen MC reserved blocks and empty MC Allocated IDs
- `NOTICES.md` — full file read, including the required-carriers list naming both Phase 3 reference files
- `SOURCES.md` — full file read, including the reproduction-boundary rule and the MEDDIC-family source table
- `tools/check_repo.py` — full 2368-line file read in two passes; every check function, parser, fixture, and mutation examined for PF-only vs. namespace-agnostic scope
- `.planning/REQUIREMENTS.md` — full file read, including AUD/ART/MOD requirement text and the traceability table
- `.planning/ROADMAP.md` — Phase 3's goal, requirements, and success criteria read
- `.planning/WINDOWS.md`, `.planning/STATE.md` — read in full for standing blockers and decision history
- `.planning/phases/02-rule-catalog-integrity-skill-md-core/02-RESEARCH.md` — read in full (630 lines) as the phase's own methodological precedent
- `.github/workflows/ci.yml`, `evals/pressure-tests.md`, `README.md` — read for CI job order and distribution/status context
- `python3 --version` (3.13.13), `git --version` (2.54.0) — run directly this session
- `python3 tools/check_repo.py --self-test && python3 tools/check_repo.py --mutation-test && python3 tools/check_repo.py` — run directly this session, full output recorded in Validation Architecture above

### Secondary (MEDIUM confidence)

- None new this session — this research is entirely grounded in repo-internal, directly-read/measured evidence. No external documentation lookup (Context7/web search) was needed, since the phase's domain is this project's own existing codebase and registries, not a third-party library or framework.

### Tertiary (LOW confidence)

- None.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no new packages, stdlib-only Python confirmed present, matches Phase 2's already-established posture exactly
- Architecture: HIGH for file layout and CI-extension patterns (all read directly this session, cross-checked line-by-line against the actual `tools/check_repo.py` source); MEDIUM for the exact new-code shape recommendation (parameterize vs. sibling function) since this is a design choice, not a fact
- Pitfalls: HIGH — grounded directly in this session's own measurements (the token-budget finding) and in Phase 2's own documented near-miss (`02-07`'s trim), not speculation
- Paraphrase-safety (Q2/Pattern 4): MEDIUM — the transferable pattern (label generically, operationalize with project facts, never restate source definitions) is directly observed from Phase 2's shipped `PF-1` content; the residual ordering-tension judgment is explicitly LOW/unresolved by design, per `SOURCES.md`'s own admission that this is a human/legal judgment, not a research finding
- Security: MEDIUM — small, honestly-scoped surface, matching Phase 2's own ASVS mapping precedent

**Research date:** 2026-09-11
**Valid until:** Effectively the life of this phase's plan. The one time-sensitive fact is `SKILL.md`'s measured token margin (198 estimated tokens) — this must be re-measured at the start of planning if any other phase or hotfix touches `SKILL.md` between this research and plan execution, since the margin is thin enough that even a small unrelated edit could change the calculus materially.
