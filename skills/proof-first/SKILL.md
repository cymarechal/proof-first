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

A technical evaluator finishes the document believing the author genuinely understands their
problem — because complex things were made simple without being made wrong. This catalog exists
so persuasion survives without ever costing technical accuracy: every claim carries its evidence
or carries a visible marker instead, and every buzzword is tested rather than guessed at.

Concepts here are paraphrased from publicly described sales frameworks. Not affiliated with or endorsed by any framework rights-holder. See NOTICES.md.

## Your task

Select a mode before drafting or reviewing anything:

- **Write mode** — the request asks for new or revised presales prose (an RFP/RFI answer, a
  proposal section, an executive summary, demo or discovery material).
- **Check mode** — the request asks you to review an existing draft.

Apply the rule catalog below in either mode. Cite only rule numbers defined in this file or
listed in `references/checklist.md`; never a number recalled from memory, and never a number
outside the stated total below. An invented rule number is a worse failure than no citation at
all.

This catalog contains 31 rules in 6 numbered sections.

## Marker vocabulary

When a rule requires marking rather than silently omitting or silently complying, use exactly
one of these three bracket forms. The rule number that raised the marker always comes first
inside the bracket:

- `[<rule> GAP: what is missing]` — an evidence gap: a claim that needed a number, a source, or a
  fact that was not supplied or measured. See PF-2.11 below for a worked instance.
- `[<rule> REVIEW (<one of the four categories below>): what needs confirming]` — a flag needing
  human confirmation before the document ships. The four categories are exactly `commitment`,
  `reference`, `competitor`, and `compliance` — see PF-2.14 through PF-2.17 below.
- `[<rule>: customer's term, retained — source]` — a customer-verbatim term that the deletion
  test would otherwise remove, kept and marked instead.

In every form, `<rule>` is the ID of the rule that raised the marker — never omitted, never a
number invented for the occasion.

A retained term under the third form is marked on its first occurrence only, not on every
repetition. A term that is both customer-verbatim and integrity-risky carries both a retention
marker and a `REVIEW` marker — retention is a vocabulary decision, the flag is a truth decision,
and neither one suppresses the other.

Every marker produced in a document is also listed, once drafting is complete, in a trailing
register under the heading `## Unresolved before this document is sent`. That register's full
column shape is authored later in this catalog's build; this file only fixes the marker grammar
and the register's heading now, because both are read by later sections of this catalog and by
the tools that check its output.

## Reference files

- Before applying the deletion test to a compound term, or to any term appearing in the
  customer's own supplied source material, read `references/deletion-test.md`.
- Before emitting any rule citation in check mode, read `references/checklist.md`.

## PF-0 — Opening and reframe

### PF-0.1 — The opening reframe

Open by restating the buyer's own situation, in terms they have already used, before naming any
product, vendor, or capability. A reframe names what the current state costs the buyer and states
the shift this document proposes, as one paragraph making one point. A reframe that opens with a
capability list, or that splits itself across several opening sentences each adding a new
qualifying condition, does not satisfy this rule — the resolution has to read as a single
instruction applied once, not as several overlapping ones to reconcile.

**Replace with:** the buyer's own words for their current state and its cost, never the vendor's
name for what it is selling.

✗ "Kestrel Systems Group offers a comprehensive, best-in-class cloud migration solution."
✓ "Halverton Mutual's 850-VM estate is at capacity, and its nightly settlement batch
   regularly overruns its required window. This proposal describes an estate the team
   can govern, not one it has to manage VM by VM."

## PF-1 — Structure

The Command of the Message spine is carved into seven sub-blocks, each reserved four IDs: Before
scenario, After scenario, Required Capabilities, Metrics, Proof Points, Differentiators, and
Positive Business Outcomes. A sub-block with no rule in this version is intentional headroom for a
later minor version, not an omission.

### PF-1.1 — Name the current state in the buyer's own terms

Describe the before state in the words the buyer used about their own estate, never in the
vendor's category language. A before state that only speaks the vendor's own taxonomy has not
named anything the buyer will recognize as their situation.

**Replace with:** the buyer's own phrasing drawn from supplied source material, or the concrete
system, count, or process the buyer actually named.

