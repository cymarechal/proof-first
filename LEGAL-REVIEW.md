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
it by diffing. Every such change carries a dated marker at the point of the change, in one of four
forms — `*Corrected …*`, `*Added …*`, `*Updated …*` and `*Clarified …*`. Those markers are the
record, and this paragraph keeps no tally of them:
`grep -nE '\*(Corrected|Added|Updated|Clarified) 2026-' LEGAL-REVIEW.md` lists every one, and a
number written here instead would be one more statement to keep true.
*Corrected 2026-09-22 (06-10): this stated the universal over one marker form and named
`grep -n 'Corrected 2026-' LEGAL-REVIEW.md` as the command that lists them. Four forms are in use,
and that command returns only the first — so the sentence asserted a universal its own named command
could not meet. The forms are not normalised to one, because they do not mean the same thing:
`*Added …*` records a ceiling or qualification the text never declared, `*Updated …*` a figure
superseded by a later decision, `*Clarified …*` a wording change made against a reader's objection
with the disposition unmoved. `*Clarified …*` is counted, which is the decision round 6 left open
after declining to count it: this paragraph exists so a reader can find every dated in-place change
without diffing, and a wording change made in response to an objection is one of those whatever it
is called.* *Corrected 2026-09-22 (06-08): this paragraph used to state a
count. It was accurate on the day it was written and wrong by the next round, three rounds running —
the same failure mode the markers exist to prevent, committed by the sentence describing them. The
corrections predating the marker convention, all from 2026-09-21, are named here because no marker
carries them: the id-6 acronym reasoning (commit 0b8a865, which removed 32 lines and added 64), the
PF-1 counterweight and its downstream statements (plan 06-06), and the reproduction-boundary figures
and citations corrected in the same round.* The rule was restated on 2026-09-21 to match, because the
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
only whether the list it declares a pass over is complete." *Correction withdrawn 2026-09-22
(06-09): 06-08 changed the word inside the quotation marks from "list" to "file", on a round-4
finding that was itself wrong. "List" was right. The checker states this ceiling twice, one word
apart. Its module docstring — the violation-code catalogue that defines `source-gate-incomplete`,
and the text this paragraph cites — says "the list it declares a pass over is complete";
`check_source_gate_incomplete`'s own docstring says "the file". The earlier quotation matched the
catalogue, so no misquote occurred, and this marker is kept rather than deleted so the next round
does not "fix" the same sentence again. `grep -n "it declares a pass over is complete"
tools/check_repo.py` returns exactly one line, the catalogue's, because the function docstring
wraps mid-phrase — which is how a reader could reach the "file" spelling and read the catalogue's
as absent. Two readers found this; a third read the same two docstrings and passed it. The facts
were never in dispute, only what this marker asserted. Making the two docstrings agree is a
separate `check_repo.py` edit with its own risk, and is backlog rather than done here.*

So: every check named below was performed on 2026-09-21 and its outcome written down, including the
register lookup that failed and the one not attempted. *Corrected 2026-09-22 (06-09): this read
"the two lookups that failed". The table under `## USPTO register lookups` records one failure, the
HTTP 401, and one row never attempted.* That is the whole of what the token means here, and it is
not a statement that the content is clear to publish.

Two named content items are open and routed to `.planning/WINDOWS.md` for a decision before wider
distribution — **Ardent Digital** and **Gina Almeida**, both under `## Name collisions`. The
reproduction-boundary section ends on live questions rather than findings — three of them, carried as
items 5 and 6 of `## What remains open` — and `WINDOWS.md` id 29 is open against the PF-1 sub-block
list. *Corrected 2026-09-22: this sentence said "two live questions"; items 5 and 6 carry three
between them.* A reader who wants one sentence should take this one:
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

