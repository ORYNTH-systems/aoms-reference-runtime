# AOMS v1-to-Canonical Crosswalk

| Canonical element | Published role | v1 representation | Phase II disposition |
|---|---|---|---|
| AuthorityArtifact | Historical authority evidence | `AuthorizedState` | Replace with evidence-bearing canonical object |
| AuthorityState | Reconstructed present authority conditions | Implicit in `CurrentState` | Implement separately |
| ContinuityVector | Per-dimension continuity evaluation | Direct equality comparisons | Implement separately |
| BoundaryAssessment | Boundary preservation or crossing evaluation | Partial environment and policy comparison | Implement separately |
| GovernanceState | Current governance conditions | Scattered fields | Implement separately |
| ExecutionContext | Present execution circumstances | Partial `CurrentState` | Implement separately |
| ReconciliationRecord | Material-divergence composition | `ReconciliationResult` | Expand to canonical outcomes |
| EligibilityRecord | Current admissibility determination | Boolean `admissibility` | Implement separately |
| ExecutionDecision | Terminal governed result | `APPROVED` or `DECLINED` | Implement four canonical decisions |
| Reconstruction engine | Reconstruct present Authority Conditions | Not separately represented | Implement |
| Continuity engine | Determine continuity by dimension | Collapsed into reconciliation | Implement |
| Boundary engine | Detect and classify boundary status | Not separately represented | Implement |
| Reconciliation engine | Compose material divergence | Simplified implementation | Refactor and expand |
| Eligibility engine | Determine governed eligibility | Boolean wrapper | Implement |
| Decision engine | Map eligibility to terminal decision | Binary mapping | Expand |
| Provenance chain | Link decision to originating evidence | Final JSON result only | Implement transitive references |
