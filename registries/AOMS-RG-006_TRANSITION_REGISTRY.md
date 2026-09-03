# AOMS-RG-006 Transition Registry

| ID | From | To | Condition |
| --- | --- | --- | --- |
| AOMS-TR-001 | AUTHORIZED | PENDING_EXECUTION | Execution requested |
| AOMS-TR-002 | PENDING_EXECUTION | RECONSTRUCTION | Governance initiated |
| AOMS-TR-003 | RECONSTRUCTION | CONTINUITY_EVALUATION | AuthorityState produced |
| AOMS-TR-004 | CONTINUITY_EVALUATION | BOUNDARY_EVALUATION | ContinuityVector produced |
| AOMS-TR-005 | BOUNDARY_EVALUATION | RECONCILIATION | BoundaryAssessment produced |
| AOMS-TR-006 | RECONCILIATION | ELIGIBILITY_DETERMINATION | ReconciliationRecord produced |
| AOMS-TR-007 | ELIGIBILITY_DETERMINATION | EXECUTION_DECISION | EligibilityRecord produced |
| AOMS-TR-008 | EXECUTION_DECISION | ALLOW | Positive eligibility |
| AOMS-TR-009 | EXECUTION_DECISION | DENY | Blocking or failed admissibility |
| AOMS-TR-010 | EXECUTION_DECISION | ESCALATE | Authorized review required |
| AOMS-TR-011 | EXECUTION_DECISION | REAUTHORIZE | Fresh authority required |
