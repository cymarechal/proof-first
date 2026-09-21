# LEGAL-REVIEW.md

Review date: 2026-09-21

## What this document is, and what it is not

This is a diligence record. A non-lawyer read public sources, recorded what was found, and recorded
what could not be found. It is **not legal advice**, it is not a clearance opinion, and it is not a
substitute for either. It establishes that specific checks were run against specific sources on a
named date, that their outcomes are written down, and that the repository's published statements
were reconciled against those outcomes. It establishes nothing about whether any of those statements
would survive a challenge, and nobody should rely on it as though it did.

Its companion files: `NOTICES.md` states the posture a reader is entitled to rely on; `SOURCES.md`
lists the approved sources and their provenance; this file is the dated evidence behind both. It is
append-only in its findings: later reviews add sections, and a check that was run, or was not run,
stays recorded as it was — which is why `## Human observations` sections 1 to 3 are still here under
headings marking them superseded rather than deleted when section 4 replaced them.

A statement found false against this repository's own files is the one exception, and it is
corrected in place rather than appended around. The condition is that the correction says what was
corrected, on what date, and against which file, so a reader can see the change rather than discover
it by diffing. Three corrections in this file were made on that basis: the id-6 acronym reasoning
(2026-09-21, commit 0b8a865, which removed 32 lines and added 64), the PF-1 counterweight and its
downstream statements (2026-09-21, plan 06-06), and the four reproduction-boundary figures and
citations corrected in the same round. The rule was restated on 2026-09-21 to match, because the
earlier wording forbade what this round and the one before it had already done for good reason. The
alternative considered and not taken was to keep the wording and restore each superseded passage
under a dated heading, the way sections 1 to 3 were kept. It was rejected on the distinction this
paragraph draws: a record of what was and was not done is evidence and is preserved, while a reading
that was simply wrong about a file in this repository is not evidence of anything and preserving it
raises the cost of every later read.

Where a lookup failed, the failure is recorded as a failure. An unconfirmed fact is a disclosed gap,
never an assumed one.

## What this review found, in one place

**LEG-04 source list complete. Content items still needing a decision: 2.**

Gate status: PASSED

That token is a machine-checked fact with a narrow meaning, and it sits here rather than at the top
of the file because an earlier revision put it above the disclaimer, where a skimming reader met it
before being told what this document is. `tools/check_repo.py`'s `source-gate-incomplete` code
defines what it asserts and nothing more: that no row in `SOURCES.md` still reads `unverified`. The
checker's own text says it "does not judge whether the review behind a declared pass was any good,
only whether the list it declares a pass over is complete."

So: every check named below was performed on 2026-09-21 and its outcome written down, including the
two lookups that failed. That is the whole of what the token means here, and it is not a statement
that the content is clear to publish.

Two named content items are open and routed to `.planning/WINDOWS.md` for a decision before wider
distribution — **Ardent Digital** and **Gina Almeida**, both under `## Name collisions`. The
reproduction-boundary section ends on two live questions rather than a finding, and `WINDOWS.md` id
29 is open against the PF-1 sub-block list. A reader who wants one sentence should take this one:
the diligence was done and written down by a non-lawyer, and some of it points at decisions nobody
has made yet.

## Command of the Message — Force Management

**Read on 2026-09-21:** Force Management's own public offering page
(`https://www.forcemanagement.com/offerings/b2b-sales-message-consulting`), which uses
`Command of the Message®` as the company's own mark and carries a 2026 copyright line in Force
Management's name; and a publicly bylined commentary piece by John Kaplan, a founder of the firm
(`https://www.forcemanagement.com/blog/why-sales-reps-struggle-with-metrics-in-the-sales-conversation`).

**Confirmed:** Force Management uses the mark in its own name, on its own site, currently. Both
pages are public, with no login, registration, or paywall.

**Not confirmed:** no registration number was retrievable for this mark — see the USPTO section
below for why. A search-engine aggregator reported a 2021 corporate transaction involving Force
Management; no primary source was found for it and it is therefore **not recorded as a fact**. The
statement in `NOTICES.md` names Force Management as the holder because that is what Force
Management's own current pages show.

**Changed in `NOTICES.md`:** the Rights-holder element now says the mark is used by Force Management
in its own name on its own public pages, and that no change of holder was found at this review.
`Last reviewed:` moved from 2026-09-10 to 2026-09-21.

## MEDDIC, MEDDICC, MEDDPICC and related marks

**Read on 2026-09-21:**

- CourtListener REST v4 search (`https://www.courtlistener.com/api/rest/v4/search/?q=MEDDICC&type=r`),
  and a docket-scoped query on the same API.
- The IPWatchdog press item reporting the ruling
  (`https://ipwatchdog.com/press/us-federal-court-rules-meddpicc-is-a-generic-term-orders-cancellation-of-trademark-registration/`).
- USPTO TSDR status view for Registration No. 6,489,058
  (`https://tsdr.uspto.gov/statusview/rn6489058`).

**Confirmed from the docket record:**

| Fact | Value |
|---|---|
| Caption | MEDDICC LTD. v. 01 CONSULTING LLC |
| Docket number | 2:24-cv-01836 |
| Court | U.S. District Court, E.D. Pennsylvania |
| Assigned to | Chief Judge Wendy Beetlestone |
| Date filed | 2024-04-30 |
| `dateTerminated` | null — the docket was **not** terminated when this review ran |
| Most recent docket entry seen | 2026-09-14, "Response in Opposition to Motion" |

