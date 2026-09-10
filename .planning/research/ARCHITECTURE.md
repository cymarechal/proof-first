# Architecture Research

**Domain:** Public, open-source AI agent skill repository (rule-based writing skill, modelled on `AminBlg/SimpleEnglish`)
**Researched:** 2026-09-10
**Confidence:** HIGH for repo layout and eval-harness shape (directly inspected reference implementation, byte-for-byte); MEDIUM-HIGH for the numbering scheme and mode-axis recommendations (novel design work, no external prior art exists for this project's specific catalog shape); HIGH for SKILL.md length/progressive-disclosure guidance (sourced from Anthropic's own docs, see Sources).

## System Overview

Reference implementation surveyed directly: `AminBlg/SimpleEnglish` v1.3.0, checked out locally at `~/.claude/plugins/marketplaces/simple-english/`.

```
┌───────────────────────────────────────────────────────────────────────┐
│                        DISTRIBUTION LAYER                              │
│  .claude-plugin/{plugin.json, marketplace.json}   (Claude Code plugin) │
│  output-styles/<name>.md                          (Claude Code style)  │
│  prompts/system-prompt.md                         (universal fallback) │
│  README.md                                        (human entry point)  │
├───────────────────────────────────────────────────────────────────────┤
│                        SKILL CONTENT LAYER                              │
│  skills/<name>/SKILL.md            (frontmatter + numbered catalog)    │
│  skills/<name>/references/*.md     (progressive disclosure, on-demand) │
├───────────────────────────────────────────────────────────────────────┤
│                        EVIDENCE / PROOF LAYER                          │
│  examples/*.md                     (worked before/after, human-facing) │
│  evals/scenarios.json              (fixed prompts, one fictional deal) │
│  evals/*_lint.py                   (deterministic proxy counter)       │
│  evals/run_bench.py                (generation + aggregation runner)   │
│  evals/results/{raw/*.json, results.json, RESULTS.md}                  │
├───────────────────────────────────────────────────────────────────────┤
│                        LEGAL LAYER                                      │
│  LICENSE                           (MIT)                                │
│  [MISSING in reference — required here] NOTICES / trademark posture    │
└───────────────────────────────────────────────────────────────────────┘
```

Four layers, each with a distinct audience: harnesses read the Distribution layer to install/activate the skill; the model reads the Content layer at inference time; humans and CI read the Evidence layer to validate the headline claim; anyone reads the Legal layer before reusing the repo commercially. This separation is the single most important structural property of the reference repo, and it holds up well for Proof First — keep it.

### What Works (keep as-is)

- **Progressive disclosure is real, not decorative.** `SKILL.md` never inlines its checklist, its full word-swap table, or its per-use-case adaptations — it names the reference file and one sentence of when to read it. The model loads `SKILL.md` on every activation and the references only when the task needs them.
- **The eval harness is a closed, auditable loop.** `scenarios.json` (fixed input) → `run_bench.py` (generation) → `*_lint.py` (deterministic scoring) → `results/raw/*.json` (committed receipts) → `results.json` + `RESULTS.md` (published, regenerable). Every headline number in the README traces to a raw file that ships in the repo.
- **One fictional artifact anchors every example.** `sqlpipe` (a Postgres-to-S3 CLI) is the subject of every scenario prompt, every before/after pair, and the README's own copy. Nothing is invented ad hoc per file, so examples never contradict each other.
- **Three consumption paths for three levels of harness support**: SKILL.md (Agent Skills standard), output-style (Claude Code, always-on), system-prompt.md (anything else, paste-able, with an explicit ~60-token emergency-budget version). This triage is why the skill installs the same way in Cursor, Codex, Copilot, and bare chat UIs.
- **Honesty is engineered into the harness, not just claimed in prose.** `ste_lint.py`'s docstring states its own ceiling ("a regex pass, not a grammar parser... undercounts... not a compliance verdict") and `RESULTS.md` carries a standing "Honest number warnings" section (effort-level sensitivity, one-generation-per-cell, no compliance guarantee). This is a load-bearing pattern, not decoration — Proof First's PROJECT.md commits to the identical evidence standard.

### What Is Missing for a Repo Carrying Three Trademarked Frameworks

SimpleEnglish's legal posture is a single line in the README footer ("Unofficial project... ASD-STE100 is a registered trademark of ASD") because it has exactly one rights-holder, and that rights-holder *publishes an open standard for exactly this kind of reuse*. Proof First has three rights-holders (Force Management for Command of the Message, Challenger Inc., and the MEDDIC/MEDDPICC training vendors), none of whom publish an open standard inviting paraphrase, and all three names will appear repeatedly across SKILL.md, references, and README. A single footer line does not scale to that.

Required additions the reference repo does not need and this repo does:

