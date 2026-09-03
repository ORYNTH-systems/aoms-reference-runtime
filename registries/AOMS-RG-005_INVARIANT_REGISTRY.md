# AOMS-RG-005 Invariant Registry

| ID | Invariant | Requirement |
| --- | --- | --- |
| AOMS-INV-001 | Authorization Non-Implication | Historical authorization cannot independently establish execution permission. |
| AOMS-INV-002 | Temporal Authority Non-Persistence | Authority valid at one time is not automatically permission at another. |
| AOMS-INV-003 | Reconstruction Requirement | Eligibility requires current-condition reconstruction. |
| AOMS-INV-004 | Fail-Closed Enforcement | Unestablished admissibility cannot produce ALLOW. |
| AOMS-INV-005 | Dependency Ordering | No required pipeline stage may be bypassed or substituted. |
| AOMS-INV-006 | Permission Non-Cacheability | A prior decision cannot authorize a later governed execution point. |
| AOMS-INV-007 | Decision Exclusivity | Only the decision engine emits terminal outcomes. |
| AOMS-INV-008 | Provenance Completeness | Every terminal decision links transitively to originating evidence. |
| AOMS-INV-009 | Cross-Agent Non-Inheritance | One agent cannot inherit another agent's execution permission. |
| AOMS-INV-010 | Boundary Sensitivity | Material boundary change must affect eligibility. |