**Confirmed from the press item:** summary judgment was granted on 2026-04-21; the court held
MEDDPICC generic as a term for a sales methodology rather than a source identifier, dismissed the
counterclaims with prejudice, and directed the USPTO to cancel Registration No. 6,489,058, held by
Darius Lahoutifard of 01 Consulting LLC.

**The register, confirmed — a gap that closed at this review.** The two TSDR endpoints that failed
during Phase 6 research answered this time. The TSDR status view, on a page stamped by TSDR itself
as generated 2026-09-21 05:36:50 EDT, records Registration No. 6,489,058 (Serial No. 88845076, mark
MEDDPICC, Principal Register, registered 2021-09-21, owner Lahoutifard Darius) with the common
status descriptor **LIVE/REGISTRATION/Issued and Active** and a most recent prosecution-history
entry dated 2026-09-21, a Section 8 six-year courtesy reminder. **No cancellation is recorded on the
register as of that observation.**

This is recorded as an observation and nothing more. A court order directing cancellation and a
register that has not yet been amended are two separate facts, and the gap between them is not
something this repository interprets. The docket's continuing activity is noted in the same spirit.

The second TSDR endpoint (`https://tsdrapi.uspto.gov/ts/cd/casestatus/rn6489058/info.json`) returned
**HTTP 401**, with a notice that an API key will be required from October 2. Recorded as a failed
lookup; it did not need to succeed, because the status view above did.

**Changed in `NOTICES.md`:** the Rights-holder element gained one paragraph recording the case, the
docket number, the court, the judge, the filing date, the 2026-04-21 ruling and its holding, the
registration number, the registrant, the docket's un-terminated state, its most recent entry date,
and the register's observed state. The two existing sentences — no claim about the outcome of any
proceeding, and a determination about one spelling not treated as covering another — are unchanged
and were verified present after the edit. `Last reviewed:` moved to 2026-09-21.

**Deliberately not done.** The holding is not extended to the MEDDIC or MEDDICC spellings. No
position is taken, stated or implied, on where the proceeding ends. The multi-party-contested
framing is retained: the proceeding reached one registration of one spelling and does not resolve
ownership across the family.

## Challenger

**Read on 2026-09-21:** `https://www.challengerinc.com/`, live and serving; and public reporting of
the September 2024 acquisition announcement.

**Confirmed:** the site is live and still Challenger-branded. Its own navigation identifies it as
"Powered by Richardson", and its own footer carries the corporate name **Challenger Performance
Optimization, Inc.** Richardson Sales Performance announced its acquisition of Challenger in
September 2024.

**Changed in `NOTICES.md`:** the Rights-holder element now names the operating corporate entity and
the acquirer as observed, and retains the successor clause. Recording both, rather than replacing
one with the other, is deliberate: the operating brand and the corporate parent are different facts
and a statement naming only one of them goes stale faster. `Last reviewed:` moved to 2026-09-21.

## Source rows

All six rows across `SOURCES.md`'s three tables read `verified` as of this review. Each carries an
absolute `https://` URL and the ISO-8601 date it was retrieved. The table is not duplicated here —
`SOURCES.md` is the record, and `source-row-unconfirmed` in `tools/check_repo.py` enforces that a
row claiming confirmation names what was read and when.

Every one of the six URLs was fetched during execution of plans 06-01 and 06-02, and the page
returned was checked against what its row describes before the row was marked. Two rows were
confirmed against bibliographic edition records whose `by_statement` field matched the row's author
list exactly. Three rows were confirmed against public vendor pages, each checked for a login,
registration wall, or paywall before being accepted; none had one.

`SOURCES.md`'s Out of bounds list was read before searching, not after. No candidate was taken from
a training portal, a paid course, a certification handout, an enablement deck, or a redistribution
of any of those. The qualification-checklist page is public overview material on a claimant's main
site; that claimant's separate training portal on a different subdomain was not used and is not
cited.

## Reproduction boundary

### WINDOWS.md id 3 — the `SOURCES.md` reproduction-boundary read against PF-0.1 and PF-3.1

**Read at this review:** PF-0.1 and PF-3.1 re-read against `SOURCES.md`'s definition. Neither
rule was changed. The entry is closed in the ledger on the reasoning below.

`SOURCES.md` defines reproduction as a contiguous run of a source's own wording, a source's own
ordered list reproduced in its order, a source's diagram, or a term coined by a source and adopted
here as this repository's own label.

PF-0.1 instructs a writer to open by restating the buyer's situation in the buyer's own words before
naming any product or vendor. PF-3.1 instructs a writer to delete a term and ask what evidence must
survive. Both were re-read against that definition at this review.

The reasoning: neither rule reproduces wording, because both are written as instructions in this
repository's own voice about what a writer should do next, not as restatements of how any source
words its own teaching. Neither reproduces an ordered list, because neither is a list — each is a
single operation. Neither adopts a coined term as this repository's own label: PF-0.1 uses "reframe",
PF-3.1 uses "the deletion test", and both are ordinary descriptive English for the operation being
performed rather than a distinctive coinage lifted from a source. The concepts underneath — that a
proposal should start from the buyer's situation, and that unevidenced abstraction should be cut —
are stated publicly at this level of generality by several of the sources `SOURCES.md` lists, which
is what was read here. This review makes no assertion about what any third party does or does not
hold.

Where the reasoning stops: this is a judgement about wording and structure, made by reading the two
rules against the definition. It is not an assertion that no source anywhere phrases a comparable
instruction similarly, and it is not a copyright opinion.

### WINDOWS.md id 6 — the eight MC dimension names and the MC-1 to MC-40 range order