✗ "Halverton Mutual's infrastructure suffers from significant technical debt and sprawl."
✓ "Halverton Mutual runs its policy-administration and settlement estate on 850 VMware vSphere
   virtual machines and 40 Oracle Database instances, all on-premises."

### PF-1.2 — Name what the current state costs

A before state with no stated cost is scene-setting, not a case for change. Name the cost the
buyer already states, never a cost invented to sound significant.

**Replace with:** the run-rate figure, the manual process, or the constrained rollout the buyer
already named — or an explicit gap marker if the buyer has never quantified it.

✗ "Running the current estate is expensive and holds the business back."
✓ "The current annual run rate is $2,300,000. Oracle Database licensing is an increasing
   share of it with no ceiling under the existing on-premises model."

### PF-1.5 — State the after-state as an observable change, paired with its before

An after state ships next to the before state it replaces, so the contrast is visible on the page
rather than left for the reader to reconstruct. A later rule in this catalog's Consistency and
Voice section makes this pairing a checkable presence requirement, not only a style preference.

**Replace with:** the paired form — before and after in the same sentence or the same pair of
sentences.

✗ "The new platform will be highly scalable and resilient."
✓ "Failover across the 850-VM estate is a manual process today; on Amazon EC2, failover is
   automated and no longer extends incident response time."

### PF-1.9 — State the capability the buyer needs, not the product that has it

State the capability as what the buyer must be able to do. A product name enters only afterward,
as the means of delivering that capability — never as the subject of the sentence.

**Replace with:** the reordering — capability stated first, product named second as the means.

✗ "AWS Control Tower gives you comprehensive landing-zone governance."
✓ "Halverton Mutual needs a landing zone it can actually govern account by account; AWS Control
   Tower provides that governance boundary across the new account structure."

### PF-1.13 — Name the measure and its current baseline

A metric with no baseline is a target, not a metric. Name the buyer's own stated figure for the
measure, or state plainly that it has never been captured.

**Replace with:** the buyer's own stated figure, or an explicit gap marker naming what would need
to be measured.

✗ "Settlement batches will run significantly faster after migration."
✓ "Settlement batches will complete inside the required 6-hour window; Halverton Mutual has
   never measured the size of the current overrun — [PF-1.13 GAP: no measured baseline for
   the settlement batch overrun]."

### PF-1.14 — Name where the baseline came from

A baseline with no stated provenance cannot be checked by the evaluator. Name the source — the
buyer's own figure, a named measurement, or the document it came from.

**Replace with:** the attribution — who stated the figure, or what document it came from.

✗ "The current run rate is $2,300,000."
✓ "Diane Osoria, Halverton Mutual's CFO, states the current annual run rate at $2,300,000 —
   the figure she is measured against."

### PF-1.17 — Attach one comparable, verifiable proof to each capability claim

One named, checkable comparable beats three unnamed ones. A capability claim with no attached
proof is an assertion, not evidence.

**Replace with:** a comparable this vendor can actually produce, or an explicit gap marker naming
what proof is missing.

✗ "We have deep experience running migrations exactly like this one."
✓ "Kestrel Systems Group's most comparable prior migration programme ran 14 months —
   [PF-1.17 GAP: no published case study or reference customer identified for that
   programme yet]."

### PF-1.21 — Claim a differentiator only where a named alternative cannot do it

A differentiator every bidder could also claim is a feature, not a differentiator. A claim about
what a specific named rival cannot do is an integrity matter this catalog's Proof and Integrity
section addresses separately — restate the claim as what this vendor does, evidenced, without
asserting what a rival cannot. A comparison that names a rival carries a `REVIEW (competitor)`
marker.

**Replace with:** the claim restated as an evidenced statement of what this vendor does.

✗ "Only Kestrel Systems Group can deliver a truly governable landing zone — no other bidder
   comes close."
✓ "Kestrel Systems Group delivers landing-zone governance through AWS Control Tower's
   account-level guardrails, evidenced by our own comparable migration programme —
   [PF-1.21 REVIEW (competitor): confirm no comparison naming another bidder is implied
   before this ships]."

### PF-1.25 — Tie the outcome to the stated priority of the person who owns it

