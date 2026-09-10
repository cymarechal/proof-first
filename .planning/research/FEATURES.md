# Feature Research

**Domain:** AI agent skill for presales/technical-sales writing discipline (rule catalog + linter, modeled on SimpleEnglish/ASD-STE100)
**Researched:** 2026-09-10
**Confidence:** MEDIUM overall — framework mechanics are well corroborated across official and secondary sources; "AI slop in presales specifically" and exact RFP scoring weights are thinly documented and rated LOW individually (see Sources).

## The Central Design Tension, Addressed Directly

SimpleEnglish's closing line is "STE deletes persuasion by design." Proof First cannot copy that stance — it must **keep** persuasion and delete only the fake kind. That is not a softer version of the same rule; it is the opposite instinct, and the skill has to hold both without collapsing into either "flat is safe" or "persuasive is fine."

The resolution this research converges on, and that should govern every feature below:

**Persuasion in this domain is not achieved by adjectives, it is achieved by specificity.** A reframe of the buyer's problem (Challenger), a quantified metric attached to an outcome (Command of the Message), a named proof point with a customer and a number (Command of the Message), a paper-process detail that shows the writer knows this buyer's procurement reality (MEDDICC) — these are all *more* persuasive than "robust, seamless, best-of-breed," not less. STE deletes persuasion because in a maintenance manual, ambiguity kills someone and "vivid" language is a superlative with no operational referent. In a proposal, "vivid" language can be a real metric with a real source. So the skill's rule is not "reduce adjectives," it is "an adjective is illegal unless it is doing the job a noun, number, or name should do instead." Concretely: banning "robust" is not banning strength-claims, it is banning *unattributed* strength-claims — the fix is never "delete the claim," it is "attach the claim to a metric, a proof point, or a named capability, or delete it." This is the deletion test's real mechanism (see PROJECT.md) and it must be stated as a positive instruction (replace with evidence) as often as a negative one (delete), or the skill drifts toward SimpleEnglish's flatness by default, which PROJECT.md explicitly names as a failure mode ("Flat, STE-style prose is a failure mode here, not a goal").

This reframes several "features" below: the skill is not fundamentally a ban-list tool, it is an **evidence-attachment enforcement tool**. Every rule in the catalog should be checkable as: "does this claim have a metric, proof point, capability, or name attached — yes/no."

## Feature Landscape

### Table Stakes (Skill Fails Without These)

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Command of the Message rule spine, numbered | This is the writable/checkable backbone PROJECT.md commits to. Without numbered rules, check mode (which must cite "rule number, offending text, rewrite") has nothing to cite. | MEDIUM | Six load-bearing elements to operationalize as writing rules, each with a precise, checkable job (below). Paraphrase only — Force Management's material is proprietary/trademarked. |
| Deletion test as the buzzword rule | PROJECT.md names this as the governing rule; a blocklist gets both false-positives (kills real nouns like "zero trust") and false-negatives (misses new coinages) and needs endless maintenance. | LOW | One sentence of instruction: "if deleting the term changes the technical meaning, keep it; if the sentence survives, delete it or replace it with a metric/proof point/name." Needs the positive-replacement framing above, not just deletion. |
| Integrity / anti-fabrication section | The single highest-cost failure mode in this domain (see Anti-Features below) — models produce fabricated metrics, references, and benchmarks readily because the surrounding prose implies them. PROJECT.md names this as a first-class catalog section, not a footnote. | MEDIUM | Must specify exact behavior: when a number/name/certification is not supplied by the user, write a marked gap ("[CUSTOMER METRIC NEEDED]" or similar), never invent a plausible one. Needs a concrete "what counts as fabrication" list: percentages, dollar figures, named customers, benchmark comparisons, certifications, headcounts, uptime figures, analyst quotes. |
| MEDDICC-derived completeness audit, separate from prose rules | PROJECT.md is explicit that qualification rules must not govern sentences (category error) but are excellent as a document completeness checklist. Users need this in check mode as a distinct pass from line-level style violations. | MEDIUM | Translate each MEDDICC/MEDDPICC letter into a document-level yes/no test (see table below). This becomes its own reference file, mirroring SimpleEnglish's `checklist.md` as a distinct artifact from `word-swaps.md`. |
| Challenger opening rule (reframe before capability list) | PROJECT.md: "roughly its whole useful contribution to a writing skill," and "the highest-leverage structural rule for an executive summary." Only the opening-reframe portion is in scope — teach/tailor/take-control as a sales *conversation* methodology is out of scope. | LOW-MEDIUM | Operationalize as: does the opening paragraph name the buyer's problem/cost of inaction *before* any vendor capability appears? Checkable by paragraph-order inspection. The documented 6-step choreography (warmer → reframe → rational drowning → emotional impact → new way → solution) is a useful internal model for HOW to write the reframe even though only the reframe ships as a rule. |
| Self-contained prose mechanics (no dependency on simple-english) | PROJECT.md constraint: zero dependencies, one folder. Persuasive presales prose still needs baseline mechanics — sentence length discipline, active voice, one-fact-per-sentence — but these must be restated, not imported. | MEDIUM | Cannot cite ASD-STE100 rule numbers; needs its own compact mechanics section (a handful of rules, not 53) tuned for *persuasive* prose rather than procedural/descriptive prose. E.g., "lead each paragraph with the outcome, not the mechanism" is a presales-specific ordering rule that STE has no equivalent for. |
| Write mode | Baseline generative capability; the skill's primary purpose per PROJECT.md ("makes AI write"). | LOW | Follows the same structural pattern as simple-english's "Your Task" section: classify artifact type → apply rule catalog → run self-check before delivering. |
| Check mode with (rule number, offending text, compliant rewrite) format | PROJECT.md's Active requirements name this format explicitly, matching SimpleEnglish's proven convention. | MEDIUM | Needs the numbered rule catalog to exist first (dependency). Must also report MEDDICC completeness gaps and integrity violations in a *separate* section from prose rule violations — three different check types, one command. |
| Per-artifact conventions for the four named families | PROJECT.md requirements list these explicitly: RFP/RFI responses, solution proposals, executive summaries, demo/discovery material. | HIGH | Each has a different buyer-evaluation mode (compliance scoring vs. narrative persuasion vs. skim-read vs. live conversation prep) — genuinely different structural rules, not one rule set with light variation. See per-artifact detail below. |
| Trademark/non-affiliation disclosure for all three frameworks | Legal constraint in PROJECT.md: Force Management, Challenger Inc., MEDDIC vendors are all proprietary and trademarked. SimpleEnglish's posture (name them, paraphrase concepts, reproduce zero proprietary text, state non-affiliation) is the proven template for exactly this situation with one rights-holder; here it's three. | LOW | A short paragraph per framework, once, near the top of SKILL.md or in a dedicated section — not per-mention. |
| One shared fictional example deal across all worked examples | PROJECT.md requirement; mirrors SimpleEnglish's sqlpipe example running through everything. Keeps the repo vendor-neutral and makes rules mutually reinforcing rather than each rule illustrated by an unrelated snippet. | LOW | A fictional cloud migration deal (e.g., a mid-market retailer moving off on-prem to a hyperscaler) gives every artifact family, every framework element, and every buzzword example a shared cast of characters (economic buyer, champion, competitor, metric) to reference. |

