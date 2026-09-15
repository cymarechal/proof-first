Kestrel Systems Group's architecture places Halverton Mutual's 850-VM VMware vSphere
estate onto Amazon EC2, with the 40-instance Oracle Database layer migrated to Amazon
Aurora PostgreSQL. AWS Control Tower governs the resulting account structure, giving
Marcus Feld's infrastructure team a landing zone they can actually manage rather than
a sprawl of individually configured hosts.

Our platform delivers best-in-class resilience for the settlement estate, and the
proposed design eliminates the manual failover process that currently extends
incident response whenever a host fails. Cut-over follows a wave-based sequence,
moving lower-risk workloads first and validating each wave before the next begins.

A risk worth naming: this program compresses discovery, build, and cut-over into a
timeline shorter than Kestrel Systems Group's own most comparable prior migration.
Our team is confident this is manageable given the strength of the proposed
architecture and our deep experience with regulated financial estates of this size.

The commercial model aligns to the contract's three-year term, with pricing
structured to reward early wave completion.