**Read at this review:** the eight block names and their order re-read against `SOURCES.md`'s
four prongs, and the earlier entry's reasoning corrected where it was falsifiable. No name and no
order was changed. The entry is closed in the ledger on the reasoning below, which ends on two live
questions.

The question is narrow and real: `NUMBERING.md` freezes eight dimension blocks — Metric, Economic
Buyer, Decision Criteria, Decision Process, Paper Process, Pain, Champion, Competition — in that
order, at `MC-1` through `MC-40`. `SOURCES.md` says a source's own ordered list reproduced in its
order is reproduction. This read applies all four of `SOURCES.md`'s reproduction prongs to that
list in turn.

**Correcting the earlier reading first.** An earlier draft of this entry reasoned that the order
"*is* the acronym, letter by letter," and that reordering the blocks "would produce a different
word." Both statements are false against this repository's own registry, and the correction matters
more than the conclusion it was supporting. The eight blocks give the initials M, E, D, D, P, P, C,
C — **MEDDPPCC**, which is not MEDDIC, MEDDICC or MEDDPICC. This repository ships "Pain", not
"Identify Pain", so position 6 contributes P and not I. Nor is the sequence forced even where the
letters do line up: Decision Criteria and Decision Process both give D, and Champion and Competition
both give C, and Paper Process and Pain both give P, so six of the eight positions could be swapped
with no change to any spelling. The order is therefore a choice this repository made, at least in
part, and the prong has to be answered on that footing rather than on a mnemonic that the shipped
block names do not spell.

**Prong 1 — a contiguous run of a source's own wording.** Does not apply. The unit in question is a
row of eight labels of one or two words each in a range table. There is no run of sentence-level
wording from any source here, and each audit question written underneath the blocks is in this
repository's own words and grounded in `examples/deal-brief.md`'s own facts.

**Prong 2 — a source's own ordered list reproduced in its order.** This is the prong that engages.
The sequence does follow the conventional presentation order the qualification family is taught in.
What this review rests the conclusion on is how little expression that sequence carries. Eight
blocks, each labelled with the shortest ordinary English for the thing it covers, arranged in the
order a methodology is conventionally walked through by many independent publishers rather than
composed by one of them, and organised around a mnemonic: at that thinness, the expression and the
idea it organises are hard to separate, and what can be separated is slight. That is a judgement
about how much expression is present, not a finding that no source's arrangement was followed — the
arrangement plainly was followed, and this record says so.

**Prong 3 — a source's diagram or figure.** Does not apply. `NUMBERING.md`'s MC table is this
repository's own ID-range registry. No diagram, figure or visual arrangement from any source is
reproduced anywhere in this repository.

**Prong 4 — a term coined by a source and adopted here as this repository's own label.** This prong
engages and the earlier draft never reached it, although its own step 3 described the eight names as
"labels for the blocks", which is the prong's own language. Applied honestly, the eight split.
"Metric", "Pain", "Champion", "Competition", "Decision Criteria" and "Decision Process" are ordinary
business English that stands on its own outside this framework family. "Economic Buyer" and "Paper
Process" are not — both are terms of art this family put into circulation, and both are adopted here
verbatim as block labels. This review does not find those two off the prong. What it records instead
is where they sit: they are index terms in `NUMBERING.md`'s registry and nowhere else that ships.
Neither string occurs in `completeness-audit.md` at all — its headings are MC ids plus rule titles
written in this repository's own words — and repo-wide the two appear only in `NUMBERING.md`, in
this file, and in `check_repo.py`'s fixtures. `NOTICES.md` carries the attribution for the family,
and no rule text under them is taken from a source. That narrower fact is better for this entry than
the one it replaces, not worse: the two terms of art reach no shipped reader-facing prose. A
stricter reading of prong 4 would rename both. This review did not, and the choice is recorded here
rather than left implicit.

**What the 2026-04-21 ruling contributes.** On that date a US federal court held that MEDDPICC is
generic — that the term names a methodology rather than identifying one source of training services.
That is a holding about **the term**, under **trademark** law. It is not a holding about whether any
expression of the methodology is protectable, and it is not a copyright determination. Genericness
of a name and protectability of an expression are separate questions under separate bodies of law,
and a review record that treated the first as settling the second would be worse than one that says
plainly it does not. What the ruling supports here is narrow and confined to the trademark question
the ruling itself decided: as of that date, and subject to the continuing motion practice recorded
above, a court has held the term generic. This review draws nothing further from it, and in
particular draws nothing from it about the copyright question prongs 1 to 4 are asked under.

Where the reasoning stops: this disposition addresses the eight names and their order, and it is a
reading of this repository's files against `SOURCES.md`'s four prongs by a non-lawyer. It is not a
legal opinion and not an infringement analysis. It does not establish that every future rule written
under those blocks stays inside the boundary; that remains a per-rule judgement, and `SOURCES.md`
already says no tool in this stack performs it. Two items above are live rather than settled — the
prong-2 judgement that the expression is thin, and the prong-4 position of "Economic Buyer" and
"Paper Process" — and either would be the place to reopen this entry.

### The PF-1 sub-block list — the seven Command of the Message elements

**Read at this review for the first time. Left open in the ledger.**

Neither of the two entries above reached this. `WINDOWS.md` id 3 read the PF-0.1 and PF-3.1 rule
wording; id 6 read the MC dimension list. Nothing read `NUMBERING.md`'s PF-1 carve-up, and on
`SOURCES.md`'s own definition it is the stronger instance of what id 6 examined.

