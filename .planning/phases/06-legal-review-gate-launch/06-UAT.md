---
status: complete
phase: 06-legal-review-gate-launch
source: [06-VERIFICATION.md]
started: 2026-09-21
updated: 2026-09-22
rounds: 4
round_2: "06-05 gap closure — tests 7-9 re-ask tests 2, 3 and 6 of the corrected files"
round_2_result: "1 passed, 2 issues — G-06-7 and G-06-9 opened 2026-09-21"
round_3: "06-06 gap closure — tests 10-12 re-ask tests 7 and 9 of the corrected files, plus a new whole-tree sweep bound to no named file"
round_3_result: "0 passed, 3 issues — G-06-10, G-06-11 and G-06-12 opened 2026-09-22, all three closed by 06-07 the same day"
round_4: "06-07 gap closure — tests 13-16 re-ask tests 10-12 of the corrected files, plus the first run of the four-brief standing set"
round_4_result: "0 passed, 4 issues — G-06-13, G-06-14, G-06-15 and G-06-16 opened 2026-09-22; 17 findings, 10 of them authored by the closing commit"
---

## Current Test

[testing complete — round 4; 4 gaps open]

## How these six were performed

The six items were recorded as human-judgement checkpoints because the executing session could not
perform them. Two of the three stated reasons had expired by this session and were re-checked
rather than honoured:

- **"No independent reader was available"** (tests 2, 3, 4, 6). Five independent readers were run as
  separate headless `claude -p` sessions in a scratch directory holding only the files under review,
  each given a neutral brief that did not name the wanted answer, each writing to its own output
  file. None had written the text it read. Two readers were given the README contradiction hunt
  independently so their findings could be cross-checked against each other.
- **"A non-interactive session has no `/config` picker"** (test 5). An interactive Claude Code
  session was driven in a pty and its rendered terminal output captured. This observes the picker
  programmatically rather than with a human eye; what it cannot speak to is stated in the test.

Every finding a reader returned was re-verified against the repository before being recorded here.
One reader finding was refuted on verification and is recorded as refuted.

**All ten CI commands were green while the three false statements were in the tree.** Run
2026-09-21 from `.github/workflows/ci.yml`: `check_repo.py --self-test` PASS,
`--mutation-test` PASS (56 codes discrimination-proven), `check_repo.py` **0 violations**, and the
seven self-tests in `evals/` and `tools/generate_derivatives.py --check` all rc=0. This is the
fourth consecutive round matching WINDOWS.md id 17's pattern — a green mechanical gate and a false
sentence found by a reader on the first pass — and it is the argument against building a
fuzzy-proxy gate for this class, not for it.

## How tests 7-9 were performed

Round 2, 2026-09-21. Five independent readers, run as separate headless `claude -p` sessions on
`claude-opus-5` in a scratch directory holding the committed tree with `.planning/` and `.claude/`
removed, each on a neutral brief that did not name the wanted answer, each writing to its own output
file. None had written the text it read. The README contradiction hunt was given to two of them
independently, as in round 1, so their findings could be cross-checked against each other.

Every finding below was re-verified against the repository before being recorded. Findings that are
reasoning critiques rather than checkable falsehoods are recorded as observations, not gaps.

**All ten CI commands were green again while every false statement below was in the tree.** Run
2026-09-21 from `.github/workflows/ci.yml`: `check_repo.py --self-test` PASS, `--mutation-test` PASS
(56 codes discrimination-proven), `check_repo.py` **0 violations**, and the seven self-tests in
`evals/` and `tools/generate_derivatives.py --check` all rc=0. This is the fifth consecutive round
matching `WINDOWS.md` id 17's pattern.


## How tests 10-12 were performed

Round 3, 2026-09-22, against commit `034c75d`. Five independent readers, run as separate headless
`claude -p` sessions on `claude-opus-5` in five separate scratch directories, each holding its own
copy of the committed tree with `.planning/` and `.claude/` removed, each on a neutral brief that did
not name the wanted answer, each writing to its own output file. None had written the text it read.
Two briefs were given to two readers each so their findings could be cross-checked; a fifth reader
was given a whole-tree contradiction sweep bound to no single file, which is new this round.

- Readers 1 and 2 — README contradiction hunt (test 11).
- Readers 3 and 4 — `LEGAL-REVIEW.md`'s reproduction-boundary material (test 10).
- Reader 5 — any two committed files that cannot both be true (test 12).

Every finding below was re-verified against the repository before being recorded, and convergence is
noted per item. Findings that are reasoning critiques rather than checkable falsehoods are recorded
as observations, not gaps. One reader finding was adjudicated against on a 2-to-1 split and is
recorded as an observation.

**A limitation of the setup, stated because it bounds what these readers could reach.** `.planning/`
is tracked in this repository but was removed from the readers' trees, so README's two
`.planning/WINDOWS.md` cross-references (`:96`, `:153`) and `LEGAL-REVIEW.md`'s ledger provenance
were outside what any reader could check. Reader 3 said so unprompted. Those were checked by this
session instead: `WINDOWS.md` entries 16 and 24 carry what the two files cite.

**The sweep brief, recorded verbatim so the next round runs it rather than reinventing it.** This is
the one that found all three of test 12's statements, in three files six earlier readers across two
rounds had no reason to open. It costs the same as a file-scoped reader.

> You are reading a software repository you did not write. Your task: find places where two committed
> files in this repository state things that cannot both be true.
>
> Do not restrict yourself to any one file. Pay particular attention to:
> - statements about whether a measurement, benchmark, search, review or observation has or has not
>   been performed;
> - counts of anything (rules, examples, routes, runs, sessions, dimensions, files, violations);
> - descriptions of what a script or an automated check does, measured against what its code does;
> - claims about what some other file contains or does not contain;
> - statements about the environment this repository was built in.
>
> Note that skills/proof-first/SKILL.md, output-styles/proof-first.md and prompts/system-prompt.md
> carry overlapping generated text and all three ship to users: a sentence that is stale in one is
> stale in all three.
>
> For each finding: both file paths with line numbers, both quoted texts, and one sentence saying why
> they cannot both be true. Open the files and check; do not report suspicions.
>
> End with a list of what you checked and found consistent.
>
> Work only from files in this directory. Output plain text, no preamble.

The two file-scoped briefs are the round-1 and round-2 briefs unchanged, one pointed at `README.md`
and one at `LEGAL-REVIEW.md`, each asking only for statements a committed file contradicts and
requiring the reader to open that file before writing a finding down.

**The standing brief set, from round 4 on — four briefs, not three.** Recorded here by 06-07 task 12
because three rounds have each found a class the round before could not see, and the fix is the brief
set rather than any one correction:

1. `README.md` — contradiction hunt, file-scoped.
2. `LEGAL-REVIEW.md` — contradiction hunt plus reasoning critique, file-scoped.
3. **The whole-tree sweep above, bound to no named file.** Non-negotiable: it is the only brief that
   can reach a contradiction between two files neither of the first two names, and it found three
   on its first run.
4. **One brief pointed at whatever the last gap-closure round rewrote.** Four of round 3's eleven
   findings were authored by the round that was closing round 2, and two of round 2's fourteen by the
   round closing round 1. The closing round's own new sentences are the highest-yield unread surface
   in the repository, and no brief has ever been aimed at them directly.

A round that runs fewer than four is not comparable with round 3 and must not be read as cleaner
than it.

**All ten CI commands were green again while all eleven false statements below were in the tree.**
Run 2026-09-22 from `.github/workflows/ci.yml`: `check_repo.py --self-test` PASS,
`--mutation-test` PASS (57 codes discrimination-proven), `check_repo.py` **0 violations**, and the
seven self-tests in `evals/` and `tools/generate_derivatives.py --check` all rc=0. This is the sixth
consecutive round matching `WINDOWS.md` id 17's pattern, and the third in which the gap-closure round
that fixed the previous round's findings authored one of the next round's.


## How tests 13-16 were performed

Round 4, 2026-09-22, against commit `38c873b`. **Six readers across the four-brief standing set** this
repository recorded after round 3 — the first round to run it. Each reader was a separate headless
`claude -p` session on `claude-opus-5`, in its own copy of the committed tree with `.planning/` and
`.claude/` removed, on a brief that did not name the wanted answer, writing to its own output file.
None had written the text it read.

| Brief | Readers | Test |
|---|---|---|
| `README.md` contradiction hunt | 2 | 14 |
| `LEGAL-REVIEW.md` reproduction-boundary material | 2 | 13 |
| Whole-tree sweep, bound to no named file | 1 | 15 |
| **What the last gap-closure round rewrote** (new) | 1 | 16 |

The fourth brief was added because four of round 3's eleven findings were authored by the round
closing round 2. Its reader was given `RECENT-CHANGES.txt` — the 202 added lines of commit `908b90b`,
grouped by file — and asked to verify every citation, count, scope claim and absolute in them against
the tree. **It was the highest-yield reader of the round.** It justified the brief on first use.

Every finding below was re-verified against the repository before being recorded. Attribution is
`git blame` on each cited line.

**All ten CI commands were green while all seventeen false statements below were in the tree.** Run
2026-09-22 at `38c873b`: `check_repo.py --self-test` PASS, `--mutation-test` PASS (57 codes
discrimination-proven), `check_repo.py` **0 violations**, and the seven self-tests in `evals/` and
`tools/generate_derivatives.py --check` all rc=0. Seventh consecutive round of `WINDOWS.md` id 17's
pattern.

**The round's result, stated before the detail, because it reverses the trend.** Round 4 found *more*
than round 3 (17 against 11), and **ten of the seventeen are in text commit `908b90b` wrote while
closing round 3.** Round 3's corrections were verified to hold — again, by readers who did not make
them — and the round that made them introduced more defects than it closed. The `.planning/` absence
bounds what these readers could reach, as in round 3; reader 6 flagged it unprompted.


## Tests

### 1. The six confirmed sources are in bounds, and nothing was reproduced from them
expected: Every URL in SOURCES.md is public and outside the "Out of bounds" list, and no wording from any of them appears in this repository.
result: pass
evidence: |
  All six URLs fetched 2026-09-21, all HTTP 200.

  Public, no login/registration/paywall:
  - The three openlibrary.org records redirect an automated client to a `verify_human` bot
    interstitial. That is an anti-scraping challenge, not a gate: the records returned over the
    unauthenticated JSON API (`/books/<id>.json`) with title and publish date — MEDDICC (Nov 25,
    2020), The challenger sale (2011), The challenger customer (2015). The interstitial's only
    "Log In / Sign Up" text is ordinary site navigation.
  - The two forcemanagement.com pages and the meddicc.com page are public marketing pages.

  Out of bounds, checked hardest on the vendor page as the test directs: meddicc.com's own login
  link resolves to `https://mos.meddicc.com/login` — the training portal, on a different subdomain.
  SOURCES.md cites `https://meddicc.com/meddpicc-sales-methodology-and-process` and never
  `mos.meddicc.com`. The claim in LEGAL-REVIEW.md's "Source rows" section is accurate.

  Reproduction: word-shingle overlap between all six sources and SOURCES.md, NOTICES.md,
  LEGAL-REVIEW.md, README.md, NUMBERING.md, `skills/**`, `output-styles/**`, `prompts/**` and the
  phase-06 commit messages. At N=8 every hit is a title, subtitle or author list — citations by
  SOURCES.md's own rule ("Titles, publishers, URLs and dates are citations"). At N=6, with those
  citation strings excluded, exactly one residual survives across the whole corpus: the
  MEDDPICC dimension-name sequence in LEGAL-REVIEW.md. That string is the subject of test 2 and is
  adjudicated there, not here. No run of a source's own prose appears anywhere.

### 2. The reproduction-boundary reasoning for WINDOWS ids 3 and 6 is sound
expected: The id-6 acronym distinction holds, and the section engages the 2026-04-21 genericness holding correctly — neither ignoring nor over-reading it.
result: issue
reported: "The id-6 distinction does not hold as written — its load-bearing premise is false against the repository's own NUMBERING.md, and the disposition tests one of SOURCES.md's four reproduction prongs. The ruling half is sound."
severity: major
evidence: |
  **The acronym distinction — does not hold.** Three defects, each checked against NUMBERING.md:

  1. LEGAL-REVIEW.md:173-176 says the order "*is* the acronym, letter by letter". The eight blocks
     NUMBERING.md freezes are Metric, Economic Buyer, Decision Criteria, Decision Process, Paper
     Process, **Pain**, Champion, Competition. Their initials spell **M-E-D-D-P-P-C-C**. The repo
     ships "Pain", not "Identify Pain", so position 6 contributes P, not I. The shipped names do
     not spell MEDDPICC, and do not spell MEDDICC either. The premise is false.
  2. "Reordering the dimensions ... would produce a different word" is false for at least two
     swaps. Decision Criteria (MC-11-15) and Decision Process (MC-16-20) both begin with D;
     Champion (MC-31-35) and Competition (MC-36-40) both begin with C. Swapping either pair leaves
     the letter string unchanged. For those positions the order is a chosen sequence the mnemonic
     does not constrain — which is the thing SOURCES.md's definition covers.
  3. The disposition argues one of SOURCES.md's four reproduction prongs. The fourth — "a term
     coined by a source and adopted here as this repository's own label" — is never tested, even
     though the section's own third step says "The eight names are **labels** for the blocks".
     The id-3 disposition runs all its relevant prongs explicitly; id-6 does not.

  **Scope gap, larger than the item examined.** NUMBERING.md:26-40 carves PF-1 into "seven named
  sub-blocks, **one per Command of the Message element**" — Before scenario, After scenario,
  Required Capabilities, Metrics, Proof Points, Differentiators, Positive Business Outcomes — frozen
  in that order in a table. On SOURCES.md's own definition that is a source's ordered list
  reproduced in its order, for a live `®` mark with no adjudication of any kind, and no acronym
  defence is available for it. Neither id 3 (which read PF-0.1 and PF-3.1 wording) nor id 6 (which
  read the MC list) examined it.

  **The ruling half — sound.** LEGAL-REVIEW.md:180-186 states the genericness/protectability
  separation correctly and uses it to *refuse* an inference. It neither ignores the 2026-04-21
  holding nor over-reads it into copyright. One residual: the affirmative point it keeps
  (:186-188) is about "the term", but the ruling is on MEDDPICC while NUMBERING.md:9 names the
  namespace MEDDICC, and LEGAL-REVIEW.md:95-96 elsewhere refuses to extend the holding across
  spellings.

  The id-6 conclusion is probably defensible. The reasoning recorded for it is not what makes it so,
  and for an append-only diligence record whose declared value is that the reasoning is written
  down, a false load-bearing premise is the defect.