1. **A single canonical `NOTICES.md` at repo root** (or a top-level section of README, but a dedicated file is safer for a public repo that may get scraped or forked) naming all three frameworks, their rights-holders, an explicit non-affiliation statement per framework, and the paraphrase boundary ("concepts only, zero reproduced training material, zero reproduced proprietary diagrams or terminology owned outright by the vendor"). Every other file (SKILL.md header, README, the three framework-touching reference files) **links to this file once** rather than repeating the disclaimer. Repetition of legal language across N files is N chances to state it slightly wrong; one canonical file with N pointers is one thing to get right and keep current.
2. **MEDDICC needs its own reference file, structurally separate from the prose rule catalog**, not because of length but because of legal and semantic hygiene: it is a licensed sales-qualification framework being paraphrased as a checklist, and keeping it in its own file with its own disclaimer keeps the "this is paraphrase, not reproduction" boundary auditable per-framework instead of smeared across the whole skill.
3. **Framework attribution belongs at the point of use, not only in NOTICES.md.** Each of the three framework-derived sections (the CotM-spine catalog section, the MEDDICC checklist file, the Challenger opening rule) should carry a one-line "derived from, not affiliated with, see NOTICES.md" pointer at its own top. This is the same posture SimpleEnglish takes with ASD-STE100 in SKILL.md's own header ("paraphrased... reproducing zero spec or dictionary text") — just repeated three times at three points of use instead of once, because three different rights-holders are involved and a reader (or a lawyer) auditing only the MEDDICC file should not have to go find the CotM disclaimer to know the posture applies uniformly.

### Genuine Dependency Order Between Distribution-Layer Components (repo-layout level)

- `LICENSE` and `NOTICES.md` have zero content dependencies — write first, anytime.
- `.claude-plugin/{plugin.json,marketplace.json}` depend only on final directory names (`skills/<name>/`, not on SKILL.md content) — scaffold early, edit description text late.
- `output-styles/<name>.md` and `prompts/system-prompt.md` are **lossy compressions of SKILL.md**, not independent artifacts. They must be authored (and re-authored on every material SKILL.md change) after SKILL.md's rule content is stable, exactly as SimpleEnglish's own `output-styles/simple-english.md` and `prompts/system-prompt.md` are near-identical condensed restatements of `SKILL.md`. Treat this as a **synced-derivative pair with an ongoing maintenance cost**, not a one-time build task.
- `README.md`'s prose can be drafted early; its **badges and headline numbers are a hard dependency on the benchmark having actually run** (SimpleEnglish's badge literally reads "−74.6% measured," sourced from `evals/results/RESULTS.md`). Do not draft a README with placeholder numbers and forget to close the loop — this is the single most likely place for the repo to accidentally violate its own "measured claims or no claims" evidence constraint.

## Component Responsibilities

| Component | Owns | Must NOT own |
|---|---|---|
| `skills/proof-first/SKILL.md` | Frontmatter (name/description/license/compatibility/version), two-mode framing (write/check), artifact-family classification step, the full numbered rule catalog (compact: one instruction line + short before/after per rule), the deletion-test rule statement (with 1-2 examples only), the integrity rules, the self-check sequence, pointers to every reference file | Exhaustive verification checklists, the full MEDDICC checklist, the full per-artifact-family templates, the full contested-terms table for the deletion test — all of these delegate |
| `skills/proof-first/references/checklist.md` | Exhaustive, searchable audit pass over the **prose rule catalog only** (PF-numbered rules), for check mode and final self-review | MEDDICC completeness — that is a different catalog with a different namespace, kept in its own file |
| `skills/proof-first/references/meddicc-checklist.md` | The completeness audit: does the document name a metric, address the economic buyer, mirror decision criteria, respect the paper process, name identified pain, arm the champion, address competition — as binary/graded checklist items (MC-numbered), not prose instructions | Any judgment about sentence quality, buzzwords, or tense/voice — MEDDICC is a qualification lens, never a style rule |
| `skills/proof-first/references/artifact-patterns.md` | Per-artifact-family structural templates: RFP/RFI response, solution proposal, executive summary, demo/discovery material — section order, which CotM elements dominate which artifact, which buyer-stage concerns apply | Restating prose mechanics or the deletion test — these are referenced by rule number (`PF-4.x`), never re-explained |
| `skills/proof-first/references/deletion-test.md` | The deletion test worked in detail: a table of contested terms shown **as pairs** (sentence with term → same sentence with term deleted → verdict: meaning survived = buzzword, meaning broke = legitimate technical noun), so the file teaches the mechanism, not a static blocklist | A verdict-only table — that would silently recreate the maintained blocklist the deletion test exists to avoid |
| `output-styles/proof-first.md` | Always-on Claude Code style: condensed instruction set for every reply, not just triggered writing tasks | Anything not already stated in SKILL.md — it is a compression, never a divergent source of truth |
| `prompts/system-prompt.md` | Paste-able fallback for harnesses with no skill support, plus a token-budget emergency version | Framework attribution nuance beyond a one-line pointer — full NOTICES.md content does not belong in a 60-token budget |
| `examples/deal-brief.md` (new — no analog in reference repo) | The single fictional cloud-migration deal: company profile, deal size, competitors, timeline, pain points, target metrics — the shared facts every other example and scenario must agree with | Rule content or persuasion technique — it is data, not instruction |
| `examples/before-after.md` | Human-facing worked rewrites, all set in the deal-brief's fictional deal, demonstrating specific rule numbers | Claims not backed by the deal brief's stated facts (no inventing a new number mid-example) |
| `evals/scenarios.json` | Fixed prompts per artifact family, anchored to the deal brief, tagged by artifact type (and, for check-mode scenarios, pre-written "before" text to audit) | Scoring logic — scenarios are pure input |
| `evals/proof_lint.py` | Deterministic proxy counter: sentence-length/hedge/modal proxies for prose mechanics, presence-of-number/named-role proxies for CotM and MEDDICC completeness, an illustrative (not authoritative) buzzword regex list | Any claim to BE the deletion test or the MEDDICC audit — it is explicitly a correlate, caveated exactly as `ste_lint.py` caveats itself |
| `evals/run_bench.py` | Orchestration: model × condition × scenario generation, lint invocation, aggregation to `results.json`, rendering of `RESULTS.md`, resumability | Judging quality — that is a separate rubric-based pass, kept in its own function/flow |
| `evals/results/raw/*.json` | Committed, one file per model × condition × scenario (× judge), the actual receipts | Aggregation logic — raw files are immutable once written for a given run |
| `evals/results/results.json` + `RESULTS.md` | Generated/regenerable summary and published report, with a standing "honest number warnings" section | Anything not derivable from `raw/` — no manually-edited numbers |
| `NOTICES.md` (new) | Canonical statement of all three frameworks' rights-holders, non-affiliation, and paraphrase boundary | Being duplicated verbatim elsewhere — other files point to it |
| `.claude-plugin/{plugin.json,marketplace.json}` | Distribution metadata for the Claude Code plugin marketplace | Skill content — pure manifest |
| `README.md` | Before/after hook, install instructions for every harness, links out to everything else, badges sourced from `RESULTS.md` | Being the source of truth for any number — it only ever quotes `RESULTS.md` |

