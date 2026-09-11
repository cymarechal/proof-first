# The Deletion Test — Edge Cases

Open this file before applying PF-3.1 to a compound term, or to any term appearing in the
customer's own source material — the four classes below are exactly where a naive, whole-phrase
application of the test gets the verdict wrong. Each row is a worked pair, not a verdict-only
entry: the mechanism has to transfer to a term this skill has never seen before, not just to the
terms listed here.

| Class | Sentence with the term | Sentence with the term deleted | Verdict and why |
|---|---|---|---|
| Connotation-only terms | "The proposal delivers a robust, enterprise-grade landing zone." | "The proposal delivers a landing zone." | Buzzword — deleting "robust, enterprise-grade" changes nothing the sentence claims about the landing zone itself. Cut it. |
| Customer-first terms | "The new landing zone replaces the ungoverned VM sprawl Marcus Feld described." | "The new [deleted] replaces the ungoverned VM sprawl Marcus Feld described." | Retain and mark — "landing zone" is Marcus Feld's own term from discovery ("We need a landing zone we can actually govern"). The provenance override retains and marks a customer-verbatim term rather than deleting it, even though the whole-term test alone would flag it as jargon. |
| RFP-mandated wording | "Section 3 describes the operating model after go-live that Q3 asks for." | "Section 3 describes go-live that Q3 asks for." | Retain — "operating model" is Q3's own scored wording. Deleting it breaks alignment with the buyer's own scoring rubric, a value the sentence-only test cannot see. |
| Half-empty compounds | "The next-generation Oracle Database migration moves all 40 instances to the target platform." | "The Oracle Database migration moves all 40 instances to the target platform." | Partial — deleting "next-generation" changes nothing the sentence claims (buzzword, cut it); deleting "Oracle Database migration" would remove the only concrete technical noun in the sentence (retain it). Test each token separately so the buzzword cannot ride on the real noun. |
