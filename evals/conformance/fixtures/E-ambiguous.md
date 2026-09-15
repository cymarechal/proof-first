This draft covers the proposed architecture for moving Halverton Mutual's 850-VM
VMware vSphere estate and 40 Oracle Database instances onto Amazon EC2 and Amazon
Aurora PostgreSQL, and it also lays out the discovery walkthrough and live demo
sequence planned for Marcus Feld's infrastructure team next week.

The architecture section proposes AWS Control Tower for landing-zone governance,
replacing today's manually configured account sprawl with best-in-class guardrails.
Cut-over follows a wave-based sequence designed to protect the nightly settlement
batch window throughout the migration.

The discovery and demo section walks through what was heard in the last session —
the team calling every VM "a snowflake" and wanting a landing zone they can
actually govern — and lays out demo steps: show the current estate, show the
target estate side by side, then simulate a failover live so the team can see the
manual-intervention problem disappear in the proposed design.

Both halves reference the same $6,000,000, three-year program and the same
regulatory examination deadline driving Halverton Mutual's urgency.
