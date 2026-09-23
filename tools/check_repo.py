#!/usr/bin/env python3
"""Structural and textual consistency checker for this repository's registries.

This script is a structural and textual consistency check over this
repository's registries and the shipped files that cite them. A live run
opens 23 files. README.md's "## Status" section enumerates every one of them
and names what is deliberately not opened, in the bullet whose sentence begins
"A live run opens 23 files". That enumeration is the single place this scope is
written down, and it is pointed at here rather than restated, so there is one
statement to keep true instead of two. The section is the one frozen as
README_STATUS_HEADING below, and the bullet is anchored by its opening words
rather than by a line number, because a line number in README moves whenever a
bullet above it is edited.
It does not read framework source material and it cannot judge whether a
paraphrase reproduces proprietary text — that judgement is Phase 6's legal
review gate (LEG-04). It imports
only the Python standard library; no package-manager dependency is
introduced by this file or by the CI job that runs it.

It also does not compare two factual assertions in the same document for
consistency (G-04-8): detecting that one passage contradicts another,
fifty-odd lines apart, is entailment over two independent phrasings, not
pattern matching, and nothing in this stdlib-only stack performs it. A
blocklist of the exact wording this class of defect has used so far would
only prove that instance did not come back, and a broad negative-existential
regex over prose would be a fuzzy-proxy build gate on every future
disclosure sentence. See .planning/WINDOWS.md for the full assessment,
including the narrow presence-code candidate that was measured and refused.

Usage:
  python3 tools/check_repo.py                # live run against this repo
  python3 tools/check_repo.py --self-test     # run fixture-based self-tests
  python3 tools/check_repo.py --mutation-test # for each violation code, inject
                                               # one named defect into a copy of
                                               # this repository's real documents
                                               # and assert that code fires

Output ordering: the live run sorts violations on (code, subject) with
Python's stable sort over sorted() file iteration, so violations that
compare equal on that key keep their original insertion order.

Violation codes implemented in this file:
  dup-id            - an ID appears in more than one row of the Allocated
                      IDs table.
  range-id          - a PF ID sits outside its section's reserved range, an
                      MC ID belongs to no declared MC dimension block
                      (checked per block, not against one aggregate range
                      spanning all blocks), or a PF ID sits inside its
                      section's reserved range but outside every sub-block
                      that section's own NUMBERING.md table declares (a
                      section declaring no sub-blocks keeps exactly the
                      section-range behaviour, unchanged). Declared ceiling:
                      when a section's sub-blocks tile its whole reserved
                      range — which both PF-1 and PF-2 currently do — this
                      test adds nothing beyond the section-range test; it
                      exists so a future narrowed or gapped sub-block table
                      is enforced rather than decorative.
  revived-id        - an ID appears in both the Allocated IDs table and
                      the Deprecated IDs table.
  undefined-id      - a PF-#.# or MC-# token is cited in skills/,
                      examples/, or README.md but is absent from the
                      Allocated IDs table.
  dup-figure-key    - two rows of examples/deal-brief.md's Canonical
                      figures table share a key.
  figure-order      - the Canonical figures table's rows are not in
                      ascending key order. Ordering rule: keys are
                      compared with Python's default string ordering
                      over code points (plain `sorted()`), so two keys
                      differing only by case or by separator character
                      have a specified, reproducible position. Reports
                      the first key of the table that is not in
                      ascending order.
  unlisted-figure   - a currency amount, a percentage, or an ISO date in
                      examples/**/*.md or skills/**/*.md has no matching
                      Canonical figures row. Scan roots are examples/ and
                      skills/; evals/ is deliberately excluded because
                      Phase 5's benchmark data is not bound by the
                      Canonical figures interface. Declared ceiling (bare
                      count): this check catches currency, percentages,
                      and ISO dates only.
                      It does not catch bare counts, so a bare count
                      that drifts between examples is not detected by
                      this tool. Declared ceiling (value collision):
                      matching is by formatted value string with no binding to a canonical key,
                      so two Canonical figures rows may share one
                      formatted value, and a new fact whose formatted
                      value coincides with an unrelated canonical row's
                      value is accepted even though no row actually
                      backs that new fact. This is a limitation of this
                      tool, not a property of the data.
  pointer-missing   - a path listed in NOTICES.md under "Files required
                      to carry it" exists on disk and does not contain
                      the attribution pointer string. Declared ceiling:
                      each line of the carrier is UTF-8 decoded and
                      stripped, then compared to the canonical string
                      with Python string equality - code-point
                      equality, with no Unicode normalisation and no
                      case folding, so a visually identical line built
                      from different code points is reported as
                      missing.
  pointer-duplicated - such a path contains the attribution pointer
                      string more than once.
  pointer-unparseable - either NOTICES.md's "Attribution pointer"
                      section yields no usable pointer definition (no
                      fenced block, or an empty one), or a required
                      carrier entry is not a repository-relative path.
  license-missing   - the LICENSE file is absent from the repository
                      root, is empty, or does not begin with the string
                      "MIT License". Declared ceiling: only the first line
                      is inspected; the license body is never compared
                      against the full MIT text, so a file carrying
                      "MIT License" as its first line over a different
                      license body is accepted.
  framework-statement-missing - NOTICES.md is absent, or its
                      "Framework statements" section is missing one of the
                      three required framework subsections (Command of the
                      Message, MEDDIC/MEDDICC, or Challenger), or one of
                      those subsections is present but missing its
                      non-affiliation or trademark-rights language. The
                      check fires per-missing-framework, naming which one.
                      When NOTICES.md is absent, all three frameworks are
                      reported as missing.
  catalog-id-drift  - for each installed skill folder (a path matching
                      skills/*/SKILL.md), the PF subset of NUMBERING.md's
                      Allocated IDs, the SKILL.md's own rule-defining
                      headings, and references/checklist.md's listed PF
                      rows are not all equal. Fires once per divergent ID,
                      naming the files it is inconsistent between. A repo
                      with no path matching skills/*/SKILL.md yields no
                      violations. Declared ceiling: this check compares ID
                      sets only. It does not detect a rule whose title in
                      checklist.md disagrees with its title in
                      NUMBERING.md, nor a heading whose title text has
                      drifted from its registry row; and it reads only
                      paths one directory level below skills/, so a
                      SKILL.md placed anywhere else is not validated.
  mc-catalog-id-drift - for each installed skill folder (a path matching
                      skills/*/SKILL.md) whose references/completeness-
                      audit.md exists, the MC subset of NUMBERING.md's
                      Allocated IDs, that file's own rule-defining
                      headings, and references/checklist.md's listed MC
                      rows are not all equal. Fires once per divergent ID,
                      naming the files it is inconsistent between, via the
                      same three-way comparison catalog-id-drift uses for
                      the PF namespace. A skill folder with no
                      completeness-audit.md yields no violations for that
                      folder -- absence is not failure, matching this
                      checker's established posture. Declared ceiling:
                      this check compares ID sets only, exactly like
                      catalog-id-drift; it says nothing about whether a
                      cited MC-# token is valid, which is undefined-id's
                      job.
  mc-rule-in-skill  - a skills/*/SKILL.md defines an MC-# rule via a
                      heading matching the same shape MC rule headings use
                      in references/completeness-audit.md. AUD-02 requires
                      every MC rule to be defined in that reference file,
                      never blended into the prose catalog; this check
                      turns that requirement into a build failure. Declared
                      ceiling: this matches heading shape only -- it cannot
                      distinguish a genuine rule definition from a heading
                      that merely happens to look like one.
  frontmatter-unparseable - a skills/*/SKILL.md's frontmatter block has no
                      `---` delimited block at the file's first line, is
                      unterminated (no closing `---`), is missing one of
                      the two required keys (`name`, `description`), or
                      repeats a column-zero key. A repeated key is
                      reported rather than silently kept as a last-value-
                      wins merge — the first value is what the parser
                      keeps, but the repetition itself is the violation.
                      Declared ceiling: this parser recognises only a
                      column-zero key, a `|` block scalar, and an
                      indented nested map; a value written with any other
                      construct is read as an opaque string, never
                      individually validated.
  frontmatter-unknown-key - a skills/*/SKILL.md's frontmatter carries a
                      column-zero key outside the Agent Skills
                      specification's six-key allow-list (`name`,
                      `description`, `license`, `compatibility`,
                      `metadata`, `allowed-tools`), naming the key.
                      Declared ceiling: only the key's name is checked,
                      never the shape of its value.
  frontmatter-name-mismatch - a skills/*/SKILL.md's frontmatter `name`
                      value differs from its own parent directory name,
                      naming both. Declared ceiling: this check compares
                      `name` against the parent directory only; it does
                      not enforce the specification's own character-set
                      or length rules for `name`.
  frontmatter-description-invalid - a skills/*/SKILL.md's frontmatter
                      `description` key is present but, after whitespace
                      collapse, is empty, shorter than 200 characters, or
                      longer than 1024 characters, naming the measured
                      length and the bound it broke. A frontmatter with no
                      `description` key at all is frontmatter-unparseable's
                      missing-required-key case, not this code's -- the
                      length evaluation below only runs once the key is
                      known to be present. Declared ceiling: 200 is
                      this project's own chosen floor, not a
                      specification requirement; 1024 is the
                      specification's own ceiling, used here unchanged.
  catalog-count-unstated - a skills/*/SKILL.md contains no line matching
                      the frozen stated-count template ("This catalog
                      contains {N} rules in {M} numbered sections.").
                      Absence of the file is still not a violation.
                      Declared ceiling: the template is matched
                      byte-exactly, so a reworded but equivalent sentence
                      is reported as unstated rather than as a mismatch.
  catalog-count-mismatch - a skills/*/SKILL.md's stated rule count or
                      stated section count disagrees with the count of
                      PF rows (or distinct PF sections among them) in
                      NUMBERING.md's Allocated IDs table, naming both the
                      stated and the registry figures. Declared ceiling:
                      this check compares the two stated numbers against
                      the registry only — it does not detect a stated
                      total that is right while a rule body is missing
                      from the file entirely; that direction is
                      catalog-id-drift's.
  catalog-opening-rule-count - the Opening / Reframe section holds a
                      number of allocated PF-0 IDs other than exactly one,
                      in NUMBERING.md's Allocated IDs table or in a skill
                      folder's references/checklist.md, naming the count
                      found and the file it was found in. CAT-03 requires
                      exactly one: the Before-scenario / Identify-Pain /
                      Reframe convergence must resolve into a single
                      instruction rather than several a writer has to
                      reconcile. Declared ceiling: it counts PF-0 rows and
                      nothing else — a single row whose body states two
                      opening rules in prose passes.
  mc-count-unstated - a skill folder's references/completeness-audit.md
                      exists and contains no line matching the frozen MC
                      stated-count template ("This audit contains {N}
                      checks across {M} dimensions."). Absence of the file
                      is not a violation, matching mc-catalog-id-drift's
                      and mc-rule-in-skill's own declared posture.
                      Declared ceiling: the template is matched
                      byte-exactly, so a reworded but equivalent sentence
                      is reported as unstated rather than as a mismatch.
  mc-count-mismatch - a skill folder's references/completeness-audit.md's
                      stated check count or stated dimension count
                      disagrees with the count of MC rows (or distinct MC
                      dimension blocks among them) in NUMBERING.md's
                      Allocated IDs table, naming both the stated and the
                      registry figures. Declared ceiling: this check
                      compares the two stated numbers against the registry
                      only — it does not detect a stated total that is
                      right while a check body is missing from the file
                      entirely; that direction is mc-catalog-id-drift's.
  artifact-family-section-missing - a skill folder's
                      references/artifact-patterns.md exists and is missing
                      one of the four frozen artifact-family section
                      headings (## RFP and RFI response, ## Solution
                      proposal, ## Executive summary, ## Demo and discovery
                      material). Absence of the file is not a violation,
                      matching this checker's established posture for
                      references/completeness-audit.md. Declared ceiling:
                      this check is heading presence only — it says nothing
                      about whether a section's content is correct or
                      complete, and it does not check that each section
                      carries exactly one **Order:** line or that the
                      fourteen frozen element labels are present, both
                      enforced at plan level instead of here. Fourteen under
                      the rule 03-03-PLAN.md's own verification command
                      applies, stated here because "element label" is
                      defined in no committed file: the bold `**Label:**`
                      lines that are not **Order:** lines -- thirteen inside
                      the four family sections plus **No family fits:** in
                      the classification section. The file carries eighteen
                      bold labels in total; the other four are the
                      **Order:** lines this sentence counts separately. It
                      also emits no violation for an extra section the file
                      also contains: the classification section and the
                      closing refusal section are both legitimate and
                      neither is a family.
  skill-family-line-gate-missing - a skills/*/SKILL.md's '## Self-check
                      before delivering' section is present but its body
                      does not name both anchors MOD-04's family-line gate
                      requires: the phrase naming the artifact family, and
                      the literal 'No family fits' value spelled exactly as
                      references/artifact-patterns.md spells it. Fires once
                      per missing anchor, naming the file and which anchor
                      is missing. A SKILL.md with no self-check section at
                      all yields no violations -- the declared ceiling,
                      required so every pre-existing synthetic
                      _good_skill() fixture (none of which defines this
                      section) stays silent and the whole suite is not
                      disabled. Declared ceiling: this check asserts the
                      instruction text is present. It cannot assert a live
                      session obeys it -- that is a model-behaviour
                      property no file-reading checker observes;
                      evals/conformance/run_conformance.py is the
                      instrument for that. Its passing does not mean MOD-04
                      is mechanically verified.
  skill-family-order-gate-missing - a skills/*/SKILL.md's '## Self-check
                      before delivering' section is present but its body
                      does not name both anchors the ordering gate
                      requires: the literal 're-scan' and the literal
                      'before any rule marker', matched
                      case-insensitively. This is the sibling of
                      skill-family-line-gate-missing, extended from
                      presence of the family line to its position ahead
                      of any rule marker -- the residual failure mode
                      03-08 measured (rule-before-family). Fires once per
                      missing anchor, naming the file and which anchor is
                      missing. A SKILL.md with no self-check section at
                      all yields no violations -- the same declared
                      ceiling its sibling uses, required so every
                      pre-existing synthetic _good_skill() fixture stays
                      silent. Declared ceiling: this check asserts the
                      instruction text is present. It cannot assert a
                      live session obeys it -- that is a model-behaviour
                      property no file-reading checker observes;
                      evals/conformance/run_conformance.py is the
                      instrument for that. Its passing does not mean
                      MOD-04 is mechanically verified.
  source-label-in-skill-content - a file matching SKILL_GLOB, or a
                      references/*.md beside it, contains a frozen
                      source-coined dimension label from
                      SOURCE_COINED_LABELS used as this repository's own
                      unattributed noun. Fires once per file-and-label
                      pair, naming the file, the label, and the first line
                      number it occurs on. Three declared ceilings: (1)
                      this is a literal-string scan over a closed,
                      enumerated list, not the semantic paraphrase
                      judgement SOURCES.md states no tool in this stack
                      performs -- it catches a known label returning, and a
                      novel one has no string to match; (2) the
                      ordinary-English word for a measurement is
                      deliberately excluded from the list, because this
                      repository's own MC-1 and integrity rules use it as
                      ordinary business English, and including it would
                      fire on legitimate content; (3) it scans shipped
                      skill content only -- NUMBERING.md's frozen registry
                      labels are out of scope, owned by .planning/
                      WINDOWS.md entry 6 and routed to Phase 6 LEG-04.
  skill-too-long    - a skills/*/SKILL.md exceeds 500 lines, naming the
                      measured count and the ceiling. Silent at exactly
                      500. Declared ceiling: line count is a proxy for
                      the Agent Skills specification's approximate
                      5,000-token progressive-disclosure budget; a file
                      under 500 lines with unusually long lines can still
                      exceed that token budget, which this check cannot
                      detect on its own — skill-token-budget-exceeded is
                      the companion check for that direction.
  skill-token-budget-exceeded - a skills/*/SKILL.md's estimated token
                      count exceeds 5,000, the Agent Skills
                      specification's own approximate ceiling behind
                      CAT-08 ("under 500 lines, approximately 5,000
                      tokens"). No tokenizer is available to a standard-
                      library-only checker, so this check estimates
                      tokens as word_count * 1.3 — a word-to-token ratio
                      calibrated against this project's own sibling
                      skill (`simple-english/SKILL.md`), which
                      02-RESEARCH.md measured at 3,664 words and recorded
                      as comfortably under the same ~5,000-token ceiling;
                      3,664 * 1.3 ≈ 4,763, consistent with that recorded
                      finding. Declared ceiling: this is a word-count
                      proxy, not a real tokenizer; it counts words across
                      the whole file including its frontmatter block, not
                      the post-frontmatter body alone; and a different
                      estimator (for example characters / 4) gives a
                      materially different figure for the same file —
                      this check uses one stated estimator consistently,
                      never the more favourable of several. This check
                      previously fired against this repository's own
                      skills/proof-first/SKILL.md before the 02-07/02-08
                      trim (see .planning/WINDOWS.md entry 5, status:
                      fixed); it is silent against the current tree.
  readme-results-pointer-missing - README.md does not contain the literal
                      path 'evals/conformance/RESULTS-mod04.md'. This is a
                      repository-level documentation check, not a catalog
                      check -- it does not depend on NUMBERING.md or on any
                      skills/*/SKILL.md path. Declared ceiling: this check
                      asserts one literal path string is present in
                      README.md. It does not assert that the file at that
                      path exists, that the figures in it are current, or
                      that the prose around the pointer is accurate -- a
                      human read is the only thing that establishes the
                      last of those; this check only makes the measurement
                      discoverable and makes its silent disappearance from
                      README a gate failure, nothing more.
  results-breakdown-count-mismatch - a verdict-breakdown bullet in
                      evals/conformance/RESULTS-mod04.md
                      (RESULTS_BREAKDOWN_PATH) states a count that
                      disagrees with its own parenthetical enumeration, or
                      states a count above zero with no enumeration at
                      all. One code covers both triggers, rather than the
                      unstated/mismatch code pair the PF and MC catalog
                      counts use (catalog-count-unstated/-mismatch,
                      mc-count-unstated/-mismatch), because both triggers
                      here are the same defect -- an itemization a reader
                      cannot re-derive -- against a free-prose file, not
                      two distinct authoring errors against a frozen
                      sentence template. Counts a parenthetical item
                      carrying a standalone 'xN' multiplier as N and any
                      other comma-separated item as one; two items naming
                      the same fixture are never merged, and the sum does
                      not depend on item order. Silent when the file does
                      not exist. Declared ceiling: this check asserts
                      internal consistency between a stated count and its
                      own enumeration. It asserts nothing about whether
                      the measurement is correct, current, or
                      well-designed; an enumeration written in a different
                      grammar (a range, a prose 'and two more') will not
                      be counted the way its author intended; and it reads
                      one named path, not every results file that might
                      ever exist.
  source-row-unconfirmed - a row in one of SOURCES.md's three source
                      tables is marked `verified` while its Where cell
                      carries no absolute https:// URL, no
                      `(retrieved YYYY-MM-DD)` date that parses as a real
                      calendar date, or neither. Also fires on a row whose
                      cell count is not the five those tables declare,
                      naming the parse failure rather than skipping the
                      row silently. Rows marked `unverified` are out of
                      scope in every case: an unverified row makes no
                      provenance claim, so there is nothing yet to check.
                      Status is compared case-sensitively, consistent with
                      this module's no-case-folding discipline for the
                      attribution pointer. Silent when SOURCES.md does not
                      exist. Declared ceiling (no fetch): this check does
                      not fetch the recorded URL. A URL that has rotted,
                      moved, or never resolved reads identical here to a
                      live one -- the lookup happens once, by hand, when
                      the row is confirmed, and CI reads only the
                      committed record. A build that fails because a third
                      party had an outage is not a build failure worth
                      having, so do not "improve" this check by adding a
                      network call. Declared ceiling (no semantics): it
                      does not judge whether the source at that URL says
                      what the row claims. That is the same semantic
                      judgement SOURCES.md's own "What counts as
                      reproduction" section states no tool in this stack
                      performs, and this check is not the exception.
  readme-claim-unsourced - a numeric token inside README.md's claim
                      region (delimited by the frozen
                      `<!-- claim-region:start -->` / `<!-- claim-region:end -->`
                      pair) appears in no file matching
                      evals/*/RESULTS*.md; also fires once when those
                      markers are unbalanced or reversed, because an
                      unbounded region is not an empty one and reading it
                      as empty would make deleting the end marker a way
                      around the check. The region is bounded because
                      README legitimately carries numbers that are not
                      measured claims. Silent when README carries neither
                      marker, and when README.md does not exist. Declared
                      ceiling: matching is substring containment over the
                      concatenated corpus, so `48` is sourced by any file
                      containing `1948`. This catches a number invented out
                      of nothing; it does not prove provenance to the
                      digit.
  readme-claim-unanchored - a claim-region paragraph containing a numeric
                      token carries no exact model version from
                      CLAIM_MODEL_STRINGS, or no ISO-8601 date, or
                      neither. Paragraphs are split on blank lines, so the
                      anchor has to travel with the figure rather than
                      sitting once at the top of a section. Fires once per
                      offending paragraph, naming its first line. Silent
                      with no claim region, with no README.md, and on the
                      unbalanced-marker condition, which
                      readme-claim-unsourced reports alone so one broken
                      region is one violation. Declared ceiling: this
                      asserts a model string and a date are PRESENT in the
                      paragraph. It cannot assert they are the model and
                      date that produced that paragraph's number.
  readme-badge-unlisted - README.md carries a Markdown image whose URL
                      contains `badge` or `shields.io`, or ends `.svg`,
                      and matches no entry in the frozen BADGE_ALLOW_LIST.
                      The allow-list admits build status and license only:
                      a CI badge reports that ten offline commands exited
                      zero and a license badge states what LICENSE already
                      states, so neither carries a measured product claim.
                      Fires once per offending image, naming its URL.
                      Silent when README.md does not exist. Declared
                      ceiling: this reads Markdown image syntax only, so a
                      badge embedded as a raw HTML `<img>` tag is invisible
                      to it.
  readme-layout-tree-stale - an immediate subdirectory of evals/ exists on
                      disk and its name does not appear in README.md's
                      `## Repository layout` section. Closes the gap
                      readme-layout-legend-drift's own docstring declares
                      it does not cover -- whether the tree matches the
                      filesystem. Scoped to evals/ because that is where
                      this repository adds families, and to one level
                      because a full tree diff would fire on __pycache__
                      and on every future fixture directory; __pycache__
                      and dot-prefixed names are skipped. Fires once per
                      missing directory. Silent when README.md or evals/
                      does not exist. Declared ceiling: it checks that the
                      name appears somewhere in the section, not that the
                      entry is correctly placed, that its children are
                      listed, or that every path the tree names still
                      exists.
  source-gate-incomplete - LEGAL-REVIEW.md declares the frozen line
                      `Gate status: PASSED` while at least one SOURCES.md
                      row still reads `unverified`; also fires when
                      LEGAL-REVIEW.md exists and carries no readable
                      `Gate status:` line, or more than one, since an
                      unreadable gate is neither a passed gate nor a silent
                      one. The marker is compared byte for byte after
                      stripping leading and trailing whitespace, with no
                      case folding -- the attribution pointer's equality
                      discipline, for the same reason. Silent when
                      LEGAL-REVIEW.md does not exist, so a repository that
                      has not yet run a review is not retroactively in
                      violation. Declared ceiling (no fetch): no network
                      call; it reads two committed files. Declared ceiling
                      (frozen literal, not prose): a review record that
                      describes a pass in prose without that exact line is
                      not detected -- the marker is frozen rather than
                      fuzzy-matched on purpose, because a fuzzy match over
                      prose is the fuzzy-proxy build gate
                      .planning/WINDOWS.md id 17 records this repository
                      measuring and refusing. Declared ceiling (no
                      semantics): it does not judge whether the review
                      behind a declared pass was any good, only whether the
                      list it declares a pass over is complete.
  framework-statement-stale-review - a NOTICES.md framework statement
                      carries no `Last reviewed:` line, one that does not
                      parse as ISO-8601, or one whose date precedes
                      LEGAL-REVIEW.md's `Review date:`. Fires once per
                      offending statement with the framework name as its
                      subject, so two stale statements are two
                      distinguishable rows under the (code, subject) sort.
                      A date on or after the review date is silent -- later
                      is fine, earlier is the defect. Silent when
                      LEGAL-REVIEW.md is absent or carries no parseable
                      review date, because there is nothing to compare
                      against and inventing a comparison would make the
                      code fire for a reason it cannot name; silent when
                      NOTICES.md is absent, because
                      framework-statement-missing owns that condition.
                      Declared ceiling (no fetch): no network call.
                      Declared ceiling (date, not truth): it does not judge
                      whether a statement is correct, only whether it
                      carries a date consistent with the review claiming to
                      have produced it -- a thoroughly wrong statement
                      re-dated today passes. Declared ceiling (coverage):
                      it reads the `Last reviewed:` line only; the
                      `Paraphrase boundary:` element stays unchecked by any
                      code in this module.
  plugin-manifest-version-mismatch - a .claude-plugin/plugin.json or
                      .claude-plugin/marketplace.json states a `version`
                      that disagrees with skills/*/SKILL.md's frontmatter
                      `metadata.version`, or either manifest exists while no
                      skill states a version to compare against, or two or
                      more shipped skills each state a metadata.version and
                      those versions disagree with each other. Fires once
                      per disagreeing manifest, naming both values, and
                      once naming every disagreeing skill and its version
                      when the skills themselves disagree. Absence of both
                      manifests is not a violation. Declared ceiling: the
                      manifest comparison resolves its single comparison
                      value from the alphabetically first skill that states
                      a version -- unchanged and exact when exactly one
                      skill states one, the live case; in a multi-skill
                      repository a manifest could still agree with that one
                      skill and disagree with another with no manifest-
                      level violation naming that specific disagreement --
                      the skills' mutual disagreement is what fires
                      instead. It says nothing about whether the version is
                      semantically correct, whether a git tag exists for
                      it, or whether the manifest installs.
  plugin-manifest-invalid - a .claude-plugin/plugin.json or
                      .claude-plugin/marketplace.json is not valid JSON, is
                      missing a required key at either of the two positions
                      PLUGIN_REQUIRED_KEYS is enforced against --
                      plugin.json's top-level object and marketplace.json's
                      plugins[0] entry, the object `claude plugin
                      marketplace add` actually reads -- or, once both
                      objects parse, one of MARKETPLACE_ENTRY_EQUAL_KEYS
                      (description, displayName, author, license, keywords)
                      disagrees between them, or plugin.json's `name`
                      differs from the one shipped skills/*/ folder name,
                      or marketplace.json's `owner` has no non-empty
                      `name`, or its `plugins` array is not exactly one
                      object, or that object's `source` is not the literal
                      `./`. Also fires when plugin.json states a `name` and
                      the repository ships anything other than exactly one
                      skills/*/ folder, naming how many were found -- zero
                      and multiple are worded differently, since zero means
                      the manifest names a skill that is not there and
                      multiple means it names one of several without saying
                      which. Absence of both manifests is not a violation.
                      Declared ceiling: it asserts JSON well-formedness, key
                      presence at both positions, the five-field equality,
                      and the folder-name equality only, and the
                      folder-name equality is verified (not merely
                      not-skipped) only in the one-skill case -- the
                      multi-skill and zero-skill cases are reported as
                      unverifiable rather than resolved. `name`, `version`,
                      `homepage` and `repository` are deliberately excluded
                      from MARKETPLACE_ENTRY_EQUAL_KEYS -- `name` and
                      `version` are separately owned by this same check's
                      folder-name assertion and by
                      plugin-manifest-version-mismatch respectively, and
                      `homepage`/`repository` are owned by
                      publish-location-drift at owner-segment granularity,
                      which permits the two manifests to write the same
                      publish location in four different GitHub URL
                      syntaxes -- an exact-string check on those two fields
                      would contradict that. It never validates a value's
                      semantics beyond presence and equality, never reaches
                      the network, and says nothing about whether a real
                      `claude plugin marketplace add` succeeds -- that is a
                      manual smoke test recorded in 04-VALIDATION.md.
  before-after-family-missing - examples/before-after.md, if it exists,
                      is missing one of the four frozen ARTIFACT_FAMILY_
                      SECTIONS headings; or a present heading's section
                      body carries no line beginning with ✗, or no line
                      beginning with ✓; or, only once all four headings
                      are present, they appear in an order other than
                      ARTIFACT_FAMILY_SECTIONS' own order. Absence of the
                      file is not a violation. Declared ceiling: this is
                      heading presence, ✗/✓ line presence, and order
                      only. It says nothing about whether a pair's before
                      half is genuinely non-compliant, whether its after
                      half is genuinely a rewrite rather than a
                      restatement of the rule's own wording, or whether
                      the rewrite obeys its family's stated ordering
                      convention -- those are semantic judgements this
                      repository's stack does not perform, and they stay
                      with end-of-phase UAT.
  before-after-citation-missing - examples/before-after.md, if it exists,
                      has a present ARTIFACT_FAMILY_SECTIONS heading whose
                      section body carries no PF-#.# or MC-# token.
                      Absence of the file is not a violation. Declared
                      ceiling: it asserts that a citation exists somewhere
                      in the section, not that the citation is textually
                      adjacent to the sentence it justifies, nor that the
                      cited rule is the correct one for that rewrite.
                      Validity of the token itself is undefined-id's job;
                      this check asserts presence only.
  example-sentence-length - a ✓ column line in either file named by
                      EXAMPLE_PROSE_PATHS (examples/before-after.md or
                      skills/proof-first/references/worked-examples.md)
                      carries a sentence over PF41_WORD_CEILING (25)
                      words, PF-4.1's own stated ceiling, counted as
                      words delimited by whitespace after bracketed
                      marker spans are removed -- one stated definition,
                      not an implied one. Fires once per over-ceiling
                      sentence, naming the file, the measured word
                      count, the ceiling, and the sentence's opening
                      words. Absence of a path is not a violation,
                      checked before any read. Declared ceiling: only
                      lines beginning with the check character are
                      inspected -- a ✗ column is the deliberately
                      non-compliant exhibit its pair exists to contrast
                      against, and holding it to the rule would delete
                      the contrast; bracketed marker spans are removed
                      before counting, so a long marker never forces a
                      split; sentence boundaries are a period, question
                      mark, or exclamation mark followed by whitespace,
                      so an abbreviation carrying an internal period
                      splits a sentence early and undercounts; and this
                      check enforces PF-4.1 alone, saying nothing about
                      PF-4.2's active voice, PF-4.3's modal discipline,
                      or any other prose-mechanics rule.
  before-after-spelled-count - a ✗ or ✓ column line in
                      examples/before-after.md names a word-spelled
                      cardinal from two through twelve (SPELLED_CARDINAL_RE;
                      one is deliberately excluded -- English uses it as
                      an article far more often than as a count), unless
                      the matched word and the whitespace-delimited word
                      immediately after it both begin with an uppercase
                      letter, a two-token proper-noun heuristic that
                      exempts a party name containing a number word.
                      Fires once per surviving match, naming the matched
                      word and the line's opening words. Absence of the
                      file is not a violation, checked before any read.
                      Rationale: unlisted-figure inspects digit-shaped
                      tokens only, so a count written as a word is
                      structurally invisible to the Canonical figures
                      interface; requiring a count in this file's quoted
                      columns to be written in digits routes every count
                      through that interface instead of around it. This
                      is the word-spelled half of the bare-count hole
                      unlisted-figure's own declared ceiling discloses;
                      the digit half remains open and is named as still
                      open. Declared ceiling: the scan is this one
                      file's quoted lines only. examples/deal-brief.md
                      is out of scope because the brief is the
                      definition of what counts as invented, and a count
                      it states is by construction not invented. Its
                      prose carries spelled cardinals throughout,
                      including a party name containing a number word,
                      and none of them sits on a ✗ or ✓ line -- this
                      check opens no file but examples/before-after.md.
                      skills/** is out of scope because the same party
                      name appears there and because a per-rule
                      illustrative pair reads naturally with a spelled
                      count -- 5 matches sit on ✗ or ✓ lines across
                      those files. A raw scan of their whole text finds
                      far more, in ordinary prose this check never
                      reads; the 5 is the mark-line count, which is the
                      only one this scope decision turns on.
                      One of them ("Nine", in the party name "Vantage
                      Nine Consulting") is a proper noun the check's own
                      two-token exemption would excuse even if the check
                      applied to that path, leaving 4 would-be
                      violations. The proper-noun heuristic is two
                      tokens wide and will therefore also exempt a
                      cardinal that happens to end a sentence
                      immediately before a capitalised sentence start.
  example-rule-narration - a ✓ column line in either file named by
                      EXAMPLE_PROSE_PATHS pairs a listed contrastive
                      connective (NARRATION_CONNECTIVE_RE: "rather
                      than", ", not", or "instead of") with one of ten
                      listed meta terms (NARRATION_META_TERMS) naming
                      the catalog's own vocabulary for a rule's
                      rejected alternative, within
                      NARRATION_WINDOW_CHARS (60) characters of the
                      connective. Fires at most once per line, naming
                      the connective and the meta term matched.
                      Absence of a path is not a violation, checked
                      before any read. This is an explicitly disclosed
                      proxy for SKILL.md line 261's "No list of applied
                      rules follows the prose", never a verdict on it
                      -- the verdict stays with end-of-phase UAT.
                      Declared ceiling: it catches one narration shape
                      only. It does not detect narration phrased as
                      self-reference to the document's own ordering --
                      a sentence announcing that the answer stands
                      first rather than simply placing it first carries
                      no listed connective and is invisible here; that
                      instance was found by an adversarial
                      human-substitute read, was repaired by hand, and
                      remains a semantic judgement no code in this
                      repository performs. It does not detect novel
                      narration built from words absent from the
                      frozen term list. It will report a legitimate
                      technical contrast that happens to pair a listed
                      connective with a listed term, and the repair in
                      that case is to reword the example rather than to
                      widen the list. Measured 2026-09-17: 4 of 4 ✓
                      columns in examples/before-after.md matched
                      before the 04-05 repair, and 0 of 28 in
                      worked-examples.md.
  publish-location-drift - the GitHub owner segment stated by this
                      repository's own carriers of its publish location
                      (plugin.json's and marketplace.json's `homepage`,
                      `repository`, and `owner.url` fields; README.md's
                      `npx skills add`, `claude plugin marketplace add`
                      and in-session `/plugin marketplace add` command
                      arguments) disagree, or a manifest carrier
                      exists and states none at all while another existing
                      carrier states one. Each value is normalised across
                      four GitHub URL forms before comparison -- HTTPS,
                      plaintext HTTP, scheme-less, and the SSH remote form
                      `git remote -v` prints -- so two carriers naming the
                      same owner in different syntaxes agree rather than
                      falsely disagreeing. A carrier yielding no match at
                      all (README.md before any install command is
                      written) is silently skipped, not treated as
                      disagreeing. Declared ceiling: it asserts every
                      existing carrier states the same GitHub account/org
                      segment, once normalised. It does not recognise a
                      GitHub Enterprise or other self-hosted host; it does
                      not assert the location is correct, that it
                      resolves, or that the repository is published there;
                      it also compares owner segments only, so a
                      repository-name-only drift under an unchanged owner
                      is not detected. See .planning/WINDOWS.md for the
                      open placeholder item.
  skill-derivative-stale - output-styles/proof-first.md or
                      prompts/system-prompt.md, if present, carries a
                      stamp -- the file's first line matching the frozen
                      generated-by pattern -- recording a sha256 digest
                      and a source-path list. Fires when a present
                      derivative carries no such stamp; when its recorded
                      source-path list differs from this checker's own
                      frozen DERIVATIVE_SOURCE_NAMES tuple; or when a
                      fresh hash of DERIVATIVE_SOURCE_NAMES no longer
                      equals the recorded digest, which is what happens
                      after skills/proof-first/SKILL.md or a named
                      reference file is edited and
                      tools/generate_derivatives.py is not re-run.
                      Absence of both derivatives is not a violation,
                      checked before any read. Declared ceiling: the
                      recorded hash proves a derivative was produced from
                      some version of the named sources, not that the
                      generator's own derivation logic is correct -- a
                      bug there that dropped a rule would still produce a
                      matching hash. It proves structural freshness only
                      and says nothing about a live session's conduct. A
                      hand-edit to a derivative's body after generation
                      leaves the recorded hash valid, which is exactly
                      why `python3 tools/generate_derivatives.py --check`
                      runs in CI as a second, independent guard.
  derivative-rule-coverage-incomplete - output-styles/proof-first.md or
                      prompts/system-prompt.md, if present, is missing a
                      '### <ID> -- ' rule heading for one of
                      NUMBERING.md's allocated PF- or MC- IDs, or is
                      missing one of the four frozen
                      ARTIFACT_FAMILY_SECTIONS headings. Absence of both
                      derivatives, or absence of NUMBERING.md, is not a
                      violation. Declared ceiling: this proves every
                      shipped rule heading and every artifact-family
                      heading reaches each derivative -- a structural
                      statement about content presence. It proves nothing
                      about what a model does with that content, nothing
                      about whether a session driven by a derivative
                      reaches the same conclusions as one with the skill
                      folder installed, and nothing about whether the
                      omitted illustration file's absence changes
                      anything. Phase 5's benchmark is the only place
                      such a statement could ever be sourced from; until
                      then this repository makes no such claim.
  readme-install-path-missing - README.md is missing one of
                      README_INSTALL_ANCHORS' four route anchors: the
                      skills-CLI command prefix (SKILLS_CLI_INSTALL_RE),
                      the marketplace add command prefix
                      (MARKETPLACE_ADD_RE), or the literal
                      output-styles/proof-first.md or
                      prompts/system-prompt.md path. Reads README.md's raw
                      text, never strip_fences -- every anchor lives
                      inside a fenced command block, and stripping fences
                      would find none of them. Fires once per missing
                      anchor. Absence of README.md is not a violation,
                      checked before any read. Declared ceiling: this
                      check asserts each route's identifying text appears
                      somewhere in the file. It does not assert the
                      command is correct, that it resolves, that its
                      argument names a real repository, or that the four
                      routes appear under the '## Install' heading rather
                      than scattered elsewhere -- publish-location-drift
                      owns the argument's consistency, and nothing owns
                      the command's correctness until the repository is
                      published.
  readme-before-after-order - README.md is missing one of
                      README_BEFORE_AFTER_HEADING, README_INSTALL_HEADING,
                      or README_STATUS_HEADING (the '## Before and
                      after', '## Install', and '## Status' headings), or
                      -- only once all three are present -- the before/
                      after heading does not precede both the install and
                      the status heading. Fires once per missing heading,
                      and once naming the order found and the order
                      required when all three are present but out of
                      order. Absence of README.md is not a violation,
                      checked before any read. Declared ceiling: this
                      check asserts heading presence and relative
                      position only. It says nothing about whether the
                      '## Before and after' section actually contains a
                      pair, whether the pair is any good, or whether a
                      reader experiences the file as leading with
                      examples -- the first of those is
                      before-after-family-missing's job over a different
                      file, and the last two are manual judgments left to
                      end-of-phase UAT.
  readme-example-drift - a line of README.md beginning with the
                      ballot-cross character, the check character, or
                      the applied-rules footer prefix (README_CROSS_CHAR,
                      README_CHECK_CHAR, README_APPLIED_RULES_PREFIX) is
                      not, character for character, a line of
                      examples/before-after.md (BEFORE_AFTER_PATH).
                      Returns no violation before any read when either
                      README.md or BEFORE_AFTER_PATH does not exist --
                      both files are required for the comparison to mean
                      anything. Fires once per unmatched README line,
                      naming the line number and the line's opening
                      words. Declared ceiling: comparison is whole-line
                      code-point equality with no Unicode normalisation,
                      no case folding and no whitespace collapsing -- the
                      same convention pointer-missing already states, so
                      a reproduction differing only in an invisible code
                      point is reported as drift, which is the intended
                      direction. It asserts membership, not position or
                      completeness: README may reproduce one pair, four
                      pairs, or none at all, and may reproduce a check
                      line without its ballot-cross line. It says
                      nothing about the surrounding prose, the family
                      label, or the link line. And it asserts nothing in
                      the opposite direction: a line present in
                      examples/before-after.md and absent from README is
                      not a violation, because README is a lead-in and
                      is not required to reproduce everything.
  readme-example-lead-distance - README.md carries no line beginning
                      with the ballot-cross character at all, or its
                      first such line sits past
                      README_FIRST_EXAMPLE_MAX_LINE (20), a frozen
                      ceiling with deliberate margin over the measured
                      pre-repair value of 23. Returns no violation
                      before any read when README.md does not exist.
                      Fires once, naming which of the two conditions
                      applied. Declared ceiling: line numbers are
                      counted as physical lines from the top of the raw
                      file, so one long paragraph written as a single
                      physical line counts once while the same prose
                      hard-wrapped counts many times -- a stated
                      definition, not an implied one, and the reason the
                      ceiling carries margin. It asserts the example
                      arrives early, never that the example is good,
                      that the prose above it is necessary, or that the
                      pair below it is complete -- readme-example-drift
                      owns the reproduction's fidelity and
                      readme-before-after-order owns the section
                      ordering. It reads only the ballot-cross
                      character, so a README leading with a check line
                      and no ballot-cross line is reported as having no
                      example, which is intended: the contrast is the
                      point.
  readme-layout-legend-drift - README.md's '## Repository layout'
                      section, if present, carries a legend-prose marker
                      (a short lowercase word or hyphenated phrase inside
                      double quotes) the fenced tree never uses in
                      parentheses, or a tree marker the legend prose
                      never mentions. Returns no violation before any
                      read when README.md does not exist, and when the
                      layout heading itself is absent -- a README with
                      no layout section is silent, not violating,
                      matching publish-location-drift's stated decision
                      that a carrier with nothing to say is silent.
                      Fires once per mismatched marker, naming the
                      marker and which direction the mismatch runs.
                      Declared ceiling: it compares marker vocabulary
                      only. It says nothing about whether a marker is
                      applied to the right entries, whether the tree
                      matches the filesystem, whether the legend's
                      explanation of a marker is accurate, or whether an
                      entry that carries no marker should. Its marker
                      shape is a short lowercase token inside double
                      quotes in prose and inside parentheses in the
                      tree, bounded to at most 20 characters each; a
                      marker written in any other shape -- bracketed,
                      uppercase, or longer than the stated bound -- is
                      invisible to this check. And it reads only the
                      layout section, so a marker vocabulary introduced
                      elsewhere in README is out of scope.
  readme-output-style-destination-missing - README.md names
                      README_OUTPUT_STYLE_PATH as the output-style
                      install route but names neither directory Claude
                      Code scans for output styles
                      (README_OUTPUT_STYLE_DESTINATIONS: the user-level
                      '~/.claude/output-styles/' or the project-level
                      '.claude/output-styles/'). Returns no violation
                      before any read when README.md does not exist,
                      and returns no violation when README never names
                      README_OUTPUT_STYLE_PATH at all -- a README
                      stating no output-style route has nothing for
                      this code to say. Fires once. Declared ceiling:
                      this check asserts the README tells a reader
                      which directory the output-style file has to
                      reach. It asserts nothing about whether the copy
                      succeeds, whether Claude Code lists or applies
                      the style, whether the stated command is correct,
                      or whether any other route is executable --
                      readme-install-path-missing owns anchor presence
                      and nothing in this repository owns route
                      executability. The comparison is literal
                      substring containment with no path expansion and
                      no filesystem access, so a README naming the
                      directory in a different notation is invisible to
                      it.
  derivative-comparison-claim-stale - the generated derivatives
                      (DERIVATIVE_PATHS) make a factual claim about
                      whether any benchmark has compared a session
                      driven by a derivative against a session with the
                      skill folder installed. Fires when
                      ROUTES_RESULTS_PATH exists in the tree -- that is,
                      when such a comparison IS committed -- and a
                      present derivative still carries the literal
                      STALE_COMPARISON_CLAIM asserting that none has.
                      One violation per offending derivative, naming the
                      file, the literal and the results path that
                      contradicts it. Returns no violation before any
                      read when ROUTES_RESULTS_PATH does not exist: with
                      no comparison committed, the derivatives' claim is
                      true and this code has nothing to say. Declared
                      ceiling: this is a two-sided literal-substring
                      presence conjunction and nothing more. It does not
                      read ROUTES_RESULTS_PATH's contents, does not
                      check that the replacement sentence is accurate,
                      does not check that the derivatives point at the
                      results file, and cannot see the same false claim
                      restated in different words. It closes exactly one
                      regression path: a regeneration or a revert
                      putting the known stale sentence back while the
                      measurement that falsifies it sits in the tree.
  benchmark-run-claim-stale - the same regression, one literal over.
                      Fires when BENCHMARK_RESULTS_PATH exists in the
                      tree -- that is, when a benchmark HAS run -- and a
                      file in BENCHMARK_CLAIM_PATHS still carries the
                      literal STALE_BENCHMARK_RUN_CLAIM. One violation
                      per offending file. Scans the generated
                      derivatives AND the skill sources they are
                      generated from, because this sentence originated
                      in a source and a derivative-only scan stays
                      silent until the next regeneration. Matches
                      case-insensitively, unlike its sibling, because
                      the sentence is hand-written prose rather than
                      generator output and can plausibly return
                      capitalised. Returns no violation before any read
                      when BENCHMARK_RESULTS_PATH does not exist: with
                      no benchmark committed the sentence is true.
                      Declared ceiling: literal-substring presence and
                      nothing more -- it does not read the results
                      file's contents, does not judge whether the
                      replacement sentence is accurate, and cannot see
                      the same false claim restated in other words.
  record-citation-unresolvable - a `path`:N or `path`:N-M citation in one
                      of CITATION_RECORD_PATHS does not resolve: the path
                      names no file in the tree, or the cited line range
                      runs past the end of the file it names, or the range
                      is inverted. One violation per distinct citation,
                      naming the record, the cited spelling and what was
                      wrong. Added by 06-08 against a measured pattern:
                      four rounds of cold reads on this repository kept
                      producing citation-drift findings, every one of them
                      a line number that was right when written and wrong
                      after the cited file was edited -- usually by the
                      round that wrote the citation. Declared
                      ceiling, and it is narrower than it looks: this
                      checks that a citation RESOLVES, not that the cited
                      lines say what the citing sentence claims. Measured,
                      not asserted: replayed over this repository's full
                      history as measured at 06-08 -- 435 commits then, 164
                      citation-instances, 14 distinct spellings, 37 commits
                      carrying at least one -- this code fired ZERO times.
                      The figures are pinned to that measurement, not
                      restated as a live count: 06-08's own commits moved
                      three of the four (only the 14 distinct spellings
                      held), which is the defect class this file keeps
                      recording. Every citation finding four rounds of
                      cold reads produced was a line number that existed
                      and pointed at the wrong content, including the
                      SKILL.md:63 misquote and the NUMBERING.md:26-40
                      slip. This code catches none of them. It is future insurance against three shapes
                      that have not yet occurred here -- a path that names
                      no file, a range past end-of-file, an inverted range
                      -- and it must not be cited as a guard over citation
                      accuracy, which remains a human read. It also stays
                      silent on a retired citation quoted inside a
                      correction paragraph, which still resolves, and on
                      anything inside a fenced block -- it reads
                      strip_fences() output, so a fence that illustrates the
                      `path`:N format is documentation rather than a
                      citation. Corrected 06-09: this said "like every other
                      content-scanning code here", which is false in the
                      majority direction -- of this file's 51 check_*
                      functions, 15 call strip_fences and 36 do not, several
                      of them saying so in their own docstrings. The
                      sentence needs no comparison and now makes none.
                      Second ceiling: a bare basename is resolved by
                      searching the tree, so a citation naming a file
                      that is not in this repository fires as unresolvable.
                      Neither record makes such a citation; if one ever
                      needs to, it must not use the `path`:N form. Third:
                      where a basename matches more than one file the check
                      fires only if the range overruns EVERY candidate,
                      since it cannot tell which was meant.
"""
import argparse
import datetime
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

PF_ID_RE = re.compile(r'^PF-(\d+)\.(\d+)$')
MC_ID_RE = re.compile(r'^MC-(\d+)$')
FENCE_RE = re.compile(r'```.*?```', re.S)

POINTER_SECTION = 'Attribution pointer'
CARRIERS_MARKER = 'Files required to carry it'

SKILL_GLOB = 'skills/*/SKILL.md'

PLUGIN_MANIFEST_PATH = '.claude-plugin/plugin.json'
MARKETPLACE_MANIFEST_PATH = '.claude-plugin/marketplace.json'

BEFORE_AFTER_PATH = 'examples/before-after.md'

# The repository's two example-prose files, both of which carry ✗/✓ quoted
# columns (Phase 4, 04-07). The first element is composed from
# BEFORE_AFTER_PATH rather than a second copy of the same literal.
EXAMPLE_PROSE_PATHS = (
    BEFORE_AFTER_PATH,
    'skills/proof-first/references/worked-examples.md',
)

# PF-4.1's own stated ceiling ("No sentence runs longer than 25 words").
# This value must track that rule's own text -- changing it here without
# changing the rule would put the checker and the catalog into disagreement.
PF41_WORD_CEILING = 25

MARKER_SPAN_RE = re.compile(r'\[[^\]]*\]')
SENTENCE_SPLIT_RE = re.compile(r'(?<=[.?!])\s+')

# Word-spelled cardinals two through twelve, case-insensitively. 'one' is
# deliberately excluded: English uses it as an article far more often than
# as a count, and including it would fire on ordinary prose such as
# "one folder" or "one shared brief".
SPELLED_CARDINAL_RE = re.compile(
    r'\b(two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b', re.I)

# Three contrastive connectives naming a rejected alternative: the two-word
# form meaning "in preference to", the comma-plus-negation form, and the
# two-word form meaning "in place of".
NARRATION_CONNECTIVE_RE = re.compile(r'rather than|,\s*not\b|instead of', re.I)

# An explicitly-labelled proxy list belonging to this checker only, never
# to the rule catalog itself -- the catalog's own vocabulary for the
# alternative a rule rejects. The deletion test remains the standard;
# this list is a regex proxy for one narrow narration shape, not a
# restatement of it.
NARRATION_META_TERMS = (
    'asserted', 'a claim', 'a capability list', 'a generic strength',
    'a standard product tour', 'a feature list', 'a paraphrase',
    'an assertion', 'boilerplate', 'marketing',
)

# Window width, in characters, within which a meta term must follow a
# connective for the pair to count as narration.
NARRATION_WINDOW_CHARS = 60


def strip_fences(text):
    return FENCE_RE.sub('', text)


def split_sections(text):
    """Split a Markdown document into {heading: body} by '## ' headings."""
    sections = {}
    current = None
    buf = []
    for line in text.splitlines():
        m = re.match(r'^## (.+?)\s*$', line)
        if m:
            if current is not None:
                sections[current] = '\n'.join(buf)
            current = m.group(1).strip()
            buf = []
        else:
            if current is not None:
                buf.append(line)
    if current is not None:
        sections[current] = '\n'.join(buf)
    return sections


def table_rows(section_text):
    """Return data rows (list of stripped cells) from the first Markdown
    table found in section_text, skipping the header and separator rows."""
    rows = []
    lines = [l for l in section_text.splitlines() if l.strip().startswith('|')]
    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if i == 0:
            continue  # header row
        if all(re.fullmatch(r':?-{1,}:?', c) for c in cells):
            continue  # separator row
        rows.append(cells)
    return rows


# ---------------------------------------------------------------------------
# NUMBERING.md
# ---------------------------------------------------------------------------

def parse_numbering(path):
    text = path.read_text(encoding='utf-8')
    sections = split_sections(text)

    pf_ranges = {}
    for row in table_rows(sections.get('PF reserved ranges', '')):
        section = row[0].strip()
        nums = re.findall(r'PF-\d+\.(\d+)', row[1])
        if len(nums) >= 2:
            pf_ranges[section] = (int(nums[0]), int(nums[-1]))

    mc_ranges = {}
    for row in table_rows(sections.get('MC reserved blocks', '')):
        dimension = row[0].strip()
        nums = [int(n) for n in re.findall(r'MC-(\d+)', row[1])]
        if len(nums) >= 2:
            mc_ranges[dimension] = (min(nums), max(nums))

    allocated = []
    for row in table_rows(sections.get('Allocated IDs', '')):
        if not row or not row[0]:
            continue
        allocated.append({
            'id': row[0].strip(),
            'title': row[1].strip() if len(row) > 1 else '',
            'defined_in': row[2].strip() if len(row) > 2 else '',
            'added_in': row[3].strip() if len(row) > 3 else '',
        })

    deprecated_ids = set()
    for row in table_rows(sections.get('Deprecated IDs', '')):
        if row and row[0]:
            deprecated_ids.add(row[0].strip())

    return {
        'pf_ranges': pf_ranges,
        'mc_ranges': mc_ranges,
        'allocated': allocated,
        'deprecated': deprecated_ids,
    }


def parse_pf_subblocks(path):
    """Return {section: [(low, high, element_name), ...]} built from every
    '## PF-<n> sub-blocks' section, reusing split_sections/table_rows rather
    than a second table reader. A section with no such heading (PF-0, PF-3,
    PF-4, and PF-5 as of this writing) is simply absent from the returned
    mapping -- absence means "no sub-blocks declared", not a defect, and
    check_range_id below keeps exactly today's section-range-only behaviour
    for it."""
    text = path.read_text(encoding='utf-8')
    sections = split_sections(text)
    subblocks = {}
    for heading, body in sections.items():
        m = re.match(r'^(PF-\d+) sub-blocks$', heading)
        if not m:
            continue
        section = m.group(1)
        blocks = []
        for row in table_rows(body):
            if len(row) < 2:
                continue
            element_name = row[0].strip()
            nums = re.findall(r'PF-\d+\.(\d+)', row[1])
            if len(nums) >= 2:
                blocks.append((int(nums[0]), int(nums[-1]), element_name))
        if blocks:
            subblocks[section] = blocks
    return subblocks


# ---------------------------------------------------------------------------
# ID-integrity checks (D-05)
# ---------------------------------------------------------------------------

def check_dup_id(allocated):
    seen = {}
    for row in allocated:
        seen.setdefault(row['id'], []).append(row)
    violations = []
    for id_, rows in seen.items():
        if len(rows) > 1:
            violations.append((id_, f"dup-id {id_} appears in {len(rows)} rows of the Allocated IDs table"))
    return violations


def check_range_id(allocated, pf_ranges, mc_ranges, pf_subblocks=None):
    pf_subblocks = pf_subblocks or {}
    violations = []
    for row in allocated:
        id_ = row['id']
        m = PF_ID_RE.match(id_)
        if m:
            section = f"PF-{m.group(1)}"
            n = int(m.group(2))
            rng = pf_ranges.get(section)
            if rng is None or not (rng[0] <= n <= rng[1]):
                violations.append((id_, f"range-id {id_} sits outside section {section}'s reserved range"))
                continue
            blocks = pf_subblocks.get(section)
            if blocks and not any(lo <= n <= hi for lo, hi, _ in blocks):
                violations.append((id_, f"range-id {id_} sits inside section {section}'s reserved range but outside every sub-block {section} declares"))
            continue
        m = MC_ID_RE.match(id_)
        if m:
            n = int(m.group(1))
            if not any(rng[0] <= n <= rng[1] for rng in mc_ranges.values()):
                violations.append((id_, f"range-id {id_} belongs to no declared MC dimension block"))
    return violations


def check_revived_id(allocated, deprecated_ids):
    violations = []
    for row in allocated:
        if row['id'] in deprecated_ids:
            violations.append((row['id'], f"revived-id {row['id']} appears in both the Allocated IDs and Deprecated IDs tables"))
    return violations


def check_undefined_id(allocated, repo_root):
    allocated_ids = {row['id'] for row in allocated}
    roots = [repo_root / 'skills', repo_root / 'examples', repo_root / 'README.md']
    files = []
    for root in roots:
        if not root.exists():
            continue
        if root.is_file():
            files.append(root)
        else:
            files.extend(sorted(root.rglob('*.md')))
    violations = []
    seen = set()
    for f in files:
        if f.name == 'NUMBERING.md':
            continue
        text = strip_fences(f.read_text(encoding='utf-8'))
        tokens = set(re.findall(r'PF-\d+\.\d+', text)) | set(re.findall(r'MC-\d+', text))
        for tok in sorted(tokens):
            key = (tok, str(f))
            if tok not in allocated_ids and key not in seen:
                seen.add(key)
                rel = f.relative_to(repo_root)
                violations.append((tok, f"undefined-id {tok} cited in {rel} but not defined in the Allocated IDs table"))
    return violations


ID_CHECK_CODES = ['dup-id', 'range-id', 'revived-id', 'undefined-id']


def run_id_checks(repo_root):
    numbering_path = repo_root / 'NUMBERING.md'
    if not numbering_path.exists():
        return []
    data = parse_numbering(numbering_path)
    pf_subblocks = parse_pf_subblocks(numbering_path)
    violations = []
    violations += check_dup_id(data['allocated'])
    violations += check_range_id(data['allocated'], data['pf_ranges'], data['mc_ranges'], pf_subblocks)
    violations += check_revived_id(data['allocated'], data['deprecated'])
    violations += check_undefined_id(data['allocated'], repo_root)
    return violations


# ---------------------------------------------------------------------------
# examples/deal-brief.md — figure integrity (D-10)
# ---------------------------------------------------------------------------

def parse_deal_brief(path):
    text = path.read_text(encoding='utf-8')
    sections = split_sections(text)
    figures = []
    for row in table_rows(sections.get('Canonical figures', '')):
        if not row or not row[0]:
            continue
        figures.append({
            'key': row[0].strip(),
            'value': row[1].strip() if len(row) > 1 else '',
            'type': row[2].strip() if len(row) > 2 else '',
            'what': row[3].strip() if len(row) > 3 else '',
        })
    return figures


def check_dup_figure_key(figures):
    seen = {}
    for f in figures:
        seen.setdefault(f['key'], []).append(f)
    violations = []
    for key, rows in seen.items():
        if len(rows) > 1:
            violations.append((key, f"dup-figure-key {key} appears in {len(rows)} rows of the Canonical figures table"))
    return violations


def check_figure_order(figures):
    keys = [f['key'] for f in figures]
    if keys and keys != sorted(keys):
        return [(keys[0], "figure-order the Canonical figures table's rows are not in ascending key order")]
    return []


CURRENCY_RE = re.compile(r'\$\d[\d,]*(?:\.\d+)?[MKB]?')
PERCENT_RE = re.compile(r'\b\d+(?:\.\d+)?%')
ISO_DATE_RE = re.compile(r'\b\d{4}-\d{2}-\d{2}\b')


UNLISTED_FIGURE_SCAN_ROOTS = ('examples', 'skills')


def check_unlisted_figure(figures, repo_root):
    canonical_values = {f['value'] for f in figures}
    violations = []
    seen = set()
    files = []
    for root_name in UNLISTED_FIGURE_SCAN_ROOTS:
        root = repo_root / root_name
        if not root.exists():
            continue
        files.extend(sorted(root.rglob('*.md')))
    for f in files:
        if f.name == 'NUMBERING.md':
            continue
        text = strip_fences(f.read_text(encoding='utf-8'))
        lines = text.splitlines()
        in_canonical = False
        for line in lines:
            if re.match(r'^## Canonical figures\s*$', line):
                in_canonical = True
                continue
            # Bound the exempt region by table shape, not only by the next
            # heading: a blank/table-row line keeps it open; the first line
            # that is neither ends it and is itself scanned below.
            if in_canonical:
                stripped = line.strip()
                if stripped == '' or stripped.startswith('|'):
                    continue
                in_canonical = False
            if re.match(r'^## ', line):
                in_canonical = False
            if line.startswith('Last reviewed:'):
                continue
            tokens = CURRENCY_RE.findall(line) + PERCENT_RE.findall(line) + ISO_DATE_RE.findall(line)
            for tok in tokens:
                if tok not in canonical_values:
                    key = (tok, str(f))
                    if key not in seen:
                        seen.add(key)
                        rel = f.relative_to(repo_root)
                        violations.append((tok, f"unlisted-figure {tok} in {rel} has no matching Canonical figures row"))
    return violations


FIGURE_CHECK_CODES = ['dup-figure-key', 'figure-order', 'unlisted-figure']


def run_figure_checks(repo_root):
    brief_path = repo_root / 'examples' / 'deal-brief.md'
    if not brief_path.exists():
        return []
    figures = parse_deal_brief(brief_path)
    violations = []
    violations += check_dup_figure_key(figures)
    violations += check_figure_order(figures)
    violations += check_unlisted_figure(figures, repo_root)
    return violations


# ---------------------------------------------------------------------------
# NOTICES.md — attribution integrity (D-14)
# ---------------------------------------------------------------------------

FENCE_CONTENT_RE = re.compile(r'```[^\n]*\n(.*?)\n```', re.S)


def _carrier_is_repo_relative(carrier):
    """True unless carrier is absolute, a drive-letter path, or escapes the
    repository via a '..' path segment. A carrier failing this test is never
    opened (T-01-01: pathlib's '/' operator silently discards the base for an
    absolute right-hand side)."""
    if carrier.startswith('/') or carrier.startswith('\\'):
        return False
    if re.match(r'^[A-Za-z]:', carrier):
        return False
    parts = re.split(r'[\\/]', carrier)
    if '..' in parts:
        return False
    return True


def parse_notices(path):
    text = path.read_text(encoding='utf-8')
    sections = split_sections(text)
    body = sections.get(POINTER_SECTION, '')

    pointer = None
    m = FENCE_CONTENT_RE.search(body)
    if m:
        content = m.group(1).strip()
        if content:
            pointer = content

    carriers = []
    idx = body.find(CARRIERS_MARKER)
    if idx != -1:
        tail = body[idx:]
        for line in tail.splitlines()[1:]:
            m2 = re.match(r'^\s*[-*]\s+`?([^`\n]+?)`?\s*$', line)
            if m2:
                carriers.append(m2.group(1).strip())
            elif line.strip().startswith('#'):
                break
    return pointer, carriers


def check_pointer(pointer, carriers, repo_root):
    violations = []
    if pointer is None:
        return violations
    for carrier in carriers:
        p = repo_root / carrier
        if not p.exists():
            continue
        count = sum(1 for line in p.read_text(encoding='utf-8').splitlines() if line.strip() == pointer)
        if count == 0:
            violations.append((carrier, f"pointer-missing {carrier} does not contain the attribution pointer string"))
        elif count > 1:
            violations.append((carrier, f"pointer-duplicated {carrier} contains the attribution pointer string {count} times"))
    return violations


NOTICES_CHECK_CODES = ['pointer-missing', 'pointer-duplicated', 'pointer-unparseable']


# ---------------------------------------------------------------------------
# LICENSE.md — license integrity (LEG-01)
# ---------------------------------------------------------------------------

def check_license_missing(repo_root):
    """Check that LICENSE exists at repo root, is non-empty, and begins
    with 'MIT License'."""
    violations = []
    license_path = repo_root / 'LICENSE'
    if not license_path.exists():
        violations.append(('LICENSE', "license-missing LICENSE file is absent from the repository root"))
        return violations

    text = license_path.read_text(encoding='utf-8')
    if not text:
        violations.append(('LICENSE', "license-missing LICENSE file is empty"))
        return violations

    first_line = text.split('\n')[0] if text else ''
    if not first_line.startswith('MIT License'):
        violations.append(('LICENSE', "license-missing LICENSE file does not identify itself as the MIT License"))

    return violations


LICENSE_CHECK_CODES = ['license-missing']


def run_license_checks(repo_root):
    violations = []
    violations += check_license_missing(repo_root)
    return violations


# ---------------------------------------------------------------------------
# README.md — results pointer integrity (CR-02)
#
# This is a repository-level documentation check, not a catalog check: it
# does not depend on NUMBERING.md or on any skills/*/SKILL.md path. It
# asserts only that the literal results-pointer path string is present in
# README.md, unconditionally -- it is not gated on the file the path names
# actually existing on disk.
# ---------------------------------------------------------------------------

README_RESULTS_POINTER = 'evals/conformance/RESULTS-mod04.md'


def check_readme_results_pointer(repo_root):
    """Check that README.md contains the literal path
    'evals/conformance/RESULTS-mod04.md' at least once, so a reader can
    discover this repository's one committed measurement from the same
    README that would otherwise claim no measurement exists (CR-02).

    Returns no violation when README.md itself does not exist -- no
    fixture root in this suite ships a bare repo with no README.md at all,
    and a missing README.md is a different, unrelated failure mode this
    check does not own.

    Declared ceiling: this check asserts one literal path string is present
    in README.md. It does not assert that the file at that path exists,
    that the figures in it are current, or that the prose around the
    pointer is accurate. A human read is the only thing that establishes
    the last of those -- this check only makes the measurement discoverable
    and makes its silent disappearance from README a gate failure, nothing
    more."""
    violations = []
    readme_path = repo_root / 'README.md'
    if not readme_path.exists():
        return violations
    text = readme_path.read_text(encoding='utf-8')
    if README_RESULTS_POINTER not in text:
        violations.append(('README.md', (
            f"readme-results-pointer-missing README.md does not contain the literal path "
            f"'{README_RESULTS_POINTER}', so a reader has no pointer to this repository's "
            f"committed measurement"
        )))
    return violations


README_CHECK_CODES = [
    'readme-results-pointer-missing', 'readme-install-path-missing', 'readme-before-after-order',
    'readme-example-drift', 'readme-example-lead-distance', 'readme-layout-legend-drift',
    'readme-output-style-destination-missing',
    'readme-claim-unsourced', 'readme-claim-unanchored', 'readme-badge-unlisted',
    'readme-layout-tree-stale',
]


def run_readme_checks(repo_root):
    # check_readme_install_paths, check_readme_before_after_order,
    # check_readme_example_drift, check_readme_example_lead_distance,
    # and check_readme_layout_legend_drift are all defined later in this
    # file, after SKILLS_CLI_INSTALL_RE and MARKETPLACE_ADD_RE (Phase 4,
    # 04-04) or after README_BEFORE_AFTER_HEADING/
    # README_FIRST_EXAMPLE_MAX_LINE/README_LAYOUT_HEADING (Phase 4,
    # 04-09) -- each reuses module-level patterns declared at those
    # later points rather than declaring a second copy, so each is
    # defined where those patterns already exist. Python resolves these
    # names at call time, not at def time, so calling them here (before
    # their own def statements appear in the file) is safe: by the time
    # run_readme_checks() actually runs, the whole module has been
    # loaded.
    violations = []
    violations += check_readme_results_pointer(repo_root)
    violations += check_readme_install_paths(repo_root)
    violations += check_readme_before_after_order(repo_root)
    violations += check_readme_example_drift(repo_root)
    violations += check_readme_example_lead_distance(repo_root)
    violations += check_readme_layout_legend_drift(repo_root)
    violations += check_readme_output_style_destination(repo_root)
    violations += check_readme_claim_unsourced(repo_root)
    violations += check_readme_claim_unanchored(repo_root)
    violations += check_readme_badge_unlisted(repo_root)
    violations += check_readme_layout_tree_stale(repo_root)
    return violations


# ---------------------------------------------------------------------------
# README.md claim region, badges, and layout-tree currency (LEG-05)
# ---------------------------------------------------------------------------

CLAIM_REGION_START = '<!-- claim-region:start -->'
CLAIM_REGION_END = '<!-- claim-region:end -->'

# A maximal run of a digit followed by digits, commas, dots or percent
# signs. Frozen here so the check is not arguable: '2026-09-18', '38',
# '7.47', '30.0%' and '48' are one token each.
_CLAIM_NUMERIC_TOKEN_RE = re.compile(r'\d[\d,.%]*')

# The exact model strings a claim-region paragraph may anchor to. Exact
# strings, not a pattern: LEG-05 asks for model VERSIONS, and a pattern
# matching 'claude-*' would accept a family name that names no version.
CLAIM_MODEL_STRINGS = ('claude-opus-5', 'claude-sonnet-5')

_CLAIM_ISO_DATE_RE = re.compile(r'\d{4}-\d{2}-\d{2}')

# Glob for the committed results files a claim-region number may source
# from. Sorted at read time so the corpus is deterministic.
CLAIM_SOURCE_GLOB = 'evals/*/RESULTS*.md'

_MARKDOWN_IMAGE_RE = re.compile(r'!\[[^\]]*\]\(([^)]*)\)')

# Badge policy, frozen: build status and license only. Neither carries a
# measured product claim -- a CI badge reports that ten offline commands
# exited zero, and a license badge states what LICENSE already states. No
# badge may carry a number this repository has not measured, which is why
# every shields.io endpoint and every dynamic badge is refused rather than
# reviewed case by case.
BADGE_ALLOW_LIST = (
    'actions/workflows/ci.yml/badge.svg',
    'img.shields.io/badge/License-MIT-',
)

# Directory under which every immediate subdirectory must appear in
# README's layout tree, and the names never expected to appear there.
LAYOUT_TREE_SCAN_DIR = 'evals'
LAYOUT_TREE_SKIP_DIRS = ('__pycache__',)


def _claim_region(repo_root):
    """Return (region_text, error) for README's claim region.

    error is a message when the markers are unbalanced or out of order --
    an unbounded region is not an empty one, and reading it as empty would
    let deleting the end marker switch the check off. (None, None) means
    README has neither marker, which is silent by design so a README
    without a claim region is not retroactively in violation."""
    path = repo_root / 'README.md'
    if not path.exists():
        return None, None
    text = path.read_text(encoding='utf-8')
    starts = text.count(CLAIM_REGION_START)
    ends = text.count(CLAIM_REGION_END)
    if starts == 0 and ends == 0:
        return None, None
    if starts != 1 or ends != 1:
        return None, (
            f"README.md carries {starts} '{CLAIM_REGION_START}' and {ends} "
            f"'{CLAIM_REGION_END}' marker(s); exactly one of each is required"
        )
    start_idx = text.find(CLAIM_REGION_START)
    end_idx = text.find(CLAIM_REGION_END)
    if end_idx < start_idx:
        return None, (
            f"README.md's '{CLAIM_REGION_END}' precedes its '{CLAIM_REGION_START}', "
            f"so the claim region has no readable extent"
        )
    return text[start_idx + len(CLAIM_REGION_START):end_idx], None


def _claim_numeric_tokens(text):
    """Every numeric token in text, trailing sentence punctuation stripped.
    A token that is only punctuation after stripping is discarded."""
    tokens = []
    for raw in _CLAIM_NUMERIC_TOKEN_RE.findall(text):
        token = raw.rstrip('.,')
        if token:
            tokens.append(token)
    return tokens


def check_readme_claim_unsourced(repo_root):
    """Check that every number inside README's claim region appears in a
    committed results file (LEG-05).

    README legitimately carries numbers that are not measured claims -- a
    rule count, a worked-pair count, the figures inside the before/after
    example. A whole-file check would have to whitelist all of those, which
    is unmaintainable, or be switched off, which is useless. The region is
    bounded so the check can be strict where strictness means something.

    Fires once per unsourced token, naming it. Also fires once when the
    markers are unbalanced or reversed, because an unbounded region is not
    an empty one and reading it as empty would make deleting the end marker
    a way around the check. Silent when README carries neither marker, and
    silent when README.md does not exist.

    Declared ceiling (substring matching): a token is sourced if it appears
    anywhere in the corpus as a substring, so `48` is sourced by any file
    containing `1948`. This check exists to catch a number invented out of
    nothing, not to prove provenance to the digit -- the pointer to the
    results file is what does that."""
    violations = []
    region, error = _claim_region(repo_root)
    if error:
        return [('README.md', f"readme-claim-unsourced {error}")]
    if region is None:
        return violations
    corpus = ''
    for path in sorted((repo_root).glob(CLAIM_SOURCE_GLOB)):
        corpus += path.read_text(encoding='utf-8')
    for token in sorted(set(_claim_numeric_tokens(region))):
        if token not in corpus:
            violations.append(('README.md', (
                f"readme-claim-unsourced README.md's claim region states {token}, which appears "
                f"in no file matching {CLAIM_SOURCE_GLOB}"
            )))
    return violations


def check_readme_claim_unanchored(repo_root):
    """Check that every claim-region paragraph carrying a number also names
    an exact model version and an ISO-8601 date (LEG-05).

    A number with no model behind it is a number about nothing, and a
    number with no date behind it cannot be re-derived. Paragraphs are
    separated by blank lines, so the anchor has to travel with the figure
    rather than sitting once at the top of a section a reader may not have
    read.

    Fires once per offending paragraph, naming its first line. Silent when
    README carries no claim region and when README.md does not exist; the
    unbalanced-marker condition is reported by readme-claim-unsourced
    alone, so one broken region is one violation and not two.

    Declared ceiling (presence, not correspondence): this asserts that a
    model string and a date are present in the paragraph. It does not and
    cannot assert that they are the model and the date that produced that
    paragraph's number."""
    violations = []
    region, error = _claim_region(repo_root)
    if error or region is None:
        return violations
    for paragraph in re.split(r'\n\s*\n', region):
        if not _claim_numeric_tokens(paragraph):
            continue
        has_model = any(model in paragraph for model in CLAIM_MODEL_STRINGS)
        has_date = bool(_CLAIM_ISO_DATE_RE.search(paragraph))
        if has_model and has_date:
            continue
        missing = []
        if not has_model:
            missing.append('a model version from ' + '/'.join(CLAIM_MODEL_STRINGS))
        if not has_date:
            missing.append('an ISO-8601 date')
        first_line = next((l.strip() for l in paragraph.splitlines() if l.strip()), '')
        violations.append(('README.md', (
            f"readme-claim-unanchored README.md's claim-region paragraph beginning "
            f"{first_line[:60]!r} states a figure without {' and without '.join(missing)}"
        )))
    return violations


def check_readme_badge_unlisted(repo_root):
    """Check that README carries no badge outside the frozen allow-list.

    A badge is read as third-party verification. BADGE_ALLOW_LIST admits
    build status and license only, because neither asserts anything about
    document quality. Everything else -- any shields.io endpoint, any
    dynamic badge, any badge carrying a number -- is refused.

    README carries no images at all today, so this code ships silent and
    stands as a gate against a future addition rather than a cleanup of an
    existing one.

    Fires once per offending image, naming its URL. Silent when README.md
    does not exist.

    Declared ceiling (Markdown syntax only): this sees `![alt](url)`. A
    badge embedded as a raw HTML `<img>` tag is invisible to it. That is
    stated rather than papered over with a second regex, because an HTML
    detector would have to decide what counts as an image element and this
    check does not need that argument."""
    violations = []
    path = repo_root / 'README.md'
    if not path.exists():
        return violations
    for url in _MARKDOWN_IMAGE_RE.findall(path.read_text(encoding='utf-8')):
        looks_like_badge = (
            'badge' in url or 'shields.io' in url or url.endswith('.svg')
        )
        if not looks_like_badge:
            continue
        if any(allowed in url for allowed in BADGE_ALLOW_LIST):
            continue
        violations.append(('README.md', (
            f"readme-badge-unlisted README.md carries a badge image {url} that is not on the "
            f"frozen allow-list; build status and license badges are permitted because neither "
            f"carries a measured product claim"
        )))
    return violations


def check_readme_layout_tree_stale(repo_root):
    """Check that README's layout tree names every eval family on disk.

    readme-layout-legend-drift's own docstring says it "says nothing about
    ... whether the tree matches the filesystem". This closes exactly that
    gap, at one level: every immediate subdirectory of evals/ that exists
    on disk must appear in README's layout tree. evals/routes/ existed on
    disk, was referenced twice in README prose, and was absent from the
    tree -- and nothing caught it.

    Scoped to evals/ because that is where this repository adds families,
    and to one level because a full tree diff would fire on __pycache__ and
    on every future fixture directory. __pycache__ and dot-prefixed names
    are skipped.

    Fires once per missing directory, sorted by name. Silent when README.md
    or evals/ does not exist.

    Declared ceiling (presence, not placement): it checks that the
    directory's name appears somewhere in the tree text. It does not check
    that the entry sits in the right place, that its children are listed,
    or that every path the tree names still exists -- only that no family
    on disk is missing from it."""
    violations = []
    path = repo_root / 'README.md'
    scan_dir = repo_root / LAYOUT_TREE_SCAN_DIR
    if not path.exists() or not scan_dir.is_dir():
        return violations
    text = path.read_text(encoding='utf-8')
    heading_idx = text.find(README_LAYOUT_HEADING)
    if heading_idx == -1:
        return violations
    next_heading = text.find('\n## ', heading_idx + 1)
    section = text[heading_idx:] if next_heading == -1 else text[heading_idx:next_heading]

    for child in sorted(scan_dir.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith('.') or child.name in LAYOUT_TREE_SKIP_DIRS:
            continue
        if f'{child.name}/' in section:
            continue
        violations.append(('README.md', (
            f"readme-layout-tree-stale README.md's '{README_LAYOUT_HEADING}' tree does not name "
            f"{LAYOUT_TREE_SCAN_DIR}/{child.name}/, which exists on disk"
        )))
    return violations


# ---------------------------------------------------------------------------
# evals/conformance/RESULTS-mod04.md — verdict-breakdown enumeration
# integrity (03-REVIEW.md WR-01 gap closure)
#
# This is a repository-level documentation check, not a catalog check: it
# does not depend on NUMBERING.md or on any skills/*/SKILL.md path. It
# reads exactly RESULTS_BREAKDOWN_PATH, the one file holding this
# project's only committed measurement, and requires that any
# verdict-breakdown bullet's stated count agree with its own parenthetical
# enumeration -- the exact defect class 03-REVIEW.md WR-01 found and
# 03-13 hand-corrected. This check makes the class mechanically guarded
# rather than protecting only today's instance.
# ---------------------------------------------------------------------------

RESULTS_BREAKDOWN_PATH = 'evals/conformance/RESULTS-mod04.md'

# Frozen against run_conformance.py's own verdict vocabulary -- a
# reworded copy here would silently stop matching the lines it exists to
# guard.
RESULTS_VERDICT_LABELS = ('conformant', 'no-family', 'rule-before-family', 'unscoreable')

_RESULTS_BULLET_RE = re.compile(
    r'^- (' + '|'.join(re.escape(label) for label in RESULTS_VERDICT_LABELS) +
    r'): (\d+)(?:\s*\((.*)\))?\s*$'
)
_RESULTS_XN_RE = re.compile(r'(?<![\w-])x(\d+)(?![\w-])')


def check_results_breakdown_count(repo_root):
    """Check that every verdict-breakdown bullet in
    evals/conformance/RESULTS-mod04.md (RESULTS_BREAKDOWN_PATH) states a
    count that agrees with its own parenthetical enumeration, so a reader
    can re-derive the number without opening the raw run blocks (WR-01).

    Walks the file (after strip_fences()) line by line, joining each
    bullet matching '- {verdict-label}: {count}' with its continuation
    lines -- a following line that is non-blank, begins with whitespace,
    and does not itself start a new bullet or heading -- and collapsing
    the joined line's whitespace to single spaces. A line whose label is
    not one of RESULTS_VERDICT_LABELS is not a verdict-breakdown bullet at
    all (e.g. the 03-08 section's '- claude-sonnet-5: 12 attempted ...'
    model tallies) and is skipped entirely.

    For the parenthetical that follows the count, if any, splits its
    contents on commas and sums one per item, except an item carrying a
    standalone 'xN' multiplier token contributes N -- so two items naming
    the same fixture (e.g. 'A-rfp-answer x2') are never merged, and the
    sum does not depend on item order. An empty parenthetical sums to
    zero.

    Fires results-breakdown-count-mismatch in either of two cases: the
    parenthetical is absent and the stated count is greater than zero, or
    the parenthetical is present and its sum disagrees with the stated
    count. One code covers both triggers rather than the unstated/
    mismatch code pair the PF and MC catalog counts use
    (catalog-count-unstated/-mismatch, mc-count-unstated/-mismatch) --
    both triggers here are the same defect (an itemization a reader
    cannot re-derive) against a free-prose measurement file, not two
    distinct authoring errors against a frozen sentence template.

    Returns no violations when RESULTS_BREAKDOWN_PATH does not exist,
    checked before any read -- the same declared ceiling every other
    optional-file check in this module uses, so a fixture root shipping
    no results file stays silent and the suite is not disabled.

    Declared ceiling: this check asserts an enumeration is internally
    consistent with the count beside it. It makes no claim about whether
    the measurement itself is correct, current, or well-designed. It
    counts an 'xN' token as N and any other comma-separated item as one,
    so an enumeration written in a different grammar (a range, a prose
    'and two more') will not be counted the way its author intended. It
    reads one named path, not every results file that might ever exist."""
    violations = []
    path = repo_root / RESULTS_BREAKDOWN_PATH
    if not path.exists():
        return violations
    text = strip_fences(path.read_text(encoding='utf-8'))
    lines = text.splitlines()

    joined_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('- '):
            parts = [line.strip()]
            j = i + 1
            while j < len(lines):
                nxt = lines[j]
                if nxt.strip() == '':
                    break
                if not nxt[:1].isspace():
                    break
                stripped_nxt = nxt.lstrip()
                if stripped_nxt.startswith('- ') or stripped_nxt.startswith('#'):
                    break
                parts.append(stripped_nxt)
                j += 1
            joined_lines.append(' '.join(parts))
            i = j
        else:
            i += 1

    for joined in joined_lines:
        collapsed = re.sub(r'\s+', ' ', joined).strip()
        m = _RESULTS_BULLET_RE.match(collapsed)
        if not m:
            continue
        label, stated_str, parenthetical = m.groups()
        stated = int(stated_str)
        if parenthetical is None:
            if stated > 0:
                violations.append((str(path.relative_to(repo_root)), (
                    f"results-breakdown-count-mismatch {RESULTS_BREAKDOWN_PATH} states "
                    f"'{label}: {stated}' with no enumeration to re-derive it from"
                )))
            continue
        items = [item.strip() for item in parenthetical.split(',') if item.strip()]
        total = 0
        for item in items:
            xm = _RESULTS_XN_RE.search(item)
            total += int(xm.group(1)) if xm else 1
        if total != stated:
            violations.append((str(path.relative_to(repo_root)), (
                f"results-breakdown-count-mismatch {RESULTS_BREAKDOWN_PATH} states "
                f"'{label}: {stated}' but its enumeration sums to {total}"
            )))
    return violations


RESULTS_CHECK_CODES = ['results-breakdown-count-mismatch']


def run_results_checks(repo_root):
    violations = []
    violations += check_results_breakdown_count(repo_root)
    return violations


# ---------------------------------------------------------------------------
# SOURCES.md — approved-source provenance (LEG-04)
# ---------------------------------------------------------------------------

SOURCES_PATH = 'SOURCES.md'

# The three '## ' headings whose bodies carry source tables. Every other
# heading in SOURCES.md is prose -- the rule, the reproduction boundary,
# the out-of-bounds list -- and carries no rows to check. Naming the three
# rather than scanning every table means a future prose section that
# happens to contain a Markdown table is not read as a source list.
SOURCES_TABLE_HEADINGS = (
    'Message articulation sources',
    'Qualification checklist sources',
    'Commercial teaching sources',
)

# Title | Author or publisher | Kind | Status | Where
SOURCES_ROW_CELLS = 5

_SOURCES_RETRIEVED_RE = re.compile(r'\(retrieved (\d{4}-\d{2}-\d{2})\)')


def check_source_row_unconfirmed(repo_root):
    """Check that every SOURCES.md row claiming `verified` status records
    what was read and when, so the approved-source rule that file states
    ("a concept with no listed source does not ship") is enforced by the
    build rather than by good intentions (LEG-04).

    Reads the three tables named by SOURCES_TABLE_HEADINGS with the
    existing split_sections()/table_rows() pair. A row is in scope only
    when its Status cell is exactly 'verified' after whitespace stripping,
    compared case-sensitively -- the same no-case-folding discipline this
    module applies to the attribution pointer. An 'unverified' row is an
    honest statement that the source has not been confirmed yet; firing on
    it would make the pre-review state a build failure and would force
    every row to be confirmed at once.

    An in-scope row must carry both an absolute URL and a retrieval date in
    its Where cell. The URL test is a plain 'https://' prefix test over
    whitespace-delimited tokens rather than a general URL regex -- what
    counts as a well-formed URL is an argument this check does not need to
    have, and a bare prefix test cannot be satisfied by prose. The date
    must match '(retrieved YYYY-MM-DD)' AND parse with
    datetime.date.fromisoformat, so a well-shaped impossibility like
    2026-13-45 is caught rather than matched.

    A row whose cell count is not SOURCES_ROW_CELLS fires once naming the
    parse failure. Skipping it silently would let a row that lost its
    Status column be read as out of scope -- the failure mode a checker
    exists to prevent.

    Returns no violations when SOURCES.md does not exist, checked before
    any read: the same declared ceiling every other optional-file check in
    this module uses, so a fixture root shipping no sources file stays
    silent and the rest of the suite is not disabled. This is deliberately
    not the check_license_missing precedent -- SOURCES.md is not required
    to exist the way LICENSE is.

    Declared ceiling (no fetch): this check does not fetch the recorded
    URL. A URL that has rotted, moved, or never resolved is
    indistinguishable here from a live one. The lookup happens once, by
    hand, at the moment a row is confirmed; CI reads only the committed
    record and performs no network call. A build that fails because a
    third party had an outage is not reproducible, so this ceiling is a
    design decision, not a gap to close.

    Declared ceiling (no semantics): this check does not judge whether the
    source at that URL says what the row claims. That is the same semantic
    judgement SOURCES.md's own "What counts as reproduction" section
    states no tool in this project's stack performs, and this check does
    not become the exception."""
    violations = []
    path = repo_root / SOURCES_PATH
    if not path.exists():
        return violations
    subject = str(path.relative_to(repo_root))
    sections = split_sections(path.read_text(encoding='utf-8'))

    for heading in SOURCES_TABLE_HEADINGS:
        if heading not in sections:
            continue
        for row in table_rows(sections[heading]):
            if len(row) != SOURCES_ROW_CELLS:
                violations.append((subject, (
                    f"source-row-unconfirmed {SOURCES_PATH} '{heading}' has a row of "
                    f"{len(row)} cells where {SOURCES_ROW_CELLS} are required, so its "
                    f"status and provenance cannot be read: {' | '.join(row)}"
                )))
                continue
            title, _publisher, _kind, status, where = row
            if status != 'verified':
                continue
            has_url = any(token.startswith('https://') for token in where.split())
            date_match = _SOURCES_RETRIEVED_RE.search(where)
            has_date = False
            if date_match:
                try:
                    datetime.date.fromisoformat(date_match.group(1))
                except ValueError:
                    has_date = False
                else:
                    has_date = True
            if has_url and has_date:
                continue
            if not has_url and not has_date:
                missing = "no https:// URL and no valid (retrieved YYYY-MM-DD) date"
            elif not has_url:
                missing = "no https:// URL"
            else:
                missing = "no valid (retrieved YYYY-MM-DD) date"
            violations.append((subject, (
                f"source-row-unconfirmed {SOURCES_PATH} row {title} is marked verified "
                f"but its Where cell carries {missing}"
            )))

    # Every violation here shares one subject, so the live run's
    # (code, subject) sort cannot order them. Sort on the message so two
    # offending rows report in a fixed order rather than in whatever order
    # the tables happened to be written.
    violations.sort(key=lambda v: v[1])
    return violations

LEGAL_REVIEW_PATH = 'LEGAL-REVIEW.md'

# One frozen line, compared byte for byte after stripping leading and
# trailing whitespace, with no case folding -- the same equality discipline
# check_pointer applies to the attribution pointer, and for the same reason:
# a gate marker a reader could satisfy three different ways is not a marker.
GATE_STATUS_PREFIX = 'Gate status:'
GATE_STATUS_PASSED = 'PASSED'
GATE_STATUS_VALUES = ('PASSED', 'OPEN', 'FAILED')

_REVIEW_DATE_RE = re.compile(r'^Review date: (\d{4}-\d{2}-\d{2})$', re.M)

# Heading -> the name reported as the violation's subject, so two stale
# statements produce two distinguishable rows under the (code, subject) sort.
FRAMEWORK_STATEMENT_HEADINGS = (
    ('### Command of the Message', 'Command of the Message'),
    ('### MEDDIC, MEDDICC, and related marks', 'MEDDIC/MEDDICC'),
    ('### Challenger', 'Challenger'),
)

_LAST_REVIEWED_RE = re.compile(r'^Last reviewed: (.+)$', re.M)


def _framework_section(text, heading):
    """Bound one framework statement from its heading to the next '### ' or
    '## ' heading -- the same bounding check_framework_statements() uses.
    Returns None when the heading is absent."""
    heading_idx = text.find(heading)
    if heading_idx == -1:
        return None
    next_section = len(text)
    for pattern in ('### ', '## '):
        idx = text.find('\n' + pattern, heading_idx + 1)
        if idx != -1 and idx < next_section:
            next_section = idx
    return text[heading_idx:next_section]


def _review_date(repo_root):
    """Parse LEGAL-REVIEW.md's single 'Review date: YYYY-MM-DD' line.
    Returns None when the file is absent or carries no parseable date --
    both are 'nothing to compare against', not a violation on their own."""
    path = repo_root / LEGAL_REVIEW_PATH
    if not path.exists():
        return None
    match = _REVIEW_DATE_RE.search(path.read_text(encoding='utf-8'))
    if not match:
        return None
    try:
        return datetime.date.fromisoformat(match.group(1))
    except ValueError:
        return None


def check_source_gate_incomplete(repo_root):
    """Check that LEGAL-REVIEW.md cannot declare the approved-source gate
    passed while SOURCES.md still carries an unconfirmed row (LEG-04).

    check_source_row_unconfirmed() above asserts that an individual row
    claiming confirmation names its evidence. It says nothing about
    completeness -- a review record could declare a pass over a file with
    five rows still reading 'unverified' and no check would notice. This
    code closes that half.

    Reads the gate marker by scanning LEGAL-REVIEW.md's lines for
    GATE_STATUS_PREFIX, stripping leading and trailing whitespace, and
    comparing the remainder byte for byte against GATE_STATUS_VALUES with no
    case folding. Fires when exactly one such line reads PASSED and any
    SOURCES.md row's Status cell reads 'unverified', naming the count.

    Also fires when LEGAL-REVIEW.md exists and carries no gate line at all,
    or carries more than one: an unreadable gate is not a passed gate, and
    it is not a silent one either -- silence there would let the marker be
    deleted to route around the check.

    Silent when LEGAL-REVIEW.md does not exist, so a repository that has not
    yet run a review is not retroactively in violation.

    Declared ceiling (no fetch): this check performs no network call. It
    reads two committed files and nothing else.

    Declared ceiling (frozen literal, not prose): a declared pass is read as
    one exact line. A review record that describes a pass in prose without
    that line is not detected. The marker is a frozen string rather than a
    fuzzy phrase match on purpose -- a fuzzy match over prose would be
    exactly the fuzzy-proxy build gate .planning/WINDOWS.md id 17 records
    this repository measuring and refusing.

    Declared ceiling (no semantics): it does not judge whether the review
    behind a declared pass was any good, only whether the file it declares a
    pass over is complete."""
    violations = []
    review_path = repo_root / LEGAL_REVIEW_PATH
    if not review_path.exists():
        return violations
    subject = str(review_path.relative_to(repo_root))

    gate_values = []
    for line in review_path.read_text(encoding='utf-8').splitlines():
        stripped = line.strip()
        if stripped.startswith(GATE_STATUS_PREFIX):
            gate_values.append(stripped[len(GATE_STATUS_PREFIX):].strip())

    if len(gate_values) != 1 or gate_values[0] not in GATE_STATUS_VALUES:
        violations.append((subject, (
            f"source-gate-incomplete {LEGAL_REVIEW_PATH} carries {len(gate_values)} readable "
            f"'{GATE_STATUS_PREFIX}' line(s) with value(s) {gate_values or 'none'}; exactly one "
            f"reading {' or '.join(GATE_STATUS_VALUES)} is required -- an unreadable gate is not "
            f"a passed gate"
        )))
        return violations

    if gate_values[0] != GATE_STATUS_PASSED:
        return violations

    sources_path = repo_root / SOURCES_PATH
    if not sources_path.exists():
        return violations
    sections = split_sections(sources_path.read_text(encoding='utf-8'))
    unverified = 0
    for heading in SOURCES_TABLE_HEADINGS:
        if heading not in sections:
            continue
        for row in table_rows(sections[heading]):
            if len(row) == SOURCES_ROW_CELLS and row[3] == 'unverified':
                unverified += 1

    if unverified:
        violations.append((subject, (
            f"source-gate-incomplete {LEGAL_REVIEW_PATH} declares "
            f"'{GATE_STATUS_PREFIX} {GATE_STATUS_PASSED}' while {unverified} {SOURCES_PATH} "
            f"row(s) still read unverified"
        )))
    return violations


def check_framework_statement_stale_review(repo_root):
    """Check that each NOTICES.md framework statement carries a review date
    consistent with the review that claims to have produced it (LEG-04).

    A bare date bump is indistinguishable in a diff from a review that
    actually happened. This code ties every statement's 'Last reviewed:'
    line to LEGAL-REVIEW.md's single 'Review date:' line, so a statement
    left unread while the review record was re-dated is a build failure.

    Fires once per statement that carries no 'Last reviewed:' line, one that
    does not parse as ISO-8601, or one whose date precedes the review date.
    The framework name is the violation's subject, so two stale statements
    produce two distinguishable rows under the live run's (code, subject)
    sort. A statement dated on or after the review date is silent -- later
    is fine, earlier is the defect.

    Silent when LEGAL-REVIEW.md does not exist or carries no parseable
    review date: there is nothing to compare against, and inventing a
    comparison would make the code fire for a reason it cannot name. Silent
    when NOTICES.md does not exist -- framework-statement-missing owns that
    condition and firing here too would double-report one defect.

    Declared ceiling (no fetch): this check performs no network call.

    Declared ceiling (date, not truth): it does not judge whether a
    statement is correct, only whether it carries a date and whether that
    date is consistent with the review claiming to have produced it. A
    thoroughly wrong statement re-dated today passes this check.

    Declared ceiling (coverage): it reads the 'Last reviewed:' line only.
    The 'Paraphrase boundary:' element remains unchecked by any code in this
    module -- check_framework_statements() asserts 'Non-affiliation' and
    'Rights-holder' and does not reach it."""
    violations = []
    review_date = _review_date(repo_root)
    if review_date is None:
        return violations
    notices_path = repo_root / 'NOTICES.md'
    if not notices_path.exists():
        return violations
    text = notices_path.read_text(encoding='utf-8')

    for heading, name in FRAMEWORK_STATEMENT_HEADINGS:
        section = _framework_section(text, heading)
        if section is None:
            continue  # framework-statement-missing owns an absent statement
        match = _LAST_REVIEWED_RE.search(section)
        if not match:
            violations.append((name, (
                f"framework-statement-stale-review NOTICES.md {name} statement carries no "
                f"'Last reviewed:' line to compare against {LEGAL_REVIEW_PATH}'s review date "
                f"{review_date.isoformat()}"
            )))
            continue
        raw = match.group(1).strip()
        try:
            stated = datetime.date.fromisoformat(raw)
        except ValueError:
            violations.append((name, (
                f"framework-statement-stale-review NOTICES.md {name} statement's "
                f"'Last reviewed:' value {raw!r} does not parse as an ISO-8601 date"
            )))
            continue
        if stated < review_date:
            violations.append((name, (
                f"framework-statement-stale-review NOTICES.md {name} statement was last "
                f"reviewed {stated.isoformat()}, before {LEGAL_REVIEW_PATH}'s review date "
                f"{review_date.isoformat()} -- the review that claims to have produced it "
                f"did not re-read it"
            )))
    violations.sort(key=lambda v: (v[0], v[1]))
    return violations


SOURCES_CHECK_CODES = [
    'source-row-unconfirmed',
    'source-gate-incomplete',
    'framework-statement-stale-review',
]


def run_sources_checks(repo_root):
    violations = []
    violations += check_source_row_unconfirmed(repo_root)
    violations += check_source_gate_incomplete(repo_root)
    violations += check_framework_statement_stale_review(repo_root)
    return violations


# ---------------------------------------------------------------------------
# NOTICES.md — framework statements integrity (LEG-02)
# ---------------------------------------------------------------------------

def check_framework_statements(repo_root):
    """Check that NOTICES.md carries the three required framework statements
    with their non-affiliation and trademark-rights language."""
    violations = []
    notices_path = repo_root / 'NOTICES.md'

    # Define required frameworks and their required sub-heading patterns
    frameworks = {
        'Command of the Message': ('### Command of the Message', 'Non-affiliation'),
        'MEDDIC/MEDDICC': ('### MEDDIC, MEDDICC, and related marks', 'Non-affiliation'),
        'Challenger': ('### Challenger', 'Non-affiliation'),
    }

    if not notices_path.exists():
        # If NOTICES.md is missing, all three frameworks are missing
        for framework_name in frameworks.keys():
            violations.append((framework_name, f"framework-statement-missing {framework_name} subsection is missing from NOTICES.md"))
        return violations

    text = notices_path.read_text(encoding='utf-8')

    for framework_name, (heading_pattern, required_language) in frameworks.items():
        if heading_pattern not in text:
            violations.append((framework_name, f"framework-statement-missing {framework_name} subsection is missing from NOTICES.md"))
            continue

        # Find the section for this framework
        heading_idx = text.find(heading_pattern)
        # Find the end of this section (next ### or ##)
        next_section = len(text)
        for pattern in ['### ', '## ']:
            idx = text.find('\n' + pattern, heading_idx + 1)
            if idx != -1 and idx < next_section:
                next_section = idx

        framework_section = text[heading_idx:next_section]

        # Check for non-affiliation language
        if 'Non-affiliation' not in framework_section or 'not affiliated' not in framework_section.lower():
            violations.append((framework_name, f"framework-statement-missing {framework_name} subsection missing non-affiliation language"))

        # Check for trademark/rights language
        if 'Rights-holder' not in framework_section:
            violations.append((framework_name, f"framework-statement-missing {framework_name} subsection missing trademark-rights language"))

    return violations


FRAMEWORK_CHECK_CODES = ['framework-statement-missing']


def run_framework_checks(repo_root):
    violations = []
    violations += check_framework_statements(repo_root)
    return violations


def run_notices_checks(repo_root):
    notices_path = repo_root / 'NOTICES.md'
    if not notices_path.exists():
        return []
    pointer, carriers = parse_notices(notices_path)
    if pointer is None:
        return [('NOTICES.md', "pointer-unparseable NOTICES.md's Attribution pointer section yields no usable pointer definition")]

    violations = []
    valid_carriers = []
    for carrier in carriers:
        if not _carrier_is_repo_relative(carrier):
            violations.append((carrier, f"pointer-unparseable {carrier} is a required-carrier entry that is not a repository-relative path"))
            continue
        valid_carriers.append(carrier)

    violations += check_pointer(pointer, valid_carriers, repo_root)
    return violations


# ---------------------------------------------------------------------------
# skills/*/SKILL.md — frontmatter integrity (D-33)
#
# No general-purpose config-format parser exists in the standard library and
# none is added here (D-33). Only six top-level keys are ever legal, so a
# targeted extractor -- in parse_notices's style of finding a specific known
# shape line by line, not a general parser -- is sufficient.
# ---------------------------------------------------------------------------

ALLOWED_FRONTMATTER_KEYS = frozenset({
    'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools',
})
REQUIRED_FRONTMATTER_KEYS = frozenset({'name', 'description'})
DESCRIPTION_MIN = 200
DESCRIPTION_MAX = 1024
FRONTMATTER_DELIM = '---'

FRONTMATTER_KEY_RE = re.compile(r'^([A-Za-z][A-Za-z0-9_-]*):(.*)$')


def parse_frontmatter(path):
    """Parse the frontmatter block of a SKILL.md file with a targeted,
    stdlib-only extractor -- not a general-purpose parser. Returns
    (keys, problems): keys maps each column-zero key found to its value as
    a plain scalar, a `|` block scalar's joined body, or a nested map's raw
    indented text kept as an opaque string (the way parse_notices already
    keeps a fenced block's content opaque). problems is a list of
    human-readable structural defects -- no opening delimiter at the file's
    first line, no closing delimiter, or a column-zero key repeated (kept
    at its FIRST value, never silently overwritten by a later one). Key
    order carries no meaning: the parser reads keys into a mapping and
    never depends on the order they appear in."""
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    problems = []

    if not lines or lines[0].strip() != FRONTMATTER_DELIM:
        problems.append(f"no `{FRONTMATTER_DELIM}` block at the file's first line")
        return {}, problems

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == FRONTMATTER_DELIM:
            end_idx = i
            break
    if end_idx is None:
        problems.append(f"unterminated frontmatter block (no closing `{FRONTMATTER_DELIM}`)")
        return {}, problems

    keys = {}
    current_key = None
    current_lines = []

    def _flush():
        if current_key is None:
            return
        value = '\n'.join(l.strip() for l in current_lines).strip()
        if current_key in keys:
            problems.append(f"repeated top-level key '{current_key}'")
        else:
            keys[current_key] = value

    for line in lines[1:end_idx]:
        m = FRONTMATTER_KEY_RE.match(line)
        if m:
            _flush()
            current_key = m.group(1)
            rest = m.group(2).strip()
            current_lines = [rest] if rest and rest != '|' else []
        else:
            if current_key is not None:
                current_lines.append(line)
    _flush()

    missing_required = sorted(k for k in REQUIRED_FRONTMATTER_KEYS if k not in keys)
    if missing_required:
        problems.append(f"missing required key(s): {', '.join(missing_required)}")

    return keys, problems


METADATA_VERSION_RE = re.compile(r'^version:\s*"?([^"\s]+)"?\s*$', re.MULTILINE)


def _skill_metadata_version(skill_path):
    """Return the version string a SKILL.md's frontmatter `metadata` block
    states, or None if the file has no `metadata` key or that key's opaque
    text has no `version:` sub-key. Built on parse_frontmatter, which keeps
    a nested map's value as opaque indented text (D-33) -- this applies one
    small, targeted regex over that opaque string rather than adding a
    general YAML parser."""
    keys, _ = parse_frontmatter(skill_path)
    metadata_text = keys.get('metadata', '')
    m = METADATA_VERSION_RE.search(metadata_text)
    return m.group(1) if m else None


def _load_json_manifest(repo_root, rel_path):
    """Load a .claude-plugin/*.json manifest with stdlib json only -- these
    are genuine JSON files, unlike SKILL.md's hand-parsed frontmatter, so no
    targeted extractor is needed here. Returns (data, error): (None, None)
    when the file does not exist (absence is not a violation, matching this
    checker's established posture); (None, message) when the file exists
    but fails to parse as JSON or does not parse to a JSON object; (data,
    None) on success."""
    path = repo_root / rel_path
    if not path.exists():
        return None, None
    text = path.read_text(encoding='utf-8')
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        return None, f"{rel_path} is not valid JSON: {e}"
    if not isinstance(data, dict):
        return None, f"{rel_path} does not parse to a JSON object"
    return data, None


def _collapse_whitespace(text):
    return ' '.join(text.split())


def check_frontmatter(repo_root):
    violations = []
    for skill_path in sorted(repo_root.glob(SKILL_GLOB)):
        rel = skill_path.relative_to(repo_root)
        keys, problems = parse_frontmatter(skill_path)

        for problem in problems:
            violations.append((str(rel), f"frontmatter-unparseable {rel} {problem}"))

        for key in keys:
            if key not in ALLOWED_FRONTMATTER_KEYS:
                violations.append((str(rel), f"frontmatter-unknown-key {rel} declares unknown key '{key}'"))

        if 'name' in keys:
            name_value = keys['name']
            dir_name = skill_path.parent.name
            if name_value != dir_name:
                violations.append((str(rel), f"frontmatter-name-mismatch {rel} name '{name_value}' differs from parent directory '{dir_name}'"))

        if 'description' in keys:
            description = _collapse_whitespace(keys['description'])
            desc_len = len(description)
            if desc_len == 0:
                violations.append((str(rel), f"frontmatter-description-invalid {rel} description is empty after whitespace collapse"))
            elif desc_len < DESCRIPTION_MIN:
                violations.append((str(rel), f"frontmatter-description-invalid {rel} description length {desc_len} is below the {DESCRIPTION_MIN}-character floor"))
            elif desc_len > DESCRIPTION_MAX:
                violations.append((str(rel), f"frontmatter-description-invalid {rel} description length {desc_len} exceeds the {DESCRIPTION_MAX}-character ceiling"))
    return violations


FRONTMATTER_CHECK_CODES = [
    'frontmatter-unparseable', 'frontmatter-unknown-key',
    'frontmatter-name-mismatch', 'frontmatter-description-invalid',
]


def run_frontmatter_checks(repo_root):
    return check_frontmatter(repo_root)


# ---------------------------------------------------------------------------
# Skill catalog ID-set integrity (D-32) -- closes the drift a third file
# holding PF IDs (references/checklist.md) can create: an ID registered in
# NUMBERING.md's Allocated IDs table but missing from the checklist, or a
# rule heading defined in SKILL.md with no registry row at all.
# ---------------------------------------------------------------------------

RULE_HEADING_RE = re.compile(r'^### (PF-\d+\.\d+) — ')
MC_HEADING_RE = re.compile(r'^### (MC-\d+) — ')


def parse_skill_catalog(path):
    """Return the ordered list of PF IDs a SKILL.md *defines* via its rule
    headings. This is distinct from the citation tokens check_undefined_id
    already scans for -- a heading defines a rule, a bracketed marker or a
    prose reference only cites one."""
    text = strip_fences(path.read_text(encoding='utf-8'))
    ids = []
    for line in text.splitlines():
        m = RULE_HEADING_RE.match(line)
        if m:
            ids.append(m.group(1))
    return ids


def parse_completeness_audit(path):
    """Return the ordered list of MC IDs a references/completeness-audit.md
    *defines* via its rule headings, mirroring parse_skill_catalog's shape
    but pointed at the MC reference file instead of SKILL.md. A heading
    defines a rule; a bracketed marker or a prose reference only cites one,
    and check_undefined_id already owns citations."""
    text = strip_fences(path.read_text(encoding='utf-8'))
    ids = []
    for line in text.splitlines():
        m = MC_HEADING_RE.match(line)
        if m:
            ids.append(m.group(1))
    return ids


def parse_checklist(path, section_name='PF rules'):
    """Return the IDs listed in a references/checklist.md's named section's
    table, built on the same split_sections/table_rows pair every other
    parser in this file reuses rather than a second table reader. The
    section_name default ('PF rules') preserves every existing call site's
    behaviour unchanged; the MC call site passes 'MC rules' explicitly."""
    text = path.read_text(encoding='utf-8')
    sections = split_sections(text)
    ids = []
    for row in table_rows(sections.get(section_name, '')):
        if row and row[0]:
            ids.append(row[0].strip())
    return ids


def _three_way_id_diff(code, sets_by_label):
    """Shared three-way divergence comparison behind both
    check_catalog_id_drift (PF) and check_mc_catalog_id_drift (MC).
    sets_by_label is an ordered sequence of exactly three (label, id_set)
    pairs. Returns one (id, message) tuple per ID that is not present in
    all three sets, naming which labels it is present in and which it is
    missing from -- the same comparison shape and message wording
    check_catalog_id_drift has always produced, now shared by construction
    rather than by copy-paste, so a future rule about definitional
    agreement cannot be fixed in one namespace and silently drift from the
    other."""
    all_ids = set()
    for _, id_set in sets_by_label:
        all_ids |= id_set
    violations = []
    for id_ in sorted(all_ids):
        presence = [(label, id_ in id_set) for label, id_set in sets_by_label]
        if all(present for _, present in presence):
            continue
        present_in = [label for label, present in presence if present]
        missing_from = [label for label, present in presence if not present]
        violations.append((
            id_,
            f"{code} {id_} is present in {', '.join(present_in)} "
            f"but missing from {', '.join(missing_from)}",
        ))
    return violations


def check_catalog_id_drift(allocated, repo_root):
    """Compare three sets per installed skill folder: the PF subset of
    NUMBERING.md's Allocated IDs, the SKILL.md's defined-heading IDs, and
    references/checklist.md's listed rows. Report one violation per
    divergent ID, naming the files it is inconsistent between. Absence is
    not failure: a repo with no path matching SKILL_GLOB returns no
    violations, matching this checker's established posture."""
    violations = []
    skill_paths = sorted(repo_root.glob(SKILL_GLOB))
    if not skill_paths:
        return violations

    numbering_pf_ids = {row['id'] for row in allocated if PF_ID_RE.match(row['id'])}

    for skill_path in skill_paths:
        skill_rel = skill_path.relative_to(repo_root)
        skill_ids = set(parse_skill_catalog(skill_path))

        checklist_path = skill_path.parent / 'references' / 'checklist.md'
        checklist_rel = checklist_path.relative_to(repo_root)
        checklist_ids = set(parse_checklist(checklist_path)) if checklist_path.exists() else set()

        violations += _three_way_id_diff(
            'catalog-id-drift',
            [
                ('NUMBERING.md', numbering_pf_ids),
                (str(skill_rel), skill_ids),
                (str(checklist_rel), checklist_ids),
            ],
        )
    return violations


def check_mc_catalog_id_drift(allocated, repo_root):
    """Compare three sets per installed skill folder: the MC subset of
    NUMBERING.md's Allocated IDs, references/completeness-audit.md's
    defined-heading IDs, and references/checklist.md's '## MC rules'
    listed rows -- the MC-namespace sibling of check_catalog_id_drift,
    sharing its comparison body via _three_way_id_diff.

    Absence is not failure: if a skill folder has no
    references/completeness-audit.md, this function reports no violations
    for that folder, before computing any set. This early return is
    required, not optional: _good_numbering() (the fixture behind most
    self-test roots, and several other roots below it) already allocates
    MC-1 and MC-5 with no completeness-audit.md anywhere in those roots,
    so an implementation without this guard would report "allocated in
    NUMBERING.md, missing from the other two" and fire on every one of
    those known-good fixtures, breaking the whole self-test suite.
    Declared ceiling: like catalog-id-drift, this check compares ID sets
    only -- it says nothing about whether a cited MC-# token is valid,
    which is undefined-id's job."""
    violations = []
    skill_paths = sorted(repo_root.glob(SKILL_GLOB))
    if not skill_paths:
        return violations

    numbering_mc_ids = {row['id'] for row in allocated if MC_ID_RE.match(row['id'])}

    for skill_path in skill_paths:
        audit_path = skill_path.parent / 'references' / 'completeness-audit.md'
        if not audit_path.exists():
            continue
        audit_rel = audit_path.relative_to(repo_root)
        audit_ids = set(parse_completeness_audit(audit_path))

        checklist_path = skill_path.parent / 'references' / 'checklist.md'
        checklist_rel = checklist_path.relative_to(repo_root)
        checklist_ids = (
            set(parse_checklist(checklist_path, 'MC rules'))
            if checklist_path.exists() else set()
        )

        violations += _three_way_id_diff(
            'mc-catalog-id-drift',
            [
                ('NUMBERING.md', numbering_mc_ids),
                (str(audit_rel), audit_ids),
                (str(checklist_rel), checklist_ids),
            ],
        )
    return violations


def check_mc_rule_in_skill(repo_root):
    """Scan each skills/*/SKILL.md for a line matching the MC heading
    shape and emit one violation per match, naming the file and the ID.
    AUD-02 requires every MC rule to be defined in
    references/completeness-audit.md, never blended into the prose
    catalog; this turns that requirement into a build failure instead of
    a convention -- the structural half of AUD-02 that mc-catalog-id-drift
    does not cover, since that check never reads SKILL.md at all. Declared
    ceiling: this matches heading shape only -- it cannot distinguish a
    genuine rule definition from a heading that merely happens to look
    like one."""
    violations = []
    for skill_path in sorted(repo_root.glob(SKILL_GLOB)):
        rel = skill_path.relative_to(repo_root)
        text = strip_fences(skill_path.read_text(encoding='utf-8'))
        for line in text.splitlines():
            m = MC_HEADING_RE.match(line)
            if m:
                mc_id = m.group(1)
                violations.append((str(rel), (
                    f"mc-rule-in-skill {rel} defines {mc_id} via a rule heading, "
                    f"but AUD-02 requires every MC rule to be defined in "
                    f"references/completeness-audit.md, never blended into the prose catalog"
                )))
    return violations


# ---------------------------------------------------------------------------
# skills/*/SKILL.md — stated rule count vs registry (D-32)
# ---------------------------------------------------------------------------

COUNT_SENTENCE_RE = re.compile(r'^This catalog contains (\d+) rules in (\d+) numbered sections\.$')
MC_COUNT_SENTENCE_RE = re.compile(r'^This audit contains (\d+) checks across (\d+) dimensions\.$')


def check_catalog_count(allocated, repo_root):
    """For each skill file, require exactly the frozen stated-count
    template and require its two numbers to match the registry: the count
    of PF rows in the Allocated IDs table, and the count of distinct PF
    sections among those rows. Absence of the file is not a violation."""
    violations = []
    pf_ids = {row['id'] for row in allocated if PF_ID_RE.match(row['id'])}
    registry_rule_count = len(pf_ids)
    registry_section_count = len({PF_ID_RE.match(id_).group(1) for id_ in pf_ids})

    for skill_path in sorted(repo_root.glob(SKILL_GLOB)):
        rel = skill_path.relative_to(repo_root)
        text = skill_path.read_text(encoding='utf-8')
        stated = None
        for line in text.splitlines():
            m = COUNT_SENTENCE_RE.match(line.strip())
            if m:
                stated = (int(m.group(1)), int(m.group(2)))
                break
        if stated is None:
            violations.append((str(rel), f"catalog-count-unstated {rel} contains no line matching the frozen stated-count template"))
            continue
        stated_rules, stated_sections = stated
        if stated_rules != registry_rule_count or stated_sections != registry_section_count:
            violations.append((str(rel), (
                f"catalog-count-mismatch {rel} states {stated_rules} rules in {stated_sections} numbered sections, "
                f"but the registry has {registry_rule_count} rules in {registry_section_count} numbered sections"
            )))
    return violations


def check_mc_count(allocated, repo_root, mc_ranges):
    """For each skill folder found through SKILL_GLOB, locate
    references/completeness-audit.md and, when it exists, require the
    frozen MC stated-count template and require its two numbers to match
    the registry: the count of MC rows in NUMBERING.md's Allocated IDs
    table, and the count of distinct MC dimension blocks (from
    parse_numbering's mc_ranges) those rows fall into.

    Absence of completeness-audit.md is not a violation, checked before any
    set is computed for that folder -- the same declared ceiling
    mc-catalog-id-drift and mc-rule-in-skill both carry, and required for
    the same reason: no existing self-test fixture root that reaches this
    function ships that file, so an unguarded implementation would report
    every one of those roots as unstated and break --self-test."""
    violations = []
    mc_ids = {row['id'] for row in allocated if MC_ID_RE.match(row['id'])}
    registry_check_count = len(mc_ids)
    dims_hit = set()
    for id_ in mc_ids:
        n = int(MC_ID_RE.match(id_).group(1))
        for dimension, (low, high) in mc_ranges.items():
            if low <= n <= high:
                dims_hit.add(dimension)
    registry_dimension_count = len(dims_hit)

    for skill_path in sorted(repo_root.glob(SKILL_GLOB)):
        audit_path = skill_path.parent / 'references' / 'completeness-audit.md'
        if not audit_path.exists():
            continue
        rel = audit_path.relative_to(repo_root)
        text = audit_path.read_text(encoding='utf-8')
        stated = None
        for line in text.splitlines():
            m = MC_COUNT_SENTENCE_RE.match(line.strip())
            if m:
                stated = (int(m.group(1)), int(m.group(2)))
                break
        if stated is None:
            violations.append((str(rel), f"mc-count-unstated {rel} contains no line matching the frozen MC stated-count template"))
            continue
        stated_checks, stated_dimensions = stated
        if stated_checks != registry_check_count or stated_dimensions != registry_dimension_count:
            violations.append((str(rel), (
                f"mc-count-mismatch {rel} states {stated_checks} checks across {stated_dimensions} dimensions, "
                f"but the registry has {registry_check_count} checks across {registry_dimension_count} dimensions"
            )))
    return violations


# ---------------------------------------------------------------------------
# Artifact-family section presence (P3-08) -- the four frozen artifact-family
# section headings in references/artifact-patterns.md are a build-enforced
# structure, not a convention: SKILL.md's classification instruction, Phase
# 4's committed examples, and Phase 5's linter all read them verbatim.
# ---------------------------------------------------------------------------

ARTIFACT_FAMILY_SECTIONS = (
    # Frozen interface (P3-11) -- do not reword, re-case, pluralise, or
    # reorder these four strings. SKILL.md's classification instruction,
    # Phase 4's committed before/after examples, and Phase 5's linter all
    # bind to them exactly as written here.
    'RFP and RFI response',
    'Solution proposal',
    'Executive summary',
    'Demo and discovery material',
)

ARTIFACT_FAMILY_REQUIREMENT = {
    'RFP and RFI response': 'ART-01',
    'Solution proposal': 'ART-02',
    'Executive summary': 'ART-03',
    'Demo and discovery material': 'ART-04',
}


def check_artifact_family_sections(repo_root):
    """For each installed skill folder (a path matching skills/*/SKILL.md)
    whose references/artifact-patterns.md exists, require all four frozen
    artifact-family section headings in ARTIFACT_FAMILY_SECTIONS to be
    present, firing once per missing heading and naming the file, the
    missing heading, and the requirement clause (ART-01..04) that family's
    section carries.

    Return no violations for a folder whose references/artifact-patterns.md
    does not exist, checked before any read -- the same declared ceiling
    mc-catalog-id-drift, mc-rule-in-skill, and mc-count all share: no
    existing self-test fixture root ships that file, so an unguarded
    implementation would fire on every one of them and disable the whole
    suite.

    Declared ceiling: this check is heading presence only. It says nothing
    about whether a section's content is correct or complete, and it does
    not check that each section carries exactly one **Order:** line or that
    the fourteen frozen element labels are present -- that parity is
    enforced at plan level, the same way the rule-heading-versus-**Replace
    with:**-count parity is. Fourteen under the rule 03-03-PLAN.md's own
    verification command applies, stated here because "element label" is
    defined in no committed file: the bold `**Label:**` lines that are not
    **Order:** lines -- thirteen inside the four family sections plus
    **No family fits:** in the classification section. The file carries
    eighteen bold labels in total; the other four are the **Order:** lines
    this sentence counts separately. Corrected 06-09: both this docstring
    and the catalogue entry said "fifteen", which is reachable under no
    rule and never was -- the same 18/4/13 split held at 6bc2dab, where the
    sentence was written. The miscount is inherited: 03-03-PLAN.md's prose
    says fifteen while its own verification command lists fourteen.

    It also emits no violation for an extra section the file also contains:
    the classification section and the closing refusal section are both
    legitimate and neither is a family."""
    violations = []
    for skill_path in sorted(repo_root.glob(SKILL_GLOB)):
        patterns_path = skill_path.parent / 'references' / 'artifact-patterns.md'
        if not patterns_path.exists():
            continue
        rel = patterns_path.relative_to(repo_root)
        text = strip_fences(patterns_path.read_text(encoding='utf-8'))
        sections = split_sections(text)
        for heading in ARTIFACT_FAMILY_SECTIONS:
            if heading not in sections:
                requirement = ARTIFACT_FAMILY_REQUIREMENT[heading]
                violations.append((str(rel), (
                    f"artifact-family-section-missing {rel} is missing the "
                    f"required '## {heading}' section, which {requirement} requires"
                )))
    return violations


def check_skill_family_line_gate(repo_root):
    """For each installed skill folder (a path matching SKILL_GLOB) whose
    '## Self-check before delivering' section is present, require that
    section's body to name both anchors MOD-04's family-line gate depends
    on: the phrase naming the artifact family, and the literal no-family
    value 'No family fits', spelled exactly as
    references/artifact-patterns.md spells it. Both anchors are matched
    case-insensitively (03-REVIEW.md WR-02): its sibling
    check_skill_family_order_gate() already matches its own two anchors
    case-insensitively, and two checks asserting the same class of
    instruction is still present must not disagree about whether a
    capitalization-only rewording breaks one of them. Fires once per
    missing anchor, naming the file and which anchor is missing.

    Return no violations for a skill folder with no self-check section at
    all -- the declared ceiling, required so every pre-existing synthetic
    _good_skill() fixture (none of which defines this section) stays
    silent and the whole suite is not disabled.

    Declared ceiling: this check asserts the instruction text is present.
    It cannot assert a live session obeys it -- that is a model-behaviour
    property no file-reading checker observes;
    evals/conformance/run_conformance.py is the instrument for that. Its
    passing does not mean MOD-04 is mechanically verified."""
    violations = []
    for skill_path in sorted(repo_root.glob(SKILL_GLOB)):
        rel = skill_path.relative_to(repo_root)
        text = strip_fences(skill_path.read_text(encoding='utf-8'))
        sections = split_sections(text)
        body = sections.get('Self-check before delivering')
        if body is None:
            continue
        body_lower = body.lower()
        missing = []
        if 'artifact family' not in body_lower:
            missing.append('the phrase naming the artifact family')
        if 'no family fits' not in body_lower:
            missing.append("the 'No family fits' value")
        for item in missing:
            violations.append((str(rel), (
                f"skill-family-line-gate-missing {rel}'s self-check section is present but "
                f"is missing {item}, an anchor MOD-04's family-line gate requires"
            )))
    return violations


def check_skill_family_order_gate(repo_root):
    """For each installed skill folder (a path matching SKILL_GLOB) whose
    '## Self-check before delivering' section is present, require that
    section's body to name both anchors the ordering gate depends on: the
    literal 're-scan' and the literal 'before any rule marker', matched
    case-insensitively. This is the sibling of
    check_skill_family_line_gate(), extended from presence of the family
    line to its position ahead of any rule marker -- the residual failure
    mode (rule-before-family) 03-08 measured after the presence-only gate
    was already satisfied. Fires once per missing anchor, naming the file
    and which anchor is missing.

    Return no violations for a skill folder with no self-check section at
    all -- the same declared ceiling its sibling uses, required so every
    pre-existing synthetic _good_skill() fixture (none of which defines
    this section) stays silent and the whole suite is not disabled.

    Declared ceiling: this check asserts the instruction text is present.
    It cannot assert a live session obeys it -- that is a model-behaviour
    property no file-reading checker observes;
    evals/conformance/run_conformance.py is the instrument for that. Its
    passing does not mean MOD-04 is mechanically verified."""
    violations = []
    for skill_path in sorted(repo_root.glob(SKILL_GLOB)):
        rel = skill_path.relative_to(repo_root)
        text = strip_fences(skill_path.read_text(encoding='utf-8'))
        sections = split_sections(text)
        body = sections.get('Self-check before delivering')
        if body is None:
            continue
        body_lower = body.lower()
        missing = []
        if 're-scan' not in body_lower:
            missing.append("the 're-scan' instruction")
        if 'before any rule marker' not in body_lower:
            missing.append("the 'before any rule marker' ordering phrase")
        for item in missing:
            violations.append((str(rel), (
                f"skill-family-order-gate-missing {rel}'s self-check section is present but "
                f"is missing {item}, an anchor the ordering gate requires"
            )))
    return violations


SOURCE_COINED_LABELS = (
    # Frozen list (03-07 GAP B). Seven entries: four two-word labels, two
    # single-word labels, and one single-word label ('pain') matched with
    # an optional plural -- see _source_label_pattern. The ordinary-English
    # word for a measurement ('metric') is deliberately excluded; see this
    # module's docstring.
    'economic buyer',
    'paper process',
    'decision criteria',
    'decision process',
    'champion',
    'competition',
    'pain',
)

_SOURCE_LABEL_PLURALIZABLE = frozenset({'pain'})


def _source_label_pattern(label):
    escaped = re.escape(label)
    if label in _SOURCE_LABEL_PLURALIZABLE:
        escaped += 's?'
    return re.compile(r'\b' + escaped + r'\b', re.IGNORECASE)


def check_source_label_in_skill_content(repo_root):
    """For each file matching SKILL_GLOB, and each references/*.md beside
    it, scan case-insensitively with word boundaries for every label in
    SOURCE_COINED_LABELS. Fire once per file-and-label pair, naming the
    relative path, the label, and the first line number where it occurs.

    Declared ceilings -- see this module's docstring for the full
    statement: (1) literal-string scan, not the semantic paraphrase
    judgement SOURCES.md states no tool in this stack performs; (2) the
    ordinary-English word for a measurement is deliberately excluded from
    the list; (3) scans shipped skill content only -- NUMBERING.md's
    frozen registry labels are out of scope (.planning/WINDOWS.md entry 6,
    Phase 6 LEG-04)."""
    violations = []
    for skill_path in sorted(repo_root.glob(SKILL_GLOB)):
        skill_dir = skill_path.parent
        candidates = [skill_path]
        refs_dir = skill_dir / 'references'
        if refs_dir.exists():
            candidates += sorted(refs_dir.glob('*.md'))
        for path in candidates:
            rel = path.relative_to(repo_root)
            text = strip_fences(path.read_text(encoding='utf-8'))
            lines = text.splitlines()
            for label in SOURCE_COINED_LABELS:
                pattern = _source_label_pattern(label)
                for lineno, line in enumerate(lines, start=1):
                    if pattern.search(line):
                        violations.append((str(rel), (
                            f"source-label-in-skill-content {rel}:{lineno} uses the frozen "
                            f"source-coined label '{label}', adopted here as this repository's "
                            f"own unattributed noun (see SOURCES.md's reproduction-boundary clause)"
                        )))
                        break
    return violations


def check_catalog_opening_rule_count(allocated, repo_root):
    """Enforce that PF-0 (Opening / Reframe section) has exactly one allocated
    ID, closing CAT-03. The Before-scenario / Identify-Pain / Reframe
    convergence must resolve into a single instruction, never multiple rules
    the writer must reconcile. This check fires if any allocated row's ID
    starts with 'PF-0.' but the count is not exactly 1."""
    violations = []
    pf0_ids = [row['id'] for row in allocated if row['id'].startswith('PF-0.')]

    if len(pf0_ids) != 1:
        violations.append((
            'PF-0',
            f"catalog-opening-rule-count PF-0 section has {len(pf0_ids)} allocated IDs, "
            f"but CAT-03 requires exactly 1 (Writer must get one opening rule resolving "
            f"the Before-scenario / Identify-Pain / Reframe convergence)"
        ))

    # Also verify the checklist has exactly one PF-0.x row for consistency
    checklist_path = repo_root / 'skills' / 'proof-first' / 'references' / 'checklist.md'
    if checklist_path.exists():
        checklist_ids = parse_checklist(checklist_path)
        pf0_checklist = [id_ for id_ in checklist_ids if id_.startswith('PF-0.')]
        if len(pf0_checklist) != 1:
            violations.append((
                'PF-0',
                f"catalog-opening-rule-count references/checklist.md has {len(pf0_checklist)} PF-0 rows, "
                f"but exactly 1 is required for consistency with the Opening section"
            ))

    return violations


# ---------------------------------------------------------------------------
# skills/*/SKILL.md — progressive-disclosure ceiling (CAT-08)
# ---------------------------------------------------------------------------

SKILL_LINE_CEILING = 500


def check_skill_too_long(repo_root):
    violations = []
    for skill_path in sorted(repo_root.glob(SKILL_GLOB)):
        rel = skill_path.relative_to(repo_root)
        line_count = len(skill_path.read_text(encoding='utf-8').splitlines())
        if line_count > SKILL_LINE_CEILING:
            violations.append((str(rel), f"skill-too-long {rel} has {line_count} lines, exceeding the {SKILL_LINE_CEILING}-line ceiling"))
    return violations


# Word-to-token ratio calibrated against the sibling skill's own measured
# shape (02-RESEARCH.md: simple-english/SKILL.md measures 3,664 words,
# recorded as comfortably under the ~5,000-token ceiling this constant also
# enforces here). See this module's docstring for the full derivation.
SKILL_TOKEN_WORDS_PER_TOKEN_RATIO = 1.3
SKILL_TOKEN_CEILING = 5000


def check_skill_token_budget(repo_root):
    """Estimate each skill file's token count as word_count * the ratio
    above and fire when the estimate exceeds SKILL_TOKEN_CEILING. See this
    module's docstring for the declared ceiling of this estimate."""
    violations = []
    for skill_path in sorted(repo_root.glob(SKILL_GLOB)):
        rel = skill_path.relative_to(repo_root)
        text = skill_path.read_text(encoding='utf-8')
        word_count = len(text.split())
        estimated_tokens = int(word_count * SKILL_TOKEN_WORDS_PER_TOKEN_RATIO)
        if estimated_tokens > SKILL_TOKEN_CEILING:
            violations.append((str(rel), (
                f"skill-token-budget-exceeded {rel} is estimated at {estimated_tokens} tokens "
                f"({word_count} words x {SKILL_TOKEN_WORDS_PER_TOKEN_RATIO}), "
                f"exceeding the {SKILL_TOKEN_CEILING}-token ceiling"
            )))
    return violations


CATALOG_CHECK_CODES = [
    'catalog-id-drift', 'catalog-count-unstated', 'catalog-count-mismatch',
    'catalog-opening-rule-count', 'skill-too-long', 'skill-token-budget-exceeded',
    'mc-catalog-id-drift', 'mc-rule-in-skill', 'mc-count-unstated', 'mc-count-mismatch',
    'artifact-family-section-missing', 'skill-family-line-gate-missing',
    'skill-family-order-gate-missing', 'source-label-in-skill-content',
]


def run_catalog_checks(repo_root):
    numbering_path = repo_root / 'NUMBERING.md'
    if not numbering_path.exists():
        return []
    data = parse_numbering(numbering_path)
    violations = []
    violations += check_catalog_id_drift(data['allocated'], repo_root)
    violations += check_catalog_count(data['allocated'], repo_root)
    violations += check_catalog_opening_rule_count(data['allocated'], repo_root)
    violations += check_skill_too_long(repo_root)
    violations += check_skill_token_budget(repo_root)
    violations += check_mc_catalog_id_drift(data['allocated'], repo_root)
    violations += check_mc_rule_in_skill(repo_root)
    violations += check_mc_count(data['allocated'], repo_root, data['mc_ranges'])
    violations += check_artifact_family_sections(repo_root)
    violations += check_skill_family_line_gate(repo_root)
    violations += check_skill_family_order_gate(repo_root)
    violations += check_source_label_in_skill_content(repo_root)
    return violations


# ---------------------------------------------------------------------------
# examples/before-after.md -- EX-02's family coverage and citation guarantee
# (Phase 4, 04-02). Reuses ARTIFACT_FAMILY_SECTIONS (declared above) rather
# than a second typed copy of the four frozen family strings.
# ---------------------------------------------------------------------------

def check_before_after_families(repo_root):
    """For BEFORE_AFTER_PATH, if it exists, require all four frozen
    ARTIFACT_FAMILY_SECTIONS headings to be present; require each present
    heading's body to carry at least one line starting with the
    ballot-cross character ('✗') and at least one line starting with
    the check character ('✓'); and, only once all four headings are
    present, require them to appear in the file in exactly
    ARTIFACT_FAMILY_SECTIONS' own order. Returns an empty list before any
    read when BEFORE_AFTER_PATH does not exist.

    Declared ceiling: this is heading presence, ✗/✓ line presence, and
    order only. It says nothing about whether a pair's before half is
    genuinely non-compliant, whether its after half is genuinely a
    rewrite rather than a restatement of the rule's own wording, or
    whether the rewrite obeys its family's stated ordering convention --
    those are semantic judgements this repository's stack does not
    perform, and they stay with end-of-phase UAT."""
    path = repo_root / BEFORE_AFTER_PATH
    if not path.exists():
        return []
    rel = path.relative_to(repo_root)
    text = strip_fences(path.read_text(encoding='utf-8'))
    sections = split_sections(text)
    violations = []

    for heading in ARTIFACT_FAMILY_SECTIONS:
        if heading not in sections:
            violations.append((str(rel), (
                f"before-after-family-missing {rel} is missing the required "
                f"'## {heading}' section, which EX-02 requires"
            )))
            continue
        body_lines = sections[heading].splitlines()
        if not any(l.startswith('✗') for l in body_lines):
            violations.append((str(rel), (
                f"before-after-family-missing {rel}'s '## {heading}' section is present but "
                f"carries no line beginning with ✗, which EX-02 requires"
            )))
        if not any(l.startswith('✓') for l in body_lines):
            violations.append((str(rel), (
                f"before-after-family-missing {rel}'s '## {heading}' section is present but "
                f"carries no line beginning with ✓, which EX-02 requires"
            )))

    # Ordering: read the raw heading line sequence, not split_sections'
    # unordered {heading: body} mapping.
    found_order = [m.group(1).strip() for m in re.finditer(r'^## (.+?)\s*$', text, re.M)]
    family_order_found = [h for h in found_order if h in ARTIFACT_FAMILY_SECTIONS]
    if (
        len(family_order_found) == len(ARTIFACT_FAMILY_SECTIONS)
        and set(family_order_found) == set(ARTIFACT_FAMILY_SECTIONS)
        and tuple(family_order_found) != ARTIFACT_FAMILY_SECTIONS
    ):
        violations.append((str(rel), (
            f"before-after-family-missing {rel}'s four family headings appear in the order "
            f"{family_order_found}, but EX-02 requires the order {list(ARTIFACT_FAMILY_SECTIONS)}"
        )))

    return violations


def check_before_after_citations(repo_root):
    """For BEFORE_AFTER_PATH, if it exists, require each present
    ARTIFACT_FAMILY_SECTIONS heading's body to carry at least one PF-#.# or
    MC-# token, using the same token shapes check_undefined_id already
    uses. Returns an empty list before any read when BEFORE_AFTER_PATH
    does not exist.

    Declared ceiling: it asserts that a citation exists somewhere in the
    section, not that the citation is textually adjacent to the sentence
    it justifies, nor that the cited rule is the correct one for that
    rewrite. Validity of the token itself is undefined-id's job; this
    check asserts presence only."""
    path = repo_root / BEFORE_AFTER_PATH
    if not path.exists():
        return []
    rel = path.relative_to(repo_root)
    text = strip_fences(path.read_text(encoding='utf-8'))
    sections = split_sections(text)
    violations = []
    for heading in ARTIFACT_FAMILY_SECTIONS:
        if heading not in sections:
            continue
        body = sections[heading]
        if not (re.search(r'PF-\d+\.\d+', body) or re.search(r'MC-\d+', body)):
            violations.append((str(rel), (
                f"before-after-citation-missing {rel}'s '## {heading}' section carries no "
                f"PF- or MC- rule citation, which EX-02 requires"
            )))
    return violations


def check_example_sentence_length(repo_root):
    """For each path in EXAMPLE_PROSE_PATHS that exists, require every ✓
    column sentence to obey PF-4.1's 25-word ceiling (PF41_WORD_CEILING).
    Returns an empty list before any read for a path that does not exist.

    Declared ceiling: only lines beginning with the check character are
    inspected -- a ✗ column is the deliberately non-compliant exhibit its
    pair exists to contrast against, and holding it to the rule would
    delete the contrast; bracketed marker spans are removed before
    counting, so a long marker never forces a split, a stated definition
    rather than an implied one; sentence boundaries are a period,
    question mark, or exclamation mark followed by whitespace, so an
    abbreviation carrying an internal period splits a sentence early and
    undercounts; and this check enforces PF-4.1 alone, saying nothing
    about PF-4.2's active voice, PF-4.3's modal discipline, or any other
    prose-mechanics rule."""
    violations = []
    for rel_path in EXAMPLE_PROSE_PATHS:
        path = repo_root / rel_path
        if not path.exists():
            continue
        rel = path.relative_to(repo_root)
        text = strip_fences(path.read_text(encoding='utf-8'))
        for line in text.splitlines():
            if not line.startswith('✓'):
                continue
            body = line[1:].strip()
            if body.startswith('"') and body.endswith('"') and len(body) >= 2:
                body = body[1:-1]
            body = MARKER_SPAN_RE.sub('', body)
            for sentence in SENTENCE_SPLIT_RE.split(body):
                words = sentence.split()
                if len(words) > PF41_WORD_CEILING:
                    prefix = ' '.join(words[:8])
                    violations.append((str(rel), (
                        f"example-sentence-length {rel} carries a {len(words)}-word "
                        f"sentence over PF-4.1's {PF41_WORD_CEILING}-word ceiling: "
                        f"\"{prefix} ...\""
                    )))
    return violations


def check_before_after_spelled_count(repo_root):
    """For BEFORE_AFTER_PATH, if it exists, require every ✗/✓ column line
    to write a count from two through twelve in digits, not words --
    routing every count through the digit-shaped Canonical figures
    interface unlisted-figure already reads, rather than letting a
    word-spelled count drift between examples undetected. Returns an
    empty list before any read when BEFORE_AFTER_PATH does not exist.

    Rationale: unlisted-figure inspects digit-shaped tokens only, so a
    count written as a word is structurally invisible to the Canonical
    figures interface. This is the word-spelled half of the bare-count
    hole unlisted-figure's own declared ceiling discloses; the digit
    half remains open. Declared ceiling: the scan is this one file's
    quoted lines only. examples/deal-brief.md is out of scope because
    the brief is the definition of what counts as invented, and a count
    it states is by construction not invented. Its prose carries spelled
    cardinals throughout, including a party name containing a number
    word, and none of them sits on a ✗ or ✓ line -- this check opens no
    file but BEFORE_AFTER_PATH. skills/** is out of scope because the
    same party name appears there and because a per-rule illustrative
    pair reads naturally with a spelled count -- 5 matches sit on ✗ or ✓
    lines across those files. A raw scan of their whole text finds far
    more, in ordinary prose this check never reads; the 5 is the
    mark-line count, which is the only one this scope decision turns
    on. One of them ("Nine", in the party name "Vantage Nine
    Consulting") is a proper noun the check's own two-token exemption
    would excuse even if the check applied to that path, leaving 4
    would-be violations. The proper-noun heuristic (matched word and
    the following word both capitalised) is two tokens wide and will
    therefore also exempt a cardinal that happens to end a sentence
    immediately before a capitalised sentence start."""
    path = repo_root / BEFORE_AFTER_PATH
    if not path.exists():
        return []
    rel = path.relative_to(repo_root)
    text = strip_fences(path.read_text(encoding='utf-8'))
    violations = []
    for line in text.splitlines():
        if not (line.startswith('✗') or line.startswith('✓')):
            continue
        for m in SPELLED_CARDINAL_RE.finditer(line):
            word = m.group(0)
            rest = line[m.end():].lstrip()
            next_word = rest.split(' ', 1)[0] if rest else ''
            if word[0:1].isupper() and next_word[0:1].isupper():
                continue
            prefix = ' '.join(line[1:].strip().split()[:8])
            violations.append((str(rel), (
                f"before-after-spelled-count {rel} names the word-spelled count "
                f"'{word}' instead of a digit: \"{prefix} ...\""
            )))
    return violations


def check_example_rule_narration(repo_root):
    """For each path in EXAMPLE_PROSE_PATHS that exists, fire on a ✓
    column line pairing a listed contrastive connective
    (NARRATION_CONNECTIVE_RE) with one of NARRATION_META_TERMS within
    NARRATION_WINDOW_CHARS characters of the connective -- one narration
    shape only, an explicitly disclosed proxy for SKILL.md line 261's
    "No list of applied rules follows the prose", never a verdict on it.
    Returns an empty list before any read for a path that does not
    exist. Fires at most once per line.

    Declared ceiling: it catches one narration shape only. It does not
    detect narration phrased as self-reference to the document's own
    ordering -- a sentence announcing that the answer stands first
    rather than simply placing it first carries no listed connective
    and is invisible here; that instance was found by an adversarial
    human-substitute read, was repaired by hand in 04-05, and remains a
    semantic judgement no code in this repository performs. It does not
    detect novel narration built from words absent from the frozen term
    list, the structural limit of any list-based proxy. It will report
    a legitimate technical contrast that happens to pair a listed
    connective with a listed term, and the repair in that case is to
    reword the example rather than to widen the list. It is a proxy for
    SKILL.md line 261, not a verdict on it; the verdict stays with
    end-of-phase UAT. Measured 2026-09-17: 4 of 4 ✓ columns in
    examples/before-after.md matched before the 04-05 repair, and 0 of
    28 in worked-examples.md."""
    violations = []
    for rel_path in EXAMPLE_PROSE_PATHS:
        path = repo_root / rel_path
        if not path.exists():
            continue
        rel = path.relative_to(repo_root)
        text = strip_fences(path.read_text(encoding='utf-8'))
        for line in text.splitlines():
            if not line.startswith('✓'):
                continue
            fired = False
            for m in NARRATION_CONNECTIVE_RE.finditer(line):
                window = line[m.end():m.end() + NARRATION_WINDOW_CHARS]
                for term in NARRATION_META_TERMS:
                    if term in window.lower():
                        prefix = ' '.join(line[1:].strip().split()[:8])
                        violations.append((str(rel), (
                            f"example-rule-narration {rel} pairs connective "
                            f"'{m.group(0)}' with meta term '{term}': \"{prefix} ...\""
                        )))
                        fired = True
                        break
                if fired:
                    break
    return violations


EXAMPLE_CHECK_CODES = [
    'before-after-family-missing', 'before-after-citation-missing',
    'example-sentence-length', 'before-after-spelled-count',
    'example-rule-narration',
]


def run_example_checks(repo_root):
    violations = []
    violations += check_before_after_families(repo_root)
    violations += check_before_after_citations(repo_root)
    violations += check_example_sentence_length(repo_root)
    violations += check_before_after_spelled_count(repo_root)
    violations += check_example_rule_narration(repo_root)
    return violations


# ---------------------------------------------------------------------------
# .claude-plugin/plugin.json and .claude-plugin/marketplace.json (Phase 4,
# 04-01) -- the Claude Code plugin distribution channel.
# ---------------------------------------------------------------------------

def check_plugin_manifest_version(repo_root):
    """Compare each existing plugin manifest's stated `version` against
    skills/proof-first/SKILL.md's frontmatter `metadata.version`, the
    source of truth NUMBERING.md already names for this obligation.
    Returns an empty list before any read when neither manifest exists.
    Fires once per manifest whose version disagrees with the skill's, and
    once per manifest when the skill states no version to compare against
    at all. A manifest that fails to parse as JSON is silently skipped
    here -- that is plugin-manifest-invalid's job, not this code's. Also
    fires once, independent of either manifest, when two or more shipped
    skills each state a metadata.version and those stated versions are
    not all equal, naming every disagreeing skill and its version.
    Declared ceiling: the manifest comparison above still resolves its
    single comparison value from the alphabetically first skill that
    states a version -- unchanged when exactly one skill states one, the
    live case -- so in a multi-skill repository a manifest could agree
    with that one skill and disagree with another without a
    manifest-level violation naming that disagreement; the skills'
    mutual disagreement is what fires instead, via the check just
    described."""
    plugin_exists = (repo_root / PLUGIN_MANIFEST_PATH).exists()
    marketplace_exists = (repo_root / MARKETPLACE_MANIFEST_PATH).exists()
    if not plugin_exists and not marketplace_exists:
        return []

    skill_versions = {}
    for skill_path in sorted(repo_root.glob(SKILL_GLOB)):
        v = _skill_metadata_version(skill_path)
        if v is not None:
            skill_versions[skill_path.parent.name] = v
    skill_version = next(iter(skill_versions.values()), None)

    violations = []

    plugin_data, plugin_error = _load_json_manifest(repo_root, PLUGIN_MANIFEST_PATH)
    if plugin_data is not None and plugin_error is None:
        manifest_version = plugin_data.get('version')
        if skill_version is None:
            violations.append((PLUGIN_MANIFEST_PATH, (
                f"plugin-manifest-version-mismatch {PLUGIN_MANIFEST_PATH} states version "
                f"'{manifest_version}', but no skills/*/SKILL.md states a metadata.version "
                f"to compare against"
            )))
        elif manifest_version != skill_version:
            violations.append((PLUGIN_MANIFEST_PATH, (
                f"plugin-manifest-version-mismatch {PLUGIN_MANIFEST_PATH} states version "
                f"'{manifest_version}', but the skill frontmatter states '{skill_version}'"
            )))

    marketplace_data, marketplace_error = _load_json_manifest(repo_root, MARKETPLACE_MANIFEST_PATH)
    if marketplace_data is not None and marketplace_error is None:
        plugins = marketplace_data.get('plugins')
        entry_version = None
        if isinstance(plugins, list) and plugins and isinstance(plugins[0], dict):
            entry_version = plugins[0].get('version')
        if skill_version is None:
            violations.append((MARKETPLACE_MANIFEST_PATH, (
                f"plugin-manifest-version-mismatch {MARKETPLACE_MANIFEST_PATH} states version "
                f"'{entry_version}', but no skills/*/SKILL.md states a metadata.version to "
                f"compare against"
            )))
        elif entry_version != skill_version:
            violations.append((MARKETPLACE_MANIFEST_PATH, (
                f"plugin-manifest-version-mismatch {MARKETPLACE_MANIFEST_PATH} states version "
                f"'{entry_version}', but the skill frontmatter states '{skill_version}'"
            )))

    if len(skill_versions) > 1 and len(set(skill_versions.values())) > 1:
        detail = ', '.join(
            f"{name} states '{v}'" for name, v in sorted(skill_versions.items())
        )
        violations.append((PLUGIN_MANIFEST_PATH, (
            f"plugin-manifest-version-mismatch shipped skills disagree on their own "
            f"metadata.version: {detail}"
        )))

    return violations


PLUGIN_REQUIRED_KEYS = (
    'name', 'displayName', 'description', 'version', 'author', 'homepage',
    'repository', 'license', 'keywords',
)
MARKETPLACE_REQUIRED_KEYS = ('name', 'owner', 'description', 'plugins')
MARKETPLACE_ENTRY_EQUAL_KEYS = ('description', 'displayName', 'author', 'license', 'keywords')


def check_plugin_manifest_invalid(repo_root):
    """Assert both plugin manifests are well-formed. `PLUGIN_REQUIRED_KEYS`
    presence is enforced at two positions: `plugin.json`'s top-level object
    and `marketplace.json`'s `plugins[0]` entry -- the object
    `claude plugin marketplace add` actually reads. Required-key presence
    at both positions is proven exhaustively by `--self-test`'s
    required-key coverage matrix -- one assertion per key per position, 18
    cells in all -- so the claim is verified rather than sampled by a
    single fixture. Also asserts plugin.json's `name` equal to the single
    shipped skill folder name, and marketplace.json's
    `owner`/`plugins`/`source` shape correct. Once both objects parse,
    `MARKETPLACE_ENTRY_EQUAL_KEYS` (`description`, `displayName`, `author`,
    `license`, `keywords`) must agree between the marketplace plugin entry
    and plugin.json's top-level object, compared only where the key is
    present on both sides -- presence is the required-key loop's job, so
    double-reporting one absence as two defects would mislead. `name` is
    excluded from that set because plugin.json's `name` is separately held
    equal to the shipped skill folder name, and `version` because
    `check_plugin_manifest_version` owns it. `homepage` and `repository`
    are deliberately excluded too: `check_publish_location_drift` owns
    them at owner-segment granularity, normalising the HTTPS, plaintext
    HTTP, scheme-less and SSH remote forms to the same owner, so the two
    manifests are permitted to write the same publish location in
    different syntaxes -- an exact-string equality check on those two
    fields would contradict that and misfire on a mixed-URL-form
    manifest pair that is otherwise correct. Returns an empty list before
    any read when neither manifest exists. Declared ceiling: the
    required-key loop, its matrix, and the equality guard all assert
    presence/agreement only -- no deeper value semantics, and nothing
    about whether a real `claude plugin marketplace add` succeeds. The
    folder-name equality check is verified only when exactly one skill
    folder matches SKILL_GLOB, the live case; when the repository ships
    zero or more than one skill folder while plugin.json states a `name`,
    the equality itself cannot be resolved against a single shipped
    skill, so this fires naming the ambiguity (how many skill folders
    were found) instead of silently skipping the check -- zero and
    multiple are reported with different wording, because zero means the
    manifest names a skill that is not there and multiple means it names
    one of several without saying which."""
    plugin_exists = (repo_root / PLUGIN_MANIFEST_PATH).exists()
    marketplace_exists = (repo_root / MARKETPLACE_MANIFEST_PATH).exists()
    if not plugin_exists and not marketplace_exists:
        return []

    violations = []

    plugin_data, plugin_error = _load_json_manifest(repo_root, PLUGIN_MANIFEST_PATH)
    if plugin_error:
        violations.append((PLUGIN_MANIFEST_PATH, f"plugin-manifest-invalid {plugin_error}"))
    elif plugin_data is not None:
        for key in PLUGIN_REQUIRED_KEYS:
            if key not in plugin_data:
                violations.append((PLUGIN_MANIFEST_PATH, (
                    f"plugin-manifest-invalid {PLUGIN_MANIFEST_PATH} is missing required key '{key}'"
                )))
        skill_dirs = sorted({p.parent.name for p in repo_root.glob(SKILL_GLOB)})
        if 'name' in plugin_data:
            name_value = plugin_data['name']
            if len(skill_dirs) == 1:
                skill_dir = skill_dirs[0]
                if name_value != skill_dir:
                    violations.append((PLUGIN_MANIFEST_PATH, (
                        f"plugin-manifest-invalid {PLUGIN_MANIFEST_PATH} name '{name_value}' "
                        f"differs from the shipped skill folder name '{skill_dir}'"
                    )))
            elif len(skill_dirs) == 0:
                violations.append((PLUGIN_MANIFEST_PATH, (
                    f"plugin-manifest-invalid {PLUGIN_MANIFEST_PATH} states name "
                    f"'{name_value}', but no skills/*/SKILL.md folder exists to check it against"
                )))
            else:
                violations.append((PLUGIN_MANIFEST_PATH, (
                    f"plugin-manifest-invalid {PLUGIN_MANIFEST_PATH} states name "
                    f"'{name_value}', but {len(skill_dirs)} skill folders exist "
                    f"({', '.join(skill_dirs)}) -- the name cannot be checked against a "
                    f"single shipped skill folder"
                )))

    marketplace_data, marketplace_error = _load_json_manifest(repo_root, MARKETPLACE_MANIFEST_PATH)
    if marketplace_error:
        violations.append((MARKETPLACE_MANIFEST_PATH, f"plugin-manifest-invalid {marketplace_error}"))
    elif marketplace_data is not None:
        for key in MARKETPLACE_REQUIRED_KEYS:
            if key not in marketplace_data:
                violations.append((MARKETPLACE_MANIFEST_PATH, (
                    f"plugin-manifest-invalid {MARKETPLACE_MANIFEST_PATH} is missing required key '{key}'"
                )))
        if 'owner' in marketplace_data:
            owner = marketplace_data['owner']
            if not isinstance(owner, dict) or not owner.get('name'):
                violations.append((MARKETPLACE_MANIFEST_PATH, (
                    f"plugin-manifest-invalid {MARKETPLACE_MANIFEST_PATH} 'owner' must be an "
                    f"object carrying a non-empty 'name'"
                )))
        if 'plugins' in marketplace_data:
            plugins = marketplace_data['plugins']
            if not isinstance(plugins, list) or len(plugins) != 1 or not isinstance(plugins[0], dict):
                violations.append((MARKETPLACE_MANIFEST_PATH, (
                    f"plugin-manifest-invalid {MARKETPLACE_MANIFEST_PATH} 'plugins' must be a "
                    f"list of exactly one object"
                )))
            else:
                entry = plugins[0]
                for key in PLUGIN_REQUIRED_KEYS:
                    if key not in entry:
                        violations.append((MARKETPLACE_MANIFEST_PATH, (
                            f"plugin-manifest-invalid {MARKETPLACE_MANIFEST_PATH}'s plugin "
                            f"entry is missing required key '{key}'"
                        )))
                if plugin_data is not None and not plugin_error:
                    for key in MARKETPLACE_ENTRY_EQUAL_KEYS:
                        if key in entry and key in plugin_data and entry[key] != plugin_data[key]:
                            violations.append((MARKETPLACE_MANIFEST_PATH, (
                                f"plugin-manifest-invalid {MARKETPLACE_MANIFEST_PATH}'s plugin "
                                f"entry '{key}' differs from {PLUGIN_MANIFEST_PATH}'s '{key}'"
                            )))
                source = entry.get('source')
                if source != './':
                    violations.append((MARKETPLACE_MANIFEST_PATH, (
                        f"plugin-manifest-invalid {MARKETPLACE_MANIFEST_PATH} plugin entry "
                        f"'source' is '{source}', not the required './'"
                    )))

    return violations


PUBLISH_LOCATION_CARRIERS = (PLUGIN_MANIFEST_PATH, MARKETPLACE_MANIFEST_PATH, 'README.md')

SKILLS_CLI_INSTALL_RE = re.compile(r'npx skills add ([^\s`]+)')
MARKETPLACE_ADD_RE = re.compile(r'claude plugin marketplace add ([^\s`]+)')
# Route 2's in-session form, which Claude Code's own slash command spells
# without the `claude` prefix. Kept as a separate pattern rather than
# folded into MARKETPLACE_ADD_RE because that regex is also
# check_readme_install_paths' route-2 anchor, where the CLI form is the
# text being asserted present; only publish-location-drift reads both.
IN_SESSION_MARKETPLACE_ADD_RE = re.compile(r'/plugin marketplace add ([^\s`]+)')


def _owner_segment(value):
    """Normalise one of four GitHub URL forms a contributor plausibly
    writes -- the HTTPS form (https://github.com/<owner>/<repo>), the
    plaintext HTTP form (http://github.com/<owner>/<repo>), the
    scheme-less form (github.com/<owner>/<repo>), and the SSH remote form
    (git@github.com:<owner>/<repo>.git, exactly as `git remote -v`
    prints it) -- then return the text before the first remaining '/',
    or the whole remainder if there is none: the GitHub account/org
    segment, the one granularity every carrier position (a full
    owner/repo URL, or owner.url's bare owner URL) can state. Tries each
    prefix in the order listed above and stops at the first hit, so a
    value already stripped is never stripped twice; after whichever
    prefix matched (or none), strips surrounding whitespace, a trailing
    slash, and a trailing '.git' suffix (the SSH form carries one, the
    HTTPS form usually does not -- left on, it would make the repository
    segment disagree between two forms of the same repository even once
    the owner agrees). Declared ceiling: this does not recognise a
    GitHub Enterprise or other self-hosted host, and it compares the
    owner segment only, so two carriers naming the same owner and
    different repositories are treated as agreeing -- the granularity
    check_publish_location_drift's own docstring already claims and this
    normalisation preserves rather than widens."""
    v = value
    for prefix in ('https://github.com/', 'http://github.com/', 'github.com/'):
        if v.startswith(prefix):
            v = v[len(prefix):]
            break
    else:
        ssh_prefix = 'git@github.com:'
        if v.startswith(ssh_prefix):
            v = v[len(ssh_prefix):]
    v = v.strip().rstrip('/')
    if v.endswith('.git'):
        v = v[:-len('.git')]
    return v.split('/', 1)[0] if v else v


def _publish_locations_in(repo_root, rel_path):
    """Return the set of distinct GitHub owner segments a single carrier
    states, read from structured positions only, never from a loose scan
    of every link in the file: for plugin.json, its `homepage` and
    `repository` values; for marketplace.json, its plugin entry's same two
    fields plus the top-level `owner.url`, which sits beside `plugins`
    rather than inside a plugin entry; for README.md, the argument
    following any of the literal command prefixes `npx skills add `,
    `claude plugin marketplace add ` and `/plugin marketplace add ` (route
    2's in-session form) on a line. Every position is reduced to its owner
    segment via _owner_segment. Returns an empty set when the carrier does
    not exist or states nothing at any of its positions."""
    if not (repo_root / rel_path).exists():
        return set()

    owners = set()

    if rel_path == PLUGIN_MANIFEST_PATH:
        data, error = _load_json_manifest(repo_root, rel_path)
        if data is not None and error is None:
            for field in ('homepage', 'repository'):
                value = data.get(field)
                if value:
                    owners.add(_owner_segment(value))
    elif rel_path == MARKETPLACE_MANIFEST_PATH:
        data, error = _load_json_manifest(repo_root, rel_path)
        if data is not None and error is None:
            plugins = data.get('plugins')
            if isinstance(plugins, list) and plugins and isinstance(plugins[0], dict):
                for field in ('homepage', 'repository'):
                    value = plugins[0].get(field)
                    if value:
                        owners.add(_owner_segment(value))
            owner = data.get('owner')
            if isinstance(owner, dict) and owner.get('url'):
                owners.add(_owner_segment(owner['url']))
    else:
        text = (repo_root / rel_path).read_text(encoding='utf-8')
        for m in SKILLS_CLI_INSTALL_RE.finditer(text):
            owners.add(_owner_segment(m.group(1)))
        for m in MARKETPLACE_ADD_RE.finditer(text):
            owners.add(_owner_segment(m.group(1)))
        for m in IN_SESSION_MARKETPLACE_ADD_RE.finditer(text):
            owners.add(_owner_segment(m.group(1)))

    return owners


# Carriers whose very existence structurally implies they should state a
# publish location once plugin-manifest-invalid's own required-key check
# passes (both manifests declare homepage/repository as required keys).
# README.md is not in this set: a README with no install command yet is
# silent, not violating (see the module docstring's publish-location-drift
# entry and the P4-05 decision this mirrors).
PUBLISH_LOCATION_REQUIRED_CARRIERS = (PLUGIN_MANIFEST_PATH, MARKETPLACE_MANIFEST_PATH)


def check_publish_location_drift(repo_root):
    """Assert every existing carrier in PUBLISH_LOCATION_CARRIERS states the
    same GitHub owner segment for this repository's publish location.
    Fires once naming a required carrier (a manifest) that exists but
    states none while another existing carrier states one, and once
    naming every carrier and the distinct owner segments they state when
    more than one distinct value exists across all non-empty carriers.
    Returns an empty list when no carrier exists, or when every existing
    carrier states nothing at all."""
    existing = {}
    for rel_path in PUBLISH_LOCATION_CARRIERS:
        if (repo_root / rel_path).exists():
            existing[rel_path] = _publish_locations_in(repo_root, rel_path)

    if not existing:
        return []

    non_empty = {p: o for p, o in existing.items() if o}
    if not non_empty:
        return []

    violations = []

    for rel_path in PUBLISH_LOCATION_REQUIRED_CARRIERS:
        if rel_path in existing and not existing[rel_path]:
            others = ', '.join(sorted(non_empty))
            violations.append((rel_path, (
                f"publish-location-drift {rel_path} exists but states no publish "
                f"location, while {others} does"
            )))

    all_owners = set()
    for owners in non_empty.values():
        all_owners |= owners
    if len(all_owners) > 1:
        detail = '; '.join(
            f"{p} states {', '.join(sorted(o))}" for p, o in sorted(non_empty.items())
        )
        violations.append((PUBLISH_LOCATION_CARRIERS[0], (
            f"publish-location-drift these carriers disagree on the repository's "
            f"publish location: {detail}"
        )))

    return violations


PLUGIN_CHECK_CODES = [
    'plugin-manifest-version-mismatch', 'plugin-manifest-invalid', 'publish-location-drift',
]


def run_plugin_checks(repo_root):
    violations = []
    violations += check_plugin_manifest_version(repo_root)
    violations += check_plugin_manifest_invalid(repo_root)
    violations += check_publish_location_drift(repo_root)
    return violations


# ---------------------------------------------------------------------------
# README.md -- install-path coverage and before/after ordering (Phase 4,
# 04-04). DIST-06's structural half: every promised install route has a
# stated anchor, and the before/after lead-in precedes both the install
# and the status sections. Defined here, after SKILLS_CLI_INSTALL_RE and
# MARKETPLACE_ADD_RE, because both new checks reuse those two module-level
# patterns rather than declaring a third copy of either command prefix.
# Both codes join README_CHECK_CODES / run_readme_checks() above, which
# already calls them by name (Python resolves module-level names at call
# time, not at def time) -- there is no fourth README aggregator.
# ---------------------------------------------------------------------------

# The output-style path literal, referenced both by README_INSTALL_ANCHORS'
# 'output style' entry below and by check_readme_output_style_destination
# further down, so this literal is typed once here rather than a second
# time as an inline duplicate (Phase 4, 04-13).
README_OUTPUT_STYLE_PATH = 'output-styles/proof-first.md'

# The two directories Claude Code scans for output styles: the user-level
# one and a project's own. Provenance: 04-UAT.md test 4,
# orchestrator-verified; the project-level form was corroborated again on
# 2026-09-21 by a driven interactive session whose /config picker listed a
# style installed into a project's own .claude/output-styles/
# (LEGAL-REVIEW.md, Human observations section 4). Phase 4 gave this
# environment's lack of live network access as the reason no documentation
# URL is cited here; that premise has since expired (ledger row 18) and no
# URL has been cited since. The project-level form is a substring of the
# user-level form ('.claude/output-styles/' sits inside
# '~/.claude/output-styles/'), so a README naming only the user-level
# directory already satisfies check_readme_output_style_destination for
# both, and a mutation targeting this fact must match on the shorter,
# project-level literal or it leaves the user-level sentence behind and
# stays inert (Phase 4, 04-13).
README_OUTPUT_STYLE_DESTINATIONS = ('~/.claude/output-styles/', '.claude/output-styles/')

README_INSTALL_ANCHORS = (
    ('skills CLI', SKILLS_CLI_INSTALL_RE),
    ('Claude Code marketplace', MARKETPLACE_ADD_RE),
    ('output style', README_OUTPUT_STYLE_PATH),
    ('system prompt', 'prompts/system-prompt.md'),
)

README_BEFORE_AFTER_HEADING = '## Before and after'
README_INSTALL_HEADING = '## Install'
README_STATUS_HEADING = '## Status'
README_LAYOUT_HEADING = '## Repository layout'

# The ✗/✓ column marker characters and the applied-rules footer prefix
# that open each footer line in both README.md's reproduced quotations
# and examples/before-after.md (Phase 4, 04-09 Task 1). The module
# already uses the raw '✗'/'✓' characters directly at several existing
# call sites with no shared constant; these three names exist because
# check_readme_example_drift below is a new call site that needs one
# shared definition rather than retyping the raw characters or the
# prefix string at each of its own comparisons.
README_CROSS_CHAR = '✗'
README_CHECK_CHAR = '✓'
README_APPLIED_RULES_PREFIX = 'Rules applied:'

# Frozen ceiling with deliberate margin (Phase 4, 04-09 Task 2): the
# measured pre-repair first-ballot-cross-line number was 23; the
# repaired file sits at or below 20. Raising this number is a
# deliberate weakening of DIST-06's lead-with-examples promise and
# should be argued for, not typed.
README_FIRST_EXAMPLE_MAX_LINE = 20


def check_readme_install_paths(repo_root):
    """For README.md, require each of README_INSTALL_ANCHORS' four route
    anchors to appear somewhere in the file: the skills-CLI command
    prefix (SKILLS_CLI_INSTALL_RE, reused rather than a second copy), the
    marketplace add command prefix (MARKETPLACE_ADD_RE, likewise reused),
    and the literal output-style and system-prompt paths. Reads
    README.md's raw text and never calls strip_fences: every anchor lives
    inside a fenced command block or a code span, and stripping fences
    would find none of them and pass silently on an empty README. Fires
    once per missing anchor. Returns an empty list before any read when
    README.md does not exist.

    Declared ceiling: this check asserts each route's identifying text
    appears somewhere in the file. It does not assert the command is
    correct, that it resolves, that its argument names a real
    repository, or that the four routes appear under the '## Install'
    heading rather than scattered elsewhere in the file --
    publish-location-drift owns the argument's consistency, and nothing
    in this repository owns the command's correctness until the
    repository is published."""
    violations = []
    readme_path = repo_root / 'README.md'
    if not readme_path.exists():
        return violations
    text = readme_path.read_text(encoding='utf-8')
    for label, matcher in README_INSTALL_ANCHORS:
        found = (matcher in text) if isinstance(matcher, str) else (matcher.search(text) is not None)
        if not found:
            violations.append(('README.md', (
                f"readme-install-path-missing README.md is missing the {label} install route, "
                f"which DIST-06 requires"
            )))
    return violations


def check_readme_before_after_order(repo_root):
    """For README.md, require README_BEFORE_AFTER_HEADING,
    README_INSTALL_HEADING, and README_STATUS_HEADING to each be present
    as an exact '## ' heading line, and -- only once all three are
    present -- require the before/after heading's line index to be lower
    than both the install and the status heading's line index. Fires once
    per absent heading, and once naming the order found and the order
    required when all three are present but out of order. Returns an
    empty list before any read when README.md does not exist.

    Declared ceiling: this check asserts heading presence and relative
    position only. It says nothing about whether the '## Before and
    after' section actually contains a pair, whether the pair is any
    good, or whether a reader experiences the file as leading with
    examples -- the first of those is before-after-family-missing's job
    over a different file, and the last two are manual judgments left to
    end-of-phase UAT."""
    violations = []
    readme_path = repo_root / 'README.md'
    if not readme_path.exists():
        return violations
    lines = readme_path.read_text(encoding='utf-8').splitlines()
    headings = (README_BEFORE_AFTER_HEADING, README_INSTALL_HEADING, README_STATUS_HEADING)
    indices = {}
    for heading in headings:
        for i, line in enumerate(lines):
            if line.strip() == heading:
                indices[heading] = i
                break
    missing = [h for h in headings if h not in indices]
    for heading in missing:
        violations.append(('README.md', (
            f"readme-before-after-order README.md is missing the required '{heading}' "
            f"heading, which DIST-06 requires"
        )))
    if not missing:
        ba_idx = indices[README_BEFORE_AFTER_HEADING]
        install_idx = indices[README_INSTALL_HEADING]
        status_idx = indices[README_STATUS_HEADING]
        if not (ba_idx < install_idx and ba_idx < status_idx):
            violations.append(('README.md', (
                f"readme-before-after-order README.md's '{README_BEFORE_AFTER_HEADING}' heading "
                f"(line {ba_idx + 1}) does not precede both '{README_INSTALL_HEADING}' "
                f"(line {install_idx + 1}) and '{README_STATUS_HEADING}' (line {status_idx + 1}); "
                f"DIST-06 requires before/after pairs to precede both sections"
            )))
    return violations


def check_readme_example_drift(repo_root):
    """Require every README.md line beginning with README_CROSS_CHAR,
    README_CHECK_CHAR, or README_APPLIED_RULES_PREFIX to be, character
    for character, a line of examples/before-after.md (BEFORE_AFTER_PATH).
    Reads both files raw, without calling strip_fences, for the same
    reason check_readme_install_paths gives: the reproduced lines are
    plain prose lines and fence-stripping would change what is compared.
    Returns an empty list before any read when either README.md or
    BEFORE_AFTER_PATH does not exist -- both files are required for the
    comparison to mean anything. Fires once per README line with no
    match, naming the line number and a short prefix of the line's text.

    Declared ceiling: comparison is whole-line code-point equality with
    no Unicode normalisation, no case folding, and no whitespace
    collapsing -- the same convention pointer-missing already states --
    so a reproduction differing only in an invisible code point is
    reported as drift, which is the intended direction. It asserts
    membership, not position or completeness: README may reproduce one
    pair, four pairs, or none at all, and may reproduce a check line
    without its ballot-cross line; this check says nothing about which
    pair README chose or whether the pair is whole. It does not compare
    the surrounding prose, the family label, or the link line. And it
    asserts nothing in the opposite direction: a line present in
    examples/before-after.md and absent from README is not a violation,
    because README is a lead-in and is not required to reproduce
    everything."""
    readme_path = repo_root / 'README.md'
    before_after_path = repo_root / BEFORE_AFTER_PATH
    if not readme_path.exists() or not before_after_path.exists():
        return []
    rel = readme_path.relative_to(repo_root)
    before_after_lines = set(before_after_path.read_text(encoding='utf-8').splitlines())
    readme_lines = readme_path.read_text(encoding='utf-8').splitlines()
    violations = []
    for i, line in enumerate(readme_lines):
        if not (
            line.startswith(README_CROSS_CHAR)
            or line.startswith(README_CHECK_CHAR)
            or line.startswith(README_APPLIED_RULES_PREFIX)
        ):
            continue
        if line not in before_after_lines:
            prefix = ' '.join(line.split()[:8])
            violations.append((str(rel), (
                f"readme-example-drift {rel} line {i + 1} is not, character for "
                f"character, a line of {BEFORE_AFTER_PATH}: \"{prefix} ...\""
            )))
    return violations


def check_readme_example_lead_distance(repo_root):
    """Require README.md to carry at least one line beginning with
    README_CROSS_CHAR, and require the first such line's one-based line
    number to be at or below README_FIRST_EXAMPLE_MAX_LINE. Reads the
    file raw, without calling strip_fences. Returns an empty list before
    any read when README.md does not exist. Fires once, naming whichever
    of the two conditions applied: no such line exists at all, or the
    first one sits past the ceiling.

    Declared ceiling: it counts physical lines from the top of the raw
    file, so a long paragraph written as one physical line counts once
    while the same prose hard-wrapped counts many times -- a stated
    definition, not an implied one, and the reason the ceiling carries
    margin. It asserts the example arrives early, never that the example
    is good, that the prose above it is necessary, or that the pair
    below it is complete -- readme-example-drift owns the reproduction's
    fidelity and readme-before-after-order owns the section ordering. It
    reads only README_CROSS_CHAR, so a README leading with a check line
    and no ballot-cross line is reported as having no example, which is
    intended: the contrast is the point."""
    readme_path = repo_root / 'README.md'
    if not readme_path.exists():
        return []
    rel = readme_path.relative_to(repo_root)
    lines = readme_path.read_text(encoding='utf-8').splitlines()
    first_idx = next((i for i, l in enumerate(lines) if l.startswith(README_CROSS_CHAR)), None)
    if first_idx is None:
        return [(str(rel), (
            f"readme-example-lead-distance {rel} carries no line beginning with "
            f"'{README_CROSS_CHAR}', so it shows no before/after example at all"
        ))]
    line_no = first_idx + 1
    if line_no > README_FIRST_EXAMPLE_MAX_LINE:
        return [(str(rel), (
            f"readme-example-lead-distance {rel}'s first '{README_CROSS_CHAR}' line "
            f"sits at line {line_no}, past the {README_FIRST_EXAMPLE_MAX_LINE}-line ceiling"
        ))]
    return []


# Bounded to a lowercase letter followed by up to 19 more lowercase
# letters or hyphens (20 characters total), so an ordinary quoted phrase
# or a parenthesised sentence containing spaces or punctuation is not
# mistaken for a marker -- the character class itself excludes spaces,
# so there is no unbounded-width match to backtrack over.
README_LAYOUT_LEGEND_MARKER_RE = re.compile(r'"([a-z][a-z-]{0,19})"')
README_LAYOUT_TREE_MARKER_RE = re.compile(r'\(([a-z][a-z-]{0,19})\)')


def check_readme_layout_legend_drift(repo_root):
    """Within README.md's README_LAYOUT_HEADING section (if present),
    compare the set of markers the prose explains (a short lowercase
    word or hyphenated phrase inside double quotes,
    README_LAYOUT_LEGEND_MARKER_RE) against the set of markers the
    fenced tree uses (the same shape inside parentheses,
    README_LAYOUT_TREE_MARKER_RE), reusing FENCE_RE to isolate the tree
    away from the surrounding prose. Returns an empty list before any read
    when README.md does not exist, and returns an empty list when the
    layout heading itself is absent -- a README with no layout section
    is silent, not violating, matching publish-location-drift's stated
    decision that a carrier with nothing to say is silent. Fires once
    per marker the prose explains that the tree never uses, and once
    per marker the tree uses that the prose never mentions, naming the
    marker and which direction the mismatch runs.

    Declared ceiling: it compares marker vocabulary only. It says
    nothing about whether a marker is applied to the right entries,
    whether the tree matches the filesystem, whether the legend's
    explanation of a marker is accurate, or whether an entry that
    carries no marker should. Its marker shape is a short lowercase
    token inside double quotes in prose and inside parentheses in the
    tree, bounded to at most 20 characters each; a marker written in any
    other shape -- bracketed, uppercase, or longer than the stated bound
    -- is invisible to this check. And it reads only the layout section,
    so a marker vocabulary introduced elsewhere in README is out of
    scope."""
    readme_path = repo_root / 'README.md'
    if not readme_path.exists():
        return []
    rel = readme_path.relative_to(repo_root)
    lines = readme_path.read_text(encoding='utf-8').splitlines()
    start = next((i for i, l in enumerate(lines) if l.strip() == README_LAYOUT_HEADING), None)
    if start is None:
        return []
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if re.match(r'^## ', lines[j]):
            end = j
            break
    body = '\n'.join(lines[start + 1:end])

    fence_match = FENCE_RE.search(body)
    if fence_match:
        tree_text = fence_match.group(0)
        prose_text = body[:fence_match.start()] + body[fence_match.end():]
    else:
        tree_text = ''
        prose_text = body

    legend_markers = {m.group(1) for m in README_LAYOUT_LEGEND_MARKER_RE.finditer(prose_text)}
    tree_markers = {m.group(1) for m in README_LAYOUT_TREE_MARKER_RE.finditer(tree_text)}

    violations = []
    for marker in sorted(legend_markers - tree_markers):
        violations.append((str(rel), (
            f"readme-layout-legend-drift {rel}'s '{README_LAYOUT_HEADING}' legend "
            f"explains marker \"{marker}\", which the tree never uses"
        )))
    for marker in sorted(tree_markers - legend_markers):
        violations.append((str(rel), (
            f"readme-layout-legend-drift {rel}'s '{README_LAYOUT_HEADING}' tree uses "
            f"marker \"{marker}\", which the legend never mentions"
        )))
    return violations


def check_readme_output_style_destination(repo_root):
    """Require README.md, if it names README_OUTPUT_STYLE_PATH anywhere,
    to also name at least one of README_OUTPUT_STYLE_DESTINATIONS -- the
    directory Claude Code actually scans for output styles, as distinct
    from this repository's root-level output-styles/, which is where a
    plugin ships a style from and is scanned only once the repository is
    installed as a plugin. Reads README.md raw, without calling
    strip_fences, for the reason check_readme_install_paths already
    states in its own docstring: the copy command lives inside a fence,
    and stripping fences would find nothing and pass silently. Returns
    an empty list before any read when README.md does not exist, and
    returns an empty list when README never names README_OUTPUT_STYLE_PATH
    at all -- a README stating no output-style route has nothing for this
    code to say. Otherwise fires once when the text names neither
    destination directory, naming the file, the route, and both
    directories it could have named.

    Declared ceiling: this check asserts the README tells a reader which
    directory the output-style file has to reach. It asserts nothing
    about whether the copy succeeds, whether Claude Code lists or applies
    the style, whether the stated command is correct, or whether any
    other route is executable -- readme-install-path-missing owns anchor
    presence and nothing in this repository owns route executability.
    The comparison is literal substring containment with no path
    expansion and no filesystem access, so a README naming the directory
    in a different notation (a different home-directory alias, a
    relative path, an environment variable) is invisible to it."""
    violations = []
    readme_path = repo_root / 'README.md'
    if not readme_path.exists():
        return violations
    text = readme_path.read_text(encoding='utf-8')
    if README_OUTPUT_STYLE_PATH not in text:
        return violations
    if not any(dest in text for dest in README_OUTPUT_STYLE_DESTINATIONS):
        violations.append(('README.md', (
            f"readme-output-style-destination-missing README.md names "
            f"{README_OUTPUT_STYLE_PATH} as the output-style route but names "
            f"neither directory Claude Code scans for output styles "
            f"({' or '.join(README_OUTPUT_STYLE_DESTINATIONS)})"
        )))
    return violations


# ---------------------------------------------------------------------------
# output-styles/proof-first.md and prompts/system-prompt.md (Phase 4, 04-03)
# -- DIST-05's generated-derivative freshness and coverage guarantee. This
# is the authoritative copy of DERIVATIVE_SOURCE_NAMES and DERIVATIVE_PATHS;
# tools/generate_derivatives.py mirrors it. Neither file imports the other
# -- a sibling import inside tools/ would depend on how the script happens
# to be invoked -- so the stamp's own recorded path list, checked against
# this tuple by check_skill_derivative_stale, is what enforces the two
# staying in agreement (P4-13).
# ---------------------------------------------------------------------------

DERIVATIVE_PATHS = ('output-styles/proof-first.md', 'prompts/system-prompt.md')

DERIVATIVE_SOURCE_NAMES = (
    'skills/proof-first/SKILL.md',
    'skills/proof-first/references/deletion-test.md',
    'skills/proof-first/references/completeness-audit.md',
    'skills/proof-first/references/artifact-patterns.md',
    'skills/proof-first/references/checklist.md',
)

DERIVATIVE_STAMP_RE = re.compile(
    r'^<!-- generated by tools/generate_derivatives\.py from (.+) sha256:([0-9a-f]{64}) -->$'
)

# Mirrors tools/generate_derivatives.py's own STAMP_TEMPLATE. Self-test
# fixtures below build stamp lines with this template so a fixture's own
# hand-written stamp matches the shape DERIVATIVE_STAMP_RE parses.
DERIVATIVE_STAMP_RE_TEMPLATE = '<!-- generated by tools/generate_derivatives.py from {paths} sha256:{digest} -->'


def _derivative_stamp(path):
    """Return (paths_tuple, digest) read from the first line in path
    matching DERIVATIVE_STAMP_RE. The stamp is located by pattern, not by
    physical line number (P4-12): an output style needs its YAML
    frontmatter delimiter at line 1, so the stamp sits after it there,
    while a system prompt with no frontmatter carries it at line 1.
    Returns (None, None) when no line matches."""
    text = path.read_text(encoding='utf-8')
    for line in text.splitlines():
        m = DERIVATIVE_STAMP_RE.match(line)
        if m:
            paths = tuple(p.strip() for p in m.group(1).split(','))
            return paths, m.group(2)
    return None, None


def _hash_sources(repo_root):
    """One hashlib.sha256 over the concatenated bytes of every path in
    DERIVATIVE_SOURCE_NAMES, in tuple order -- the identical recipe
    tools/generate_derivatives.py's source_hash() uses, stated once here
    and once there, with the stamp as the bridge between them."""
    h = hashlib.sha256()
    for name in DERIVATIVE_SOURCE_NAMES:
        h.update((repo_root / name).read_bytes())
    return h.hexdigest()


def check_skill_derivative_stale(repo_root):
    """For each of DERIVATIVE_PATHS that exists, require a stamp line
    recording the frozen source-path list and a digest matching a fresh
    hash of those sources. Returns an empty list before any read when
    neither derivative exists.

    Declared ceiling: the recorded hash proves a derivative was produced
    from some version of the named sources, not that the generator's own
    derivation logic is correct -- a bug there that dropped a rule would
    still produce a matching hash. It proves structural freshness only
    and says nothing about a live session. A hand-edit to a derivative's
    body after generation leaves the recorded hash valid, which is
    exactly why `python3 tools/generate_derivatives.py --check` runs in
    CI as a second, independent guard."""
    violations = []
    existing = [rel for rel in DERIVATIVE_PATHS if (repo_root / rel).exists()]
    if not existing:
        return violations

    fresh_digest = None
    for rel in existing:
        path = repo_root / rel
        paths, digest = _derivative_stamp(path)
        if digest is None:
            violations.append((rel, (
                f"skill-derivative-stale {rel} records no stamp matching the frozen "
                f"generated-by pattern -- run python3 tools/generate_derivatives.py"
            )))
            continue
        if paths != DERIVATIVE_SOURCE_NAMES:
            violations.append((rel, (
                f"skill-derivative-stale {rel}'s stamp records the source list {list(paths)}, "
                f"but tools/check_repo.py's frozen DERIVATIVE_SOURCE_NAMES is "
                f"{list(DERIVATIVE_SOURCE_NAMES)}"
            )))
            continue
        if fresh_digest is None:
            fresh_digest = _hash_sources(repo_root)
        if digest != fresh_digest:
            violations.append((rel, (
                f"skill-derivative-stale {rel}'s stamp records sha256:{digest}, but a fresh "
                f"hash of the named sources is sha256:{fresh_digest} -- run "
                f"python3 tools/generate_derivatives.py to re-sync"
            )))
    return violations


def check_derivative_rule_coverage(allocated, repo_root):
    """For each of DERIVATIVE_PATHS that exists, require a '### <ID> -- '
    rule heading (the same shape RULE_HEADING_RE and MC_HEADING_RE match)
    for every PF- and MC- ID in `allocated`, and require every string in
    ARTIFACT_FAMILY_SECTIONS to appear. Emits one violation per missing
    item, naming the derivative, the missing ID or family string, and the
    requirement it serves (DIST-03 for the output style, DIST-04 for the
    system prompt). Returns an empty list before any read when a
    derivative does not exist.

    Declared ceiling: this proves every shipped rule heading and every
    artifact-family heading reaches each derivative -- a structural
    statement about content presence. It proves nothing about what a
    model does with that content, nothing about whether a session driven
    by a derivative reaches the same conclusions as one with the skill
    folder installed, and nothing about whether the omitted illustration
    file's absence changes anything. That second statement now has a
    committed source: evals/routes/RESULTS-routes.md, which 04-15 wrote
    from 36 headless sessions and which reports a null result -- every
    pair of arms overlapping -- not equivalence. This check is not that
    measurement and does not stand in for it; read the results file.
    check_derivative_comparison_claim below is built on the same premise
    and fails the build if a derivative reasserts the old "no benchmark
    has compared" denial while that results file exists."""
    violations = []
    pf_ids = sorted(row['id'] for row in allocated if PF_ID_RE.match(row['id']))
    mc_ids = sorted(row['id'] for row in allocated if MC_ID_RE.match(row['id']))
    requirement_for = {DERIVATIVE_PATHS[0]: 'DIST-03', DERIVATIVE_PATHS[1]: 'DIST-04'}

    for rel in DERIVATIVE_PATHS:
        path = repo_root / rel
        if not path.exists():
            continue
        text = strip_fences(path.read_text(encoding='utf-8'))
        requirement = requirement_for[rel]
        found_pf = set()
        found_mc = set()
        for line in text.splitlines():
            m = RULE_HEADING_RE.match(line)
            if m:
                found_pf.add(m.group(1))
            m = MC_HEADING_RE.match(line)
            if m:
                found_mc.add(m.group(1))
        for pf_id in pf_ids:
            if pf_id not in found_pf:
                violations.append((rel, (
                    f"derivative-rule-coverage-incomplete {rel} is missing the rule heading "
                    f"for {pf_id}, which {requirement} requires"
                )))
        for mc_id in mc_ids:
            if mc_id not in found_mc:
                violations.append((rel, (
                    f"derivative-rule-coverage-incomplete {rel} is missing the rule heading "
                    f"for {mc_id}, which {requirement} requires"
                )))
        for family in ARTIFACT_FAMILY_SECTIONS:
            if family not in text:
                violations.append((rel, (
                    f"derivative-rule-coverage-incomplete {rel} is missing the artifact-family "
                    f"heading '{family}', which {requirement} requires"
                )))
    return violations


# The committed route-equivalence measurement (Phase 4, 04-15). Its mere
# existence is what makes the derivatives' old "no benchmark has compared"
# sentence false, which is the whole conjunction check_derivative_comparison_claim
# tests. Stored as a relative POSIX string, joined onto repo_root at call time,
# so a fixture root is checked against its own tree and never the real one.
ROUTES_RESULTS_PATH = 'evals/routes/RESULTS-routes.md'

# The exact literal the pre-04-15 generator preamble emitted. Matched as a
# substring, case-sensitively, with no normalisation -- the sentence is
# generator output, so it either comes back byte-identical or it is a
# different sentence this code deliberately does not judge.
STALE_COMPARISON_CLAIM = 'No benchmark has compared'

# The benchmark results file whose existence falsifies STALE_BENCHMARK_RUN_CLAIM.
# Same shape as ROUTES_RESULTS_PATH above: a relative POSIX string joined onto
# repo_root at call time, so a fixture root is checked against its own tree.
BENCHMARK_RESULTS_PATH = 'evals/benchmark/RESULTS.md'

# The sibling stale claim, found by round-2 UAT on 2026-09-21 in
# skills/proof-first/references/artifact-patterns.md and carried verbatim into
# both derivatives. Unlike STALE_COMPARISON_CLAIM this sentence is hand-written
# prose in a skill source rather than generator output, so a regression can
# plausibly restore it capitalised at a sentence start; it is matched
# case-insensitively for that reason, and that is the only deliberate difference
# between the two literals' matching discipline.
STALE_BENCHMARK_RUN_CLAIM = 'no benchmark has run'

# What the benchmark-run claim is scanned in: the generated derivatives AND the
# skill sources they are generated from. The sentence originated in a source, so
# scanning derivatives alone would stay silent until the next regeneration --
# which is precisely the window in which the false sentence shipped.
BENCHMARK_CLAIM_PATHS = DERIVATIVE_PATHS + DERIVATIVE_SOURCE_NAMES


def check_derivative_comparison_claim(repo_root):
    """Fire when the route-equivalence measurement exists and a generated
    derivative still asserts that no such comparison has been run.

    Returns an empty list before reading any derivative when
    ROUTES_RESULTS_PATH does not exist: with no comparison committed, the
    derivatives' claim is true and there is nothing to report. Otherwise
    reads each present derivative raw -- no strip_fences, because the
    preamble is prose outside any fence and stripping would change nothing
    except the offsets -- and emits one violation per file still carrying
    STALE_COMPARISON_CLAIM.

    Declared ceiling: a two-sided literal-substring presence conjunction.
    It does not read the results file's contents, does not check that
    whatever replaced the sentence is accurate, does not check that a
    derivative points at the results file at all, and cannot see the same
    false claim restated in other words. What it does close is the one
    regression path that matters here: the generator's preamble is
    regenerated on every release, and a revert or a bad merge putting the
    stale sentence back while the measurement sits in the tree would ship a
    derivative that contradicts the repository's own committed evidence.
    That is worth a code precisely because a reader of the sentence has no
    way to tell whether it is still true."""
    violations = []
    results_path = repo_root / ROUTES_RESULTS_PATH
    if not results_path.exists():
        return violations
    for rel in DERIVATIVE_PATHS:
        path = repo_root / rel
        if not path.exists():
            continue
        if STALE_COMPARISON_CLAIM in path.read_text(encoding='utf-8'):
            violations.append((rel, (
                f"derivative-comparison-claim-stale {rel} still states "
                f"'{STALE_COMPARISON_CLAIM}', but {ROUTES_RESULTS_PATH} exists in this tree "
                f"and is exactly such a comparison -- regenerate the derivatives from "
                f"tools/generate_derivatives.py rather than editing this file"
            )))
    return violations


def check_stale_benchmark_run_claim(repo_root):
    """Fire when the benchmark results file exists and a shipped skill source
    or a generated derivative still asserts that no benchmark has run.

    The sibling of check_derivative_comparison_claim, and deliberately the
    same shape: a two-sided literal-substring presence conjunction, gated on
    the existence of the evidence file that falsifies the sentence. Returns
    an empty list before reading anything when BENCHMARK_RESULTS_PATH does
    not exist -- with no benchmark committed the sentence is true and there
    is nothing to report.

    Two deliberate differences from its sibling, both of them because this
    sentence is hand-written prose rather than generator output. It matches
    case-insensitively, so a regression restoring the sentence at the start
    of a sentence is still caught. And it scans BENCHMARK_CLAIM_PATHS --
    the derivatives plus the skill sources they are generated from -- rather
    than the derivatives alone, because the origin of the sentence is a
    source file and a source-only regression would otherwise stay invisible
    until the next regeneration.

    Declared ceiling: literal-substring presence, nothing more. It does not
    read BENCHMARK_RESULTS_PATH's contents, does not check that whatever
    replaced the sentence is accurate, does not check that any file points
    at the results, and cannot see the same false claim restated in other
    words."""
    violations = []
    if not (repo_root / BENCHMARK_RESULTS_PATH).exists():
        return violations
    needle = STALE_BENCHMARK_RUN_CLAIM.lower()
    for rel in BENCHMARK_CLAIM_PATHS:
        path = repo_root / rel
        if not path.exists():
            continue
        if needle in path.read_text(encoding='utf-8').lower():
            violations.append((rel, (
                f"benchmark-run-claim-stale {rel} still states "
                f"'{STALE_BENCHMARK_RUN_CLAIM}', but {BENCHMARK_RESULTS_PATH} exists in this "
                f"tree and records a benchmark that ran -- state what the benchmark does and "
                f"does not establish rather than denying that it happened"
            )))
    return violations


DERIVATIVE_CHECK_CODES = [
    'skill-derivative-stale', 'derivative-rule-coverage-incomplete',
    'derivative-comparison-claim-stale', 'benchmark-run-claim-stale',
]


def run_derivative_checks(repo_root):
    violations = []
    violations += check_skill_derivative_stale(repo_root)
    violations += check_derivative_comparison_claim(repo_root)
    violations += check_stale_benchmark_run_claim(repo_root)
    numbering_path = repo_root / 'NUMBERING.md'
    if not numbering_path.exists():
        return violations
    data = parse_numbering(numbering_path)
    violations += check_derivative_rule_coverage(data['allocated'], repo_root)
    return violations


# ---------------------------------------------------------------------------
# Citation resolution inside this repository's own records (06-08)
#
# Rounds 1-4 of cold reads on this repository produced 45 findings. Citation
# defects were among them, and this code catches NONE of those: every citation
# finding those four rounds produced was a line number that still existed and
# pointed at the wrong content -- a semantic mismatch, not an unresolvable
# reference. The full-history replay recorded in the module docstring's
# record-citation-unresolvable entry fired ZERO times.
#
# What this code is, therefore, is future insurance against three shapes that
# have not yet occurred here: a path that names no file, a range past
# end-of-file, an inverted range. It deliberately does not attempt the harder
# half -- whether the cited lines say what the citing sentence claims -- which
# is the semantic judgement this repository has refused to put behind a build
# gate four times, and which is the half every citation finding so far has
# actually been.
#
# Corrected 06-09. This comment previously said nine of the 45 were "a
# `path`:N citation that ... stopped resolving" and that "This code closes
# that class." Both contradicted the module docstring, which is the more
# careful account and was written by the same commit. A block comment is the
# first thing a maintainer reads to learn why code exists, so it is the worse
# of the two places to overstate. Round 5 then produced two more citation
# findings -- two derivative `path`:N pairs broken by 06-08's own first
# commit -- and this code was silent on both, because the cited lines existed.
# ---------------------------------------------------------------------------

# The records whose citations are validated. Both are already read by other
# codes. Scoped to these two because they are where the drift was measured,
# not because no other file can carry a citation -- README.md is in scope
# because it is where a citation would next be written, not because it
# carries one today.
#
# Corrected 06-09. The first sentence read "Both already carry `path`:N
# citations", which was never true of README.md. Measured at 06-09 by running
# this file's own CITATION_RE over both paths: 9 matches in LEGAL-REVIEW.md, 0
# in README.md, identical before and after strip_fences(). Those figures are
# pinned to that measurement, not restated as a live count -- the same
# convention the record-citation-unresolvable docstring uses for its replay,
# and for the same reason.
CITATION_RECORD_PATHS = ('LEGAL-REVIEW.md', 'README.md')

# Directories never searched when resolving a bare basename, and never
# scanned for citations. `.planning/` is tracked but is a planning-artifact
# archive: a citation into a superseded plan is a historical record, not a
# live claim.
CITATION_SKIP_DIRS = frozenset({'.git', '.planning'})

# A citation is a backticked path carrying a file extension, immediately
# followed by ':N' or ':N-M'. The backticks are load-bearing. Without them
# this matches shell snippets, table cells and prose that put a filename and
# a number next to each other for unrelated reasons -- the exact
# false-positive class that would make this gate unusable.
CITATION_RE = re.compile(
    r'`([A-Za-z0-9_][A-Za-z0-9_./-]*\.[A-Za-z0-9]+)`:(\d+)(?:-(\d+))?'
)


def _citation_tree_index(repo_root):
    """Map basename -> list of repo-relative paths, over every file in the
    tree outside CITATION_SKIP_DIRS. Built by walking rather than by asking
    git, because the self-test and mutation harnesses run against temporary
    roots that have no git repository."""
    index = {}
    for path in repo_root.rglob('*'):
        if not path.is_file():
            continue
        rel = path.relative_to(repo_root)
        if CITATION_SKIP_DIRS & set(rel.parts):
            continue
        index.setdefault(rel.name, []).append(rel)
    return index


def _citation_line_count(repo_root, rel):
    try:
        return len((repo_root / rel).read_text(encoding='utf-8').splitlines())
    except (OSError, UnicodeDecodeError):
        return None


def check_record_citations(repo_root):
    """Check that every `path`:N / `path`:N-M citation in
    CITATION_RECORD_PATHS resolves to a real file and a real line range.

    Resolution order: an exact repository-relative path first, then -- for a
    spelling with no directory separator -- a basename search over the tree.
    A range is reported when its high bound runs past the file's last line,
    when its low bound is below 1, or when the bounds are inverted.

    Declared ceiling: see this module's docstring. In one sentence: this
    proves a citation points at lines that exist, and says nothing whatever
    about whether those lines support the sentence citing them."""
    violations = []
    index = None
    for record in CITATION_RECORD_PATHS:
        record_path = repo_root / record
        if not record_path.exists():
            continue
        text = strip_fences(record_path.read_text(encoding='utf-8'))
        seen = set()
        for match in CITATION_RE.finditer(text):
            spelling, low_s, high_s = match.group(1), match.group(2), match.group(3)
            cited = f'`{spelling}`:{low_s}' + (f'-{high_s}' if high_s else '')
            if cited in seen:
                continue
            seen.add(cited)
            low = int(low_s)
            high = int(high_s) if high_s else low

            if index is None:
                index = _citation_tree_index(repo_root)
            exact = Path(spelling)
            if (repo_root / exact).is_file():
                candidates = [exact]
            elif '/' in spelling:
                candidates = []
            else:
                candidates = index.get(spelling, [])

            if not candidates:
                violations.append((record, (
                    f'record-citation-unresolvable {record} cites {cited}, '
                    f'and no file named {spelling} exists in the tree'
                )))
                continue

            if high < low:
                violations.append((record, (
                    f'record-citation-unresolvable {record} cites {cited}, '
                    f'whose line range is inverted'
                )))
                continue
            if low < 1:
                violations.append((record, (
                    f'record-citation-unresolvable {record} cites {cited}, '
                    f'whose first line is below 1'
                )))
                continue

            lengths = {}
            for rel in candidates:
                count = _citation_line_count(repo_root, rel)
                if count is not None:
                    lengths[str(rel)] = count
            if not lengths:
                continue
            # With more than one candidate the check cannot tell which file
            # was meant, so it fires only when the range overruns every one.
            if all(high > count for count in lengths.values()):
                detail = ', '.join(
                    f'{name} has {count} line(s)' for name, count in sorted(lengths.items())
                )
                violations.append((record, (
                    f'record-citation-unresolvable {record} cites {cited}, '
                    f'which runs past the end of the file it names ({detail})'
                )))
    return sorted(violations)


CITATION_CHECK_CODES = ['record-citation-unresolvable']


def run_citation_checks(repo_root):
    violations = []
    violations += check_record_citations(repo_root)
    return violations


ALL_CHECK_CODES = (
    ID_CHECK_CODES + FIGURE_CHECK_CODES + NOTICES_CHECK_CODES
    + LICENSE_CHECK_CODES + README_CHECK_CODES + RESULTS_CHECK_CODES
    + SOURCES_CHECK_CODES
    + FRAMEWORK_CHECK_CODES + FRONTMATTER_CHECK_CODES + CATALOG_CHECK_CODES
    + PLUGIN_CHECK_CODES + EXAMPLE_CHECK_CODES + DERIVATIVE_CHECK_CODES
    + CITATION_CHECK_CODES
)


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def run_all_checks(repo_root):
    violations = []
    violations += run_id_checks(repo_root)
    violations += run_figure_checks(repo_root)
    violations += run_notices_checks(repo_root)
    violations += run_license_checks(repo_root)
    violations += run_readme_checks(repo_root)
    violations += run_results_checks(repo_root)
    violations += run_sources_checks(repo_root)
    violations += run_framework_checks(repo_root)
    violations += run_frontmatter_checks(repo_root)
    violations += run_catalog_checks(repo_root)
    violations += run_plugin_checks(repo_root)
    violations += run_example_checks(repo_root)
    violations += run_derivative_checks(repo_root)
    violations += run_citation_checks(repo_root)
    return violations


# ---------------------------------------------------------------------------
# Known, tracked, currently-open violations -- see .planning/WINDOWS.md
#
# This set is deliberately empty. It previously excused
# skill-token-budget-exceeded against skills/proof-first/SKILL.md
# (.planning/WINDOWS.md id 5), but that finding is now closed -- 02-07's
# trim brought the file under the 5,000-token ceiling, so mutation-test's
# CONTROL step is back to an unweakened "zero violations on an unmutated
# copy" assertion for every code, with no allowance masking a future
# regression.
#
# If a future finding needs this set populated again, name the specific
# (code, subject) pair it excuses -- e.g.
# frozenset({('skill-token-budget-exceeded', 'skills/proof-first/SKILL.md')})
# -- never a bare code. A bare code excuses every subject that code could
# ever fire against, so a second skill folder independently breaching the
# same ceiling for an unrelated reason would be silently absorbed into the
# known-open bucket instead of surfacing as the new, unexpected regression
# it actually is (02-REVIEW.md WR-01).
# ---------------------------------------------------------------------------

KNOWN_OPEN_VIOLATIONS = frozenset()


# ---------------------------------------------------------------------------
# Mutation testing (CR-01 gap closure)
#
# The self-test above proves each check fires against a hand-built fixture.
# It cannot prove a check fires against this repository's own production
# document shapes -- that gap is exactly what let a dead check ship named as
# covered (01-VERIFICATION.md). This section injects one named defect at a
# time into a throwaway copy of the real repository files and asserts the
# matching violation code fires, closing the class rather than today's
# instances of it.
# ---------------------------------------------------------------------------

MUTATION_SOURCES = (
    'LICENSE', 'NUMBERING.md', 'NOTICES.md', 'README.md', 'examples', 'tools', 'skills',
    'evals', '.claude-plugin', 'output-styles', 'prompts',
    # 06-01: without SOURCES.md here the mutation harness cannot reach the real
    # approved-source list, and source-row-unconfirmed would be registered but not
    # discrimination-proven -- this repository's named recurring defect, recorded
    # as .planning/WINDOWS.md id 10.
    'SOURCES.md',
    # 06-02: source-gate-incomplete reads LEGAL-REVIEW.md's gate marker and
    # framework-statement-stale-review reads its review date. Without the file here
    # neither code has anything to mutate, and both would be registered but not
    # discrimination-proven.
    'LEGAL-REVIEW.md',
)


def _copy_repo_subset(repo_root, dest):
    """Copy exactly MUTATION_SOURCES into dest. Never copies .git or
    .planning -- only the repository-relative paths the checker reads.

    Three entries were added after the original tuple, each so that one code
    would be discrimination-proven rather than merely registered: 'evals' by
    03-14, for results-breakdown-count-mismatch; 'SOURCES.md' by 06-01, for
    source-row-unconfirmed; and 'LEGAL-REVIEW.md' by 06-02, for
    source-gate-incomplete and framework-statement-stale-review. Without each
    path in this tuple the mutation copy has no file for its code to mutate.

    Every one of those widenings also brings other readers into the mutation
    copy. They are listed rather than denied, because three successive
    versions of this comment asserted that no other check read these paths and
    all three assertions were false. The block was edited three times after the
    first absolute went into it -- 82535c7, c0fca5f and e2e4aa2 -- and each of
    those edits left the absolutes then standing in place. The readers below
    were measured on 2026-09-22 by running
    the live checker under a pathlib.Path.read_text wrapper that records the
    enclosing check_* frame of every read, which is the fact the assertions
    were making rather than a proxy for it:

      evals/*/RESULTS*.md  readme-claim-unsourced (all four files),
                           results-breakdown-count-mismatch (RESULTS-mod04.md
                           only)
      SOURCES.md           source-row-unconfirmed, source-gate-incomplete,
                           record-citation-unresolvable
      LEGAL-REVIEW.md      source-gate-incomplete,
                           framework-statement-stale-review,
                           record-citation-unresolvable

    So a widening here is not neutral for the other codes in its row, and a
    mutation to one of these files can legitimately trip more than the code it
    was written for."""
    for name in MUTATION_SOURCES:
        src = repo_root / name
        if not src.exists():
            continue
        target = dest / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, target)
        else:
            shutil.copy2(src, target)


def _insert_table_rows_after_heading(text, heading, new_rows):
    """Insert new_rows immediately after the first Markdown table's
    separator row that follows the '## {heading}' line -- the only
    insertion point that works while a table has zero data rows."""
    lines = text.splitlines()
    heading_line = f'## {heading}'
    h_idx = next(i for i, l in enumerate(lines) if l.strip() == heading_line)
    i = h_idx + 1
    while i < len(lines) and not lines[i].strip().startswith('|'):
        i += 1
    header_idx = i
    sep_idx = header_idx + 1
    insert_at = sep_idx + 1
    out = lines[:insert_at] + list(new_rows) + lines[insert_at:]
    return '\n'.join(out) + '\n'


def _mutate_dup_id(root):
    path = root / 'NUMBERING.md'
    text = path.read_text(encoding='utf-8')
    row = '| PF-0.1 | Mutation dup row | SKILL.md | v0.0.0 |'
    text = _insert_table_rows_after_heading(text, 'Allocated IDs', [row, row])
    path.write_text(text, encoding='utf-8')


def _mutate_range_id(root):
    path = root / 'NUMBERING.md'
    text = path.read_text(encoding='utf-8')
    row = '| PF-0.99 | Mutation over-ceiling row | SKILL.md | v0.0.0 |'
    text = _insert_table_rows_after_heading(text, 'Allocated IDs', [row])
    path.write_text(text, encoding='utf-8')


def _mutate_revived_id(root):
    path = root / 'NUMBERING.md'
    text = path.read_text(encoding='utf-8')
    text = _insert_table_rows_after_heading(
        text, 'Allocated IDs', ['| PF-0.3 | Mutation revived row | SKILL.md | v0.0.0 |'])
    text = _insert_table_rows_after_heading(
        text, 'Deprecated IDs', ['| PF-0.3 | v0.0.0 | PF-0.1 |'])
    path.write_text(text, encoding='utf-8')


def _mutate_undefined_id(root):
    path = root / 'README.md'
    text = path.read_text(encoding='utf-8')
    if not text.endswith('\n'):
        text += '\n'
    text += '\nThis mutation cites PF-9.9, which no Allocated IDs row defines.\n'
    path.write_text(text, encoding='utf-8')


def _mutate_dup_figure_key(root):
    path = root / 'examples' / 'deal-brief.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    h_idx = next(i for i, l in enumerate(lines) if l.strip() == '## Canonical figures')
    i = h_idx + 1
    while not lines[i].strip().startswith('|'):
        i += 1
    first_row_idx = i + 2  # i = header row, i+1 = separator row, i+2 = first data row
    lines.insert(first_row_idx + 1, lines[first_row_idx])
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_figure_order(root):
    path = root / 'examples' / 'deal-brief.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    h_idx = next(i for i, l in enumerate(lines) if l.strip() == '## Canonical figures')
    i = h_idx + 1
    while not lines[i].strip().startswith('|'):
        i += 1
    first_row_idx = i + 2
    j = first_row_idx
    while j < len(lines) and lines[j].strip().startswith('|'):
        j += 1
    last_row_idx = j - 1
    last_row = lines.pop(last_row_idx)
    lines.insert(first_row_idx, last_row)
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_unlisted_figure(root):
    path = root / 'examples' / 'deal-brief.md'
    text = path.read_text(encoding='utf-8')
    if not text.endswith('\n'):
        text += '\n'
    text += (
        "This prose line was appended after the Canonical figures table, the "
        "file's last section, and cites $123,456,789 which matches no row.\n"
    )
    path.write_text(text, encoding='utf-8')


def _mutate_pointer_missing(root):
    pointer, _carriers = parse_notices(root / 'NOTICES.md')
    path = root / 'README.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    lines = [l for l in lines if l.strip() != pointer]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_pointer_duplicated(root):
    pointer, _carriers = parse_notices(root / 'NOTICES.md')
    path = root / 'README.md'
    text = path.read_text(encoding='utf-8')
    if not text.endswith('\n'):
        text += '\n'
    text += pointer + '\n'
    path.write_text(text, encoding='utf-8')


def _mutate_pointer_unparseable(root):
    path = root / 'NOTICES.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    lines = [l for l in lines if l.strip() != '## Attribution pointer']
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_license_missing(root):
    path = root / 'LICENSE'
    if path.exists():
        path.unlink()


def _mutate_readme_results_pointer_missing(root):
    """Delete every line of the copied real README.md that contains the
    results-pointer path, leaving everything else in place -- the mutation
    targets exactly what the check reads."""
    path = root / 'README.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    lines = [l for l in lines if README_RESULTS_POINTER not in l]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_results_breakdown_count_mismatch(root):
    """Raise the copied real results file's Arm A no-family bullet's
    stated count above its own enumeration sum (7 -> 99), leaving the
    parenthetical enumeration itself untouched -- isolates exactly the
    count/enumeration disagreement this check reads. Asserts the target
    text is found before substituting, following the existing mutators'
    precedent, so a future rewording of that bullet turns into a loud
    mutation failure rather than a silent no-op."""
    path = root / RESULTS_BREAKDOWN_PATH
    text = path.read_text(encoding='utf-8')
    target = '- no-family: 7 ('
    replacement = '- no-family: 99 ('
    assert target in text, (
        "results-breakdown-count-mismatch mutation: Arm A no-family bullet "
        "text not found in the real results file -- has its wording changed?"
    )
    text = text.replace(target, replacement, 1)
    path.write_text(text, encoding='utf-8')


def _mutate_framework_statement_missing(root):
    path = root / 'NOTICES.md'
    if path.exists():
        path.unlink()


def _mutate_catalog_id_drift(root):
    path = root / 'skills' / 'proof-first' / 'references' / 'checklist.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    h_idx = next(i for i, l in enumerate(lines) if l.strip() == '## PF rules')
    i = h_idx + 1
    while not lines[i].strip().startswith('|'):
        i += 1
    first_row_idx = i + 2  # i = header row, i+1 = separator row, i+2 = first data row
    del lines[first_row_idx]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_mc_catalog_id_drift(root):
    """Delete the single MC data row from references/checklist.md's
    '## MC rules' table in the copied tree, mirroring
    _mutate_catalog_id_drift's shape for the MC namespace."""
    path = root / 'skills' / 'proof-first' / 'references' / 'checklist.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    h_idx = next(i for i, l in enumerate(lines) if l.strip() == '## MC rules')
    i = h_idx + 1
    while not lines[i].strip().startswith('|'):
        i += 1
    first_row_idx = i + 2  # i = header row, i+1 = separator row, i+2 = first data row
    del lines[first_row_idx]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_mc_rule_in_skill(root):
    """Insert one MC-shaped rule heading into the copied
    skills/proof-first/SKILL.md. Because check_mc_catalog_id_drift compares
    the registry, the audit file and the checklist -- and never SKILL.md --
    this mutation fires the in-skill code alone."""
    path = root / 'skills' / 'proof-first' / 'SKILL.md'
    text = path.read_text(encoding='utf-8')
    if not text.endswith('\n'):
        text += '\n'
    text += '\n### MC-1 — Mutation-inserted MC rule inside SKILL.md\n\nBody text.\n'
    path.write_text(text, encoding='utf-8')


def _mutate_frontmatter_unparseable(root):
    """Remove the real SKILL.md's opening '---' line, so no frontmatter
    block can be isolated at all."""
    path = root / 'skills' / 'proof-first' / 'SKILL.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    del lines[0]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_frontmatter_unknown_key(root):
    """Insert a column-zero key outside the six-key allow-list (D-33) into
    the real frontmatter. 'compatibility' is deliberately NOT used here --
    it is one of the six *allowed* keys per the Agent Skills specification
    (this project simply omits it by convention, per D-29/D-30), so
    inserting it would prove nothing about this check."""
    path = root / 'skills' / 'proof-first' / 'SKILL.md'
    text = path.read_text(encoding='utf-8')
    text = text.replace('license: MIT\n', 'license: MIT\nauthor: Mutation Author\n', 1)
    path.write_text(text, encoding='utf-8')


def _mutate_frontmatter_name_mismatch(root):
    """Change the real frontmatter's name value so it no longer equals its
    parent directory."""
    path = root / 'skills' / 'proof-first' / 'SKILL.md'
    text = path.read_text(encoding='utf-8')
    text = text.replace('name: proof-first\n', 'name: not-proof-first\n', 1)
    path.write_text(text, encoding='utf-8')


def _mutate_frontmatter_description_invalid(root):
    """Truncate the real description body (the indented lines following
    'description: |') to a few characters, well below the floor."""
    path = root / 'skills' / 'proof-first' / 'SKILL.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        if line.strip() == 'description: |':
            i += 1
            while i < len(lines) and (lines[i].startswith(' ') or lines[i].strip() == ''):
                i += 1
            out.append('  short')
            continue
        i += 1
    path.write_text('\n'.join(out) + '\n', encoding='utf-8')


def _mutate_catalog_count_unstated(root):
    """Delete the stated-count line from the real SKILL.md."""
    path = root / 'skills' / 'proof-first' / 'SKILL.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    lines = [l for l in lines if not COUNT_SENTENCE_RE.match(l.strip())]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_catalog_count_mismatch(root):
    """Change the rule-count number in the real SKILL.md's stated-count
    line so it disagrees with the registry."""
    path = root / 'skills' / 'proof-first' / 'SKILL.md'
    text = path.read_text(encoding='utf-8')
    text = text.replace(
        'This catalog contains 31 rules in 6 numbered sections.',
        'This catalog contains 30 rules in 6 numbered sections.',
        1,
    )
    path.write_text(text, encoding='utf-8')


def _mutate_mc_count_unstated(root):
    """Delete the stated-count line from the real completeness-audit.md."""
    path = root / 'skills' / 'proof-first' / 'references' / 'completeness-audit.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    lines = [l for l in lines if not MC_COUNT_SENTENCE_RE.match(l.strip())]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_mc_count_mismatch(root):
    """Change the checks number in the real completeness-audit.md's
    stated-count line so it disagrees with the registry."""
    path = root / 'skills' / 'proof-first' / 'references' / 'completeness-audit.md'
    text = path.read_text(encoding='utf-8')
    text = text.replace(
        'This audit contains 8 checks across 8 dimensions.',
        'This audit contains 7 checks across 8 dimensions.',
        1,
    )
    path.write_text(text, encoding='utf-8')


def _mutate_skill_too_long(root):
    """Append filler lines to the real SKILL.md past its 500-line ceiling."""
    path = root / 'skills' / 'proof-first' / 'SKILL.md'
    text = path.read_text(encoding='utf-8')
    if not text.endswith('\n'):
        text += '\n'
    filler = '\n'.join(f"Filler line {i} pushing the file past its line ceiling." for i in range(200)) + '\n'
    text += filler
    path.write_text(text, encoding='utf-8')


def _mutate_skill_token_budget_exceeded(root):
    """Append filler words to the real SKILL.md, pushing its estimated
    token count over the ceiling. The control copy is under the ceiling
    (3,694 words / 4,802 estimated tokens as of 02-07's trim, a 198-token
    margin below the 5,000-token ceiling), so this mutation is clean ->
    fires like every other mutation: mutation_test()'s discrimination
    comparison applies to this code exactly as it applies to every other
    one, rather than depending on a pre-trimmed scratch copy."""
    path = root / 'skills' / 'proof-first' / 'SKILL.md'
    text = path.read_text(encoding='utf-8')
    if not text.endswith('\n'):
        text += '\n'
    text += '\n' + ' '.join(['filler'] * 2000) + '\n'
    path.write_text(text, encoding='utf-8')


def _mutate_artifact_family_section_missing(root):
    """Delete the '## Solution proposal' heading line from the copied
    real skills/proof-first/references/artifact-patterns.md, leaving its
    body in place -- a minimal mutation targeting exactly the heading the
    check reads."""
    path = root / 'skills' / 'proof-first' / 'references' / 'artifact-patterns.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    lines = [l for l in lines if l.strip() != '## Solution proposal']
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_skill_family_line_gate_missing(root):
    """Delete the self-check section's first numbered pass item from the
    copied real SKILL.md -- the pass carrying the two anchors this check
    reads (the artifact-family phrase, the No family fits value) --
    leaving the section heading and the other two passes in place. Matched
    by its '1. ' list position rather than its pass name, so a 03-11-style
    rename of that pass (Family-line -> Family-order) does not silently
    stop this mutation from targeting it; the check itself reads anchors
    in the section body, not the pass's name."""
    path = root / 'skills' / 'proof-first' / 'SKILL.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    lines = [l for l in lines if not l.strip().startswith('1. ')]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_skill_family_order_gate_missing(root):
    """Replace the copied real SKILL.md's ordering-pass wording with the
    pre-03-11 presence-only wording -- deleting the 're-scan' /
    'before any rule marker' anchors this check reads while leaving the
    artifact-family phrase and the No family fits value (the sibling
    check's own anchors) and the other two passes untouched. Isolates
    exactly the ordering gate this mutation targets."""
    path = root / 'skills' / 'proof-first' / 'SKILL.md'
    text = path.read_text(encoding='utf-8')
    ordered_pass = (
        "1. Family-order pass (mandatory): re-scan the response you just drafted, "
        "from its first character, before returning it, and confirm the line "
        "naming the artifact family — or stating **No family fits:** — stands "
        "before any rule marker, meaning no `PF-` or `MC-` citation appears "
        "earlier in the response. When one does, move the family line to the "
        "top and re-check before returning."
    )
    presence_only_pass = (
        "1. Family-line pass (mandatory): confirm the response's first line "
        "names the artifact family or states **No family fits:** — a response "
        "failing this is not ready to return."
    )
    assert ordered_pass in text, (
        "skill-family-order-gate-missing mutation: ordering pass text not found "
        "in the real SKILL.md -- has the self-check section wording changed?"
    )
    text = text.replace(ordered_pass, presence_only_pass)
    path.write_text(text, encoding='utf-8')


def _mutate_source_label_in_skill_content(root):
    """Insert one frozen source-coined label ('economic buyer') into the
    copied real references/artifact-patterns.md -- a minimal mutation
    targeting exactly what the check reads."""
    path = root / 'skills' / 'proof-first' / 'references' / 'artifact-patterns.md'
    text = path.read_text(encoding='utf-8')
    if not text.endswith('\n'):
        text += '\n'
    text += '\nMutation: reintroduces the economic buyer label here.\n'
    path.write_text(text, encoding='utf-8')


def _mutate_plugin_manifest_version_mismatch(root):
    """Change the copied real .claude-plugin/plugin.json's version so it no
    longer equals skills/proof-first/SKILL.md's frontmatter metadata.version,
    mutating only the copy."""
    path = root / PLUGIN_MANIFEST_PATH
    data = json.loads(path.read_text(encoding='utf-8'))
    data['version'] = '9.9.9'
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


def _mutate_plugin_manifest_invalid(root):
    """Delete the required 'license' key from the copied real
    .claude-plugin/plugin.json, mutating only the copy."""
    path = root / PLUGIN_MANIFEST_PATH
    data = json.loads(path.read_text(encoding='utf-8'))
    data.pop('license', None)
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


def _mutate_marketplace_entry_required_key_missing(root):
    """Delete the required 'license' key from the copied real
    .claude-plugin/marketplace.json's plugins[0] entry, mutating only the
    copy. This is a separate mutation from _mutate_plugin_manifest_invalid
    because that function deletes the same key from plugin.json, a
    different position -- and position is precisely what CR-01 was about:
    the marketplace entry's required keys were never checked at all."""
    path = root / MARKETPLACE_MANIFEST_PATH
    data = json.loads(path.read_text(encoding='utf-8'))
    data['plugins'][0].pop('license', None)
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


def _mutate_publish_location_drift(root):
    """Rewrite the copied real .claude-plugin/marketplace.json's plugin
    entry 'repository' to a different owner/repo than plugin.json states,
    mutating only the copy."""
    path = root / MARKETPLACE_MANIFEST_PATH
    data = json.loads(path.read_text(encoding='utf-8'))
    data['plugins'][0]['repository'] = 'https://github.com/someone/else'
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


def _mutate_before_after_family_missing(root):
    """Delete the '## Solution proposal' heading line from the copied real
    examples/before-after.md, leaving its body in place -- a minimal
    mutation targeting exactly the heading the check reads, mirroring
    _mutate_artifact_family_section_missing's shape."""
    path = root / BEFORE_AFTER_PATH
    lines = path.read_text(encoding='utf-8').splitlines()
    lines = [l for l in lines if l.strip() != '## Solution proposal']
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_before_after_citation_missing(root):
    """Strip every PF-/MC- token from the '## Demo and discovery material'
    section of the copied real examples/before-after.md, leaving every
    other section's citations in place -- isolates exactly the one
    section-level citation-absence condition this check reads."""
    path = root / BEFORE_AFTER_PATH
    lines = path.read_text(encoding='utf-8').splitlines()
    heading = '## Demo and discovery material'
    start = next(i for i, l in enumerate(lines) if l.strip() == heading)
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith('## '):
            end = j
            break
    token_re = re.compile(r'PF-\d+\.\d+|MC-\d+')
    for j in range(start, end):
        lines[j] = token_re.sub('', lines[j])
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_catalog_opening_rule_count(root):
    """Add a second PF-0 rule to both NUMBERING.md and the checklist, violating
    CAT-03 which requires exactly one opening rule resolving the Before-scenario /
    Identify-Pain / Reframe convergence."""
    path = root / 'NUMBERING.md'
    text = path.read_text(encoding='utf-8')
    text = _insert_table_rows_after_heading(
        text, 'Allocated IDs', ['| PF-0.2 | Mutation second opening rule | SKILL.md | v0.0.0 |'])
    path.write_text(text, encoding='utf-8')

    checklist_path = root / 'skills' / 'proof-first' / 'references' / 'checklist.md'
    checklist_text = checklist_path.read_text(encoding='utf-8')
    checklist_text = _insert_table_rows_after_heading(
        checklist_text, 'PF rules', ['| PF-0.2 | Mutation second opening rule |'])
    checklist_path.write_text(checklist_text, encoding='utf-8')


def _mutate_skill_derivative_stale(root):
    """Change one hex character of the recorded sha256 digest in the
    copied real output-styles/proof-first.md stamp line, mutating only
    the copy -- a minimal mutation targeting exactly the digest the
    check recomputes and compares."""
    path = root / 'output-styles' / 'proof-first.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    for i, line in enumerate(lines):
        m = DERIVATIVE_STAMP_RE.match(line)
        if m:
            digest = m.group(2)
            flipped = ('1' if digest[0] != '1' else '2') + digest[1:]
            lines[i] = line.replace(f"sha256:{digest}", f"sha256:{flipped}")
            break
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_derivative_rule_coverage(root):
    """Delete one '### PF-' rule heading line from the copied real
    prompts/system-prompt.md, leaving its body in place -- a minimal
    mutation targeting exactly the heading shape the check reads."""
    path = root / 'prompts' / 'system-prompt.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    idx = next(i for i, l in enumerate(lines) if l.startswith('### PF-'))
    del lines[idx]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_readme_install_path_missing(root):
    """Delete every line of the copied real README.md containing the
    skills-CLI install command prefix ('npx skills add '), mutating only
    the copy -- removes exactly one of readme-install-path-missing's four
    anchors, leaving the other three untouched."""
    path = root / 'README.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    lines = [l for l in lines if 'npx skills add ' not in l]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_readme_before_after_order(root):
    """Move the copied real README.md's '## Before and after' heading
    line to immediately after its '## Status' heading line, mutating
    only the copy -- moving the one heading line is enough to violate
    the ordering check without relocating the section body it heads."""
    path = root / 'README.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    ba_idx = lines.index(README_BEFORE_AFTER_HEADING)
    line = lines.pop(ba_idx)
    status_idx = lines.index(README_STATUS_HEADING)
    lines.insert(status_idx + 1, line)
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_readme_example_drift(root):
    """Locate the copied real README.md's first line beginning with
    README_CROSS_CHAR and replace one phrase of it with a different
    phrase, mutating only the copy -- reproduces the real failure mode
    this code exists for: README drifting away from the source it names
    itself as reproduced from."""
    path = root / 'README.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    idx = next(i for i, l in enumerate(lines) if l.startswith(README_CROSS_CHAR))
    lines[idx] = lines[idx].replace('Kestrel Systems Group', 'A Different Vendor', 1)
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_readme_example_lead_distance(root):
    """Insert plain filler lines immediately after the copied real
    README.md's title line, pushing its first README_CROSS_CHAR line
    past README_FIRST_EXAMPLE_MAX_LINE, mutating only the copy. The
    filler text carries no PF-/MC--shaped token, because
    check_undefined_id scans README with fences stripped and an
    unallocated token there would make this mutation fire a second,
    unrelated code."""
    path = root / 'README.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    filler = [f"Fixture filler line {n}." for n in range(1, 11)]
    lines = lines[:1] + [''] + filler + lines[1:]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_readme_layout_legend_drift(root):
    """Insert one sentence into the copied real README.md's
    '## Repository layout' section prose, immediately after the heading,
    explaining a quoted "planned" marker the real tree never uses,
    mutating only the copy."""
    path = root / 'README.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    h_idx = next(i for i, l in enumerate(lines) if l.strip() == README_LAYOUT_HEADING)
    lines.insert(h_idx + 1, '')
    lines.insert(h_idx + 2, 'An entry marked "planned" does not yet exist in this repository.')
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_derivative_comparison_claim(root):
    """Append the stale comparison sentence to the copied real
    output-styles/proof-first.md, mutating only the copy.

    Appending rather than replacing is deliberate: the sentence this code
    watches for was deleted from the generator in 04-15 Task 4C, so there is
    no occurrence left in the real tree to edit in place. Putting it back is
    exactly the regression the code exists to catch -- a revert or a bad
    merge restoring the pre-04-15 preamble while the measurement that
    falsifies it sits in evals/routes/RESULTS-routes.md."""
    path = root / DERIVATIVE_PATHS[0]
    text = path.read_text(encoding='utf-8')
    path.write_text(
        text + f"\n{STALE_COMPARISON_CLAIM} a session driven by this file against a session "
        f"with the skill folder installed.\n",
        encoding='utf-8',
    )


def _mutate_stale_benchmark_run_claim(root):
    """Append the pre-06-06 'no benchmark has run' sentence back onto the
    copied real skills/proof-first/references/artifact-patterns.md, mutating
    only the copy.

    Appending rather than replacing, for the same reason as its sibling: the
    sentence was corrected in 06-06 Task 3, so there is no occurrence left in
    the real tree to edit in place. Putting it back into the skill source is
    the exact regression this code exists to catch, and it is the source
    rather than a derivative deliberately -- that is the path the real defect
    took, and the path the sibling code could not see."""
    path = root / 'skills/proof-first/references/artifact-patterns.md'
    text = path.read_text(encoding='utf-8')
    path.write_text(
        text + f"\nIt is not evidence that a convention wins deals; "
        f"{STALE_BENCHMARK_RUN_CLAIM}.\n",
        encoding='utf-8',
    )


def _mutate_readme_output_style_destination(root):
    """Delete every line of the copied real README.md containing the
    shorter, project-level destination literal
    ('.claude/output-styles/'), mutating only the copy. Matching on the
    shorter literal is required: the user-level form
    ('~/.claude/output-styles/') contains the project-level form as a
    substring, so a mutation matching only the longer literal would
    leave the project-level sentence behind, which still satisfies the
    check, and the mutation would silently not fire."""
    path = root / 'README.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    lines = [l for l in lines if '.claude/output-styles/' not in l]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_example_sentence_length(root):
    """Insert one additional sentence of 30 repeated filler words
    immediately before the closing quotation mark of the ✓ line under
    '## Executive summary' in the copied real examples/before-after.md,
    mutating only the copy. Does not touch worked-examples.md: one file
    is enough to demonstrate discrimination, and the self-test already
    proves the second path is read."""
    path = root / BEFORE_AFTER_PATH
    lines = path.read_text(encoding='utf-8').splitlines()
    heading = '## Executive summary'
    start = next(i for i, l in enumerate(lines) if l.strip() == heading)
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith('## '):
            end = j
            break
    check_idx = next(j for j in range(start, end) if lines[j].startswith('✓'))
    filler_sentence = ' '.join(['filler'] * 30) + '.'
    line = lines[check_idx].rstrip()
    lines[check_idx] = line[:-1] + ' ' + filler_sentence + '"'
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_before_after_spelled_count(root):
    """Insert ' across seven bidders' immediately before the closing
    period of the ✓ line under '## RFP and RFI response' in the copied
    real examples/before-after.md, mutating only the copy. 'seven' and
    'bidders' appear nowhere in the real repaired prose, so the mutation
    is unambiguously the thing under test."""
    path = root / BEFORE_AFTER_PATH
    lines = path.read_text(encoding='utf-8').splitlines()
    heading = '## RFP and RFI response'
    start = next(i for i, l in enumerate(lines) if l.strip() == heading)
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith('## '):
            end = j
            break
    check_idx = next(j for j in range(start, end) if lines[j].startswith('✓'))
    line = lines[check_idx].rstrip()
    lines[check_idx] = line[:-2] + ' across seven bidders."'
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_example_rule_narration(root):
    """Insert one short sentence pairing the 'rather than' connective
    with the 'a generic strength' meta term immediately before the
    closing quotation mark of the ✓ line under '## Solution proposal'
    in the copied real examples/before-after.md, mutating only the
    copy."""
    path = root / BEFORE_AFTER_PATH
    lines = path.read_text(encoding='utf-8').splitlines()
    heading = '## Solution proposal'
    start = next(i for i, l in enumerate(lines) if l.strip() == heading)
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith('## '):
            end = j
            break
    check_idx = next(j for j in range(start, end) if lines[j].startswith('✓'))
    narration_sentence = 'This capability is demonstrated rather than a generic strength.'
    line = lines[check_idx].rstrip()
    lines[check_idx] = line[:-1] + ' ' + narration_sentence + '"'
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_source_row_unconfirmed(root):
    """Re-mark the real SOURCES.md's one confirmed row as `verified` with
    its evidence stripped back to the pre-confirmation placeholder -- the
    exact defect this code exists to catch: a row hand-edited to claim
    provenance that was never recorded. Mutating the real file rather than
    a fixture is what makes the code discrimination-proven instead of
    merely registered."""
    path = root / SOURCES_PATH
    lines = path.read_text(encoding='utf-8').splitlines()
    idx = next(
        i for i, line in enumerate(lines)
        if line.startswith('| ') and '| verified |' in line
    )
    cells = lines[idx].strip().strip('|').split('|')
    cells[-1] = ' to confirm at LEG-04 '
    lines[idx] = '|' + '|'.join(cells) + '|'
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_source_gate_incomplete(root):
    """Flip one real SOURCES.md row's Status back to `unverified` while the
    real LEGAL-REVIEW.md keeps declaring the gate PASSED -- the defect this
    code exists to catch: a pass declared over a list that is not finished."""
    path = root / SOURCES_PATH
    lines = path.read_text(encoding='utf-8').splitlines()
    idx = next(
        i for i, line in enumerate(lines)
        if line.startswith('| ') and '| verified |' in line
    )
    lines[idx] = lines[idx].replace('| verified |', '| unverified |', 1)
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_framework_statement_stale_review(root):
    """Roll one real NOTICES.md statement's `Last reviewed:` date back to
    2026-09-10, the date it carried before this review, while
    LEGAL-REVIEW.md keeps its later review date -- the defect being a
    statement the review claims to have re-read and did not."""
    path = root / 'NOTICES.md'
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    idx = next(i for i, line in enumerate(lines) if line.startswith('Last reviewed: '))
    lines[idx] = 'Last reviewed: 2026-09-10'
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_readme_claim_unsourced(root):
    """Insert a fabricated figure into the real README's claim region --
    a number that appears in no committed results file, which is the
    defect this code exists to catch."""
    path = root / 'README.md'
    text = path.read_text(encoding='utf-8')
    marker = CLAIM_REGION_START
    idx = text.find(marker) + len(marker)
    fabricated = (
        "\n\nMeasured 2026-09-18 across `claude-opus-5` and `claude-sonnet-5`: "
        "buyers rated the output 91743 points higher.\n"
    )
    path.write_text(text[:idx] + fabricated + text[idx:], encoding='utf-8')


def _mutate_readme_claim_unanchored(root):
    """Strip the model strings out of one real claim-region paragraph,
    leaving its figures standing with nothing behind them."""
    path = root / 'README.md'
    text = path.read_text(encoding='utf-8')
    start = text.find(CLAIM_REGION_START)
    end = text.find(CLAIM_REGION_END)
    region = text[start:end]
    for model in CLAIM_MODEL_STRINGS:
        region = region.replace(model, 'the tested model')
    path.write_text(text[:start] + region + text[end:], encoding='utf-8')


def _mutate_readme_badge_unlisted(root):
    """Hang a shields.io badge carrying a number on the real README."""
    path = root / 'README.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    lines.insert(1, '![quality](https://img.shields.io/badge/quality-98%25-brightgreen.svg)')
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _mutate_readme_layout_tree_stale(root):
    """Delete the routes/ line from the real README's layout tree, the
    exact omission that shipped undetected before this code existed."""
    path = root / 'README.md'
    lines = path.read_text(encoding='utf-8').splitlines()
    kept = [l for l in lines if not (l.strip().endswith('routes/') and '─' in l)]
    path.write_text('\n'.join(kept) + '\n', encoding='utf-8')


def _mutate_record_citation_unresolvable(root):
    """Push the high bound of the real LEGAL-REVIEW.md's first `path`:N-M
    citation past the end of the file it names, which is what a citation
    does on its own when the cited file is shortened under it. Operates on
    the real record and the real cited file, so this proves the code fires
    against this repository's production citation shape rather than only
    against the fixture."""
    path = root / LEGAL_REVIEW_PATH
    text = path.read_text(encoding='utf-8')
    match = next(
        m for m in CITATION_RE.finditer(text)
        if m.group(3) is not None
    )
    broken = f'`{match.group(1)}`:{match.group(2)}-999999'
    path.write_text(text[:match.start()] + broken + text[match.end():], encoding='utf-8')


MUTATIONS = [
    ('dup-id', "insert the same allocated-ID row twice into NUMBERING.md's Allocated IDs table", _mutate_dup_id),
    ('range-id', "insert an allocated-ID row whose PF number sits above its section's declared ceiling", _mutate_range_id),
    ('revived-id', "insert the same ID into both the Allocated IDs table and the Deprecated IDs table", _mutate_revived_id),
    ('undefined-id', "cite a PF ID in README.md that no Allocated IDs row defines", _mutate_undefined_id),
    ('dup-figure-key', "duplicate the first data row of the Canonical figures table", _mutate_dup_figure_key),
    ('figure-order', "move the Canonical figures table's last data row to the top", _mutate_figure_order),
    ('unlisted-figure', "append a stray currency token after the Canonical figures table, the file's last section", _mutate_unlisted_figure),
    ('pointer-missing', "remove the canonical pointer line from README.md", _mutate_pointer_missing),
    ('pointer-duplicated', "append a second copy of the canonical pointer line to README.md", _mutate_pointer_duplicated),
    ('pointer-unparseable', "remove the Attribution pointer heading from NOTICES.md", _mutate_pointer_unparseable),
    ('license-missing', "delete the LICENSE file from the repository root", _mutate_license_missing),
    ('readme-results-pointer-missing', "delete every line of README.md containing the results-pointer path", _mutate_readme_results_pointer_missing),
    ('results-breakdown-count-mismatch', "raise the real results file's Arm A no-family bullet's stated count above its own enumeration sum", _mutate_results_breakdown_count_mismatch),
    ('source-row-unconfirmed', "strip the real SOURCES.md's one confirmed row back to its pre-confirmation placeholder while leaving its status reading verified", _mutate_source_row_unconfirmed),
    ('readme-claim-unsourced', "insert a fabricated figure into the real README's claim region that no committed results file sources", _mutate_readme_claim_unsourced),
    ('readme-claim-unanchored', "strip the model strings out of the real README's claim region, leaving its figures unanchored", _mutate_readme_claim_unanchored),
    ('readme-badge-unlisted', "hang a numeric shields.io badge on the real README", _mutate_readme_badge_unlisted),
    ('readme-layout-tree-stale', "delete the routes/ line from the real README's repository-layout tree", _mutate_readme_layout_tree_stale),
    ('source-gate-incomplete', "flip one real SOURCES.md row back to unverified while LEGAL-REVIEW.md keeps declaring the gate PASSED", _mutate_source_gate_incomplete),
    ('framework-statement-stale-review', "roll one real NOTICES.md statement's Last reviewed date back behind LEGAL-REVIEW.md's review date", _mutate_framework_statement_stale_review),
    ('framework-statement-missing', "delete the NOTICES.md file entirely from the repository root", _mutate_framework_statement_missing),
    ('record-citation-unresolvable', "push the high bound of the real LEGAL-REVIEW.md's first line-range citation past the end of the file it names", _mutate_record_citation_unresolvable),
    ('catalog-id-drift', "delete one PF data row from references/checklist.md's PF rules table", _mutate_catalog_id_drift),
    ('catalog-opening-rule-count', "add a second PF-0 rule to NUMBERING.md and checklist.md, violating CAT-03's exactly-one requirement", _mutate_catalog_opening_rule_count),
    ('frontmatter-unparseable', "remove the opening '---' line from the real skills/proof-first/SKILL.md frontmatter block", _mutate_frontmatter_unparseable),
    ('frontmatter-unknown-key', "add an 'author:' key (outside the six-key allow-list) to the real skills/proof-first/SKILL.md frontmatter block", _mutate_frontmatter_unknown_key),
    ('frontmatter-name-mismatch', "change the real skills/proof-first/SKILL.md frontmatter's name value so it no longer equals its parent directory", _mutate_frontmatter_name_mismatch),
    ('frontmatter-description-invalid', "truncate the real skills/proof-first/SKILL.md frontmatter description to a few characters", _mutate_frontmatter_description_invalid),
    ('catalog-count-unstated', "delete the stated-count line from the real skills/proof-first/SKILL.md", _mutate_catalog_count_unstated),
    ('catalog-count-mismatch', "change the rule-count number in the real skills/proof-first/SKILL.md's stated-count line", _mutate_catalog_count_mismatch),
    ('skill-too-long', "append filler lines to the real skills/proof-first/SKILL.md past its 500-line ceiling", _mutate_skill_too_long),
    ('skill-token-budget-exceeded', "append filler words to the real skills/proof-first/SKILL.md, an under-ceiling control, pushing its estimated token count over the ceiling", _mutate_skill_token_budget_exceeded),
    ('mc-catalog-id-drift', "delete the single MC data row from references/checklist.md's MC rules table", _mutate_mc_catalog_id_drift),
    ('mc-rule-in-skill', "insert an MC-shaped rule heading into the real skills/proof-first/SKILL.md", _mutate_mc_rule_in_skill),
    ('mc-count-unstated', "delete the stated-count line from the real skills/proof-first/references/completeness-audit.md", _mutate_mc_count_unstated),
    ('mc-count-mismatch', "change the checks number in the real skills/proof-first/references/completeness-audit.md's stated-count line", _mutate_mc_count_mismatch),
    ('artifact-family-section-missing', "delete the '## Solution proposal' heading from the real skills/proof-first/references/artifact-patterns.md, leaving its body in place", _mutate_artifact_family_section_missing),
    ('skill-family-line-gate-missing', "delete the family-line pass item from the real skills/proof-first/SKILL.md's self-check section, leaving the heading and other two passes in place", _mutate_skill_family_line_gate_missing),
    ('skill-family-order-gate-missing', "replace the ordering pass wording with pre-03-11 presence-only wording in the real skills/proof-first/SKILL.md's self-check section, leaving the family-line presence anchors and other two passes in place", _mutate_skill_family_order_gate_missing),
    ('source-label-in-skill-content', "insert the frozen 'economic buyer' label into the real skills/proof-first/references/artifact-patterns.md", _mutate_source_label_in_skill_content),
    ('plugin-manifest-version-mismatch', "change the real .claude-plugin/plugin.json version so it no longer equals the skill frontmatter's metadata.version", _mutate_plugin_manifest_version_mismatch),
    ('plugin-manifest-invalid', "delete the required 'license' key from the real .claude-plugin/plugin.json", _mutate_plugin_manifest_invalid),
    ('plugin-manifest-invalid', "delete the required 'license' key from the real .claude-plugin/marketplace.json's plugin entry", _mutate_marketplace_entry_required_key_missing),
    ('publish-location-drift', "rewrite the real .claude-plugin/marketplace.json plugin entry's repository to a different owner/repo than plugin.json states", _mutate_publish_location_drift),
    ('before-after-family-missing', "delete the '## Solution proposal' heading from the real examples/before-after.md, leaving its body in place", _mutate_before_after_family_missing),
    ('before-after-citation-missing', "strip every PF-/MC- token from the '## Demo and discovery material' section of the real examples/before-after.md", _mutate_before_after_citation_missing),
    ('skill-derivative-stale', "change one hex character of the recorded sha256 in the real output-styles/proof-first.md stamp", _mutate_skill_derivative_stale),
    ('derivative-rule-coverage-incomplete', "delete one '### PF-' rule heading line from the real prompts/system-prompt.md, leaving its body in place", _mutate_derivative_rule_coverage),
    ('readme-install-path-missing', "delete every line of the real README.md containing the skills-CLI install command prefix", _mutate_readme_install_path_missing),
    ('readme-before-after-order', "move the real README.md's '## Before and after' heading line to immediately after its '## Status' heading line", _mutate_readme_before_after_order),
    ('example-sentence-length', "insert one 30-word filler sentence into the real examples/before-after.md's Executive summary ✓ line, past PF-4.1's 25-word ceiling", _mutate_example_sentence_length),
    ('before-after-spelled-count', "insert 'seven bidders' into the real examples/before-after.md's RFP and RFI response ✓ line, a word-spelled cardinal that routes around unlisted-figure's digit-shaped interface", _mutate_before_after_spelled_count),
    ('example-rule-narration', "insert a 'rather than a generic strength' narration sentence into the real examples/before-after.md's Solution proposal ✓ line", _mutate_example_rule_narration),
    ('readme-example-drift', "change one phrase of the real README.md's first ✗ line, breaking its promised reproduction from examples/before-after.md", _mutate_readme_example_drift),
    ('readme-example-lead-distance', "insert plain filler lines after the real README.md's title line, pushing its first ✗ line past the frozen 20-line ceiling", _mutate_readme_example_lead_distance),
    ('readme-layout-legend-drift', "insert a sentence explaining a quoted 'planned' marker into the real README.md's Repository layout section prose, which the real tree never uses", _mutate_readme_layout_legend_drift),
    ('readme-output-style-destination-missing', "delete every line of the real README.md containing the project-level output-style destination directory", _mutate_readme_output_style_destination),
    ('derivative-comparison-claim-stale', "append the pre-04-15 'No benchmark has compared' sentence back onto the real output-styles/proof-first.md, while evals/routes/RESULTS-routes.md sits in the tree disproving it", _mutate_derivative_comparison_claim),
    ('benchmark-run-claim-stale', "append the pre-06-06 'no benchmark has run' sentence back onto the real skills/proof-first/references/artifact-patterns.md, while evals/benchmark/RESULTS.md sits in the tree recording 96 generations", _mutate_stale_benchmark_run_claim),
]


def mutation_test(repo_root):
    """Run a clean control copy, then one isolated mutation per violation
    code, and report per-code pass/fail. A code only counts as
    discrimination-proven when it was silent on the control copy and fires
    on its mutated copy -- silent-then-fires is what actually demonstrates
    the check can tell good content from bad. A code that already fires on
    the control copy cannot demonstrate that, even if it also fires after
    the mutation, so it is counted separately as confirmed-fire-only and
    never folded into the discrimination-proven total. This makes the
    tool's own printed claim state-independent: the comparison runs for
    every code regardless of whether the control happens to be clean, so a
    future drift back over a ceiling degrades what is printed instead of
    silently invalidating it. Returns True only when the control had no
    *unexpected* violations (KNOWN_OPEN_VIOLATIONS aside -- see that
    constant's own comment), every mutation fired its expected code, and
    every code in ALL_CHECK_CODES has a registered mutation. A
    confirmed-fire-only code does not by itself fail the run -- it makes
    the run disclose rather than fail."""
    all_ok = True
    discrimination_proven = set()
    fire_only = set()

    with tempfile.TemporaryDirectory(prefix='check-repo-mutation-control-') as tmp:
        control_root = Path(tmp) / 'control'
        _copy_repo_subset(repo_root, control_root)
        control_violations = run_all_checks(control_root)
        unexpected_control_violations = [
            v for v in control_violations
            if v[1].split(' ', 1)[0] not in KNOWN_OPEN_VIOLATIONS
        ]
        known_count = len(control_violations) - len(unexpected_control_violations)
        print(
            f"mutation-test CONTROL: {len(control_violations)} violations on the unmutated copy "
            f"({known_count} known-open per KNOWN_OPEN_VIOLATIONS, {len(unexpected_control_violations)} unexpected)"
        )
        if unexpected_control_violations:
            all_ok = False
        # The control copy is the identical pre-state for every mutation --
        # every scratch root below starts from the same _copy_repo_subset of
        # the same tree -- so this one control run is a sound pre-state for
        # all of them; no second control run per mutation is needed.
        control_codes = {v[1].split(' ', 1)[0] for v in control_violations}

    for code, description, mutate_fn in MUTATIONS:
        with tempfile.TemporaryDirectory(prefix=f'check-repo-mutation-{code}-') as tmp:
            scratch_root = Path(tmp) / 'scratch'
            _copy_repo_subset(repo_root, scratch_root)
            mutate_fn(scratch_root)
            violations = run_all_checks(scratch_root)
            fired = any(line.split(' ', 1)[0] == code for _, line in violations)
        if not fired:
            print(f"mutation-test FAIL: {code} {description}")
            all_ok = False
        elif code in control_codes:
            fire_only.add(code)
            print(
                f"mutation-test FIRE-ONLY: {code} {description} "
                f"(the control copy was already non-clean for this code, so this mutation "
                f"cannot demonstrate discrimination between good content and bad)"
            )
        else:
            discrimination_proven.add(code)
            print(f"mutation-test OK: {code} {description}")

    uncovered = [c for c in ALL_CHECK_CODES if c not in {m[0] for m in MUTATIONS}]
    for code in uncovered:
        print(f"mutation-test FAIL: {code} has no registered mutation")
        all_ok = False

    if all_ok:
        print(f"mutation-test PASS: {len(discrimination_proven)} codes discrimination-proven")
        if fire_only:
            print(
                f"mutation-test PASS: {len(fire_only)} codes confirmed-fire-only, not "
                f"discrimination-proven ({', '.join(sorted(fire_only))}) -- see the FIRE-ONLY "
                f"line above for each one's reason"
            )
    else:
        failed = len(ALL_CHECK_CODES) - len(discrimination_proven) - len(fire_only)
        print(f"mutation-test FAILED: {failed} codes not discrimination-proven")

    return all_ok


# ---------------------------------------------------------------------------
# Self-test fixtures
# ---------------------------------------------------------------------------

def _write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def _bad_numbering():
    return """## PF reserved ranges
| Section | Range | Concern | Allocated | Next free |
|---|---|---|---|---|
| PF-0 | PF-0.1-PF-0.9 | Opening | 1 | PF-0.2 |
| PF-1 | PF-1.1-PF-1.4 | Structure | 0 | PF-1.1 |

## MC reserved blocks
| Dimension | Range |
|---|---|
| Metric | MC-1-MC-5 |
| Economic Buyer | MC-8-MC-10 |

## Allocated IDs
| ID | Title | Defined in | Added in |
|---|---|---|---|
| PF-0.1 | Opening rule | SKILL.md | v1.0.0 |
| PF-0.1 | Opening rule dup | SKILL.md | v1.0.0 |
| PF-1.9 | Out of range rule | SKILL.md | v1.0.0 |
| MC-6 | Gap-landing rule | SKILL.md | v1.0.0 |
| MC-99 | Out of range MC | SKILL.md | v1.0.0 |
| PF-0.5 | Revived rule | SKILL.md | v1.0.0 |

## Deprecated IDs
| ID | Deprecated in | Absorbed by |
|---|---|---|
| PF-0.5 | v1.1.0 | PF-0.1 |
"""


def _good_numbering():
    return """## PF reserved ranges
| Section | Range | Concern | Allocated | Next free |
|---|---|---|---|---|
| PF-0 | PF-0.1-PF-0.9 | Opening | 1 | PF-0.2 |
| PF-1 | PF-1.1-PF-1.4 | Structure | 0 | PF-1.1 |

## MC reserved blocks
| Dimension | Range |
|---|---|
| Metric | MC-1-MC-5 |

## Allocated IDs
| ID | Title | Defined in | Added in |
|---|---|---|---|
| PF-0.1 | Opening rule | SKILL.md | v1.0.0 |
| MC-1 | Lower boundary rule | SKILL.md | v1.0.0 |
| MC-5 | Upper boundary rule | SKILL.md | v1.0.0 |

## Deprecated IDs
| ID | Deprecated in | Absorbed by |
|---|---|---|
"""


def _bad_deal_brief():
    return """## Canonical figures
| Key | Value | Type | What it is |
|---|---|---|---|
| total-contract-value | $6,000,000 | currency | Total contract value |
| bidder-count | 3 | count | Number of bidders |
| bidder-count | 4 | count | Duplicate key |

A stray figure of $999,999,999 appears after the table, with no further heading in this fixture.
"""


def _good_deal_brief():
    return """## Canonical figures
| Key | Value | Type | What it is |
|---|---|---|---|
| audit-fee-rate | 5% | percent | Fee rate charged for the audit engagement |
| bidder-count | 3 | count | Number of bidders |
| escrow-fee-rate | 5% | percent | Fee rate charged for the escrow arrangement |
| total-contract-value | $6,000,000 | currency | Total contract value |

The escrow fee rate is 5%, a value-collision fixture pinning the documented matching ceiling.
This trailing line sits after the table's last row and cites no currency, percentage, or date.
"""


def _bad_notices():
    return """## Attribution pointer

The following string is the canonical, verbatim attribution pointer. A human contributor and
`tools/check_repo.py` both read this fenced block as the single source of truth for the string.

```
Test pointer string.
```

### Files required to carry it

- `carrier-missing.md`
- `carrier-dup.md`
- `carrier-lookalike.md`

## Framework statements

The three headings below are present but carry neither the non-affiliation nor the
rights-holder language, and each is dated before the review that claims to have read it --
so framework-statement-missing and framework-statement-stale-review both fire on this root.

### Command of the Message

Last reviewed: 2026-09-10

### MEDDIC, MEDDICC, and related marks

Last reviewed: 2026-09-10

### Challenger

Last reviewed: 2026-09-10
"""


def _good_notices():
    return """## Attribution pointer

The following string is the canonical, verbatim attribution pointer. A human contributor and
`tools/check_repo.py` both read this fenced block as the single source of truth for the string.

```
Test pointer string.
```

### Files required to carry it

- `carrier-ok.md`

## Framework statements

The three statements below appear in a fixed order.

### Command of the Message

**Mark:** Command of the Message

**Rights-holder:** Force Management.

**Non-affiliation:** This project is not affiliated with, endorsed by, sponsored by, or connected
to Force Management.

**Paraphrase boundary:** This repository restates concepts.

### MEDDIC, MEDDICC, and related marks

**Mark:** MEDDIC, MEDDICC, MEDDPICC.

**Rights-holder:** Multiple parties.

**Non-affiliation:** This project is not affiliated with any party claiming rights.

**Paraphrase boundary:** This repository restates concepts.

### Challenger

**Mark:** Challenger.

**Rights-holder:** Challenger Inc.

**Non-affiliation:** This project is not affiliated with Challenger Inc.

**Paraphrase boundary:** This repository restates concepts.
"""


def _unparseable_notices():
    return """## Attribution pointer

The following string is the canonical, verbatim attribution pointer, but this fixture omits the
fenced block entirely so the section yields no usable pointer definition.

### Files required to carry it

- `carrier-ok.md`
"""


def _escaping_notices():
    return """## Attribution pointer

The following string is the canonical, verbatim attribution pointer. A human contributor and
`tools/check_repo.py` both read this fenced block as the single source of truth for the string.

```
Test pointer string.
```

### Files required to carry it

- `../escaped.md`
"""


def _bad_license():
    return ""  # Empty file


def _good_license():
    return """MIT License

Copyright (c) 2026 Proof First contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
"""


def _bad_notices_frameworks():
    return """## Framework statements

The three statements below appear in a fixed order, and each carries the same four labelled
elements in the same order, so a future diff to this section shows a content change and never a
reordering.

### MEDDIC, MEDDICC, and related marks

**Mark:** MEDDIC, MEDDICC, MEDDPICC, and related marks in this family.

**Rights-holder:** Ownership of these marks is claimed by multiple parties and is contested.

**Non-affiliation:** This project is not affiliated with, endorsed by, or sponsored by any party
claiming rights in these marks.

**Paraphrase boundary:** This repository restates concepts associated with this family of marks in
its own words and reproduces no training material.

### Challenger

**Mark:** Challenger (the Challenger Sale methodology).

**Rights-holder:** Challenger Inc. and its trademark successors.

**Non-affiliation:** This project is not affiliated with, endorsed by, sponsored by, or connected
to Challenger Inc. or its trademark successors.

**Paraphrase boundary:** This repository restates concepts associated with Challenger in its own
words and reproduces no training material.
"""


def _good_notices_frameworks():
    return """## Framework statements

The three statements below appear in a fixed order, and each carries the same four labelled
elements in the same order, so a future diff to this section shows a content change and never a
reordering.

### Command of the Message

**Mark:** Command of the Message

**Rights-holder:** Force Management.

**Non-affiliation:** This project is not affiliated with, endorsed by, sponsored by, or connected
to Force Management.

**Paraphrase boundary:** This repository restates concepts associated with Command of the Message
in its own words and reproduces no training material, no course content, and no proprietary
diagram belonging to Force Management.

### MEDDIC, MEDDICC, and related marks

**Mark:** MEDDIC, MEDDICC, MEDDPICC, and related marks in this family.

**Rights-holder:** Ownership of these marks is claimed by multiple parties and is contested.

**Non-affiliation:** This project is not affiliated with, endorsed by, or sponsored by any party
claiming rights in these marks.

**Paraphrase boundary:** This repository restates concepts associated with this family of marks in
its own words and reproduces no training material, no course content, and no proprietary diagram
belonging to any claimant.

### Challenger

**Mark:** Challenger (the Challenger Sale methodology).

**Rights-holder:** Challenger Inc. and its trademark successors.

**Non-affiliation:** This project is not affiliated with, endorsed by, sponsored by, or connected
to Challenger Inc. or its trademark successors.

**Paraphrase boundary:** This repository restates concepts associated with Challenger in its own
words and reproduces no training material, no course content, and no proprietary diagram belonging
to Challenger Inc. or its trademark successors.
"""


def _good_skill():
    return "### PF-0.1 — Opening rule\n\nBody text for the opening rule.\n"


def _bad_skill():
    return "### PF-9.9 — Mutation-only rule\n\nBody text citing no registered ID.\n"


def _good_checklist():
    return """## PF rules

| ID | Rule |
|---|---|
| PF-0.1 | Opening rule |
"""


def _bad_checklist():
    return """## PF rules

| ID | Rule |
|---|---|
"""


def _good_frontmatter():
    return (
        "---\n"
        "name: good-skill\n"
        "description: |\n"
        f"  {'x' * DESCRIPTION_MIN}\n"
        "license: MIT\n"
        "metadata:\n"
        "  version: \"1.0.0\"\n"
        "---\n"
        "\n# Good skill\n\nBody text.\n"
    )


def _bad_frontmatter():
    """One root, three codes: an unknown 'author' key (not one of the six
    allowed keys -- 'compatibility' is allowed and deliberately not used
    here, see _mutate_frontmatter_unknown_key), a name that differs from
    its own directory, and a three-character description."""
    return (
        "---\n"
        "name: wrong-name\n"
        "description: hi\n"
        "author: Someone Else\n"
        "---\n"
        "\n# Bad skill\n\nBody text.\n"
    )


def _dupkey_frontmatter():
    return (
        "---\n"
        "name: dupkey-skill\n"
        "name: dupkey-skill-again\n"
        f"description: {'x' * (DESCRIPTION_MIN + 10)}\n"
        "---\n"
        "\n# Dup key skill\n\nBody text.\n"
    )


def _reordered_frontmatter():
    """The same allowed keys as _good_frontmatter, in a different order,
    still valid -- and its description is exactly DESCRIPTION_MAX
    characters, the upper boundary, which must also stay silent."""
    return (
        "---\n"
        "license: MIT\n"
        "metadata:\n"
        "  version: \"1.0.0\"\n"
        "description: |\n"
        f"  {'x' * DESCRIPTION_MAX}\n"
        "name: reordered-skill\n"
        "---\n"
        "\n# Reordered skill\n\nBody text.\n"
    )


def _overmax_frontmatter():
    """Description at DESCRIPTION_MAX + 1 -- the one character past the
    ceiling that must fire, isolated from every other frontmatter code."""
    return (
        "---\n"
        "name: overmax-skill\n"
        f"description: {'x' * (DESCRIPTION_MAX + 1)}\n"
        "---\n"
        "\n# Overmax skill\n\nBody text.\n"
    )


def _plugin_fixture_skill(version):
    """A minimal, valid SKILL.md fixture at skills/proof-first/ whose
    frontmatter metadata.version is the given string -- the source of
    truth the plugin-manifest-version-mismatch fixtures below compare
    their manifests against."""
    return (
        "---\n"
        "name: proof-first\n"
        f"description: {'x' * DESCRIPTION_MIN}\n"
        "license: MIT\n"
        "metadata:\n"
        f"  version: \"{version}\"\n"
        "---\n"
        "\n# Proof First\n\nBody text.\n"
    )


def _plugin_manifest_json(version, name='proof-first'):
    return json.dumps({
        'name': name,
        'displayName': 'Proof First',
        'description': 'Fixture description.',
        'version': version,
        'author': {'name': 'Test'},
        'homepage': 'https://github.com/<owner>/<repo>',
        'repository': 'https://github.com/<owner>/<repo>',
        'license': 'MIT',
        'keywords': ['presales'],
    }, indent=2) + '\n'


def _marketplace_manifest_json(version, name='proof-first', source='./'):
    return json.dumps({
        'name': name,
        'owner': {'name': 'Test', 'url': 'https://github.com/<owner>'},
        'description': 'Fixture description.',
        'plugins': [{
            'name': name,
            'source': source,
            'displayName': 'Proof First',
            'description': 'Fixture description.',
            'version': version,
            'author': {'name': 'Test'},
            'homepage': 'https://github.com/<owner>/<repo>',
            'repository': 'https://github.com/<owner>/<repo>',
            'license': 'MIT',
            'keywords': ['presales'],
        }],
    }, indent=2) + '\n'


def _good_plugin_manifests(root):
    """A skill fixture stating version '0.1.0' and both manifests agreeing
    with it and with each other -- silent on plugin-manifest-version-
    mismatch."""
    _write(root / 'skills' / 'proof-first' / 'SKILL.md', _plugin_fixture_skill('0.1.0'))
    _write(root / PLUGIN_MANIFEST_PATH, _plugin_manifest_json('0.1.0'))
    _write(root / MARKETPLACE_MANIFEST_PATH, _marketplace_manifest_json('0.1.0'))


def _bad_plugin_manifests(root):
    """The skill fixture states '0.1.0'; plugin.json states '9.9.9' instead
    -- disagreeing with its own fixture SKILL.md, so
    plugin-manifest-version-mismatch must fire naming plugin.json.
    marketplace.json is left agreeing with the skill so this root isolates
    the one code under test."""
    _write(root / 'skills' / 'proof-first' / 'SKILL.md', _plugin_fixture_skill('0.1.0'))
    _write(root / PLUGIN_MANIFEST_PATH, _plugin_manifest_json('9.9.9'))
    _write(root / MARKETPLACE_MANIFEST_PATH, _marketplace_manifest_json('0.1.0'))


def _invalid_plugin_manifests(root):
    """A root isolating plugin-manifest-invalid: plugin.json is missing its
    required 'license' key and its name 'wrong-name' differs from the
    shipped skill folder 'proof-first'. marketplace.json is left
    well-formed and agreeing with plugin.json's version, so this root
    fires plugin-manifest-invalid only."""
    _write(root / 'skills' / 'proof-first' / 'SKILL.md', _plugin_fixture_skill('0.1.0'))
    data = json.loads(_plugin_manifest_json('0.1.0', name='wrong-name'))
    data.pop('license')
    _write(root / PLUGIN_MANIFEST_PATH, json.dumps(data, indent=2) + '\n')
    _write(root / MARKETPLACE_MANIFEST_PATH, _marketplace_manifest_json('0.1.0', name='wrong-name'))


def _bad_marketplace_shape(root):
    """A root isolating the marketplace-shape half of plugin-manifest-
    invalid: an empty 'plugins' array. plugin.json is left well-formed so
    this root fires plugin-manifest-invalid for marketplace.json alone."""
    _write(root / 'skills' / 'proof-first' / 'SKILL.md', _plugin_fixture_skill('0.1.0'))
    _write(root / PLUGIN_MANIFEST_PATH, _plugin_manifest_json('0.1.0'))
    data = json.loads(_marketplace_manifest_json('0.1.0'))
    data['plugins'] = []
    _write(root / MARKETPLACE_MANIFEST_PATH, json.dumps(data, indent=2) + '\n')


def _marketplace_entry_missing_key_manifests(root):
    """The fixture-world counterpart of _invalid_plugin_manifests, which
    removes the required 'license' key from plugin.json: good manifests
    via the same construction _good_plugin_manifests uses, with 'license'
    removed from marketplace.json's plugins[0] entry only. plugin.json is
    left well-formed and version-matched, so this root isolates the
    marketplace-entry half of plugin-manifest-invalid -- the half CR-01
    found untested."""
    _write(root / 'skills' / 'proof-first' / 'SKILL.md', _plugin_fixture_skill('0.1.0'))
    _write(root / PLUGIN_MANIFEST_PATH, _plugin_manifest_json('0.1.0'))
    data = json.loads(_marketplace_manifest_json('0.1.0'))
    data['plugins'][0].pop('license', None)
    _write(root / MARKETPLACE_MANIFEST_PATH, json.dumps(data, indent=2) + '\n')


def _required_key_matrix_root(root, position, key):
    """Build one cell of the required-key coverage matrix: well-formed,
    version-matched plugin and marketplace manifests with a single named
    key deleted from the object named by `position` -- one of the two
    literal strings 'plugin.json' or "marketplace.json's plugin entry",
    chosen so a failure message reads cleanly and names which object the
    key was deleted from. Its job is to prove plugin-manifest-invalid
    fires for every key PLUGIN_REQUIRED_KEYS declares, at every position
    the docstring claims to enforce it -- not just the one key at the one
    position a single hand-built fixture happens to sample, which is
    exactly the gap CR-01 left open."""
    _write(root / 'skills' / 'proof-first' / 'SKILL.md', _plugin_fixture_skill('0.1.0'))
    plugin_data = json.loads(_plugin_manifest_json('0.1.0'))
    marketplace_data = json.loads(_marketplace_manifest_json('0.1.0'))
    if position == 'plugin.json':
        plugin_data.pop(key, None)
    else:
        marketplace_data['plugins'][0].pop(key, None)
    _write(root / PLUGIN_MANIFEST_PATH, json.dumps(plugin_data, indent=2) + '\n')
    _write(root / MARKETPLACE_MANIFEST_PATH, json.dumps(marketplace_data, indent=2) + '\n')


def _marketplace_entry_field_drift_manifests(root):
    """A root isolating the WR-02 equality half of plugin-manifest-invalid:
    good manifests via the same construction _good_plugin_manifests uses,
    with marketplace.json's plugins[0]['keywords'] changed to a value that
    disagrees with plugin.json's, while both remain present and
    well-formed -- so this root fires plugin-manifest-invalid for the
    equality guard alone, and only for the equality guard, never the
    required-key loop (both sides still carry every key)."""
    _write(root / 'skills' / 'proof-first' / 'SKILL.md', _plugin_fixture_skill('0.1.0'))
    _write(root / PLUGIN_MANIFEST_PATH, _plugin_manifest_json('0.1.0'))
    data = json.loads(_marketplace_manifest_json('0.1.0'))
    data['plugins'][0]['keywords'] = ['a-different-keyword']
    _write(root / MARKETPLACE_MANIFEST_PATH, json.dumps(data, indent=2) + '\n')


def _publish_location_drift_manifests(root):
    """A root isolating publish-location-drift: plugin.json states one
    owner, marketplace.json's plugin entry states a different one for
    'repository' -- both manifests are otherwise well-formed and version-
    matched, so this root fires publish-location-drift only."""
    _write(root / 'skills' / 'proof-first' / 'SKILL.md', _plugin_fixture_skill('0.1.0'))
    _write(root / PLUGIN_MANIFEST_PATH, _plugin_manifest_json('0.1.0'))
    data = json.loads(_marketplace_manifest_json('0.1.0'))
    data['plugins'][0]['repository'] = 'https://github.com/someone/else'
    _write(root / MARKETPLACE_MANIFEST_PATH, json.dumps(data, indent=2) + '\n')


def _mixed_url_form_manifests(root):
    """A root isolating the WR-01 false positive this task fixes: all
    three publish-location carrier positions name the same owner, acme,
    but each writes it in a different GitHub URL syntax -- plugin.json's
    `repository` in the SSH form, marketplace.json's plugin entry
    `repository` in the HTTPS form, and marketplace.json's `owner.url` in
    the scheme-less form. Built by the same construction
    _good_plugin_manifests uses -- same required keys, same version
    agreement with the fixture skill -- so this root is silent on
    plugin-manifest-version-mismatch and plugin-manifest-invalid and
    must be silent on publish-location-drift too, once _owner_segment
    normalises all three syntaxes to the same owner."""
    _write(root / 'skills' / 'proof-first' / 'SKILL.md', _plugin_fixture_skill('0.1.0'))

    plugin_data = json.loads(_plugin_manifest_json('0.1.0'))
    plugin_data['homepage'] = 'https://github.com/acme/proof-first'
    plugin_data['repository'] = 'git@github.com:acme/proof-first.git'
    _write(root / PLUGIN_MANIFEST_PATH, json.dumps(plugin_data, indent=2) + '\n')

    marketplace_data = json.loads(_marketplace_manifest_json('0.1.0'))
    marketplace_data['plugins'][0]['homepage'] = 'https://github.com/acme/proof-first'
    marketplace_data['plugins'][0]['repository'] = 'https://github.com/acme/proof-first'
    marketplace_data['owner']['url'] = 'github.com/acme'
    _write(root / MARKETPLACE_MANIFEST_PATH, json.dumps(marketplace_data, indent=2) + '\n')


def _mixed_url_form_drift_manifests(root):
    """Identical to _mixed_url_form_manifests except plugin.json's
    SSH-form `repository` names a different owner, other, from the
    acme every other carrier position states -- the proof that
    normalising URL syntax across the four forms did not also turn
    publish-location-drift into a tautology that never fires."""
    _write(root / 'skills' / 'proof-first' / 'SKILL.md', _plugin_fixture_skill('0.1.0'))

    plugin_data = json.loads(_plugin_manifest_json('0.1.0'))
    plugin_data['homepage'] = 'https://github.com/acme/proof-first'
    plugin_data['repository'] = 'git@github.com:other/proof-first.git'
    _write(root / PLUGIN_MANIFEST_PATH, json.dumps(plugin_data, indent=2) + '\n')

    marketplace_data = json.loads(_marketplace_manifest_json('0.1.0'))
    marketplace_data['plugins'][0]['homepage'] = 'https://github.com/acme/proof-first'
    marketplace_data['plugins'][0]['repository'] = 'https://github.com/acme/proof-first'
    marketplace_data['owner']['url'] = 'github.com/acme'
    _write(root / MARKETPLACE_MANIFEST_PATH, json.dumps(marketplace_data, indent=2) + '\n')


def _multi_skill_manifests(root):
    """A root isolating WR-03: two skill folders exist, each stating its
    own metadata.version, and the second's version differs from the
    first's. Built by the same construction _good_plugin_manifests
    uses -- same manifests, same first skill fixture, same version
    agreement between plugin.json, marketplace.json and the first
    skill -- with a second skill folder added under skills/ so the
    folder count is two rather than one. This root is expected to also
    trip unrelated catalog/frontmatter checks from the second skill
    folder; that noise is harmless, because the two assertions this
    fixture proves name plugin-manifest-invalid and
    plugin-manifest-version-mismatch explicitly."""
    _write(root / 'skills' / 'proof-first' / 'SKILL.md', _plugin_fixture_skill('0.1.0'))
    _write(root / 'skills' / 'second-skill' / 'SKILL.md', _plugin_fixture_skill('9.9.9'))
    _write(root / PLUGIN_MANIFEST_PATH, _plugin_manifest_json('0.1.0'))
    _write(root / MARKETPLACE_MANIFEST_PATH, _marketplace_manifest_json('0.1.0'))


def _minimal_frontmatter_lines():
    """A valid, minimal frontmatter block (name equals 'proof-first',
    matching the directory every catalog/line-ceiling/token-budget fixture
    below uses) so those fixtures exercise only the one code each is built
    to test, with no incidental frontmatter-code noise."""
    return [
        '---',
        'name: proof-first',
        f"description: {'x' * DESCRIPTION_MIN}",
        '---',
        '',
    ]


def _skill_body_at_line_count(n, extra_lines):
    """Build a full SKILL.md fixture: valid minimal frontmatter, the given
    extra content lines, then trailing blank filler lines so the file's
    total line count is exactly n."""
    lines = _minimal_frontmatter_lines() + list(extra_lines)
    filler_needed = n - len(lines)
    if filler_needed < 0:
        raise ValueError('extra_lines already exceeds the requested line count')
    lines += [''] * filler_needed
    return '\n'.join(lines) + '\n'


_LINE_CEILING_HEADING = ['### PF-0.1 — Opening rule', '', 'Body text for the opening rule.']


def _skill_at_line_count(n):
    return _skill_body_at_line_count(n, _LINE_CEILING_HEADING)


def _numbering_for_catalog_count():
    return """## PF reserved ranges
| Section | Range | Concern | Allocated | Next free |
|---|---|---|---|---|
| PF-0 | PF-0.1-PF-0.9 | Opening | 1 | PF-0.2 |
| PF-1 | PF-1.1-PF-1.4 | Structure | 2 | PF-1.3 |

## Allocated IDs
| ID | Title | Defined in | Added in |
|---|---|---|---|
| PF-0.1 | Opening rule | SKILL.md | v1.0.0 |
| PF-1.1 | Rule one | SKILL.md | v1.0.0 |
| PF-1.2 | Rule two | SKILL.md | v1.0.0 |

## Deprecated IDs
| ID | Deprecated in | Absorbed by |
|---|---|---|
"""


def _checklist_for_catalog_count():
    return """## PF rules

| ID | Rule |
|---|---|
| PF-0.1 | Opening rule |
| PF-1.1 | Rule one |
| PF-1.2 | Rule two |
"""


def _catalog_count_extra_lines(count_line):
    lines = [
        '### PF-0.1 — Opening rule', '', 'Body text.', '',
        '### PF-1.1 — Rule one', '', 'Body text.', '',
        '### PF-1.2 — Rule two', '', 'Body text.', '',
    ]
    if count_line is not None:
        lines.append(count_line)
    return lines


def _good_catalog_count_skill():
    return _skill_body_at_line_count(
        60, _catalog_count_extra_lines('This catalog contains 3 rules in 2 numbered sections.'))


def _unstated_count_skill():
    return _skill_body_at_line_count(60, _catalog_count_extra_lines(None))


def _mismatched_count_skill():
    return _skill_body_at_line_count(
        60, _catalog_count_extra_lines('This catalog contains 5 rules in 2 numbered sections.'))


def _single_opening_rule_numbering():
    """A registry with exactly one PF-0 rule allocated (the good case for
    catalog-opening-rule-count)."""
    return """## PF reserved ranges
| Section | Range | Concern | Allocated | Next free |
|---|---|---|---|---|
| PF-0 | PF-0.1-PF-0.9 | Opening | 1 | PF-0.2 |

## Allocated IDs
| ID | Title | Defined in | Added in |
|---|---|---|---|
| PF-0.1 | Opening rule | SKILL.md | v1.0.0 |

## Deprecated IDs
| ID | Deprecated in | Absorbed by |
|---|---|---|
"""


def _multiple_opening_rules_numbering():
    """A registry with multiple PF-0 rules allocated (the bad case for
    catalog-opening-rule-count). Adding PF-0.2 violates CAT-03."""
    return """## PF reserved ranges
| Section | Range | Concern | Allocated | Next free |
|---|---|---|---|---|
| PF-0 | PF-0.1-PF-0.9 | Opening | 2 | PF-0.3 |

## Allocated IDs
| ID | Title | Defined in | Added in |
|---|---|---|---|
| PF-0.1 | Opening rule | SKILL.md | v1.0.0 |
| PF-0.2 | Conflicting opening rule | SKILL.md | v1.0.0 |

## Deprecated IDs
| ID | Deprecated in | Absorbed by |
|---|---|---|
"""


def _single_opening_rule_checklist():
    """Checklist with exactly one PF-0 rule."""
    return """## PF rules

| ID | Rule |
|---|---|
| PF-0.1 | Opening rule |
"""


def _multiple_opening_rules_checklist():
    """Checklist with multiple PF-0 rules (mismatches the NUMBERING.md)."""
    return """## PF rules

| ID | Rule |
|---|---|
| PF-0.1 | Opening rule |
| PF-0.2 | Conflicting opening rule |
"""


def _subblock_numbering():
    """A PF-2 sub-block table with a deliberate gap: Proof covers
    PF-2.1-PF-2.5 and Integrity covers PF-2.15-PF-2.20, leaving
    PF-2.6-PF-2.14 declared by neither. PF-2.10 sits inside PF-2's overall
    reserved range (so the pre-existing section-range test passes) but
    lands in that gap, so only the new sub-block containment test fires --
    the same technique _bad_numbering already uses for MC dimension
    blocks."""
    return """## PF reserved ranges
| Section | Range | Concern | Allocated | Next free |
|---|---|---|---|---|
| PF-2 | PF-2.1-PF-2.20 | Proof and Integrity | 1 | PF-2.11 |

## PF-2 sub-blocks
| Element | Range |
|---|---|
| Proof | PF-2.1-PF-2.5 |
| Integrity | PF-2.15-PF-2.20 |

## Allocated IDs
| ID | Title | Defined in | Added in |
|---|---|---|---|
| PF-2.10 | Gap-landing rule | SKILL.md | v1.0.0 |

## Deprecated IDs
| ID | Deprecated in | Absorbed by |
|---|---|---|
"""


def _mc_numbering():
    """A registry allocating a small, self-contained MC set (MC-1, MC-2)
    inside the Metric block -- distinct from the real repository's 8-ID
    content, per this plan's fixture-isolation discipline."""
    return """## MC reserved blocks
| Dimension | Range |
|---|---|
| Metric | MC-1-MC-5 |

## Allocated IDs
| ID | Title | Defined in | Added in |
|---|---|---|---|
| MC-1 | Fixture metric rule one | completeness-audit.md | v1.0.0 |
| MC-2 | Fixture metric rule two | completeness-audit.md | v1.0.0 |

## Deprecated IDs
| ID | Deprecated in | Absorbed by |
|---|---|---|
"""


def _mc_checklist():
    """The matching MC checklist fixture, used for both the good and bad
    mc-catalog-id-drift roots -- the divergence in the bad root comes from
    the completeness-audit fixture omitting an ID, not from this file."""
    return """## MC rules

| ID | Rule |
|---|---|
| MC-1 | Fixture metric rule one |
| MC-2 | Fixture metric rule two |
"""


def _good_completeness_audit():
    """Defines exactly the two IDs _mc_numbering() allocates."""
    return (
        "### MC-1 — Fixture metric rule one\n\nBody text for fixture rule one.\n\n"
        "### MC-2 — Fixture metric rule two\n\nBody text for fixture rule two.\n"
    )


def _bad_completeness_audit():
    """Omits MC-2 -- present in NUMBERING.md and the checklist, missing
    from this file, the divergence mc-catalog-id-drift must catch."""
    return "### MC-1 — Fixture metric rule one\n\nBody text for fixture rule one.\n"


def _good_artifact_patterns():
    """All four frozen artifact-family headings, each with a short filler
    body -- self-contained, not a copy of the real file's content."""
    return (
        "## RFP and RFI response\n\nFixture body.\n\n"
        "## Solution proposal\n\nFixture body.\n\n"
        "## Executive summary\n\nFixture body.\n\n"
        "## Demo and discovery material\n\nFixture body.\n"
    )


def _bad_artifact_patterns():
    """Omits '## Solution proposal' -- the missing-heading case
    artifact-family-section-missing exists to catch."""
    return (
        "## RFP and RFI response\n\nFixture body.\n\n"
        "## Executive summary\n\nFixture body.\n\n"
        "## Demo and discovery material\n\nFixture body.\n"
    )


def _before_after_section(heading, cross_line=True, check_line=True, citation=None, check_text=None):
    """Build one '## {heading}' section body for an examples/before-after.md
    fixture. cross_line/check_line control whether the ✗/✓ lines are
    present at all; citation, when given, is appended as its own short
    line naming a bare PF-/MC- token; check_text, when given, replaces
    the default ✓ line's quoted text (existing call sites omitting it
    keep the original five-word default, unchanged)."""
    lines = [f"## {heading}", ""]
    if cross_line:
        lines.append(f"✗ \"Fixture non-compliant passage for {heading}.\"")
    if check_line:
        text = check_text if check_text is not None else f"Fixture compliant rewrite for {heading}."
        lines.append(f"✓ \"{text}\"")
    if citation:
        lines.append("")
        lines.append(f"Rules applied: {citation}.")
    lines.append("")
    return "\n".join(lines)


def _good_before_after():
    """All four frozen family headings, in the frozen order, each with a
    ✗ line, a ✓ line, and at least one bare PF-/MC- token -- silent on
    both before-after-family-missing and before-after-citation-missing."""
    return "\n".join(
        _before_after_section(heading, citation=citation)
        for heading, citation in zip(
            ARTIFACT_FAMILY_SECTIONS, ('PF-0.1', 'PF-1.9', 'PF-1.25', 'MC-31'),
        )
    )


def _bad_before_after():
    """Combines three of the four conditions before-after-family-missing
    and before-after-citation-missing exist to catch, isolated from the
    fourth (heading order) because the ordering comparison is only
    meaningful once all four headings are present -- see
    _order_bad_before_after() for that case:
    - '## Solution proposal' is missing entirely (family-missing, missing
      heading).
    - '## RFP and RFI response' is present but carries no ✓ line
      (family-missing, missing half).
    - '## Demo and discovery material' is present, complete, but cites no
      PF-/MC- token (citation-missing).
    - '## Executive summary' is present and fully compliant, so both
      codes' silence on a compliant section is exercised in the same
      fixture as their firing on the non-compliant ones."""
    return "\n".join([
        _before_after_section('RFP and RFI response', check_line=False),
        _before_after_section('Executive summary', citation='PF-1.25'),
        _before_after_section('Demo and discovery material'),
    ])


def _order_bad_before_after():
    """All four frozen headings present and each section complete and
    cited, but 'Executive summary' and 'Solution proposal' are swapped
    relative to ARTIFACT_FAMILY_SECTIONS' own order -- isolates the
    ordering condition from the other three, which this fixture does not
    exercise at all (every section here is fully compliant on its own)."""
    return "\n".join([
        _before_after_section('RFP and RFI response', citation='PF-2.1'),
        _before_after_section('Executive summary', citation='PF-1.25'),
        _before_after_section('Solution proposal', citation='PF-1.9'),
        _before_after_section('Demo and discovery material', citation='MC-31'),
    ])


def _long_sentence_before_after():
    """All four frozen family headings, each complete and cited, except
    'Executive summary' carries a ✓ line whose single sentence is built
    from 30 repeated filler words -- self-evidently over PF41_WORD_CEILING
    without writing prose whose length has to be counted by eye."""
    filler_sentence = ' '.join(['filler'] * 30) + '.'
    return "\n".join([
        _before_after_section('RFP and RFI response', citation='PF-2.1'),
        _before_after_section('Solution proposal', citation='PF-1.9'),
        _before_after_section('Executive summary', citation='PF-1.25', check_text=filler_sentence),
        _before_after_section('Demo and discovery material', citation='MC-31'),
    ])


def _long_sentence_worked_examples():
    """A minimal skills/proof-first/references/worked-examples.md-shaped
    fixture: one '## PF-4.1' heading, one ✗ line, and one ✓ line whose
    sentence exceeds PF41_WORD_CEILING the same way
    _long_sentence_before_after's does -- proves the second scan path is
    genuinely read, not merely listed in EXAMPLE_PROSE_PATHS."""
    filler_sentence = ' '.join(['filler'] * 30) + '.'
    return (
        "## PF-4.1\n\n"
        "✗ \"Fixture non-compliant exhibit.\"\n"
        f"✓ \"{filler_sentence}\"\n"
    )


def _spelled_count_before_after():
    """All four frozen family headings, each complete and cited, except
    'RFP and RFI response' carries a ✓ line naming a lowercase
    word-spelled cardinal followed by an ordinary noun (the firing
    path) and 'Executive summary' carries a ✓ line naming a capitalised
    two-token phrase whose first word is a cardinal (the proper-noun
    exemption) -- exercising both conditions in the same fixture the
    way _bad_before_after already does for the other example codes."""
    return "\n".join([
        _before_after_section(
            'RFP and RFI response', citation='PF-2.1',
            check_text='The proposal spans three phases.',
        ),
        _before_after_section('Solution proposal', citation='PF-1.9'),
        _before_after_section(
            'Executive summary', citation='PF-1.25',
            check_text='Nine Peaks Advisory reviewed this proposal.',
        ),
        _before_after_section('Demo and discovery material', citation='MC-31'),
    ])


def _rule_narration_before_after():
    """All four frozen family headings, each complete and cited, except
    'Solution proposal' carries a ✓ line pairing a listed connective
    with a listed meta term inside NARRATION_WINDOW_CHARS (the firing
    path) and 'Demo and discovery material' carries a ✓ line pairing a
    listed connective with a word absent from NARRATION_META_TERMS (the
    deliberate silence that keeps the signature composite rather than a
    bare connective ban) -- exercising both conditions in the same
    fixture the way _bad_before_after already does for the other
    example codes."""
    return "\n".join([
        _before_after_section('RFP and RFI response', citation='PF-2.1'),
        _before_after_section(
            'Solution proposal', citation='PF-1.9',
            check_text='This capability is demonstrated rather than a generic strength.',
        ),
        _before_after_section('Executive summary', citation='PF-1.25'),
        _before_after_section(
            'Demo and discovery material', citation='MC-31',
            check_text='This capability is demonstrated rather than the alternative approach.',
        ),
    ])


def _good_readme_install():
    """All three ordering headings present in the required order, and all
    four install anchors present -- silent on both
    readme-install-path-missing and readme-before-after-order. Extended
    in 04-09 Task 1 to also carry a ballot-cross line, a check line, and
    an applied-rules footer line immediately after the before/after
    heading, so readme_install_good_root also proves
    readme-example-drift's both-files-required precondition: this root
    ships no examples/before-after.md, so the check must stay silent
    here even though README carries reproduced-looking lines."""
    return (
        "# Proof First\n\n"
        "## What this is\n\nFixture body.\n\n"
        f"{README_BEFORE_AFTER_HEADING}\n\n"
        f"{README_CROSS_CHAR} \"Fixture non-compliant passage.\"\n"
        f"{README_CHECK_CHAR} \"Fixture compliant passage.\"\n\n"
        f"{README_APPLIED_RULES_PREFIX} PF-0.1.\n\n"
        f"{README_INSTALL_HEADING}\n\n"
        "```\nnpx skills add <owner>/<repo>\n```\n\n"
        "```\nclaude plugin marketplace add <owner>/<repo>\n```\n\n"
        "`output-styles/proof-first.md` and `prompts/system-prompt.md` are the other two routes.\n\n"
        f"{README_STATUS_HEADING}\n\nFixture status body.\n"
    )


def _bad_readme_install():
    """Missing two of the four readme-install-path-missing anchors (the
    skills-CLI command and the system-prompt path), and
    '## Before and after' placed after '## Status' rather than before it
    -- both new codes fire on this one fixture, matching the task's own
    bad-fixture description."""
    return (
        "# Proof First\n\n"
        "## What this is\n\nFixture body.\n\n"
        f"{README_INSTALL_HEADING}\n\n"
        "```\nclaude plugin marketplace add <owner>/<repo>\n```\n\n"
        "`output-styles/proof-first.md` is one of the routes.\n\n"
        f"{README_STATUS_HEADING}\n\nFixture status body.\n\n"
        f"{README_BEFORE_AFTER_HEADING}\n\nFixture pair, moved below Status.\n"
    )


def _readme_drift_before_after():
    """Minimal examples/before-after.md fixture whose lines include the
    exact three lines _good_readme_install() reproduces in README, so
    readme_drift_good_root's pair is consistent."""
    return (
        f"{README_CROSS_CHAR} \"Fixture non-compliant passage.\"\n"
        f"{README_CHECK_CHAR} \"Fixture compliant passage.\"\n"
        f"{README_APPLIED_RULES_PREFIX} PF-0.1.\n"
    )


def _readme_drift_before_after_bad():
    """Same three lines as _readme_drift_before_after(), but the check
    line differs by one word from what README reproduces -- the drift
    readme-example-drift exists to catch."""
    return (
        f"{README_CROSS_CHAR} \"Fixture non-compliant passage.\"\n"
        f"{README_CHECK_CHAR} \"Fixture different passage.\"\n"
        f"{README_APPLIED_RULES_PREFIX} PF-0.1.\n"
    )


def _late_example_readme():
    """Same headings and anchors as _good_readme_install(), preceded by
    fifteen filler prose lines so the first ballot-cross line lands past
    README_FIRST_EXAMPLE_MAX_LINE (with margin, not merely one line
    over)."""
    filler = "".join(f"Fixture filler line {n}.\n" for n in range(1, 16))
    return (
        "# Proof First\n\n"
        f"{filler}\n"
        "## What this is\n\nFixture body.\n\n"
        f"{README_BEFORE_AFTER_HEADING}\n\n"
        f"{README_CROSS_CHAR} \"Fixture non-compliant passage.\"\n"
        f"{README_CHECK_CHAR} \"Fixture compliant passage.\"\n\n"
        f"{README_APPLIED_RULES_PREFIX} PF-0.1.\n\n"
        f"{README_INSTALL_HEADING}\n\n"
        "```\nnpx skills add <owner>/<repo>\n```\n\n"
        "```\nclaude plugin marketplace add <owner>/<repo>\n```\n\n"
        "`output-styles/proof-first.md` and `prompts/system-prompt.md` are the other two routes.\n\n"
        f"{README_STATUS_HEADING}\n\nFixture status body.\n"
    )


def _no_example_readme():
    """Same headings and anchors as _good_readme_install(), but with no
    ballot-cross line at all -- readme-example-lead-distance's other
    firing condition."""
    return (
        "# Proof First\n\n"
        "## What this is\n\nFixture body.\n\n"
        f"{README_BEFORE_AFTER_HEADING}\n\nFixture pair, no ballot-cross line.\n\n"
        f"{README_INSTALL_HEADING}\n\n"
        "```\nnpx skills add <owner>/<repo>\n```\n\n"
        "```\nclaude plugin marketplace add <owner>/<repo>\n```\n\n"
        "`output-styles/proof-first.md` and `prompts/system-prompt.md` are the other two routes.\n\n"
        f"{README_STATUS_HEADING}\n\nFixture status body.\n"
    )


def _good_readme_layout():
    """A minimal README carrying a layout heading, a prose sentence
    explaining one marker in the quoted shape, and a fenced tree using
    that same marker on at least one entry -- silent on
    readme-layout-legend-drift."""
    return (
        "# Proof First\n\n"
        f"{README_LAYOUT_HEADING}\n\n"
        "The tree below marks a fixture entry \"planned\" when it does not yet exist.\n\n"
        "```\n"
        "proof-first/\n"
        "├── fixture.md (planned)\n"
        "└── other.md\n"
        "```\n"
    )


def _bad_readme_layout():
    """A prose sentence explaining marker \"planned\", which the tree
    never uses, and a tree using marker \"exists\", which the prose
    never mentions -- both mismatch directions in one fixture,
    following _bad_before_after's documented practice of combining
    conditions."""
    return (
        "# Proof First\n\n"
        f"{README_LAYOUT_HEADING}\n\n"
        "The tree below marks a fixture entry \"planned\" when it does not yet exist.\n\n"
        "```\n"
        "proof-first/\n"
        "├── fixture.md (exists)\n"
        "└── other.md\n"
        "```\n"
    )


def _good_readme_output_style():
    """A minimal README naming README_OUTPUT_STYLE_PATH as a route and
    naming one destination directory -- silent on
    readme-output-style-destination-missing. A dedicated fixture rather
    than a reuse of _good_readme_install(), which names the output-style
    path with no destination and would incidentally fire this code if
    reused as the 'good' side (Phase 4, 04-13)."""
    return (
        "# Proof First\n\n"
        "## Install\n\n"
        f"`{README_OUTPUT_STYLE_PATH}` is a Claude Code output style. Copy it into "
        f"`{README_OUTPUT_STYLE_DESTINATIONS[0]}`, then select it through `/config`.\n"
    )


def _bad_readme_output_style():
    """Same output-style route as _good_readme_output_style(), with no
    destination directory named anywhere -- fires
    readme-output-style-destination-missing (Phase 4, 04-13)."""
    return (
        "# Proof First\n\n"
        "## Install\n\n"
        f"`{README_OUTPUT_STYLE_PATH}` is a Claude Code output style. Select it "
        "through `/config`.\n"
    )


def _no_route_readme_output_style():
    """A README naming neither README_OUTPUT_STYLE_PATH nor either
    destination directory -- silent on readme-output-style-destination-missing:
    a README stating no output-style route has nothing for this code to
    say (Phase 4, 04-13)."""
    return (
        "# Proof First\n\n"
        "## Install\n\n"
        "`prompts/system-prompt.md` is a paste-able system prompt.\n"
    )


def _derivative_source_fixture_files():
    """Minimal fixture content for each of the five real
    DERIVATIVE_SOURCE_NAMES paths, used by derivative_good_root and
    derivative_bad_root below. Content is arbitrary -- only its bytes
    need to be stable so a sha256 over them is reproducible within one
    self-test run."""
    return {
        'skills/proof-first/SKILL.md': "See PF-0.1 for details.\n",
        'skills/proof-first/references/deletion-test.md': "Fixture deletion-test body.\n",
        'skills/proof-first/references/completeness-audit.md': "Fixture completeness-audit body.\n",
        'skills/proof-first/references/artifact-patterns.md': "Fixture artifact-patterns body.\n",
        'skills/proof-first/references/checklist.md': "Fixture checklist body.\n",
    }


def _write_derivative_sources(root):
    for rel, content in _derivative_source_fixture_files().items():
        _write(root / rel, content)


def _derivative_fixture_digest(root):
    h = hashlib.sha256()
    for name in DERIVATIVE_SOURCE_NAMES:
        h.update((root / name).read_bytes())
    return h.hexdigest()


def _good_derivative(digest):
    """A derivative body carrying a correct stamp, all three fixture
    rule headings (PF-0.1, MC-1, MC-5, matching _good_numbering()'s
    Allocated IDs table), and all four frozen artifact-family
    headings -- the silent case for both skill-derivative-stale and
    derivative-rule-coverage-incomplete."""
    stamp = DERIVATIVE_STAMP_RE_TEMPLATE.format(paths=', '.join(DERIVATIVE_SOURCE_NAMES), digest=digest)
    families = '\n'.join(ARTIFACT_FAMILY_SECTIONS)
    return (
        f"{stamp}\n\n"
        "### PF-0.1 — Fixture rule\n\n"
        "### MC-1 — Fixture check\n\n"
        "### MC-5 — Fixture check\n\n"
        f"{families}\n"
    )


def _stale_derivative(digest):
    """A derivative body carrying a stamp whose digest does not match a
    fresh hash of the fixture sources (simulating a source edit with no
    regeneration), and missing the MC-5 rule heading and the 'Executive
    summary' artifact-family heading -- isolates
    skill-derivative-stale's digest-mismatch condition and
    derivative-rule-coverage-incomplete's missing-heading /
    missing-family conditions in one fixture."""
    wrong_digest = ('0' if digest[0] != '0' else '1') + digest[1:]
    stamp = DERIVATIVE_STAMP_RE_TEMPLATE.format(paths=', '.join(DERIVATIVE_SOURCE_NAMES), digest=wrong_digest)
    families = '\n'.join(h for h in ARTIFACT_FAMILY_SECTIONS if h != 'Executive summary')
    return (
        f"{stamp}\n\n"
        "### PF-0.1 — Fixture rule\n\n"
        "### MC-1 — Fixture check\n\n"
        f"{families}\n"
    )


def _no_stamp_derivative():
    """A derivative body with no line matching the stamp pattern at
    all, but every rule and family heading otherwise present -- isolates
    skill-derivative-stale's missing-stamp condition from
    derivative-rule-coverage-incomplete, which stays silent on this
    fixture."""
    families = '\n'.join(ARTIFACT_FAMILY_SECTIONS)
    return (
        "### PF-0.1 — Fixture rule\n\n"
        "### MC-1 — Fixture check\n\n"
        "### MC-5 — Fixture check\n\n"
        f"{families}\n"
    )


def _comparison_derivative(carries_stale_claim):
    """A minimal derivative body for derivative-comparison-claim-stale's
    fixtures. Carries no stamp and no rule headings -- skill-derivative-stale
    and derivative-rule-coverage-incomplete fire on these roots and are
    asserted on elsewhere; what these fixtures isolate is whether the
    comparison claim is present."""
    body = "Generated preamble. This project publishes measured claims or none.\n"
    if carries_stale_claim:
        body += (
            f"{STALE_COMPARISON_CLAIM} a session driven by this file against a session with "
            f"the skill folder installed.\n"
        )
    else:
        body += (
            f"A route comparison is committed at {ROUTES_RESULTS_PATH}; read it for what was "
            f"measured and what bounds the finding.\n"
        )
    return body


def _benchrun_claim_file(carries_stale_claim):
    """A minimal artifact-patterns-shaped body for benchmark-run-claim-stale's
    fixtures. Its contents are otherwise irrelevant: the check tests only
    whether the literal is present, so the fixture says that plainly rather
    than dressing itself up as a real reference file."""
    body = "# Artifact families (fixture stand-in)\n\nThis project makes measured claims or none.\n"
    if carries_stale_claim:
        body += (
            "It is not evidence that a convention wins deals or improves scores; "
            f"{STALE_BENCHMARK_RUN_CLAIM}.\n"
        )
    else:
        body += (
            f"A benchmark is committed at {BENCHMARK_RESULTS_PATH}; read it for what was "
            "measured and what bounds the finding.\n"
        )
    return body


def _benchrun_results_file():
    """A stand-in for the committed benchmark report. Its CONTENTS are
    irrelevant to check_stale_benchmark_run_claim, which tests only that the
    path exists."""
    return (
        "# Benchmark (fixture stand-in)\n\n"
        "This file's existence is the whole signal. The check does not read it.\n"
    )


def _comparison_results_file():
    """A stand-in for the committed route-equivalence report. Its CONTENTS
    are irrelevant to check_derivative_comparison_claim, which tests only
    that the path exists -- the fixture says so plainly rather than
    implying the check reads it."""
    return (
        "# Route equivalence (fixture stand-in)\n\n"
        "This file's existence is the whole signal. The check does not read it.\n"
    )


def _good_skill_family_gate():
    """A SKILL.md whose self-check section names both anchors the
    family-line gate requires -- the silent case for
    skill-family-line-gate-missing."""
    return (
        "### PF-0.1 — Opening rule\n\nBody text for the opening rule.\n\n"
        "## Self-check before delivering\n\n"
        "1. Family-line pass: confirm the first line names the artifact family "
        "or states **No family fits:**.\n"
    )


def _bad_skill_family_gate():
    """A SKILL.md whose self-check section is present but names neither
    anchor -- the firing case for skill-family-line-gate-missing."""
    return (
        "### PF-0.1 — Opening rule\n\nBody text for the opening rule.\n\n"
        "## Self-check before delivering\n\n"
        "1. Subtractive pass: find the violations to remove.\n"
    )


def _good_skill_family_order_gate():
    """A SKILL.md whose self-check section names both anchors the
    ordering gate requires -- the silent case for
    skill-family-order-gate-missing."""
    return (
        "### PF-0.1 — Opening rule\n\nBody text for the opening rule.\n\n"
        "## Self-check before delivering\n\n"
        "1. Family-order pass: re-scan the drafted response and confirm the "
        "artifact family line stands before any rule marker; states "
        "**No family fits:** otherwise.\n"
    )


def _bad_skill_family_order_gate():
    """A SKILL.md whose self-check section is present, and even names
    both of skill-family-line-gate-missing's own anchors, but names
    neither ordering anchor -- the firing case for
    skill-family-order-gate-missing, isolating the ordering check from
    its presence-only sibling."""
    return (
        "### PF-0.1 — Opening rule\n\nBody text for the opening rule.\n\n"
        "## Self-check before delivering\n\n"
        "1. Family-line pass: confirm the first line names the artifact family "
        "or states **No family fits:**.\n"
    )


def _good_results_breakdown():
    """A minimal results file whose verdict-breakdown bullets all agree
    with their own enumerations: one 'xN' multiplier item, one
    single-item enumeration, and one zero count with no parenthetical at
    all -- the silent case for results-breakdown-count-mismatch."""
    return (
        "# Fixture results\n\n"
        "### Arm A\n\n"
        "- conformant: 3 (`A-rfp-answer` x2, `B-proposal-section`)\n"
        "- no-family: 1 (`C-exec-summary`)\n"
        "- rule-before-family: 0\n"
    )


def _bad_results_breakdown():
    """_good_results_breakdown()'s content with the 'conformant' bullet's
    stated count raised from 3 to 4 while its enumeration (still summing
    to 3) is left untouched -- the firing case for
    results-breakdown-count-mismatch."""
    return (
        "# Fixture results\n\n"
        "### Arm A\n\n"
        "- conformant: 4 (`A-rfp-answer` x2, `B-proposal-section`)\n"
        "- no-family: 1 (`C-exec-summary`)\n"
        "- rule-before-family: 0\n"
    )


def _sources_table(rows):
    """Wrap source rows in the one heading + header + separator shape
    check_source_row_unconfirmed() reads, so every fixture below differs
    only in its rows."""
    return (
        "# Fixture sources\n\n"
        "## Qualification checklist sources\n\n"
        "| Title | Author or publisher | Kind | Status | Where |\n"
        "|---|---|---|---|---|\n"
        + "".join(row + "\n" for row in rows)
    )


def _good_sources():
    """Every silent direction in one file: a verified row carrying both a
    URL and a real retrieval date, and two unverified rows -- one whose
    Where cell is a placeholder and one carrying neither URL nor date --
    which are out of scope whatever they say."""
    return _sources_table([
        '| "A confirmed book" | An author | book | verified | https://example.com/a (retrieved 2026-09-21) |',
        '| "An unconfirmed page" | A publisher | public page | unverified | to confirm at LEG-04 |',
        '| "Another unconfirmed page" | A publisher | public page | unverified | https://example.com/b |',
    ])


def _good_sources_all_verified():
    """_good_sources() with no unverified rows left -- the completeness
    direction source-gate-incomplete must stay silent on when a gate
    declares PASSED."""
    return _sources_table([
        '| "A confirmed book" | An author | book | verified | https://example.com/a (retrieved 2026-09-21) |',
        '| "A confirmed page" | A publisher | public page | verified | https://example.com/b (retrieved 2026-09-21) |',
    ])


def _bad_sources():
    """Three firing directions at once: a verified row with no URL, a
    verified row with a URL but no retrieval date, and a verified row
    whose date is well-shaped but not a real calendar date. The fourth row
    is unverified -- out of scope for source-row-unconfirmed, so it does
    not change this fixture's count of three, and present so that pairing
    this file with a PASSED gate gives source-gate-incomplete a trigger."""
    return _sources_table([
        '| "No URL at all" | An author | book | verified | to confirm at LEG-04 |',
        '| "URL but no date" | An author | book | verified | https://example.com/c |',
        '| "URL and an impossible date" | An author | book | verified | https://example.com/d (retrieved 2026-13-45) |',
        '| "Still unconfirmed" | An author | book | unverified | to confirm at LEG-04 |',
    ])


def _malformed_sources():
    """A row that lost its Status column, so its provenance cannot be read
    at all. Skipping it silently would let a row with no status be treated
    as out of scope -- the failure a checker exists to prevent."""
    return _sources_table([
        '| "A row missing a column" | An author | book | https://example.com/e (retrieved 2026-09-21) |',
    ])


def _two_offending_sources():
    """Two verified rows, both unconfirmed, written in reverse message
    order so the check's own sort is what puts them back in order rather
    than the file's row order."""
    return _sources_table([
        '| "Zulu row" | An author | book | verified | to confirm at LEG-04 |',
        '| "Alpha row" | An author | book | verified | to confirm at LEG-04 |',
    ])


def _claim_readme(region_body, tree_extra='', images='', markers=True):
    """A minimal README carrying the layout heading, an optional image, and
    a claim region built from region_body. markers=False omits the end
    marker, giving the unbalanced-region direction."""
    start = CLAIM_REGION_START + '\n'
    end = CLAIM_REGION_END + '\n' if markers else ''
    return (
        "# Fixture readme\n\n"
        + images
        + start + "\n" + region_body + "\n\n" + end
        + "\n## Repository layout\n\n"
        "```\nproof-first/\n├── evals/\n│   └── benchmark/\n"
        + tree_extra +
        "```\n"
    )


def _claim_results_corpus(root):
    """The committed-results corpus a claim-region token may source from,
    at the one glob CLAIM_SOURCE_GLOB reads."""
    _write(root / 'evals' / 'benchmark' / 'RESULTS.md',
           "# Fixture results\n\nMeasured 2026-09-18: 45 wins, 1 tie, 2 losses over 48 pairs.\n")


def _legal_review(gate='PASSED', review_date='2026-09-21'):
    """A minimal LEGAL-REVIEW.md carrying exactly one gate line and one
    review-date line -- the two markers both 06-02 codes read."""
    return (
        "# Fixture legal review\n\n"
        f"Review date: {review_date}\n\n"
        f"Gate status: {gate}\n\n"
        "This fixture is not legal advice.\n"
    )


def _notices_statements(dates):
    """The three framework statements, bounded exactly as NOTICES.md bounds
    them, each carrying the Last reviewed date supplied for it. A None date
    omits the line entirely -- the no-date firing direction."""
    out = ["## Framework statements\n"]
    for heading, date in zip(
        ('Command of the Message', 'MEDDIC, MEDDICC, and related marks', 'Challenger'),
        dates,
    ):
        out.append(f"### {heading}\n")
        out.append(f"**Mark:** {heading}\n")
        out.append("**Rights-holder:** A holder.\n")
        out.append("**Non-affiliation:** This project is not affiliated with the holder.\n")
        out.append("**Paraphrase boundary:** Restated in this repository's own words.\n")
        if date is not None:
            out.append(f"Last reviewed: {date}\n")
    return "\n".join(out)


def _capitalized_skill_family_gate():
    """A SKILL.md whose self-check section names both family-line anchors
    with initial capitals -- proving check_skill_family_line_gate()'s
    WR-02 case-insensitivity fix: this must stay silent for
    skill-family-line-gate-missing, exactly as it already does for its
    case-insensitive sibling check_skill_family_order_gate()."""
    return (
        "### PF-0.1 — Opening rule\n\nBody text for the opening rule.\n\n"
        "## Self-check before delivering\n\n"
        "1. Family-line pass: confirm the first line names the Artifact Family "
        "or states **No Family Fits:**.\n"
    )


def _artifact_patterns_with_source_label():
    """_good_artifact_patterns()'s content, with one frozen source-coined
    label ('economic buyer') inserted -- the firing case for
    source-label-in-skill-content."""
    return _good_artifact_patterns() + "\n\nDiane Osoria, the economic buyer, signs.\n"


def _artifact_patterns_with_metric_word():
    """_good_artifact_patterns()'s content, with the ordinary-English word
    'metric' inserted -- deliberately excluded from SOURCE_COINED_LABELS,
    so this must stay silent for source-label-in-skill-content."""
    return _good_artifact_patterns() + "\n\nName the metric and its baseline.\n"


def _mc_rule_in_skill_bad_skill():
    """An MC-shaped rule heading defined directly inside a SKILL.md -- the
    structural violation mc-rule-in-skill exists to catch."""
    return "### MC-1 — Rule blended directly into SKILL.md\n\nBody text.\n"


def _mc_numbering_for_count():
    """A self-contained MC registry spread across two dimension blocks,
    3 rows total -- deliberately different from the real repository's
    8-checks-across-8-dimensions, so a fixture can never pass by
    coincidence."""
    return """## MC reserved blocks
| Dimension | Range |
|---|---|
| Metric | MC-1-MC-5 |
| Economic Buyer | MC-6-MC-10 |

## Allocated IDs
| ID | Title | Defined in | Added in |
|---|---|---|---|
| MC-1 | Fixture metric rule one | completeness-audit.md | v1.0.0 |
| MC-2 | Fixture metric rule two | completeness-audit.md | v1.0.0 |
| MC-6 | Fixture economic buyer rule | completeness-audit.md | v1.0.0 |

## Deprecated IDs
| ID | Deprecated in | Absorbed by |
|---|---|---|
"""


def _mc_checklist_for_count():
    return """## MC rules

| ID | Rule |
|---|---|
| MC-1 | Fixture metric rule one |
| MC-2 | Fixture metric rule two |
| MC-6 | Fixture economic buyer rule |
"""


def _mc_count_audit_headings():
    return (
        "### MC-1 — Fixture metric rule one\n\nBody text.\n\n"
        "### MC-2 — Fixture metric rule two\n\nBody text.\n\n"
        "### MC-6 — Fixture economic buyer rule\n\nBody text.\n"
    )


def _good_mc_count_completeness_audit():
    return _mc_count_audit_headings() + "\nThis audit contains 3 checks across 2 dimensions.\n"


def _unstated_mc_count_completeness_audit():
    return _mc_count_audit_headings()


def _mismatched_mc_count_completeness_audit():
    return _mc_count_audit_headings() + "\nThis audit contains 4 checks across 2 dimensions.\n"


def _token_budget_good_skill():
    return _skill_body_at_line_count(
        10, ['### PF-0.1 — Opening rule', '', 'Short body text, well under the token budget.'])


def _token_budget_bad_skill():
    filler_words = ' '.join(['word'] * 4200)
    return _skill_body_at_line_count(20, ['### PF-0.1 — Opening rule', '', filler_words])


DOCSTRING_CATALOGUE_MARKER = 'Violation codes implemented in this file:'

_CATALOGUE_ENTRY_RE = re.compile(r'^  ([a-z0-9][a-z0-9-]*)[^\S\n]+- ', re.M)


def docstring_catalogue_codes():
    """Return the set of violation codes this module's own docstring
    catalogue names, parsed out of __doc__ rather than kept as a second
    hand-maintained list. An entry is a line beginning with exactly two
    spaces, then the code, then horizontal whitespace and a '- ' separator,
    all on ONE line; the continuation lines of an entry are indented further
    and are skipped by that shape. The horizontal-only class is deliberate --
    the general whitespace class would let the separator match on the
    FOLLOWING line, so a catalogue entry that wrapped its code away from its
    '- ' would be read as an entry, and a two-space-indented prose line
    followed by one could be read as a phantom code. A catalogue entry must therefore not wrap before its
    separator. Neither shape can produce a false pass in either regex: an
    extra code and a missing one both fail catalogue_matches_registry()
    loudly. The stricter class is chosen so this docstring describes what the
    pattern does.

    The scanned region runs from the catalogue heading to the end of __doc__,
    because the catalogue is the docstring's last section and has no
    terminator. A section appended after it would be scanned too; keep the
    catalogue last.

    Returns None when the catalogue heading is absent, which the caller
    reports as a failure rather than treating as an empty set."""
    doc = __doc__ or ''
    if DOCSTRING_CATALOGUE_MARKER not in doc:
        return None
    body = doc[doc.index(DOCSTRING_CATALOGUE_MARKER) + len(DOCSTRING_CATALOGUE_MARKER):]
    return set(_CATALOGUE_ENTRY_RE.findall(body))


def catalogue_matches_registry():
    """Assert the docstring catalogue names exactly the codes ALL_CHECK_CODES
    registers, and print the difference in both directions when it does not.

    This is the whole of what 06-10 decided to ship against the enforcement-
    scope defect class (six instances in round 6, five of them in this file).
    It is exact, not a proxy: both sides are lists this module already holds,
    so the assertion compares the fact the catalogue heading asserts rather
    than an approximation of it, and it re-enters nothing.

    What was considered and refused, with the measurement that refused it: a
    scope assertion over a frozen path -> reading-checks map, asserted without
    tracing by scanning each check_* body for the paths it names. Measured on
    2026-09-22 against the three readers whose absence from this module's
    comments produced the round's findings -- check_record_citations reaches
    its paths through CITATION_RECORD_PATHS, check_source_gate_incomplete
    through SOURCES_PATH and LEGAL_REVIEW_PATH, and check_readme_claim_unsourced
    through CLAIM_SOURCE_GLOB plus the _claim_region helper. Every path the
    three open is reached through a module constant, a glob or a helper, never
    written as a literal at the point of the read, so a static scan of these
    bodies would have found none of the paths they read. One qualifier, because
    the unqualified form of that sentence is false: check_readme_claim_unsourced
    does carry the literal 'README.md' in its body, twice, as the subject label
    on the violation tuples it returns. A scan keyed on string shape would pick
    it up and would be reading a label, not a read -- which is the same failure
    in the other direction. Producing the
    map needs the tracer, and running the tracer needs the checker to run
    itself, which is the re-entrancy WINDOWS.md id 17 has twice recorded as
    the reason for deferring. The tracer stays a build-time instrument and the
    general scope check stays a candidate, with round 6's six instances as its
    evidence; a regex over comment prose is refused outright, as it has been
    six times before."""
    catalogue = docstring_catalogue_codes()
    if catalogue is None:
        print(f"FAIL: module docstring has no '{DOCSTRING_CATALOGUE_MARKER}' heading")
        return False
    registry = set(ALL_CHECK_CODES)
    missing = sorted(registry - catalogue)
    extra = sorted(catalogue - registry)
    for code in missing:
        print(f"FAIL: {code} is in ALL_CHECK_CODES but absent from the docstring catalogue")
    for code in extra:
        print(f"FAIL: {code} is in the docstring catalogue but absent from ALL_CHECK_CODES")
    return not missing and not extra


def self_test():
    codes_covered = set()
    all_ok = True
    if not catalogue_matches_registry():
        all_ok = False
    with tempfile.TemporaryDirectory(prefix='check-repo-self-test-') as tmp:
        tmp_root = Path(tmp)
        bad_root = tmp_root / 'bad'
        good_root = tmp_root / 'good'
        unparseable_root = tmp_root / 'unparseable'
        escaping_root = tmp_root / 'escaping'
        bad_license_root = tmp_root / 'bad_license'
        readme_good_root = tmp_root / 'readme_good'
        readme_bad_root = tmp_root / 'readme_bad'
        bad_frameworks_root = tmp_root / 'bad_frameworks'
        bad_catalog_root = tmp_root / 'bad_catalog'
        good_catalog_root = tmp_root / 'good_catalog'

        fm_good_root = tmp_root / 'fm_good'
        fm_bad_root = tmp_root / 'fm_bad'
        fm_dupkey_root = tmp_root / 'fm_dupkey'
        fm_reordered_root = tmp_root / 'fm_reordered'
        fm_overmax_root = tmp_root / 'fm_overmax'

        line500_root = tmp_root / 'line500'
        line501_root = tmp_root / 'line501'

        count_good_root = tmp_root / 'count_good'
        count_unstated_root = tmp_root / 'count_unstated'
        count_mismatch_root = tmp_root / 'count_mismatch'

        subblock_root = tmp_root / 'subblock'

        token_good_root = tmp_root / 'token_good'
        token_bad_root = tmp_root / 'token_bad'

        opening_good_root = tmp_root / 'opening_good'
        opening_bad_root = tmp_root / 'opening_bad'

        mc_good_root = tmp_root / 'mc_good'
        mc_bad_root = tmp_root / 'mc_bad'

        mc_count_good_root = tmp_root / 'mc_count_good'
        mc_count_unstated_root = tmp_root / 'mc_count_unstated'
        mc_count_mismatch_root = tmp_root / 'mc_count_mismatch'

        artifact_good_root = tmp_root / 'artifact_good'
        artifact_bad_root = tmp_root / 'artifact_bad'

        family_good_root = tmp_root / 'family_good'
        family_bad_root = tmp_root / 'family_bad'

        family_order_good_root = tmp_root / 'family_order_good'
        family_order_bad_root = tmp_root / 'family_order_bad'

        source_label_bad_root = tmp_root / 'source_label_bad'
        source_label_metric_root = tmp_root / 'source_label_metric'

        results_good_root = tmp_root / 'results_good'

        sources_good_root = tmp_root / 'sources_good'
        sources_bad_root = tmp_root / 'sources_bad'
        sources_malformed_root = tmp_root / 'sources_malformed'
        sources_two_root = tmp_root / 'sources_two'

        gate_clean_root = tmp_root / 'gate_clean'
        gate_incomplete_root = tmp_root / 'gate_incomplete'
        gate_open_root = tmp_root / 'gate_open'
        gate_unreadable_root = tmp_root / 'gate_unreadable'
        gate_double_root = tmp_root / 'gate_double'
        stale_clean_root = tmp_root / 'stale_clean'
        stale_two_root = tmp_root / 'stale_two'
        stale_nodate_root = tmp_root / 'stale_nodate'
        stale_unparseable_root = tmp_root / 'stale_unparseable'
        stale_noreview_root = tmp_root / 'stale_noreview'

        claim_clean_root = tmp_root / 'claim_clean'
        claim_unsourced_root = tmp_root / 'claim_unsourced'
        claim_unanchored_root = tmp_root / 'claim_unanchored'
        claim_unbalanced_root = tmp_root / 'claim_unbalanced'
        claim_nomarker_root = tmp_root / 'claim_nomarker'
        claim_two_root = tmp_root / 'claim_two'
        badge_allowed_root = tmp_root / 'badge_allowed'
        badge_bad_root = tmp_root / 'badge_bad'
        tree_stale_root = tmp_root / 'tree_stale'
        results_bad_root = tmp_root / 'results_bad'

        # record-citation-unresolvable fixtures (06-08). One clean root and
        # one per firing direction, so a single broken direction cannot hide
        # behind another.
        citation_clean_root = tmp_root / 'citation_clean'
        citation_overrun_root = tmp_root / 'citation_overrun'
        citation_missing_root = tmp_root / 'citation_missing'
        citation_inverted_root = tmp_root / 'citation_inverted'
        citation_nobacktick_root = tmp_root / 'citation_nobacktick'
        citation_planning_root = tmp_root / 'citation_planning'
        citation_fenced_root = tmp_root / 'citation_fenced'

        family_capitalized_root = tmp_root / 'family_capitalized'

        plugin_good_root = tmp_root / 'plugin_good'
        plugin_bad_root = tmp_root / 'plugin_bad'
        plugin_invalid_root = tmp_root / 'plugin_invalid'
        plugin_marketplace_shape_root = tmp_root / 'plugin_marketplace_shape'
        plugin_marketplace_entry_key_root = tmp_root / 'plugin_marketplace_entry_key'
        plugin_marketplace_entry_drift_root = tmp_root / 'plugin_marketplace_entry_drift'
        plugin_publish_drift_root = tmp_root / 'plugin_publish_drift'
        plugin_mixed_url_root = tmp_root / 'plugin_mixed_url'
        plugin_mixed_url_drift_root = tmp_root / 'plugin_mixed_url_drift'
        plugin_multiskill_root = tmp_root / 'plugin_multiskill'

        beforeafter_good_root = tmp_root / 'beforeafter_good'
        beforeafter_bad_root = tmp_root / 'beforeafter_bad'
        beforeafter_order_bad_root = tmp_root / 'beforeafter_order_bad'

        sentence_bad_root = tmp_root / 'sentence_bad'
        sentence_skill_bad_root = tmp_root / 'sentence_skill_bad'

        spelled_bad_root = tmp_root / 'spelled_bad'
        spelled_brief_root = tmp_root / 'spelled_brief'

        narration_bad_root = tmp_root / 'narration_bad'

        derivative_good_root = tmp_root / 'derivative_good'
        derivative_bad_root = tmp_root / 'derivative_bad'

        readme_install_good_root = tmp_root / 'readme_install_good'
        readme_install_bad_root = tmp_root / 'readme_install_bad'

        readme_drift_good_root = tmp_root / 'readme_drift_good'
        readme_drift_bad_root = tmp_root / 'readme_drift_bad'

        readme_lead_late_root = tmp_root / 'readme_lead_late'
        readme_lead_none_root = tmp_root / 'readme_lead_none'

        readme_layout_good_root = tmp_root / 'readme_layout_good'
        readme_layout_bad_root = tmp_root / 'readme_layout_bad'

        readme_output_style_good_root = tmp_root / 'readme_output_style_good'
        readme_output_style_bad_root = tmp_root / 'readme_output_style_bad'
        readme_output_style_no_route_root = tmp_root / 'readme_output_style_no_route'

        comparison_good_root = tmp_root / 'comparison_good'
        comparison_bad_root = tmp_root / 'comparison_bad'
        comparison_no_results_root = tmp_root / 'comparison_no_results'
        benchrun_good_root = tmp_root / 'benchrun_good'
        benchrun_bad_root = tmp_root / 'benchrun_bad'
        benchrun_no_results_root = tmp_root / 'benchrun_no_results'

        _write(bad_root / 'NUMBERING.md', _bad_numbering())
        _write(bad_root / 'skills' / 'SKILL.md', "See PF-9.9 and MC-1 for details.\n")
        _write(bad_root / 'examples' / 'deal-brief.md', _bad_deal_brief())
        _write(bad_root / 'examples' / 'scenario.md', "The deal is valued at $999,999 over the term.\n")
        _write(bad_root / 'NOTICES.md', _bad_notices())
        _write(bad_root / 'carrier-missing.md', "This file does not carry the pointer.\n")
        _write(bad_root / 'carrier-dup.md', "Test pointer string.\nSomething else.\nTest pointer string.\n")
        _write(bad_root / 'carrier-lookalike.md', "Test pointer string.\n")
        _write(bad_root / 'LICENSE', _bad_license())
        _write(bad_root / SOURCES_PATH, _bad_sources())
        _write(bad_root / LEGAL_REVIEW_PATH, _legal_review())

        _write(good_root / 'NUMBERING.md', _good_numbering())
        _write(good_root / 'skills' / 'SKILL.md', "See PF-0.1 for details.\n")
        _write(good_root / 'examples' / 'deal-brief.md', _good_deal_brief())
        _write(good_root / 'NOTICES.md', _good_notices())
        _write(good_root / 'carrier-ok.md', "Test pointer string.\n")
        _write(good_root / 'LICENSE', _good_license())
        # No LEGAL-REVIEW.md here on purpose: _good_notices()'s statements
        # carry no 'Last reviewed:' line, and both 06-02 codes are specified
        # to stay silent with no review record to compare against.
        _write(good_root / SOURCES_PATH, _good_sources_all_verified())

        # Third and fourth scratch roots isolate the two `pointer-unparseable`
        # triggers so each fires alone, on its own root, and stays silent on
        # both bad_root and good_root.
        _write(unparseable_root / 'NOTICES.md', _unparseable_notices())
        _write(unparseable_root / 'carrier-ok.md', "Test pointer string.\n")
        _write(unparseable_root / 'LICENSE', _good_license())

        _write(escaping_root / 'NOTICES.md', _escaping_notices())
        _write(escaping_root / 'LICENSE', _good_license())

        # Fifth root tests license-missing
        _write(bad_license_root / 'NUMBERING.md', _good_numbering())
        _write(bad_license_root / 'NOTICES.md', _good_notices())
        _write(bad_license_root / 'carrier-ok.md', "Test pointer string.\n")
        # Deliberately omit LICENSE file

        # README results-pointer fixtures (CR-02): readme_good_root's
        # README.md carries the literal results-pointer path, so the check
        # stays silent; readme_bad_root's omits it, so the check fires
        # exactly once naming README.md.
        _write(readme_good_root / 'README.md', "See evals/conformance/RESULTS-mod04.md for the committed measurement.\n")
        _write(readme_bad_root / 'README.md', "This README does not point at any results file.\n")

        # Sixth root tests framework-statement-missing
        _write(bad_frameworks_root / 'NUMBERING.md', _good_numbering())
        _write(bad_frameworks_root / 'NOTICES.md', _bad_notices_frameworks())
        _write(bad_frameworks_root / 'carrier-ok.md', "Test pointer string.\n")
        _write(bad_frameworks_root / 'LICENSE', _good_license())

        # Seventh/eighth roots isolate catalog-id-drift: bad_catalog_root's
        # SKILL.md defines PF-9.9 (no registry row anywhere) and its
        # checklist.md is missing PF-0.1 (registered in NUMBERING.md but
        # absent from the checklist) -- both divergence directions in one
        # fixture. good_catalog_root keeps all three files in agreement.
        _write(bad_catalog_root / 'NUMBERING.md', _good_numbering())
        _write(bad_catalog_root / 'skills' / 'proof-first' / 'SKILL.md', _bad_skill())
        _write(bad_catalog_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _bad_checklist())

        _write(good_catalog_root / 'NUMBERING.md', _good_numbering())
        _write(good_catalog_root / 'skills' / 'proof-first' / 'SKILL.md', _good_skill())
        _write(good_catalog_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _good_checklist())

        # Frontmatter fixtures (D-33): each root isolates its own code(s),
        # each written one level below skills/ so SKILL_GLOB matches.
        _write(fm_good_root / 'skills' / 'good-skill' / 'SKILL.md', _good_frontmatter())
        _write(fm_bad_root / 'skills' / 'actual-dir' / 'SKILL.md', _bad_frontmatter())
        _write(fm_dupkey_root / 'skills' / 'dupkey-skill' / 'SKILL.md', _dupkey_frontmatter())
        _write(fm_reordered_root / 'skills' / 'reordered-skill' / 'SKILL.md', _reordered_frontmatter())
        _write(fm_overmax_root / 'skills' / 'overmax-skill' / 'SKILL.md', _overmax_frontmatter())

        # Line-ceiling boundary fixtures (CAT-08): 500 lines stays silent,
        # 501 fires. Each carries a matching NUMBERING.md/checklist.md so
        # catalog-id-drift and the frontmatter codes stay silent, isolating
        # skill-too-long as the only code under test.
        _write(line500_root / 'NUMBERING.md', _good_numbering())
        _write(line500_root / 'skills' / 'proof-first' / 'SKILL.md', _skill_at_line_count(500))
        _write(line500_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _good_checklist())

        _write(line501_root / 'NUMBERING.md', _good_numbering())
        _write(line501_root / 'skills' / 'proof-first' / 'SKILL.md', _skill_at_line_count(501))
        _write(line501_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _good_checklist())

        # Stated-count fixtures (D-32): a self-contained 3-rule/2-section
        # registry, isolated from the real 31-rule catalog.
        _write(count_good_root / 'NUMBERING.md', _numbering_for_catalog_count())
        _write(count_good_root / 'skills' / 'proof-first' / 'SKILL.md', _good_catalog_count_skill())
        _write(count_good_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _checklist_for_catalog_count())

        _write(count_unstated_root / 'NUMBERING.md', _numbering_for_catalog_count())
        _write(count_unstated_root / 'skills' / 'proof-first' / 'SKILL.md', _unstated_count_skill())
        _write(count_unstated_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _checklist_for_catalog_count())

        _write(count_mismatch_root / 'NUMBERING.md', _numbering_for_catalog_count())
        _write(count_mismatch_root / 'skills' / 'proof-first' / 'SKILL.md', _mismatched_count_skill())
        _write(count_mismatch_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _checklist_for_catalog_count())

        # PF sub-block containment fixture (D-05): a gapped PF-2 sub-block
        # table with an allocated ID landing in the gap.
        _write(subblock_root / 'NUMBERING.md', _subblock_numbering())

        # Token-budget boundary fixtures (CAT-08 companion check).
        _write(token_good_root / 'NUMBERING.md', _good_numbering())
        _write(token_good_root / 'skills' / 'proof-first' / 'SKILL.md', _token_budget_good_skill())
        _write(token_good_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _good_checklist())

        _write(token_bad_root / 'NUMBERING.md', _good_numbering())
        _write(token_bad_root / 'skills' / 'proof-first' / 'SKILL.md', _token_budget_bad_skill())
        _write(token_bad_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _good_checklist())

        # Opening-rule-count fixtures (CAT-03 enforcement): exactly one PF-0
        # rule must exist, closing the Before-scenario / Identify-Pain /
        # Reframe convergence into a single instruction.
        _write(opening_good_root / 'NUMBERING.md', _single_opening_rule_numbering())
        _write(opening_good_root / 'skills' / 'proof-first' / 'SKILL.md', _good_skill())
        _write(opening_good_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _single_opening_rule_checklist())

        _write(opening_bad_root / 'NUMBERING.md', _multiple_opening_rules_numbering())
        _write(opening_bad_root / 'skills' / 'proof-first' / 'SKILL.md', _good_skill())
        _write(opening_bad_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _multiple_opening_rules_checklist())

        # MC-namespace fixtures (mc-catalog-id-drift, mc-rule-in-skill):
        # mc_good_root keeps the registry, the completeness-audit headings,
        # and the checklist in agreement, with no MC-shaped heading in
        # SKILL.md. mc_bad_root's completeness-audit fixture omits MC-2
        # (firing mc-catalog-id-drift) and its SKILL.md carries an
        # MC-shaped rule heading (firing mc-rule-in-skill) -- both codes
        # isolated from each other since neither check reads the other
        # check's source file.
        _write(mc_good_root / 'NUMBERING.md', _mc_numbering())
        _write(mc_good_root / 'skills' / 'proof-first' / 'SKILL.md', _good_skill())
        _write(mc_good_root / 'skills' / 'proof-first' / 'references' / 'completeness-audit.md', _good_completeness_audit())
        _write(mc_good_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _mc_checklist())

        _write(mc_bad_root / 'NUMBERING.md', _mc_numbering())
        _write(mc_bad_root / 'skills' / 'proof-first' / 'SKILL.md', _mc_rule_in_skill_bad_skill())
        _write(mc_bad_root / 'skills' / 'proof-first' / 'references' / 'completeness-audit.md', _bad_completeness_audit())
        _write(mc_bad_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _mc_checklist())

        # MC stated-count fixtures (D-32's MC counterpart): a self-contained
        # 3-check/2-dimension registry, isolated from the real 8-check
        # namespace, with a matching checklist and completeness-audit
        # headings across all three roots so mc-catalog-id-drift stays
        # silent and only the count codes are exercised.
        _write(mc_count_good_root / 'NUMBERING.md', _mc_numbering_for_count())
        _write(mc_count_good_root / 'skills' / 'proof-first' / 'SKILL.md', _good_skill())
        _write(mc_count_good_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _mc_checklist_for_count())
        _write(mc_count_good_root / 'skills' / 'proof-first' / 'references' / 'completeness-audit.md', _good_mc_count_completeness_audit())

        _write(mc_count_unstated_root / 'NUMBERING.md', _mc_numbering_for_count())
        _write(mc_count_unstated_root / 'skills' / 'proof-first' / 'SKILL.md', _good_skill())
        _write(mc_count_unstated_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _mc_checklist_for_count())
        _write(mc_count_unstated_root / 'skills' / 'proof-first' / 'references' / 'completeness-audit.md', _unstated_mc_count_completeness_audit())

        _write(mc_count_mismatch_root / 'NUMBERING.md', _mc_numbering_for_count())
        _write(mc_count_mismatch_root / 'skills' / 'proof-first' / 'SKILL.md', _good_skill())
        _write(mc_count_mismatch_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _mc_checklist_for_count())
        _write(mc_count_mismatch_root / 'skills' / 'proof-first' / 'references' / 'completeness-audit.md', _mismatched_mc_count_completeness_audit())

        # Artifact-family-section fixtures (artifact-family-section-missing):
        # artifact_good_root's artifact-patterns.md carries all four frozen
        # family headings; artifact_bad_root's omits one. NUMBERING.md/
        # SKILL.md/checklist.md are the same known-consistent trio
        # good_catalog_root/bad_catalog_root already use, so this pair
        # isolates the one new code under test.
        _write(artifact_good_root / 'NUMBERING.md', _good_numbering())
        _write(artifact_good_root / 'skills' / 'proof-first' / 'SKILL.md', _good_skill())
        _write(artifact_good_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _good_checklist())
        _write(artifact_good_root / 'skills' / 'proof-first' / 'references' / 'artifact-patterns.md', _good_artifact_patterns())

        _write(artifact_bad_root / 'NUMBERING.md', _good_numbering())
        _write(artifact_bad_root / 'skills' / 'proof-first' / 'SKILL.md', _good_skill())
        _write(artifact_bad_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _good_checklist())
        _write(artifact_bad_root / 'skills' / 'proof-first' / 'references' / 'artifact-patterns.md', _bad_artifact_patterns())

        # Family-line gate fixtures (skill-family-line-gate-missing,
        # 03-07 GAP A): family_good_root's self-check section names both
        # anchors, family_bad_root's names neither. NUMBERING.md/
        # checklist.md are the same known-consistent pair every other
        # catalog fixture uses, isolating the one new code under test.
        _write(family_good_root / 'NUMBERING.md', _good_numbering())
        _write(family_good_root / 'skills' / 'proof-first' / 'SKILL.md', _good_skill_family_gate())
        _write(family_good_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _good_checklist())

        _write(family_bad_root / 'NUMBERING.md', _good_numbering())
        _write(family_bad_root / 'skills' / 'proof-first' / 'SKILL.md', _bad_skill_family_gate())
        _write(family_bad_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _good_checklist())

        # Family-order gate fixtures (skill-family-order-gate-missing,
        # 03-11): family_order_good_root's self-check section names both
        # ordering anchors ('re-scan', 'before any rule marker');
        # family_order_bad_root names neither ordering anchor even
        # though it names both of the sibling presence-only gate's
        # anchors, isolating this new code from
        # skill-family-line-gate-missing (which must stay silent on
        # family_order_bad_root).
        _write(family_order_good_root / 'NUMBERING.md', _good_numbering())
        _write(family_order_good_root / 'skills' / 'proof-first' / 'SKILL.md', _good_skill_family_order_gate())
        _write(family_order_good_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _good_checklist())

        _write(family_order_bad_root / 'NUMBERING.md', _good_numbering())
        _write(family_order_bad_root / 'skills' / 'proof-first' / 'SKILL.md', _bad_skill_family_order_gate())
        _write(family_order_bad_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _good_checklist())

        # Source-label fixtures (source-label-in-skill-content, 03-07
        # GAP B): the silent case reuses artifact_good_root's clean
        # artifact-patterns.md (asserted below); source_label_bad_root
        # inserts one frozen label, source_label_metric_root inserts the
        # deliberately-excluded ordinary-English word.
        _write(source_label_bad_root / 'NUMBERING.md', _good_numbering())
        _write(source_label_bad_root / 'skills' / 'proof-first' / 'SKILL.md', _good_skill())
        _write(source_label_bad_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _good_checklist())
        _write(source_label_bad_root / 'skills' / 'proof-first' / 'references' / 'artifact-patterns.md', _artifact_patterns_with_source_label())

        _write(source_label_metric_root / 'NUMBERING.md', _good_numbering())
        _write(source_label_metric_root / 'skills' / 'proof-first' / 'SKILL.md', _good_skill())
        _write(source_label_metric_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _good_checklist())
        _write(source_label_metric_root / 'skills' / 'proof-first' / 'references' / 'artifact-patterns.md', _artifact_patterns_with_metric_word())

        # Results-breakdown fixtures (results-breakdown-count-mismatch,
        # 03-14 WR-01 gap closure): results_good_root's bullets all agree
        # with their own enumerations; results_bad_root's 'conformant'
        # bullet states one more than its enumeration sums to. Neither
        # root ships NUMBERING.md/skills/, so every other check stays
        # silent (or fires codes already proven elsewhere) and this pair
        # isolates the one new code under test.
        _write(results_good_root / RESULTS_BREAKDOWN_PATH, _good_results_breakdown())
        _write(results_bad_root / RESULTS_BREAKDOWN_PATH, _bad_results_breakdown())

        # Sources-provenance fixtures (source-row-unconfirmed, 06-01).
        # sources_good_root carries every silent direction (a fully
        # confirmed row, and unverified rows whatever their Where cell
        # says); sources_bad_root carries the three firing directions;
        # sources_malformed_root a row whose column count is wrong; and
        # sources_two_root two offending rows, to pin the output order.
        # No root here ships NUMBERING.md or skills/, so this set
        # isolates the one code under test. The absent-file direction
        # needs no root of its own: results_good_root ships no
        # SOURCES.md at all and is asserted against below.
        _write(sources_good_root / SOURCES_PATH, _good_sources())
        _write(sources_bad_root / SOURCES_PATH, _bad_sources())
        _write(sources_malformed_root / SOURCES_PATH, _malformed_sources())
        _write(sources_two_root / SOURCES_PATH, _two_offending_sources())

        # Gate-completeness fixtures (source-gate-incomplete, 06-02).
        # gate_clean_root declares PASSED over a fully verified list;
        # gate_incomplete_root declares PASSED over a list with an
        # unverified row; gate_open_root declares OPEN over that same
        # incomplete list, which is honest and must stay silent;
        # gate_unreadable_root has no gate line and gate_double_root has
        # two -- neither is a passed gate and neither may be silent.
        _write(gate_clean_root / LEGAL_REVIEW_PATH, _legal_review())
        _write(gate_clean_root / SOURCES_PATH, _good_sources_all_verified())
        _write(gate_incomplete_root / LEGAL_REVIEW_PATH, _legal_review())
        _write(gate_incomplete_root / SOURCES_PATH, _good_sources())
        _write(gate_open_root / LEGAL_REVIEW_PATH, _legal_review(gate='OPEN'))
        _write(gate_open_root / SOURCES_PATH, _good_sources())
        _write(gate_unreadable_root / LEGAL_REVIEW_PATH,
               "# Fixture legal review\n\nReview date: 2026-09-21\n")
        _write(gate_unreadable_root / SOURCES_PATH, _good_sources_all_verified())
        _write(gate_double_root / LEGAL_REVIEW_PATH,
               _legal_review() + "\nGate status: OPEN\n")
        _write(gate_double_root / SOURCES_PATH, _good_sources_all_verified())

        # Stale-review fixtures (framework-statement-stale-review, 06-02).
        # stale_clean_root's three statements all carry the review date;
        # stale_two_root rolls two of them back, pinning both the
        # multiple-offender count and the (code, subject) order;
        # stale_nodate_root omits one date line entirely;
        # stale_unparseable_root carries a well-shaped impossible date;
        # stale_noreview_root ships statements but no LEGAL-REVIEW.md, so
        # there is nothing to compare against and the code must stay silent.
        _write(stale_clean_root / LEGAL_REVIEW_PATH, _legal_review())
        _write(stale_clean_root / 'NOTICES.md',
               _notices_statements(('2026-09-21', '2026-09-22', '2026-09-21')))
        _write(stale_two_root / LEGAL_REVIEW_PATH, _legal_review())
        _write(stale_two_root / 'NOTICES.md',
               _notices_statements(('2026-09-10', '2026-09-21', '2026-09-10')))
        _write(stale_nodate_root / LEGAL_REVIEW_PATH, _legal_review())
        _write(stale_nodate_root / 'NOTICES.md',
               _notices_statements(('2026-09-21', None, '2026-09-21')))
        _write(stale_unparseable_root / LEGAL_REVIEW_PATH, _legal_review())
        _write(stale_unparseable_root / 'NOTICES.md',
               _notices_statements(('2026-09-21', '2026-13-45', '2026-09-21')))
        _write(stale_noreview_root / 'NOTICES.md',
               _notices_statements(('2026-09-10', '2026-09-10', '2026-09-10')))

        # Citation-resolution fixtures (record-citation-unresolvable, 06-08).
        # Every root ships the same three-line cited file, so what fires is
        # decided by the citation's own range and spelling, not by the
        # target. citation_nobacktick_root pins the non-firing direction
        # that keeps this code usable: the same path and number written
        # WITHOUT the enclosing backticks is prose, not a citation.
        # citation_planning_root pins the other: a cited file that exists
        # only under .planning/ is a planning artifact the resolver does not
        # search, so it must report the path as unresolvable rather than
        # silently resolving into the archive.
        _cited = "line one\nline two\nline three\n"
        for _root in (citation_clean_root, citation_overrun_root, citation_missing_root,
                      citation_inverted_root, citation_nobacktick_root,
                      citation_planning_root, citation_fenced_root):
            _write(_root / 'cited-fixture.md', _cited)
        _write(citation_clean_root / LEGAL_REVIEW_PATH,
               "# Fixture\n\nSee `cited-fixture.md`:2-3 for the rule.\n")
        _write(citation_overrun_root / LEGAL_REVIEW_PATH,
               "# Fixture\n\nSee `cited-fixture.md`:2-9 for the rule.\n")
        _write(citation_missing_root / LEGAL_REVIEW_PATH,
               "# Fixture\n\nSee `no-such-fixture.md`:2-3 for the rule.\n")
        _write(citation_inverted_root / LEGAL_REVIEW_PATH,
               "# Fixture\n\nSee `cited-fixture.md`:3-2 for the rule.\n")
        _write(citation_nobacktick_root / LEGAL_REVIEW_PATH,
               "# Fixture\n\nSee cited-fixture.md:2-9 for the rule.\n")
        _write(citation_planning_root / '.planning' / 'archived-fixture.md', _cited)
        _write(citation_planning_root / LEGAL_REVIEW_PATH,
               "# Fixture\n\nSee `archived-fixture.md`:2-3 for the rule.\n")
        # citation_fenced_root: the SAME out-of-range citation as
        # citation_overrun_root, inside a fenced block. A fence that shows
        # readers what the citation format looks like is documentation, and
        # firing on it would make this gate hostile to its own docs.
        _write(citation_fenced_root / LEGAL_REVIEW_PATH,
               "# Fixture\n\n```\nSee `cited-fixture.md`:2-9 for the rule.\n```\n")

        # README claim-region, badge and layout-tree fixtures (06-03).
        # Every root below ships the same one-file results corpus so token
        # sourcing is decided by the region's content, not by the corpus.
        anchored = "Measured 2026-09-18 across `claude-opus-5`: 45 wins over 48 pairs."
        for root in (claim_clean_root, claim_unsourced_root, claim_unanchored_root,
                     claim_unbalanced_root, claim_nomarker_root, claim_two_root,
                     badge_allowed_root, badge_bad_root, tree_stale_root):
            _claim_results_corpus(root)
            (root / 'evals' / 'benchmark').mkdir(parents=True, exist_ok=True)

        _write(claim_clean_root / 'README.md', _claim_readme(anchored))
        _write(claim_unsourced_root / 'README.md', _claim_readme(
            anchored + "\n\nMeasured 2026-09-18 across `claude-opus-5`: 91743 points higher."))
        _write(claim_unanchored_root / 'README.md', _claim_readme(
            "The skill won 45 of 48 pairs."))
        _write(claim_unbalanced_root / 'README.md', _claim_readme(anchored, markers=False))
        _write(claim_nomarker_root / 'README.md',
               "# Fixture readme\n\nThe skill won 45 of 48 pairs with no claim region at all.\n")
        _write(claim_two_root / 'README.md', _claim_readme(
            "Measured 2026-09-18 across `claude-opus-5`: 91743 points.\n\n"
            "Measured 2026-09-18 across `claude-opus-5`: 80512 points."))
        _write(badge_allowed_root / 'README.md', _claim_readme(
            anchored,
            images="![build](https://github.com/o/r/actions/workflows/ci.yml/badge.svg)\n"
                   "![license](https://img.shields.io/badge/License-MIT-green.svg)\n\n"))
        _write(badge_bad_root / 'README.md', _claim_readme(
            anchored,
            images="![quality](https://img.shields.io/badge/quality-98%25-brightgreen.svg)\n\n"))
        _write(tree_stale_root / 'README.md', _claim_readme(anchored))
        (tree_stale_root / 'evals' / 'routes').mkdir(parents=True, exist_ok=True)
        (tree_stale_root / 'evals' / '__pycache__').mkdir(parents=True, exist_ok=True)

        # Case-insensitivity fixture (skill-family-line-gate-missing,
        # 03-REVIEW.md WR-02 gap closure): family_capitalized_root's
        # self-check section names both family-line anchors with initial
        # capitals. Must stay silent after the fix, proving the direction
        # family_bad_root (which names neither anchor in any case) cannot
        # demonstrate on its own.
        _write(family_capitalized_root / 'NUMBERING.md', _good_numbering())
        _write(family_capitalized_root / 'skills' / 'proof-first' / 'SKILL.md', _capitalized_skill_family_gate())
        _write(family_capitalized_root / 'skills' / 'proof-first' / 'references' / 'checklist.md', _good_checklist())

        # Plugin-manifest-version fixtures (plugin-manifest-version-mismatch,
        # Phase 4 04-01): plugin_good_root's manifests and skill all state
        # '0.1.0'; plugin_bad_root's plugin.json states '9.9.9' against its
        # own fixture SKILL.md's '0.1.0'.
        _good_plugin_manifests(plugin_good_root)
        _bad_plugin_manifests(plugin_bad_root)
        _invalid_plugin_manifests(plugin_invalid_root)
        _bad_marketplace_shape(plugin_marketplace_shape_root)
        _marketplace_entry_missing_key_manifests(plugin_marketplace_entry_key_root)
        _marketplace_entry_field_drift_manifests(plugin_marketplace_entry_drift_root)
        _publish_location_drift_manifests(plugin_publish_drift_root)
        _mixed_url_form_manifests(plugin_mixed_url_root)
        _mixed_url_form_drift_manifests(plugin_mixed_url_drift_root)
        _multi_skill_manifests(plugin_multiskill_root)

        # examples/before-after.md fixtures (before-after-family-missing,
        # before-after-citation-missing, Phase 4 04-02): beforeafter_good_root
        # is silent on both new codes; beforeafter_bad_root combines a missing
        # heading, a section missing its ✓ half, and a section with no rule
        # citation; beforeafter_order_bad_root isolates the heading-order
        # condition, which only applies once all four headings are present.
        # None of these roots ship NUMBERING.md, examples/deal-brief.md, or
        # skills/ -- every other check silently returns no violations for a
        # root missing the file it reads, isolating the two new codes.
        _write(beforeafter_good_root / BEFORE_AFTER_PATH, _good_before_after())
        _write(beforeafter_bad_root / BEFORE_AFTER_PATH, _bad_before_after())
        _write(beforeafter_order_bad_root / BEFORE_AFTER_PATH, _order_bad_before_after())

        # example-sentence-length fixtures (Phase 4, 04-07 Task 1):
        # sentence_bad_root carries an over-ceiling ✓ sentence in
        # examples/before-after.md; sentence_skill_bad_root carries one in
        # skills/proof-first/references/worked-examples.md, proving the
        # second scan path is genuinely read and not merely listed in
        # EXAMPLE_PROSE_PATHS. Neither root ships NUMBERING.md,
        # examples/deal-brief.md, or a SKILL.md, isolating this code from
        # every other check the same way the other beforeafter_* roots do.
        _write(sentence_bad_root / BEFORE_AFTER_PATH, _long_sentence_before_after())
        _write(
            sentence_skill_bad_root / 'skills' / 'proof-first' / 'references' / 'worked-examples.md',
            _long_sentence_worked_examples(),
        )

        # before-after-spelled-count fixtures (Phase 4, 04-07 Task 2):
        # spelled_bad_root exercises both the firing path (a lowercase
        # word-spelled cardinal) and the proper-noun exemption (a
        # capitalised two-token phrase) in one fixture, mirroring
        # _bad_before_after's documented practice of combining
        # conditions. spelled_brief_root ships only the real repository's
        # examples/deal-brief.md, proving the brief's deliberate
        # out-of-scope decision is a tested assertion, not a docstring
        # claim -- neither root ships NUMBERING.md or skills/.
        _write(spelled_bad_root / BEFORE_AFTER_PATH, _spelled_count_before_after())
        _write(
            spelled_brief_root / 'examples' / 'deal-brief.md',
            (REPO_ROOT / 'examples' / 'deal-brief.md').read_text(encoding='utf-8'),
        )

        # example-rule-narration fixtures (Phase 4, 04-07 Task 3):
        # narration_bad_root exercises both the firing path (a listed
        # connective paired with a listed meta term) and the deliberate
        # silence on a listed connective paired with a non-listed word,
        # in one fixture. Ships no NUMBERING.md or skills/, isolating
        # this code the same way the other beforeafter_* roots do.
        _write(narration_bad_root / BEFORE_AFTER_PATH, _rule_narration_before_after())

        # derivative_good_root / derivative_bad_root (skill-derivative-stale,
        # derivative-rule-coverage-incomplete, Phase 4 04-03): each root
        # carries its own NUMBERING.md and its own copy of the five
        # DERIVATIVE_SOURCE_NAMES fixture files, so each root's stamp digest
        # is computed from that root's own sources rather than the real
        # repository's. The good root's derivatives carry a matching digest
        # and every required heading; the bad root's output-styles derivative
        # carries a stale digest and two missing headings, and its
        # prompts derivative carries no stamp at all but every heading --
        # isolating skill-derivative-stale's missing-stamp condition from
        # derivative-rule-coverage-incomplete, which stays silent on that file.
        _write(derivative_good_root / 'NUMBERING.md', _good_numbering())
        _write_derivative_sources(derivative_good_root)
        _derivative_good_digest = _derivative_fixture_digest(derivative_good_root)
        _write(derivative_good_root / DERIVATIVE_PATHS[0], _good_derivative(_derivative_good_digest))
        _write(derivative_good_root / DERIVATIVE_PATHS[1], _good_derivative(_derivative_good_digest))

        _write(derivative_bad_root / 'NUMBERING.md', _good_numbering())
        _write_derivative_sources(derivative_bad_root)
        _derivative_bad_digest = _derivative_fixture_digest(derivative_bad_root)
        _write(derivative_bad_root / DERIVATIVE_PATHS[0], _stale_derivative(_derivative_bad_digest))
        _write(derivative_bad_root / DERIVATIVE_PATHS[1], _no_stamp_derivative())

        # comparison_good_root / comparison_bad_root / comparison_no_results_root
        # (derivative-comparison-claim-stale, Phase 4 04-15): the code is a
        # two-sided conjunction, so it takes three roots to prove rather than
        # two. The good root ships the results file and derivatives that do
        # not carry the stale sentence. The bad root ships the results file
        # and one derivative that does. The third root ships the stale
        # sentence in BOTH derivatives and NO results file -- the case where
        # the sentence is simply true, and the one a presence-only check
        # would false-positive on.
        _write(comparison_good_root / ROUTES_RESULTS_PATH, _comparison_results_file())
        _write(comparison_good_root / DERIVATIVE_PATHS[0], _comparison_derivative(False))
        _write(comparison_good_root / DERIVATIVE_PATHS[1], _comparison_derivative(False))

        _write(comparison_bad_root / ROUTES_RESULTS_PATH, _comparison_results_file())
        _write(comparison_bad_root / DERIVATIVE_PATHS[0], _comparison_derivative(True))
        _write(comparison_bad_root / DERIVATIVE_PATHS[1], _comparison_derivative(False))

        _write(comparison_no_results_root / DERIVATIVE_PATHS[0], _comparison_derivative(True))
        _write(comparison_no_results_root / DERIVATIVE_PATHS[1], _comparison_derivative(True))

        # benchrun_good_root / benchrun_bad_root / benchrun_no_results_root
        # (benchmark-run-claim-stale, Phase 6 06-06): the same two-sided
        # conjunction as its sibling above, so the same three roots. The bad
        # root carries the stale sentence in a SKILL SOURCE rather than a
        # derivative -- that is the path the real 2026-09-21 defect took, and
        # the path the sibling code cannot see.
        _write(benchrun_good_root / BENCHMARK_RESULTS_PATH, _benchrun_results_file())
        _write(benchrun_good_root / DERIVATIVE_SOURCE_NAMES[3], _benchrun_claim_file(False))
        _write(benchrun_good_root / DERIVATIVE_PATHS[0], _benchrun_claim_file(False))

        _write(benchrun_bad_root / BENCHMARK_RESULTS_PATH, _benchrun_results_file())
        _write(benchrun_bad_root / DERIVATIVE_SOURCE_NAMES[3], _benchrun_claim_file(True))
        _write(benchrun_bad_root / DERIVATIVE_PATHS[0], _benchrun_claim_file(False))

        _write(benchrun_no_results_root / DERIVATIVE_SOURCE_NAMES[3], _benchrun_claim_file(True))
        _write(benchrun_no_results_root / DERIVATIVE_PATHS[0], _benchrun_claim_file(True))

        # readme_install_good_root / readme_install_bad_root
        # (readme-install-path-missing, readme-before-after-order, Phase 4
        # 04-04): the good root's README.md carries all three ordering
        # headings in the required order and all four install anchors, so
        # both new codes stay silent. The bad root's README.md is missing
        # two of the four install anchors and carries '## Before and
        # after' after '## Status' rather than before it, so both new
        # codes fire. Neither root ships NUMBERING.md, examples/, or
        # skills/ -- every other check silently returns no violations for
        # a root missing the file it reads, isolating the two new codes.
        _write(readme_install_good_root / 'README.md', _good_readme_install())
        _write(readme_install_bad_root / 'README.md', _bad_readme_install())

        # readme_drift_good_root / readme_drift_bad_root
        # (readme-example-drift, Phase 4 04-09 Task 1): both roots share
        # the same README.md (_good_readme_install(), which now carries a
        # ballot-cross line, a check line, and an applied-rules footer
        # line). The good root's examples/before-after.md reproduces
        # those same three lines exactly; the bad root's differs by one
        # word on the check line, so only the bad root fires.
        _write(readme_drift_good_root / 'README.md', _good_readme_install())
        _write(readme_drift_good_root / BEFORE_AFTER_PATH, _readme_drift_before_after())
        _write(readme_drift_bad_root / 'README.md', _good_readme_install())
        _write(readme_drift_bad_root / BEFORE_AFTER_PATH, _readme_drift_before_after_bad())

        # readme_lead_late_root / readme_lead_none_root
        # (readme-example-lead-distance, Phase 4 04-09 Task 2): the late
        # root's first ballot-cross line sits past
        # README_FIRST_EXAMPLE_MAX_LINE; the none root carries no
        # ballot-cross line at all -- both firing conditions proven
        # separately, neither standing in for the other.
        _write(readme_lead_late_root / 'README.md', _late_example_readme())
        _write(readme_lead_none_root / 'README.md', _no_example_readme())

        # readme_layout_good_root / readme_layout_bad_root
        # (readme-layout-legend-drift, Phase 4 04-09 Task 3): the good
        # root's legend and tree agree on one marker; the bad root's
        # legend explains a marker the tree never uses while the tree
        # uses a second marker the legend never mentions -- both
        # mismatch directions in one fixture.
        _write(readme_layout_good_root / 'README.md', _good_readme_layout())
        _write(readme_layout_bad_root / 'README.md', _bad_readme_layout())

        # readme_output_style_good_root / readme_output_style_bad_root /
        # readme_output_style_no_route_root
        # (readme-output-style-destination-missing, Phase 4 04-13): the
        # good root names the output-style path and one destination
        # directory; the bad root names the path and no destination; the
        # no-route root names neither the path nor a destination at all.
        # A dedicated fixture pair rather than a reuse of
        # readme_install_good_root/readme_install_bad_root, whose
        # _good_readme_install()/_bad_readme_install() both name the
        # output-style path with no destination and would incidentally
        # fire this code if reused as either side of this code's proof.
        _write(readme_output_style_good_root / 'README.md', _good_readme_output_style())
        _write(readme_output_style_bad_root / 'README.md', _bad_readme_output_style())
        _write(readme_output_style_no_route_root / 'README.md', _no_route_readme_output_style())

        bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(bad_root)}
        good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(good_root)}
        unparseable_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(unparseable_root)}
        escaping_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(escaping_root)}
        bad_license_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(bad_license_root)}
        readme_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(readme_good_root)}
        readme_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(readme_bad_root)}
        bad_frameworks_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(bad_frameworks_root)}
        bad_catalog_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(bad_catalog_root)}
        good_catalog_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(good_catalog_root)}

        fm_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(fm_good_root)}
        fm_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(fm_bad_root)}
        fm_dupkey_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(fm_dupkey_root)}
        fm_reordered_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(fm_reordered_root)}
        fm_overmax_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(fm_overmax_root)}

        line500_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(line500_root)}
        line501_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(line501_root)}

        count_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(count_good_root)}
        count_unstated_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(count_unstated_root)}
        count_mismatch_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(count_mismatch_root)}

        subblock_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(subblock_root)}

        token_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(token_good_root)}
        token_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(token_bad_root)}

        opening_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(opening_good_root)}
        opening_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(opening_bad_root)}

        mc_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(mc_good_root)}
        mc_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(mc_bad_root)}

        mc_count_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(mc_count_good_root)}
        mc_count_unstated_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(mc_count_unstated_root)}
        mc_count_mismatch_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(mc_count_mismatch_root)}

        artifact_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(artifact_good_root)}
        artifact_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(artifact_bad_root)}

        family_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(family_good_root)}
        family_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(family_bad_root)}

        family_order_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(family_order_good_root)}
        family_order_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(family_order_bad_root)}

        source_label_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(source_label_bad_root)}
        source_label_metric_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(source_label_metric_root)}

        results_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(results_good_root)}
        results_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(results_bad_root)}

        sources_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(sources_good_root)}
        sources_bad_violations = run_all_checks(sources_bad_root)
        sources_bad_codes = {line.split(' ', 1)[0] for _, line in sources_bad_violations}
        sources_malformed_violations = run_all_checks(sources_malformed_root)
        sources_malformed_codes = {line.split(' ', 1)[0] for _, line in sources_malformed_violations}
        sources_two_violations = [
            line for _, line in run_all_checks(sources_two_root)
            if line.startswith('source-row-unconfirmed ')
        ]

        def _codes(root):
            return {line.split(' ', 1)[0] for _, line in run_all_checks(root)}

        gate_clean_codes = _codes(gate_clean_root)
        gate_incomplete_codes = _codes(gate_incomplete_root)
        gate_open_codes = _codes(gate_open_root)
        gate_unreadable_codes = _codes(gate_unreadable_root)
        gate_double_codes = _codes(gate_double_root)
        stale_clean_codes = _codes(stale_clean_root)
        stale_nodate_codes = _codes(stale_nodate_root)
        stale_unparseable_codes = _codes(stale_unparseable_root)
        stale_noreview_codes = _codes(stale_noreview_root)
        claim_clean_codes = _codes(claim_clean_root)
        claim_unsourced_codes = _codes(claim_unsourced_root)
        claim_unanchored_codes = _codes(claim_unanchored_root)
        claim_unbalanced_codes = _codes(claim_unbalanced_root)
        claim_nomarker_codes = _codes(claim_nomarker_root)
        badge_allowed_codes = _codes(badge_allowed_root)
        badge_bad_codes = _codes(badge_bad_root)
        tree_stale_codes = _codes(tree_stale_root)
        citation_clean_codes = _codes(citation_clean_root)
        citation_overrun_codes = _codes(citation_overrun_root)
        citation_missing_codes = _codes(citation_missing_root)
        citation_inverted_codes = _codes(citation_inverted_root)
        citation_nobacktick_codes = _codes(citation_nobacktick_root)
        citation_planning_codes = _codes(citation_planning_root)
        citation_fenced_codes = _codes(citation_fenced_root)
        claim_two_violations = [
            line for _, line in run_all_checks(claim_two_root)
            if line.startswith('readme-claim-unsourced ')
        ]
        tree_stale_violations = [
            line for _, line in run_all_checks(tree_stale_root)
            if line.startswith('readme-layout-tree-stale ')
        ]
        stale_two_violations = [
            (subject, line) for subject, line in run_all_checks(stale_two_root)
            if line.startswith('framework-statement-stale-review ')
        ]

        family_capitalized_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(family_capitalized_root)}

        plugin_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(plugin_good_root)}
        plugin_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(plugin_bad_root)}
        plugin_invalid_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(plugin_invalid_root)}
        plugin_marketplace_shape_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(plugin_marketplace_shape_root)}
        plugin_marketplace_entry_key_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(plugin_marketplace_entry_key_root)}
        plugin_marketplace_entry_drift_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(plugin_marketplace_entry_drift_root)}
        plugin_publish_drift_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(plugin_publish_drift_root)}
        plugin_mixed_url_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(plugin_mixed_url_root)}
        plugin_mixed_url_drift_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(plugin_mixed_url_drift_root)}
        plugin_multiskill_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(plugin_multiskill_root)}

        beforeafter_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(beforeafter_good_root)}
        beforeafter_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(beforeafter_bad_root)}
        beforeafter_order_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(beforeafter_order_bad_root)}

        sentence_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(sentence_bad_root)}
        sentence_skill_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(sentence_skill_bad_root)}

        spelled_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(spelled_bad_root)}
        spelled_brief_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(spelled_brief_root)}

        narration_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(narration_bad_root)}

        derivative_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(derivative_good_root)}
        derivative_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(derivative_bad_root)}

        readme_install_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(readme_install_good_root)}
        readme_install_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(readme_install_bad_root)}

        readme_drift_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(readme_drift_good_root)}
        readme_drift_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(readme_drift_bad_root)}

        readme_lead_late_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(readme_lead_late_root)}
        readme_lead_none_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(readme_lead_none_root)}

        readme_layout_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(readme_layout_good_root)}
        readme_layout_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(readme_layout_bad_root)}

        comparison_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(comparison_good_root)}
        comparison_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(comparison_bad_root)}
        comparison_no_results_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(comparison_no_results_root)}
        benchrun_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(benchrun_good_root)}
        benchrun_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(benchrun_bad_root)}
        benchrun_no_results_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(benchrun_no_results_root)}

        readme_output_style_good_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(readme_output_style_good_root)}
        readme_output_style_bad_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(readme_output_style_bad_root)}
        readme_output_style_no_route_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(readme_output_style_no_route_root)}

        # Union the new roots' codes into the bad-code set so the coverage
        # loop below needs no edit -- it still just checks "did the code
        # fire on some known-bad fixture and stay silent on good_root".
        bad_codes |= (
            unparseable_codes | escaping_codes | bad_license_codes | readme_bad_codes
            | bad_frameworks_codes
            | bad_catalog_codes | fm_bad_codes | fm_dupkey_codes | fm_overmax_codes
            | line501_codes | count_unstated_codes | count_mismatch_codes | subblock_codes
            | token_bad_codes | opening_bad_codes | mc_bad_codes
            | mc_count_unstated_codes | mc_count_mismatch_codes | artifact_bad_codes
            | family_bad_codes | family_order_bad_codes | source_label_bad_codes
            | results_bad_codes | plugin_bad_codes | plugin_invalid_codes
            | plugin_marketplace_shape_codes | plugin_marketplace_entry_key_codes
            | plugin_marketplace_entry_drift_codes | plugin_publish_drift_codes
            | plugin_mixed_url_drift_codes | plugin_multiskill_codes
            | beforeafter_bad_codes | beforeafter_order_bad_codes
            | derivative_bad_codes | readme_install_bad_codes
            | sentence_bad_codes | sentence_skill_bad_codes
            | spelled_bad_codes | narration_bad_codes
            | readme_drift_bad_codes
            | readme_lead_late_codes | readme_lead_none_codes
            | readme_layout_bad_codes
            | readme_output_style_bad_codes
            | comparison_bad_codes
            | benchrun_bad_codes
            | claim_unsourced_codes | claim_unanchored_codes
            | badge_bad_codes | tree_stale_codes
            | citation_overrun_codes | citation_missing_codes
            | citation_inverted_codes | citation_planning_codes
        )

        # skill-derivative-stale / derivative-rule-coverage-incomplete
        # assertions (DIST-05, Phase 4 04-03).
        if 'skill-derivative-stale' in derivative_good_codes:
            print("FAIL: skill-derivative-stale fired on the known-good derivative fixture")
            all_ok = False
        if 'skill-derivative-stale' not in derivative_bad_codes:
            print("FAIL: skill-derivative-stale did not fire on the stale-digest/no-stamp derivative fixture")
            all_ok = False
        if 'skill-derivative-stale' in good_codes:
            print("FAIL: skill-derivative-stale fired on a fixture root shipping no derivative files")
            all_ok = False

        if 'derivative-rule-coverage-incomplete' in derivative_good_codes:
            print("FAIL: derivative-rule-coverage-incomplete fired on the known-good derivative fixture")
            all_ok = False
        if 'derivative-rule-coverage-incomplete' not in derivative_bad_codes:
            print("FAIL: derivative-rule-coverage-incomplete did not fire on the missing-heading/missing-family derivative fixture")
            all_ok = False
        if 'derivative-rule-coverage-incomplete' in good_codes:
            print("FAIL: derivative-rule-coverage-incomplete fired on a fixture root shipping no derivative files")
            all_ok = False

        # readme-install-path-missing / readme-before-after-order
        # assertions (DIST-06, Phase 4 04-04).
        if 'readme-install-path-missing' in readme_install_good_codes:
            print("FAIL: readme-install-path-missing fired on the known-good README install fixture")
            all_ok = False
        if 'readme-before-after-order' in readme_install_good_codes:
            print("FAIL: readme-before-after-order fired on the known-good README install fixture")
            all_ok = False
        if 'readme-install-path-missing' not in readme_install_bad_codes:
            print("FAIL: readme-install-path-missing did not fire on the two-missing-anchor README fixture")
            all_ok = False
        if 'readme-before-after-order' not in readme_install_bad_codes:
            print("FAIL: readme-before-after-order did not fire on the README fixture with Before-and-after moved below Status")
            all_ok = False
        if 'readme-install-path-missing' in good_codes:
            print("FAIL: readme-install-path-missing fired on a fixture root shipping no README.md")
            all_ok = False
        if 'readme-before-after-order' in good_codes:
            print("FAIL: readme-before-after-order fired on a fixture root shipping no README.md")
            all_ok = False

        # readme-example-drift assertions (Phase 4, 04-09 Task 1).
        if 'readme-example-drift' in readme_drift_good_codes:
            print("FAIL: readme-example-drift fired on the known-good drift fixture")
            all_ok = False
        if 'readme-example-drift' not in readme_drift_bad_codes:
            print("FAIL: readme-example-drift did not fire on the drifted before-after fixture")
            all_ok = False
        if 'readme-example-drift' in readme_install_good_codes:
            print("FAIL: readme-example-drift fired on readme_install_good_root, which ships no examples/before-after.md -- both-files-required precondition violated")
            all_ok = False
        if 'readme-example-drift' in good_codes:
            print("FAIL: readme-example-drift fired on a fixture root shipping no README.md")
            all_ok = False

        # readme-example-lead-distance assertions (Phase 4, 04-09 Task 2).
        if 'readme-example-lead-distance' not in readme_lead_late_codes:
            print("FAIL: readme-example-lead-distance did not fire on the late-example fixture")
            all_ok = False
        if 'readme-example-lead-distance' not in readme_lead_none_codes:
            print("FAIL: readme-example-lead-distance did not fire on the no-example fixture")
            all_ok = False
        if 'readme-example-lead-distance' in readme_install_good_codes:
            print("FAIL: readme-example-lead-distance fired on the known-good README install fixture")
            all_ok = False
        if 'readme-example-lead-distance' in good_codes:
            print("FAIL: readme-example-lead-distance fired on a fixture root shipping no README.md")
            all_ok = False

        # readme-layout-legend-drift assertions (Phase 4, 04-09 Task 3).
        if 'readme-layout-legend-drift' in readme_layout_good_codes:
            print("FAIL: readme-layout-legend-drift fired on the known-good layout fixture")
            all_ok = False
        if 'readme-layout-legend-drift' not in readme_layout_bad_codes:
            print("FAIL: readme-layout-legend-drift did not fire on the mismatched-marker layout fixture")
            all_ok = False
        if 'readme-layout-legend-drift' in readme_install_good_codes:
            print("FAIL: readme-layout-legend-drift fired on readme_install_good_root, which ships no '## Repository layout' heading at all")
            all_ok = False
        if 'readme-layout-legend-drift' in good_codes:
            print("FAIL: readme-layout-legend-drift fired on a fixture root shipping no README.md")
            all_ok = False

        # readme-output-style-destination-missing assertions (Phase 4, 04-13).
        # derivative-comparison-claim-stale assertions (Phase 4, 04-15).
        if 'derivative-comparison-claim-stale' in comparison_good_codes:
            print("FAIL: derivative-comparison-claim-stale fired on a results file with no stale claim")
            all_ok = False
        if 'derivative-comparison-claim-stale' not in comparison_bad_codes:
            print("FAIL: derivative-comparison-claim-stale did not fire on a derivative carrying the stale claim beside a committed results file")
            all_ok = False
        if 'derivative-comparison-claim-stale' in comparison_no_results_codes:
            print("FAIL: derivative-comparison-claim-stale fired on the stale claim with no results file -- the sentence is true there")
            all_ok = False
        if 'derivative-comparison-claim-stale' in good_codes:
            print("FAIL: derivative-comparison-claim-stale fired on a fixture root shipping no derivative files")
            all_ok = False

        # benchmark-run-claim-stale assertions (Phase 6, 06-06 Task 3).
        if 'benchmark-run-claim-stale' in benchrun_good_codes:
            print("FAIL: benchmark-run-claim-stale fired on a benchmark results file with no stale claim")
            all_ok = False
        if 'benchmark-run-claim-stale' not in benchrun_bad_codes:
            print("FAIL: benchmark-run-claim-stale did not fire on a skill source carrying the stale claim beside a committed benchmark")
            all_ok = False
        if 'benchmark-run-claim-stale' in benchrun_no_results_codes:
            print("FAIL: benchmark-run-claim-stale fired on the stale claim with no benchmark results file -- the sentence is true there")
            all_ok = False
        if 'benchmark-run-claim-stale' in good_codes:
            print("FAIL: benchmark-run-claim-stale fired on a fixture root shipping no skill sources and no derivatives")
            all_ok = False

        if 'readme-output-style-destination-missing' in readme_output_style_good_codes:
            print("FAIL: readme-output-style-destination-missing fired on the known-good output-style fixture")
            all_ok = False
        if 'readme-output-style-destination-missing' not in readme_output_style_bad_codes:
            print("FAIL: readme-output-style-destination-missing did not fire on the no-destination output-style fixture")
            all_ok = False
        if 'readme-output-style-destination-missing' in readme_output_style_no_route_codes:
            print("FAIL: readme-output-style-destination-missing fired on a fixture naming no output-style route at all")
            all_ok = False
        if 'readme-output-style-destination-missing' in good_codes:
            print("FAIL: readme-output-style-destination-missing fired on a fixture root shipping no README.md")
            all_ok = False

        # before-after-family-missing / before-after-citation-missing
        # assertions (EX-02, Phase 4 04-02).
        if 'before-after-family-missing' in beforeafter_good_codes:
            print("FAIL: before-after-family-missing fired on the known-good before-after fixture")
            all_ok = False
        if 'before-after-citation-missing' in beforeafter_good_codes:
            print("FAIL: before-after-citation-missing fired on the known-good before-after fixture")
            all_ok = False
        if 'before-after-family-missing' not in beforeafter_bad_codes:
            print("FAIL: before-after-family-missing did not fire on the combined missing-heading/missing-half fixture")
            all_ok = False
        if 'before-after-citation-missing' not in beforeafter_bad_codes:
            print("FAIL: before-after-citation-missing did not fire on the section with no rule token")
            all_ok = False
        if 'before-after-family-missing' in good_codes:
            print("FAIL: before-after-family-missing fired on a fixture root shipping no examples/before-after.md")
            all_ok = False
        if 'before-after-citation-missing' in good_codes:
            print("FAIL: before-after-citation-missing fired on a fixture root shipping no examples/before-after.md")
            all_ok = False
        if 'before-after-family-missing' not in beforeafter_order_bad_codes:
            print("FAIL: before-after-family-missing did not fire on the swapped-heading-order fixture")
            all_ok = False
        if 'before-after-citation-missing' in beforeafter_order_bad_codes:
            print("FAIL: before-after-citation-missing fired on the swapped-heading-order fixture, which cites a token in every section")
            all_ok = False

        # example-sentence-length assertions (Phase 4, 04-07 Task 1).
        if 'example-sentence-length' in beforeafter_good_codes:
            print("FAIL: example-sentence-length fired on the known-good before-after fixture")
            all_ok = False
        if 'example-sentence-length' not in sentence_bad_codes:
            print("FAIL: example-sentence-length did not fire on the over-ceiling examples/before-after.md fixture")
            all_ok = False
        if 'example-sentence-length' not in sentence_skill_bad_codes:
            print("FAIL: example-sentence-length did not fire on the over-ceiling worked-examples.md fixture -- the second scan path is not being read")
            all_ok = False
        if 'example-sentence-length' in good_codes:
            print("FAIL: example-sentence-length fired on a fixture root shipping neither example file")
            all_ok = False
        if 'example-sentence-length' in beforeafter_bad_codes:
            print("FAIL: example-sentence-length fired on beforeafter_bad_root, whose short fixture lines are within the ceiling")
            all_ok = False
        if 'example-sentence-length' in beforeafter_order_bad_codes:
            print("FAIL: example-sentence-length fired on beforeafter_order_bad_root, whose short fixture lines are within the ceiling")
            all_ok = False

        # before-after-spelled-count assertions (Phase 4, 04-07 Task 2).
        if 'before-after-spelled-count' not in spelled_bad_codes:
            print("FAIL: before-after-spelled-count did not fire on the lowercase-spelled-cardinal fixture")
            all_ok = False
        if 'before-after-spelled-count' in beforeafter_good_codes:
            print("FAIL: before-after-spelled-count fired on the known-good before-after fixture")
            all_ok = False
        if 'before-after-spelled-count' in good_codes:
            print("FAIL: before-after-spelled-count fired on a fixture root shipping no examples/before-after.md")
            all_ok = False
        if 'before-after-spelled-count' in spelled_brief_codes:
            print("FAIL: before-after-spelled-count fired on a root shipping only the real examples/deal-brief.md, which is deliberately out of scope")
            all_ok = False

        # example-rule-narration assertions (Phase 4, 04-07 Task 3).
        if 'example-rule-narration' not in narration_bad_codes:
            print("FAIL: example-rule-narration did not fire on the connective-plus-meta-term fixture")
            all_ok = False
        if 'example-rule-narration' in beforeafter_good_codes:
            print("FAIL: example-rule-narration fired on the known-good before-after fixture")
            all_ok = False
        if 'example-rule-narration' in good_codes:
            print("FAIL: example-rule-narration fired on a fixture root shipping no examples/before-after.md")
            all_ok = False
        if 'example-rule-narration' in sentence_bad_codes:
            print("FAIL: example-rule-narration fired on sentence_bad_root, whose fixture carries no connective")
            all_ok = False
        if 'example-rule-narration' in spelled_bad_codes:
            print("FAIL: example-rule-narration fired on spelled_bad_root, whose fixture carries no connective")
            all_ok = False

        if 'catalog-id-drift' in good_catalog_codes:
            print("FAIL: catalog-id-drift fired on the known-good skill/checklist fixture")
            all_ok = False

        # Frontmatter-specific assertions.
        if FRONTMATTER_CHECK_CODES and set(FRONTMATTER_CHECK_CODES) & fm_good_codes:
            print("FAIL: a frontmatter code fired on the known-good frontmatter fixture")
            all_ok = False
        if set(FRONTMATTER_CHECK_CODES) & fm_reordered_codes:
            print("FAIL: a frontmatter code fired on the reordered-but-valid frontmatter fixture")
            all_ok = False
        if fm_bad_codes & {'frontmatter-unknown-key', 'frontmatter-name-mismatch', 'frontmatter-description-invalid'} != {
            'frontmatter-unknown-key', 'frontmatter-name-mismatch', 'frontmatter-description-invalid',
        }:
            print("FAIL: the bad frontmatter fixture did not fire all three of its expected codes")
            all_ok = False
        if 'frontmatter-unparseable' not in fm_dupkey_codes:
            print("FAIL: frontmatter-unparseable did not fire on the duplicate-key fixture")
            all_ok = False
        if 'frontmatter-description-invalid' not in fm_overmax_codes:
            print("FAIL: frontmatter-description-invalid did not fire one character past the ceiling")
            all_ok = False

        # Line-ceiling boundary assertions.
        if 'skill-too-long' in line500_codes:
            print("FAIL: skill-too-long fired at exactly the 500-line ceiling")
            all_ok = False
        if 'skill-too-long' not in line501_codes:
            print("FAIL: skill-too-long did not fire at 501 lines")
            all_ok = False

        # Stated-count assertions.
        if 'catalog-count-unstated' in count_good_codes or 'catalog-count-mismatch' in count_good_codes:
            print("FAIL: a catalog-count code fired on the known-good stated-count fixture")
            all_ok = False
        if 'catalog-count-unstated' not in count_unstated_codes:
            print("FAIL: catalog-count-unstated did not fire when the stated-count line is absent")
            all_ok = False
        if 'catalog-count-mismatch' not in count_mismatch_codes:
            print("FAIL: catalog-count-mismatch did not fire when the stated numbers disagree with the registry")
            all_ok = False

        # Sub-block containment assertion.
        if 'range-id' not in subblock_codes:
            print("FAIL: range-id did not fire for a PF ID landing in a gap between declared sub-blocks")
            all_ok = False

        # Token-budget boundary assertions.
        if 'skill-token-budget-exceeded' in token_good_codes:
            print("FAIL: skill-token-budget-exceeded fired on the known-good, low-word-count fixture")
            all_ok = False
        if 'skill-token-budget-exceeded' not in token_bad_codes:
            print("FAIL: skill-token-budget-exceeded did not fire on the high-word-count fixture")
            all_ok = False

        # Opening-rule-count assertions.
        if 'catalog-opening-rule-count' in opening_good_codes:
            print("FAIL: catalog-opening-rule-count fired on the known-good (exactly one PF-0) fixture")
            all_ok = False
        if 'catalog-opening-rule-count' not in opening_bad_codes:
            print("FAIL: catalog-opening-rule-count did not fire on the multiple-opening-rules fixture")
            all_ok = False

        # MC-namespace assertions.
        if 'mc-catalog-id-drift' in mc_good_codes:
            print("FAIL: mc-catalog-id-drift fired on the known-good MC completeness-audit/checklist fixture")
            all_ok = False
        if 'mc-catalog-id-drift' not in mc_bad_codes:
            print("FAIL: mc-catalog-id-drift did not fire when completeness-audit.md omits an allocated MC ID")
            all_ok = False
        if 'mc-rule-in-skill' in mc_good_codes:
            print("FAIL: mc-rule-in-skill fired on a SKILL.md with no MC-shaped rule heading")
            all_ok = False
        if 'mc-rule-in-skill' not in mc_bad_codes:
            print("FAIL: mc-rule-in-skill did not fire when SKILL.md defines an MC-shaped rule heading")
            all_ok = False

        # MC stated-count assertions.
        if 'mc-count-unstated' in mc_count_good_codes or 'mc-count-mismatch' in mc_count_good_codes:
            print("FAIL: an mc-count code fired on the known-good MC stated-count fixture")
            all_ok = False
        if 'mc-count-unstated' not in mc_count_unstated_codes:
            print("FAIL: mc-count-unstated did not fire when the stated-count line is absent")
            all_ok = False
        if 'mc-count-mismatch' not in mc_count_mismatch_codes:
            print("FAIL: mc-count-mismatch did not fire when the stated numbers disagree with the registry")
            all_ok = False

        # Artifact-family-section assertions.
        if 'artifact-family-section-missing' in artifact_good_codes:
            print("FAIL: artifact-family-section-missing fired on the known-good four-heading fixture")
            all_ok = False
        if 'artifact-family-section-missing' not in artifact_bad_codes:
            print("FAIL: artifact-family-section-missing did not fire when a required heading is missing")
            all_ok = False

        # Family-line gate assertions.
        if 'skill-family-line-gate-missing' in family_good_codes:
            print("FAIL: skill-family-line-gate-missing fired on a self-check section naming both anchors")
            all_ok = False
        if 'skill-family-line-gate-missing' not in family_bad_codes:
            print("FAIL: skill-family-line-gate-missing did not fire on a self-check section naming neither anchor")
            all_ok = False
        if 'skill-family-line-gate-missing' in good_catalog_codes:
            print("FAIL: skill-family-line-gate-missing fired on a SKILL.md with no self-check section at all")
            all_ok = False
        if 'skill-family-line-gate-missing' in family_capitalized_codes:
            print("FAIL: skill-family-line-gate-missing fired on a self-check section naming both anchors with initial capitals (WR-02 case-insensitivity fix)")
            all_ok = False

        # Family-order gate assertions.
        if 'skill-family-order-gate-missing' in family_order_good_codes:
            print("FAIL: skill-family-order-gate-missing fired on a self-check section naming both ordering anchors")
            all_ok = False
        if 'skill-family-order-gate-missing' not in family_order_bad_codes:
            print("FAIL: skill-family-order-gate-missing did not fire on a self-check section naming neither ordering anchor")
            all_ok = False
        if 'skill-family-line-gate-missing' in family_order_bad_codes:
            print("FAIL: skill-family-line-gate-missing fired on the family-order-bad fixture, which names both of its own anchors")
            all_ok = False
        if 'skill-family-order-gate-missing' in good_catalog_codes:
            print("FAIL: skill-family-order-gate-missing fired on a SKILL.md with no self-check section at all")
            all_ok = False

        # README results-pointer assertions.
        if 'readme-results-pointer-missing' in readme_good_codes:
            print("FAIL: readme-results-pointer-missing fired on a README containing the results pointer")
            all_ok = False
        if 'readme-results-pointer-missing' not in readme_bad_codes:
            print("FAIL: readme-results-pointer-missing did not fire on a README missing the results pointer")
            all_ok = False

        # Source-label assertions.
        if 'source-label-in-skill-content' in artifact_good_codes:
            print("FAIL: source-label-in-skill-content fired on shipped-clean artifact-patterns.md content")
            all_ok = False
        if 'source-label-in-skill-content' not in source_label_bad_codes:
            print("FAIL: source-label-in-skill-content did not fire when a frozen label was inserted")
            all_ok = False
        if 'source-label-in-skill-content' in source_label_metric_codes:
            print("FAIL: source-label-in-skill-content fired on the ordinary-English word for a measurement")
            all_ok = False

        # Results-breakdown assertions.
        if 'results-breakdown-count-mismatch' in results_good_codes:
            print("FAIL: results-breakdown-count-mismatch fired on bullets whose counts agree with their enumerations")
            all_ok = False
        if 'results-breakdown-count-mismatch' not in results_bad_codes:
            print("FAIL: results-breakdown-count-mismatch did not fire when a stated count disagreed with its enumeration")
            all_ok = False
        if 'results-breakdown-count-mismatch' in good_codes:
            print("FAIL: results-breakdown-count-mismatch fired on a fixture root shipping no results file")
            all_ok = False

        # Sources-provenance assertions.
        if 'source-row-unconfirmed' in sources_good_codes:
            print("FAIL: source-row-unconfirmed fired on a sources file whose verified row carries a URL and a retrieval date, or on its unverified rows")
            all_ok = False
        if 'source-row-unconfirmed' not in sources_bad_codes:
            print("FAIL: source-row-unconfirmed did not fire on verified rows missing a URL, a date, or carrying an impossible date")
            all_ok = False
        sources_bad_count = sum(
            1 for _, line in sources_bad_violations
            if line.startswith('source-row-unconfirmed ')
        )
        if sources_bad_count != 3:
            print(f"FAIL: source-row-unconfirmed fired {sources_bad_count} times on three distinct offending rows, expected 3")
            all_ok = False
        if 'source-row-unconfirmed' not in sources_malformed_codes:
            print("FAIL: source-row-unconfirmed did not fire on a row whose cell count is not the five the source tables declare")
            all_ok = False
        if not any(
            'cells where 5 are required' in line
            for _, line in sources_malformed_violations
        ):
            print("FAIL: source-row-unconfirmed fired on a malformed row without naming the parse failure")
            all_ok = False
        if len(sources_two_violations) != 2:
            print(f"FAIL: source-row-unconfirmed produced {len(sources_two_violations)} violations for two offending rows, expected 2")
            all_ok = False
        elif sources_two_violations != sorted(sources_two_violations):
            print("FAIL: source-row-unconfirmed reported two offending rows out of sorted order")
            all_ok = False
        if 'source-row-unconfirmed' in results_good_codes:
            print("FAIL: source-row-unconfirmed fired on a fixture root shipping no sources file")
            all_ok = False

        # Gate-completeness assertions (source-gate-incomplete, 06-02).
        if 'source-gate-incomplete' in gate_clean_codes:
            print("FAIL: source-gate-incomplete fired on a PASSED gate over a fully verified source list")
            all_ok = False
        if 'source-gate-incomplete' not in gate_incomplete_codes:
            print("FAIL: source-gate-incomplete did not fire on a PASSED gate over a list with unverified rows")
            all_ok = False
        if 'source-gate-incomplete' in gate_open_codes:
            print("FAIL: source-gate-incomplete fired on an OPEN gate, which makes no completeness claim")
            all_ok = False
        if 'source-gate-incomplete' not in gate_unreadable_codes:
            print("FAIL: source-gate-incomplete did not fire on a review record carrying no Gate status line")
            all_ok = False
        if 'source-gate-incomplete' not in gate_double_codes:
            print("FAIL: source-gate-incomplete did not fire on a review record carrying two Gate status lines")
            all_ok = False
        if 'source-gate-incomplete' in results_good_codes:
            print("FAIL: source-gate-incomplete fired on a fixture root shipping no LEGAL-REVIEW.md")
            all_ok = False

        # Citation-resolution assertions (record-citation-unresolvable, 06-08).
        if 'record-citation-unresolvable' in citation_clean_codes:
            print("FAIL: record-citation-unresolvable fired on a citation whose range is inside the cited file")
            all_ok = False
        if 'record-citation-unresolvable' not in citation_overrun_codes:
            print("FAIL: record-citation-unresolvable did not fire on a range running past the cited file's end")
            all_ok = False
        if 'record-citation-unresolvable' not in citation_missing_codes:
            print("FAIL: record-citation-unresolvable did not fire on a citation naming no file in the tree")
            all_ok = False
        if 'record-citation-unresolvable' not in citation_inverted_codes:
            print("FAIL: record-citation-unresolvable did not fire on an inverted line range")
            all_ok = False
        if 'record-citation-unresolvable' in citation_nobacktick_codes:
            print("FAIL: record-citation-unresolvable fired on an out-of-range path:N written without backticks, which is prose")
            all_ok = False
        if 'record-citation-unresolvable' not in citation_planning_codes:
            print("FAIL: record-citation-unresolvable did not fire on a citation resolvable only inside .planning/")
            all_ok = False
        if 'record-citation-unresolvable' in citation_fenced_codes:
            print("FAIL: record-citation-unresolvable fired on an out-of-range citation inside a fenced block, which is documentation")
            all_ok = False
        if 'record-citation-unresolvable' in results_good_codes:
            print("FAIL: record-citation-unresolvable fired on a fixture root shipping no LEGAL-REVIEW.md or README.md")
            all_ok = False

        # Stale-review assertions (framework-statement-stale-review, 06-02).
        if 'framework-statement-stale-review' in stale_clean_codes:
            print("FAIL: framework-statement-stale-review fired on statements dated on or after the review date")
            all_ok = False
        if 'framework-statement-stale-review' not in stale_nodate_codes:
            print("FAIL: framework-statement-stale-review did not fire on a statement carrying no Last reviewed line")
            all_ok = False
        if 'framework-statement-stale-review' not in stale_unparseable_codes:
            print("FAIL: framework-statement-stale-review did not fire on a Last reviewed value that is not a real date")
            all_ok = False
        if 'framework-statement-stale-review' in stale_noreview_codes:
            print("FAIL: framework-statement-stale-review fired with no LEGAL-REVIEW.md to compare against")
            all_ok = False
        if len(stale_two_violations) != 2:
            print(f"FAIL: framework-statement-stale-review produced {len(stale_two_violations)} violations for two stale statements, expected 2")
            all_ok = False
        elif stale_two_violations != sorted(stale_two_violations):
            print("FAIL: framework-statement-stale-review reported two stale statements out of (subject, message) order")
            all_ok = False
        elif len({s for s, _ in stale_two_violations}) != 2:
            print("FAIL: framework-statement-stale-review reported two stale statements under one subject, so they cannot be told apart")
            all_ok = False

        # README claim-region assertions (readme-claim-unsourced /
        # readme-claim-unanchored, 06-03).
        if 'readme-claim-unsourced' in claim_clean_codes:
            print("FAIL: readme-claim-unsourced fired on a claim region whose numbers all appear in the results corpus")
            all_ok = False
        if 'readme-claim-unanchored' in claim_clean_codes:
            print("FAIL: readme-claim-unanchored fired on a claim-region paragraph carrying a model string and a date")
            all_ok = False
        if 'readme-claim-unsourced' not in claim_unsourced_codes:
            print("FAIL: readme-claim-unsourced did not fire on a fabricated figure sourced by no results file")
            all_ok = False
        if 'readme-claim-unanchored' not in claim_unanchored_codes:
            print("FAIL: readme-claim-unanchored did not fire on a numeric paragraph with no model string and no date")
            all_ok = False
        if 'readme-claim-unsourced' not in claim_unbalanced_codes:
            print("FAIL: readme-claim-unsourced did not fire on a region with a start marker and no end marker")
            all_ok = False
        if 'readme-claim-unanchored' in claim_unbalanced_codes:
            print("FAIL: readme-claim-unanchored double-reported an unbalanced region that readme-claim-unsourced owns")
            all_ok = False
        if 'readme-claim-unsourced' in claim_nomarker_codes or 'readme-claim-unanchored' in claim_nomarker_codes:
            print("FAIL: a claim-region code fired on a README carrying no claim region at all")
            all_ok = False
        if 'readme-claim-unsourced' in good_codes or 'readme-claim-unanchored' in good_codes:
            print("FAIL: a claim-region code fired on a fixture root shipping no README.md")
            all_ok = False
        if len(claim_two_violations) != 2:
            print(f"FAIL: readme-claim-unsourced produced {len(claim_two_violations)} violations for two fabricated figures, expected 2")
            all_ok = False
        elif claim_two_violations != sorted(claim_two_violations):
            print("FAIL: readme-claim-unsourced reported two unsourced tokens out of sorted order")
            all_ok = False

        # Badge assertions (readme-badge-unlisted, 06-03).
        if 'readme-badge-unlisted' in badge_allowed_codes:
            print("FAIL: readme-badge-unlisted fired on the allow-listed build-status and license badges")
            all_ok = False
        if 'readme-badge-unlisted' not in badge_bad_codes:
            print("FAIL: readme-badge-unlisted did not fire on a numeric shields.io badge")
            all_ok = False
        if 'readme-badge-unlisted' in good_codes:
            print("FAIL: readme-badge-unlisted fired on a fixture root shipping no README.md")
            all_ok = False

        # Layout-tree assertions (readme-layout-tree-stale, 06-03).
        if 'readme-layout-tree-stale' not in tree_stale_codes:
            print("FAIL: readme-layout-tree-stale did not fire on an evals/ subdirectory absent from the layout tree")
            all_ok = False
        if len(tree_stale_violations) != 1:
            print(f"FAIL: readme-layout-tree-stale produced {len(tree_stale_violations)} violations, expected 1 — __pycache__ must be skipped")
            all_ok = False
        elif '__pycache__' in tree_stale_violations[0]:
            print("FAIL: readme-layout-tree-stale reported __pycache__, which it is specified to skip")
            all_ok = False
        if 'readme-layout-tree-stale' in claim_clean_codes:
            print("FAIL: readme-layout-tree-stale fired on a tree naming every evals/ subdirectory on disk")
            all_ok = False
        if 'readme-layout-tree-stale' in good_codes:
            print("FAIL: readme-layout-tree-stale fired on a fixture root shipping no README.md")
            all_ok = False

        # Plugin-manifest-version assertions.
        if 'plugin-manifest-version-mismatch' in plugin_good_codes:
            print("FAIL: plugin-manifest-version-mismatch fired on manifests agreeing with the skill's version")
            all_ok = False
        if 'plugin-manifest-version-mismatch' not in plugin_bad_codes:
            print("FAIL: plugin-manifest-version-mismatch did not fire when plugin.json's version disagreed with the skill's")
            all_ok = False
        if 'plugin-manifest-version-mismatch' in good_codes:
            print("FAIL: plugin-manifest-version-mismatch fired on a fixture root shipping no .claude-plugin/ directory")
            all_ok = False

        # Plugin-manifest-invalid assertions.
        if 'plugin-manifest-invalid' in plugin_good_codes:
            print("FAIL: plugin-manifest-invalid fired on well-formed manifests")
            all_ok = False
        if 'plugin-manifest-invalid' not in plugin_invalid_codes:
            print("FAIL: plugin-manifest-invalid did not fire on a manifest missing a required key with a mismatched name")
            all_ok = False
        if 'plugin-manifest-invalid' not in plugin_marketplace_shape_codes:
            print("FAIL: plugin-manifest-invalid did not fire on a marketplace.json with an empty plugins array")
            all_ok = False
        if 'plugin-manifest-invalid' not in plugin_marketplace_entry_key_codes:
            print("FAIL: plugin-manifest-invalid did not fire when a required key was missing from marketplace.json's plugin entry")
            all_ok = False

        # Marketplace-entry equality assertions (WR-02): the five
        # hand-duplicated distribution fields must agree between
        # plugin.json and marketplace.json's plugin entry, and the
        # exclusion of homepage/repository from that set (owned by
        # publish-location-drift's owner-segment normalisation instead)
        # must be proven silent, not merely described.
        if 'plugin-manifest-invalid' not in plugin_marketplace_entry_drift_codes:
            print("FAIL: plugin-manifest-invalid did not fire when marketplace.json's plugin entry disagreed with plugin.json on a MARKETPLACE_ENTRY_EQUAL_KEYS field")
            all_ok = False
        # The fire direction is plugin_marketplace_entry_drift_codes above;
        # these two prove the exclusion is real rather than merely stated --
        # homepage/repository's mixed-URL-form root must stay silent, and so
        # must the plain well-formed, agreeing root.
        if 'plugin-manifest-invalid' in plugin_good_codes:
            print("FAIL: plugin-manifest-invalid fired on well-formed, agreeing manifests")
            all_ok = False
        if 'plugin-manifest-invalid' in plugin_mixed_url_codes:
            print("FAIL: plugin-manifest-invalid fired on carriers naming the same owner in different GitHub URL forms -- homepage/repository must stay excluded from the equality set")
            all_ok = False
        if 'plugin-manifest-invalid' in good_codes:
            print("FAIL: plugin-manifest-invalid fired on a fixture root shipping no .claude-plugin/ directory")
            all_ok = False

        # Publish-location-drift assertions.
        if 'publish-location-drift' in plugin_good_codes:
            print("FAIL: publish-location-drift fired on manifests agreeing on their publish location")
            all_ok = False
        if 'publish-location-drift' not in plugin_publish_drift_codes:
            print("FAIL: publish-location-drift did not fire when marketplace.json's repository disagreed with plugin.json's")
            all_ok = False
        if 'publish-location-drift' in good_codes:
            print("FAIL: publish-location-drift fired on a fixture root shipping no .claude-plugin/ directory")
            all_ok = False

        # Publish-location-drift mixed-URL-form assertions (WR-01):
        # normalising four GitHub URL forms must stay silent on genuine
        # agreement and still fire on genuine disagreement.
        if 'publish-location-drift' in plugin_mixed_url_codes:
            print("FAIL: publish-location-drift fired on carriers naming the same owner in different GitHub URL forms")
            all_ok = False
        if 'publish-location-drift' not in plugin_mixed_url_drift_codes:
            print("FAIL: publish-location-drift did not fire when the SSH-form carrier named a different owner from the others")
            all_ok = False

        # Multi-skill plugin-manifest assertions (WR-03): a repository
        # shipping other than exactly one skill folder must raise the
        # ambiguity rather than silently skip the checks that assume one.
        if 'plugin-manifest-invalid' not in plugin_multiskill_codes:
            print("FAIL: plugin-manifest-invalid did not fire when two skill folders existed")
            all_ok = False
        if 'plugin-manifest-version-mismatch' not in plugin_multiskill_codes:
            print("FAIL: plugin-manifest-version-mismatch did not fire when two skills stated disagreeing versions")
            all_ok = False

        # Required-key coverage matrix (Task 2, closing the class CR-01
        # exposed): every member of PLUGIN_REQUIRED_KEYS must make
        # plugin-manifest-invalid fire at both positions the docstring
        # claims to enforce it -- plugin.json's top-level object and
        # marketplace.json's plugin entry -- not just the one key at the
        # one position a single hand-built fixture happens to sample.
        # Presence is asserted, never exclusivity: deleting 'version'
        # legitimately also trips plugin-manifest-version-mismatch, and
        # this fixture-world root legitimately trips license-missing and
        # framework-statement-missing exactly as _good_plugin_manifests's
        # own root already does.
        required_key_matrix_misses = []
        for required_key in PLUGIN_REQUIRED_KEYS:
            for position in ('plugin.json', "marketplace.json's plugin entry"):
                slug = 'plugin' if position == 'plugin.json' else 'marketplace'
                cell_root = tmp_root / f'required_key_matrix_{slug}_{required_key}'
                _required_key_matrix_root(cell_root, position, required_key)
                cell_codes = {line.split(' ', 1)[0] for _, line in run_all_checks(cell_root)}
                if 'plugin-manifest-invalid' not in cell_codes:
                    print(f"FAIL: plugin-manifest-invalid did not fire for key '{required_key}' missing from {position}")
                    all_ok = False
                    required_key_matrix_misses.append((position, required_key))

        for code in ALL_CHECK_CODES:
            if code not in bad_codes:
                print(f"FAIL: {code} did not fire on the known-bad fixture")
                all_ok = False
                continue
            if code in good_codes:
                print(f"FAIL: {code} fired on the known-good fixture")
                all_ok = False
                continue
            codes_covered.add(code)

    if not all_ok:
        return False

    print(f"self-test PASS - verified violation codes: {', '.join(sorted(codes_covered))}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--mutation-test', action='store_true')
    args = parser.parse_args()

    if args.self_test:
        ok = self_test()
        sys.exit(0 if ok else 1)

    if args.mutation_test:
        ok = mutation_test(REPO_ROOT)
        sys.exit(0 if ok else 1)

    violations = run_all_checks(REPO_ROOT)
    violations.sort(key=lambda v: (v[1].split(' ', 1)[0], v[0]))
    if not violations:
        print("check_repo: 0 violations")
        sys.exit(0)
    for _, line in violations:
        print(line)
    sys.exit(1)


if __name__ == '__main__':
    main()
