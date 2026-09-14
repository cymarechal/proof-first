# Artifact Family Patterns

Open this file before classifying a document into an artifact family, or before applying
that family's own conventions in either mode. Classification is decided and named before any
rule in this file or in the prose catalog is applied — in Write mode, as the assumed family
the writer states up front; in Check mode, as the family a finding is checked against. Each
family's conventions live only here, never folded into the prose catalog in `SKILL.md`.

Concepts here are paraphrased from publicly described sales frameworks. Not affiliated with or endorsed by any framework rights-holder. See NOTICES.md.

## Classifying the document

Three signals decide which family a document belongs to: what the document is answering, who
it is addressed to, and what artefact the reader expects back. Apply all three before applying
any rule, in either mode.

- A document answering the buyer's own scored questions, addressed to a scoring committee,
  expected back as a compliant response the committee can grade — an **RFP and RFI response**.
- A document answering how the work would actually be delivered, addressed to a technical
  buyer, expected back as an architecture and a delivery plan — a **Solution proposal**.
- A document answering why the person who signs should sign, addressed to that person,
  expected back as a one-page case for the decision — an **Executive summary**.
- A document answering "show me," addressed to a room in a discovery conversation or a demo
  session, expected back as a script or a set of proof-of-concept success criteria — **Demo and
  discovery material**.

**No family fits:** state the closest-fitting family by name, say plainly that the document
does not fit it, and apply only the conventions that are family-independent. Never force a
genuine mismatch silently into one of the four — a half-proposal, half-discovery-summary
document is reported as exactly that, not quietly filed under whichever family is closer.

A structural-ordering finding names the artifact family and the convention label it breaks, and
cites no rule number — no numbered namespace, `PF-` or `MC-`, covers these conventions.

## RFP and RFI response

A response to a formally issued RFP or RFI is scored by a committee working from the buyer's
own written rubric, not read for impression by a single reader — every convention below exists
because a scored response has a different physics than a proposal or a summary.

**Order:** the direct answer to the question being scored comes first, before the context, the
architecture, or the vendor's background.

**Answer first:** a scored evaluator awards points against how directly a section answers the
question asked. A section opening with company background or an architecture narrative before
answering the question has already cost points to a competitor who answered first. State the
answer to what was actually asked, in the first sentences of each section.

**Compliance apart from value:** the statement of what the vendor does and does not meet is
kept in its own place, separate from the argument for why the approach is worth choosing — an
evaluator scoring compliance reads a yes or a no there, not an argument. Blending the two makes
the evaluator hunt through persuasive prose to find a scoring answer, which is the failure this
convention names.

**Mirror the buyer's criteria:** the response follows the buyer's own stated evaluation
criteria, in the buyer's own order and the buyer's own words — never reorganised into the
vendor's preferred sequence, and never renamed into the vendor's own vocabulary. Halverton
Mutual keeps two separate weighting schemes apart: a three-row weighted evaluation-criteria
table (technical approach at 55%, commercial model at 25%, security posture at 20%) and five
separately weighted scored questions (30%, 20%, 15%, 15%, 20%). A response that reorders either
scheme, or merges the two into one, has stopped mirroring the buyer's own evaluation and
started substituting its own.
