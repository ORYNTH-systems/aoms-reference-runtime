# AOMS Phase II Architecture Manifest

## Objective

Implement the published reconstruction-governed execution pipeline as a typed, deterministic, fail-closed, provenance-complete reference runtime.

## Canonical Composition

```text
Decision(
  Eligibility(
    Reconcile(
      Boundary(
        Continuity(
          Reconstruct(Evidence, CurrentConditions)
        )
      )
    )
  )
)
```

The composition is ordered and semantically load-bearing. No downstream stage may substitute for a required upstream producer.

## Required State Objects

1. `AuthorityArtifact`
2. `AuthorityState`
3. `ContinuityVector`
4. `BoundaryAssessment`
5. `GovernanceState`
6. `ExecutionContext`
7. `ReconciliationRecord`
8. `EligibilityRecord`
9. `ExecutionDecision`

## Required Engines

1. Authority-State Reconstruction Engine
2. Continuity Verification Engine
3. Boundary Evaluation Engine
4. Reconciliation Engine
5. Execution-Eligibility Engine
6. Execution-Decision Engine

## Required Decisions

- `ALLOW`
- `DENY`
- `ESCALATE`
- `REAUTHORIZE`

## Phase II Safety Rules

- No upstream engine may emit `ALLOW`.
- Only the decision engine may emit a terminal decision.
- The decision engine may emit `ALLOW` only from a positive EligibilityRecord.
- Unknown, malformed, incomplete, or unavailable critical state cannot produce `ALLOW`.
- Historical authority evidence cannot bypass reconstruction.
- A cached ExecutionDecision cannot authorize a later governed execution point.
- Every terminal decision must contain a complete provenance path.
- Each engine must consume the canonical output of its required predecessor.
- The v1 runtime must remain available through a compatibility adapter.