What is there: `NUMBERING.md`:31-45 divides `PF-1`'s reserved range into "seven named sub-blocks,
one per Command of the Message element" and freezes them in a table in this order — Before scenario,
After scenario, Required Capabilities, Metrics, Proof Points, Differentiators, Positive Business
Outcomes. The prose names the source on the table's face.

Why it is stronger than id 6, point by point:

- It is a source's ordered list, in that source's order, and `NUMBERING.md` says so in its own
  words. Id 6 at least had to be argued into that description; this one declares it.
- No acronym defence is available. The MC blocks could at least be argued to follow a mnemonic that
  many publishers teach; these seven spell nothing and are ordered the way the framework itself
  sequences them.
- The mark is live and unadjudicated. `Command of the Message®` is used by Force Management in its
  own name on its own current public pages (see the section above). There is no genericness holding
  here of the kind the 2026-04-21 MEDDPICC ruling supplied — no adjudication of any kind was found.
- Prong 4 engages harder. "Required Capabilities", "Proof Points", "Differentiators" and "Positive
  Business Outcomes" are this framework's own vocabulary for its own blocks, adopted here verbatim
  as `NUMBERING.md` labels. They are not neutral English the way "Metric" or "Competition" are.

What weighs the other way, recorded so this entry is not one-sided: the seven labels are short noun
phrases; no rule text under them is taken from a source; and `NOTICES.md` carries the attribution
and the non-affiliation statement.

**Correcting this entry's fourth counterweight, 2026-09-21.** When this section was written it
carried a fourth item on that list: that the seven appear in an internal ID registry rather than in
`SKILL.md`, the output style or the system prompt, so nothing a reader of the shipped skill sees
names them as a set in this order. That is false against this repository's own files. All three
carry one identical sentence naming all seven in the table's order:

    skills/proof-first/SKILL.md:63
    output-styles/proof-first.md:87
    prompts/system-prompt.md:75

The list ships. It reaches every installed user, and the two derivatives carry it because
`tools/generate_derivatives.py` copies `SKILL.md`'s line into both.

**This review does not close the entry, and the correction above changes why.** The plan that
commissioned this read required the list to be examined, not disposed of. It was opened on two
questions. The first — whether an internal ID registry counts as shipping the list — is no longer a
question: the list is in the shipped skill, so it does not turn on how a registry is characterised.
The second stands: whether `SOURCES.md`'s fourth prong is answered by attribution or only by
renaming, asked here against a live unadjudicated mark instead of an adjudicated one. That question
also sits inside id 6's disposition, which is why the two entries were compared when this section
was written; they are related questions about the same prong, not the same open items — `## What
remains open` carries them separately, as items 5 and 6, with different content. Recorded as
`WINDOWS.md` id 29, open.

The narrower observation, as corrected: the exposure is not confined to `NUMBERING.md`. Renaming the
seven sub-blocks to this repository's own terms would still remove it entirely, and it is still the
cheapest available answer, but it costs three files rather than one — `NUMBERING.md`,
`skills/proof-first/SKILL.md`, and a `python3 tools/generate_derivatives.py` run to carry the change
into both derivatives. No rule body, no worked example and no reader-facing instruction depends on
the seven labels, so nothing a reader relies on breaks. What the correction changes is the kind of
decision it is: a change to shipped content, and so a version decision, rather than an edit to an
internal registry.

## Name collisions

Every invented party and person in `examples/deal-brief.md` and `evals/benchmark/bench-deal-brief.md`
was enumerated directly from the two files and searched on 2026-09-21. Both files were counted rather
than trusted: the first carries four invented parties and five invented persons, as `WINDOWS.md` id 1
recorded; the second carries **five** parties and five persons, not four.

"Collision" below means an entity or person of that exact name was found. "Near" means a similarly
named real entity was found but not that name.

### Parties

| Name | File | Outcome |
|---|---|---|
| Halverton Mutual | `examples/deal-brief.md` | No collision. Near: GPT Halverton, Halverton Investments Ltd (dissolved 2015), and a real insurer named Halwell Mutual — one letter apart, same industry |
| Kestrel Systems Group | `examples/deal-brief.md` | No collision. Near: Kestrel Technology Group LLC, Kestrel Technology LLC, Kestrel Group |
| **Ardent Digital** | `examples/deal-brief.md` | **Collision.** A real company trading at `ardent.digital` carries this exact name, alongside Ardent Digital Media, Ardent Digital Solutions, Ardent Digital Agency LLC and Ardent Digital Marketing |
| Vantage Nine Consulting | `examples/deal-brief.md` | No collision. Near: Vantage Consulting Group, Vantage Technology Consulting Group |
| Thornfield Freight Systems | `evals/benchmark/bench-deal-brief.md` | No collision. Near: Thornfield Technical Solutions Ltd, Thornfield Group Ltd — neither in freight |
| Meridian Cloud Partners | `evals/benchmark/bench-deal-brief.md` | No collision. Near: Meridian Solutions, a real cloud MSP |
| Palisade Managed Services | `evals/benchmark/bench-deal-brief.md` | No collision. Near: Palisade Technology Solutions, a real MSP; Palisade Integrated Management Services |
| Brightline Cloud Advisors | `evals/benchmark/bench-deal-brief.md` | No collision. Near: Brightline Technologies / Brightline IT, a real MSP; BrightLine Group; Brightline Advisors |
| Anchorpoint Systems Group | `evals/benchmark/bench-deal-brief.md` | No collision, and no near match found |

### Persons

