# LEGAL-REVIEW.md

Review date: 2026-09-21

Gate status: PASSED

## What this document is, and what it is not

This is a diligence record. A non-lawyer read public sources, recorded what was found, and recorded
what could not be found. It is **not legal advice**, it is not a clearance opinion, and it is not a
substitute for either. It establishes that specific checks were run against specific sources on a
named date, that their outcomes are written down, and that the repository's published statements
were reconciled against those outcomes. It establishes nothing about whether any of those statements
would survive a challenge, and nobody should rely on it as though it did.

Its companion files: `NOTICES.md` states the posture a reader is entitled to rely on; `SOURCES.md`
lists the approved sources and their provenance; this file is the dated evidence behind both. It is
append-only — later reviews add sections, they do not rewrite earlier ones.

Where a lookup failed, the failure is recorded as a failure. An unconfirmed fact is a disclosed gap,
never an assumed one.

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

**Disposition: closed, boundary not crossed.**

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
are stated publicly at this level of generality by many sources and by none exclusively.

Where the reasoning stops: this is a judgement about wording and structure, made by reading the two
rules against the definition. It is not an assertion that no source anywhere phrases a comparable
instruction similarly, and it is not a copyright opinion.

### WINDOWS.md id 6 — the eight MC dimension names and the MC-1 to MC-40 range order

**Disposition: closed, with the boundary of the reasoning stated.**

The question is narrow and real: `NUMBERING.md` freezes eight dimension blocks — Metric, Economic
Buyer, Decision Criteria, Decision Process, Paper Process, Pain, Champion, Competition — in that
order, at `MC-1` through `MC-40`. That order is the acronym's own canonical expansion order.
`SOURCES.md` says a source's own ordered list reproduced in its order is reproduction.

The reasoning, in three steps.

First, what the order is. The sequence is not an editorial arrangement this repository could have
chosen differently while keeping the acronym intact — it *is* the acronym, letter by letter. An
acronym's expansion is not an ordered list a source composed and this repository copied; it is the
only order in which the letters spell the word. Reordering the dimensions would not produce a
differently-arranged version of the same thing, it would produce a different word. That is the
distinction between reproducing someone's chosen sequence and being bound by a mnemonic's own
structure, and it is the step the id-6 entry was waiting on.

Second, what the ruling does and does not contribute. On 2026-04-21 a US federal court held that
MEDDPICC is generic — that the term names a methodology rather than identifying one source of
training services. That is a holding about **the term**, under **trademark** law. It is not a
holding about whether any expression of the methodology is protectable, and it is not a copyright
determination. Genericness of a name and protectability of an expression are separate questions
under separate bodies of law, and a review record that treated the first as settling the second
would be worse than one that says plainly it does not. The ruling therefore supports one narrow
point — that the term itself is not a source identifier the repository could be seen to be trading
on — and supports nothing further. It is also, as recorded above, under continuing motion practice.

Third, what this repository actually ships. The eight names are labels for the blocks; every audit
question underneath them is written in this repository's own words and grounded in
`examples/deal-brief.md`'s own facts. No dimension was renamed and none was reordered, which means
no arrangement decision was taken from a source either — the arrangement was determined by the
acronym before any source expressed a preference about it.

Where the reasoning stops: this disposition addresses the names and their order. It does not and
cannot establish that every future rule written under those blocks stays inside the boundary; that
remains a per-rule judgement, and `SOURCES.md` already says no tool in this stack performs it.

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

**Disposition.** One party collision and five person collisions were found. Both files already
state on their face that their parties are invented, which is the disclaimer that makes a
coincidental name a coincidence rather than a depiction. No character is attributed a real person's
biography, employer, or conduct, and no named party is set against a real competitor.

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
5. **The per-rule reproduction judgement is permanent, not closable.** `SOURCES.md` states no tool in
   this stack performs it. Every future rule added under a `PF-` or `MC-` block needs the same read
   this review gave PF-0.1, PF-3.1, and the MC block names.
6. **This record is not legal advice and never becomes it.** If this repository's exposure ever needs
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

The legal review gate itself is unaffected: it is a gate on content, not on publication, and
`Gate status: PASSED` above records that it passed on 2026-09-21. Roadmap criterion 1 asks that the
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
