# AOMS-SPEC-001: Canonical Reconstruction-Governed Runtime

Status: Phase II reference implementation  
Version: 2.0.0  
Authority: Ashley S. Harris / ORYNTH

## Normative pipeline

Every execution attempt MUST be evaluated from fresh source state in this order:

1. `AuthorityArtifact` is reconstructed into `AuthorityState`.
2. `ExecutionContext` is compared into a `ContinuityVector`.
3. agent-readable signals become a `BoundaryAssessment`.
4. differences become a `ReconciliationRecord`.
5. the record becomes an `EligibilityRecord`.
6. only the decision engine emits an `ExecutionDecision`.

`GovernanceState` binds stages 1-5. No intermediate engine may authorize execution.

## Decisions

- `ALLOW`: authority is effective, continuity holds, no boundary is crossed, reconciliation is resolved, and provenance is complete.
- `DENY`: execution is ineligible without a condition requiring escalation or renewed authority.
- `ESCALATE`: a personal, psychological, therapeutic, safety, or unknown boundary requires review outside autonomous execution.
- `REAUTHORIZE`: authority, identity, action, policy, actor, or temporal scope must be renewed or reconstructed.

## Safety invariants

- Capability does not establish authority.
- Missing or failed proof produces no permission.
- Runtime exceptions fail closed to terminal `DENY`.
- Every evaluation receives a new execution identity; cached terminal decisions are not reused.
- Provenance crosses every stage and binds the terminal decision.
- Boundary labels are machine-readable governance signals, not diagnoses or factual claims about a person.
- The v1 adapter preserves `APPROVED` only for canonical `ALLOW`; all other decisions preserve `DECLINED`.

## Public boundary

This reference implementation exposes interfaces, deterministic logic, tests, and trace semantics. It does not disclose private claim strategy, unpublished embodiment detail, proprietary training material, or confidential deployment policy.