### 3. LEGAL-REVIEW.md does not read as legal advice
expected: A reader cannot come away treating any part of it — particularly the trademark sections and the reproduction-boundary dispositions — as a professional opinion.
result: issue
reported: "Independent reader's verdict: yes, a reader could reasonably come away treating parts of it as a professional opinion. The disclaimer is well written but does not reach the verdict layer, which is what a skimming reader consumes."
severity: major
evidence: |
  The opening disclaimer (:7-21) does say, in words, everything the test requires. The defect is
  structural: the document has a heavily-hedged reasoning layer and an unhedged verdict layer, and
  the verdicts are what travel.

  - `Gate status: PASSED` is **line 5** — above the disclaimer at line 7. "PASSED" on a document
    named LEGAL-REVIEW.md is clearance language. It is qualified only at :312.
  - The same header sits against :244-250, which routes Ardent Digital and Gina Almeida as open
    items needing a rename decision "before wider distribution". The gate reads PASSED while
    content items are unresolved.
  - The ledger books ids 3 and 6 as **Fixed**, which :420-421 defines as "the defect is gone from
    shipped content". No shipped content changed for either — a judgement was recorded. Under the
    file's own taxonomy these are not Fixed, and the 11/9/8 counts at :455 inherit it.
  - `Disposition: closed, boundary not crossed` (:138) is a finding of non-infringement in form.
    "Disposition" is itself a term of art for how an adjudicator resolves a matter.
  - :155 "stated publicly at this level of generality by many sources and **by none exclusively**"
    is an unbounded negative assertion about third parties' rights that the described diligence
    cannot establish — and it is broader than the walk-back three lines later at :158.
  - :187 "not a source identifier the repository could be seen to be **trading on**" applies a
    court holding to the author's own exposure, in trademark's own framing, with "therefore".
  - :240-241 "which is the disclaimer that makes a coincidental name a coincidence rather than a
    depiction" asserts that a specific mitigation is sufficient to defeat a class of claim, and the
    sentence after it enumerates elements found unmet.

  Where it holds, and this is real: the register/cancellation gap refused rather than explained
  (:78-82), "Deliberately not done" (:95-98), the aggregator report "not recorded as a fact"
  (:34-36), failed lookups recorded as failures including the HTTP 401 (:84-86, :254-258), and the
  Challenger section throughout (:100-113).

