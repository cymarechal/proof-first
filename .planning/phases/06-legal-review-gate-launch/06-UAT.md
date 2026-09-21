---
status: testing
phase: 06-legal-review-gate-launch
source: [06-VERIFICATION.md]
started: 2026-09-21
updated: 2026-09-21
---

## Current Test

number: 1
name: The six confirmed sources are in bounds, and nothing was reproduced from them
expected: |
  Open SOURCES.md and follow each of the six URLs. Confirm for each that the page is public
  (no login, registration wall, or paywall) and is NOT vendor training-portal content, paid course
  material, a certification handout, an internal enablement deck, or a redistributed copy of any of
  those — the list in SOURCES.md's "Out of bounds" section.

  Then confirm that SOURCES.md, NOTICES.md, LEGAL-REVIEW.md and the phase's commit messages carry no
  sentence taken from any of those pages. Titles, publishers, URLs and dates are citations; a run of
  a source's own wording is a reproduction and does not ship.

  The three vendor pages are the ones to look at hardest. One of them is on the main site of a party
  that also sells training in the same methodology; its separate training portal lives on a different
  subdomain and was deliberately not used.
awaiting: user response

## Tests

### 1. The six confirmed sources are in bounds, and nothing was reproduced from them
expected: Every URL in SOURCES.md is public and outside the "Out of bounds" list, and no wording from any of them appears in this repository.
result: [pending]

### 2. The reproduction-boundary reasoning for WINDOWS ids 3 and 6 is sound
expected: |
  Read LEGAL-REVIEW.md's "## Reproduction boundary" section.

  For id 6 the argument is: the eight MC dimension names in NUMBERING.md's MC-1..MC-40 order are not
  a source's chosen arrangement this repository copied — they ARE the acronym, and reordering them
  would produce a different word rather than a rearranged list. Judge whether that distinction holds.

  Then judge whether the section engages the 2026-04-21 genericness holding correctly. It claims the
  holding supports one narrow point (the term is not a source identifier) and settles nothing about
  whether an expression of the methodology is protectable, because genericness is trademark and
  protectability is copyright. Confirm it neither ignores the ruling nor over-reads it.
result: [pending]

### 3. LEGAL-REVIEW.md does not read as legal advice
expected: |
  Read LEGAL-REVIEW.md's opening section. It states in words that it is a diligence record by a
  non-lawyer against public sources, that it is not legal advice and not a clearance opinion, and
  what it therefore does and does not establish.

  Saying so is not the same as reading that way. Judge whether a reader could come away treating any
  part of it — particularly the trademark sections and the reproduction-boundary dispositions — as a
  professional opinion rather than as a record of what was looked at on a date.
result: [pending]

### 4. README's claim region reads as an honest report of a mixed result
expected: |
  Read README.md's "### What the benchmark measured" section, between the two claim-region markers.

  It states that on evidence the skill won 45 pairs, on clarity 32, and on persuasive force it LOST
  38 of 48 — the judge preferred the un-skilled draft in four pairs out of five. The 38-loss result
  is deliberately in its own sentence rather than a subordinate clause, and the caveats follow the
  number rather than softening it.

  The question is whether it READS that way to someone meeting this project for the first time.
  Would a technical evaluator feel the unfavourable dimension was reported plainly, or feel it was
  buried? This is the one judgement the author of the text cannot make about it.
result: [pending]

### 5. The output style is listed and selectable in /config
expected: |
  NOT PERFORMED in the executing session — a non-interactive session has no picker to open, and
  copying the file without being able to observe the result would have changed your configuration
  directory for no verification gain.

  On a machine with Claude Code and a /config picker:
    mkdir -p ~/.claude/output-styles
    cp output-styles/proof-first.md ~/.claude/output-styles/
  Start Claude Code, open /config, and record whether "proof-first" is listed and whether selecting
  it persists for the session. Note the platform.

  04-15 already measured the half a script can reach: the style's content does arrive in a live
  session, and an unrouted control on the same prompt cited none of this project's rule markers.
  What is unobserved is the single word *permanently*.

  WINDOWS.md id 16 and DIST-03's second half close on this observation, or stay open.
result: [pending]

### 6. A cold read of README by someone who did not write it
expected: |
  NOT PERFORMED AS A COLD READ in the executing session — the agent that wrote this round's README
  edits would have been the reader, and no independent reader was available.

  WINDOWS.md id 17 records three consecutive rounds in which check_repo.py reported zero violations
  and a cold human reader found a false sentence on the first pass. The method is a reader who did
  not write the text; a self-read is not a substitute, and the refusal to build a fuzzy-proxy gate
  for this class stands.

  Read README.md end to end and check whether any two passages contradict each other, with attention
  to the new claim region against the "## Status" prose and against the repository-layout tree.

  For context, not as a substitute: a mechanical cross-reference of twelve checkable claims was run
  and found nothing checkably false — rule count, worked-pair count, every layout-tree and "What
  exists today" path, all nine pooled tallies and the direction count against RESULTS.md's rendered
  tables, the trigger summary against RESULTS-trigger.md's totals, and the absence of the two
  sentences 06-03 superseded. Four apparent findings all proved to be defects in the checking script.

  WINDOWS.md ids 12 and 17 close on this read, or stay open with what it found.
result: [pending]

## Summary

total: 6
passed: 0
issues: 0
pending: 6
skipped: 0
blocked: 0

## Gaps
