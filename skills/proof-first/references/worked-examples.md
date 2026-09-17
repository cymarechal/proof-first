# Worked Examples

This file carries the worked ✗/✓ contrast for each catalog rule that has one. Every fact in every
example comes from `examples/deal-brief.md`. Each rule's own statement and its `**Replace with:**`
line live in `SKILL.md` for the prose catalog and in `references/completeness-audit.md` for the
completeness audit — this file supplies the contrast only, keyed by the ID of the rule it belongs
to.

## PF-0.1

✗ "Kestrel Systems Group offers a comprehensive, best-in-class cloud migration solution."
✓ "Halverton Mutual's 850-VM estate is at capacity, and its nightly settlement batch regularly overruns its required window. This proposal describes an estate the team can govern, not one it has to manage VM by VM."

## PF-1.1

✗ "Halverton Mutual's infrastructure suffers from significant technical debt and sprawl."
✓ "Halverton Mutual runs its policy-administration and settlement estate on 850 VMware vSphere virtual machines and 40 Oracle Database instances, all on-premises."

## PF-1.2

✗ "Running the current estate is expensive and holds the business back."
✓ "The current annual run rate is $2,300,000. Oracle Database licensing is an increasing share of it with no ceiling under the existing on-premises model."

## PF-1.5

✗ "The new platform will be highly scalable and resilient."
✓ "Failover across the 850-VM estate is a manual process today; on Amazon EC2, failover is automated and no longer extends incident response time."

## PF-1.9

✗ "AWS Control Tower gives you comprehensive landing-zone governance."
✓ "Halverton Mutual needs a landing zone it can actually govern account by account; AWS Control Tower provides that governance boundary across the new account structure."

## PF-1.13

✗ "Settlement batches will run significantly faster after migration."
✓ "Settlement batches will complete inside the required 6-hour window; Halverton Mutual has never measured the size of the current overrun — [PF-1.13 GAP: no measured baseline for the settlement batch overrun]."

## PF-1.14

✗ "The current run rate is $2,300,000."
✓ "Diane Osoria, Halverton Mutual's CFO, states the current annual run rate at $2,300,000 — the figure she is measured against."

## PF-1.17

✗ "We have deep experience running migrations exactly like this one."
✓ "Kestrel Systems Group's most comparable prior migration programme ran 14 months — [PF-1.17 GAP: no published case study or reference customer identified for that programme yet]."

## PF-1.21

✗ "Only Kestrel Systems Group can deliver a truly governable landing zone — no other bidder comes close."
✓ "Kestrel Systems Group delivers landing-zone governance through AWS Control Tower's account-level guardrails, evidenced by our own comparable migration programme — [PF-1.21 REVIEW (competitor): confirm no comparison naming another bidder is implied before this ships]."

## PF-1.25

✗ "This migration delivers significant business value across the organization."
✓ "For Diane Osoria, Halverton Mutual's CFO, this migration is measured on the run rate she needs down from $2,300,000. It is also measured on a clean regulatory examination — not on architecture elegance."

## PF-2.11

✗ "Our migration significantly reduces settlement batch overruns."
✓ "Settlement batches will complete inside the window they currently overrun; Halverton Mutual has never measured the size of that overrun — [PF-2.11 GAP: no measured baseline for the settlement batch overrun]."

## PF-2.12

✗ "A large regulated insurer already runs this exact migration pattern in production."
✓ "Kestrel Systems Group has not been given a reference customer to cite for this migration pattern — [PF-2.12 GAP: no reference customer supplied]."

## PF-2.13

✗ "Kestrel Systems Group delivers landing-zone governance for the new account structure."
✓ "Kestrel Systems Group delivers landing-zone governance for the new account structure — [PF-2.13 GAP: no differentiator supplied against either rival bidder for this capability]."

## PF-2.14

✗ "Kestrel Systems Group will complete the migration within Halverton Mutual's 8-month examination window."
✓ "Kestrel Systems Group's own most comparable prior migration programme ran 14 months, longer than Halverton Mutual's 8-month examination window — [PF-2.14 REVIEW (commitment): confirm the proposed timeline against that comparable duration before this date is promised]."

## PF-2.15

