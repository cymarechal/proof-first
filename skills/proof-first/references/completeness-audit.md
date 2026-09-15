# Completeness Audit

Open this file before running a document-level completeness audit, or before reporting a
completeness gap in check mode. This audit asks questions of a document rather than judging its
prose sentence by sentence, and its verdict is reported separately from the prose catalog in
`SKILL.md`. Its rule IDs live in the `MC-` namespace, disjoint from that catalog's `PF-`
namespace, so a citation from one namespace never satisfies or interferes with the other's
citation check.

Concepts here are paraphrased from publicly described sales frameworks. Not affiliated with or endorsed by any framework rights-holder. See NOTICES.md.

The dimension blocks below are ordered the way `NUMBERING.md` reserves their ID ranges. That
order is inherited numbering-scheme structure, fixed in this repository's registry before this
file was written — it states nothing about which order is correct or original for the
methodology these dimensions derive from.

This audit contains 8 checks across 8 dimensions.
An MC number outside that count does not exist and must never be cited.

### MC-1 — Name the buyer's own measure and where its baseline came from

A document missing this dimension never names the figure the person who signs is actually measured
on, or names one with no stated baseline to move it from. The person who signs for Halverton Mutual
states her own run-rate target directly: $2,300,000 is the number she answers for, not a
capability the vendor prefers to lead with. A metric can also be present in name and missing in
substance — the nightly settlement batch job's required window is stated, but Halverton Mutual
has never instrumented how far the job overruns it, so no baseline exists to report. A document
inventing an overrun figure for that job, instead of marking the missing baseline, has fabricated
what this dimension asks it to name honestly.

**Replace with:** the buyer's own stated figure and the source that produced it, or a
`[MC-1 GAP: what baseline is missing]` marker where the buyer's own figure was never captured.

### MC-6 — Name the person who signs and the priority they stated in their own words

A document missing this dimension addresses the buyer as an undifferentiated organisation rather
than naming the person whose signature closes the deal, or names a title with no priority in that
person's own words attached to it. The person who signs for Halverton Mutual is Diane Osoria, its
Chief Financial Officer, and she states her own priorities directly. A document that substitutes a
generic reference to "the buyer" or "stakeholders" for her name, or that states a priority in the
vendor's language rather than hers, has not named the person who signs.

**Replace with:** the name and role of the person who signs, and one priority stated in their own
words, or a `[MC-6 GAP: what is missing]` marker where neither was captured.

### MC-11 — Mirror the buyer's own stated evaluation criteria and their weights

A document missing this dimension substitutes the vendor's own preferred framing for the buyer's
stated evaluation criteria, or blends separate weighting schemes the buyer keeps apart. Halverton
Mutual scores bidders on three weighted criteria — technical approach, commercial model, and
security posture — and separately scores five RFP questions against their own weights. A document
that reorders those criteria into the vendor's preferred sequence, or that merges the two weighting
schemes into one, has not mirrored the buyer's own evaluation.

**Replace with:** the buyer's own criteria and weights, restated in the buyer's own structure, or a
`[MC-11 GAP: what is missing]` marker where the buyer's own weighting was never captured.

### MC-16 — State the steps, dates, and people the buyer's evaluation runs through

A document missing this dimension never states when the buyer decides, who scores the response, or
how many competitors are in the running. Halverton Mutual has shortlisted three bidders, requires
proposals by a stated submission date, and scores every bidder against the same five questions
inside a stated regulatory examination window. A document silent on any of those specifics has not
stated how the buyer's evaluation runs.

**Replace with:** the submission date, the bidder count, and the scoring process the buyer itself
stated, or a `[MC-16 GAP: what is missing]` marker where one of those was never captured.

### MC-21 — State the reviews the document must clear before a signature is possible

A document missing this dimension treats the path to signature as a single step, when the buyer's
own process is a sequence of named reviews with named owners. Halverton Mutual's proposal moves
through a security review, a procurement review, and a legal review, each with its own named owner,
and two of the three with a stated duration in business days — the third has no duration the buyer
has stated. A document that omits a review, invents a duration the buyer never gave, or rounds a
partially-stated review up to fully specified, has not stated the reviews it must clear honestly.

**Replace with:** each review's named owner and its stated duration where the buyer has stated one,
or a `[MC-21 GAP: what duration is missing]` marker beside the review whose duration the buyer
never stated.

### MC-26 — Name the cost the buyer already states, in the buyer's own words

A document missing this dimension never names the cost the buyer itself points to, or invents a
figure to fill a baseline the buyer has never measured. Halverton Mutual's own stated cost is a
nightly settlement batch job that regularly overruns its required window, with no baseline the
buyer has ever instrumented for how far it overruns; rising Oracle Database licensing, a vSphere
estate at capacity, and a manual failover process are named costs too. Naming one of these costs
without a fabricated number attached, or explicitly marking that no baseline exists, satisfies this
dimension; inventing an overrun figure to replace a genuinely missing one does not.

**Replace with:** the cost in the buyer's own words and its stated figure where one exists, or a
`[MC-26 GAP: no baseline stated]` marker where the buyer has never measured it — an explicitly
marked missing baseline satisfies this dimension.

### MC-31 — Name the person inside the buyer who carries this internally

A document missing this dimension never names who inside the buyer's organisation is advocating for
the deal internally, once the vendor is no longer in the room. The person inside Halverton Mutual
who carries this internally is Marcus Feld, its Vice President of Infrastructure, who states his
own reason for wanting change directly. A document that substitutes a generic reference to "the
infrastructure team" for his name, or that never quotes his stated reason in his own words, has not
named the person who carries this internally.

**Replace with:** the name, role, and stated reason for wanting the change of the person inside the
buyer who carries this internally, or a `[MC-31 GAP: what is missing]` marker where neither was
captured.

### MC-36 — State the alternatives the buyer is weighing, without asserting what a rival cannot do

A document missing this dimension never names who else the buyer is evaluating, or names a rival
only to assert a capability that rival supposedly lacks. Halverton Mutual is weighing three
bidders, including Ardent Digital, the incumbent managed-services provider already running a
majority share of the estate, and Vantage Nine Consulting; the buyer's own technical evaluator has
stated a preference for extending the incumbent's contract rather than migrating. Naming these
alternatives without asserting what a named rival cannot do satisfies this dimension — a claim
about a competitor's inability is a prose integrity hazard, not this dimension's job to make.

**Replace with:** the named alternatives the buyer is weighing and any stated preference among
them, or a `[MC-36 GAP: what is missing]` marker where the buyer's alternatives were never named.

## Running the audit on its own

A writer can ask for this audit on its own, separate from a full check-mode pass over prose and
integrity. Run against a document, it returns the check-mode report's `## Completeness gaps`
section by that exact heading, followed by one verdict line naming how many of the eight dimensions
the document satisfies and naming each dimension it does not. A standalone run returns no prose
findings and never rewrites the document, and adds no `## Integrity flags` section, no
`## Prose violations` section, and no `## Structural ordering` verdict; naming the artifact family
it read the document as is permitted and is not a finding.

## What this file does not do

This file is not a scoring rubric, and it is not a pass/fail gate that substitutes for a human's
judgment about whether a document is ready to send. It is not a qualification tool for a live
deal — it asks questions of a document and reports what the document does not contain; it does
not decide whether the underlying deal itself is winnable.
