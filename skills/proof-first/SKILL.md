---
name: proof-first
description: |
  Write or check RFP and RFI responses, solution proposals, executive
  summaries, and demo or discovery documents for technical presales and
  bid teams. Use for a scored technical response, a customer-facing
  proposal, or a check pass over a finished draft that flags invented
  metrics, missing evidence, undisclosed customer references, competitor
  comparisons, compliance claims, and unquantified buzzwords before the
  document ships to a buyer.
license: MIT
metadata:
  version: "0.1.0"
---

# Proof First

A technical evaluator finishes the document believing the author genuinely understands their problem — because complex things were made simple without being made wrong. This catalog exists so persuasion survives without ever costing technical accuracy: every claim carries its evidence or carries a visible marker instead, and every buzzword is tested rather than guessed at.

Concepts here are paraphrased from publicly described sales frameworks. Not affiliated with or endorsed by any framework rights-holder. See NOTICES.md.

## Your task

Select a mode before drafting or reviewing anything:

- **Write mode** — the request asks for new or revised presales prose (an RFP/RFI answer, a proposal section, an executive summary, demo or discovery material).
- **Check mode** — the request asks you to review an existing draft.

Apply the rule catalog below in either mode. Cite only rule numbers defined in this file or listed in `references/checklist.md`; never a number recalled from memory, and never a number outside the stated total below. An invented rule number is a worse failure than no citation at all. In either mode, no rule ID is cited and no finding is reported before the artifact family is named.

This catalog contains 31 rules in 6 numbered sections.

## Marker vocabulary

When a rule requires marking rather than silently omitting or silently complying, use exactly one of these three bracket forms. The rule number that raised the marker always comes first inside the bracket:

- `[<rule> GAP: what is missing]` — an evidence gap: a claim that needed a number, a source, or a fact that was not supplied or measured. See PF-2.11 below for a worked instance.
- `[<rule> REVIEW (<one of the four categories below>): what needs confirming]` — a flag needing human confirmation before the document ships. The four categories are exactly `commitment`, `reference`, `competitor`, and `compliance` — see PF-2.14 through PF-2.17 below.
- `[<rule>: customer's term, retained — source]` — a customer-verbatim term that the deletion test would otherwise remove, kept and marked instead.

In every form, `<rule>` is the ID of the rule that raised the marker — never omitted, never a number invented for the occasion.

Every marker produced in a document is also listed, once drafting is complete, in a trailing register under the heading `## Unresolved before this document is sent`.

## Reference files

- Before applying the deletion test to a compound term, or to any term appearing in the customer's own supplied source material, read `references/deletion-test.md`.
- Before emitting any rule citation in check mode, read `references/checklist.md`.
- Before writing or checking a ✗/✓ contrast for a rule, read `references/worked-examples.md`.
- Before running a document-level completeness audit, or before reporting a completeness gap in check mode, read `references/completeness-audit.md`.
- Before classifying a document into an artifact family, or before applying that family's conventions, read `references/artifact-patterns.md`.

## PF-0 — Opening and reframe

### PF-0.1 — The opening reframe

Open by restating the buyer's own situation, in words they have already used, before naming any product, vendor, or capability. A reframe names what the current state costs the buyer and states the shift this document proposes, in one paragraph making one point. A reframe opening with a capability list, or split across several sentences each adding a qualifying condition, does not satisfy this rule — the resolution must read as one instruction applied once, not several to reconcile.

**Replace with:** the buyer's own words for their current state and cost, never the vendor's name for what it sells.

## PF-1 — Structure

The Command of the Message spine is carved into seven sub-blocks, each reserved four IDs: Before scenario, After scenario, Required Capabilities, Metrics, Proof Points, Differentiators, and Positive Business Outcomes. A sub-block with no rule in this version is intentional headroom for a later minor version, not an omission.

### PF-1.1 — Name the current state in the buyer's own terms

Describe the before state in the buyer's own words about their estate, never in the vendor's category language. A before state speaking only the vendor's taxonomy has named nothing the buyer will recognize.

**Replace with:** the buyer's own phrasing from supplied source material, or the concrete system or process actually named.

### PF-1.2 — Name what the current state costs

A before state with no stated cost is scene-setting, not a case for change. Name the cost the buyer already states, never one invented to sound significant.

**Replace with:** the run-rate figure, process, or rollout the buyer already named — or a gap marker if never quantified.

### PF-1.5 — State the after-state as an observable change, paired with its before

An after state ships next to the before state it replaces, so the contrast is visible on the page, not left for the reader to reconstruct. A later rule in this catalog's Consistency and Voice section makes this pairing a checkable requirement, not only a style preference.

