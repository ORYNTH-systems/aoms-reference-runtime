# AOMS-RG-008 Violation Registry

| Code | Family | Default Route |
| --- | --- | --- |
| authority_invalid | Authority | DENY |
| authorization_expired | Temporal | DENY |
| execution_too_early | Temporal | DENY |
| identity_continuity_failed | Identity | DENY |
| action_drift_detected | Agentic | DENY |
| policy_changed | Policy | RECONCILE |
| dependency_state_changed | Dependency | RECONCILE |
| resource_unavailable | Resource | DENY |
| environment_invalid | Environment | DENY |
| evidence_insufficient | Evidence | ESCALATE_OR_DENY |
| boundary_crossed | Boundary | REAUTHORIZE_OR_DENY |
| pipeline_bypass_attempted | Architecture | DENY |
| provenance_incomplete | Evidence | DENY |
