---
status: diagnosed
trigger: "CAT-10 gap G-02-2: two must-not-fire phrasings activated proof-first in the 2026-09-20 live trigger run"
created: 2026-09-20
updated: 2026-09-20
mode: find_root_cause_only
gap_id: G-02-2
requirement: CAT-10
windows_id: 24
---

Every claim in this file is labelled **VERIFIED** (checked in a named file at a named
line, or produced by a named command whose output is quoted) or **HYPOTHESIS**
(plausible, not measured here). An unlabelled guess in this file would be the exact
failure this repository exists to prevent. Where the evidence does not reach, this file
says so instead of reaching further.

No shipped file was modified during this investigation. Every mutation described below
was made to a throwaway `rsync` copy of the tree in a scratchpad directory outside the
repository, and the live tree's gates were confirmed green before and after.

---

## Symptom

Requirement CAT-10 states the SKILL.md frontmatter `description` "triggers the skill
reliably on presales writing requests, acting as an explicit trigger list."

Measured live 2026-09-20 by `evals/trigger/run_trigger_test.py` (`claude-sonnet-5`,
`claude` 2.1.267, one fresh `claude -p` session per phrasing in a temp dir outside the
repo with only `skills/proof-first/` installed, no `--bare`, verdict read from each
session's own `Skill` tool-use event rather than its prose):

- Must-fire: 9 of 9 fired. Correct.
- Must-not-fire: 3 of 5 stayed quiet. Two fired that should not have:
  1. `Build me a slide deck for the kickoff meeting.`
  2. `Work out pricing and sizing for a 500-seat deployment.`

Source rows: `evals/trigger/RESULTS-trigger.md:33-34`, `evals/pressure-tests.md:67-68`.

---

## Investigation

### Baseline: the live tree is green before anything

```
$ python3 tools/check_repo.py
check_repo: 0 violations                                   EXIT=0

$ python3 tools/generate_derivatives.py --check              EXIT=0
$ python3 evals/trigger/run_trigger_test.py --self-test
self-test PASS: 3 detector cases, 2 table rows, 2 scope-hash cases   EXIT=0
$ python3 evals/lint.py --self-test
self-test PASS - verified violation codes: buzzword-term, ...        EXIT=0
```

So every failure reported below is caused by the mutation that produced it, not by
pre-existing tree state.

### Q1 — Does the `description` contain any negative or exclusionary clause?

**VERIFIED: No. Not one.**

The full frontmatter `description` (`skills/proof-first/SKILL.md:3-10`), whitespace-collapsed:

> Write or check RFP and RFI responses, solution proposals, executive summaries, and demo
> or discovery documents for technical presales and bid teams. Use for a scored technical
> response, a customer-facing proposal, or a check pass over a finished draft that flags
> invented metrics, missing evidence, undisclosed customer references, competitor
> comparisons, compliance claims, and unquantified buzzwords before the document ships to
> a buyer.

A scan for every common negation and exclusion token over that collapsed string returned
an empty list:

```
$ python3 -c "...re.findall(r'\b(not|never|no|except|exclude[sd]?|excluding|
                 without|does not|avoid|beyond|outside)\b', collapsed, re.I)"
NEGATION TOKENS FOUND: []
COLLAPSED LEN: 439
HEAD14 SHA256: d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675
```

Two things confirmed as a side effect: the 439-character length claimed at
`evals/pressure-tests.md:19` is accurate, and the live hash matches the one the Scope
section binds the rows to (`evals/pressure-tests.md:25`).

The description is two sentences, both purely inclusive. Sentence one names artifact
types and an audience. Sentence two names a use and a list of things the skill flags. It
states what the skill is for and never once states what it is not for.

### Q2 — Do the two over-firing phrasings correspond to exclusions in the body?

**VERIFIED: The lexical correspondence is exact for both.**

`skills/proof-first/SKILL.md:308` (`## Limits`):

> What this skill does not produce: slide decks and visual design, pricing calculation,
> sizing, or commercial modelling, CRM or bid-management integration, and marketing or
> brand writing.

| Over-firing phrasing | Limits text it names | Correspondence |
|---|---|---|
| Build me a **slide deck** for the kickoff meeting. | "**slide decks** and visual design" | exact head-noun match (singular/plural) |
| Work out **pricing** and **sizing** for a 500-seat deployment. | "**pricing** calculation, **sizing**, or commercial modelling" | exact match on both nouns |

`.planning/PROJECT.md:52-53` carries the same two exclusions as the first two bullets of
its Out of Scope list, so these are agreed project scope, not incidental wording.

**But the correspondence is not the whole story, and the orchestrator hypothesis stops
one row too early.** A third must-not-fire phrasing also names a Limits exclusion, and it
did **not** fire:

| Phrasing | Limits text it names | Observed |
|---|---|---|
| Write **launch copy** for our new product announcement. | "**marketing** or **brand writing**" (`SKILL.md:308`); "Marketing copy, brand writing, **launch posts**" (`PROJECT.md:57`) | did not fire |

**VERIFIED:** three of the five must-not-fire phrasings name a stated Limits exclusion.
Two fired; one did not. Whatever explains the two over-fires must also explain why the
third exclusion-naming phrasing stayed quiet. "The body is not read" cannot, on its own,
because the body is equally unread for all three.

### Q3 — Is it structurally true that only the frontmatter `description` is read at activation?

This is the load-bearing claim in the hypothesis and it needs splitting in two.

**What this repository establishes — VERIFIED as a recorded repo belief, not as an
independently measured fact:**

`.planning/research/STACK.md` (mirrored verbatim into `.claude/CLAUDE.md`) states of the
`description` key: *"this is the only field an idle agent reads at startup, so keyword
density matters for activation."* It sources this to `https://agentskills.io/specification`,
fetched directly, and marks it HIGH confidence. The same document describes the standard's
progressive-disclosure model: `SKILL.md` body and `references/` load on invocation, not
before it.

**What this repository measures — VERIFIED, and it is consistent with the claim without
proving it:**

The runner's design is itself a partial argument. `run_trigger_test.py:150-201` installs
only `skills/proof-first/` into a fresh temp dir and passes nothing in the prompt naming
the skill; its docstring (lines 6-11) states the question as "did the harness activate
`proof-first` on its own, from the skill's frontmatter `description` alone." The must-fire
half returning 9 of 9 (`RESULTS-trigger.md:23-31`) is consistent with the description
being sufficient for activation. It says nothing about whether the body was *also*
available.

**What I did not and cannot establish here — stated plainly:**

Nothing in this repository directly observes what the harness loads at activation time.
No transcript survives: `run_trigger_test.py:390-391` writes per-session streams to a
`tempfile.mkdtemp()` directory when `--transcripts` is not passed, and `ls evals/trigger/`
shows only `RESULTS-trigger.md`, `run_trigger_test.py`, and `__pycache__`. The 2026-09-20
run's `system/init` events — which would show what the session was given — are gone.

**Verdict on Q3: the structural claim is CONFIRMED as this repository's own sourced,
HIGH-confidence reading of the Agent Skills standard, and is consistent with every
observation here. It is not independently measured in this repository, and this file does
not upgrade it to measured.** It is strong enough to act on. It is not strong enough to
be cited as a Proof First measured claim.

### Q4 — What exactly breaks if the description string changes?

Measured by copying the tree to a scratchpad, appending a negative clause to the
description, and running every gate. Details in **Blast radius** below.

### Q5 — Is there a competing explanation the hypothesis misses?

**VERIFIED, and this is the most important finding in the investigation: lexical keyword
pull is refuted as the mechanism for both over-fires.**

Content-word overlap between each probe phrasing and the 439-character description
(stopwords removed):

```
Build me a slide deck for the kickoff meeting.                 overlap=NONE
Work out pricing and sizing for a 500-seat deployment.         overlap=NONE
Write launch copy for our new product announcement.            overlap=['write']
Write the API reference docs for the /migrations endpoint.     overlap=['write']
Rewrite this paragraph in plain English for a general reader.  overlap=NONE
I need an executive summary for the Halverton board deck.      overlap=['executive']
```

The two phrasings that **did** fire share **zero** content words with the description.
Two that did **not** fire share `write`. A keyword-overlap model predicts the opposite of
what was observed.

Note also the third row: the description contains "discovery **documents**", and
"Write the API reference **docs**" did not fire. Lexical proximity on the artifact noun
was not sufficient there either.

This has a direct consequence for the candidate pull phrases named in the brief and in
`evals/pressure-tests.md:89-92` ("for technical presales and bid teams", "a customer-facing
proposal"). Those are **semantic** pull claims, and the data neither confirms nor refutes
them — it only rules out the lexical version. See Open causal questions.

### Q6 — How much can a re-run prove?

Computed, not asserted. See **What a gap-closure plan must do** below.

---

## Root cause (VERIFIED parts)

**One-line root cause: the frontmatter `description` — the only surface the harness reads
when deciding whether to activate — is a purely inclusive 439-character list with zero
negation tokens, while every exclusion this project has agreed lives in `SKILL.md`'s body
`## Limits` section and in `PROJECT.md`'s Out of Scope list, neither of which is available
at activation time. The trigger surface cannot state a boundary it does not contain.**

Verified components:

1. **The description contains no negative clause.** Zero negation tokens over the
   collapsed 439-character string (`SKILL.md:3-10`). Command and output in Q1.
2. **The exclusions exist and are agreed.** `SKILL.md:308` and `PROJECT.md:52-53,57` name
   slide decks, pricing/sizing/commercial modelling, and marketing/brand writing.
3. **The two over-firing phrasings name two of those exclusions, one for one, with exact
   head-noun matches.** Table in Q2.
4. **The placement asymmetry is real.** The exclusion text this repository needs already
   exists, agreed and reviewed, in the one place the trigger cannot read it — given the
   standard's activation model as this repo records it (Q3).

**The orchestrator hypothesis is CONFIRMED on its structural claim** — this is a placement
failure, the description encodes inclusion only, and the exclusion text already exists in
the wrong place.

**It is INCOMPLETE on its causal claim.** "The harness never sees the exclusions" is a
statement about a *missing* signal. It does not explain the *differential*: three probe
phrasings name a Limits exclusion and the body is equally invisible for all three, yet
only two fired. Something in the description is actively pulling those two in, and Q5
verifies it is not lexical overlap. The missing negative clause is necessary to the
defect. It is not demonstrated to be sufficient.

This matters for the fix, and it is the difference between a diagnosis and a guess:
**adding a negative clause removes a missing constraint, but the mechanism that produced
the positive pull remains unidentified.**

---

## Open causal questions (HYPOTHESIS — none of this is measured)

**H1 — The pull is semantic, not lexical.** With lexical overlap refuted, the remaining
candidate is that the harness's activation decision is made on meaning-similarity between
the request and the description, in which case:

- *"for technical presales and bid teams"* names an **audience** rather than a document.
  Pricing and sizing a 500-seat deployment is squarely presales-and-bid-team work, so an
  audience-shaped description collects it. This is the pull `pressure-tests.md:89-92`
  already guessed at, and it is the strongest available candidate for over-fire 2.
  **HYPOTHESIS. Live candidate.**
- *"a customer-facing proposal"* and *"executive summaries"* both name deliverables that
  are, in practice, frequently slide decks. That is the strongest available candidate for
  over-fire 1. **HYPOTHESIS. Live candidate, weaker than the above** — nothing in the
  prompt "Build me a slide deck for the kickoff meeting" names a customer, a proposal, or
  a summary, so this requires the model to supply the bridge itself.
- *"demo or discovery documents"* — a demo asset is very often a deck. **HYPOTHESIS. Live
  candidate for over-fire 1**, and arguably closer than "customer-facing proposal", since
  "demo" and "slide deck" co-occur more tightly than "proposal" and "kickoff".
- *"Write or check"* as a bare verb pair. **Considered and judged NOT a live pull**:
  "Write launch copy" and "Write the API reference docs" both open with the same verb and
  both stayed quiet.

**H2 — The harness does not simply fire on any writing request.** Partially supported:
three of five must-not-fire rows stayed quiet, two of them plain writing tasks. So a
blanket "fires on anything writing-shaped" model is inconsistent with the data.
**HYPOTHESIS, with in-repo evidence against the blanket model.**

**H3 — Row 5 is confounded and should not be counted as a clean non-fire.** `Rewrite this
paragraph in plain English for a general reader.` did not fire. `--bare` is deliberately
off (`run_trigger_test.py:18-25`), so the operator's `$HOME` configuration loaded, and
`simple-english` **is** installed there — verified at
`/Users/cymarechal/devoteam/.claude/plugins/marketplaces/simple-english/skills/simple-english/SKILL.md`.
That phrasing is close to verbatim from `simple-english`'s own trigger description. A
competing skill winning the selection is not the same evidence as `proof-first`'s
description correctly declining. **HYPOTHESIS about the cause; the install is VERIFIED.**

**H4 — Negation handling at activation time is untested here.** The proposed fix assumes
a harness deciding activation will correctly apply a negative clause inside a description
— that "Not for slide decks" suppresses rather than merely adding the token "slide decks"
to the surface the matcher sees. **Nothing in this repository tests that.** Under H1
(semantic matching), appending exclusion nouns could plausibly *increase* similarity to
the excluded prompts rather than decrease it. **HYPOTHESIS, and it is the single largest
risk to the fix.** The gap-closure plan must treat the negative clause as an experiment
with a real chance of null or inverted effect, not as a repair.

**H5 — What would discriminate.** Capturing session transcripts (`--transcripts`, already
supported at `run_trigger_test.py:361-362`) and reading each `system/init` event would
show what the session was actually given at activation, settling Q3 by measurement rather
than by citation, and would show which other installed skills were candidates. Costs
nothing beyond the sessions already planned. **Not done here; recommended.**

---

## Blast radius of a fix

### Carriers of the description string

Found by `grep -rn "Write or check RFP and RFI"` across the tree:

| Path | What it carries | How it is maintained | Gate that catches drift |
|---|---|---|---|
| `skills/proof-first/SKILL.md:3-10` | the source, 439 chars collapsed | hand-edited | `frontmatter-description-invalid` (length bounds only) |
| `output-styles/proof-first.md:3-10` | **verbatim copy** of the whole block | **generated** by `tools/generate_derivatives.py` (`render_output_style`, line 190) | `skill-derivative-stale` + `generate_derivatives.py --check` — **VERIFIED to fire** |
| `prompts/system-prompt.md:1` | not the description text, but the source-set `sha256` stamp | **generated** (`render_system_prompt`, line 208) | same two — **VERIFIED to fire** |
| `.claude-plugin/plugin.json:4` | **first sentence only**, 148 chars | **hand-maintained** | **none — VERIFIED silent** |
| `.claude-plugin/marketplace.json:7` and `:13` | same 148-char first sentence, twice | **hand-maintained** | `plugin-manifest-invalid` enforces the two JSON copies equal *each other*; **nothing binds either to SKILL.md — VERIFIED silent** |
| `evals/pressure-tests.md:18-19` | quotes the first line verbatim; states length 439 | hand-maintained prose | **none — no script reads these two facts** |
| `evals/pressure-tests.md:25` | `head -14` sha256 | hand-maintained | `run_trigger_test.py:380-384` halts — **VERIFIED to fire** |
| `evals/trigger/RESULTS-trigger.md:16` | the same sha256 | regenerated by a full run | none directly; stale by construction once the hash changes |

**The UAT gap entry G-02-2 is wrong on one point and must be corrected before planning.**
`02-UAT.md:68-73` states that `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
and `output-styles/proof-first.md` are all "regenerated by tools/generate_derivatives.py".
Only the third is. `generate_derivatives.py:96-97` declares exactly two outputs
(`OUTPUT_STYLE_PATH`, `SYSTEM_PROMPT_PATH`) and `_render_both` (line 217) returns exactly
those two. The two JSON manifests are hand-maintained and carry a truncated 148-character
first-sentence variant, not the full string. The gap entry also omits `prompts/system-prompt.md`
entirely, which its own generator does touch.

Proved by experiment — with the mutated description **and derivatives regenerated**, the
stale manifests pass:

```
$ python3 tools/generate_derivatives.py           EXIT=0
$ python3 tools/check_repo.py
check_repo: 0 violations                          EXIT=0
SKILL.md mentions the new exclusion clause: True
plugin.json mentions it: False
```

A plan that trusts `check_repo.py` to catch manifest drift will ship a plugin marketplace
listing whose description contradicts the skill's own.

### Gates that fire when the description changes

Mutation used: appended `Not for slide decks or visual design, pricing, sizing, or
commercial modelling, or marketing and brand writing.` to the end of the description
block (collapsed length 439 → 551).

```
$ python3 tools/check_repo.py                                     EXIT=1
skill-derivative-stale output-styles/proof-first.md's stamp records sha256:2b7735d8...,
  but a fresh hash of the named sources is sha256:91e8d025... -- run python3 tools/generate_derivatives.py to re-sync
skill-derivative-stale prompts/system-prompt.md's stamp records sha256:2b7735d8...,
  but a fresh hash of the named sources is sha256:91e8d025... -- run ... to re-sync

$ python3 tools/generate_derivatives.py --check                   EXIT=1
  output-styles/proof-first.md differs ... starting at line 10
  prompts/system-prompt.md differs ... starting at line 1

$ python3 evals/trigger/run_trigger_test.py --model claude-sonnet-5   EXIT=1
ERROR: evals/pressure-tests.md binds its rows to description sha256 d5dd651a...
  but the live SKILL.md hashes to 52455558.... The rows must be re-authored against
  the new description, not filled in.
```

Note the third: the runner halts **before opening a single session**. Re-authoring the
Scope hash is a precondition for the re-run, not a cleanup after it. Getting the order
wrong costs nothing but wastes a cycle.

### The 200-character constraint in the UAT gap is backwards and would fail the build

`02-UAT.md:80` instructs: *"Keep the description within the 200-character claude.ai ceiling
discipline the stack notes flag."*

**VERIFIED that following this instruction breaks the repo.** `tools/check_repo.py:1572-1573`
sets `DESCRIPTION_MIN = 200`, `DESCRIPTION_MAX = 1024`, and enforces 200 as a **floor**:

```
$ # description shortened to 133 chars, derivatives regenerated
$ python3 tools/check_repo.py
frontmatter-description-invalid skills/proof-first/SKILL.md description length 133
  is below the 200-character floor                                EXIT=1
```

`check_repo.py:187-190` says so in its own docstring: *"200 is this project's own chosen
floor, not a specification requirement; 1024 is the specification's own ceiling."*

This is not an accident. `.planning/phases/02-.../02-CONTEXT.md:84` records **decision
D-30**: *"The description is a front-loaded trigger list of roughly 400–600 characters. No
target harness enforces 200 — the four DIST requirements name the skills CLI, the plugin
marketplace, an output style, and a paste-able system prompt, not claude.ai upload...
Accepted cost: this closes off a claude.ai upload path without an edit."* The claude.ai
200-char figure is itself flagged LOW confidence in `.planning/research/STACK.md:180`.

The usable budget is therefore **200–1024 hard, 400–600 by decision D-30**. The current
439 sits inside it; the probe at 551 also sits inside it. There is room for an exclusion
clause without reopening D-30.

### Downstream records

`.planning/REQUIREMENTS.md:21` (CAT-10 verdict text) and `:141` (the Gaps Found row);
`.planning/WINDOWS.md` id 24 (open). Both carry the current measurement in prose and both
need re-verdicting against whatever a re-run actually measures. WINDOWS id 4 is already
`fixed` and is a different entry — do not reuse it.

---

## What a gap-closure plan must do and must not do

### Must do

1. **Re-author the Scope hash first.** `evals/pressure-tests.md:25` must carry the new
   `head -14 skills/proof-first/SKILL.md | shasum -a 256`, and the quoted first line at
   `:18` and the length figure at `:19` must both be updated to match, or the file states
   two falsifiable facts that are false. The runner halts before any session otherwise.
2. **Blank every Observed / Date / Harness cell in both tables** (`:46-56` and `:64-70`).
   `pressure-tests.md:28-30` says so in its own words: observations do not transfer across
   a description change. Carrying them forward would be the exact defect this product
   exists to name.
3. **Hand-update `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.** Three
   sites, one file plus two in the other. No generator touches them and no check catches
   them. Decide explicitly whether they carry the new first sentence only (current pattern)
   or gain the exclusion clause too, and write the decision down.
4. **Run `python3 tools/generate_derivatives.py` with no flag**, then confirm
   `python3 tools/check_repo.py` exits 0 and `python3 tools/generate_derivatives.py --check`
   exits 0.
5. **Keep the collapsed length in 400–600** (D-30), hard-bounded 200–1024 by
   `frontmatter-description-invalid`. Reuse the agreed `SKILL.md:308` / `PROJECT.md:52-57`
   wording; inventing new scope in the trigger surface would make it disagree with the body.
6. **Pass `--transcripts <dir>` on the re-run and keep the captures.** Free, already
   supported, and it is the only way to settle Q3 and H3 by measurement rather than by
   citation. Without it the next investigation starts where this one did, with no evidence.
7. **Decide N before running, and record the pre-fix rate at the same N** — see below.
8. **Re-verdict `REQUIREMENTS.md` CAT-10 and close or update `WINDOWS.md` id 24** against
   what was measured, not against what was intended.

### Must not do

1. **Must not treat one quiet session per phrasing as a fix.** Numbers, computed here:

   - The current evidence is one session per phrasing. A single "fired" gives a 95%
     Clopper-Pearson interval for that phrasing's true fire rate of **[0.050, 1.000]**. A
     single "did not fire" gives **[0.000, 0.950]**. Both are almost the entire unit
     interval. Neither observation constrains anything.
   - Zero fires in n sessions, 95% upper bound on the true rate:
     n=1 → p ≤ 0.95 · n=3 → p ≤ 0.63 · **n=5 → p ≤ 0.45** · **n=10 → p ≤ 0.26** ·
     n=20 → p ≤ 0.14 · n=30 → p ≤ 0.10 · n=59 → p ≤ 0.05.
   - So a 5-of-5-quiet result at n=1 is fully consistent with each phrasing still firing
     up to 95% of the time. It would be indistinguishable from the current run by luck.

2. **Must not claim improvement without a paired pre-fix measurement at the same N.**
   Fisher exact on one phrasing, before-vs-after:

   | n per phrasing | before | after | Fisher p | |
   |---|---|---|---|---|
   | 5 | 3/5 fired | 0/5 | 0.167 | not significant |
   | 5 | 5/5 fired | 0/5 | 0.008 | significant |
   | 10 | 2/10 fired | 0/10 | 0.474 | not significant |
   | 10 | 5/10 fired | 0/10 | 0.033 | significant |
   | 10 | 7/10 fired | 0/10 | 0.003 | significant |
   | 20 | 4/20 fired | 0/20 | 0.106 | not significant |

   The detectable effect depends entirely on the pre-fix rate, which is **currently
   unknown** — one observation is not a rate, as `RESULTS-trigger.md:48-49` already says.
   If the true pre-fix rate on those two phrasings is around 20%, even n=20 cannot
   distinguish the fix from noise. **Measuring the old description at the chosen N is not
   optional; without it there is no denominator.**

3. **Must not ignore the session cost.** Full 14-row table: n=1 → 14 sessions · n=3 → 42 ·
   n=5 → 70 · n=10 → 140. Doubled if the old description is run as a paired control:
   n=3 → 84, n=5 → 140, n=10 → 280.

   **Recommendation: n=5, paired, 140 sessions total**, giving p ≤ 0.45 per phrasing on a
   clean sweep. `evals/benchmark/` already uses 3 repeats (`r0/r1/r2`), so n=3 (84 paired
   sessions) is the in-repo precedent and the cheaper honest floor. Either is defensible.
   n=1 is not. **Whichever is chosen, the resulting `RESULTS-trigger.md` must state the
   bound reached and must not state a percentage** — `pressure-tests.md:10-12` and
   `run_trigger_test.py:13-16` both forbid computing a rate from this file, and that
   prohibition holds at n=5 as much as at n=1 unless the runner is redesigned to report
   intervals.

4. **Must not close CAT-10 on the must-not-fire half alone.** 9 of 9 must-fire is the
   current baseline. A narrowed description that suppresses a must-fire row trades one
   measured defect for another. Closure requires both halves.

5. **Must not present the negative clause as a verified repair.** Per H4, no evidence in
   this repository shows that a harness applies negation correctly when deciding
   activation, and under the semantic-matching hypothesis H1 the exclusion nouns could
   raise similarity to the excluded prompts rather than lower it. If the re-run shows no
   improvement, that is a real possible outcome, and the plan should say in advance what
   it will do then — most likely removing the audience-naming phrase "for technical
   presales and bid teams" (H1's strongest candidate) as a second, separately-measured
   intervention rather than bundling both changes into one run and losing the ability to
   attribute the effect.

6. **Must not change two things in one measured run.** Adding a negative clause and
   removing "for technical presales and bid teams" are two distinct interventions against
   two distinct mechanisms. Bundled, a null result is uninterpretable and a positive result
   cannot be attributed.

7. **Must not trust `02-UAT.md:80`'s 200-character instruction.** It inverts the floor
   `check_repo.py` enforces and contradicts decision D-30. Correct the gap entry.

8. **Must not trust `02-UAT.md:68-73`'s claim that the two JSON manifests are generated.**
   They are not. Correct the gap entry, and add `prompts/system-prompt.md` to it.

---

## Reproduction commands

Baseline, live tree, all green, no live sessions, no writes:

```bash
cd /Users/cymarechal/devoteam/devoteam/technical-presales
python3 tools/check_repo.py                          # 0 violations, exit 0
python3 tools/generate_derivatives.py --check        # exit 0
python3 evals/trigger/run_trigger_test.py --self-test # exit 0
python3 evals/lint.py --self-test                    # exit 0
```

The description and its two facts:

```bash
sed -n '3,10p' skills/proof-first/SKILL.md
head -14 skills/proof-first/SKILL.md | shasum -a 256
# -> d5dd651a99ccd63b74805c493217c349053ca33d3743265cdd913dfd28f60675
sed -n '308p' skills/proof-first/SKILL.md            # the Limits exclusions
sed -n '50,57p' .planning/PROJECT.md                 # PROJECT.md Out of Scope
```

Every carrier of the string:

```bash
grep -rn "Write or check RFP and RFI" --include="*.md" --include="*.json" . \
  | grep -v "^./.git/" | grep -v "^./.planning/"
```

The blast-radius experiment, in a throwaway copy — never in the live tree:

```bash
SP=$(mktemp -d)
rsync -a --exclude '.git' /Users/cymarechal/devoteam/devoteam/technical-presales/ "$SP/"
cd "$SP"
# append any negative clause to the description block in skills/proof-first/SKILL.md, then:
python3 tools/check_repo.py                          # -> 2x skill-derivative-stale, exit 1
python3 tools/generate_derivatives.py --check        # -> 2 files differ, exit 1
python3 evals/trigger/run_trigger_test.py            # -> scope-hash halt, exit 1, zero sessions
python3 tools/generate_derivatives.py                # re-sync
python3 tools/check_repo.py                          # -> 0 violations: manifests drift SILENTLY
python3 -c "import json;print(json.load(open('.claude-plugin/plugin.json'))['description'])"
rm -rf "$SP"
```

The 200-character floor:

```bash
# in a throwaway copy, shorten the description below 200 collapsed chars, regenerate, then:
python3 tools/check_repo.py
# -> frontmatter-description-invalid ... length 133 is below the 200-character floor, exit 1
grep -n "DESCRIPTION_MIN\|DESCRIPTION_MAX" tools/check_repo.py    # 1572-1573
grep -n "D-30" .planning/phases/02-rule-catalog-integrity-skill-md-core/02-CONTEXT.md
```

The statistics quoted above (Clopper-Pearson bounds, Fisher exact, session counts) were
computed with a stdlib-only `math.comb` script; the inputs are in the tables themselves
and any equivalent implementation reproduces them.

**Deliberately not run here:** `python3 evals/trigger/run_trigger_test.py --model claude-sonnet-5`
without the scope-hash halt. That is 14 live sessions and it is the gap-closure plan's
measurement, not diagnosis's.