| Name | File | Outcome |
|---|---|---|
| Diane Osoria | `examples/deal-brief.md` | No collision |
| Marcus Feld | `examples/deal-brief.md` | No collision |
| **Priya Raghunathan** | `examples/deal-brief.md` | **Collision.** At least two real professionals carry this exact name, including a management consultant and a venture-capital founding partner |
| Tom Weatherly | `examples/deal-brief.md` | No collision |
| **Gina Almeida** | `examples/deal-brief.md` | **Collision, and the sharpest one.** Several real professionals carry this exact name, one of whom is an associate lawyer at an insurance group — against a brief that casts Gina Almeida as Associate General Counsel at an insurance firm. Name and role both land close |
| Renata Achebe | `evals/benchmark/bench-deal-brief.md` | No collision |
| **Oskar Lindqvist** | `evals/benchmark/bench-deal-brief.md` | **Collision.** Multiple real people, including a professional ice-hockey player, an actor, and a consultancy employee |
| **Fumiko Sato** | `evals/benchmark/bench-deal-brief.md` | **Collision.** Multiple real people, including a listed-company board member |
| Devon Okafor | `evals/benchmark/bench-deal-brief.md` | No collision |
| **Helena Marsh** | `evals/benchmark/bench-deal-brief.md` | **Collision.** A named education executive and campaigner |

**What the search returned:** one party collision and five person collisions. What the two files
state, quoted rather than characterised: each says on its face that it is invented for illustration
and that any resemblance to a real company, person, or transaction is unintended. Read against the
collisions, no character is attributed a real person's biography, employer, or conduct, and no named
party is set against a real competitor. Whether those statements are sufficient for any particular
name is a question this review does not answer.

That said, the two collisions worth acting on are **Ardent Digital** and **Gina Almeida**, and
neither is closed by this review. Ardent Digital is cast as the incumbent being displaced and a
losing rival bidder — an adverse role, against a name a real company trades under. Gina Almeida
matches a real individual on name and on professional role at once. Both are recorded here and
routed to `WINDOWS.md` as open items for a rename decision before wider distribution. The remaining
four person collisions are common-name coincidences in neutral roles and are recorded without a
recommended action.

## USPTO register lookups

| Target | Endpoint | Result |
|---|---|---|
| Reg. No. 6,489,058 status | `https://tsdr.uspto.gov/statusview/rn6489058` | **HTTP 200** — status retrieved; LIVE/REGISTRATION/Issued and Active, page generated 2026-09-21 05:36:50 EDT |
| Reg. No. 6,489,058 status | `https://tsdrapi.uspto.gov/ts/cd/casestatus/rn6489058/info.json` | **HTTP 401** — an API key will be required from October 2 |
| Command of the Message registration | not attempted separately | The same API gate applies; no registration number is recorded for this mark and none is claimed |

The endpoints that returned HTTP 503 and HTTP 403 during Phase 6 research answered on this attempt.
That is recorded because the earlier failure was recorded: a lookup's outcome is reported as
observed on the day, in both directions.

## What remains open

1. **Rename decision for `Ardent Digital`** in `examples/deal-brief.md`. An exact-name collision with
   a real trading company, in an adverse role. Routed to `WINDOWS.md`.
2. **Rename decision for `Gina Almeida`** in `examples/deal-brief.md`. An exact-name collision with a
   real individual whose profession matches the role the brief assigns. Routed to `WINDOWS.md`.
3. **The register state for Reg. No. 6,489,058 will change.** It was observed live and active on
   2026-09-21 against a court order directing its cancellation and a docket still under motion
   practice. This is a fact with a shelf life, and the next review re-reads it rather than carrying
   this one forward.
4. **No registration number is recorded for Command of the Message or for the Challenger marks.** The
   TSDR API gate blocked bulk lookup, and none was pursued through other channels. `NOTICES.md`
   makes no claim that depends on one.
5. **The PF-1 sub-block labels** — the seven Command of the Message elements frozen in
   `NUMBERING.md` and named in the same order in `skills/proof-first/SKILL.md`, the output style and
   the system prompt. Examined for the first time at this review under `## Reproduction boundary`
   and left open as `WINDOWS.md` id 29. One of the two questions it was opened on — whether an
   internal ID registry counts as shipping the list — was answered by the files themselves on
   2026-09-21: the list ships. What stays open is `SOURCES.md`'s fourth prong, whether it is
   answered by attribution or only by renaming. Renaming the seven is still the cheap alternative —
   three files and a regeneration, and nothing a reader depends on.
6. **Two live questions inside the id-6 disposition** — whether the MC list's expression is thin
   enough to carry the conclusion, and where "Economic Buyer" and "Paper Process" sit on the fourth
   prong. Either is a reason to reopen id 6.
7. **The per-rule reproduction judgement is permanent, not closable.** `SOURCES.md` states no tool in
   this stack performs it. Every future rule added under a `PF-` or `MC-` block needs the same read
   this review gave PF-0.1, PF-3.1, and the MC block names.
8. **This record is not legal advice and never becomes it.** If this repository's exposure ever needs
   a professional answer, this file is the input to that conversation, not a replacement for it.

## Launch

Decision date: 2026-09-21

Decision: **DEFER PUBLICATION.**

The operator was presented with three options at the launch checkpoint — publish to a real public
location now, create the remote private first, or defer — and chose to defer.

Nothing was substituted. The publish location in `.claude-plugin/plugin.json`,
`.claude-plugin/marketplace.json` and `README.md`'s install commands remains the disclosed
placeholder `<owner>/<repo>`, and `publish-location-drift` stays silent because all four occurrences
still agree with each other. No git remote was created. No commit left this machine.

