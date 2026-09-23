# Legal and Intellectual Property Review

Review date: 2026-09-21

Gate status: PASSED

## Executive Summary

This document records the intellectual property and provenance diligence conducted for the Proof First repository. Diligence covered trademark nominative fair use, copyright originality of expression, public source verification, and licensing compliance.

All primary sources cited in `SOURCES.md`:41-44 have been verified against public records, authorized publications, and judicial dockets. All machine-checked compliance criteria under the LEG-04 provenance gate are verified and passing.

## Trademark and Nominative Fair Use Diligence

The repository references established enterprise sales methodologies strictly for interoperability, classification, and educational fair use. Appropriate disclaimers and notices are prominently maintained in `NOTICES.md`.

### 1. Command of the Message
- **Rights Holder:** Force Management.
- **Analysis:** The repository references the core elements of message articulation as a structural framework for technical presales documentation. As recorded in `NUMBERING.md`:31-45 and `NUMBERING.md`:33-35, the seven sub-blocks reserve distinct rule numbering ranges without reproducing proprietary course materials, enablement decks, or protected training assets.
- **Attribution:** Fully attributed in `NOTICES.md` with explicit non-affiliation disclaimers.

### 2. MEDDIC, MEDDICC, and MEDDPICC
- **Rights Landscape:** The qualification methodology known across these variations is referenced to structure the 8 deal qualification checks. As documented in `skills/proof-first/references/completeness-audit.md`:12-15, the dimension blocks follow an independent numbering scheme and do not reproduce proprietary assessment rubrics.
- **Judicial Context:** Docket records (MEDDICC Ltd. v. 01 Consulting LLC, No. 2:24-cv-01836, E.D. Pa.) and USPTO TSDR registrations have been inspected. The project maintains strict descriptive use and disclaims affiliation in `NOTICES.md`.

### 3. Challenger
- **Rights Holder:** Challenger Performance Optimization, Inc. (an operating entity of Richardson Sales Performance).
- **Analysis:** Referenced for commercial teaching principles regarding constructive tension and customer-led insight in RFP responses.
- **Attribution:** Documented with corporate entity history and disclaimers in `NOTICES.md`.

## Originality of Expression and Copyright Boundary

All functional components, rule catalogs, and evaluation suites in this repository represent original authorial expression:

1. **Rule Catalogs:** The 32 Prose Discipline rules (`PF-`) and 8 Completeness Audit checks (`MC-`) are original formulations designed specifically for automated coding agents.
2. **Deletion Test and Heuristics:** The buzzword deletion test and sentence-ceiling constraints were developed independently as automated linting mechanisms.
3. **Synthetic Reference Scenario:** The worked examples in `examples/deal-brief.md` and `examples/before-after.md` center on "Halverton Mutual", a fictional composite financial institution. No confidential customer data, real commercial quotes, or proprietary vendor bids were utilized.

## Provenance and Source Verification Gate

Under rule `LEG-04`, all reference sources must be documented with stable public locators and verified retrieval dates:
- **Status:** All entries in `SOURCES.md` are marked `verified`.
- **Integrity Enforcement:** Continuous integration runs `tools/check_repo.py` to prevent unconfirmed source rows, citation drift, or attribution discrepancies.

## Licensing Conclusion

All original contributions, agent instructions, evaluation harnesses, and documentation in this repository are published under the open-source MIT License. See `LICENSE` for the complete grant.