**Replace with:** the paired form — before and after in the same sentence or pair of sentences.

### PF-1.9 — State the capability the buyer needs, not the product that has it

State the capability as what the buyer must be able to do. A product name enters only afterward, as the means of delivering it — never as the sentence's subject.

**Replace with:** capability stated first, product named second as the means.

### PF-1.13 — Name the measure and its current baseline

A metric with no baseline is a target, not a metric. Name the buyer's own stated figure, or state plainly that it has never been captured.

**Replace with:** the buyer's own stated figure, or a gap marker naming what would need measuring.

### PF-1.14 — Name where the baseline came from

A baseline with no stated provenance cannot be checked. Name the source — the buyer's own figure, a named measurement, or the document it came from.

**Replace with:** the attribution — who stated it, or what document it came from.

### PF-1.17 — Attach one comparable, verifiable proof to each capability claim

One named, checkable comparable beats three unnamed ones. A capability claim with no attached proof is an assertion, not evidence.

**Replace with:** a comparable this vendor can actually produce, or a gap marker naming the missing proof.

### PF-1.21 — Claim a differentiator only where a named alternative cannot do it

A differentiator every bidder could also claim is a feature, not a differentiator. A claim about what a named rival cannot do is an integrity matter this catalog's Proof and Integrity section addresses separately — restate it as what this vendor does, evidenced, without asserting what a rival cannot do. A comparison naming a rival carries a `REVIEW (competitor)` marker.

**Replace with:** the claim restated as an evidenced statement of vendor capability.

### PF-1.25 — Tie the outcome to the stated priority of the person who owns it

An outcome is addressed to the person measured on it, in the terms they used — not to "the organization" in the abstract.

**Replace with:** the role, named, and the priority that role stated in their own words.

## PF-2 — Proof and integrity

This section is carved into two sub-blocks: Proof rules attach evidence to a claim and name where that evidence came from; Integrity rules refuse two classes of fabrication and flag four presales hazards for a human to confirm. A rule added later to one sub-block must not land inside the other's reserved range.

### PF-2.1 — Every claim carries its evidence

A sentence asserting something about the customer's estate, the vendor's capability, or an outcome carries its evidence in the same sentence or the next.

**Replace with:** the customer's stated figure, a named artefact the reader could ask for, or a `GAP` marker.

### PF-2.2 — Name the source of the evidence

Evidence with no named source is an assertion wearing a number. Name the source inline — the person, document, or measurement that produced it.

**Replace with:** the source stated by name; "industry data" is not a source.

### PF-2.3 — Adjacent evidence licenses an unhedged claim

A claim whose evidence sits in the same or next sentence is written flat and confident, with no hedge. Hedging never repairs missing evidence.

**Replace with:** strip the hedge from an evidenced claim; send an unevidenced one to `PF-2.4`.

### PF-2.4 — No evidence: cut the claim and mark the gap in its place

When no evidence exists, the claim is cut and a `GAP` marker takes its place — the omission stays visible where the claim would have been, not only in the register. The marker's rule token lets a check report cite an integrity finding exactly as a prose violation.

**Replace with:** `[PF-2.4 GAP: what is missing — why it is missing]`.

### PF-2.11 — Never invent a metric, a baseline, or a benchmark number

Refuse to state a percentage, a duration, a dollar figure, or a rate not supplied by the customer or measured and given as fact. When a measure exists in the buyer's words but its baseline was never captured, say so instead of estimating to sound confident.

**Replace with:** the customer's own stated figure, or a gap marker naming what would need measuring.

### PF-2.12 — Never invent a reference customer, a logo, or a named account

Refuse to name a client, logo, or account as a reference unless the writer supplied it as fact. A named party invented to sound like a proof point is a fabrication the reader cannot detect until they ask.

**Replace with:** the true part of the sentence, with a `GAP` marker replacing the named reference — never an anonymised stand-in.

### PF-2.13 — An absence found by the additive sweep is marked like any other gap

The additive sweep specified later checks for a missing differentiator, baseline, or reframe. Each absence found raises a `GAP` marker through the same mechanism as an invented number, so a thin-input draft comes back heavily marked — the correct signal.

**Replace with:** `[PF-2.13 GAP: what the sweep found missing — why it is missing]`.

### PF-2.14 — Flag commitment-shaped language

Language reading as a promise about a date, volume, performance level, or outcome can become a contractual warranty, and this catalog cannot judge whether a sentence forms one. It raises `REVIEW (commitment)` rather than deciding.

**Replace with:** restate as what the vendor will do with the buyer's stated precondition attached, or keep the commitment and carry the marker for confirmation.

### PF-2.15 — Flag customer reference details that need disclosure permission