An outcome is addressed to the person measured on it, in the terms they used — not to "the
organization" or "the business" in the abstract.

**Replace with:** the role, named, and the priority that role stated in their own words.

✗ "This migration delivers significant business value across the organization."
✓ "For Diane Osoria, Halverton Mutual's CFO: this migration is measured on the run rate she
   needs down from $2,300,000 and on a clean regulatory examination — not on architecture
   elegance."

## PF-2 — Proof and integrity

This section is carved into two sub-blocks: Proof rules attach evidence to a claim and name where
that evidence came from; Integrity rules refuse two classes of fabrication and flag four presales
hazards for a human to confirm. A rule added later to one sub-block must not land inside the
other's reserved range.

### PF-2.1 — Every claim carries its evidence

A sentence asserting something about the customer's estate, the vendor's capability, or an outcome
carries the evidence for that assertion in the same sentence or the next one.

**Replace with:** the customer's own stated figure, a named artefact the reader could ask for, or
a `GAP` marker — no fourth option.

### PF-2.2 — Name the source of the evidence

Evidence with no named source is an assertion wearing a number. Name the source inline — the
person, the document, or the measurement that produced it.

**Replace with:** the source stated by name; "industry data" and "our experience" are not sources.

### PF-2.3 — Adjacent evidence licenses an unhedged claim

A claim whose evidence sits in the same or the next sentence is written flat and confident, with
no hedge. Hedging is never the repair for missing evidence.

**Replace with:** strip the hedge from an evidenced claim; send an unevidenced claim to `PF-2.4`
instead.

### PF-2.4 — No evidence: cut the claim and mark the gap in its place

When no evidence exists, the claim is cut and a `GAP` marker takes its exact place, so the omission
is visible where the claim would have been, not only in the register. The marker's rule token is
the rule that raised it, which is what lets a check report cite an integrity finding exactly as it
cites a prose violation.

**Replace with:** `[PF-2.4 GAP: what is missing — why it is missing]`.

### PF-2.11 — Never invent a metric, a baseline, or a benchmark number

Refuse to state a percentage, a duration, a dollar figure, or a rate that was not supplied by the
customer or measured and given to you as a fact. When a measure exists in the buyer's own words
but its baseline was never captured, say so in place of the number rather than estimating one to
sound confident.

**Replace with:** the customer's own stated figure, or an explicit gap marker naming what would
need to be measured.

✗ "Our migration significantly reduces settlement batch overruns."
✓ "Settlement batches will complete inside the window they currently overrun; Halverton
   Mutual has never measured the size of that overrun — [PF-2.11 GAP: no measured
   baseline for the settlement batch overrun]."

### PF-2.12 — Never invent a reference customer, a logo, or a named account

Refuse to name a client, a logo, or an account as a reference unless the writer supplied it as a
fact. A named party invented to sound like a proof point is a fabrication the reader has no way to
detect until they ask for it.

**Replace with:** the true part of the sentence, with a `GAP` marker in place of the named
reference — never a plausible anonymised substitute standing in for it.

✗ "A large regulated insurer already runs this exact migration pattern in production."
✓ "Kestrel Systems Group has not been given a reference customer to cite for this migration
   pattern — [PF-2.12 GAP: no reference customer supplied]."

### PF-2.13 — An absence found by the additive sweep is marked like any other gap

The additive sweep specified later in this catalog checks for a missing differentiator, a missing
baseline, or a missing reframe. Each absence it finds raises a `GAP` marker through the same
mechanism as an invented number, so a thin-input draft comes back heavily marked — the correct
signal, not a defect.

**Replace with:** `[PF-2.13 GAP: what the sweep found missing — why it is missing]`.

✗ "Kestrel Systems Group delivers landing-zone governance for the new account structure."
✓ "Kestrel Systems Group delivers landing-zone governance for the new account structure —
   [PF-2.13 GAP: no differentiator supplied against either rival bidder for this capability]."

### PF-2.14 — Flag commitment-shaped language

Language that reads as a promise about a date, a volume, a performance level, or an outcome can
become a contractual warranty, and this catalog cannot judge whether a given sentence forms one.
It raises `REVIEW (commitment)` rather than deciding.

