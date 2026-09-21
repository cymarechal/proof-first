---
status: complete
phase: 06-legal-review-gate-launch
source: [06-VERIFICATION.md]
started: 2026-09-21
updated: 2026-09-21
rounds: 2
round_2: "06-05 gap closure — tests 7-9 re-ask tests 2, 3 and 6 of the corrected files"
round_2_result: "1 passed, 2 issues — G-06-7 and G-06-9 opened 2026-09-21"
---

## Current Test

[testing complete — round 2; 2 gaps open]

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

## Summary

total: 9
passed: 4
issues: 5
pending: 0
skipped: 0
blocked: 0

Round 1: tests 1-6 — 3 passed, 3 issues (G-06-2, G-06-3, G-06-6), all three resolved by 06-05.
Round 2: tests 7-9 — 1 passed, 2 issues (G-06-7, G-06-9).

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
  status: failed
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
  status: failed
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
