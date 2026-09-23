# Deal Brief: Cloud Migration RFP (Fictional)

Last reviewed: 2026-09-10

This brief is entirely invented for illustration; any resemblance to a real company, person, or transaction is unintended. The migration source and target platforms named in later sections are real products, cited only where a worked example genuinely needs a concrete technical noun.

## The deal in one paragraph

Halverton Mutual, a fictional United States mid-market insurance and retirement services firm, has issued a formal scored request for proposal for a three-year programme to move its policy administration and settlement estate off on-premises VMware vSphere and Oracle Database onto Amazon Web Services. The programme is valued at $6,000,000 over the three-year term. Three bidders are shortlisted: Kestrel Systems Group, the incumbent managed-services provider Ardent Digital, and Vantage Nine Consulting. Kestrel Systems Group is the proposing integrator whose voice every worked example in this repository writes in.

## Parties

- **Halverton Mutual** (the buyer): a mid-market insurance and retirement services firm running its policy administration and settlement estate on-premises.
- **Kestrel Systems Group** (the proposing integrator): the bidder whose voice every worked example in this repository writes in.
- **Ardent Digital** (a rival bidder): the incumbent managed-services provider currently running Halverton Mutual's on-premises estate.
- **Vantage Nine Consulting** (a rival bidder): competing for the same contract.

All four parties are invented. The platform names used below (VMware vSphere, Oracle Database, Amazon EC2, Amazon Aurora PostgreSQL, and AWS Control Tower) are real products, named only as the migration's source and target, never set against each other or against a real competitor.

## Estate and target platforms

Halverton Mutual's current estate runs on VMware vSphere across 850 virtual machines, with a policy-administration and settlement data layer held in 40 Oracle Database instances. The target platform is Amazon Web Services: Amazon EC2 for compute, Amazon Aurora PostgreSQL for the migrated data layer, and AWS Control Tower for landing-zone governance across the new account structure.

## People and roles

- **Diane Osoria**: Chief Financial Officer, the economic buyer. Cares about run-rate reduction and a clean regulatory examination.
- **Marcus Feld**: Vice President of Infrastructure, the champion. Cares about a governable landing zone and an end to manual failover.
- **Priya Raghunathan**: Chief Architect, the technical evaluator. Cares about operational continuity and is openly skeptical of migrating away from the incumbent.
- **Tom Weatherly**: Procurement Lead. Cares about a clean, comparable scoring process across all three bidders.
- **Gina Almeida**: Associate General Counsel. Cares about contractual exposure in the proposed commitments.

## Pain points

- The nightly settlement batch job regularly overruns its 6-hour window, and Halverton Mutual has never instrumented by how much: there is no measured baseline for this overrun, only the fact that it happens.
- Oracle Database licensing costs are an increasing share of the estate's current annual run rate, with no ceiling in sight under the existing on-premises model.
- The VMware vSphere estate is at capacity, constraining the rollout of new policy-administration features that Marcus Feld's team wants to ship.
- Failover across the 850-VM estate is a manual process, which extends incident response time whenever a host fails.

## Timeline

Proposals are due to Halverton Mutual on 2026-10-30. Halverton Mutual's next regulatory examination opens in 8 months, and Halverton wants the Oracle estate off-premises before that window opens. Kestrel Systems Group's own most comparable prior migration programme took 14 months, longer than the examination window Halverton is working against.

## Inconvenient facts

- The settlement batch overrun pain point above has no measured baseline, so Kestrel Systems Group cannot honestly quote a before-and-after number for it in this proposal.
- Halverton Mutual's RFP requires a SOC 2 Type II report, and Kestrel Systems Group holds only a SOC 2 Type I report today; Kestrel's own Type II observation window closes after the RFP submission date.
- Priya Raghunathan, the Chief Architect and a scored technical evaluator, said in the discovery call that she would rather extend the Ardent Digital contract than run a migration.
- Halverton wants the Oracle estate off-premises before its next regulatory examination, and that examination window is shorter than Kestrel Systems Group's own comparable-programme duration.

These facts are in this brief on purpose: they give the integrity requirements real material to fire on, and they stop the shared deal from being a favorable proving ground for the benchmark.

## Customer source material

The material below is written in Halverton Mutual's own voice, not Kestrel Systems Group's: its purpose is to supply words that exist outside the sentence a later example is writing.

### Scored RFP questions

These percentages score the five RFP questions against each other and are distinct from the three top-level evaluation weights keyed in the Canonical figures table below.

