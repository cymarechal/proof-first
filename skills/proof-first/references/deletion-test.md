# The Deletion Test: Edge Cases

Open this file before applying PF-3.1 to a compound term, or to any term appearing in the
customer's own source material; the four classes below are exactly where a naive, whole-phrase
application of the test gets the verdict wrong. Each row is a worked pair, not a verdict-only
entry: the mechanism has to transfer to a term this skill has never seen before, not just to the
terms listed here.

| Class | Sentence with the term | Sentence with the term deleted | Verdict and why |
|---|---|---|---|
| Connotation-only terms | "The proposal delivers a robust, enterprise-grade landing zone." | "The proposal delivers a landing zone." | Buzzword: deleting "robust, enterprise-grade" changes nothing the sentence claims about the landing zone itself. Cut it. |
| Customer-first terms | "The new landing zone replaces the ungoverned VM sprawl Marcus Feld described." | "The new [deleted] replaces the ungoverned VM sprawl Marcus Feld described." | Retain and mark: "landing zone" is Marcus Feld's own term from discovery ("We need a landing zone we can actually govern"). The provenance override retains and marks a customer-verbatim term rather than deleting it, even though the whole-term test alone would flag it as jargon. |
| RFP-mandated wording | "Section 3 describes the operating model after go-live that Q3 asks for." | "Section 3 describes go-live that Q3 asks for." | Retain: "operating model" is Q3's own scored wording. Deleting it breaks alignment with the buyer's own scoring rubric, a value the sentence-only test cannot see. |
| Half-empty compounds | "The next-generation Oracle Database migration moves all 40 instances to the target platform." | "The Oracle Database migration moves all 40 instances to the target platform." | Partial: deleting "next-generation" changes nothing the sentence claims (buzzword, cut it); deleting "Oracle Database migration" would remove the only concrete technical noun in the sentence (retain it). Test each token separately so the buzzword cannot ride on the real noun. |

## Testing a compound term token by token

A whole-phrase deletion test on a compound term can give the wrong verdict, because deleting the
entire compound removes the real technical noun along with the decoration riding on it: the
sentence loses its only concrete claim, so the whole phrase looks load-bearing and passes,
incorrectly, when only half of it ever needed to survive on its own.

Whole-phrase test: "The migration modernizes the estate with a resilient Amazon Aurora PostgreSQL
data layer." Delete the entire compound, "a resilient Amazon Aurora PostgreSQL data layer": "The
migration modernizes the estate." The sentence loses its only concrete claim, so the whole phrase
reads as load-bearing and passes (the wrong verdict, because "resilient" never had to survive
independently of the noun it rides on.

Per-token test: delete "resilient" alone: "The migration modernizes the estate with an Amazon
Aurora PostgreSQL data layer." Nothing the sentence claims about the data layer changes: cut it.
Delete "Amazon Aurora PostgreSQL" alone: "The migration modernizes the estate with a resilient
data layer." The only concrete technical noun in the sentence is gone and there is nothing left to
check: retain it. Testing each token independently is what isolates the buzzword the
whole-phrase test let through.

## What counts as supplied customer source material

`PF-3.3`'s override fires only against material the writer actually supplied as customer source
material for this task (RFP question text, discovery-call notes, and stated requirements the
buyer put in writing or said aloud. It does not fire against anything Kestrel Systems Group itself
wrote, however close the wording: a vendor's own draft cannot become the customer's term by being
reused. Without supplied source material, the override does not fire and every term is judged by
the deletion test alone (provenance).

Worked instance (both markers on one phrase): Marcus Feld's discovery quote supplies the term
"landing zone" verbatim ("We need a landing zone we can actually govern; right now every VM is a
snowflake"). A sentence retaining that term while also promising something this catalog cannot
verify carries both markers at once:

✗ "The proposal replaces ungoverned VM sprawl with a landing zone that will be fully governed
   from day one."
✓ "The proposal replaces ungoverned VM sprawl with a landing zone
   [PF-3.3: customer's term, retained: Marcus Feld, discovery] that will be fully governed
   from day one: [PF-2.14 REVIEW (commitment): confirm 'fully governed from day one' before
   this ships]."

Retention and the `REVIEW` flag are answering different questions about the same phrase:
retention says this is the buyer's own vocabulary and it stays; `REVIEW` says a human still has to
confirm the promise is one Kestrel Systems Group can keep. Neither one substitutes for the other.

## What this file does not do

This file does not enumerate a list of banned or allowed terms. A list is stale on arrival, and it
gets the noun-versus-modifier boundary wrong in both directions: a term that is legal in one
sentence because it carries evidence can be decorative in the next. The classes and worked
instances above teach the mechanism so it transfers to a term this skill has never seen before,
which a static list cannot do.