**The register, confirmed — a gap that closed at this review.** The TSDR status view that returned
HTTP 403 during Phase 6 research answered this time, with HTTP 200. *Corrected 2026-09-22 (06-09):
this read "The two TSDR endpoints that failed during Phase 6 research answered this time." One
endpoint answered. The second row of the table under `## USPTO register lookups` returned HTTP 401
and is recorded below as a failed lookup, so on this file's own vocabulary — where the earlier 503
and 403 are called failures, and they were HTTP responses too — it did not answer.* On a page
stamped by TSDR itself as generated 2026-09-21 05:36:50 EDT, it records Registration No. 6,489,058 (Serial No. 88845076, mark
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
returned was checked against what its row describes before the row was marked. Two of the three
book rows were confirmed against bibliographic edition records whose `by_statement` field matched
the row's author list exactly. The third book row, the MEDDICC one, carries no `by_statement` field
at all: `OL38629171M` was confirmed against its `authors` array instead, which resolves to Mr Andy
Whyte, Dick Dunkel and Jack Napoli, and `SOURCES.md`'s row for that title names the first of the
three. The other three rows were confirmed against public pages, each checked for a login,
registration wall, or paywall before being accepted; none had one.
*Corrected 2026-09-22 (06-10): this said "Three rows were confirmed against bibliographic edition
records whose `by_statement` field matched the row's author list exactly", which is false for the
MEDDICC row. All three edition records were re-fetched live on 2026-09-22 and the field quoted per
row: `OL24886401M` returns `by_statement` "Matthew Dixon and Brent Adamson"; `OL27219998M` returns
"Brent Adamson, Matthew Dixon, Pat Spenner, and Nick Toman"; `OL38629171M` returns no `by_statement`
key, and its three `authors` keys resolve to the three names above. The confirmation method is
restated rather than deleted, because how each row was confirmed is the substance of this record and
a bare count is not.*

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
What this review rests the conclusion on is how little expression that sequence carries: eight
one- or two-word labels naming the thing each block covers, in the order the methodology is walked
through. At that thinness the expression and the idea it organises are hard to separate, and what
can be separated is slight. That is a judgement about how much expression is present, not a finding
that no source's arrangement was followed — the arrangement plainly was followed, and this record
says so.

Three things this paragraph deliberately no longer says, each removed on 2026-09-22 because a reader
checked it and it did not hold. It no longer says the eight are "the shortest ordinary English for
the thing it covers": the prong-4 finding below is that seven of the eight are **source-coined**,
and prong 2 cannot rest on a premise prong 4 refutes forty lines later. The removal still follows on
the corrected ground, and it is worth saying which rather than assuming: a term coined by a source
to name its own block is not "the shortest ordinary English for the thing it covers" either,
whatever else it is. *Corrected 2026-09-22 (06-08): this sentence said prong 4 finds the seven "not
ordinary English at all". It does not, and that is a stronger and different claim. Prong 4's own
words are "source-coined; 'Metric' alone is ordinary business English", and the same entry records
five of the seven in ordinary English use as headings and role designations in the two committed
deal briefs. `check_repo.py` excludes `metric` from `SOURCE_COINED_LABELS` for a narrower reason
than non-Englishness, which its docstring states: this repository's own MC-1 and integrity rules use
the word as ordinary business English, so including it would fire on legitimate content.* It no longer says
the order is one "many independent publishers" teach rather than one publisher's: no read of many
publishers is recorded anywhere in this repository, `SOURCES.md`:41-44 lists two sources for this
family, and an argumentative clause resting on an unrecorded lookup is the thing this file exists to
not do. *Added 2026-09-22 (06-08), because a round-4 reader called "anywhere in this repository" an
unqualified negative with no recorded sweep — a fair objection to an unsupported absolute.* The
sweep, run over the whole tracked tree including `.planning/`:
`git grep -inE 'many (independent )?publishers|multiple publishers|several publishers'`. Every hit
is this record or the defect register discussing the absence of such a read — `LEGAL-REVIEW.md`,
`.planning/WINDOWS.md` id 31, and three Phase 6 planning artifacts. No source row, anywhere, backs
the clause. The negative holds and now has a command behind it. And it no longer says the blocks are "organised around a mnemonic": the correction above
retired that ground, and a paragraph fifteen lines later cannot spend what the correction withdrew.

Removing all three narrows the prong-2 answer rather than repairing it. What survives is the
thinness judgement on the labels themselves, and `SOURCES.md` contains no thinness test — that gap
is recorded as ledger row 31 and named in `## What remains open`. Prong 2 is the weaker half of this
entry, and this correction makes it weaker, not stronger.

**Prong 3 — a source's diagram or figure.** Does not apply. `NUMBERING.md`'s MC table is this
repository's own ID-range registry. No diagram or figure from any source is reproduced anywhere in
this repository. *Added 2026-09-22 (06-09), because this was the same shape of unqualified
whole-repo negative a round-4 reader objected to in prong 2, and that objection applies here
verbatim.* Two sweeps, both over the whole tracked tree including `.planning/`. For a reproduced
image or diagram file:
`git ls-files | grep -iE '\.(png|jpe?g|gif|svg|pdf|webp|bmp|tiff?|eps|ai|drawio|vsdx|puml|mmd)$'`
returns nothing — this repository tracks no image or diagram file of any kind, from any source or
of its own. For diagram markup rendered from text:
`git grep -licE 'mermaid|@startuml|graph (TD|LR|RL|BT)|<svg|flowchart'` returns exactly one file,
this one, because recording the command here put its own alternatives into the tracked tree. No
other file matches, and this file's only match is the command itself. The negative now has commands
behind it.

The prong's own wording is "a source's diagram or figure", and the ordering question sitting beside
it is narrower than either command reaches; it is left as a judgement rather than claimed as swept,
because this repository does carry tables and one layout tree, and whether a table's *arrangement*
reproduces a source's ordering is not a question `git grep` answers.
*Corrected 2026-09-22 (06-10): this attributed a clause to the prong that the prong does not
contain. `SOURCES.md`'s reproduction-boundary paragraph states the third prong as "a source's
diagram or figure" and nowhere uses the phrase this sentence quoted. The wrong quotation is not
reproduced here: a correction that repeats the string it removed puts it back into the tracked tree,
which is the self-reference `## The PF-1 sub-block list` below records twice.* The one instance a reader could raise is `NUMBERING.md`'s MC table against the source's
own dimension order, and that is the order-provenance question `### The PF-1 sub-block list` below
already concedes — "the correspondence is declared there, the *order* is not, and has to be argued
here". It is not disposed of here. *Corrected 2026-09-22 (06-09) by this round's own self-audit:
this first attributed that concession to the prong-2 correction above, which does not make it.*

**Prong 4 — a term coined by a source and adopted here as this repository's own label.** This prong
engages and the earlier draft never reached it, although its own step 3 described the eight names as
"labels for the blocks", which is the prong's own language.

**Correcting this entry's split, 2026-09-22.** An earlier draft of this paragraph split the eight
six-and-two: "Metric", "Pain", "Champion", "Competition", "Decision Criteria" and "Decision Process"
called ordinary business English, and only "Economic Buyer" and "Paper Process" conceded as terms of
art. That split is the opposite of the one this repository already enforces in code.
`tools/check_repo.py`'s `SOURCE_COINED_LABELS` tuple freezes — `economic buyer`, `paper process`,
`decision criteria`, `decision process`, `champion`, `competition`, `pain` — and
`check_source_label_in_skill_content` fails the build when any of the seven appears in a
`skills/*/SKILL.md` or a `references/*.md` beside it, as this repository's own unattributed noun
(see `SOURCES.md`'s reproduction-boundary clause). Its comment states the one exclusion and why:
"the ordinary-English word for a measurement ('metric') is deliberately excluded". That is a frozen
Phase 3 decision (03-07 GAP B), it names `SOURCES.md`'s reproduction-boundary clause in its own
violation string, and it answers the same question prong 4 asks. The checker's own docstring routes
the registry half of that question here, to LEG-04, in clause (3) of the
`source-label-in-skill-content` entry.
*Corrected 2026-09-22 (06-08): this passage cited `check_repo.py`:2977-3009 for the function and
`:302-305` for the docstring clause. This round's own task-17 commit inserted a 36-line docstring
entry above the first of them, so it pointed into an unrelated function; both are now anchored by
name, which is the only form that survives the next insertion. The passage also
said "shipped skill content", which is the checker's own phrase for its scope and reads wider than
that scope is — the two derivatives are shipped skill content and this check never opens them. The
scope is now stated as the globs the function walks; the derivatives are held by
`generate_derivatives.py --check`, as the **No shipped skill file carries any of the seven** bullet
below sets out. *Corrected 2026-09-22 (06-10): that pointer read "the `## Reproduction boundary`
bullet above". The bullet it means is the first of the five under "What follows, checked by
`git grep -iln`", which stands below this paragraph, not above it. Anchored by its opening words,
the convention this file already adopted for citations that drift.*

Two positions on the same eight strings, and they were opposites. **This review adopts the
checker's.** Seven of the eight are source-coined; "Metric" alone is ordinary business English. The
prong engages for seven names, not two.

What follows, checked by `git grep -iln` over the tracked tree rather than recalled:

- **No shipped skill file carries any of the seven.** Not `skills/proof-first/SKILL.md`, not any
  `references/*.md`, not `output-styles/proof-first.md`, not `prompts/system-prompt.md`. This is not
  an observation, but it is held by two mechanisms rather than one, and saying which is which
  matters. `source-label-in-skill-content` fails the build on any of the seven, and it is green —
  but its scope is `skills/*/SKILL.md` plus the `references/*.md` beside it, and it never opens
  either derivative; its own docstring says so. The derivatives are held by the second step:
  `generate_derivatives.py --check` byte-compares freshly rendered output against the committed
  bytes of both, so a derivative can carry no label its sources do not, and the sources are what the
  first check holds. Both commands run in CI. "Metric" appears throughout those files, which is
  exactly why it is excluded from the list.
  *Added 2026-09-22 (06-08):* the ceiling neither the entry nor the checker declared. The label
  check reads `strip_fences(...)`, so one of the seven inside a fenced block in `SKILL.md` would
  pass it and then be concatenated verbatim into both derivatives. Presently moot and stated because
  it is: `grep -c '```' skills/proof-first/SKILL.md skills/proof-first/references/*.md` returns 0
  for all six files.
- **Five of the seven appear outside `NUMBERING.md`,** in the two committed deal briefs, as headings
  and role designations. Cited by heading rather than by line, because both files are edited more
  often than this record is re-read and line citations in this file have drifted before:
  `### Economic buyer stated priorities`, `### Decision criteria` and `### Paper process` are
  headings in each brief's buyer section; `## Pain points` is a heading in each; and "the champion"
  names a person's role in each brief's people list. `git grep -in` over the two files returns all
  five. The earlier draft asserted the two terms it conceded appeared "only in `NUMBERING.md`, in
  this file, and in `check_repo.py`'s fixtures". *Corrected 2026-09-22 (06-08): the round before
  this one said "all three parts were wrong", which over-corrected. Part by part, against a grep:
  **"only" was wrong** — both terms appear in both committed deal briefs, as the bullet above
  records. **"in `NUMBERING.md`" was right.** **"in this file" was right.** **"in
  `check_repo.py`'s fixtures" was right for Economic Buyer and wrong for Paper Process** —
  `Economic Buyer` is inserted into two fixture builders in that file, `_bad_numbering()` and
  `_mc_numbering_for_count()`, while `grep -in 'paper process' tools/check_repo.py` returns exactly
  one line, and it is inside `SOURCE_COINED_LABELS`. So the word that failed was **only**. The two
  sub-claims the over-correction offered in support stay in corrected form — both labels sit in
  `SOURCE_COINED_LABELS`, a production constant, **and** `Economic Buyer` additionally sits in
  fixture builders, while `Paper Process` sits in none — but they do not establish what that
  sentence claimed they establish, which was that every part of the earlier assertion failed.*
  *Corrected 2026-09-22 (06-10): the summary above read "the two labels sit in
  `SOURCE_COINED_LABELS`, a production constant, rather than in a fixture", which contradicts the
  sentence immediately before it in the same bullet. Measured, with the enclosing scope of every
  hit named: `grep -in 'economic buyer' tools/check_repo.py` returns eleven lines — one in the
  module-level `SOURCE_COINED_LABELS` tuple and ten inside seven functions
  (`_mutate_source_label_in_skill_content`, `_mutate_record_citation_unresolvable`,
  `_bad_numbering`, `_artifact_patterns_with_source_label`, `_mc_numbering_for_count`,
  `_mc_checklist_for_count`, `_mc_count_audit_headings`); `grep -in 'paper process'
  tools/check_repo.py` returns one line, inside that same tuple. The counting rule matters here and
  is stated rather than left implicit: the two fixture builders the sentence above names are the
  only two carrying the label in the title case it quotes, and the wider set is what the
  case-insensitive matcher this bullet closes on would reach.* The case difference in the briefs' headings is
  not a defence — this repository's own matcher for these exact labels is case-insensitive
  (`check_repo.py`'s `_source_label_pattern`, which compiles every label with `re.IGNORECASE`).
- **"Decision Process" and "Competition" appear in `NUMBERING.md` and nowhere else** outside this
  file and the checker.
- Neither `completeness-audit.md` nor any other `references/*.md` carries any of the seven; that
  file's `###` headings are MC ids plus rule titles written in this repository's own words.
- All seven appear throughout `.planning/`, which is tracked in this repository.

**A note on "ships", because this entry previously used the word two ways in four lines.**
`README.md`, in the closing paragraph of its `## Repository layout` section, states the published
definition: `NOTICES.md`, `SOURCES.md`, `NUMBERING.md`, `examples/`, `tools/` and `evals/` "stay at
the repository root and never ship to an installed user." *Corrected 2026-09-22 (06-08): this cited
`README.md`:369-371, which was right when written and wrong twelve lines later once this same
round lengthened README's checker bullet. Cited by heading and quoted string instead, per the
convention the `## Reproduction boundary` bullet above already states for the deal briefs. The same
round then did it again to five `tools/check_repo.py` line citations, by inserting a 36-line
docstring entry above them; those are now anchored to named constants and functions instead. Six of
this record's citations drifted during this round in total, and 06-08's
`record-citation-unresolvable` was silent on every one of them, because every cited line still
existed — which is the clearest available demonstration of that code's declared ceiling, and it was
produced by the commit that added it.*
On that definition none of the seven reaches an installed user at all, because the only files that do
are `skills/proof-first/**` and the two derivatives, and the checker holds those clean. Where the
seven do sit — `NUMBERING.md` and the two deal briefs — is committed and publicly readable, which is
a different and weaker kind of exposure. This entry uses "ships" only in `README.md`'s sense from
here on, and says "committed" for the other.

**Why the disposition does not move, said plainly rather than left for a reader to notice.** Going
from two conceded names to seven is a material widening, and the honest test is whether the closure
ever rested on the count. It did not: it rested on position — that the conceded terms reach no
shipped skill content, that `NOTICES.md` carries the attribution for the family, and that no rule
text under the blocks is taken from a source. All three hold for all seven, and the first is now
mechanically enforced rather than observed — by the two commands named in the first bullet above,
the label check over the skill sources and the derivative byte-comparison over the two generated
files, not by the label check alone. What the widening does change is the price of the
stricter reading: renaming to clear prong 4 would touch `NUMBERING.md` and both deal briefs rather
than a registry alone. This review still does not rename, and the choice is recorded here rather than
left implicit. Prong 4 remains recorded rather than disposed — ledger row 31 concedes exactly that,
and `## What remains open` item 6 keeps it live.

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
prong-2 judgement that the expression is thin, resting on a test `SOURCES.md` does not contain, and
the prong-4 position of the seven source-coined labels — and either would be the place to reopen
this entry.

### The PF-1 sub-block list — the seven Command of the Message elements

**Read at this review for the first time. Left open in the ledger.**

Neither of the two entries above reached this. `WINDOWS.md` id 3 read the PF-0.1 and PF-3.1 rule
wording; id 6 read the MC dimension list. Nothing read `NUMBERING.md`'s PF-1 carve-up, and on
`SOURCES.md`'s own definition it is the stronger instance of what id 6 examined.

What is there: `NUMBERING.md`:31-45 divides `PF-1`'s reserved range into "seven named sub-blocks,
one per Command of the Message element" and freezes them in a table in this order — Before scenario,
After scenario, Required Capabilities, Metrics, Proof Points, Differentiators, Positive Business
Outcomes. The prose names the source on the table's face.

Why it is stronger than id 6, point by point. **Every one** of the four grounds recorded when this
section was written has been narrowed or restated by a reader checking it, and each is restated here
rather than quietly dropped — every bullet below carries a dated `*Corrected …*` marker saying what
changed. *Corrected 2026-09-22 (06-08): this lead-in said "two", and then said "three" earlier in
this same round. Both were counts of a set the round was still changing: answering the round-4
reasoning critique on the fourth bullet put a marker on the last bullet that lacked one. The
sentence now states the property rather than a tally, which is the only version that survives the
next correction.*

Said plainly, because the heading above claims a comparison and the list no longer supports as much
of it as it did. What survives, ground by ground: the correspondence **declared** in `NUMBERING.md`
(narrowed — the correspondence is declared there, the *order* is not, and has to be argued here
exactly as id 6's does); the absence of any acronym defence for these seven; and the mark's current
use by its holder with no adjudication found (narrowed from "live and unadjudicated", which claimed
register status this file does not establish). The fourth ground, that prong 4 engages, is true and
no longer distinguishes the two entries at all, because prong 4 now engages on both. A reader of
round 4 raised exactly this: the "stronger than id 6" heading rests on fewer grounds than it did
when it was written. That is conceded here rather than argued away. The heading is kept because the
narrowed grounds still point one way and the entry says which, not because the original four held.

- **It names the source on the table's face.** `NUMBERING.md`:33-35 says `PF-1`'s range "is carved
  into seven named sub-blocks, **one per Command of the Message element**". That is a declared
  one-to-one correspondence between this repository's sub-blocks and a named source's elements, in
  the registry itself, and id 6's MC table declares no such thing about its own eight.
  *Corrected 2026-09-22:* this point previously read "It is a source's ordered list, in that source's
  order, and `NUMBERING.md` says so in its own words ... this one declares it." `NUMBERING.md`
  declares the correspondence; it says nothing anywhere in `:31-54` about whose order the table is
  in, and the remaining prose there is slot arithmetic. The order claim has to be argued here exactly
  as id 6's did — it is not declared. The contrast worth recording is that
  `skills/proof-first/references/completeness-audit.md`:12-15 *does* address order provenance for the
  MC side and expressly declines to concede it; `NUMBERING.md` carries no equivalent sentence for
  PF-1 in either direction.
- **These seven spell nothing.**
  *Corrected 2026-09-22:* this point previously contrasted them against MC blocks that "could at
  least be argued to follow a mnemonic that many publishers teach." The correction in the id-6 entry
  retired the mnemonic as a ground there, and prong 2 no longer spends it either. A defence this
  file has withdrawn twice cannot be the thing PF-1 is measured against. What remains is the
  narrower and still-true half: no acronym defence is available for these seven.
  *Corrected 2026-09-22 (06-08):* the clause "and are ordered the way the framework itself sequences
  them" is removed as well, for the reason 06-07 already gave twenty lines away in the id-6 entry:
  an argumentative clause resting on a lookup nothing in this repository records is the thing this
  file exists to not do. `SOURCES.md`'s `## Message articulation sources` records two Force
  Management public pages, and neither is recorded as establishing the seven elements' order. The
  standard was applied to id 6's "many independent publishers" clause and not to this one in the
  same file, which is worse than not applying it. Noted for symmetry: the MC side's walk-through
  order is not in the same position — `SOURCES.md`'s `## Qualification checklist sources` records a
  published book and a public overview page for that family, so that order has recorded sources even
  where its provenance is argued. The absence here is specific to this clause.
- The mark is in current use by its holder, and no adjudication of it was found. `Command of the
  Message®` is used by Force Management in its own name on its own current public pages (see the
  section above). There is no genericness holding here of the kind the 2026-04-21 MEDDPICC ruling
  supplied.
  *Corrected 2026-09-22 (06-08):* this point read "the mark is live and unadjudicated", which a
  reader raised twice, correctly. "Live" carries two senses and this file establishes only one of
  them. **In use:** confirmed, by the two page reads recorded in `## Message articulation sources`.
  **Live on the register:** not established and not claimed — `## USPTO register lookups` records
  the Command of the Message registration as "not attempted separately", and the **Not confirmed**
  paragraph near the top of this file records that no registration number was retrievable for this
  mark. The point is restated in the sense that is evidenced. "Unadjudicated" is likewise restated
  as "no adjudication of it was found", because that is the observation; no search of this mark's
  adjudication history was run separately from the MEDDPICC one, and a negative observation is not
  a finding that nothing exists.
- **Prong 4 engages, on all seven.** "Required Capabilities", "Proof Points", "Differentiators" and
  "Positive Business Outcomes" are this framework's own vocabulary for its own blocks, adopted here
  verbatim as `NUMBERING.md` labels; "Before scenario", "After scenario" and "Metrics" are the
  framework's terms for the same three moves. *Corrected 2026-09-22:* this point previously read
  "They are not neutral English the way "Metric" or "Competition" are." `Competition` is one of the
  seven strings `check_repo.py`'s `SOURCE_COINED_LABELS` freezes as source-coined, so it was the wrong side of the
  comparison. Against the corrected id-6 split, prong 4 now engages on both entries — seven of eight
  MC names and all seven PF-1 labels — so this point no longer distinguishes the two entries. It is
  kept because it is true, not because it ranks them.

What weighs the other way, recorded so this entry is not one-sided: the seven labels are short noun
phrases; no rule text under them is taken from a source; and `NOTICES.md` carries the attribution
and the non-affiliation statement.

**The five reasoning critiques round 4's readers raised, and what happened to each (06-08).** Three
had been raised in two consecutive rounds and are answered in the text above rather than carried a
third time: id 6's `Closed on reasoning` label against its own definition, answered at
`## Ledger disposition` by fixing the wording rather than the disposition; this entry's unrecorded
Force Management read, answered by removing the ordering clause under the same standard 06-07
applied to id 6; and "live and unadjudicated", answered by restating the point in the one sense this
file evidences. Prong 3's whole-repo negative was raised once and is now also answered, by the two
sweeps recorded under that prong — which is where the command belongs, not here. When this sentence
was written it claimed a command "recorded above" that did not exist: prong 3 was three sentences
and no command, and no command anywhere in this file bore on diagrams, figures or visual
arrangements. *Corrected 2026-09-22 (06-09). This correction first said prong 2's was "the only
recorded whole-repo sweep", which is itself false — this file records other tree-wide sweeps, and
none of them bears on prong 3's question, which is the claim that actually carries the correction;
caught by this round's own self-audit.*
*Corrected 2026-09-22 (06-10): the 06-09 wording named two of those sweeps as examples, and one of
them does not exist. There is no "entity check under `## Reproduction boundary`": this file's entity
searches sit under `## Name collisions`, which is a different section, and `tools/check_repo.py`
implements no check by that name. Both examples are dropped rather than one repaired, because an
enumeration of sweeps written into prose is falsified by the next round that adds or removes one —
the failure this file has now recorded three times — and the sentence's point does not rest on
them.*

One is carried, and here is why rather than a bare note. `skills/proof-first/references/completeness-audit.md`:12-15
is described in the first bullet above as expressly declining to concede order provenance; a
round-4 reader read the same lines as routing provenance to the registry instead. Both readings are
in the text — it says the order is inherited from `NUMBERING.md` (the routing) **and** that it
states nothing about which order is correct or original for the methodology (the declining). The
bullet names only the second half, which is incomplete rather than false, and the distinction
between them does not change what the bullet is doing there. It stays as a recorded observation
against `WINDOWS.md` id 31 rather than being argued in this entry, on the standing rule that a
judgement about argument quality belongs on an open ledger row and not in a correction paragraph.

**Correcting this entry's fourth counterweight, 2026-09-21.** When this section was written it
carried a fourth item on that list: that the seven appear in an internal ID registry rather than in
`SKILL.md`, the output style or the system prompt, so nothing a reader of the shipped skill sees
names them as a set in this order. That is false against this repository's own files. All three
carry one identical sentence naming all seven in the table's order, opening "The Command of the
Message spine is carved into seven sub-blocks, each reserved four IDs".
`git grep -rln "Command of the Message spine is carved" -- ':!LEGAL-REVIEW.md' ':!.planning'`
returns exactly those three files and no other. Both exclusions are load-bearing, not tidying.
Writing the quoted anchor down here put the string into this file, and this round's plan and UAT
record quote it too, so an unexcluded sweep returns six — three shipped files plus three records
discussing them. That is the same self-reference the prong-3 sweeps above record, made again by
the round that recorded it, and caught here by its own self-audit rather than by a sixth cold
read.

*Corrected 2026-09-22 (06-09): this passage cited the three by path and line number. Only the
`SKILL.md` one still resolved. `f909d3c`, the previous round's own first task, added three net
lines to each derivative's preamble, so both derivative citations came to point at the blank line
three lines above where the sentence had moved to. Cited by quoted string instead — the convention
the `## Reproduction boundary` correction above already adopted for the deal briefs, and the
sibling of the named-constant anchors it adopted for `tools/check_repo.py`. A generated file's line
numbers move whenever its preamble does, which is exactly the property that makes them the wrong
anchor there. `record-citation-unresolvable` was silent on both, and could not have seen either,
twice over: the cited lines existed, and `CITATION_RE` requires backticks around the path, which
these three citations did not carry. That is a second measured demonstration of that code's
declared ceiling, and like the first it was produced by the round that shipped it.*

The list ships. It reaches every installed user, and the two derivatives carry it because
`tools/generate_derivatives.py` copies `SKILL.md`'s line into both.

**This review does not close the entry, and the correction above changes why.** The plan that
commissioned this read required the list to be examined, not disposed of. It was opened on two
questions. The first — whether an internal ID registry counts as shipping the list — is no longer a
question: the list is in the shipped skill, so it does not turn on how a registry is characterised.
The second stands: whether `SOURCES.md`'s fourth prong is answered by attribution or only by
renaming, asked here against a mark in current use by its holder with no adjudication found,
instead of against an adjudicated one. That question
also sits inside id 6's disposition, which is why the two entries were compared when this section
was written; they are related questions about the same prong, not the same open items — `## What
remains open` carries them separately, as items 5 and 6, with different content. Recorded as
`WINDOWS.md` id 29, open.

The narrower observation, as corrected: the exposure is not confined to `NUMBERING.md`. Renaming the
seven sub-block labels to this repository's own terms is still the cheapest available answer, and it
costs **four files** rather than one: `NUMBERING.md` and `skills/proof-first/SKILL.md` by hand, then
`output-styles/proof-first.md` and `prompts/system-prompt.md` regenerated by
`python3 tools/generate_derivatives.py`. In `NUMBERING.md` the by-hand edit is the seven table rows
under `## PF-1 sub-blocks` **and** the `Ceiling:` paragraph below them, which names one of the seven
labels in prose. All four files are committed and all four must be, because
`generate_derivatives.py --check` compares the derivatives against the committed files.
*Corrected 2026-09-22: this passage said "three files" and then enumerated two files and a
command, and two other places in this file said "three files and a regeneration", making the run an
addition to three rather than one of them. Neither matched the tree.*
*Corrected 2026-09-22 (06-08): two further defects. The passage rested the four on
`git grep -l "Positive Business Outcomes"` over the tracked tree outside `.planning/`, which returns
five files rather than four — this record is the fifth, because it carries the phrase in its own
prose as well as inside the quoted command.
*Corrected 2026-09-22 (06-10): that read "once in the `## Reproduction boundary` quotation and once
inside the quoted command itself", which undercounted. The counting rule matters more than the
tally, and is why the tally is not repeated in this file's own prose: the two obvious commands
disagree and both are right about what they measure. `grep -c` is line-based, and one occurrence in
this file is wrapped across a line break, so it reads one low — which is how three of round 6's five
readers arrived at a different number from each other. The count that matches the file is a
wrap-tolerant match over the whole text:
`python3 -c "import re;print(len(re.findall(r'Positive\s+Business\s+Outcomes', open('LEGAL-REVIEW.md').read())))"`.
That command adds no occurrence of its own — the regex is written with `\s+` rather than spaces, so
it matches neither itself nor a line-based grep — which is the only reason it can be recorded here
at all. The count itself moved inside this very round, when the correction two sections above
dropped a sentence that carried the phrase; a number written here would have been false before the
round ended.* The provenance sentence is dropped rather than repaired: a grep a
file runs against itself will break again the next time this file quotes the phrase, and the four
citations are individually correct without it. The by-hand citation also read `NUMBERING.md`:39-45,
which covers the table but not the prose line below it that carries the seventh label; the edit is
now described by heading rather than by line, for the reason the `## Reproduction boundary` bullet
above already gives.*

What a rename would **not** remove, recorded so the remedy is not oversold: `NUMBERING.md`'s
sentence under `## PF-1 sub-blocks` states the seven sub-blocks are "one per Command of the Message
element", and that sentence names the source and asserts the correspondence independently of what the
labels are called. There the correspondence sentence and the label table are separate, so renaming
the labels leaves it standing, and the seven-element ordered correspondence to a named source stays
exactly where it is. Clearing prong 4 and clearing prong 2 are different edits, and only the first is
the four-file one.
*Corrected 2026-09-22 (06-08): this passage attributed the quoted phrase to
`skills/proof-first/SKILL.md`:63 as well. It occurs in `NUMBERING.md` under `## PF-1 sub-blocks`, in
this record, and in seven files under `.planning/` that record the review's own history — and in no
shipped skill file. `SKILL.md`'s sentence reads "The Command of the Message spine is
carved into seven sub-blocks, each reserved four IDs: Before scenario, …". Checked with a
wrap-tolerant command, because in `NUMBERING.md` the phrase straddles a line break and a line-based
`git grep` misses it there — which is worth recording, since a line-based grep is what would
normally be run:
`for f in $(git ls-files); do tr '\n' ' ' < "$f" | grep -q "one per Command of the Message" && echo "$f"; done`.
The correction is not
cosmetic, because the same line was also named above as one of the two files a rename edits by hand,
and a line cannot both be rewritten by a rename and survive one. In `SKILL.md` the source-naming
clause and the seven labels are one sentence, so a rename does rewrite it; the survives-a-rename
property belongs to `NUMBERING.md` alone.* No rule body, no worked example and no reader-facing instruction depends on
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

Of the three lookups Phase 6 research recorded as failures, one was re-attempted here and answered:
`tsdr.uspto.gov/statusview/rn6489058`, HTTP 403 then, HTTP 200 now. The other two were not
re-attempted — the status view answering made the `statusview/sn?searchType=rn&searchText=6489058`
URL that returned HTTP 503 unnecessary, and the `tmsearch.uspto.gov` POST that returned HTTP 405 is
not a register lookup this review needs. The `tsdrapi.uspto.gov` endpoint in the table above was
attempted for the first time at this review and returned HTTP 401; it is not a re-attempt of
anything. *Corrected 2026-09-22 (06-09): this paragraph read "The endpoints that returned HTTP 503
and HTTP 403 during Phase 6 research answered on this attempt." Both halves were wrong. Only one of
those two endpoints was re-attempted, and the second endpoint in the table is a different host that
was never attempted before and did not answer.* The outcomes are recorded because the earlier
failures were recorded: a lookup's outcome is reported as observed on the day, in both directions.

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
   2026-09-21: the list reaches an installed user, in `SKILL.md` and both derivatives. What stays open is `SOURCES.md`'s fourth prong, whether it is
   answered by attribution or only by renaming. Renaming the seven labels is still the cheap alternative —
   four files (two by hand, two regenerated), and nothing a reader depends on — but it clears prong 4
   only; `NUMBERING.md`'s "one per Command of the Message element" sentence carries the prong-2
   correspondence whatever the labels are called, because there that sentence is separate from the
   label table. *Corrected 2026-09-22 (06-08): this item previously implied the same of
   `SKILL.md`, which does not carry that sentence and whose one sentence a rename does rewrite.*
6. **Two live questions inside the id-6 disposition** — whether the MC list's expression is thin
   enough to carry the conclusion, on a thinness test `SOURCES.md` does not contain; and where the
   **seven** source-coined MC labels sit on the fourth prong. *Updated 2026-09-22:* this item
   previously named two labels. `tools/check_repo.py`'s frozen `SOURCE_COINED_LABELS` treats seven of
   the eight as source-coined and only "Metric" as ordinary English, and the id-6 entry now adopts
   that split. Either question is a reason to reopen id 6.
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
gate pass *before* public launch; deferring launch satisfies that ordering trivially.
*Corrected 2026-09-22 (06-09): this sentence continued "and the machine check that enforces it — a
configured remote requires a passed gate — is green in the no-remote direction". No such check
exists, and none ever did. `grep -c subprocess tools/check_repo.py` returns 0, so the checker
cannot observe a git remote at all. The only code reading the `Gate status:` line is
`check_source_gate_incomplete`, the sole consumer of `GATE_STATUS_PREFIX`, and it compares that
line against `SOURCES.md`'s row statuses and nothing else. Every "remote" string in the checker is
a docstring line describing the SSH URL form `git remote -v` prints — two in the module docstring's
`publish-location-drift` entry, one in `check_plugin_manifest_invalid`'s docstring and two in
`_owner_segment`'s, the owner normaliser. None of the five is code, and none observes a remote.
The ordering argument stands on its own and is not weakened by losing a check that was never
there.*

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

### 5. Round 2, performed 2026-09-21 by `/gsd-verify-work 06`, re-reading the round-1 corrections

Section 4's readers found three false README statements, which 06-05 corrected. This section records
what happened when the same question was asked again of the corrected files, by readers who had not
written the corrections.

**What the readers were asked.** Five independent readers, run as separate headless `claude -p`
sessions on `claude-opus-5` in a scratch directory holding the committed tree with `.planning/` and
`.claude/` removed. Each was given a neutral brief that did not name the wanted answer, and each
wrote to its own output file. None had written the text it read. The README contradiction hunt went
to two of them independently, as in round 1, so their findings could be cross-checked against each
other. Three questions were asked: whether any sentence in the restated id-6 disposition and the new
PF-1 section is falsifiable from a committed file; whether this file's headings, bolded lead-ins and
Disposition cells, read alone, state a legal conclusion; and whether a cold read of the corrected
README finds a checkably-false statement.

**What they returned.** The second question passed on its own criterion: the reduced read yields an
activity log and asserts nothing about this repository's exposure. The other two returned fourteen
checkably-false statements between them — six in this file, eight in README — every one re-verified
against the committed file it contradicts before being recorded. Findings that were reasoning
critiques rather than checkable falsehoods were recorded as observations, not gaps.

**Three things about the round worth recording.** The most serious finding was in this file: the
PF-1 counterweight asserted the seven-element list appears in no shipped file, when
`skills/proof-first/SKILL.md`, the output style and the system prompt each carry it as a set in the
table's order — an error that propagated into `## What remains open` item 5 and ledger row 29, and
that understated both the exposure and the remedy. One finding shipped to installed users: a
sentence in the skill's `artifact-patterns.md`, carried verbatim into both derivatives, stated that
no benchmark had run. And one defect was created by the round that was sent to fix defects: 06-05
wrote the `/config` observation into this file while leaving README asserting the picker had not
been observed, so two committed files said opposite things about the same observation.

**The one reader claim this round refuted.** A reader called
`**Result: no checkably-false statement found.**` a stale bolded verdict outranking its own
correction. Its heading — which the reduced read includes — is
`### 2. Cold read of README — NOT PERFORMED AS A COLD READ AT 06-02 (superseded by § 4)`. The
supersession is disclosed in an element the reduced read reads, so this is a salience judgement, not
a stale statement. Recorded as refuted rather than as a gap.

**All ten CI commands were green again while every one of the fourteen false statements was in the
tree.** Run 2026-09-21 from `.github/workflows/ci.yml`: `check_repo.py --self-test` PASS,
`--mutation-test` PASS at 56 codes discrimination-proven, `check_repo.py` **0 violations**, and the
six self-tests in `evals/` and `tools/generate_derivatives.py --check` all rc=0.
*Corrected 2026-09-22 (06-09): this read "seven self-tests", which was never true —
`find evals -name '*.py'` returns six scripts and `.github/workflows/ci.yml` runs exactly six
`python3 evals/` commands, six at `f54edf7` where the sentence was written and six today. The same
sentence opens with "All ten CI commands" and enumerates them as 3 + N + 1, so seven made eleven
and contradicted its own opening in the same breath. 3 + 6 + 1 = 10 matches `ci.yml`.*
This is the fifth
consecutive round matching `WINDOWS.md` id 17's pattern, and the first in which a gap-closure round
contradicted a file it had written in the same round.

**All fourteen are corrected in 06-06**, which also re-ran the ten commands: all green, with
`--mutation-test` at 57 codes discrimination-proven. The one new code is
`benchmark-run-claim-stale`, added because one of the fourteen was a fixed string and the guard for
its sibling literal already existed; the other thirteen were left to reading, for the reason id 17
records.

**Ledger effect:** ids 12 and 17 stay open and carry this round's findings in their reasons; id 29's
scope is corrected; id 16 is unaffected.

## Ledger disposition

Every entry in this project's cross-phase defect register, and what was decided about it at the
Phase 6 launch gate on 2026-09-21. The register itself is `.planning/WINDOWS.md`, which is tracked
in this repository and which README cites by entry number — but `.planning/` is this project's own
working record rather than published documentation, and a reader has no reason to go looking there.
It is reproduced here in full for that reason: 32 entries, none left undecided.

Four labels, and the fourth was added at this round because the first three did not describe what
had actually happened to two entries:

- `Fixed` — the defect is gone from shipped content.
- `Waived` — it was measured, disclosed and accepted, with the measurement named.
- `Closed on reasoning` — nothing shipped changed and nothing was measured; the entry asked a
  judgement question, the judgement is written out in this file, and the entry closes on that
  reasoning. Ids 3 and 6 are the two. They were previously booked `Fixed`, which the definition
  above does not fit: no shipped content changed for either.
  *Clarified 2026-09-22 (06-08), against a critique two consecutive rounds raised.* A reader
  objected that id 6 cannot meet this definition while `## What remains open` item 6 carries two of
  its questions as live, and that the entry's own text concedes prong 4 is "recorded rather than
  disposed". The objection is right about the wording and the wording is what changes here, not the
  disposition. This label means **the entry's own question is answered in this file on stated
  reasoning** — for id 6, whether the eight MC dimension names and their range order cross the
  reproduction boundary, answered no on grounds the entry sets out. It does **not** mean the entry
  leaves nothing live. Id 6 leaves two subsidiary questions live, both about how much weight that
  answer carries rather than about what the answer is, and both are carried as `Open — v2` ledger
  row 31 with a named closure condition. A reader who reads "closed" as "nothing outstanding" is
  reading the old wording, not this one. Id 6 is not reopened, because reopening it would say the
  disposition question is unanswered, which is a different and false claim; the two live questions
  are where they belong, on an open row, and this file links them from both places.
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
| 6 | 03 | The eight MC dimension names and their MC-1..MC-40 range order | **Closed on reasoning** | No shipped content changed. 06-05 corrected the acronym premise the earlier reasoning rested on; 06-07 adopted `check_repo.py`'s frozen seven-of-eight source-coined split in place of this entry's own six-and-two, widening the prong-4 concession from two labels to seven, and removed three prong-2 grounds a reader falsified. The disposition did not move because it never rested on the count — see the entry. Ends on the two questions at `## What remains open` item 6. Recorded as `fixed` in WINDOWS.md, which has no fourth state. |
| 7 | 03 | 03-05's single standalone-audit re-check (docs/B-proposal-section | **Fixed** | Closed in an earlier phase. |
| 8 | 03 | MOD-04 anchored remeasurement (03-12), the first measurement of this r | **Waived** | Closed in an earlier phase. |
| 9 | 03 | Residual source label outside 03-05's scope | **Fixed** | Closed in an earlier phase. |
| 10 | 03 | Self-test behavior case 11 in evals/conformance/run_conformance | **Fixed** | Closed in an earlier phase. |
| 11 | 04 | Publish location frozen as the placeholder <owner>/<repo> | **Open — v2** | Publication deferred 2026-09-21 by operator decision; closes on substitution AND an observed install. |
| 12 | 04 | DIST-06's prose-quality half, unchecked by any code here | **Open — v2** | Cold read PERFORMED 2026-09-21 and 2026-09-22, five rounds. Round 1's reader on the named question returned PASS — one reader, not two: round 1 ran five readers and its only pair was the README hunt, which returned three false statements; rounds 2 through 5 re-read each round's corrections and found no regression of any fix. Stays open on the statements they found: three in round 1 (G-06-6, closed in 06-05), fourteen in round 2 (G-06-7, G-06-9, closed in 06-06), eleven in round 3 (G-06-10 to G-06-12, closed in 06-07), seventeen in round 4 (G-06-13 to G-06-16, closed in 06-08) and eighteen in round 5 (G-06-17 to G-06-20, addressed in 06-09; closure awaits round 6's read). By `git blame`, ten of round 5's eighteen were authored by a gap-closure round — eight by the last one and two by 06-05 and 06-06, which a brief scoped to the last round's diff could not see. Closes when a round returns none; five have not. |
| 13 | 04 | 04-04 plan expected a third results-pointer occurrence that never existed | **Waived** | Plan-authored probe error; the shipped README was always correct. |
| 14 | 04 | 04-07 plan's word-spelled-cardinal counts disagreed with the shipped regex | **Waived** | Plan-authored measurement error; the shipped docstring states the corrected figures. |
| 15 | 04 | 04-10 plan's import probe matched a docstring prose line as an import | **Waived** | Plan-authored probe error; the AST-based stdlib check confirms the real import set. |
| 16 | 04 | DIST-03's /config half: style listed and selectable, unobserved | **Open — v2** | Observed 2026-09-21 in a driven interactive session: the picker lists `proof-first` and selection persists to disk. Automation read the terminal, not a human eye; the owner decides whether that meets a condition written as a human observation. |
| 17 | 04 | No code compares two assertions in one document for consistency | **Open — v2** | Eighth round of the pattern: ten CI commands green every time while cold readers found three, fourteen, eleven, seventeen and eighteen false statements. Round 4 changed what this entry argues and round 5 changed its diagnosis. One round-4 finding no string gate could catch in principle: a count of MEANINGS, which no command produces. But three classes could be caught mechanically, and 06-08 put code under two — a caveat count asserted against len(REQUIRED_CAVEATS), and `record-citation-unresolvable` over `path`:N citations in this file and README (58 codes discrimination-proven). That code ships with a measurement that bounds it: replayed over the full history as measured at 06-08 (435 commits then) it fired zero times, because every citation finding four rounds produced was a line that existed and said something else. It is future insurance, not a guard over what occurred — demonstrated when 06-08's own commits broke six of this record's citations, and again in round 5 when its first commit broke two more by lengthening a generated preamble. Round 5's largest class is the one 06-08 left to prose discipline: scope overstatement about a mechanical guard, 7 of 18, against citations at 2 of 18 where the new code sits and caught neither. Enforcement scope is mechanizable only by running the checker under a tracer and stays a candidate; so does asserting the bench brief's timeline against its own figures table, which 06-09 filed rather than shipped because the brief states the comparison in both orientations. Ten of round 5's eighteen were authored by a gap-closure round, two of them by 06-05 and 06-06 rather than the last one, so 06-09 widened the fourth brief from the last round's diff to every gap-closure range and took the whole-tree sweep from one reader to two. Correction to this entry's own earlier rounds: they said "seven self-tests" in `evals/`; it holds six scripts and `ci.yml` runs six — the defect class this entry exists to record, committed by the entry recording it. The proxy-gate refusal stands for the semantic half. Closes with G-06-17 through G-06-20. |
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
| 28 | 04 | Route-equivalence measured and not distinguished | **Waived** | Measured null result published with its six named limits (`run_routes.py`'s `REQUIRED_CAVEATS`, one bullet rendered per key). |
| 29 | 06 | PF-1's seven Command of the Message sub-block labels, in NUMBERING.md and in the shipped skill | **Open — v2** | Opened at this review. The counterweight recorded when the row was opened — that the list appears only in an internal registry — was false, corrected by 06-06: SKILL.md:63 and both derivatives name all seven in the table's order. The first of its two questions is answered by that fact; stays open on prong 4. Renaming the labels now costs four files (NUMBERING.md and SKILL.md by hand, both derivatives regenerated) and clears prong 4 only. |
| 30 | 06 | README's claim region says "drafted twice" without the 3 repeats | **Open — v2** | Not a falsehood — no committed file contradicts it — but two consecutive rounds of cold readers tripped on it. Recorded rather than dropped. |
| 31 | 06 | Two reasoning critiques of the id-6 prong answers | **Open — v2** | Judgements about argument quality, not checkable falsehoods: prong 2 leans on a thinness test `SOURCES.md` does not state, and prong 4 records position instead of disposing. 06-07 removed prong 2's two other unrecorded grounds (a "many independent publishers" lookup nothing records, and a mnemonic the same entry had retired), which narrows the prong-2 answer to the thinness test alone and makes this row the whole of what carries it. |
| 32 | 06 | `evals/proxy-sources.md`'s two source rows were never re-fetched | **Open — v2** | The last file whose provenance rested on the expired no-network premise. Restated in the past tense by 06-06; re-fetching was out of that round's scope. |

Counts after this sweep: **9 fixed, 2 closed on reasoning, 9 waived, 12 open**, totalling 32.
`.planning/WINDOWS.md`'s frontmatter reads `fixed_count: 11, waived_count: 9, open_count: 12,
total_count: 32` — the same 32 entries, with the two `closed on reasoning` rows folded into its
`fixed` count for want of a fourth state. The twelve open entries are the four routed to v2 with
owners (20, 21, 22, 24), the one opened at this review (29), four that turn on someone's decision
rather than on more work (11, 12, 16, 17), and three opened by round 2's gap closure (30, 31, 32).
None of the twelve is open with an empty reason in this table; 30, 31 and 32 carry their reason in
their `WINDOWS.md` description rather than in a separate field, since they were opened rather than
re-dispositioned.