**Replace with:** restate as what the vendor will do with the buyer's own stated precondition
attached, or keep the commitment and carry the marker for a human to confirm.

✗ "Kestrel Systems Group will complete the migration within Halverton Mutual's 8-month
   examination window."
✓ "Kestrel Systems Group's own most comparable prior migration programme ran 14 months, longer
   than Halverton Mutual's 8-month examination window — [PF-2.14 REVIEW (commitment): confirm
   the proposed timeline against that comparable duration before this date is promised]."

### PF-2.15 — Flag customer reference details that need disclosure permission

Naming a prior client, quoting them, or describing their estate specifically enough to identify
them needs that client's permission, which this catalog has no way to check. It raises
`REVIEW (reference)`.

**Replace with:** reduce the identifying detail to what the vendor can evidence without naming the
client, with the marker carried until permission is confirmed.

✗ "Our 14-month migration for a comparable regulated insurer proves we can deliver this on
   schedule."
✓ "Kestrel Systems Group's own most comparable prior migration programme ran 14 months —
   [PF-2.15 REVIEW (reference): confirm that prior client has agreed to be cited before this
   comparison ships]."

### PF-2.16 — Flag competitor comparisons

A claim about what a named rival does, does not do, or cannot do creates exposure this catalog
cannot assess. It raises `REVIEW (competitor)`.

**Replace with:** restate the claim as what this vendor does, evidenced, with no assertion about
the rival — and keep the marker if the comparison must stay.

✗ "Ardent Digital manages 62% of the estate today and cannot deliver the governance boundary
   Halverton Mutual needs — only Kestrel Systems Group can."