### Command of the Message elements as writing rules (detail for the rule-spine table stakes item)

Paraphrased from public secondary sources (Force Management's own blog/site plus independent breakdowns — see Sources); no proprietary training content reproduced.

| Element | What it means | Writing rule it implies |
|---|---|---|
| Before scenario | The buyer's current state: its costs, risks, and friction, described in the buyer's terms, not the vendor's. | A document section (or opening paragraph) must state the buyer's current-state cost/risk *before* any vendor capability is introduced. This is the same instinct as the Challenger reframe — the two frameworks reinforce each other at the opening. |
| After scenario | The buyer's future state once the outcome is achieved, described as a business condition, not a product state. | The after-state must be phrased as a buyer outcome ("time-to-provision drops from weeks to hours"), not a vendor achievement ("our platform delivers X"). |
| Required Capabilities | The functional things a solution must do to close the Before→After gap — capability requirements, not a feature list of what the vendor happens to sell. | Every capability claim must trace to a stated buyer requirement. A capability with no corresponding Required-Capability antecedent is a feature dump, not an argument — this is the checkable form of "no capability lists with no customer problem attached" from the research question. |
| Metrics | The quantified measure the buyer will use to judge success. Force Management's stated position: a value claim without a metric is unverifiable and therefore unconvincing. | Any outcome claim ("faster," "more efficient," "reduces cost") must carry an adjacent number or be flagged as a gap. This is the single most checkable rule in the whole catalog — a linter proxy for it is trivial (superlative/comparative adjective with no number within N words). |
| Proof Points | Not a logo wall, not a bare metric — a short story: a named context, a specific number, delivered in a form the buyer recognizes as their own situation. | A proof point must contain three things to be legal: a recognizable context, a number, and (when real) a name or an honest placeholder. Fabricated versions of any of the three trip the integrity rule. |
| Differentiators | Two kinds: unique (capability only this vendor has) and comparative (a capability others also have, but this vendor executes measurably better). | A differentiator claim must declare which kind it is implicitly by its phrasing, and comparative differentiators require a measurable "better" (a number or named mechanism), not an adjective ("more advanced"). |
| Positive Business Outcomes (PBO) | The business-level result the buyer's own leadership cares about — revenue, risk, time, cost — distinct from the technical Required Capability that produces it. | Executive-facing sections (executive summary, top of proposal) must be written in PBO language; capability language belongs in the body/technical annex. This is a placement rule as much as a content rule, and it maps directly onto the per-artifact conventions below. |

**Sources for this table:** forcemanagement.com (vendor-official blog posts, definitional but not the proprietary training curriculum), cross-checked against four independent secondary breakdowns (Qwilr, Fullcast, Oliv.ai, Salespeople.co.uk). Confidence: MEDIUM (cross-checked, no single-source reliance, but all secondary sources are marketing/sales-enablement content rather than academic or standards-body material).

### MEDDICC/MEDDPICC as a document completeness checklist (detail for that table-stakes item)

The framework is a *qualification* methodology (used in a live sales conversation to judge deal health). PROJECT.md is explicit that governing sentences with it would be a category error. Translated into document-level yes/no tests instead:

| Letter | Conversational meaning | Document completeness test |
|---|---|---|
| Metrics | The quantified outcome the buyer expects. | Does the document name at least one metric the buyer itself would recognize as their success measure (not a vendor-chosen vanity metric)? |
| Economic Buyer | The person with budget authority and final say. | Does the document contain content written *for* that persona — a section, page, or paragraph pitched at business/financial language rather than only technical language? |
| Decision Criteria | The buyer's own stated technical/vendor/financial evaluation criteria. | Does the document's structure mirror the buyer's stated criteria (e.g., an RFP's own section headings), or does it impose the vendor's preferred narrative structure instead? |
| Decision Process | The buyer's internal approval sequence and stakeholders. | Does the document acknowledge the buyer's process (e.g., "for your security review," "for the architecture board") anywhere, or does it assume a single reader? |
| Paper Process | Legal, security, procurement steps to finalize a contract. | Does the document address (or explicitly flag as pending) the procurement/security/legal artifacts this buyer will require — SOC2, DPA, MSA terms, data-residency attestation? |
| Identify Pain | The pain identified, indicated, and implicated with the customer. | Does the document state the buyer's pain in the buyer's own words/context (this overlaps with Command of the Message's Before scenario and the Challenger reframe — the three frameworks converge hardest here) rather than a generic industry pain statement? |
| Champion | An internal advocate with power and credibility. | Does the document give the champion something usable in a meeting the vendor will not attend — a one-page summary, a slide, a quotable metric — or does it only work as a vendor-narrated pitch? |
| Competition | Understanding of and strategy against alternatives, including "do nothing." | Does the document address the status-quo/do-nothing alternative and, if named competitors are relevant, does it do so without disparagement (see Anti-Features)? |

This becomes its own reference file (mirroring SimpleEnglish's `checklist.md`), run as a document-level pass distinct from the sentence-level rule catalog. A document can pass every prose rule and fail most of this checklist — that is the design point PROJECT.md makes explicitly.

**Sources:** meddicc.com (official framework site), cross-checked against independent breakdowns (Zapier, HubSpot, Scratchpad, DemandFarm). Confidence: MEDIUM.

### Challenger opening structure (detail, opening-only per scope)

Publicly documented as a six-step choreography for a "commercial teaching pitch," of which only the reframe belongs in scope per the research question:

1. **The Warmer** — establish credibility and demonstrate understanding of the buyer's world (overlaps with Command of the Message's Before scenario and MEDDICC's Identify Pain).
2. **The Reframe** — connect the buyer's stated problem to a bigger, previously-unconsidered problem or opportunity. *This is the one rule in scope.*
3. Rational Drowning — quantify the cost of the status quo (out of scope as a standalone rule, but reinforces the Metrics rule above).
4. Emotional Impact — make the cost felt, not just counted (out of scope for a writing skill governed by evidence-attachment, and in tension with the anti-fabrication posture if pushed too far — flagged as a risk, not adopted).
5. A New Way — a vendor-neutral statement of how to think about solving the reframed problem (out of scope, but useful internal framing for how the reframe should read: the solution should not appear yet).
6. Your Solution — the vendor's answer, deliberately last (out of scope as a standalone rule, but reinforces the ordering constraint the opening rule implies: capabilities never precede the reframe).

**The actual rule the skill ships:** an executive summary or proposal opening must state the buyer's reframed problem before any vendor capability, product name, or "our platform" sentence appears. This is checkable by paragraph order.

**Sources:** challengerinc.com (official company blog, though the book/training IP itself is proprietary and not reproduced), cross-checked against independent summaries (Anaplan's public PDF summary, Forbes, pitchmonster). Confidence: MEDIUM.

### Differentiators (What Makes This Better Than a Prompt)

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Integrity as an enforced, checkable rule (not a disclaimer) | Any prompt can say "don't lie." The differentiator is making refusal the *default path with a specific output shape* — a marked gap placeholder — so the model has somewhere safe to go instead of inventing. This directly targets the highest-cost, highest-frequency failure mode research surfaced: fabricated metrics/references/benchmarks appearing readily because surrounding text implies them. | MEDIUM | Requires a defined "gap marker" convention (e.g., `[NEEDS: named reference customer with permission]`) used consistently across write mode and check mode, so check mode can also detect *silent* fabrication (a number with no traceable source) vs. properly marked gaps. |
| Evidence-attachment as the buzzword mechanism, not a blocklist | A prompt-based "avoid buzzwords" instruction degrades fast (models revert after a few paragraphs, and static blocklists miss context — "seamless" is fine describing a literal API seam, illegitimate describing a migration). The deletion test plus positive evidence-attachment framing is a durable, teachable rule that survives longer documents and doesn't need a maintained wordlist to work correctly. | MEDIUM | The linter (regex proxies) is necessarily an approximation of this judgment call, same as SimpleEnglish's linter is explicitly "not a compliance verdict." This gap must be stated honestly, mirroring SimpleEnglish's own linter docstring. |
| Three-framework structural discipline (spine / audit / opening) | A prompt can say "use MEDDIC" but blends qualification, articulation, and structure into one mush, which PROJECT.md calls out as the exact failure to avoid. Keeping the three frameworks in three distinct catalog roles is what makes the checklist genuinely different from "sound persuasive." | HIGH | This is the single hardest thing to get right and the reason a plain prompt underperforms: the frameworks have to compose without a writer needing to know sales methodology. The Before/After/Reframe/Identify-Pain overlap across all three frameworks (noted above) needs to be resolved into ONE opening instruction in the actual skill, not three redundant ones the writer has to reconcile. |
| Per-artifact structural conventions baked in | A generic writing prompt does not know that an RFP answer must mirror the buyer's own numbering, that an executive summary is read in isolation during shortlisting, or that discovery material needs a different rule set than a written proposal. Encoding this saves the user from re-explaining domain convention every time. | HIGH | Four artifact families, each needs its own reference file (mirroring SimpleEnglish's `use-cases.md` pattern) rather than one generic "adjust tone" instruction. |
| Deterministic linter with regex proxies for the qualitative rules | Enables the benchmark PROJECT.md commits to (violations-per-100-words, skill-on vs skill-off, multiple models) — a prompt alone cannot produce a reproducible measured claim. This is the credibility mechanism: "the repo makes measured claims or no claims." | HIGH | Direct analogue to SimpleEnglish's `ste_lint.py` — needs its own proxy set: unquantified superlative detection, claim-with-no-adjacent-number detection, hedge-word detection, vendor-centric-subject detection ("our platform enables" pattern), passive-voice rate, paragraph-order check for the opening-reframe rule. |
| Multi-model, blind-pairwise benchmark, published and reproducible | Differentiates from "a well-written prompt" the same way SimpleEnglish's 74.6%-fewer-violations and 45/56-pairwise numbers differentiate it. Directly required by PROJECT.md Active requirements. | HIGH | Needs a scenario set analogous to SimpleEnglish's `scenarios.json`, built around the one shared fictional deal, across the four artifact families. |
| Persuasion-preserving self-check | The self-check step cannot just be "did I remove buzzwords" (that produces flat text, an explicit anti-goal per PROJECT.md's Voice constraint). It must also check "did I attach evidence to every claim I kept" — a check for presence of the good thing, not just absence of the bad thing. | LOW-MEDIUM | This is a genuinely novel self-check step relative to SimpleEnglish's model (which only checks for absence of violations) — worth calling out explicitly in the roadmap as a distinguishing design element. |

### Anti-Features (Deliberately Not Built, With Reasoning)

| Feature | Why It Seems Appealing | Why Problematic | Alternative |
|---------|------------------------|------------------|-------------|
| Fabricating metrics, reference customers, benchmarks, or certifications | Models produce these fluently because the surrounding persuasive prose structurally implies a number/name should be there; refusing feels like it weakens the document. | Legal: research confirms RFP responses can become part of a binding contract, and misrepresentations there can create express-warranty and fraud liability (the EMC Corporation case — $87.5M settlement over procurement misrepresentation — is a documented instance; the U.S. False Claims Act requires only reckless disregard, not intent, to establish fraud). Reputational: a buyer who checks a fabricated reference or number and finds it false discounts the entire document, which is the exact trust-destroying failure PROJECT.md's Core Value is built to prevent. | Marked gap placeholders in the output, consistently formatted, that the human writer must fill in with real data — never a plausible-sounding invented substitute. |
| Naming or disparaging named competitors | Feels persuasive — direct comparison seems like the fastest way to look better. | Legal: commercial/product disparagement is a recognized form of defamation applied to businesses (false or misleading statements causing competitive/economic harm); comparative-advertising law requires claims to be substantiated, not just true-sounding. Professional: research on sales ethics is consistent that direct disparagement reads as insecurity, not strength, and that the stronger convention is framing evaluative questions the buyer can apply to any vendor ("what SLA do you offer for X") rather than naming names. | Comparative *criteria*, not comparative *competitors* — teach the writer to state the evaluation question, not the competitor's name. |
| Making commitments the writer cannot keep (SLAs, delivery dates, unconditional guarantees) | Sounds confident, and confident language is exactly what a slop-averse skill is trying to produce more of. | Same legal exposure as fabricated metrics — an RFP/proposal commitment can become a contractual warranty. A writing skill has no way to verify the writer's actual delivery capacity, so any generated commitment is a liability the skill cannot discharge. | Flag any commitment-shaped sentence ("we will deliver X by Y", "we guarantee Z") for explicit human sign-off rather than generating it as settled prose; where the user supplies the commitment, keep it exactly as given rather than "improving" its confidence level. |
| Producing pricing, sizing, or commercial modelling | Adjacent and tempting to bundle — a "complete" proposal skill feels like it should include the numbers. | Explicitly out of scope in PROJECT.md ("the skill writes about numbers, it does not produce them"). Pricing is a business decision requiring current rate cards, margin targets, and deal-specific approvals a text skill has no access to and no business being involved in. | The skill writes the surrounding narrative and leaves a clearly marked slot for pricing the human supplies. |
| Replacing human review before bid submission | Tempting because the whole pitch of the skill is "the AI writes it well now." | Full automation-of-submission removes exactly the check the integrity rule depends on (a human confirming that flagged gaps got filled with true information, not just plausible information) and PROJECT.md's Out of Scope already excludes "verifying that the writer's inputs are true" — the skill cannot fact-check, so it cannot be the last gate either. | Position check mode explicitly as a pre-submission audit *for* the human reviewer, not a replacement of the reviewer — the SimpleEnglish precedent ("no tool can guarantee compliance... final approval rests with the writer") is the exact posture to copy. |
| A maintained buzzword blocklist as the enforcement mechanism | Feels more reliable/deterministic than a semantic judgment call, and easier to build a linter against. | PROJECT.md is explicit this is wrong in both directions: kills real technical nouns ("zero trust," "landing zone" would false-positive on naive lists) and needs endless maintenance as new coinages appear. It also cannot be "the rule" — the deletion test already is the rule; a blocklist is at most a linter proxy. | Ship the deletion test as the taught rule; ship a *labeled-as-approximate* buzzword inventory only inside linter tooling/documentation, explicitly not as the SKILL.md rule itself (matches PROJECT.md's explicit instruction). |
| Blending MEDDICC into the sentence-level prose rules | Seems efficient — one unified rulebook instead of three artifacts. | PROJECT.md calls this out directly as a category error: MEDDICC governs deal qualification, not sentence construction; forcing it to grade prose would produce, per PROJECT.md, "a mushy catalog." | Keep MEDDICC as a separate document-completeness pass (its own reference file and its own check-mode output section), never merged into the prose rule numbering. |
| Full teach/tailor/take-control Challenger conversational methodology | Tempting since Challenger is already an anchor framework — why not use all of it? | Out of scope per PROJECT.md and the research question: "Tailor" and "Take Control" describe live conversational tactics (adapting to stakeholder type, redirecting a sales conversation) that have no written-document analogue and would pull the skill toward being a sales-training tool rather than a writing-discipline tool. | Only the opening-reframe sequence ships as a rule; the rest of Challenger stays outside scope, same boundary PROJECT.md draws. |

## Per-Artifact Conventions (Detail for the Table-Stakes "Per-Artifact" Feature)

| Artifact | What the buyer actually evaluates | Standard structure / convention | Framework mapping |
|---|---|---|---|
| **RFP/RFI response** | Scored, weighted evaluation against stated criteria — research indicates typical weight bands of roughly technical approach/capability 30-40%, cost/value 20-25%, experience/references 15-20%, security/compliance 10-15%, implementation approach 10-15% (bands vary by buyer; treat as illustrative, not a rule to encode as fact). Compliance is a mechanical pass/fail gate checked before scoring even begins; **responsiveness** (how well an answer actually addresses what was asked) is where deals are won or lost during scoring itself — this is the compliance-vs-value distinction the research question named. | Mirror the buyer's own numbering, terminology, and requested tables exactly — evaluators use the RFP's structure as their scoring rubric, and a reorganized response forces "hunting," which is penalized even if the content is equivalent. Answer-first ordering within each response: direct answer first, only the necessary supporting detail, then evidence/proof point — repeat the requirement ID and a short form of the buyer's own wording per answer. A compliance matrix (requirement → response location → owner) is the standard cross-reference artifact. The executive summary is frequently read in isolation during shortlisting — it must independently prove buyer-specific understanding, not just summarize what follows. | Command of the Message's Required Capabilities/Metrics/Proof Points map almost directly onto individual scored requirement responses. MEDDICC's Decision Criteria and Paper Process map onto compliance-matrix completeness and procurement/legal answers respectively. |
| **Solution proposal** | Narrative persuasion under less rigid structure than an RFP — the buyer is judging both the solution's fit and (implicitly) whether the vendor understood them, since there's no fixed question list forcing that proof. | Before/After framing at the top (Command of the Message), required capabilities mapped to the buyer's stated needs in the body, proof points and differentiators supporting the recommendation, PBOs stated in business language near the top and again at the close. | This is the artifact where Command of the Message maps most cleanly end-to-end — it is close to a proposal outline already, which is exactly why PROJECT.md calls it the rule spine. |
| **Executive summary** | Read by the Economic Buyer (MEDDICC) who has the least time and the least patience for capability lists — evaluates whether the vendor understood the business problem and the outcome, not the mechanism. Often the ONLY section some stakeholders read. | Challenger's reframe opens it — buyer's problem restated in a way that shows new understanding, before any vendor name or capability appears. PBO language throughout, not Required-Capability language (that belongs in the body/technical annex). Short: this is a skim-read artifact, not a reference document. | Challenger (opening rule) + Command of the Message PBOs are the dominant frameworks here; MEDDICC's Economic Buyer persona-check applies directly. |
| **Demo/discovery material** | Different technical evaluators care about different things in the same room — research is consistent that technical evaluators care about integration/security, economic buyers care about ROI/risk, end users care about daily workflow; "the buyer" is not one persona reading one document. Quality of a demo is bounded by the quality of pre-demo intelligence gathered in discovery. | Not a single linear document — needs persona-tagged sections or a briefing structure that different roles can be pointed to selectively, plus discovery question sets organized around uncovering MEDDICC gaps (metrics, economic buyer, pain, decision process) rather than a generic feature-tour script. | MEDDICC's Identify Pain and Decision Process elements are discovery's actual job; the write-mode output here looks more like a structured briefing/question-prep document than "prose," which the skill needs to accommodate as a distinct output shape. |

## Check-Mode Requirements Beyond the Reference Pattern

SimpleEnglish's check mode reports (rule number, offending text, compliant rewrite) for line-level violations against one flat catalog. This domain needs check mode to do more, because PROJECT.md establishes three distinct kinds of failure that don't share a numbering scheme:

1. **Prose rule violations** (Command-of-the-Message-derived catalog + evidence-attachment/deletion-test rules) — reported exactly like SimpleEnglish: rule number, offending text, compliant rewrite.
2. **MEDDICC completeness gaps** — not a sentence-level violation; reported as a checklist pass/fail per letter, with the specific missing element named (e.g., "no content addresses Paper Process — no mention of security/compliance requirements"). This needs its own section in the check-mode report, structurally separate from prose violations, per PROJECT.md's explicit instruction that MEDDICC must stay "separate from the prose rules."
3. **Integrity flags** — a third category: claims that look unverifiable (an unattributed number, an unnamed "leading customer," a benchmark with no source) that check mode should surface as "flag for human verification" rather than a violation to silently fix, since check mode cannot know if the underlying claim is true — only the human reviewer can confirm that (consistent with PROJECT.md's Out of Scope: "verifying that the writer's inputs are true").
4. **Structural/ordering checks** — the Challenger opening rule and the per-artifact structure conventions are checked by document *position*, not by sentence content — check mode needs a pass that looks at paragraph order and section placement, not just individual sentences.
5. **A closing disclaimer**, mirroring SimpleEnglish's own ("no tool can guarantee compliance... final approval rests with the writer"), stated once at the end of a check-mode report for this domain: no tool can guarantee that a document will win a deal or that its claims are true — it audits form, not truth.

## Feature Dependencies

```
Command of the Message rule spine (numbered)
    └──requires──> Nothing (foundational; built first)

Deletion test / evidence-attachment framing
    └──enhances──> Command of the Message rule spine (gives the Metrics/Proof-Points rules their enforcement mechanism)

MEDDICC completeness checklist
    └──requires──> Nothing directly, but is written AFTER the rule spine exists,
                     so its "separate from prose rules" boundary has something to be separate FROM

Challenger opening rule
    └──requires──> Command of the Message Before-scenario rule
                       (the two overlap; the skill must resolve them into ONE opening instruction,
                        not ship redundant/conflicting guidance)

Integrity / anti-fabrication section
    └──requires──> Command of the Message Metrics + Proof Points rules
                       (integrity is the enforcement backstop for exactly those two elements —
                        it defines what to do when the metric/proof point is not supplied)

Per-artifact conventions (RFP, proposal, exec summary, demo/discovery)
    └──requires──> Rule spine + MEDDICC checklist + Challenger opening rule
                       (each artifact file applies all three; cannot be written first)

Check mode (three-category report + structural pass)
    └──requires──> Rule spine (for category 1)
    └──requires──> MEDDICC checklist (for category 2)
    └──requires──> Integrity section (for category 3)
    └──requires──> Challenger opening rule + per-artifact conventions (for category 4/structural pass)

Deterministic linter (regex proxies)
    └──requires──> Rule spine + buzzword deletion-test framing
                       (proxies approximate the semantic judgment call the rule spine defines)

Multi-model benchmark + blind pairwise judge
    └──requires──> Linter (for violation counts)
    └──requires──> Per-artifact conventions + shared fictional deal (for scenario set)

One shared fictional deal (used across all examples)
    └──enhances──> Every rule and every artifact file
                       (not a hard dependency, but should exist before worked examples are written,
                        or examples will be written ad hoc and need retrofitting)
```

### Dependency Notes

- **Challenger opening requires Command of the Message Before-scenario:** both frameworks independently produce "state the buyer's problem before the vendor's capability," and MEDDICC's Identify Pain converges on the same instinct. Shipping three separate rules that say almost the same thing is the "mushy catalog" PROJECT.md warns against. The roadmap should treat this convergence as a single design decision: one opening rule, sourced from three frameworks, stated once.
- **Integrity requires Metrics + Proof Points:** the integrity section is not a standalone ethics statement, it is the specific behavior for what happens when those two Command-of-the-Message elements have no real data to attach — this is why PROJECT.md calls integrity a natural consequence of the same pressure that makes the rule spine necessary.
- **Per-artifact conventions require all three frameworks to exist first:** each artifact file is really "how do the rule spine, the MEDDICC checklist, and the opening rule apply differently to this format" — writing artifact conventions before the frameworks are settled would mean rewriting them once the frameworks land.
- **Benchmark requires linter and artifact conventions and the shared fictional deal:** this is the same order dependency SimpleEnglish's own repo shows (`ste_lint.py` and `scenarios.json` both post-date the rule catalog) — the roadmap should sequence the eval harness as a later phase, not parallel to rule-catalog development.

## MVP Definition

### Launch With (v1)

- [ ] Command of the Message rule spine, numbered, with the evidence-attachment/deletion-test framing built in from the start — this is the whole point of the skill; nothing else works without it
- [ ] Integrity/anti-fabrication section — the highest-cost failure mode; cannot be deferred, must ship in v1 per PROJECT.md
- [ ] MEDDICC completeness checklist (separate reference file) — required for the "document can be well-written and still incomplete" value proposition PROJECT.md names
- [ ] Challenger opening rule, resolved into one opening instruction alongside the Before-scenario/Identify-Pain overlap — essential for the executive-summary and proposal artifact families
- [ ] Self-contained prose mechanics (no simple-english dependency) — required by the zero-dependency constraint
- [ ] Write mode + check mode (three-category report: prose / MEDDICC / integrity, plus structural pass) — both modes are named as Active requirements in PROJECT.md, not deferred
- [ ] Per-artifact conventions for all four families — PROJECT.md lists all four as Active requirements for v1, not phased
- [ ] One shared fictional deal used across every example
- [ ] Trademark/non-affiliation disclosure

### Add After Validation (v1.x)

- [ ] Deterministic linter with regex proxies — PROJECT.md wants this in v1 for the benchmark claim, but if timeline pressure hits, the rule catalog + check mode can ship and be manually validated first, with the linter following once the rule set has stabilized (a linter built against rules that are still changing is wasted work)
- [ ] Refinements to the buzzword-proxy inventory in linter tooling, once real usage surfaces new patterns the deletion test misses

### Future Consideration (v2+)

- [ ] Additional artifact families beyond the four named (e.g., SOW/statement-of-work narrative sections, vendor security questionnaires) — defer until the four core families are validated in the wild
- [ ] Localization/non-English variants of the rule catalog — defer until English-language adoption validates the approach at all
- [ ] Any expansion toward "Tailor"/"Take Control" Challenger conversational guidance — explicitly out of scope per PROJECT.md, would need a full re-scoping discussion, not a v2 feature add

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|----------------------|----------|
| Command of the Message rule spine | HIGH | MEDIUM | P1 |
| Integrity / anti-fabrication section | HIGH | MEDIUM | P1 |
| Deletion test + evidence-attachment framing | HIGH | LOW | P1 |
| MEDDICC completeness checklist | HIGH | MEDIUM | P1 |
| Challenger opening rule (resolved, not redundant) | HIGH | LOW-MEDIUM | P1 |
| Check mode (three-category + structural pass) | HIGH | MEDIUM | P1 |
| Per-artifact conventions (all four) | HIGH | HIGH | P1 |
| Self-contained prose mechanics | MEDIUM | MEDIUM | P1 |
| Shared fictional example deal | MEDIUM | LOW | P1 |
| Deterministic linter | MEDIUM | HIGH | P2 |
| Multi-model benchmark + pairwise judge | MEDIUM | HIGH | P2 |
| Additional artifact families beyond the four | LOW | HIGH | P3 |

## Sources

**Command of the Message:** [forcemanagement.com — Command of the Message glossary/blog](https://www.forcemanagement.com/blog/3-simple-metrics-to-validate-command-of-the-message-success) (vendor-official, definitional content only); cross-checked against [Qwilr](https://qwilr.com/blog/command-of-the-message/), [Fullcast](https://www.fullcast.com/content/command-of-the-message-sales-methodology/), [Oliv.ai](https://www.oliv.ai/blog/command-of-the-message), [Salespeople.co.uk](https://www.salespeople.co.uk/explained/force-management-command-of-message-deep-dive). Confidence: MEDIUM.

**MEDDICC/MEDDPICC:** [meddicc.com](https://meddicc.com/meddpicc-sales-methodology-and-process) (official framework site); cross-checked against [Zapier](https://zapier.com/blog/meddpicc/), [HubSpot](https://blog.hubspot.com/sales/meddpicc-methodology), [Scratchpad](https://www.scratchpad.com/blog/meddpicc), [DemandFarm](https://www.demandfarm.com/blog/meddpicc-sales-methodology/). Confidence: MEDIUM.

**Challenger commercial-teaching pitch:** [Challenger Inc. official blog](https://challengerinc.com/blog/commerical-teaching-and-storytelling/); cross-checked against an independent public PDF summary ([Anaplan](https://www.anaplan.com/content/dam/anaplan/wp-content/uploads/2016/02/Challenger-Sale-Summarized.pdf)), [Forbes](https://www.forbes.com/sites/propointgraphics/2015/04/17/present-like-a-challenger/), [pitchmonster.io](https://www.pitchmonster.io/blog/challenger-sale-methodology). The book/training curriculum itself is proprietary and was not read or reproduced; only public secondary descriptions were used. Confidence: MEDIUM.

**AI slop in sales/proposal writing:** [Merritt Group](https://www.merrittgrp.com/mg-blog/avoid-ai-slop-guide-for-marketers-and-pr/), [Spike AI](https://getspike.ai/blog/how-to-avoid-ai-slop/), [ingeniotech "Workslop"](https://www.ingeniotech.co.uk/ai-slop-business-writing/), [seo.com](https://www.seo.com/blog/ai-slop/). This area is thinly documented specifically for *presales* writing (most sources address marketing/blog content generally); presales-specific failure patterns in this file are partly inferred by combining the general AI-slop literature with the Command of the Message / MEDDICC frameworks rather than found as a named "presales AI slop" literature. Confidence: LOW — flagged as a research gap below.

**RFP scoring, compliance vs. responsiveness, structure conventions:** [Inventive.ai RFP evaluation criteria guide](https://www.inventive.ai/blog-posts/rfp-evaluation-criteria-best-practices), [RocketDocs](https://rocketdocs.com/resources/blog/rfp-evaluation-criteria-guide), [rfpschoolwatch compliance matrix](https://www.rfpschoolwatch.com/rfp/blog/compliance-matrix-mastery-scoring-higher-on-technical-evaluations-part-2/), [thewrite-direction.com](https://www.thewrite-direction.com/blog/what-is-an-rfp-response/). Scoring weight bands are illustrative aggregates from vendor/consultancy blog content, not a standards body — treat as directional, not authoritative. Confidence: LOW-MEDIUM.

**Cloud/enterprise technical nouns (load-bearing side of the buzzword inventory):** [Google Cloud landing zone docs](https://docs.cloud.google.com/architecture/landing-zones), [Microsoft Cloud Adoption Framework — Zero Trust](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/security-zero-trust), [AWS Builder Center — cloud ops/security architecture](https://builder.aws.com/content/36ITqdzASweW7izRZG7WExLyV16/cloud-ops-and-security-architecture-explained-iam-vpc-zero-trust-monitoring-and-compliance). These are primary vendor documentation, the highest-confidence tier available for this file. Confidence: MEDIUM-HIGH.

**Generic business-jargon inventory (pure-air side):** [Straight North — 150 Business Jargon Fixes](https://www.straightnorth.com/blog/150-business-jargon-fixes/), [Husson University](https://www.husson.edu/online/blog/2022/06/business-buzzwords-and-corporate-lingo-you-must-eliminate), [Rice Business "Words to the Wise"](https://business.rice.edu/wisdom/word-watch/business-jargon-how-optimize-verbiage-robust-value-add-or-how-not-communicate), [Atlassian](https://www.atlassian.com/blog/teamwork/6-examples-of-business-jargon-you-should-stop-using-now). Confidence: LOW-MEDIUM (general business-writing advice, not domain-specific to cloud/enterprise tech, but directly corroborates PROJECT.md's own named examples — synergy, best-of-breed, seamless, robust).

**Legal reasoning for anti-features:** [Win Without Pitching — legal implications of issuing an RFP](https://www.winwithoutpitching.com/legal-implications-of-issuing-rfp/), [Dentons — nuts and bolts of RFPs](https://www.dentons.com/-/media/pdfs/insights/2013/may/understanding-the-nuts-and-bolts-of-requests-for-proposals-rfps.pdf), [Flowcase — managing case studies for RFPs](https://www.flowcase.com/blog/how-to-manage-case-studies-for-rfps-a-complete-guide-for-2026/), [Bona Law — false advertising/fake reviews](https://www.bonalaw.com/insights/legal-resources/can-you-sue-for-false-advertising-over-fake-reviews-and-rigged-ratings), [Carroll Firm — commercial disparagement](https://www.carroll-firm.com/how-to-sue-a-competitor-for-commercial-disparagement/), [Aaron Hall — comparative advertising legal pitfalls](https://aaronhall.com/comparative-advertising-legal-pitfalls-you-should-avoid/), [gzconsulting — don't disparage your competitors](https://gzconsulting.org/2018/07/26/dont-disparage-your-competitors/). The EMC Corporation $87.5M procurement-misrepresentation figure and the False-Claims-Act reckless-disregard standard appear via the Dentons/legal-briefing material; treat as a documented example of the risk category rather than a rule to cite verbatim in the skill itself. Confidence: MEDIUM (legal-practice sources, not primary case law reviewed directly).

**Demo/discovery best practices:** [Vivun — technical discovery best practices](https://www.vivun.com/blog/technical-discovery-best-practices-a-guide-to-better-sales-conversations), [Guideflow — sales engineering demo practices](https://www.guideflow.com/blog/sales-engineering-demo-best-practices), [Storylane — sales discovery call guide](https://www.storylane.io/blog/what-is-sales-demo-discovery). Confidence: LOW-MEDIUM (sales-enablement blog content, consistent across sources but not independently verified against a named methodology).

**Reference implementation studied directly:** `simple-english` skill and its `references/use-cases.md`, `references/word-swaps.md`, `references/checklist.md`, and `examples/before-after.md`, read in full from the local plugin marketplace checkout at `/Users/cymarechal/devoteam/.claude/plugins/marketplaces/simple-english/`. This is the structural template this file's recommendations are built to fit alongside, per the assignment's explicit instruction.

## Research Gaps

- **"AI slop in presales writing" as a distinctly named, documented failure pattern is thin.** The general AI-slop literature (marketing/blog-content focused) was combined with the Command-of-the-Message/MEDDICC frameworks to infer presales-specific failure patterns (capability lists with no Required-Capability antecedent, PBO-free openings, unattributed metrics). This inference is reasonable given the frameworks, but it is not independently sourced from presales-specific case studies or practitioner post-mortems, and the roadmap should treat the exact wording of "before/after slop examples" as something to build and test empirically (the benchmark scenario set) rather than assume from this research alone.
- **Exact RFP scoring weight percentages are aggregated from vendor-blog content, not a standards body or buyer-side procurement survey** — use them as directional (technical approach and cost dominate; compliance/security is a real but smaller scored component) rather than as numbers to encode literally into any rule.
- **No public, named "MEDDICC-for-written-documents" precedent was found** — the completeness-checklist translation in this file is this research's own synthesis of the qualification framework applied to a document rather than a documented existing practice, and should be validated with actual presales practitioners during requirements definition, not treated as an established convention.

---
*Feature research for: AI agent skill for presales/technical-sales writing discipline*
*Researched: 2026-09-10*
