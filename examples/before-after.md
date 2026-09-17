# Before and After

This file carries one document-level before/after pair for each of the four artifact families
this skill classifies, at whole-passage granularity rather than the per-rule contrast
`references/worked-examples.md` already carries — read that file for the rule-by-rule pairs.
Every fact in every example below traces to `examples/deal-brief.md`; the deal, its parties, and
its figures are invented. Every after column cites at least one rule ID allocated in
`NUMBERING.md`.

## RFP and RFI response

✗ "Kestrel Systems Group brings decades of experience delivering large-scale cloud transformations for complex, regulated enterprises across many industries. Our proven methodology and world-class team have consistently delivered exceptional outcomes for clients facing challenges like Halverton Mutual's. Before turning to the specific migration approach Question 1 asks for, it is worth noting the breadth of our platform expertise and the strength of our partner ecosystem. Our approach is comprehensive and follows industry best practices, backed by a proven cut-over methodology and rigorous testing."
✓ "Question 1, the highest-weighted scored question in this RFP at 30%, asks for the migration approach and cut-over plan. Kestrel Systems Group moves Halverton Mutual's 850-VM VMware vSphere estate and 40 Oracle Database instances to Amazon EC2 and Amazon Aurora PostgreSQL. Each cut-over runs inside its own scheduled maintenance window. Settlement-batch completion is validated against the required 6-hour window before the next cut-over proceeds."

Rules applied: PF-2.1, MC-11.

## Solution proposal

✗ "Kestrel Systems Group delivers a best-in-class, enterprise-grade cloud migration built on cutting-edge AWS services. Our solution provides comprehensive landing-zone governance, seamless data migration, and world-class operational support. Halverton Mutual can expect this transformation to be executed flawlessly, on schedule, with zero disruption to the business."
✓ "Halverton Mutual must be able to govern every account in its new estate from one place, under guardrails the team can see and enforce. AWS Control Tower delivers that governance across Halverton Mutual's on-premises estate of 850 VMware vSphere virtual machines and 40 Oracle Database instances. That estate moves onto Amazon EC2 for compute and Amazon Aurora PostgreSQL for the migrated data layer. Kestrel Systems Group holds a SOC 2 Type I report while the RFP requires Type II — [PF-2.17 REVIEW (compliance): confirm this gap is acceptable to the buyer before this ships]. Kestrel Systems Group's own most comparable prior migration programme ran 14 months, longer than Halverton Mutual's 8-month examination window — [PF-2.14 REVIEW (commitment): confirm the proposed timeline against that comparable duration before this date is promised]."

Rules applied: PF-1.9, PF-2.14, PF-2.17.

## Executive summary

✗ "Kestrel Systems Group offers a comprehensive suite of cutting-edge cloud capabilities: elastic compute, managed database services, and end-to-end landing-zone governance. This migration will significantly reduce settlement batch overruns and dramatically lower operating costs. Halverton Mutual should choose Kestrel Systems Group for this transformative migration."
✓ "Halverton Mutual's nightly settlement batch job regularly overruns its required 6-hour window, and the size of that overrun has never been measured — [PF-2.11 GAP: no measured baseline for the settlement batch overrun]. Diane Osoria, the Chief Financial Officer, is measured on bringing the current annual run rate down from $2,300,000 and on a clean regulatory examination. The migration delivers automated failover, Oracle Database licensing relief, and a landing zone the team can govern."

Rules applied: PF-0.1, PF-1.25, PF-2.11.

## Demo and discovery material

✗ "This demo showcases our platform's robust governance capabilities across your entire cloud estate. We will walk through a standard product tour highlighting landing zone automation, guardrails, and account provisioning — everything a well-architected environment needs."
✓ "Marcus Feld, Vice President of Infrastructure, said in discovery: 'We need a landing zone we can actually govern'. He added: 'Right now every VM is a snowflake'. The demo script shows AWS Control Tower delivering a landing zone the team can actually govern [PF-3.3: customer's term, retained — Marcus Feld, discovery] across representative accounts drawn from the 850-VM estate. Success is judged by whether an out-of-band change to any account is blocked, agreed with Marcus Feld's team before the session runs. Follow-up owner: the Kestrel Systems Group solutions architect who ran the session, with a written summary due before the next scheduled call — [PF-2.14 REVIEW (commitment): confirm this delivery date before it is promised]."

Rules applied: PF-3.3, PF-2.14, MC-31.