**Why this is recorded rather than retried.** Publication is the one action in this project that
cannot be undone: a deleted public repository stays in search indexes, in forks, and in archive
snapshots. What would become permanently public here includes this diligence record, written by a
non-lawyer, naming three trademark rights-holders and describing a federal proceeding that was still
under motion practice on the review date. Deferring forecloses nothing and spends nothing.

**What stays open as a result**, stated plainly rather than absorbed into the phase's close:

| Item | State after this decision |
|---|---|
| `WINDOWS.md` id 11 — publish-location placeholder | Open. Reason updated to name this deferral and its date. Closes when a real location is substituted **and verified**. |
| DIST-01 — `npx skills add` | `implementation shipped; live-install reliability UNVERIFIED`. There is nothing to install from. |
| DIST-02 — `claude plugin marketplace add` | Same. |

The legal review gate itself is unaffected: it is a gate on content, not on publication, and the
summary above records that its checks were run and recorded on 2026-09-21. Roadmap criterion 1 asks that the
gate pass *before* public launch; deferring launch satisfies that ordering trivially and the
machine check that enforces it — a configured remote requires a passed gate — is green in the
no-remote direction.

### Install verification

**Not run. Recorded as skipped, with the reason.**

Both route observations require a repository that resolves for an unauthenticated user. With
publication deferred there is nothing to resolve against, so neither `npx skills add` nor
`claude plugin marketplace add` was run, and neither DIST-01 nor DIST-02 changes state.

A skipped verification recorded as skipped is honest. A skipped verification recorded as passed is
the defect this project has flagged twice, and it is not introduced here. These two routes have
never run end to end and this record continues to say so.

| Route | Command README prints | Status on 2026-09-21 | Verdict |
|---|---|---|---|
| 1 | `npx skills add` … | Not run — no published location to install from | Not tested |
| 2 | `claude plugin marketplace add` … | Not run — same reason | Not tested |

## Human observations

Three things about this repository cannot be checked by anything in it. Sections 1 to 3 below
record what the 06-02 review session observed and, explicitly, which of the three it could not
perform. **All three were performed later the same day by a different session; section 4 records
what they returned, and it supersedes the three "not performed" findings above.** Sections 1 to 3
are kept as written because this file is append-only, and because the reasons they give for not
performing the checks are the reasons the next session had to test rather than inherit.

### 1. Output style in the `/config` picker — NOT OBSERVED AT 06-02 (superseded by § 4)

Date: 2026-09-21. Platform: Darwin 25.6.0 (macOS). Destination directory README states:
`~/.claude/output-styles/`.

**Not performed.** `WINDOWS.md` id 16's closure condition is a human seeing the copied style listed
in Claude Code's `/config` picker and selecting it. The session executing this phase is
non-interactive and has no picker to open. Copying the file into `~/.claude/output-styles/` would
have produced the setup without the observation, so it was not done either — it would have changed
the operator's own configuration directory for no verification gain.

`04-15` already measured the part of this route that a script can reach: the style's content does
arrive in a live session, and an unrouted control on the same prompt cited none of this project's
rule markers (`evals/routes/probe/`). What stays unobserved is the single word *permanently* — that
the file appears in a picker and can be selected for a session.

**Ledger effect:** id 16 stays **open**. DIST-03 stays `implementation shipped; the delivery half is
MEASURED, the /config half UNVERIFIED`.

### 2. Cold read of README — NOT PERFORMED AS A COLD READ AT 06-02 (superseded by § 4)

Date: 2026-09-21.

**Not performed as specified.** `WINDOWS.md` id 17 records three consecutive rounds in which
`check_repo.py` reported zero violations and a cold human reader found a false sentence on the first
pass, and records the deliberate refusal to build a fuzzy-proxy gate for that class. Its method is a
reader who did not write the text. This round's README edits were written by the same agent that
would have read them, and no independent reader was available to this session, so the condition the
entry actually turns on was not met.

**What was performed instead, recorded as what it is:** an author's self-read backed by a mechanical
cross-reference of every checkable README claim against the shipped files. Twelve claims were
checked: the 31-rule catalog count against `SKILL.md`'s rule headings; the 28 worked pairs against
`worked-examples.md`; every path in the `## Repository layout` tree and every backticked path in
"What exists today" against the filesystem; all nine pooled tallies and the direction count against
`evals/benchmark/RESULTS.md`'s rendered tables; the trigger summary against
`evals/trigger/RESULTS-trigger.md`'s totals; and the absence of the two sentences 06-03 superseded.

**Result: no checkably-false statement found.** Four apparent findings all proved to be defects in
the checking script rather than in README — three compared a README figure against the first
matching row in `RESULTS.md`, which is a per-cell row rather than the pooled one, and the fourth
required the literal substrings `9 of 9` and `2 of 5` to appear in `RESULTS-trigger.md`, which
expresses the same totals per row and in a `## Totals` block instead. That file's second and third
blocks record a must-fire regression, which initially read as a README omission; it is Arm A, a
treatment that was measured and then **reverted**, so README's summary correctly describes the
configuration that actually ships.

This is the same class as `WINDOWS.md` entries 13, 14, 15, 26 and 27: a verification script authored
alongside the work disagreed with correct shipped content. It is recorded rather than hidden, and it
is also the reason a self-read is not accepted as a substitute — a reader checking their own text
writes the checks that match what they meant.

**Ledger effect:** ids 12 and 17 stay **open**, with the reason naming that no cold reader was
available in this round and that a self-read was performed and found nothing checkably false.

