# Canonical Runtime Trace

## Object and engine binding

| Input | Engine | Output | Terminal authority |
|---|---|---|---|
| `AuthorityArtifact` + `ExecutionContext` | Authority-state reconstruction | `AuthorityState` | No |
| `AuthorityArtifact` + `ExecutionContext` | Continuity verification | `ContinuityVector` | No |
| `ExecutionContext.boundary_signals` | Boundary evaluation | `BoundaryAssessment` | No |
| Prior three stage outputs | Reconciliation | `ReconciliationRecord` | No |
| Authority + reconciliation | Eligibility | `EligibilityRecord` | No |
| Bound `GovernanceState` | Decision | `ExecutionDecision` | Yes |

## Compatibility

The canonical layer is additive. The original v1 source files and 100-case corpus remain unchanged. `canonical.adapter` translates v1 objects into the Phase II model and proves binary outcome compatibility across the complete corpus.

## Boundary identity

The boundary engine recognizes operational, authority, identity, personal, psychological, therapeutic, and safety classes. Unknown signals escalate rather than disappearing. These labels identify governance boundaries for an agent; they do not diagnose users, infer mental state, or grant an agent independent authority.
