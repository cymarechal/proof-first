Discovery notes from the Halverton Mutual walkthrough: the infrastructure team
described every VM in the current VMware vSphere estate as "a snowflake," each
configured slightly differently from the last, which is why failover across the
850-VM estate still requires manual intervention. One team member said the
settlement batch job "just runs long some nights, nobody's ever really measured
it," which lines up with the pain point Halverton Mutual raised earlier about
having no instrumented baseline for the overrun.

Demo steps for the next session: show the target Amazon EC2 compute layer and the
Amazon Aurora PostgreSQL data layer side by side with the current on-premises
estate, then walk through a simulated failover to demonstrate the proposed
landing-zone governance under AWS Control Tower. Close with a walkthrough of how
the settlement batch window would be protected under the new architecture.

The demo should leave the audience with world-class confidence in the migration
approach and make clear this is the best possible path off the Oracle Database
estate before the next regulatory examination opens.