| ID | Question | Weight |
|---|---|---|
| Q1 | Describe the migration approach and cut-over plan. | 30% |
| Q2 | Describe data residency and encryption controls for policyholder records. | 20% |
| Q3 | Describe the operating model after go-live. | 15% |
| Q4 | Provide evidence of comparable regulated-sector migrations. | 15% |
| Q5 | Describe the commercial model and exit provisions. | 20% |

### Discovery call quotes

- Marcus Feld: "We need a landing zone we can actually govern; right now every VM is a snowflake."
- Priya Raghunathan: "Honestly, I'd rather extend the Ardent Digital contract than gamble on a migration during an exam year."
- Diane Osoria: "I'm measured on run-rate reduction and a clean exam, not on architecture elegance."
- Tom Weatherly: "Every vendor gets scored against the same five questions: no exceptions, no side conversations."

### Economic buyer stated priorities

- "I need the current annual run rate down from $2,300,000; that is the number I answer for."
- "A clean regulatory examination matters more to me than any feature list."
- "I will not sign a contract that locks us into one vendor's commercial terms for longer than this term."

### Decision criteria

| Criterion | Weight | Stated by |
|---|---|---|
| Technical approach | 55% | Halverton Mutual (RFP scoring rubric) |
| Commercial model | 25% | Halverton Mutual (RFP scoring rubric) |
| Security posture | 20% | Halverton Mutual (RFP scoring rubric) |

### Paper process

The proposal moves through three reviews in sequence: a security review owned by Priya Raghunathan that takes 15 business days, a procurement review owned by Tom Weatherly with no fixed duration stated by Halverton Mutual, and a legal review owned by Gina Almeida that takes 10 business days.

## What this file does not own

This file carries facts only. It holds no rule content and no persuasion technique. Anything a later example asserts beyond the facts stated here is an invented fact and a defect.

## Canonical figures

Every dollar amount, date, percentage, and count cited anywhere in this repository's examples has a
row below. `tools/check_repo.py` treats this table as an interface: it fails the build if a figure
elsewhere in `examples/` has no matching row here, or if two rows in this table claim the same key.
What it matches on is the formatted value and not the key, so where two rows carry the same value (`rfp-question-weight-mid` and `rfp-security-weight` both read 20%), the check cannot tell which of
them a figure means. The key is what says that, and reading it is a reader's job rather than the
build's. This is the value-collision ceiling `unlisted-figure`'s own docstring declares, and it
declares a second one that bears on the sentence above: the check reads currency, percentages and
ISO dates only, so of the four kinds this table holds, a bare count that drifts between examples is
held by reading rather than by CI.

| Key | Value | Type | What it is |
|---|---|---|---|
| annual-run-rate-current | $2,300,000 | currency | Halverton Mutual's current annual spend running the on-premises estate |
| bidder-count | 3 | count | Number of bidders competing for the contract |
| contract-term-years | 3 | count | Length of the proposed contract term, in years |
| examination-window-months | 8 | count | Months until Halverton Mutual's next regulatory examination |
| incumbent-share-of-estate | 62% | percent | Share of the buyer's infrastructure estate the incumbent vendor currently manages |
| legal-review-days | 10 | count | Business days Halverton Mutual's legal review step is expected to take |
| oracle-database-count | 40 | count | Number of Oracle Database instances in the estate being migrated |
| rfp-commercial-weight | 25% | percent | Weight the buyer's top-level scoring rubric assigns to the commercial section of the response |
| rfp-question-weight-low | 15% | percent | Weight assigned to each of the two lowest-weighted scored RFP questions (Q3 and Q4) |
| rfp-question-weight-mid | 20% | percent | Weight assigned to each of the two mid-weighted scored RFP questions (Q2 and Q5) |
| rfp-question-weight-top | 30% | percent | Weight assigned to the highest-weighted scored RFP question (Q1) |
| rfp-security-weight | 20% | percent | Weight the buyer's top-level scoring rubric assigns to the security section of the response |
| rfp-submission-date | 2026-10-30 | date | Date proposals are due to the buyer |
| rfp-technical-weight | 55% | percent | Weight the buyer's top-level scoring rubric assigns to the technical section of the response |
| security-review-days | 15 | count | Business days Halverton Mutual's security review step is expected to take |
| settlement-batch-window-hours | 6 | count | Hours the nightly settlement batch job is required to complete within |
| total-contract-value | $6,000,000 | currency | Total contract value over the proposed term |
| vendor-comparable-duration-months | 14 | count | Duration, in months, of Kestrel Systems Group's own most comparable prior migration programme |
| vm-count | 850 | count | Number of virtual machines in the VMware vSphere estate being migrated |
