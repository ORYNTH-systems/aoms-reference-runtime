# AOMS-RG-004 Engine Registry

| ID | Engine | Required Input | Canonical Output |
| --- | --- | --- | --- |
| AOMS-ENG-001 | Reconstruction | AuthorityArtifact plus current conditions | AuthorityState |
| AOMS-ENG-002 | Continuity | AuthorityState plus historical evidence | ContinuityVector |
| AOMS-ENG-003 | Boundary | AuthorityState plus ExecutionContext | BoundaryAssessment |
| AOMS-ENG-004 | Reconciliation | Upstream objects plus GovernanceState | ReconciliationRecord |
| AOMS-ENG-005 | Eligibility | ReconciliationRecord plus GovernanceState | EligibilityRecord |
| AOMS-ENG-006 | Decision | EligibilityRecord | ExecutionDecision |