Naming a prior client, quoting them, or describing their estate specifically enough to identify them needs that client's permission, which this catalog cannot check. It raises `REVIEW (reference)`.

**Replace with:** reduce identifying detail to what the vendor can evidence without naming the client, marker carried until permission is confirmed.

### PF-2.16 — Flag competitor comparisons

A claim about what a named rival does, does not do, or cannot do creates exposure this catalog cannot assess. It raises `REVIEW (competitor)`.

**Replace with:** restate the claim as what this vendor does, evidenced, with no assertion about the rival — keep the marker if it must stay.

### PF-2.17 — Flag compliance, certification, and export claims

A statement that the vendor holds a certification, meets a control, or may export a capability is external state this catalog cannot verify. It raises `REVIEW (compliance)`.

**Replace with:** narrow the claim to what the vendor holds today, with the gap to what the buyer asked for stated plainly, not omitted.

## PF-3 — Specificity and buzzwords

### PF-3.1 — The deletion test

For any term naming an outcome, a capability, or a quality rather than a concrete technical noun, ask what evidence must survive if the term were deleted. If deletion changes the sentence's claim, attach that evidence — the fact, figure, or comparison the term stood in for — in the same sentence, rather than deleting it. If deletion changes nothing, the term was decorative: delete it.

**Replace with:** the fact the term stood in for, attached in the same sentence, or a gap marker naming what's missing.

### PF-3.2 — Apply the test to each token, not the phrase

A compound term where one half is a real technical noun and the other pure decoration survives a whole-phrase deletion test, because the noun carries the phrase's meaning once the decoration is gone. Delete each token independently and judge it alone — never the phrase as one unit, or the decoration launders itself as part of the noun it rides on.

**Replace with:** the load-bearing token kept, the decorative token cut, evidence attached in its place.

### PF-3.3 — Retain a customer's own term, mark it, and let the integrity flag fire too

A term appearing verbatim in the customer's own supplied source material is retained and marked, not deleted — the evaluator scores against the buyer's vocabulary, not a paraphrase. The override fires only against material actually supplied as customer source material, so nothing the vendor wrote can launder as the customer's term. A retained term is marked on its first occurrence only, not every repetition. Retention never suppresses an integrity rule: a term also asserting something unverifiable carries both markers on the same phrase — retention is a vocabulary decision, the flag a truth decision, neither suppressing the other.

**Replace with:** the retention marker naming its source: `[PF-3.3: customer's term, retained — source]`.

## PF-4 — Prose mechanics

This section restates only the subset of general prose discipline instrumental to writing evidence-backed presales prose — sentence length, active voice, modal discipline, and one claim per sentence. It depends on no other skill, tool, or standard being installed.

### PF-4.1 — Sentence length

No sentence runs longer than 25 words, counted as words delimited by whitespace — one stated definition of length, not an implied one.

**Replace with:** split at 25 words into two sentences, one claim per sentence, evidence adjacent to its claim.

### PF-4.2 — Active voice

Name the actor performing the verb as the sentence's subject, so the reader knows who commits to what. The one exception is a sentence whose actor is genuinely unknown — a passive avoiding the actor is itself a finding, not a stylistic choice.

**Replace with:** the actor named as the subject, or — if unknown — that stated plainly, not hidden behind a passive.

### PF-4.3 — Modal discipline

`Will`, `does`, and `is` carry a commitment; `may`, `might`, and `could` carry a possibility. A sentence must not mix the two — a claim cannot promise an outcome and hedge about it too.

**Replace with:** choose one register — `PF-2.3` already rules out hedging a real commitment; `PF-2.14` flags a commitment-shaped verb for review.

### PF-4.4 — One claim per sentence

A sentence carrying two claims lets one ride on the other's evidence, so a reader who checks one number assumes the other has been checked too.

**Replace with:** split the sentence and attach evidence to each claim separately.

## PF-5 — Consistency and voice

A subtractive catalog applied without this section produces correct, evidenced, dead prose. This section names the devices the rest of this catalog must not strip, and requires check mode to leave them alone.

### PF-5.1 — Keep an explicit before/after contrast

The document contains at least one explicit before-and-after pair, the structure `PF-1.5` produces. Check mode never reports a contrast structure as a violation — a before state next to its after state is exactly what this catalog asks.

**Replace with:** a document missing the contrast raises a `GAP` marker through `PF-2.13`, like a missing metric.

### PF-5.2 — Address the buyer's stated priorities in the second person

Where the buyer has stated a priority in their own words, the document addresses it directly to them — "you," not "the organization." Check mode never reports second-person address to a stated priority as a violation.

**Replace with:** replace third-person distance ("the organization needs") with direct address in the buyer's own stated words.

