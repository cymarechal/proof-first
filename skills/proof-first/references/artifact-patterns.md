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

## Solution proposal

A solution proposal answers how the work would actually be delivered, addressed to a technical
buyer who has to defend the architecture internally after the vendor has left the room.

**Order:** the architecture narrative comes first, then the capability mapping, then the risk
treatment.

**Architecture narrative:** the target architecture is told as a narrative a reader follows
from the current estate to the target one, not presented as a component inventory. Halverton
Mutual's narrative moves from an on-premises VMware vSphere and Oracle Database estate to a
target of Amazon EC2, Amazon Aurora PostgreSQL, and AWS Control Tower for landing-zone
governance — the story is the path between those two states, not a list of either one alone.

**Capability mapping:** every capability the buyer stated they need is mapped to what delivers
it, with the capability stated first and the product named second as the means — the same
sentence shape `PF-1.9` already requires for the prose catalog, cited here rather than
restated.

**Risk treatment:** each material risk is named with what is done about it, and a risk the
vendor cannot retire is stated plainly rather than omitted. Halverton Mutual's RFP requires a
SOC 2 Type II report, and Kestrel Systems Group holds only a SOC 2 Type I report today; Kestrel
Systems Group's own most comparable prior migration programme took longer than Halverton
Mutual's examination window. Neither risk has an honest mitigation available before this
proposal ships — the convention is to say so, naming the gap plainly, never to invent one.

## Executive summary

An executive summary answers why the person who signs should sign, addressed directly to that
person, and read once before any other document in the response.

**Order:** the problem reframe comes first, then the business case, then the capability list.

**Problem reframe:** the summary opens by restating the buyer's own situation, in the buyer's
own words, before naming any product, vendor, or capability — the same opening rule `PF-0.1`
already states for the whole catalog, cited here rather than restated.

**Business case:** the case is stated before any capability list, in the terms the person who
signs is measured on, and it carries its evidence or a marker in place of it. Diane Osoria, the
economic buyer, states she is measured on run-rate reduction and a clean regulatory
examination — the business case is built from those terms, never from architecture elegance she
has said she does not weigh.

**Capability list last:** a capability list that arrives before the case has been made is the
named failure; the list is the support for the case, never the substitute for it.

## Demo and discovery material

Demo and discovery material answers "show me," addressed to a room in a discovery conversation
or a demo session, and it is read once, live, rather than at leisure.

**Order:** discovery notes come first, then the demo script they inform, then the
proof-of-concept success criteria the demo sets up, then the follow-up.

**Discovery notes:** what the buyer said is recorded in the buyer's own words and attributed to
the person who said it, so a later document can cite it as supplied customer source material —
Marcus Feld's own words about wanting a landing zone he can actually govern are recorded as his,
not paraphrased into the vendor's own vocabulary.

**Demo script:** the script shows the capability the discovery notes actually named, in the
buyer's own scenario, rather than a standard product tour.

**Proof-of-concept success criteria:** the criteria are agreed and written down before the
proof-of-concept runs, with the measure and who judges it named, so success is not decided
afterwards by whoever is in the room.

**Follow-up:** what happens next carries a named owner on the vendor's side and a date, and a
commitment-shaped statement inside it raises the `REVIEW (commitment)` marker the prose catalog
already defines.

## What this file does not do

This file is not a document template and it generates no boilerplate; it states conventions a
document is read against.

It does not decide the family for a document that genuinely spans two; the classification
section's fallback covers that case, and the ambiguity is reported, not resolved silently.

It mints no rule number, so nothing in it can be cited as one.

It is not evidence that a convention wins deals or improves scores; no benchmark has run, and
this repository makes measured claims or none.
