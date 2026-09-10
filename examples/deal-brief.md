# Deal Brief: Cloud Migration RFP (Fictional)

Last reviewed: 2026-09-10

This brief is entirely invented for illustration; any resemblance to a real company, person, or transaction is unintended. The migration source and target platforms named in later sections are real products, cited only where a worked example genuinely needs a concrete technical noun.

## The deal in one paragraph

Halverton Mutual, a fictional United States mid-market insurance and retirement services firm, has issued a formal scored request for proposal for a three-year programme to move its policy administration and settlement estate off on-premises VMware vSphere and Oracle Database onto Amazon Web Services. The programme is valued at $6,000,000 over the three-year term. Three bidders are shortlisted: Kestrel Systems Group, the incumbent managed-services provider Ardent Digital, and Vantage Nine Consulting. Kestrel Systems Group is the proposing integrator whose voice every worked example in this repository writes in.

## Parties

- **Halverton Mutual** — the buyer: a mid-market insurance and retirement services firm running its policy administration and settlement estate on-premises.
- **Kestrel Systems Group** — the proposing integrator: the bidder whose voice every worked example in this repository writes in.
- **Ardent Digital** — a rival bidder and also the incumbent managed-services provider currently running Halverton Mutual's on-premises estate.
- **Vantage Nine Consulting** — a rival bidder competing for the same contract.

All four parties are invented. The platform names used below — VMware vSphere, Oracle Database, Amazon EC2, Amazon Aurora PostgreSQL, and AWS Control Tower — are real products, named only as the migration's source and target, never set against each other or against a real competitor.

## Estate and target platforms

Halverton Mutual's current estate runs on VMware vSphere across 850 virtual machines, with a policy-administration and settlement data layer held in 40 Oracle Database instances. The target platform is Amazon Web Services: Amazon EC2 for compute, Amazon Aurora PostgreSQL for the migrated data layer, and AWS Control Tower for landing-zone governance across the new account structure.

## People and roles

- **Diane Osoria** — Chief Financial Officer, the economic buyer. Cares about run-rate reduction and a clean regulatory examination.
- **Marcus Feld** — Vice President of Infrastructure, the champion. Cares about a governable landing zone and an end to manual failover.
- **Priya Raghunathan** — Chief Architect, the technical evaluator. Cares about operational continuity and is openly skeptical of migrating away from the incumbent.
- **Tom Weatherly** — Procurement Lead. Cares about a clean, comparable scoring process across all three bidders.
- **Gina Almeida** — Associate General Counsel. Cares about contractual exposure in the proposed commitments.

## Pain points

- The nightly settlement batch job regularly overruns its 6-hour window, and Halverton Mutual has never instrumented by how much — there is no measured baseline for this overrun, only the fact that it happens.
- Oracle Database licensing costs are an increasing share of the estate's current annual run rate, with no ceiling in sight under the existing on-premises model.
- The VMware vSphere estate is at capacity, constraining the rollout of new policy-administration features that Marcus Feld's team wants to ship.
- Failover across the 850-VM estate is a manual process, which extends incident response time whenever a host fails.

## Timeline

Proposals are due to Halverton Mutual on 2026-10-30. Halverton Mutual's next regulatory examination opens in 8 months, and Halverton wants the Oracle estate off-premises before that window opens. Kestrel Systems Group's own most comparable prior migration programme took 14 months — longer than the examination window Halverton is working against.

## Canonical figures

Every dollar amount, date, percentage, and count cited anywhere in this repository's examples
traces to exactly one row below. `tools/check_repo.py` treats this table as an interface: it fails
the build if a figure elsewhere in `examples/` has no matching row here, or if two rows in this
table claim the same key.

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
| rfp-security-weight | 20% | percent | Weight the buyer's top-level scoring rubric assigns to the security section of the response |
| rfp-submission-date | 2026-10-30 | date | Date proposals are due to the buyer |
| rfp-technical-weight | 55% | percent | Weight the buyer's top-level scoring rubric assigns to the technical section of the response |
| security-review-days | 15 | count | Business days Halverton Mutual's security review step is expected to take |
| settlement-batch-window-hours | 6 | count | Hours the nightly settlement batch job is required to complete within |
| total-contract-value | $6,000,000 | currency | Total contract value over the proposed term |
| vendor-comparable-duration-months | 14 | count | Duration, in months, of Kestrel Systems Group's own most comparable prior migration programme |
| vm-count | 850 | count | Number of virtual machines in the VMware vSphere estate being migrated |