## Recommended Project Structure

```
proof-first/
├── skills/
│   └── proof-first/
│       ├── SKILL.md                      # catalog spine, ~350-450 lines
│       └── references/
│           ├── checklist.md              # exhaustive PF-rule audit pass
│           ├── meddicc-checklist.md      # MC-numbered completeness audit
│           ├── artifact-patterns.md      # RFP/RFI, proposal, exec summary, demo/discovery
│           └── deletion-test.md          # contested-term pairs, worked
├── output-styles/
│   └── proof-first.md                    # Claude Code always-on style
├── prompts/
│   └── system-prompt.md                  # universal fallback + token-budget version
├── examples/
│   ├── deal-brief.md                     # the one fictional deal — source of truth
│   └── before-after.md                   # worked rewrites, all set in the deal
├── evals/
│   ├── scenarios.json                    # fixed prompts, anchored to deal-brief.md
│   ├── proof_lint.py                     # deterministic proxy counter
│   ├── run_bench.py                      # generation + aggregation runner
│   └── results/
│       ├── raw/*.json                    # committed, one per model x condition x scenario
│       ├── results.json                  # generated summary
│       └── RESULTS.md                    # generated + published report
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── NOTICES.md                            # NEW — canonical trademark/attribution statement
├── README.md
└── LICENSE
```

### Structure Rationale

- One reference file per audit dimension, never one file mixing dimensions: `checklist.md` (prose), `meddicc-checklist.md` (completeness), `artifact-patterns.md` (structure-by-type), `deletion-test.md` (buzzword mechanism). This mirrors the reference repo's one-file-per-concern pattern (`checklist.md`, `word-swaps.md`, `use-cases.md`) but adds a fourth file because Proof First genuinely has a fourth orthogonal concern (MEDDICC) that SimpleEnglish's domain never had.
- `examples/deal-brief.md` is a new file with no analog in the reference repo — SimpleEnglish gets away without one because its "sqlpipe" facts are simple enough (a CLI tool, a handful of commands) to stay consistent by discipline alone. Proof First's fictional deal carries dollar figures, named roles, a timeline, and competitors across four artifact families and a MEDDICC completeness audit — enough moving facts that an explicit source-of-truth file is required, not optional.
- `NOTICES.md` sits at repo root, not inside `skills/`, because it must be readable by someone auditing the repo's legal posture without first understanding the skill's internal structure — the same reason `LICENSE` lives at root.

## Architectural Patterns

### Pattern 1: SKILL.md Length and Progressive Disclosure

