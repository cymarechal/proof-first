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

This catalog contains 3 rules in 3 numbered sections.

## Marker vocabulary

When a rule requires marking rather than silently omitting or silently complying, use exactly
one of these three bracket forms. The rule number that raised the marker always comes first
inside the bracket:

- `[<rule> GAP: what is missing]` — an evidence gap: a claim that needed a number, a source, or a
  fact that was not supplied or measured. See PF-2.11 below for a worked instance.
- `[<rule> REVIEW (category): what needs confirming]` — a flag needing human confirmation before
  the document ships. The category is always exactly one of `commitment`, `reference`,
  `competitor`, or `compliance`.
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

- Before applying PF-3.1 to a compound term, or to any term appearing in the customer's own
  source material, read `references/deletion-test.md`.
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

## PF-2 — Proof and integrity

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