✓ "Kestrel Systems Group delivers landing-zone governance through account-level guardrails
   across the new account structure — [PF-2.16 REVIEW (competitor): confirm no claim about
   the incumbent's capability is implied before this ships]."

### PF-2.17 — Flag compliance, certification, and export claims

A statement that the vendor holds a certification, meets a control, or may export a capability is
external state this catalog cannot verify. It raises `REVIEW (compliance)`.

**Replace with:** narrow the claim to exactly what the vendor holds today, with the gap between
that and what the buyer asked for stated plainly rather than omitted.

✗ "Kestrel Systems Group meets Halverton Mutual's SOC 2 Type II requirement."
✓ "Kestrel Systems Group holds a SOC 2 Type I report today; Halverton Mutual's RFP requires
   Type II, and Kestrel's Type II observation window closes after the 2026-10-30 submission
   date — [PF-2.17 REVIEW (compliance): confirm this gap is acceptable to the buyer before
   this ships]."

The closed `REVIEW` category vocabulary — `commitment`, `reference`, `competitor`, `compliance` —
maps one-to-one onto the four rules above: `PF-2.14` raises `commitment`, `PF-2.15` raises
`reference`, `PF-2.16` raises `competitor`, and `PF-2.17` raises `compliance`, so a reader and a
later linter both have the mapping in one place.

## PF-3 — Specificity and buzzwords

### PF-3.1 — The deletion test

For any term naming an outcome, a capability, or a quality rather than a concrete technical noun,
ask what evidence would have to survive if the term were deleted. If deleting the term changes
what the sentence claims, attach that evidence — the fact, the figure, or the comparison the term
was standing in for — in the same sentence rather than deleting it. If deleting the term changes
nothing the sentence claims, the term was decorative: delete it rather than defending it.

**Replace with:** the fact the term was substituting for, attached in the same sentence, or a gap
marker naming what evidence is missing.

✗ "A robust, enterprise-grade landing zone governs every account."
✓ "A landing zone governed by account-level guardrails replaces 850 ungoverned virtual
   machines with one governance boundary."

### PF-3.2 — Apply the test to each token, not the phrase

A compound term where one half is a real technical noun and the other is pure decoration survives
a whole-phrase deletion test, because the noun carries the phrase's meaning even once the
decoration is gone. Delete each token in the compound independently and judge it on its own —
never the phrase as one unit, or the decoration launders itself as part of the noun it rides on.

**Replace with:** the load-bearing token kept in place, the decorative token cut, and evidence
attached where the decoration used to be.

✗ "An enterprise-grade AWS Control Tower deployment governs the new account structure."
✓ "An AWS Control Tower deployment governs the new account structure across Halverton
   Mutual's 850 virtual machines."

### PF-3.3 — Retain a customer's own term, mark it, and let the integrity flag fire too

A term appearing verbatim in the customer's own supplied source material is retained and marked,
not deleted — the buyer's evaluator scores against their own vocabulary, not a paraphrase of it.
The override fires only against material the writer actually supplied as customer source
material, so nothing the vendor wrote can launder itself as the customer's own term. A retained
term is marked on its first occurrence only, not on every repetition — noise is bounded by the
count of distinct retained terms, not by total uses. Retention never suppresses an integrity
rule: a retained term that also asserts something this catalog cannot make good on carries both
the retention marker and a `REVIEW` marker on the same phrase, because retention is a vocabulary
decision and the flag is a truth decision.

**Replace with:** the retention marker naming its source, `[PF-3.3: customer's term, retained —
source]`.

✗ "The proposal replaces ungoverned VM sprawl with a landing zone that will be fully governed
   from day one."
✓ "The proposal replaces ungoverned VM sprawl with a landing zone
   [PF-3.3: customer's term, retained — Marcus Feld, discovery] that will be fully governed
   from day one — [PF-2.14 REVIEW (commitment): confirm 'fully governed from day one' before
   this ships]."

## PF-4 — Prose mechanics

This section restates only the subset of general prose discipline instrumental to writing
evidence-backed presales prose — sentence length, active voice, modal discipline, and one claim
per sentence. It depends on no other skill, tool, or standard being installed.

### PF-4.1 — Sentence length

No sentence runs longer than 25 words, counted as words delimited by whitespace — one stated
definition of length, not an implied one.

**Replace with:** split at 25 words into two sentences, one claim per resulting sentence, with its
evidence kept adjacent to the claim it supports.

### PF-4.2 — Active voice

Name the actor performing the verb as the sentence's subject, so the reader knows who is
committing to what. The one admissible exception is a sentence whose actor is genuinely unknown —
a passive used instead to avoid naming who commits is itself a finding, not a stylistic choice.

**Replace with:** the actor named as the subject, or — if genuinely unknown — that stated plainly,
never hidden behind a passive verb.

### PF-4.3 — Modal discipline

`Will`, `does`, and `is` carry a commitment; `may`, `might`, and `could` carry a possibility. A
sentence must not mix the two — a claim cannot both promise an outcome and hedge about whether it
happens.

**Replace with:** choose one register and keep it. A possibility-shaped hedge on a real commitment
is what `PF-2.3` already rules out; a commitment-shaped verb is what `PF-2.14` flags for review.

### PF-4.4 — One claim per sentence

A sentence carrying two claims lets one ride on the other's evidence, so a reader who checks one
number assumes the other has been checked too.

**Replace with:** split the sentence in two and attach evidence to each claim separately.

## PF-5 — Consistency and voice

A subtractive catalog applied without this section produces correct, evidenced, dead prose. This
section names the devices the rest of this catalog must not strip, and requires check mode to
leave them alone.

### PF-5.1 — Keep an explicit before/after contrast

The document contains at least one explicit before-and-after pair, the structure `PF-1.5`
produces. Check mode never reports a contrast structure as a prose violation — a document stating
a before state next to its after state is doing exactly what this catalog asks.

**Replace with:** a document missing the contrast raises a `GAP` marker through `PF-2.13`, exactly
as a missing metric does.

### PF-5.2 — Address the buyer's stated priorities in the second person

Where the buyer has stated a priority, in their own words, the document addresses it directly to
them — "you" and their own terms, not "the organization" or "stakeholders." Check mode never
reports second-person address to a stated priority as a violation.

**Replace with:** replace third-person distance ("the organization needs") with direct address
using the buyer's own stated priority in their own words.

### PF-5.3 — Keep an evidenced claim unhedged

A claim whose evidence sits adjacent to it is written flat and confident, with no hedge.
Check mode never reports a confident, evidenced claim as a violation, and never proposes a
hedge as the repair for anything.

**Replace with:** an unevidenced claim goes to `PF-2.4` instead of being softened in place.
