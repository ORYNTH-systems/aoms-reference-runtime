# AOMS-RG-013 Failure Registry

| ID | Failure | Required Route |
| --- | --- | --- |
| AOMS-FL-001 | Missing critical input | DENY_OR_ESCALATE |
| AOMS-FL-002 | Malformed state object | DENY |
| AOMS-FL-003 | Engine unavailable | DENY_OR_ESCALATE |
| AOMS-FL-004 | Engine timeout | DENY_OR_ESCALATE |
| AOMS-FL-005 | Conflicting evidence | ESCALATE_OR_DENY |
| AOMS-FL-006 | Unknown boundary | ESCALATE_OR_DENY |
| AOMS-FL-007 | Incomplete provenance | DENY |
| AOMS-FL-008 | Pipeline bypass | DENY |
| AOMS-FL-009 | Invalid transition | DENY |
| AOMS-FL-010 | Cached permission reuse | DENY |
