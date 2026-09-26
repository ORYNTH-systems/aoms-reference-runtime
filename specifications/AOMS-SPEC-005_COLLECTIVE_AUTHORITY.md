# AOMS-SPEC-005: Collective Authority and Composed Admissibility

Status: Phase III normative profile
Authority: Ashley S. Harris / ORYNTH

## Scope

This specification governs execution requiring multiple participants, principals, roles, delegations, or approvals. Collective capability, agreement, and quorum do not independently establish authority.

## Required reconstruction

Every required participant MUST receive an independent canonical AOMS evaluation. A participant MUST NOT inherit another participant's terminal permission. The coordinator MUST possess current authority to coordinate the collective request. Coordinator authority does not transfer to participants, and participant authority does not establish coordinator authority.

## Delegation and scope

Every delegation link MUST preserve attributable delegator and delegate identities, current validity, and action scope. A downstream scope MUST be a subset of its parent scope. Multiple insufficient scopes MUST NOT be accumulated into sufficient authority.

## Collective admissibility

`ALLOW` requires all of the following:

1. the coordinator is authorized;
2. every required role is bound;
3. every required participant is independently admissible;
4. every delegation path is valid;
5. every participant scope contains the proposed action;
6. the declared quorum is satisfied by unique admissible identities;
7. separation-of-duties constraints remain satisfied; and
8. collective provenance is complete.

Quorum is a lawful decision rule only after authority is established. It cannot manufacture authority.

## Outcome precedence

A required participant's protected boundary produces `ESCALATE`. A required participant needing renewed authority produces `REAUTHORIZE`. Unmet quorum, invalid delegation, scope enlargement, duplicate identity, missing role, or separation-of-duties failure produces `DENY` unless a higher-precedence protected outcome applies.

## Accountability

Distribution MUST NOT dissolve accountability. The terminal record MUST bind the collective request, coordinator, participants, roles, participant decisions, delegation and scope results, collective checks, and fresh collective execution identity.
