AOMS Phase II Architecture Manifest
Objective

Implement the published reconstruction-governed execution pipeline as a typed, deterministic, fail-closed, provenance-complete reference runtime.

Canonical Composition
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
Required State Objects
AuthorityArtifact
AuthorityState
ContinuityVector
BoundaryAssessment
GovernanceState
ExecutionContext
ReconciliationRecord
EligibilityRecord
ExecutionDecision
Required Engines
Authority-State Reconstruction Engine
Continuity Verification Engine
Boundary Evaluation Engine
Reconciliation Engine
Execution-Eligibility Engine
Execution-Decision Engine
Required Decisions
ALLOW
DENY
ESCALATE
REAUTHORIZE
Phase II Safety Rules
No engine may emit ALLOW.
Only the decision engine may emit a terminal decision.
The decision engine may emit ALLOW only from positive EligibilityRecord state.
Unknown, malformed, incomplete, or unavailable critical state cannot produce ALLOW.
Historical authority evidence cannot bypass reconstruction.
No cached ExecutionDecision may authorize a later governed execution point.
Every terminal decision must contain a complete provenance path.
Each engine must consume the canonical output of its required predecessor.
The v1 runtime remains available through a compatibility adapter.