**What:** SKILL.md is loaded in full whenever the model activates the skill, so its length is a direct, per-invocation token tax. Anthropic's own guidance (the Agent Skills spec and its authoring docs) states a three-level loading model: (1) frontmatter — name + description, ~100 tokens, loaded into the system prompt for every installed skill on every turn; (2) the SKILL.md body, loaded only when the skill is triggered, with a stated ceiling of **roughly 5,000 tokens / under 500 lines**; (3) bundled reference files, loaded only when the model actually opens them. Content that does not need to be present on every activation belongs at level 3.

**When to use:** Any content that is exhaustive, long-tail, or needed only for a specific sub-task (a full audit checklist, a full per-artifact template, a full contested-term table) is a level-3 candidate by definition — the question is never "is this useful" but "is this needed on *every* activation."

**Trade-offs:** Push too much to references and the model may under-read them (progressive disclosure only works if SKILL.md's pointer sentence is compelling and specific enough that the model actually opens the file when the task needs it — vague pointers get skipped). Push too little to references and SKILL.md creeps past the ceiling, and past that ceiling every activation gets more expensive and, per community authoring guidance, models measurably read and follow shorter bodies more reliably than long ones.

**Concrete budget for this project:** The reference SKILL.md is 329 lines carrying 53 rules across 9 sections — comfortably under the 500-line ceiling. Proof First's catalog has five conceptual sections (Opening/Challenger, Structure/CotM, Proof & Integrity, Specificity/Buzzwords, Prose Mechanics) and does not need to match STE's 53-rule count — a well-scoped target is **35-45 rules**, because CotM elements (roughly 6-10 rules), Integrity (6-8), the deletion test (1-3), and the Challenger opening (1) are all *smaller* than a full grammar system, and Prose Mechanics — the section at real risk of bloating past the ceiling — should be **the smallest section relative to its STE-derived scope**, not the largest.

### Pattern 2: Self-Contained Prose Mechanics Without Re-Deriving SimpleEnglish

**What:** PROJECT.md requires prose mechanics with zero dependency on the `simple-english` skill. The failure mode to avoid is re-deriving STE's full 12-rule verb/sentence/punctuation apparatus (STE Sections 3+4, 19 rules) inside Proof First's catalog, which would both duplicate a sibling skill's content (a maintainability and license-paraphrase risk of its own, since STE's own wording is itself a paraphrase of a copyrighted standard) and consume the token budget that CotM/Integrity/Buzzword sections need more.

**When to use:** Restate only the subset of prose discipline that is instrumental to *persuasive, evidence-backed* writing, not exhaustive grammar coverage: sentence-length discipline (a single ceiling, not STE's dual 20/25 procedural/descriptive split, since presales prose is overwhelmingly descriptive/persuasive rather than procedural), active voice, modal/hedge discipline (the STE modal ladder is directly reusable in spirit — "should/would/may/might/could" read as uncertainty a technical evaluator will notice — but restate it in Proof First's own words), one-claim-per-sentence, and filler deletion (governed by the deletion test, not a second word-swap list).

**Trade-offs:** A smaller mechanics section means Proof First's prose is less mechanically rigid than STE's — this is a *feature* here, not a gap: PROJECT.md is explicit that "flat, STE-style prose is a failure mode here, not a goal." The mechanics section should enforce clarity and evidence-density, not STE's telegraphic register.

**Example (rule shape, not final wording):**
```
PF-4.1  Maximum 25 words per sentence.
PF-4.2  Active voice; passive only when the agent is genuinely unknown.
PF-4.3  Approved modals: can, will, must. Treat should/would/may/might/could
        as a signal to either state the fact directly or delete the sentence.
PF-4.4  One claim per sentence — a claim and its proof point do not share a sentence.
```

### Pattern 3: The Rule-Numbering Scheme

STE's numbering (`1.1`-`9.4`, plus `GR-1`-`GR-8`) is borrowed wholesale from an external, already-versioned, already-numbered standard (ASD-STE100 Issue 9) — the skill author did not invent it, which is exactly why SKILL.md can say "cite only rule numbers that exist in this file... invented rule numbers are a known failure" and mean it: there is a fixed external ground truth to check against. Proof First has no external standard to borrow from, so the scheme has to be designed to be equally hallucination-resistant without that crutch.

**Design: two disjoint namespaces, never a single flat sequence.**

- **`PF-<section>.<n>`** — the prose rule catalog, living in `SKILL.md` and audited in full in `references/checklist.md`.
- **`MC-<n>`** — the MEDDICC completeness checklist, living entirely in `references/meddicc-checklist.md`, never appearing inside the numbered `PF` catalog.

Two prefixes exist specifically so that a check-mode report — which, unlike STE, audits a document against *two* catalogs simultaneously (prose rules and completeness) — can never produce an ambiguous citation. `PF-2.3` and `MC-2` are unambiguously different things even printed side by side in one violation report; two flat numbers (`2.3` and `2`) drawn from unrelated catalogs would not be.

**Sections and reserved ranges (PF namespace):**

