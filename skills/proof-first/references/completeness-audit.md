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

### MC-1 — Name the buyer's own measure and where its baseline came from

A document missing this dimension never names the figure the economic buyer is actually measured
on, or names one with no stated baseline to move it from. Halverton Mutual's economic buyer
states her own run-rate target directly: $2,300,000 is the number she answers for, not a
capability the vendor prefers to lead with. A metric can also be present in name and missing in
substance — the nightly settlement batch job's required window is stated, but Halverton Mutual
has never instrumented how far the job overruns it, so no baseline exists to report. A document
inventing an overrun figure for that job, instead of marking the missing baseline, has fabricated
what this dimension asks it to name honestly.

**Replace with:** the buyer's own stated figure and the source that produced it, or a
`[MC-1 GAP: what baseline is missing]` marker where the buyer's own figure was never captured.

## What this file does not do

This file is not a scoring rubric, and it is not a pass/fail gate that substitutes for a human's
judgment about whether a document is ready to send. It is not a qualification tool for a live
deal — it asks questions of a document and reports what the document does not contain; it does
not decide whether the underlying deal itself is winnable.