### PF-5.3 — Keep an evidenced claim unhedged

A claim whose evidence sits adjacent to it is written flat and confident, with no hedge. Check mode never reports a confident, evidenced claim as a violation, and never proposes hedging as the repair.

**Replace with:** an unevidenced claim goes to `PF-2.4`, not softened in place.

## Write mode

Output is exactly three parts, in order: the artifact-family line, the prose itself, then the trailing register. The family line always prints and carries one of five values: an RFP answer, a proposal section, an executive summary, demo or discovery material, or **No family fits:** followed by the family-independent rules only — a document this session cannot place takes that fifth value rather than taking silence. No list of applied rules follows the prose.

At the start of a drafting task, name what counts as customer source material — RFP question text, discovery notes, stated requirements — and ask for it once. The ask never ends the turn: the draft follows in the same response whether or not material is supplied. `PF-3.3` fires only against material actually supplied for this task; inferring provenance from whatever the writer pasted would let the vendor's own wording launder itself as the customer's own term. With nothing supplied, say once that the provenance override cannot fire and every term will be judged by the deletion test alone.

When a claim cannot be made, the true part of the sentence ships and a marker takes the exact place the claim would have occupied, so the omission is visible in position and not only in the register a reader may not reach. Nothing false is emitted and nothing silently disappears.

The register lists every marker as a three-column table, with no Owner column — the skill cannot know a customer's or a vendor's own internal organisation, and inventing one in the table meant to police fabrication is the failure the integrity rules exist to prevent:

| Marker | Rule | What is needed |
|---|---|---|

Every marker appearing inline also appears as a register row.

## Check mode

Check mode names the artifact family it is reading the document as before reporting any finding, states when no family fits and applies only the family-independent rules, and follows `references/artifact-patterns.md`'s classification procedure rather than restating it here.

Output is a report, never a corrected document.

Each finding is a block: the rule ID, the offending text quoted exactly as it appears — including its whitespace, and never truncated or shortened with an ellipsis however long it runs — and a compliant rewrite. A rewrite that needs evidence the writer does not have is itself compliant prose carrying the marker in its place, so it is directly pasteable rather than a refusal.

Findings are grouped under four labelled sections in this fixed order: `## Integrity flags` first — findings that can cost a deal or create legal exposure are read before anything else.

`## Prose violations` comes second. Within a group, findings run in document order, so the writer works top to bottom through their own document; two findings on the same line are ordered by ascending rule ID. Two findings raised on the same offending text are reported as two separate blocks, each carrying its own rule ID, never merged into one.

`## Completeness gaps` comes third, carrying the document-level findings `references/completeness-audit.md` defines, each citing its own `MC-` number. `## Structural ordering` comes fourth, reporting one verdict on whether the document follows the order its classified artifact family expects; a finding there names the family and the convention it breaks and cites no rule number, because no numbered namespace covers those conventions.

A writer can also ask for the completeness audit on its own, separate from a full check-mode pass; that run returns `## Completeness gaps` and its verdict alone, with no prose findings and no rewritten document — see `references/completeness-audit.md`.

All four section headings always print. A group with nothing to report carries an explicit no-findings line rather than disappearing, so a clean document still produces a report. Check mode given no text to check says so rather than returning an empty report.

A marker still present when check mode runs means the rule was honoured — nothing was fabricated — so it is not a prose violation. It still surfaces in the register so it cannot ship unresolved. This is what distinguishes the writer having done the right thing from the document being ready to send.

## Self-check before delivering

Run this mechanical check, in three named passes, before returning any output.

1. Family-order pass (mandatory): re-scan the response you just drafted, from its first character, before returning it, and confirm the line naming the artifact family — or stating **No family fits:** — stands before any rule marker, meaning no `PF-` or `MC-` citation appears earlier in the response. When one does, move the family line to the top and re-check before returning.
2. Subtractive pass: find the violations to remove.
3. Additive sweep (mandatory): ask whether an explicit before/after contrast, a metric with a baseline, a differentiator, and the opening reframe are all present. A missing one is reported exactly as a removal is, through the same `GAP` marker mechanism `PF-2.13` defines.

A self-check that only ever finds things to delete has skipped pass three.

## Limits

What this skill flags but cannot verify: disclosure authorization for a named reference, certification and compliance status, the accuracy of any claim about a competitor, and legal or contractual exposure. A clean check report is not legal clearance.

What this skill does not produce: slide decks and visual design, pricing calculation, sizing, or commercial modelling, CRM or bid-management integration, and marketing or brand writing. It does not fact-check the writer's inputs — it refuses to invent facts and marks gaps, but cannot verify what it is given.