### 3. DIST-06 prose read — PERFORMED AT 06-02, BUT NOT COLD (superseded by § 4)

Date: 2026-09-21.

Assessment by the author of this round's edits, therefore not independent. README does lead with the
before/after example: `## Before and after` is the first section after the title, and
`readme-example-lead-distance` holds its first ✗ line inside a frozen 20-line ceiling. The Install
section names four routes and states which of them resolve; after this phase's deferral it still
truthfully says the publish location is a placeholder.

One thing a cold reader should be asked specifically, and which the author is the wrong person to
judge: whether the new claim region reads as an honest report of a mixed result or as a defensive
one. It states 38 losses in its own sentence and then states the caveats — the order was chosen
deliberately — but whether it *reads* that way to someone encountering the project for the first
time is exactly the judgement this record cannot make about itself.

**Ledger effect:** id 12 stays **open**, carrying the specific question above for whoever performs the
cold read.

### 4. All three, performed 2026-09-21 by `/gsd-verify-work 06`

This section supersedes sections 1 to 3. Two of the three reasons those sections give for not
performing the checks had expired, and were re-checked rather than honoured.

**The `/config` picker — observed.** An interactive Claude Code 2.1.267 session on Darwin 25.6.0 was
driven in a pty and its rendered terminal output captured, scoped to a throwaway project's own
`.claude/output-styles/` so that no operator configuration directory was touched. The picker lists
`proof-first` as entry 7 with its `description` frontmatter rendered as the entry's summary.
Selecting it set the row to `proof-first`, the value survived closing and reopening the panel, and
it was written to `.claude/settings.local.json` as `{"outputStyle": "proof-first"}` — so it outlives
the session, which README understates rather than overstates. Two controls: pressing Esc without
confirming left the row at `default` and wrote nothing, and a run that landed on `Explanatory`
confirmed `Explanatory`. What this does not establish: the observation was made by automation
reading a terminal rather than by a human eye, on one platform, against the project-scoped directory
rather than `~/.claude/output-styles/`. `WINDOWS.md` id 16's closure condition is written as a human
observation; whoever owns that entry decides whether a captured render of the real picker satisfies
it. **Ledger effect:** id 16 stays open, with what was observed recorded in its reason.

**The cold read — performed.** Five independent readers were run as separate headless `claude -p`
sessions in a scratch directory holding only the files under review, each on a neutral brief that
did not name the wanted answer, each writing to its own output file. None had written the text it
read, and the README contradiction hunt was given to two of them independently so their findings
could be cross-checked. Every finding was re-verified against the repository before being recorded;
one was refuted on verification and is recorded as refuted.

**What the cold read returned.** Three checkably-false README statements, none of which the 06-02
self-read in section 2 found — which is the point, and is `WINDOWS.md` id 17's thesis demonstrated
for a fourth consecutive round. All ten CI commands were green while the three false statements were
in the tree. The three: README's claim that every number it carries is sourced, model- and
date-stamped and checked by `tools/check_repo.py`, which `check_repo.py`'s own docstring contradicts
for anything outside the claim region; a four-route count for `run_routes.py`, whose `ROUTES` tuple
holds three; and the superseded n=1 trigger figures carried as the recorded run. Section 2's
self-read reached the third of these and dismissed it as Arm A, the reverted treatment — the
superseding figure is Arm B, the control that ships. All three are corrected in 06-05.
**Ledger effect:** ids 12 and 17 stay open and close on those corrections; the "no reader available"
premise is cleared and must not be reused.

**The DIST-06 prose question — answered.** Section 3 named one question the author was the wrong
person to judge: whether the claim region reads as an honest report of a mixed result or a defensive
one. A reader who had not written it returned PASS — "an honest report of a mixed result, not a
burial, and not close to one" — noting that the loss is pre-announced, stated in its own sentence,
given more sentence-level prominence than the two wins, and has its cheapest excuse foreclosed.
**Ledger effect:** id 12 stays open on the three false statements above, not on this question.

## Ledger disposition

Every entry in this project's cross-phase defect register, and what was decided about it at the
Phase 6 launch gate on 2026-09-21. The register itself lives under `.planning/`, which a reader of
this repository cannot see, so it is reproduced here in full: 29 entries, none left undecided.

Four labels, and the fourth was added at this round because the first three did not describe what
had actually happened to two entries:

- `Fixed` — the defect is gone from shipped content.
- `Waived` — it was measured, disclosed and accepted, with the measurement named.
- `Closed on reasoning` — nothing shipped changed and nothing was measured; the entry asked a
  judgement question, the judgement is written out in this file, and the entry closes on that
  reasoning. Ids 3 and 6 are the two. They were previously booked `Fixed`, which the definition
  above does not fit: no shipped content changed for either.
- `Open — v2` — a real gap with a named owner and a stated closure condition, not carried as if it
  were finished.

`.planning/WINDOWS.md`'s own schema has three states, not four, so it records ids 3 and 6 as
`fixed`. The divergence is deliberate and named here rather than left for a reader to trip over:
this file's counts split them out, and `WINDOWS.md`'s fold them into `fixed`.