| Prefix range | Section | Rules defined (v1 target) | Reserved headroom |
|---|---|---|---|
| `PF-0.1`-`0.9` | Opening / Reframe (Challenger) | 1 | to `0.9` |
| `PF-1.1`-`1.20` | Structure — Command of the Message spine | ~8-10 | to `1.20` |
| `PF-2.1`-`2.20` | Proof & Integrity | ~6-8 | to `2.20` |
| `PF-3.1`-`3.10` | Specificity & Buzzwords (deletion test) | ~2-3 | to `3.10` |
| `PF-4.1`-`4.20` | Prose Mechanics | ~10-15 | to `4.20` |
| `PF-5.1`-`5.10` | Consistency & Voice | ~3-5 | to `5.10` |

Reserving a wide numeric range per section *before* drafting the catalog (not after) is the actual load-bearing decision: it means a new rule added in a v1.1 release takes the next free number in its section's reserved range (e.g., `PF-2.9`) without disturbing any existing citation. This is why numbering is a **Phase 0/1 design decision, not a Phase-4 cleanup task** — retrofitting reserved ranges onto an organically-numbered catalog after the fact forces exactly the renumbering the scheme exists to prevent.

**Deprecation, not deletion.** A rule that is merged or retired is marked in a "Deprecated" table at the end of SKILL.md (`PF-2.7 — deprecated in v1.2.0, folded into PF-2.3`) and its number is never reassigned to new content, ever, in any future version. This gives every historical citation (a saved check-mode report, a blog post, a GitHub issue) a permanently resolvable target, even after the rule itself is gone.