### 4. README's claim region reads as an honest report of a mixed result
expected: A technical evaluator meeting the project for the first time feels the unfavourable dimension was reported plainly rather than buried.
result: pass
evidence: |
  Independent reader's verdict: honest report of a mixed result, not a burial, and not close to one.

  - The loss is pre-announced outside the region at :163 ("The benchmark measured that directly and
    found the opposite") and then restated inside it.
  - :181 is subject-verb-number with no hedge and no lead-in clause: "On persuasive force, the
    skill-on draft lost 38 pairs."
  - The asymmetry runs *against* the project. The two favourable dimensions bundle win/tie/loss into
    one sentence each; the unfavourable one isolates the loss in its own short sentence and pushes
    the consolation figures into a second. The loss gets more sentence-level prominence, not less.
  - Caveats follow the number in a separate paragraph. Nothing pre-softens it.
  - "four pairs out of five" rounds 79.2% against the project rather than for it.
  - :183 forecloses the cheapest available excuse unprompted: "the direction is the same for both
    models rather than driven by one."
  - The proxy paragraph volunteers a second unflattering result unprompted.

  One non-blocking observation, recorded rather than actioned: the prompt-length confound at
  :191-192 is disclosed only against the losing result, but it is a property of the whole
  experiment and applies equally to the evidence and clarity wins, which carry no caveat paragraph.
  A skimmer takes away "the loss may be an artifact" without the matching "so may the wins."

### 5. The output style is listed and selectable in /config
expected: "proof-first" is listed in Claude Code's /config output-style picker and selecting it persists for the session.
result: pass
evidence: |
  Performed against Claude Code 2.1.267 on Darwin 25.6.0, in an interactive session driven in a pty
  with its rendered terminal output captured. Scoped to a throwaway project's own
  `.claude/output-styles/` — the variant README:83-84 names — so the operator's configuration
  directory was not touched.

  `/config` -> filter "output style" -> Enter -> Space opens "Preferred output style", which renders:

      ❯ 1. Default ✔
        2. Proactive
        3. Concise
        4. Explanatory
        5. Learning
        6. simple-english:simple-english
        7. proof-first — Write or check RFP and RFI responses, solution proposals, executive
           summaries, and demo or discovery documents for technical presales and bid teams. ...

  `proof-first` is listed, as entry 7, with its `description` frontmatter rendered as the entry's
  summary.

  **Selectable and persistent.** Walking the cursor down to entry 7 and pressing Enter set the row
  to `❯ Output style   proof-first`. Closing the panel, reopening `/config` and filtering again
  still read `proof-first`. It was written to disk as
  `.claude/settings.local.json` -> `{"outputStyle": "proof-first"}`, so it outlives the session
  rather than only lasting it — README:75-76 ("once selected it stays on for the whole session")
  understates this rather than overstating it.

  **Two controls, because a picker that always shows the same thing proves nothing:**
  - Opening the picker and pressing Esc without confirming left the row at `default` and wrote no
    settings file. The observed value is caused by the selection, not by the file being present.
  - An earlier run whose cursor wrapped past entry 7 landed on `Explanatory`, confirmed it, and the
    row then read `Explanatory` on reopen. The row tracks the entry actually chosen.

  What this does not establish: the observation was made by automation reading a terminal, not by a
  human eye, and it covers one platform and the project-scoped directory rather than
  `~/.claude/output-styles/`. WINDOWS.md id 16's closure condition is written as a human
  observation; whoever owns that entry decides whether a captured render of the real picker
  satisfies it.

### 6. A cold read of README by someone who did not write it
expected: No two passages of README contradict each other; particular attention to the claim region against "## Status" and against the repository-layout tree.
result: issue
reported: "Two independent cold readers, converging. Three checkably-false statements in README, each contradicted by the repository's own committed files — including one that a mechanical cross-reference had examined and dismissed."
severity: major
evidence: |
  Two readers were run independently on the same brief. Findings below are only those re-verified
  against the repository; one reader finding was refuted and is recorded as refuted.

  **Confirmed, checkably false:**

  1. **README:231-233** — "Every number this README carries is sourced from a committed results
     file under `evals/`, states the model versions and the date it was produced, and is checked by
     `tools/check_repo.py`". The checker's own docstring says the opposite, in terms
     (`tools/check_repo.py`:405-415): "The region is bounded because README legitimately carries
     numbers that are not measured claims." The 31-rule count (:120), the 28 worked pairs (:125)
     and the 14 recorded observations (:127) are sourced from no results file, carry no model
     string and no date, and are checked by neither code. Both codes named in the same sentence are
     claim-region-scoped, so the machinery cited as proof cannot reach the claim it is cited for.
     This is the most serious of the three: it is an unqualified claim about the project's own
     evidence discipline, in a project whose stated constraint is measured claims or no claims.

  2. **README:139-140** — "`evals/routes/run_routes.py` — ... measures whether **the four install
     routes** deliver equivalent behaviour". The script's own docstring line 2 says "Route-
     equivalence measurement for Proof First's **three** distribution routes", and its constant is
     `ROUTES = ('skill-on', 'style-on', 'prompt-on')`. `RESULTS-routes.md`:3 says "36 sessions
     across **3** route(s)". README's own :104 says "the three routes".

  3. **README:131-133** — cites the superseded trigger figures. It reports "the recorded run: 9 of
     9 must-fire ... and 2 of 5 near-miss" as what `RESULTS-trigger.md` holds. That file records
     three runs; WINDOWS.md entry 24 states the 2026-09-20 n=1 observation "was superseded by the
     CAT-10 gap-closure round's paired n=5 measurement", and `RESULTS-trigger.md`:166 records that
     the shipped description "still measures `OF_B/SN_B = 9/25` over-fires at n=5". Arm B is the
     shipped configuration, so a current measurement of what ships exists and README does not carry
     it. Note the self-read recorded at LEGAL-REVIEW.md:378-384 reached this exact spot and
     dismissed it as Arm A, the reverted treatment. Arm A was correctly excluded; Arm B was the
     thing missed. That is precisely the failure mode WINDOWS id 17 describes — a reader checking
     their own text writes the checks that match what they meant.

  **Confirmed, minor:**

  4. :202 "one measured v1 limitation" against the trigger over-fire (:131-133) and the skill-on
     non-activation in 3 of 12 sessions (:108), both measured, both limitations, both disclosed.
  5. :7-8 "the one shared canonical deal brief this repository ships" against
     `evals/benchmark/bench-deal-brief.md`, which the layout tree asserts exists and which does.
  6. MOD-04 given two thresholds: "names its artifact family **before drafting**" (:135-136) versus
     "before its **first rule citation**" (:202-203). `run_conformance.py`:5 says "before its first
     rule marker", so :202-203 is the accurate one.
  7. "What exists today" omits `tools/generate_derivatives.py`, `.github/workflows/ci.yml`,
     `scenarios.json`, `proxy-sources.md` and `bench-deal-brief.md`, all asserted by the layout tree
     and all present. `generate_derivatives.py` is the sharpest: :240-248 instructs the reader to
     run it.

  **Refuted on verification, recorded so it is not re-raised:** one reader argued 96 generations /
  48 pairs / 16 cells cannot be consistent. It is consistent. Counted from the committed raw
  records: 2 models x 8 scenarios = 16 cells, x 2 conditions x 3 repeats = 96 generations, and
  16 x 3 = 48 pairs. The second reader recomputed independently and also found it clean. The claim
  region does not state the 3 repeats, which is what misled the first reader — an under-
  specification, not a falsehood, and not recorded as a gap.

### 7. The id-6 disposition and the PF-1 section hold up to a reader who did not write them
expected: |
  Round 2, against `LEGAL-REVIEW.md`:186-302 and `NUMBERING.md`. Gap G-06-2 was found by a reader
  who checked the disposition's premise against the registry next to it. 06-05 restated the
  reasoning; this test asks the same question of the restatement, by a reader who did not write it.

  Specifically: (a) is any sentence in the id-6 disposition falsifiable from `NUMBERING.md`, as the
  MEDDPPCC premise was; (b) do the prong-2 and prong-4 answers actually carry the conclusion, or do
  they restate the question; (c) the PF-1 section reaches "left open" — is leaving it open the
  honest reading of its own argument, or is it a finding dressed as an open question.
result: issue
reported: "Two independent readers. The id-6 restatement is materially better and its own correction paragraph miscounts; the PF-1 section's load-bearing counterweight is false against three shipped files, and the error propagates into the ledger and into What remains open."
severity: major
evidence: |
  **(a) The PF-1 counterweight is false against three shipped files — the most serious of the six.**
  `LEGAL-REVIEW.md`:289-291 states "the list appears in an internal ID registry rather than in
  `SKILL.md`, the output style or the system prompt — nothing a reader of the shipped skill sees
  names these seven elements as a set in this order." All three named files carry the identical
  sentence, naming all seven as a set, in exactly the table's order, under the framework's name:

      skills/proof-first/SKILL.md:63
      output-styles/proof-first.md:87
      prompts/system-prompt.md:75
      "The Command of the Message spine is carved into seven sub-blocks, each reserved four IDs:
       Before scenario, After scenario, Required Capabilities, Metrics, Proof Points,
       Differentiators, and Positive Business Outcomes."

  The section enumerates the three surfaces one by one and is wrong on all three. `:299-301` inherits
  it — "the exposure ... is confined to `NUMBERING.md` ... since no shipped file cites them" — and so
  do `## What remains open` item 5 (`:383-384`, "frozen in `NUMBERING.md`") and ledger row 29
  (`:628`, "in NUMBERING.md"). This is the counterweight that justifies leaving id 29 open rather
  than acting, and the remedy it prices is understated: renaming touches `NUMBERING.md` and
  `SKILL.md` plus a `generate_derivatives.py` run, not one file.

  **(b) The correction paragraph miscounts, falsifiable from `NUMBERING.md` directly.** `:204-207`
  says Decision Criteria/Decision Process and Champion/Competition "both give" their letter, "so
  four of the eight positions could be swapped with no change to any spelling." `NUMBERING.md`:77-78
  is `Paper Process` then `Pain` — a third same-initial pair. The count is six, not four. The same
  paragraph spells M-E-D-D-P-P-C-C one sentence earlier (`:203`) and then omits the P pair from the
  list it is enumerating. The defect is inside the paragraph whose job is correcting a wrong premise,
  and commit 0b8a865's own message repeats the undercount.

  **(c) `:236-237` "block headings in `completeness-audit.md`" is false.** Neither "Economic Buyer"
  nor "Paper Process" occurs anywhere in `skills/proof-first/references/completeness-audit.md`;
  its headings are MC ids plus rule titles. Repo-wide the two strings appear only in `NUMBERING.md`,
  `check_repo.py` fixtures and `LEGAL-REVIEW.md` itself. The sentence exists to show the two conceded
  prong-4 terms have a second, more exposed home, and the second home does not exist. Note the true
  fact is narrower and better for the entry than the false one.

  **(d) `:268` cites `NUMBERING.md`:26-40 for the PF-1 carve-up.** The heading is at `:31`, the prose
  at `:33-35`, the table at `:37-45`. Line 26 is a PF-2 row of a different table, and the cited span
  ends at "After scenario", excluding five of the seven elements the same sentence then enumerates.
  Both readers found this independently. The same wrong range was carried in round 1's own evidence
  for test 2 — the error propagated from the finding into the fix.

  **(e) `:296` "are the same two live questions id 6 ends on" is contradicted by the same file.**
  `## What remains open` lists them as separate items: item 5 (`:383-387`) is registry-counts-as-
  shipping plus prong-4-attribution-vs-renaming; item 6 (`:388-390`) is MC expression thinness plus
  where Economic Buyer and Paper Process sit. Different pairs. The claimed equivalence is what
  licenses "open" rather than "closed" for id 29.

  **(f) `:16` declares the file append-only — "later reviews add sections, they do not rewrite
  earlier ones".** Commit 0b8a865 removed 32 lines and added 64, rewriting the id-6 section in place;
  the falsified acronym reasoning is gone from the file. Its substance survives in the "Correcting
  the earlier reading first" paragraph, so the record is not lost — but the file's own rule was not
  followed, and the header says so ("the earlier entry's reasoning corrected").

  **What the restatement got right, recorded so the improvement is not lost.** All four `SOURCES.md`
  prongs are now applied or explicitly excluded by name. The false MEDDPPCC premise is stated as
  corrected rather than quietly dropped, and `NUMBERING.md`:9-13 now carries the M-E-D-D-P-P-C-C
  correction itself. Prong 4 concedes "Economic Buyer" and "Paper Process" sit on the prong rather
  than finding them off it, and records the choice not to rename. The 2026-04-21 ruling paragraph is
  bounded to the trademark question. Reader 1 verified the eight names, the MC-1..MC-40 span, the
  deal-brief grounding of all eight audit questions, and the ruling/docket facts as accurate.

  **Reasoning critiques, recorded as observations rather than gaps** (not checkably false; see the
  prose-gap stopping rule): prong 2 rests on a thinness/merger judgement `SOURCES.md` does not
  contain, and its one argumentative clause ("many independent publishers") is an unrecorded lookup;
  prong 4 concedes the prong is met and then records position instead of disposing, which is
  disclosure substituted for justification against `SOURCES.md`:16's "and none of them ships";
  prong 1 answers a narrowed question ("sentence-level wording"); and `:277-279` spends an acronym
  defence that `:202-208` retracted forty lines earlier.

### 8. LEGAL-REVIEW.md's reduced read states no legal conclusion
expected: |
  Round 2, against `LEGAL-REVIEW.md`. Read the file's headings, bolded lead-ins and the ledger's
  Disposition column **alone**, skipping every line of prose. Nothing in that reduced read should
  state a legal conclusion about this repository's exposure.

  This is gap G-06-3's own test, re-run against the corrected file by a reader who did not make the
  corrections. Two specific things to judge rather than confirm: whether `Gate status: PASSED`,
  still present because `source-gate-incomplete` requires it, now reads as the narrow machine-checked
  fact the surrounding section says it is; and whether `Closed on reasoning` reads as an honest
  fourth state or as a softer word for the same closure.
result: pass
evidence: |
  Independent reader's verdict on the test as written: **the reduced read states no legal conclusion.**
  Not one heading, bolded lead-in, Disposition cell or standalone line asserts that this repository
  does or does not infringe. Every heading names a subject, every bolded lead-in names an act
  (`Read`, `Confirmed`, `Changed`, `Not performed`, `Ledger effect`), and every Disposition cell
  names a ledger state rather than a legal one. Strictly parsed, the skim yields an activity log.

  **The two things the test asked to judge rather than confirm:**

  - `Gate status: PASSED` — the move below the disclaimer did not fix what it was meant to fix. The
    reader: "Moving it down did not fix the problem; it produced exactly this reader." It is still a
    bare all-caps standalone line under a heading that promises findings, and its entire narrowing
    lives in prose the reduced read skips. Recorded as an observation, not a gap: the narrowing IS
    present, adjacent, and correct, and `source-gate-incomplete` requires the token.
  - `Closed on reasoning` — read as an honest fourth state. The reader folded it into the resolved
    bucket when counting impressions but did not find it a softer word for the same closure, and the
    `:582-595` definitions plus the named `WINDOWS.md` schema divergence were not challenged.

  **The residual, recorded and not actioned.** The reader's own summary: "the document does not lie
  to the skimmer. It just loses to them." Its honest position is carried by prose, while its
  structure hands a skimmer a PASS and a ledger where 20 of 29 rows end in a word meaning resolved.
  The one element signalling a live copying question — "This is the prong that engages" — is inline
  body text, so the three prongs that do not apply look identical to the one that does in a skim.
  Against that, the caution signals that do survive the skim are real: "This record is not legal
  advice and never becomes it.", "The per-rule reproduction judgement is permanent, not closable.",
  nine `Open — v2` cells, and `Decision: DEFER PUBLICATION.`

  One reader claim checked and partly refuted: `**Result: no checkably-false statement found.**`
  (`:495`) was called a stale bolded verdict outranking its own correction. Its heading — which the
  reduced read includes — is `### 2. Cold read of README — NOT PERFORMED AS A COLD READ AT 06-02
  (superseded by § 4)`. The supersession is disclosed in an element the reduced read reads, so this
  is a salience judgement, not a stale statement. Not recorded as a gap.

### 9. A cold read of the corrected README finds no checkably-false statement
expected: |
  Round 2, against `README.md`. Gap G-06-6 was three false statements found by two independent
  readers while all ten CI commands were green. 06-05 corrected them and self-checked. A reader who
  did not write the corrections reads README against the committed files and reports any statement
  that a file in this repository contradicts.

  Two known places to press, recorded so they are not rediscovered as new: the rewritten
  evidence-discipline paragraph at :232-247, which now makes a scoping claim about which numbers
  are enforced, and :109's activation contrast — "was not in 3 of its 12 sessions, while the output
  style and the pasted prompt are unconditionally on once selected" — where
  `evals/routes/RESULTS-routes.md`:15-17 reads style-on 11 of 12 and prompt-on 8 of 12. The second
  is already recorded as a placement judgement rather than a falsehood; a cold reader deciding
  otherwise is the finding.
result: issue
reported: "Two independent cold readers, converging on four statements; three more found by one reader each and one by the session. Seven checkably-false statements in total, each contradicted by a committed file — including one the 06-05 gap-closure round created, and one in the paragraph 06-05 rewrote to fix this exact defect class."
severity: major
evidence: |
  Two readers on the same brief, independently, as in round 1. Findings below are only those
  re-verified against the repository. Convergence is noted per item.

  **1. README says the `/config` picker has not been observed; this round's own record says it was.
  Created by 06-05.** `README.md`:86-88 — "That a Claude Code session then lists it in `/config` has
  not been observed here" — and `:89-91` — "the picker is the one link in this route nothing here
  exercises." `LEGAL-REVIEW.md`:536-541 records the observation with date, platform, harness version,
  entry position and two controls; ledger row 16 (`:615`) repeats it. Commit 36fbf6c wrote the
  observation into `LEGAL-REVIEW.md` and left README asserting the opposite. (Reader 5.)

  **2. Three shipped files still state that no benchmark has run.**
  `skills/proof-first/references/artifact-patterns.md`:144 — "no benchmark has run, and this
  repository makes measured claims or none" — carried verbatim into `output-styles/proof-first.md`:695
  and `prompts/system-prompt.md`:683. `README.md`:187 and `evals/benchmark/RESULTS.md`:1 record 96
  generations measured 2026-09-18. This is the only finding of the round that ships to an installed
  user. The guard for exactly this regression exists and matches a different literal:
  `tools/check_repo.py`:4264, `STALE_COMPARISON_CLAIM = 'No benchmark has compared'`. (Both readers.)

  **3. `README.md`:134 "three runs against the shipped skill description."**
  `evals/trigger/RESULTS-trigger.md`:101 records Arm A as a 551-character description, head-14 sha256
  `9049c7d8…`, against the shipped `d5dd651a…` carried by the other two runs, and `:152-156` records
  it reverted. Two of three, not three. README's own `:139-140` says so five lines later. (Both
  readers, and found independently by this session before either returned.)

  **4. `README.md`:43-44 — `publish-location-drift` "fails the build if any command or manifest
  carrying it stops agreeing with the others."** `tools/check_repo.py`:724-726 declares the opposite
  in terms: "it also compares owner segments only, so a repository-name-only drift under an unchanged
  owner is not detected." `_publish_locations_in` (`:3620`) returns owner segments. A carrier whose
  repo half drifts has stopped agreeing and the build still passes. (Both readers.)

  **5. The benchmark's sessions are not prompted with `bench-deal-brief.md`.** `README.md`:171-172
  ("the separate deal brief the benchmark's sessions are prompted with") and `:9-10` ("used only to
  prompt the benchmark's sessions"). `evals/benchmark/run_benchmark.py`:295 sends
  `scenario['prompt']` and nothing else; the brief is read exactly once, inside `--self-test` at
  `:1646`, to assert entity disjointness. "Thornfield", the brief's buyer, appears 0 times in
  `scenarios.json` and 0 times across the 96 committed raw records. The brief's own `:9` states the
  accurate relation — "it grounds Phase 5's benchmark scenarios". The separation half of README's
  claim does hold. (Both readers.)

  **6. `README.md`:264-265 claims codes check the inventory counts; none reads them. Same defect
  class as G-06-6 #1, reintroduced in the paragraph rewritten to fix it.** The sentence: "Different
  codes check those — `catalog-count-mismatch`, `readme-layout-tree-stale` and their neighbours read
  the counted artefact and compare." `catalog-count-mismatch` (`check_repo.py`:198-202) compares a
  `skills/*/SKILL.md` stated count against `NUMBERING.md`; it never opens README. Settled by mutation
  probe against an unmutated sibling control, both from `git archive HEAD`:

      control (unmutated):  check_repo: 0 violations   rc=0
      mutant (README 31-rule->37-rule, 31 rules->37 rules, 28 worked->44 worked, 4 replacements):
                            check_repo: 0 violations   rc=0

  The checker is green over the defect the sentence claims it catches. (Reader 5; probe by this
  session.)

  **7. The activation contrast at `README.md`:111-112.** "The installed skill has to be triggered and
  was not in 3 of its 12 sessions, while the output style and the pasted prompt are unconditionally
  on once selected." The 3-of-12 figure comes from `evals/routes/RESULTS-routes.md`:15's Activation
  column, whose metric is `run_routes.py`:487, `MARKER_RE.search(text)` over output text. On that
  same metric `prompt-on` scores 8 of 12 (`:17`) — worse than skill-on's 9 of 12 — immediately after
  README names it unconditionally on. Round 1 recorded this as a placement judgement rather than a
  falsehood; test 9's own text named "a cold reader deciding otherwise" as the finding, and reader 4
  decided otherwise. Recorded as confirmed on that instruction. (Reader 4.)

  **8. `evals/benchmark/bench-deal-brief.md`:10-12 still asserts an expired premise.** "This
  environment has no live network access, so the name-collision web search ... could not be repeated
  here for this brief's names; that is an open, disclosed unrun-verify item, not a completed check."
  `LEGAL-REVIEW.md`:617, ledger row 18, books that same search **Fixed**: "Closed by 06-02's
  searches; the premise that this environment has no network had expired." Two committed files, one
  open and one closed on the same item. (Found by this session; neither reader was pointed at that
  file.)

  **Recurring under-specification, recorded not actioned.** `README.md`:188 "Each scenario was
  drafted twice" against `evals/benchmark/RESULTS.md`:214 "each cell above is measured at 3 repeats".
  Round 1 adjudicated this as under-specification rather than a falsehood after it misled a reader;
  round 2 readers split on it again, one calling it compressed phrasing and one a contradiction. Two
  rounds of readers have now tripped on the same unstated factor. Not recorded as a gap, on round 1's
  adjudication, but the repeat is the evidence that stating the 3 repeats would be cheaper than
  defending the omission a third time.

  **What both readers verified as consistent, recorded so it is not re-checked.** 31 rules across
  SKILL.md / NUMBERING.md / checklist.md; 28 worked pairs; 8 MC dimensions with initials
  M-E-D-D-P-P-C-C; the before/after pair reproduced character-for-character from
  `examples/before-after.md`; every claim-region benchmark figure against `RESULTS.md` including the
  16-cell 8/1/7 split and the both-models direction, recomputed by hand by both readers; the
  conformance figures, CR-01 and the 03-15 disposition section; Arm B's 45/45 and 9/25; the routes
  run's 36 sessions and overlapping ranges; every one of the layout tree's paths existing on disk;
  stdlib-only imports across all eight Python files; and the ten CI commands in `ci.yml`.

### 10. The reproduction-boundary material holds up to readers who did not write it
expected: |
  Round 3, against `LEGAL-REVIEW.md`'s MEDDICC/MEDDPICC and PF-1 material and the ledger rows and
  `## What remains open` items that depend on it. Gap G-06-7 was six checkably-false statements found
  by two readers; 06-06 corrected all six. This test asks the same question of the corrected file, by
  readers who did not make the corrections: is any sentence in that material falsifiable from another
  committed file, and do the stated conclusions follow from the reasons given?
result: issue
reported: "Two independent readers, converging on five of seven. The six corrections from round 2 all hold and were verified as accurate. Seven different checkably-false statements survive in the same material — five of them in text 06-05 wrote that round 2 did not reach, one in the sentence 06-06's own self-audit commit wrote, and one spread across three places that disagree with each other. The worst is that the file's prong-4 classification of the eight MC names is the opposite of the classification this repository's own checker enforces."
severity: major
evidence: |
  **1. The prong-4 six/two split is the opposite of what `check_repo.py` enforces. (Both readers.)**
  `LEGAL-REVIEW.md`:249-252 — "Applied honestly, the eight split. "Metric", "Pain", "Champion",
  "Competition", "Decision Criteria" and "Decision Process" are ordinary business English that stands
  on its own outside this framework family. "Economic Buyer" and "Paper Process" are not". And
  `:308` — "They are not neutral English the way "Metric" or "Competition" are."

  `tools/check_repo.py`:2952-2965 freezes the same eight strings one-and-seven the other way:

      SOURCE_COINED_LABELS = (
          # ... The ordinary-English
          # word for a measurement ('metric') is deliberately excluded ...
          'economic buyer', 'paper process', 'decision criteria',
          'decision process', 'champion', 'competition', 'pain',
      )

  `metric` is the only one of the eight this repository treats as ordinary English. Five strings the
  review calls ordinary business English — pain, champion, competition, decision criteria, decision
  process — are strings `check_source_label_in_skill_content` (`:2977-3009`) makes a build failure in
  shipped skill content, on the stated ground that they are source-coined. `:308` names "Competition"
  as the example of neutral English; `:2963` names it in the coined tuple. The split is the load-
  bearing step of the prong-4 disposition, and the repository's own enforcement code contradicts it.

  **2. The occurrence enumeration is false against two committed files, and miscalls a production
  constant a fixture. (Both readers.)** `:253-256` — "they are index terms in `NUMBERING.md`'s
  registry and nowhere else that ships ... across the shipped tree the two appear only in
  `NUMBERING.md`, in this file, and in `check_repo.py`'s fixtures."

      examples/deal-brief.md:75          ### Economic buyer stated priorities
      examples/deal-brief.md:89          ### Paper process
      examples/deal-brief.md:26          ... Chief Financial Officer, the economic buyer.
      evals/benchmark/bench-deal-brief.md:130   ### Economic buyer stated priorities
      evals/benchmark/bench-deal-brief.md:145   ### Paper process
      evals/benchmark/bench-deal-brief.md:54,185  ... the economic buyer ...

  The case defence is unavailable: this repository's own matcher for these exact labels is
  `re.compile(r'\b' + escaped + r'\b', re.IGNORECASE)` (`check_repo.py`:2974). Both files ship —
  `README.md`:141 calls `examples/deal-brief.md` "the one canonical fictional deal every worked
  example cites", and the same `LEGAL-REVIEW.md` entry leans on it at `:230-231`. Separately,
  `check_repo.py`:2958-2959 is `SOURCE_COINED_LABELS`, the module-level constant the production check
  reads — not a fixture; and "Paper Process" occurs in no fixture in that file at all, only at
  `:2959`. The sentence at `:259-260` calls this "a narrower fact ... better for this entry than the
  one it replaces". The narrower fact is itself wrong, and it was written by commit a18f492 — 06-06's
  own self-audit, titled "correct two statements this round's own self-audit falsified".

  **3. Prong 2 reinstates the mnemonic the correction fifteen lines above retired. (Both readers.)**
  `:224-225` — "the prong has to be answered on that footing rather than on a mnemonic that the
  shipped block names do not spell." `:239` — "and organised around a mnemonic: at that thinness, the
  expression and the idea it organises are hard to separate". `:301` reinstates it a second time as
  the contrast that makes PF-1 stronger than id 6 — "The MC blocks could at least be argued to follow
  a mnemonic that many publishers teach". The correction exists to remove that ground; two later
  passages spend it anyway.

  **4. `NUMBERING.md` does not declare what `:298-299` says it declares. (Both readers.)**
  "It is a source's ordered list, in that source's order, and `NUMBERING.md` says so in its own words.
  Id 6 at least had to be argued into that description; this one declares it." `NUMBERING.md`:33-35
  says "carved into seven named sub-blocks, one per Command of the Message element" — a one-to-one
  correspondence of labels. Nothing in `:31-54` addresses whose order the table is in; the remaining
  prose is slot arithmetic. The contrast is available in the repository:
  `completeness-audit.md`:12-15 does address order provenance for the MC side and declines to concede
  it. No equivalent sentence exists for PF-1 in either direction. This is the entry's first and
  strongest ground for ranking PF-1 above id 6.

  **5. The rename cost is stated three times and counted two ways, and neither matches the tree.
  (Both readers, and found independently by this session before either returned.)** `:340-342` —
  "it costs three files rather than one — `NUMBERING.md`, `skills/proof-first/SKILL.md`, and a
  `python3 tools/generate_derivatives.py` run" — enumerates two files and one command and calls it
  three files. `:433` and `:731` both say "three files and a regeneration", making the regeneration an
  addition to three rather than one of them. The tree gives four: `git grep -l "Positive Business
  Outcomes"` returns `NUMBERING.md`, `skills/proof-first/SKILL.md`, `output-styles/proof-first.md`,
  `prompts/system-prompt.md` — two hand edits and two regenerated files, all four of which must be
  committed because `generate_derivatives.py --check` compares against the committed files.

  **6. "nowhere else that ships" uses a sense of "ships" `README.md` denies. (Reader 3.)** `:253`
  presupposes `NUMBERING.md` ships. `README.md`:367-369 — "`NOTICES.md`, `SOURCES.md`,
  `NUMBERING.md`, `examples/`, `tools/`, and `evals/` stay at the repository root and never ship to
  an installed user." Four lines later the same passage uses "the shipped tree" to include
  `NUMBERING.md`, `LEGAL-REVIEW.md` and `check_repo.py`, none of which ship on README's definition.
  Two incompatible senses in one passage, and the repository contradicts the first.

  **7. Prong 2's stated basis contradicts prong 4's stated finding, thirteen lines apart. (Reader 4.)**
  `:237` — "Eight blocks, each labelled with the shortest ordinary English for the thing it covers".
  `:250-252` — ""Economic Buyer" and "Paper Process" are not — both are terms of art this family put
  into circulation, and both are adopted here verbatim as block labels." Both cannot describe the
  same eight labels.

  **What the round-2 corrections got right, verified and recorded so the improvement is not lost.**
  Both readers checked all six and found all six correct. The PF-1 counterweight now names
  `SKILL.md`:63, `output-styles/proof-first.md`:87 and `prompts/system-prompt.md`:75, and all three
  carry the byte-identical seven-element sentence (reader 3 verified the bytes). The swappable-
  position count is six and recomputes from `NUMBERING.md`:73-80's three same-initial pairs. The
  `completeness-audit.md` claim is true and is mechanically enforced. The `NUMBERING.md`:31-45
  citation resolves. `:296`'s equivalence claim is gone and items 5 and 6 are described as separate.
  The append-only rule at `:16-24` now states the correction exception with its conditions. Reader 3
  additionally recomputed every ledger count (32 entries; 9 fixed, 2 closed on reasoning, 9 waived,
  12 open) row by row and found them right, and confirmed the six `SOURCES.md` rows all read verified.

  **Reasoning critiques, recorded as observations rather than gaps** (not checkably false; prose-gap
  stopping rule): prong 2's "many independent publishers" clause is a premise recorded in no committed
  file — `SOURCES.md`:41-44 lists two sources for this family — and it is the clause that converts a
  conceded reproduction into a thin one (both readers, independently, and it survives from round 2's
  own backlog); `:56` says the section "ends on two live questions" while items 5 and 6 carry three
  between them (reader 3); `:39`'s bolded "Content items still needing a decision: 2" excludes id 29,
  which `:344-345` classifies as a change to shipped content awaiting a version decision, though the
  prose at `:54-57` discloses it separately and the two name-collision items are the ones routed
  "before wider distribution" (reader 3); prong 4 still records position instead of disposing, which
  the ledger concedes at `:733` (both readers); and `:254-255`'s "its headings are MC ids plus rule
  titles" is true of the eight `###` headings but not of the file's `#` and `##` headings (reader 4).

### 11. A cold read of the corrected README finds no checkably-false statement
expected: |
  Round 3, against `README.md`. Gap G-06-9 was eight false statements found by two readers and this
  session; 06-06 corrected all eight and added a checker code for the one that shipped. This test
  asks the same question of the corrected file, by readers who did not make the corrections.
result: issue
reported: "Three independent readers converged on one statement — and it is a claim 06-06 newly imported into README while correcting a different false claim about the same file. Every one of round 2's eight corrections holds. One further reader finding was adjudicated against 2-to-1 and is recorded as an observation."
severity: major
evidence: |
  **1. README says the two deal briefs share no figure. They share one, byte for byte. (Readers 1, 2
  and 5, independently.)** `README.md`:9-11 — "`evals/benchmark/bench-deal-brief.md` is a second,
  separate brief, which grounds the benchmark's scenarios and shares no company, person, platform or
  figure with the one the examples are written against."

  The two briefs' `Canonical figures` tables — each declared by its own file to be the registry of
  every figure it owns — carry an identical row:

      examples/deal-brief.md:116               | rfp-security-weight | 20% | percent | Weight the
      evals/benchmark/bench-deal-brief.md:177    buyer's top-level scoring rubric assigns to the
                                                 security section of the response |

  Same key, same value, same type, same description. `comm -12` over the two files' table rows
  returns it and nothing else substantive. Both decision-criteria tables also read
  `| Security posture | 20% |` (`examples/deal-brief.md`:87, `bench-deal-brief.md`:143). Every other
  same-named key was deliberately varied — technical 55%/50%, commercial 25%/30%, legal-review-days
  10/8, security-review-days 15/12 — which is what makes the one that was not a slip rather than a
  policy. The company, person and platform thirds of the claim do hold; reader 1 checked all nine
  invented names and the platform lists.

  `evals/benchmark/bench-deal-brief.md`:8 has carried this claim about itself since 05-02
  (commit 1577910). What is new is that commit 3a37839 — 06-06's fix for round 2's finding 5, titled
  "correct what bench-deal-brief.md is for" — replaced README's old sentence, which made no such
  claim, with one that imports it. The round that closed G-06-9 opened this.

  **Adjudicated against, recorded so it is not re-raised as new.** Reader 1 called `README.md`:186-188
  false — "`run_benchmark.py --self-test` is the only place it is read at run time, to assert it
  shares no named entity with `examples/deal-brief.md`" — because `run_benchmark.py`:1645's
  `shared_deal_brief_entities` tuple holds four strings while `examples/deal-brief.md` invents nine.
  Readers 2 and 5 each examined the same sentence against the same code and listed it as accurate.
  The tuple's scope is a real and understated limit, and it is the same class as round 2's
  `publish-location-drift` finding, which was recorded as a gap and closed by bounding the sentence.
  Recorded here as an observation on the 2-to-1 split rather than a gap, with the bounding edit
  carried to backlog. The substantive property holds today: none of the other five names appears in
  the bench brief.

  **What all three readers verified as consistent, recorded so it is not re-checked.** Every one of
  round 2's eight corrections: the `/config` observation at `:90-98` against `LEGAL-REVIEW.md`:582-594
  including its two controls and three stated limits; `:44-46`'s publish-location ceiling against
  `check_repo.py`:703-727; `:146-154`'s "three runs, two of them against the shipped skill
  description" against the three head-14 hashes; `:184-188` on what the bench brief is for;
  `:279-284`'s inventory-enforcement paragraph, with both readers independently enumerating every
  function in `check_repo.py` that opens README and finding none that reads a stated count;
  `:121-123`'s three activation figures 9/11/8 of 12; and the "no benchmark has run" sentence gone
  from `artifact-patterns.md` and both derivatives. Beyond those: all 40 layout-tree paths exist;
  the reproduced before/after pair is character-for-character `examples/before-after.md`:12-15; the
  31-rule and 28-pair counts recompute from the files; every claim-region figure against
  `RESULTS.md`, with both readers re-summing the 48-row per-cell table to the pooled 45/1/2, 32/3/13
  and 7/3/38 totals and recomputing the 8/1/7 sixteen-cell split and the both-models direction by
  hand; the conformance 3/10 and 4/10 against `RESULTS-mod04.md`:760 and :776, with reader 2
  re-tallying all 23 committed run blocks; the 439-character description length, counted; and the ten
  CI commands in `ci.yml`.

### 12. No two committed files in the repository state things that cannot both be true
expected: |
  Round 3, new this round. Rounds 1 and 2 pointed every reader at a named file, so a contradiction
  between two files neither brief named could not be found. This reader was pointed at no file: find
  any two committed files that cannot both be true, with attention to whether a measurement has been
  performed, to counts, and to what a script's prose says against what its code does.
result: issue
reported: "Three checkably-false statements, none in a file any previous round's brief named. One is the expired no-network premise surviving in the file a companion explicitly routes the reader to — in the round whose own commit was titled 'sweep the expired no-network premise out of the tracked tree'."
severity: major
evidence: |
  **1. The expired no-network premise survives in `evals/lint.py`, and `proxy-sources.md` sends the
  reader to it.** `evals/lint.py`:98-100, in the module docstring's declared ceiling for
  `proxy-term-source-is-internal` — "it does not and cannot confirm a live http(s) URL actually
  serves the content the registry claims (see ceiling 2 above -- **this environment has no live
  network access**)." `evals/proxy-sources.md`:12-14 — "The reason given when this file was written
  was that the environment had no live network access. That premise has since expired —
  `LEGAL-REVIEW.md`'s ledger row 18 records where — and `SOURCES.md`'s own rows were re-confirmed
  against live pages on 2026-09-21". And `evals/proxy-sources.md`:37-38 — "See `evals/lint.py`'s
  module docstring for the full statement of this ceiling."

  The file that records the premise as expired points the reader at the file that still asserts it.
  Three further files agree the premise expired: `LEGAL-REVIEW.md`:720 (ledger row 18, **Fixed**),
  `bench-deal-brief.md`:16-17, and `check_repo.py`:3776-3779. Commit 467ed6e, 06-06 task 8, is titled
  "sweep the expired no-network premise out of the tracked tree"; `git grep` for the premise now
  returns `lint.py`:99 alongside the three files that disclaim it.

  **2. Ledger row 28 miscounts the route report's limits.** `LEGAL-REVIEW.md`:730 — "Measured null
  result published with its **four** named limits." `evals/routes/RESULTS-routes.md`:45-50 publishes
  six bullets, and `evals/routes/run_routes.py`:183-190 freezes `REQUIRED_CAVEATS` at exactly six
  keys with one bullet rendered per key, so the file structurally cannot publish four.

  **3. `run_conformance.py` says it cross-checks three committed fixtures; it enumerates five and
  five are committed.** `:22-23` — "Offline proof that the scorer discriminates **the three
  committed** transcript fixtures correctly" — and `:313-315` — "It then cross-checks the three
  committed transcript fixtures (conformant-family-first.txt, nonconformant-no-family.txt,
  nonconformant-rule-before-family.txt) if present", naming them exhaustively. `:459-465`'s
  `fixture_expectations` holds five, including the two `-late-phrase` fixtures the same docstring's
  own cases 8 and 9 describe, and `ls evals/conformance/transcripts/` returns all five.

  **What this reader checked and found consistent, recorded so it is not re-checked.** The PF and MC
  registries across `NUMBERING.md`, `SKILL.md`, `checklist.md` and `completeness-audit.md` — 31 PF
  IDs, 8 MC IDs, identical ID sets in all three, and the PF-1 seven-by-four arithmetic; the
  derivative triple, with `output-styles/proof-first.md`'s body line-for-line identical to
  `prompts/system-prompt.md` and both carrying the same stamp digest and source list; both stale-claim
  guards satisfied by the current text; the 96 generation records and 96 judge records on disk;
  `DECISION-RULE-cat10.md`'s Clopper-Pearson and Fisher tables recomputed by hand against `stats.py`,
  including `p_attr = 0.0016`; `INIT-EVENTS.md`'s 70+70 sessions against the committed tarball; and
  `RESULTS-mod04.md`'s 23 run blocks re-derived arm by arm.

### 13. The reproduction-boundary material holds up after the round-3 corrections
expected: |
  Round 4, against `LEGAL-REVIEW.md`'s MEDDICC/MEDDPICC and PF-1 material. Gap G-06-10 was seven
  checkably-false statements; 06-07 corrected all seven and adopted `check_repo.py`'s frozen
  seven-of-eight source-coined split in place of the file's own six-and-two. This test asks the same
  question of the corrected file, by two readers who made none of the corrections.
result: issue
reported: "Two independent readers. All seven round-3 corrections hold and the adopted split is verified accurate. Ten different checkably-false statements, nine of them authored by the correcting commit itself — including an enforcement claim naming a check that never opens two of the four files it is offered for, a sentence quoted from SKILL.md that is not in SKILL.md, and the same file cited as both a rename target and a sentence the rename leaves untouched."
severity: major
evidence: |
  **1. The "mechanically held" claim names a check that never opens two of the four files. (Readers 3,
  4 and 6 — all three who could reach it, plus this session independently before any returned.)**
  `LEGAL-REVIEW.md`:288-291 — "Not `skills/proof-first/SKILL.md`, not any `references/*.md`, not
  `output-styles/proof-first.md`, not `prompts/system-prompt.md`. This is not an observation, it is
  mechanically held: `source-label-in-skill-content` fails the build on any of the seven in that
  content, and it is green."

  `tools/check_repo.py`:983 is `SKILL_GLOB = 'skills/*/SKILL.md'`, and the check's candidate set
  (`:2991-2996`) is that file plus the `references/*.md` beside it. It never opens either derivative,
  and its own docstring says so at `:302-305`. The underlying fact is true — zero hits for all seven
  across `skills/`, `output-styles/` and `prompts/` — but for two of the four named files it is
  exactly what the sentence denies it is: an observation. `:322-323` then rests the disposition on it
  ("the first is now mechanically enforced rather than observed"). The derivatives *are* covered, but
  transitively and by a different mechanism — `generate_derivatives.py --check` byte-compares them to
  sources that are scanned — and that is a two-step argument the sentence does not make. Reader 4
  added a live ceiling neither the checker nor the entry records: `check_repo.py`:2999 scans
  `strip_fences(...)`, so a label inside a fenced block in `SKILL.md` would reach both derivatives
  unseen. Presently moot — no file under `skills/proof-first/` contains a fence.

  **2. A sentence quoted from `SKILL.md`:63 is not in `SKILL.md`. (Readers 3, 4 and 6.)**
  `:435-438` — "`NUMBERING.md`:33-35 and `skills/proof-first/SKILL.md`:63 both state the seven
  sub-blocks are "one per Command of the Message element"". `SKILL.md`:63 says "carved into seven
  sub-blocks, each reserved four IDs: Before scenario, …". The quoted phrase occurs only at
  `NUMBERING.md`:33-34, and nowhere in `skills/`, `output-styles/` or `prompts/`.

  **3. The same line is cited as both the rename's target and what the rename leaves in place.
  (Reader 4.)** `:426` names `skills/proof-first/SKILL.md`:63 as one of the two files a rename edits
  by hand; `:436-439` names the same line as one of the "two sentences" left "in place". Both cannot
  hold. The substance fails too, and in the direction that matters: in `SKILL.md`:63 the source-naming
  clause and the seven labels are one sentence, so a rename necessarily rewrites it. The
  "independently of what the labels are called" property holds for `NUMBERING.md`:33-35, where the
  correspondence sentence and the table are separate, and fails for the one shipped file. It
  propagates into `## What remains open` item 5.

  **4. The stated provenance of "four files" returns five. (Readers 3, 4 and 6.)** `:429-431` — "The
  count is `git grep -l "Positive Business Outcomes"` over the tracked tree outside `.planning/`, not
  an estimate." That command now returns `LEGAL-REVIEW.md`, `NUMBERING.md`,
  `skills/proof-first/SKILL.md`, `output-styles/proof-first.md`, `prompts/system-prompt.md` — five,
  because `LEGAL-REVIEW.md`:387 and `:430` carry the string, the second of them inside the quoted
  command. The four-file cost is right; the sentence asserting the number *is* that command's output
  is not. The passage was corrected once already for this class three lines later.

  **5. The by-hand citation under-cites its own file. (Reader 4.)** `:426` cites `NUMBERING.md`:39-45.
  `NUMBERING.md`:48 also carries a label — "six elements would get three slots and Positive Business
  Outcomes (the" — so a rename must edit line 48 too.

  **6. "All three parts were wrong" is wrong about two of the three. (Reader 3.)** `:297-300` says the
  earlier draft's "only in `NUMBERING.md`, in this file, and in `check_repo.py`'s fixtures" had "all
  three parts wrong". "In this file" was correct. "In `check_repo.py`'s fixtures" was correct for
  Economic Buyer — `check_repo.py`:7000-7004 inserts that exact label into a fixture as the firing
  case, and it recurs at `:7029`, `:7036`, `:7051`, `:7059`. What failed was the word **only**. The
  two supporting sub-claims the correction offers are both true and both verified; they just do not
  establish what the sentence says they establish.

  **7. The correction-count in the append-only rule is stale. (Reader 4.)** `:23-26` — "Three
  corrections in this file were made on that basis", listing three from 2026-09-21. Eight lines in the
  file now carry 2026-09-22 corrections from 06-07, six of them in the reproduction-boundary material,
  and the ledger names the round at `:811` and `:836`. By the paragraph's own definition these are
  corrections "on that basis", and neither the count nor the date list covers them.

  **8. "not ordinary English at all" is not what the checker's split says. (Reader 4.)** `:245-247`
  justifies removing prong 2's premise on the ground that "the prong-4 finding below is that seven of
  the eight are not ordinary English at all". The prong-4 finding (`:280-282`) says the seven are
  *source-coined*, which is a different claim, and `check_repo.py`:2955-2957 excludes `metric` for a
  narrower reason — MC-1 and the integrity rules use that word legitimately — saying nothing about the
  other seven being non-English. The same entry supplies the counter-evidence five lines later, at
  `:291-298`, by recording five of the seven in ordinary use as English headings and role designations.

  **9. The checker is misquoted inside quotation marks. (Reader 4.)** `:48` — "only whether the **list**
  it declares a pass over is complete". `check_repo.py`:2131-2133 says "only whether the **file** it
  declares a pass over is complete". Small, and it is the sentence licensing the gate token above the
  reproduction-boundary summary.

  **10. "Two of the four grounds" is three. (Reader 6.)** `:362-363` introduces the PF-1 comparison
  with "Two of the four grounds recorded when this section was written did not survive a reader
  checking them". Three of the four bullets carry a dated `*Corrected 2026-09-22:*`, and the fourth's
  correction says its ground "no longer distinguishes the two entries" — which in a list headed "Why
  it is stronger than id 6" is the same non-survival.

  **What the round-3 corrections got right, verified and recorded.** Both readers checked all seven and
  found all seven correct. Reader 6 additionally verified the adopted split line by line: the
  `SOURCE_COINED_LABELS` tuple bounds, all seven strings, the `check_source_label_in_skill_content`
  violation text, the `metric` exclusion comment, the 03-07 GAP B provenance, the `:302-305` routing to
  LEG-04, the five labels in both deal briefs, the case-insensitive matcher, the `README.md`:369-371
  citation, and that `Decision Process` and `Competition` appear nowhere else. The three-live-questions
  count and the `NUMBERING.md`:31-54 order finding were both confirmed.

  **Reasoning critiques, recorded as observations** (prose-gap stopping rule): id 6 is booked `Closed
  on reasoning` while the entry says prong 2 rests on a test `SOURCES.md` does not contain and prong 4
  is "recorded rather than disposed" — and 06-07's own narrowing made prong 2 weaker, so the closure is
  further from its own definition (`:793-796`) than before (readers 3 and 4, independently); the PF-1
  section's prong-4 engagement and its "the framework's own vocabulary" and "ordered the way the
  framework itself sequences them" claims rest on a read of Force Management material recorded nowhere
  — the same defect 06-07 removed from id 6 fifteen lines earlier, left standing in the parallel entry
  (both readers); "the mark is live and unadjudicated" outruns a register the file says it could not
  reach (reader 3); `completeness-audit.md`:12-15 is over-read as "declining to concede" order
  provenance when it routes provenance to the registry (reader 4); and prong 3's "anywhere in this
  repository" is an unqualified whole-repo negative with no recorded sweep (reader 4).

### 14. A cold read of README after the round-3 corrections
expected: |
  Round 4, against `README.md`. Gap G-06-11 was one false statement; 06-07 bounded it in both files.
  This test asks the same question by two readers who made no correction.
result: issue
reported: "Both round-3 corrections hold. One statement, found by one of the two readers and standing since Phase 1: README says the checker enforces 'all of the above' over a 17-item inventory it does not read eleven of. The second reader examined the same sentence and rejected it, but on a different comparison than the one that falsifies it."
severity: major
evidence: |
  **README.md:175 — "`tools/check_repo.py` — a stdlib-only checker enforcing all of the above, wired
  into CI." (Reader 1.)** "All of the above" is the 17-item inventory at `:136-174`.
  `grep` over the whole 8,554-line checker returns zero hits for `pressure-tests`, `proxy-sources`,
  `scenarios.json`, `lint.py`, `run_routes`, `run_trigger` and `RESULTS-trigger`. Its scan roots
  exclude the directory outright (`check_repo.py`:66-68: "Scan roots are examples/ and skills/;
  evals/ is deliberately excluded"). README itself says the opposite for one of those items at
  `:289`: "`check_repo.py` will not do it for you." Written in commit `58530a6` (Phase 1) and
  survived four rounds of cold reads — this is the first reader to open the checker and count.

  **The 2-to-1 note, recorded so it is not re-litigated.** Reader 2 examined `README.md`:175, checked
  it twice and rejected it — but against a different comparison: the checker's *docstring opening
  sentence* versus its own code list, concluding "the stale sentence is in check_repo.py, not in
  README". That does not reach reader 1's comparison, which is README's "all of the above" against
  what the checker actually reads. Recorded as confirmed on the evidence, with reader 2's reasoning
  noted because it is a real and separate observation: `check_repo.py`:4-5's opening sentence is also
  narrower than the checker it introduces.

  **What both readers verified.** Both round-3 corrections: `:9-12`'s bounded separation claim,
  including the nine-name self-test assertion read against `run_benchmark.py`:1649-1659 and the
  identical `rfp-security-weight` row named as shared; and every earlier round's correction still
  standing. Reader 2 recomputed the route means and ranges from the 36 raw records (7.9, 7.1, 6.3 and
  every pair overlapping) and recounted activation from `"activated": true` (9, 11, 8). Reader 1
  resolved all 31 listed paths. Reader 2 also examined and declined `README.md`:294's regeneration
  instruction as over-broad rather than false, since running the generator after editing
  `worked-examples.md` is a no-op.

### 15. No two committed files state things that cannot both be true
expected: |
  Round 4, the whole-tree sweep bound to no named file. Round 3's sweep found three; 06-07 closed all
  three. This asks the same question again of the whole tree.
result: issue
reported: "Four more contradictions, none of them in a file the other three briefs name, and none created by 06-07. One ships to every installed user: the derivatives tell the reader that every rule the omitted reference file illustrates carries a constructive line in SKILL.md, and eight of them cannot, because this repository's own build gate forbids it."
severity: major
evidence: |
  **1. The derivatives' omission notice is false, and it ships.**
  `output-styles/proof-first.md`:27-30 and `prompts/system-prompt.md`:15-18, written by
  `generate_derivatives.py`:183-186 — "One source is deliberately left out:
  `skills/proof-first/references/worked-examples.md` … every rule it illustrates already carries its
  own constructive line in `skills/proof-first/SKILL.md` — so nothing normative is lost."

  `worked-examples.md` illustrates **eight MC rules** (`## MC-` headings: MC-1, 6, 11, 16, 21, 26, 31,
  36). `SKILL.md` contains **zero** `### MC-` headings, and cannot contain them: `mc-rule-in-skill`
  (`check_repo.py`:144-152) makes an MC rule defined in `SKILL.md` a build failure, and
  `NUMBERING.md`:122-129 records every MC row as "Defined in | completeness-audit.md". The sentence
  cannot be true while the gate holds, and the gate is green. This is the only round-4 finding that
  reaches an installed user.

  **2. `check_repo.py`:4235-4237 — "until then this repository makes no such claim."** The claim
  disclaimed (`:4232-4234`) is "whether a session driven by a derivative reaches the same conclusions
  as one with the skill folder installed". `README.md`:113-115 and `evals/routes/RESULTS-routes.md`:1-3
  publish exactly that measurement, 36 sessions on 2026-09-21. The same file's
  `derivative-comparison-claim-stale` (`:4279-4284`) is built on the opposite premise.

  **3. `generate_derivatives.py`:8-11 — "Phase 5's benchmark is the only place such a statement could
  ever be sourced from."** The same script's `_render_preamble()` (`:189-193`) writes, into both
  derivatives, "A benchmark has compared a session driven by this file against a session with the
  skill folder installed: `evals/routes/RESULTS-routes.md` records what was measured". That is a
  different source, named by the file that says no other could exist; its own `:168-175` docstring
  says the old denial "stopped being true when 04-15 committed `evals/routes/RESULTS-routes.md`."

  **4. `run_benchmark.py`:476-479 — "The five caveats EVAL-10 requires", twice, plus "the same five
  keys", and again at `:2373`.** `REQUIRED_CAVEATS` holds six, `RESULTS.md` renders six bullets, and
  `README.md`:229 says six. The comment sits directly above the constant it miscounts.

  **What the sweep verified as consistent.** All three of round 3's sweep fixes: `evals/lint.py`'s
  restated ceiling, ledger row 28's six limits, and `run_conformance.py`'s five fixtures.

### 16. The sentences the last gap-closure round added survive checking
expected: |
  Round 4, new brief. Four of round 3's eleven findings and two of round 2's fourteen were authored by
  the round that was closing the previous one, and no brief had ever been aimed at that surface. This
  reader was given the 202 lines commit `908b90b` added, grouped by file, and asked to verify every
  citation, count, scope claim and absolute in them against the tree.
result: issue
reported: "The brief paid for itself on first use — highest-yield reader of the round. It converged with the two LEGAL-REVIEW readers on four findings and added two neither could reach, both in the deal brief: a count that is wrong under either way of counting, and a second separation claim presented as mechanically held when no code checks it."
severity: major
evidence: |
  **1. The 20% count is wrong under either counting rule.** `evals/benchmark/bench-deal-brief.md`:18-20
  — "20% carries four different meanings inside this brief alone and three inside the other". Counting
  raw occurrences in the figure and rubric tables gives **four in each** (bench `:128`, `:155`, `:187`,
  `:189`; examples `:63`, `:66`, `:87`, `:116`). Counting distinct meanings gives **two** in the bench
  brief (Q3's weight, restated at `:128` and `:187`; the security weight, at `:155` and `:189`) and
  **three** in the examples brief (Q2's weight, Q5's weight, the security weight). Neither rule
  produces "four … and three", so the two halves are counted on different rules and one is wrong under
  either. The sentence was written to justify not varying the figure, so the reasoning it carries is
  load-bearing.

  **2. The platform half of the separation is presented as mechanically held; nothing checks it.**
  `bench-deal-brief.md`:10-12 — "That separation is the one that matters and the one that is
  mechanically held: `run_benchmark.py --self-test` asserts every invented party and person in
  `examples/deal-brief.md` is absent from this file, and the platform lists are disjoint", restated at
  `:20-22` as "no shared company, person or platform … is the one held mechanically".
  `run_benchmark.py`:1649-1659's tuple holds nine person and party names and no platform name, and a
  grep for `platform`, `VMware`, `Hyper-V` and `vSphere` over `run_benchmark.py` and `check_repo.py`
  returns nothing. The platform lists *are* disjoint — reader 2 confirmed it independently — but that
  is an authored observation, and the sentence puts it inside the mechanical claim. Same defect class
  as finding 1 of test 13, in the same commit.

  **Converged with the LEGAL-REVIEW readers** on the `SKILL.md`:63 misquote, the `source-label-in-
  skill-content` scope, the `git grep -l` provenance, and the "two of the four grounds" miscount.

  **What this reader verified as accurate** — the long list is in test 13's closing paragraph; it
  covers every citation, bound, string and count in the adopted-split passage, plus the
  three-live-questions correction and ledger row 29's state.

## Summary

total: 16
passed: 4
issues: 12
pending: 0
skipped: 0
blocked: 0

Round 1: tests 1-6 — 3 passed, 3 issues (G-06-2, G-06-3, G-06-6), all three resolved by 06-05.
Round 2: tests 7-9 — 1 passed, 2 issues (G-06-7, G-06-9), both resolved by 06-06.
Round 3: tests 10-12 — 0 passed, 3 issues (G-06-10, G-06-11, G-06-12), all closed by 06-07.
Round 4: tests 13-16 — 0 passed, 4 issues (G-06-13, G-06-14, G-06-15, G-06-16), open.

**Round 4 reverses the trend and says why.** Seventeen checkably-false statements, against eleven in
round 3, fourteen in round 2 and three in round 1 — and **ten of the seventeen were authored by commit
`908b90b`, the round-3 gap closure itself.** Every one of round 3's corrections was verified to hold by
readers who did not make them; the round that made them introduced more than it closed. The new fourth
brief, aimed at exactly that surface, was the highest-yield reader of the round on its first run.

Round 3's numbers, kept for comparison:

Eleven checkably-false statements that round, against fourteen the round before and three before that.
The corrections themselves are holding: all six round-2 LEGAL-REVIEW corrections and all eight
round-2 README corrections were re-checked by readers who did not make them, and every one stands.
What has not converged is the reading — every one of round 3's eleven findings is in text no earlier
brief pointed a reader at. By `git blame` on the cited lines: four in 06-05 text round 2 did not
reach, three in files no brief had ever named (reached only by the new sweep brief), and four
authored by the closing round itself while fixing something else. Zero are regressions of a fix.
WINDOWS.md id 12's closure condition is a round that returns none; this is not it.

## Gaps

- gap_id: G-06-2
  truth: "LEGAL-REVIEW.md's WINDOWS id-6 disposition rests on sound reasoning"
  status: resolved
  resolved_by: 06-05-PLAN.md
  resolved_at: 2026-09-21
  reason: "Reader verified against NUMBERING.md: the eight shipped dimension names spell MEDDPPCC, not the acronym, so 'it IS the acronym, letter by letter' is false; and Decision Criteria/Decision Process and Champion/Competition are freely swappable without changing the letter string, so 'reordering would produce a different word' is false. The disposition also tests one of SOURCES.md's four reproduction prongs, never reaching the coined-term-as-label prong its own step 3 recites."
  severity: major
  test: 2
  artifacts:
    - path: "LEGAL-REVIEW.md"
      issue: "id-6 disposition (:161-198): false load-bearing premise; fourth reproduction prong untested"
    - path: "NUMBERING.md"
      issue: ":9 names the namespace MEDDICC over an eight-element table whose extra element is Paper Process"
  missing:
    - "Restate the id-6 reasoning on grounds that survive NUMBERING.md — short unprotectable labels, thin protection where expression merges with a mnemonic — or reopen the entry"
    - "Test the fourth reproduction prong (coined term adopted as this repository's own label) explicitly, as id 3 does for its prongs"
    - "Examine NUMBERING.md's PF-1 seven Command of the Message sub-blocks: an ordered list reproduced in its order, live ® mark, no acronym defence, examined by neither id 3 nor id 6"

- gap_id: G-06-3
  truth: "LEGAL-REVIEW.md cannot be read as a professional legal opinion"
  status: resolved
  resolved_by: 06-05-PLAN.md
  resolved_at: 2026-09-21
  reason: "Independent reader's verdict: parts of it can. The disclaimer does not reach the verdict layer — Gate status: PASSED sits above it at line 5, and the ledger's Fixed entries sit 400 lines below it stripped of every hedge. Specific sentences state conclusions about the author's own exposure rather than recording what was looked at."
  severity: major
  test: 3
  artifacts:
    - path: "LEGAL-REVIEW.md"
      issue: ":5 Gate status: PASSED above the disclaimer; :138 'boundary not crossed'; :155 'by none exclusively'; :187 'trading on'; :240 'the disclaimer that makes...'; :428/:431 ledger Fixed against the :420 definition"
  missing:
    - "Move or rename Gate status so it does not read as clearance above the disclaimer, and reconcile it with the two name collisions :244-250 leaves open before wider distribution"
    - "Reword the two Disposition: headings to describe what was done rather than what was concluded"
    - "Cut or bound :155 'by none exclusively' and :187's 'could be seen to be trading on'"
    - "Replace :240-241's 'which is the disclaimer that makes...' with what the files state rather than what that accomplishes"
    - "Give the ledger a state for judgement-based closures; ids 3 and 6 are not Fixed under :420's own definition, and the 11/9/8 counts inherit it"

- gap_id: G-06-6
  truth: "No two passages of README contradict each other"
  status: resolved
  resolved_by: 06-05-PLAN.md
  resolved_at: 2026-09-21
  reason: "Two independent cold readers converged on three checkably-false statements, each contradicted by a committed file in this repository: a universal evidence-discipline claim the project's own checker docstring denies, a four-vs-three route count the runner's own docstring denies, and a superseded trigger figure the results file supersedes."
  severity: major
  test: 6
  artifacts:
    - path: "README.md"
      issue: ":231-233 'Every number this README carries is sourced from a committed results file under evals/, states the model versions and the date' — contradicted by tools/check_repo.py:405-415"
    - path: "README.md"
      issue: ":139-140 'the four install routes' — contradicted by run_routes.py:2, ROUTES tuple, RESULTS-routes.md:3 and README's own :104"
    - path: "README.md"
      issue: ":131-133 cites the superseded n=1 trigger figures; RESULTS-trigger.md:166 records the shipped description at OF_B/SN_B = 9/25, n=5"
  missing:
    - "Bound README:231's claim to the claim region, matching what the two checker codes actually enforce and what the checker docstring already says"
    - "Correct README:139-140 to three measured routes, or state that routes 1 and 2 collapse into the skill-on arm"
    - "Carry the Arm B n=5 figure for the shipped description, or say plainly that the n=1 run is superseded"
    - "Minor, same pass: :202 'one measured v1 limitation'; :7-8 'the one ... deal brief'; MOD-04's two thresholds at :135-136 vs :202-203; the five tree paths absent from 'What exists today'"

- gap_id: G-06-7
  truth: "LEGAL-REVIEW.md's id-6 restatement and its new PF-1 section contain no sentence a committed file falsifies"
  status: resolved
  previous_status: failed
  resolved_by: "06-06 tasks 9, 10, 11 (commits d56022c, b931161, 485de7b) — all six corrected, each checked against the file the reader cited. The PF-1 counterweight was corrected in all four places it had propagated to, and the id-29 disposition was re-read against the corrected facts rather than having them patched underneath it. Self-checked, not independently read: the closure condition remains a round-3 cold read."
  reason: "Two independent readers. Six checkably-false statements survive the restatement. The worst is the PF-1 counterweight at :289-291 and :299-301, which asserts the seven-element list appears in no shipped file — SKILL.md:63, output-styles/proof-first.md:87 and prompts/system-prompt.md:75 each carry it as a set in the table's order — and the error propagates into What remains open item 5 and ledger row 29, understating both the exposure and the remedy. The correction paragraph itself miscounts the freely-swappable positions as four when NUMBERING.md gives six."
  severity: major
  test: 7
  artifacts:
    - path: "LEGAL-REVIEW.md"
      issue: ":289-291 and :299-301 — 'nothing a reader of the shipped skill sees names these seven elements as a set in this order' and 'no shipped file cites them', both false against SKILL.md:63, output-styles/proof-first.md:87, prompts/system-prompt.md:75"
    - path: "LEGAL-REVIEW.md"
      issue: ":204-207 'four of the eight positions' — NUMBERING.md:77-78 makes Paper Process/Pain a third same-initial pair, so six; the same paragraph spells M-E-D-D-P-P-C-C at :203"
    - path: "LEGAL-REVIEW.md"
      issue: ":236-237 'block headings in completeness-audit.md' — neither string occurs in that file"
    - path: "LEGAL-REVIEW.md"
      issue: ":268 cites NUMBERING.md:26-40; the PF-1 content is at :31-45 and the cited span excludes five of the seven elements"
    - path: "LEGAL-REVIEW.md"
      issue: ":296 'the same two live questions id 6 ends on' — :383-390 lists them as separate items 5 and 6 with different content"
    - path: "LEGAL-REVIEW.md"
      issue: ":16 declares the file append-only; commit 0b8a865 rewrote the id-6 section in place (-32/+64)"
  missing:
    - "Correct :289-291 and :299-301 to state that the seven elements ship in SKILL.md and both derivatives, and propagate to :383-384 and ledger row 29 — the counterweight that justifies leaving id 29 open is the false statement"
    - "Correct :204-207 to six positions, and the 0b8a865 commit-message undercount alongside it"
    - "Cut or correct :236-237's completeness-audit.md claim — the narrower true fact favours the entry"
    - "Correct the :268 line citation to NUMBERING.md:31-45"
    - "Reconcile :296 with :383-390, or state the two pairs differ and why id 29 still stays open"
    - "Reconcile the append-only rule at :16 with what 06-05 did — either restate the rule to permit correcting a falsified premise in place, or record the superseded text"
    - "Backlog, not blocking: prong 2's thinness test is not in SOURCES.md and its 'many independent publishers' clause is an unrecorded lookup; prong 4 records position instead of disposing against SOURCES.md:16"

- gap_id: G-06-9
  truth: "No statement in README is contradicted by a committed file in this repository"
  status: resolved
  previous_status: failed
  resolved_by: "06-06 tasks 1-8 (commits 4cb5c9b, 3e3dcd9, 251cad2, c850219, 3a37839, f10f8fc, d11b8a7, 467ed6e) — all eight corrected. Finding 2, the only one that shipped to installed users, also gained a check_repo.py code (benchmark-run-claim-stale, discrimination-proven). Finding 6 was closed by the second of the plan's two permitted outcomes, settled by a mutation probe against an unmutated control. Self-checked, not independently read: the closure condition remains a round-3 cold read."
  reason: "Two independent cold readers converged on four; three more found by one reader each or by the session. Eight in total. One was created by the 06-05 round itself (README still says the /config picker has not been observed while LEGAL-REVIEW.md:536-541 records observing it). One ships to installed users ('no benchmark has run' in artifact-patterns.md and both derivatives). One is the same defect class as G-06-6 #1 reintroduced in the paragraph rewritten to fix it, settled by a mutation probe with an unmutated control: README's inventory counts can be changed to any number and check_repo stays at 0 violations."
  severity: major
  test: 9
  artifacts:
    - path: "README.md"
      issue: ":86-88 and :89-91 — the /config picker 'has not been observed here' and is 'the one link in this route nothing here exercises'; contradicted by LEGAL-REVIEW.md:536-541 and ledger row 16, written this same round by commit 36fbf6c"
    - path: "skills/proof-first/references/artifact-patterns.md"
      issue: ":144 'no benchmark has run' — contradicted by README:187 and evals/benchmark/RESULTS.md:1; ships verbatim in output-styles/proof-first.md:695 and prompts/system-prompt.md:683; check_repo.py:4264's guard matches 'No benchmark has compared', a different literal"
    - path: "README.md"
      issue: ":134 'three runs against the shipped skill description' — RESULTS-trigger.md:101 records Arm A at sha 9049c7d8… against the shipped d5dd651a…; README's own :139-140 says so"
    - path: "README.md"
      issue: ":43-44 publish-location-drift 'fails the build if any ... stops agreeing' — check_repo.py:724-726 declares it compares owner segments only"
    - path: "README.md"
      issue: ":171-172 and :9-10 — bench-deal-brief.md is not what sessions are prompted with; run_benchmark.py:295 sends scenario['prompt'] only and the brief is read once inside --self-test at :1646"
    - path: "README.md"
      issue: ":264-265 'Different codes check those — catalog-count-mismatch ...' — that code reads SKILL.md, not README; mutation probe with control shows 0 violations over mutated README counts"
    - path: "README.md"
      issue: ":111-112 activation contrast — prompt-on scores 8 of 12 on the same MARKER_RE metric README cites for skill-on's 3 non-activations (RESULTS-routes.md:15-17)"
    - path: "evals/benchmark/bench-deal-brief.md"
      issue: ":10-12 still asserts 'This environment has no live network access' and calls the name-collision search an unrun item; LEGAL-REVIEW.md:617 books it Fixed with the premise expired"
  missing:
    - "Correct README:86-91 to record the /config observation and its stated limits, matching LEGAL-REVIEW.md:536-541 — a gap-closure round must not leave the two files disagreeing"
    - "Correct 'no benchmark has run' in artifact-patterns.md:144 and regenerate both derivatives; widen check_repo.py's STALE_COMPARISON_CLAIM guard to catch this literal too, since the guard for its sibling already exists"
    - "Correct README:134 to two of three runs, or drop the count"
    - "Bound README:43-44 to the owner-segment comparison the checker declares"
    - "Correct README:171-172 and :9-10 to the brief's own accurate relation — it grounds the scenario prompts rather than being sent to sessions"
    - "Correct README:264-265: name the codes that actually read README, or state plainly that the inventory counts are unenforced — the third-case sentence two lines later already shows the honest form"
    - "Decide README:111-112: either drop the contrast or carry prompt-on's 8 of 12 beside it"
    - "Reconcile bench-deal-brief.md:10-12 with ledger row 18"
    - "Backlog: README:188 'drafted twice' omits the 3 repeats; two rounds of readers have now tripped on it"

- gap_id: G-06-10
  truth: "LEGAL-REVIEW.md's reproduction-boundary material contains no sentence a committed file falsifies"
  status: resolved
  previous_status: failed
  resolved_by: "06-07 tasks 1-7, 13 (commit 908b90b). Task 1 was a decision: the review adopts check_repo.py's frozen seven-of-eight SOURCE_COINED_LABELS split over its own six-and-two, widening the prong-4 concession from two labels to seven; the disposition is unchanged and the entry now states why rather than leaving it to be noticed. The other six corrected against grep output, not recollection. Prong 2 additionally lost its unrecorded 'many independent publishers' premise — backlog, but inside a sentence two tasks had to rewrite. Self-checked, not independently read: the closure condition remains a round-4 cold read."
  reason: "Two independent readers, converging on five of seven. All six of round 2's corrections hold and were verified accurate; seven different checkably-false statements survive in the same material. The worst is that LEGAL-REVIEW.md:249-252 and :308 classify six of the eight MC names as ordinary business English while tools/check_repo.py:2952-2965 freezes seven of the eight as SOURCE_COINED_LABELS and makes them a build failure in shipped skill content — only 'metric' is excluded. The occurrence enumeration at :253-256, written by 06-06's own self-audit commit, is false against examples/deal-brief.md and evals/benchmark/bench-deal-brief.md, which both carry the two labels as section headings, and miscalls a production constant a fixture."
  severity: major
  test: 10
  artifacts:
    - path: "LEGAL-REVIEW.md"
      issue: ":249-252 and :308 — the prong-4 six/two split of the eight MC names is the inverse of tools/check_repo.py:2952-2965's SOURCE_COINED_LABELS; :308 names 'Competition' as neutral English and :2963 names it as coined"
    - path: "LEGAL-REVIEW.md"
      issue: ":253-256 'the two appear only in NUMBERING.md, in this file, and in check_repo.py's fixtures' — false against examples/deal-brief.md:26,75,89 and bench-deal-brief.md:54,130,145,185; the repo's own matcher is IGNORECASE (check_repo.py:2974); check_repo.py:2958-2959 is a production constant, and 'Paper Process' is in no fixture there"
    - path: "LEGAL-REVIEW.md"
      issue: ":239 and :301 reinstate the mnemonic ground that the correction at :224-225 retired fifteen lines earlier"
    - path: "LEGAL-REVIEW.md"
      issue: ":298-299 'NUMBERING.md says so in its own words' — NUMBERING.md:33-35 declares a one-per-element correspondence and says nothing about order provenance anywhere in :31-54"
    - path: "LEGAL-REVIEW.md"
      issue: ":340-342 enumerates two files and a command and calls it 'three files'; :433 and :731 say 'three files and a regeneration'; the tree gives four (NUMBERING.md, SKILL.md, and both derivatives)"
    - path: "LEGAL-REVIEW.md"
      issue: ":253 'nowhere else that ships' presupposes NUMBERING.md ships; README.md:367-369 says it never ships to an installed user, and :255's 'the shipped tree' uses the opposite sense four lines later"
    - path: "LEGAL-REVIEW.md"
      issue: ":237 'each labelled with the shortest ordinary English' contradicts :250-252's finding that two of the eight are terms of art, thirteen lines apart in the same section"
  missing:
    - "Reconcile the prong-4 classification at :249-252 and :308 with tools/check_repo.py's SOURCE_COINED_LABELS — either the review adopts the checker's seven-of-eight split and re-reasons the prong on it, or it states why the two classifications answer different questions and the checker's is not the reproduction-boundary one"
    - "Correct :253-256: the two labels appear as section headings in both committed deal briefs, the matcher is case-insensitive, and check_repo.py:2958-2959 is a production constant rather than a fixture"
    - "Cut the mnemonic clause at :239 and the mnemonic contrast at :301, or restate why a ground the correction retired is still available here"
    - "Correct :298-299 — NUMBERING.md declares the element correspondence, not the order; the PF-1 order claim has to be argued exactly as id 6's was"
    - "Settle the rename cost once at four files, and make :340-342, :433 and :731 agree"
    - "Reconcile :253's sense of 'ships' with README.md:367-369, or say which definition this file uses"
    - "Reconcile :237 with :250-252"
    - "Backlog, not blocking: prong 2's 'many independent publishers' clause is a premise in no committed file and carries the thinness conclusion (second round it has been raised); :56 says two live questions where items 5 and 6 carry three; :39's bolded content-item count excludes id 29, which :344-345 classifies as a shipped-content decision"

- gap_id: G-06-11
  truth: "No statement in README is contradicted by a committed file in this repository"
  status: resolved
  previous_status: failed
  resolved_by: "06-07 task 8 (commit 908b90b). Outcome 2, with outcome 1 rejected on evidence — 20% carries four meanings in the bench brief and three in the examples brief, so varying one row would leave the claim false while looking fixed. Claim bounded in README and bench-deal-brief.md in the same commit, identical row named rather than hidden. The company/person/platform separation is now mechanically held over all nine invented names (was four), discrimination-proven against an unmutated control."
  reason: "Three independent readers converged on one statement. README:9-11 says the two deal briefs share 'no company, person, platform or figure'; examples/deal-brief.md:116 and evals/benchmark/bench-deal-brief.md:177 carry a byte-identical Canonical figures row (rfp-security-weight, 20%, same description), and both decision-criteria tables read 'Security posture | 20%'. Every other same-named key between the two briefs was deliberately varied. The claim has been in bench-deal-brief.md:8 since 05-02, but commit 3a37839 — 06-06's fix for round 2's finding 5 — is what imported it into README, so the round that closed G-06-9 opened this."
  severity: major
  test: 11
  artifacts:
    - path: "README.md"
      issue: ":9-11 'shares no company, person, platform or figure with the one the examples are written against' — contradicted by the identical rfp-security-weight row at examples/deal-brief.md:116 and evals/benchmark/bench-deal-brief.md:177"
    - path: "evals/benchmark/bench-deal-brief.md"
      issue: ":8 makes the same claim about itself and has since commit 1577910; it is false against its own :177 read next to examples/deal-brief.md:116"
  missing:
    - "Decide the substance first: either vary the bench brief's rfp-security-weight so the no-shared-figure claim becomes true, or drop 'or figure' from both README:9-11 and bench-deal-brief.md:8 and state what separation the two briefs do hold (company, person and platform, all three verified this round)"
    - "Whichever is chosen, both files must be changed in the same pass — README repeats the brief's own claim, so fixing one leaves the other false"
    - "Backlog: bound README:186-188 to what run_benchmark.py:1645 actually asserts — four names of the nine examples/deal-brief.md invents. Recorded as an observation on a 2-to-1 reader split, not a gap, and it is the same class as round 2's publish-location-drift finding"

- gap_id: G-06-12
  truth: "No two committed files in this repository state things that cannot both be true"
  status: resolved
  previous_status: failed
  resolved_by: "06-07 tasks 9, 10, 11 (commit 908b90b). lint.py's ceiling restated as the property that holds rather than put in the past tense, since an environment-dependent ceiling expires again; ledger row 28 six limits; run_conformance.py five fixtures. git grep for the no-network premise now returns only the three files stating it as expired."
  reason: "A whole-tree sweep bound to no named file — new this round, because rounds 1 and 2 pointed every reader at README or LEGAL-REVIEW.md and so could not reach a contradiction between two other files. Three checkably-false statements. The first is the expired no-network premise still asserted in evals/lint.py:98-100, the file evals/proxy-sources.md:37-38 explicitly routes the reader to for the full statement of that ceiling, and the round that was meant to remove it repo-wide (commit 467ed6e, 'sweep the expired no-network premise out of the tracked tree') missed it."
  severity: major
  test: 12
  artifacts:
    - path: "evals/lint.py"
      issue: ":98-100 'this environment has no live network access' asserted as present fact; contradicted by evals/proxy-sources.md:12-14, LEGAL-REVIEW.md:720, bench-deal-brief.md:16-17 and check_repo.py:3776-3779, and proxy-sources.md:37-38 points the reader at this docstring"
    - path: "LEGAL-REVIEW.md"
      issue: ":730 ledger row 28 'its four named limits' — RESULTS-routes.md:45-50 publishes six and run_routes.py:183-190 freezes REQUIRED_CAVEATS at six keys"
    - path: "evals/conformance/run_conformance.py"
      issue: ":22-23 and :313-315 say 'the three committed transcript fixtures' and name them exhaustively; :459-465 enumerates five and all five are committed"
  missing:
    - "Restate evals/lint.py:98-100's ceiling in the past tense as the other four files do, or cut the parenthetical — the ceiling itself (a URL is never fetched) holds regardless of the environment and does not need the expired premise"
    - "Correct LEGAL-REVIEW.md:730 to six named limits"
    - "Correct run_conformance.py:22-23 and :313-315 to five fixtures, naming the two -late-phrase files the same docstring's cases 8 and 9 already describe"
    - "Consider whether the sweep brief itself belongs in every future round: this reader found three statements in three files no earlier brief had named, at the same cost as a file-scoped reader"

- gap_id: G-06-13
  truth: "LEGAL-REVIEW.md's reproduction-boundary material contains no sentence a committed file falsifies"
  status: failed
  reason: "Two independent readers, converging with a third on four. All seven round-3 corrections hold and the adopted seven-of-eight split is verified accurate line by line. Ten new checkably-false statements, nine authored by commit 908b90b while closing round 3. The worst is :288-291, which says the seven labels' absence from four files is 'mechanically held' by source-label-in-skill-content; check_repo.py:983 scopes that check to skills/*/SKILL.md plus references/*.md, so it never opens either derivative, and :322-323 rests the disposition on the claim. Two more are a sentence quoted from SKILL.md:63 that is not in SKILL.md, and the same line cited as both the rename's target and a sentence the rename leaves in place."
  severity: major
  test: 13
  artifacts:
    - path: "LEGAL-REVIEW.md"
      issue: ":288-291 'mechanically held' — check_repo.py:983's SKILL_GLOB and the candidate set at :2991-2996 never open output-styles/proof-first.md or prompts/system-prompt.md; :322-323 inherits it"
    - path: "LEGAL-REVIEW.md"
      issue: ":435-438 quotes 'one per Command of the Message element' from SKILL.md:63; the phrase occurs only at NUMBERING.md:33-34 and nowhere in skills/, output-styles/ or prompts/"
    - path: "LEGAL-REVIEW.md"
      issue: ":426 names SKILL.md:63 as a by-hand rename target while :436-439 names it as a sentence the rename leaves in place; in SKILL.md:63 the source clause and the seven labels are one sentence, so a rename rewrites it"
    - path: "LEGAL-REVIEW.md"
      issue: ":429-431 'The count is git grep -l \"Positive Business Outcomes\" ... not an estimate' — that command returns five files, because LEGAL-REVIEW.md:387 and :430 carry the string"
    - path: "LEGAL-REVIEW.md"
      issue: ":426 cites NUMBERING.md:39-45 for the by-hand edit; NUMBERING.md:48 also carries a label"
    - path: "LEGAL-REVIEW.md"
      issue: ":297-300 'All three parts were wrong' — 'in this file' was correct and 'in check_repo.py's fixtures' was correct for Economic Buyer (check_repo.py:7000-7004, :7029, :7036, :7051, :7059); what failed was 'only'"
    - path: "LEGAL-REVIEW.md"
      issue: ":23-26 'Three corrections in this file' — eight lines now carry 2026-09-22 corrections from 06-07, named by the ledger at :811 and :836"
    - path: "LEGAL-REVIEW.md"
      issue: ":245-247 'not ordinary English at all' misstates the adopted split, which says source-coined; :291-298 records five of the seven in ordinary English use"
    - path: "LEGAL-REVIEW.md"
      issue: ":48 misquotes check_repo.py:2131-2133 inside quotation marks — 'list' for 'file'"
    - path: "LEGAL-REVIEW.md"
      issue: ":362-363 'Two of the four grounds ... did not survive' — three of the four bullets carry a dated correction"
  missing:
    - "Restate :288-291 as the two-step argument it actually is: source-label-in-skill-content holds SKILL.md and references/*.md, and generate_derivatives.py --check byte-compares the derivatives to those sources. Fix :322-323 to match, and record the fenced-block ceiling (check_repo.py:2999 strips fences) the entry does not mention"
    - "Correct :435-438 — the phrase is NUMBERING.md's alone — and reconcile it with :426 so SKILL.md:63 is not on both sides of the rename; the substance changes, since renaming does rewrite SKILL.md:63"
    - "Correct :429-431's provenance, or drop the sentence and keep the four-file cost with its four citations; add NUMBERING.md:48 to the by-hand range"
    - "Correct :297-300 to name 'only' as the word that failed"
    - "Update :23-26's correction count and date list to cover 06-07's eight, or restate the paragraph so it does not carry a count that every round invalidates"
    - "Correct :245-247 to 'source-coined' and re-check that prong 2's removal still follows"
    - "Correct the :48 quotation to 'file'"
    - "Correct :362-363 to three"
    - "Backlog, not blocking: id 6's Closed-on-reasoning label against its own definition at :793-796, now further from it because 06-07 narrowed prong 2; the PF-1 section's unrecorded Force Management read, which is the same defect 06-07 removed from id 6 and left in the parallel entry; 'live and unadjudicated'; the completeness-audit.md over-read; prong 3's whole-repo negative"

- gap_id: G-06-14
  truth: "No statement in README is contradicted by a committed file in this repository"
  status: failed
  reason: "Both round-3 corrections hold and every claim-region figure recomputes. One statement, standing since commit 58530a6 in Phase 1 and missed by four rounds of cold reads: README:175 says tools/check_repo.py enforces 'all of the above' over a 17-item inventory, and the checker reads none of pressure-tests.md, proxy-sources.md, scenarios.json, lint.py, the three other runners or the RESULTS files. check_repo.py:66-68 excludes evals/ from its scan roots outright, and README:289 says the opposite for one of those items."
  severity: major
  test: 14
  artifacts:
    - path: "README.md"
      issue: ":175 'enforcing all of the above' over the :136-174 inventory — zero hits in check_repo.py for seven of the named items; :66-68 excludes evals/; README:289 concedes 'check_repo.py will not do it for you'"
  missing:
    - "Bound README:175 to what the checker reads, naming the boundary the checker already declares at :66-68 — the third-category sentence at :286-289 already shows the honest form"
    - "Consider, separately, that check_repo.py:4-5's own opening sentence is narrower than the checker it introduces (reader 2's observation, not a README defect)"

- gap_id: G-06-15
  truth: "No two committed files in this repository state things that cannot both be true"
  status: failed
  reason: "Four contradictions from the whole-tree sweep, none in a file the other three briefs name, none created by 06-07, and all three of round 3's sweep fixes verified to hold. One ships to every installed user: both derivatives tell the reader that every rule the omitted worked-examples.md illustrates 'already carries its own constructive line in SKILL.md', while eight of those rules are MC rules that check_repo.py's mc-rule-in-skill gate forbids from SKILL.md and NUMBERING.md routes to completeness-audit.md."
  severity: major
  test: 15
  artifacts:
    - path: "tools/generate_derivatives.py"
      issue: ":183-186 writes the omission notice into both derivatives (output-styles/proof-first.md:27-30, prompts/system-prompt.md:15-18); worked-examples.md carries 8 '## MC-' rules, SKILL.md carries 0 '### MC-' headings, and mc-rule-in-skill (check_repo.py:144-152) makes an MC rule in SKILL.md a build failure"
    - path: "tools/check_repo.py"
      issue: ":4235-4237 'until then this repository makes no such claim' about route equivalence; README:113-115 and evals/routes/RESULTS-routes.md:1-3 publish it, and :4279-4284 is built on the opposite premise"
    - path: "tools/generate_derivatives.py"
      issue: ":8-11 'Phase 5's benchmark is the only place such a statement could ever be sourced from'; the same script's _render_preamble() at :189-193 sources it from evals/routes/RESULTS-routes.md, and :168-175 says the old denial stopped being true at 04-15"
    - path: "evals/benchmark/run_benchmark.py"
      issue: ":476-479 'The five caveats EVAL-10 requires' and 'the same five keys', repeated at :2373; REQUIRED_CAVEATS holds six, RESULTS.md renders six, README:229 says six"
  missing:
    - "Correct the derivatives' omission notice at generate_derivatives.py:183-186 and regenerate both — the honest form names where MC constructive lines live (completeness-audit.md, which the derivatives already carry) instead of claiming SKILL.md carries them. This is the only round-4 finding that reaches an installed user; do it first"
    - "Correct check_repo.py:4235-4237 to match what :4279-4284 already assumes"
    - "Correct generate_derivatives.py:8-11 to name RESULTS-routes.md as the source its own output cites"
    - "Correct run_benchmark.py:476-479 and :2373 to six, and consider rendering the count from len(REQUIRED_CAVEATS) so a comment cannot drift from the constant beneath it"

- gap_id: G-06-16
  truth: "The sentences a gap-closure round adds are checked before the round closes"
  status: failed
  reason: "The new fourth brief, aimed at the closing round's own added lines, was the highest-yield reader of round 4 on first use. Beyond converging with the LEGAL-REVIEW readers on four findings, it reached two neither could: bench-deal-brief.md:18-20's '20% carries four different meanings inside this brief alone and three inside the other', which is wrong under both counting rules (raw occurrences are four and four; distinct meanings are two and three), and :10-12's presentation of the platform-list disjointness as mechanically held when run_benchmark.py:1649-1659 asserts only the nine names and no code compares platforms."
  severity: major
  test: 16
  artifacts:
    - path: "evals/benchmark/bench-deal-brief.md"
      issue: ":18-20 'four different meanings inside this brief alone and three inside the other' — raw occurrences are 4 and 4 (bench :128, :155, :187, :189; examples :63, :66, :87, :116); distinct meanings are 2 and 3; the sentence justifies not varying the figure"
    - path: "evals/benchmark/bench-deal-brief.md"
      issue: ":10-12 and :20-22 present 'no shared company, person or platform' as mechanically held; run_benchmark.py:1649-1659's tuple holds nine names and no platform, and no committed code compares the two briefs' platform lists"
  missing:
    - "Correct the 20% count to one stated rule, or drop the count and keep the conclusion — the argument for not varying the figure does not need a number this fragile"
    - "Split the mechanical claim at :10-12 from the authored one: the nine names are asserted by run_benchmark.py --self-test; the platform disjointness is an observation. Either say so, or add the platform assertion to the self-test the way the entity assertion was added in 06-07"
    - "Keep the fourth brief permanently: on its first run it found 2 defects no other brief reached and confirmed 4 more, and 10 of round 4's 17 findings were in the closing round's own added lines"