| id | Phase | What it records | Disposition | Why |
|---|---|---|---|---|
| 1 | 01 | Name-collision search for examples/deal-brief.md's invented names | **Fixed** | Re-run in 06-02; a collision was found and is routed as a new open item. |
| 2 | 01 | D-07/P-05 boundary check (no sentence compares two real products or co | **Fixed** | Closed in an earlier phase. |
| 3 | 02 | Reproduction-boundary read of PF-0.1/PF-3.1 against SOURCES.md | **Closed on reasoning** | No shipped content changed. Closed on 06-02's read, restated at 06-05. Recorded as `fixed` in WINDOWS.md, which has no fourth state. |
| 4 | 02 | D-31 trigger pressure-test | **Fixed** | Closed in an earlier phase. |
| 5 | 02 | CAT-08 token half | **Fixed** | Closed in an earlier phase. |
| 6 | 03 | The eight MC dimension names and their MC-1..MC-40 range order | **Closed on reasoning** | No shipped content changed. 06-05 corrected the acronym premise the earlier reasoning rested on and restated it; ends on two live questions. Recorded as `fixed` in WINDOWS.md, which has no fourth state. |
| 7 | 03 | 03-05's single standalone-audit re-check (docs/B-proposal-section | **Fixed** | Closed in an earlier phase. |
| 8 | 03 | MOD-04 anchored remeasurement (03-12), the first measurement of this r | **Waived** | Closed in an earlier phase. |
| 9 | 03 | Residual source label outside 03-05's scope | **Fixed** | Closed in an earlier phase. |
| 10 | 03 | Self-test behavior case 11 in evals/conformance/run_conformance | **Fixed** | Closed in an earlier phase. |
| 11 | 04 | Publish location frozen as the placeholder <owner>/<repo> | **Open — v2** | Publication deferred 2026-09-21 by operator decision; closes on substitution AND an observed install. |
| 12 | 04 | DIST-06's prose-quality half, unchecked by any code here | **Open — v2** | Cold read PERFORMED 2026-09-21 by two independent readers; the named question returned PASS. Stays open on the three false README statements they found (G-06-6), corrected in 06-05. |
| 13 | 04 | 04-04 plan expected a third results-pointer occurrence that never existed | **Waived** | Plan-authored probe error; the shipped README was always correct. |
| 14 | 04 | 04-07 plan's word-spelled-cardinal counts disagreed with the shipped regex | **Waived** | Plan-authored measurement error; the shipped docstring states the corrected figures. |
| 15 | 04 | 04-10 plan's import probe matched a docstring prose line as an import | **Waived** | Plan-authored probe error; the AST-based stdlib check confirms the real import set. |
| 16 | 04 | DIST-03's /config half: style listed and selectable, unobserved | **Open — v2** | Observed 2026-09-21 in a driven interactive session: the picker lists `proof-first` and selection persists to disk. Automation read the terminal, not a human eye; the owner decides whether that meets a condition written as a human observation. |
| 17 | 04 | No code compares two assertions in one document for consistency | **Open — v2** | Fourth round of the pattern, now measured: ten CI commands green while two cold readers found three false README statements. The proxy-gate refusal stands. Closes with G-06-6. |
| 18 | 05 | Name-collision search for bench-deal-brief.md's invented names | **Fixed** | Closed by 06-02's searches; the premise that this environment has no network had expired. |
| 19 | 05 | Whether the eight benchmark scenarios are realistic presales tasks | **Waived** | Backstop judgement no tool here performs; scenarios are committed and readable. |
| 20 | 05 | aggregate() pools per-order records instead of averaging pairs first | **Open — v2** | Not fixed here: the fix moves a published figure. 06-03 provably did not inherit it. |
| 21 | 05 | Raw-record key omits effort, judge_model and judge_effort | **Open — v2** | No v1 requirement depends on a re-run at a changed configuration. |
| 22 | 05 | A wholly-failed generation cell is dropped with no unscoreable count | **Open — v2** | No committed cell is affected; the risk is a future run losing one silently. |
| 23 | 05 | DISALLOWED_TOOLS omits WebSearch and WebFetch | **Waived** | Measured: web_search_requests=0 and web_fetch_requests=0 across all 96 records. |
| 24 | 02 | CAT-10 over-broad trigger description | **Open — v2** | First lever tested live and refuted, then reverted; the next lever is named. |
| 25 | 05 | README asserted its own benchmark had not run | **Fixed** | Closed by 06-03: README now states what the benchmark supports. |
| 26 | 02 | 02-10 plan's git-diff removed-lines probe always printed >=1 | **Waived** | Plan-authored probe artifact; the substantive check printed empty throughout. |
| 27 | 02 | 02-10 plan's whole-file phrase count returned 15 against 14 | **Waived** | Plan-authored probe artifact; the table-scoped count was correct at 14. |
| 28 | 04 | Route-equivalence measured and not distinguished | **Waived** | Measured null result published with its four named limits. |
| 29 | 06 | PF-1's seven Command of the Message sub-block labels, in NUMBERING.md and in the shipped skill | **Open — v2** | Opened at this review. The counterweight recorded when the row was opened — that the list appears only in an internal registry — was false, corrected by 06-06: SKILL.md:63 and both derivatives name all seven in the table's order. The first of its two questions is answered by that fact; stays open on prong 4. Renaming now costs three files and a regeneration. |

Counts after this sweep: **9 fixed, 2 closed on reasoning, 9 waived, 9 open**, totalling 29.
`.planning/WINDOWS.md`'s frontmatter reads `fixed_count: 11, waived_count: 9, open_count: 9,
total_count: 29` — the same 29 entries, with the two `closed on reasoning` rows folded into its
`fixed` count for want of a fourth state. The nine open entries are the four routed to v2 with
owners (20, 21, 22, 24), the one opened at this review (29), and four that turn on someone's
decision rather than on more work (11, 12, 16, 17). None of the nine is open with an empty
reason.