**Version discipline.** Rule numbers are stable within a major version. Only a major version bump may renumber, and only with a published migration note. Minor/patch versions may add (next free number in range) or deprecate (mark, don't delete) but never renumber or reuse.

**Anti-hallucination measures, carried over from the reference repo and strengthened:**
- SKILL.md states the total rule count and section count explicitly ("N rules across M numbered sections plus the MEDDICC checklist in `references/meddicc-checklist.md`"), so a model citing `PF-9.4` or `MC-40` is citing outside a stated, checkable range.
- The explicit instruction from STE's SKILL.md — "Cite only rule numbers that exist in this file. Do not cite rule numbers from memory." — is retained verbatim in spirit, extended to cover both namespaces: check-mode output must cite `PF-#` or `MC-#`, never a bare number, and never a number from either range that was not actually defined.
- `references/checklist.md` restates every `PF` number in one place specifically so an agent doing a final self-check has a single searchable page listing every number that is allowed to exist — the same anti-hallucination function STE's `checklist.md` already serves.

### Pattern 4: The Mode Axis — Write vs. Check, Not Strictness or Artifact Type

PROJECT.md requires "both write mode and check mode." The reference repo's own axis is pragmatic-vs-strict, i.e., a *strictness* dial over vocabulary discipline. That axis exists in STE because STE's whole domain is a controlled vocabulary with a genuine spectrum from "structural rules only" to "full dictionary compliance" — pragmatic mode is a real, useful, lesser standard, not a fake compromise.

**Candidates considered and rejected:**

- **By strictness.** Rejected. There is no legitimate "looser" version of "never fabricate a customer reference" or "reframe the customer's problem before listing capabilities" — these are binary requirements. Calling integrity or the Challenger opening rule "relaxable" in a pragmatic mode would misstate what the skill actually guarantees, in the one place PROJECT.md is most explicit that a wrong answer is unacceptable ("Integrity... its own catalog section").
- **By artifact type.** Rejected as a mode, but retained as a required classification **step**, exactly parallel to STE's own "Step 1: Classify the Text" (procedural vs. descriptive), which the reference repo explicitly does *not* call one of "the two modes" — it is a prerequisite classification that every other rule then applies against. Proof First needs the same shape: "Step 1: classify the artifact family (RFP/RFI, solution proposal, executive summary, demo/discovery)" selects which template in `references/artifact-patterns.md` applies, but every `PF` rule and the MEDDICC checklist apply identically regardless of family. Making artifact type a "mode" would force every rule to carry per-artifact exceptions it does not actually have.
- **By buyer stage.** Rejected as a separate axis. Buyer stage correlates strongly with artifact family (discovery/demo material skews early-stage, executive summaries skew late/economic-buyer) closely enough that introducing it as an independent dimension on top of artifact type produces ambiguous, rarely-real combinations ("strict discovery-stage RFP"). Buyer-stage guidance belongs *inside* `references/artifact-patterns.md` as a per-family note, not as a second orthogonal mode.

**Recommendation: write mode vs. check mode**, exactly as named in PROJECT.md's own requirements list. Justification:

1. It is the only candidate axis under which the **entire rule catalog applies identically in both settings** — only the deliverable format changes (drafted prose vs. a violation report: rule/item number, offending text, compliant rewrite), which is the actual defining property a clean mode axis needs, and the one the reference repo already demonstrates works (STE's own "When asked to CHECK text instead of writing it..." instruction).
2. Because Proof First's check mode must audit against **two** catalogs at once (`PF` prose rules and `MC` completeness items) where STE only ever audits one, the write/check axis carries more real work here than it did in the source project — which is a reason to make it the primary, explicit axis rather than an implicit afterthought.
3. Artifact-family classification and write/check mode are orthogonal and compose cleanly: a check-mode pass on an executive summary applies the same `PF`/`MC` catalogs as a check-mode pass on an RFP response; only the template it compares structure against (from `artifact-patterns.md`) differs.

## Data Flow

### Eval Harness Flow

```
examples/deal-brief.md  (single source of truth: deal facts, numbers, roles)
        │
        ▼
evals/scenarios.json  (fixed prompts per artifact family, anchored to the deal;
                        write-mode prompts + check-mode prompts with seeded
                        "before" text to audit)
        │
        ▼
evals/run_bench.py  ──generate──▶  headless model call, per (model × condition
   │                                × scenario), condition ∈ {baseline, skill}
   │                                       │
   │                                       ▼
   │                          evals/proof_lint.py  (deterministic proxy scoring:
   │                          prose-mechanics proxies, CotM/MEDDICC
   │                          presence proxies, illustrative buzzword regex —
   │                          all explicitly caveated as correlates, not verdicts)
   │                                       │
   │                                       ▼
   │                          evals/results/raw/<model>__<condition>__<scenario>.json
   │                          (COMMITTED — the receipts; one file per cell,
   │                          immutable once written, resumable runner skips
   │                          existing files)
   │
   ├──judge (optional, separate pass)──▶ blind pairwise LLM judge, both orders,
   │                                     rubric covers writing quality AND
   │                                     MEDDICC completeness AND absence of
   │                                     fabricated proof
   │                                       │
   │                                       ▼
   │                          evals/results/raw/<model>__judge__<scenario>.json
   │                          (COMMITTED)
   │
   ▼ aggregate (--report-only rebuilds from raw/ alone)
evals/results/results.json   (GENERATED — regenerable summary)
evals/results/RESULTS.md     (GENERATED + PUBLISHED — headline number, per-model
                               table, judge summary, standing "honest number
                               warnings" section)
        │
        ▼
README.md  (quotes RESULTS.md numbers in badges; never restates them independently)
```

### What Is Committed vs. Generated

- **Committed, hand-authored:** `deal-brief.md`, `scenarios.json`, `proof_lint.py`, `run_bench.py`, SKILL.md, all references.
- **Committed, machine-produced, immutable per cell:** `results/raw/*.json` — these are the actual evidence. They are not regenerated on every run; the runner is resumable and skips files that already exist, exactly as `run_bench.py` does today, so extending the model matrix never silently overwrites prior receipts.
- **Committed but fully regenerable:** `results.json` and `RESULTS.md` — derived purely from `raw/`, rebuildable with a `--report-only` flag. Committing the derived output alongside the raw inputs is deliberate redundancy: it lets a reader trust the published numbers without running Python, while a skeptical reader can still `rm -rf raw && python3 run_bench.py` and reproduce from zero.

### Reproducibility and Auditability Requirements Carried Over

- **Pin reasoning/effort level per raw file**, exactly as the reference repo does (`DEFAULT_EFFORT`, recorded per generation) — effort level swings measured numbers substantially (STE's own recorded spread: 85.0% at `low` vs. 90.2% at `xhigh` on identical scenarios), so any headline number must state what it was pinned to.
- **Every headline claim must cite the specific raw files it aggregates from.** Do not publish an aggregate number without the raw JSON that produced it sitting in the same commit.
- **The linter's scope must be stated as a ceiling, not a verdict**, in its own docstring and in `RESULTS.md`'s warnings section — for Proof First specifically: the linter can proxy for sentence length, hedges, and keyword presence, but it **cannot** run the deletion test (a semantic judgment) or verify the MEDDICC "arms the champion" item (a judgment call) — those two things are why the judge pass is not optional here the way it is somewhat supplementary in the reference repo. Proof First's judge rubric is doing more real work than STE's, because two of its five constraint families (the deletion test and Integrity's "did this fabricate anything") are not mechanically checkable at all.

## Build Order

### Real Dependencies vs. Apparent Ones

| Apparent dependency | Why it looks true | What is actually true |
|---|---|---|
| "Evals can't start until SKILL.md is fully finished." | Evals embed SKILL.md's text in the skill-condition prompt. | Only `run_bench.py`'s generation step needs the *final* SKILL.md text. `scenarios.json` needs only the deal brief + the artifact-family list; `proof_lint.py` needs only the rule *concepts* (which countable proxies exist), not final wording or final numbers. Scenario-writing and deal-brief work should start in parallel with SKILL.md drafting, not after it. |
| "MEDDICC is part of the skill, so it depends on the prose catalog." | Both live under "the skill" conceptually. | MEDDICC is deliberately a separate audit with a separate namespace (`MC-#`) and zero content dependency on `PF-#`. It can be drafted first, in parallel, or last — order doesn't matter, only namespace non-collision does. |
| "README badges can use placeholder numbers, fill in later." | README is usually the last thing polished. | The badges *are* the evidence claim (PROJECT.md: "measured claims or no claims"). They have a hard dependency on the benchmark having actually run at least once. Treat this as a release gate, not a copy-editing task. |
| "output-styles/system-prompt.md are simple copies, do anytime." | They look like short summaries. | They are lossy compressions that must be **re-derived every time SKILL.md's rule content changes materially** — a recurring sync cost, not a one-time task. Schedule a "re-sync derivatives" step into every SKILL.md revision, not just the initial build. |
| "Numbering is a formatting detail, assign numbers once the catalog is written." | Numbers look cosmetic. | Reserved ranges must be decided *before* drafting rules in earnest, or the catalog gets numbered sequentially and later needs a renumbering pass that breaks the "stable across versions" goal on day one. Numbering is Phase 0/1 design work. |

### Suggested Phases

**Phase 0 — zero content dependencies, fully parallelizable:**
- `LICENSE`
- `NOTICES.md` (framework names + non-affiliation + paraphrase boundary — needs no rule content)
- `.claude-plugin/plugin.json` + `marketplace.json` (skeleton, final paths only)
- `examples/deal-brief.md` — highest-leverage early artifact; unblocks scenarios, before/after examples, and README copy
- Rule-numbering scheme itself (namespace prefixes + reserved ranges) — a design decision, not content

**Phase 1 — depends on Phase 0's deal brief + numbering scheme, otherwise parallelizable with each other:**
- `SKILL.md` — section skeleton first (which unblocks references), then full rule prose
- `references/meddicc-checklist.md` — independent of SKILL.md's prose content, needs only its own `MC-#` namespace agreed
- `references/artifact-patterns.md` — needs SKILL.md's *section outline* (which CotM elements exist) but not final rule wording, plus the deal brief for its own mini-examples
- `references/deletion-test.md` — needs the deletion-test rule's placement (`PF-3.x`) fixed, content itself parallelizable

The real dependency inside Phase 1 is "SKILL.md's section/numbering skeleton frozen," not "SKILL.md prose complete" — treat the skeleton freeze as the actual internal milestone, not full SKILL.md sign-off.

**Phase 2 — depends on Phase 1 content stabilizing:**
- `output-styles/proof-first.md` + `prompts/system-prompt.md` (condensations — author after, re-sync on every later change)
- `references/checklist.md` (exhaustive PF-rule audit pass — needs final numbers)
- `evals/scenarios.json` (needs deal brief + artifact-family list, not final rule wording — can actually start in Phase 1)
- `evals/proof_lint.py` (needs rule *concepts* frozen — the one component with a genuine hard content dependency on SKILL.md, same relationship `ste_lint.py` has to `SKILL.md` in the reference repo)
- `examples/before-after.md` (needs deal brief + stable rule catalog for real before/after pairs)

**Phase 3 — depends on Phase 2's tooling:**
- `evals/run_bench.py` full matrix run → `results/raw/*.json`
- Judge pass → `results/raw/*__judge__*.json`

**Phase 4 — depends on Phase 3's raw results:**
- `results/results.json` + `results/RESULTS.md` (generated)
- `README.md` finalized (badges sourced from `RESULTS.md`, all internal links pointed at final paths)

## Anti-Patterns

### Anti-Pattern 1: A Verdict-Only Buzzword Table

**What people do:** Turn the deletion test into a two-column "banned / allowed" table because it is easier to write and easier for a linter to check.
**Why it's wrong:** This recreates the exact maintained blocklist PROJECT.md explicitly rejects ("no maintained blocklist governs the skill itself"), and it gets the technical-noun/air-word boundary wrong in both directions the moment cloud vocabulary shifts (yesterday's "next-generation" is tomorrow's "agentic" — a static list is stale on arrival).
**Instead:** Keep the deletion test as the rule (one sentence, in SKILL.md), and make `references/deletion-test.md` teach the mechanism through worked pairs (term in a real sentence → same sentence with the term deleted → verdict and *why*), so a model applies the test to a term it has never seen before, not just to terms on a list.

### Anti-Pattern 2: Blending MEDDICC Into the Prose Catalog

**What people do:** Add "make sure the document names a metric" as `PF` rule sitting next to sentence-length rules, because it feels like it belongs in "the rules."
**Why it's wrong:** MEDDICC is a qualification/completeness lens, not a writing instruction — a document can satisfy every prose rule and still fail every MEDDICC item (well-written prose about the wrong things), and the reverse. Blending them produces, in PROJECT.md's own words, "a mushy catalog," and it also breaks the two-catalog-in-one-report property that check mode needs.
**Instead:** Keep `MC-#` in its own file with its own namespace, always audited as a second, explicitly separate pass in check mode.

### Anti-Pattern 3: Treating Artifact Type as a Third Mode

**What people do:** Build "RFP mode," "proposal mode," "exec-summary mode" as parallel top-level modes alongside write/check.
**Why it's wrong:** This multiplies every rule by four artifact types × two write/check states, producing 8+ nominal "modes" for a catalog where the actual rules do not change by artifact type — only the document *template* does. It also invites exactly the kind of per-artifact rule exceptions that make citations ambiguous ("does `PF-3.1` apply in exec-summary mode?" should never be a question that needs asking).
**Instead:** One classification step ("which artifact family"), selecting a template from `artifact-patterns.md`; two modes (write/check) layered orthogonally on top, exactly mirroring STE's own procedural/descriptive classification-vs-mode split.

### Anti-Pattern 4: Letting the Linter's Existence Imply the Deletion Test Is Mechanically Verified

**What people do:** Ship a regex-based buzzword counter in `proof_lint.py` and let the README imply "the skill enforces the deletion test" without restating that the linter only proxies for it.
**Why it's wrong:** This is precisely the failure PROJECT.md's evidence constraint exists to prevent — a claim the repo cannot back up mechanically, stated as if it were mechanical. STE avoids this failure only because its own linter docstring and `RESULTS.md` both restate the ceiling explicitly, every time.
**Instead:** Carry the "honest number warnings" pattern forward verbatim in spirit: state in the linter's own docstring, and in `RESULTS.md`, that buzzword/proxy counts are illustrative correlates and that the deletion test itself is a judgment call the linter cannot execute — matching the same posture STE takes toward its own "not a compliance verdict."

## Integration Points

### Cross-File Reference Contract

| From | To | What must stay in sync |
|---|---|---|
| `SKILL.md` (Opening/CotM/Integrity/Buzzword/Mechanics sections) | `references/checklist.md` | Every `PF-#` cited in SKILL.md must appear in the checklist; the checklist must never invent a number SKILL.md doesn't define |
| `SKILL.md` (buzzword rule) | `references/deletion-test.md` | The rule statement in SKILL.md and the worked examples in the reference must describe the same test, in the same words for the test itself |
| `SKILL.md` (artifact classification step) | `references/artifact-patterns.md` | The four named artifact families in SKILL.md's classification step must exactly match the four templates in the reference file — no fifth family introduced only in one place |
| `examples/deal-brief.md` | `evals/scenarios.json`, `examples/before-after.md`, `README.md` | All deal facts (dollar figures, competitor names, timeline, roles) must be pulled from the brief, never independently invented per file |
| `evals/results/RESULTS.md` | `README.md` badges | Every number in a README badge must be traceable to a line in `RESULTS.md`, which must in turn be traceable to `results/raw/*.json` |
| `NOTICES.md` | SKILL.md header, `references/meddicc-checklist.md` header, README | Each framework-touching file carries a one-line pointer to `NOTICES.md`, never a restated disclaimer |

### External Dependencies

| Dependency | Integration pattern | Notes |
|---|---|---|
| Agent Skills standard (`agentskills.io`) | SKILL.md frontmatter conformance (`name`, `description`, `license`, `compatibility`) | Same conformance target as the reference repo — verify against current spec at build time, not assumed from memory |
| Claude Code plugin marketplace | `.claude-plugin/{plugin.json,marketplace.json}` | Zero content coupling to skill internals beyond paths |
| Claude Code CLI (`claude -p ... --output-format json`) | `evals/run_bench.py`'s `call_claude()` | Requires a logged-in CLI, no API key — same reproduction path the reference repo documents; if Proof First's benchmark also targets non-Claude models (mirroring the reference repo's separate Pi cross-check), keep that as an explicitly separate script/results tree (`results/<provider-run>/`), never merged into the primary Claude-only matrix |

## Sources

- Reference implementation, inspected directly: `~/.claude/plugins/marketplaces/simple-english/` (`AminBlg/SimpleEnglish` v1.3.0) — `skills/simple-english/SKILL.md`, `references/{checklist,word-swaps,use-cases}.md`, `evals/{ste_lint.py,run_bench.py,scenarios.json,pressure-tests.md,results/RESULTS.md}`, `.claude-plugin/{plugin,marketplace}.json`, `output-styles/simple-english.md`, `prompts/system-prompt.md`, `README.md` — all read in full for this research.
- `/Users/cymarechal/devoteam/devoteam/technical-presales/.planning/PROJECT.md` — settled decisions on the three-framework anchor, the deletion test, integrity, and evidence constraints.
- Anthropic, Agent Skills documentation and authoring guidance (progressive disclosure three-level model; SKILL.md body ceiling of ~5,000 tokens / under 500 lines; frontmatter budgeted at ~100 tokens) — [Claude Platform Docs: Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [The Complete Guide to Building Skills for Claude (Anthropic)](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf), [Extend Claude with skills — Claude Code Docs](https://code.claude.com/docs/en/skills).

---
*Architecture research for: Proof First (AI agent skill repository, presales writing)*
*Researched: 2026-09-10*
