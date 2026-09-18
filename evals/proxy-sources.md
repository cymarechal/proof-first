# proxy-sources.md

Authoritative term registry for `evals/lint.py`'s proxy checks. This file is the single source
of truth the linter's provenance checks read their allow-listed terms from — adding a term to
`evals/lint.py`'s `PROXY_TERMS`, `SUPERLATIVE_TERMS`, or `HEDGE_TERMS` with no matching row here
makes `proxy-term-unsourced` fail the build, exactly as `NUMBERING.md` governs `check_repo.py`'s
ID ranges.

This environment has no live network access. The membership recorded below is the membership
`.planning/phases/05-evaluation-harness/05-RESEARCH.md` Decision 1 established from reading each
source's own published page in an earlier session; it is not independently re-fetched here. This
is the same posture `SOURCES.md` already takes for its own rows (`Where: to confirm at LEG-04`) —
a documented, disclosed provenance, not a live-verified one.

## The two sources

Exactly two source labels exist in this registry: `A` and `B`. No third label is ever valid.

- **`A` — Wikipedia:Manual of Style/Words to watch** (`MOS:WTW` / `MOS:PUFFERY`).
  `https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch` — a community-maintained
  style guide naming unsupported superlatives ("peacock terms") and vague hedging language, with no
  relationship to this project or to Proof First.
- **`B` — GSA plainlanguage.gov / digital.gov "Avoid jargon"**.
  `https://digital.gov/guides/plain-language/principles/avoid-jargon` (underlying word list at
  `https://github.com/GSA/plainlanguage.gov/blob/main/_pages/guidelines/words/avoid-jargon.md`) — a
  U.S. federal government resource maintained under the Plain Writing Act of 2010, naming
  corporate-jargon terms, with no relationship to this project or to Proof First.

**Declared ceiling.** This registry proves every shipped term traces to one of these two named
external sources, and that none traces only to this repository's own content. It cannot prove a
human never looked at `skills/proof-first/references/worked-examples.md` while deciding which
external-list entries to ship, and it does not claim the shipped terms are absent from this
repository's own prose — measured 2026-09-18, nine of eighteen candidate terms already appear in
`worked-examples.md` or `examples/before-after.md`, which is the expected consequence of a skill
that illustrates itself with the puffery it deletes. See `evals/lint.py`'s module docstring for the
full statement of this ceiling.

## Buzzword and jargon terms

Drives `PROXY_TERMS` and the `buzzword-term` violation code — every registered term, mixing both
sources, sorted ascending by term.

| Term | Source | URL |
|---|---|---|
| acclaimed | A | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch |
| best-in-class | A | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch |
| comprehensive | B | https://digital.gov/guides/plain-language/principles/avoid-jargon |
| cutting-edge | A | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch |
| facilitate | B | https://digital.gov/guides/plain-language/principles/avoid-jargon |
| iconic | A | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch |
| impactful | B | https://digital.gov/guides/plain-language/principles/avoid-jargon |
| landmark | A | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch |
| leading | A | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch |
| leverage | B | https://digital.gov/guides/plain-language/principles/avoid-jargon |
| premier | A | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch |
| renowned | A | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch |
| revolutionary | A | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch |
| robust | B | https://digital.gov/guides/plain-language/principles/avoid-jargon |
| seamless | B | https://digital.gov/guides/plain-language/principles/avoid-jargon |
| solution | B | https://digital.gov/guides/plain-language/principles/avoid-jargon |
| state-of-the-art | A | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch |
| streamline | B | https://digital.gov/guides/plain-language/principles/avoid-jargon |
| synergy | B | https://digital.gov/guides/plain-language/principles/avoid-jargon |
| unparalleled | A | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch |
| utilize | B | https://digital.gov/guides/plain-language/principles/avoid-jargon |
| world-class | A | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch |

## Superlative terms

Drives `SUPERLATIVE_TERMS` and the `unquantified-superlative` violation code. A deliberately
separate label-`A` list from the buzzword table above, so a sentence exercising this code does not
also, as a side effect, exercise `buzzword-term` — the two codes are tested independently.

| Term | Source | URL |
|---|---|---|
| exceptional | A | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch |
| extraordinary | A | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch |
| outstanding | A | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch |
| unbeatable | A | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch |
| unrivaled | A | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch |

## Hedge and modal terms

Drives `HEDGE_TERMS` and the `unbounded-modal` violation code. `PF-4.3` names `may`, `might`, and
`could` as this catalog's own possibility modals — the same three words Wikipedia's Words-to-watch
page treats as unattributed hedging language when a claim's certainty is not backed by a stated
condition.

| Term | Source | URL |
|---|---|---|
| could | A | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch |
| may | A | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch |
| might | A | https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Words_to_watch |