✗ "Our 14-month migration for a comparable regulated insurer proves we can deliver this on schedule."
✓ "Kestrel Systems Group's own most comparable prior migration programme ran 14 months — [PF-2.15 REVIEW (reference): confirm that prior client has agreed to be cited before this comparison ships]."

## PF-2.16

✗ "Ardent Digital manages 62% of the estate today and cannot deliver the governance boundary Halverton Mutual needs — only Kestrel Systems Group can."
✓ "Kestrel Systems Group delivers landing-zone governance through account-level guardrails across the new account structure — [PF-2.16 REVIEW (competitor): confirm no claim about the incumbent's capability is implied before this ships]."

## PF-2.17

✗ "Kestrel Systems Group meets Halverton Mutual's SOC 2 Type II requirement."
✓ "Kestrel Systems Group holds a SOC 2 Type I report today; Halverton Mutual's RFP requires Type II. Kestrel's Type II observation window closes after the 2026-10-30 submission date — [PF-2.17 REVIEW (compliance): confirm this gap is acceptable to the buyer before this ships]."

## PF-3.1

✗ "A robust, enterprise-grade landing zone governs every account."
✓ "A landing zone governed by account-level guardrails replaces 850 ungoverned virtual machines with one governance boundary."

## PF-3.2

✗ "An enterprise-grade AWS Control Tower deployment governs the new account structure."
✓ "An AWS Control Tower deployment governs the new account structure across Halverton Mutual's 850 virtual machines."

## PF-3.3

✗ "The proposal replaces ungoverned VM sprawl with a landing zone that will be fully governed from day one."
✓ "The proposal replaces ungoverned VM sprawl with a landing zone [PF-3.3: customer's term, retained — Marcus Feld, discovery] that will be fully governed from day one — [PF-2.14 REVIEW (commitment): confirm 'fully governed from day one' before this ships]."

## MC-1

✗ "The migration will reduce operating costs and improve settlement performance across the estate."
✓ "Diane Osoria states the current annual run rate at $2,300,000. Halverton Mutual has never measured how far the settlement batch job overruns its required window — [MC-1 GAP: no measured baseline for the settlement batch overrun]."

## MC-6

✗ "This proposal addresses Halverton Mutual's leadership team, who value cost efficiency and operational excellence across the organization."
✓ "Diane Osoria, Halverton Mutual's Chief Financial Officer, states her own priority directly: 'the current annual run rate down from $2,300,000 — that is the number I answer for.'"

## MC-11

✗ "This proposal is evaluated on Kestrel Systems Group's overall value to Halverton Mutual."
✓ "Halverton Mutual scores bidders 55% on technical approach, 25% on commercial model, and 20% on security posture, and separately weights its five RFP questions from 15% to 30% each."

## MC-16

✗ "This proposal will be reviewed alongside the leading alternatives before Halverton Mutual decides."
✓ "Three bidders are shortlisted; proposals are due 2026-10-30, and every bidder is scored against the same five questions inside the 8-month window before Halverton Mutual's next regulatory examination."

## MC-21

✗ "The proposal moves quickly to signature once Halverton Mutual approves it."
✓ "The proposal clears a security review (15 business days), a procurement review with no duration Halverton Mutual has stated, and a legal review (10 business days) before signature — [MC-21 GAP: no duration stated for the procurement review]."

## MC-26

✗ "The new platform will significantly reduce settlement batch overruns."
✓ "The nightly settlement batch job regularly overruns its required 6-hour window; Halverton Mutual has never instrumented by how much — [MC-26 GAP: no measured baseline for the settlement batch overrun]."

## MC-31

✗ "Halverton Mutual's infrastructure team is supportive of this migration."
✓ "Marcus Feld, Halverton Mutual's Vice President of Infrastructure, said in discovery: 'We need a landing zone we can actually govern — right now every VM is a snowflake.'"

## MC-36

✗ "Only Kestrel Systems Group can deliver a governance boundary that actually replaces Halverton Mutual's current estate."
✓ "Halverton Mutual is weighing three bidders, including Ardent Digital, the incumbent managing 62% of the estate today, and Vantage Nine Consulting; Priya Raghunathan, the technical evaluator, has said she would rather extend the incumbent's contract than migrate."
