# AOMS Dependency State Category Report

## Scope

This report covers AOMS-041 through AOMS-050.

The Dependency State category tests whether execution is declined when a required dependency that supported prior authorization no longer remains valid at execution time.

## Cases

AOMS-041 Dependency State Changed
AOMS-042 Required Service Unavailable
AOMS-043 External API State Changed
AOMS-044 Data Source Invalidated
AOMS-045 Vendor Dependency Suspended
AOMS-046 Contract Dependency Terminated
AOMS-047 Certificate Dependency Expired
AOMS-048 Required Approval Missing
AOMS-049 Upstream Process Failed
AOMS-050 Dependency Chain Break

## Expected Violation

dependency_state_changed

## Expected Result

All executions declined.

## Architectural Finding

Execution eligibility depends on the current validity of required dependencies. A prior authorization does not remain execution-admissible when dependency state changes before execution.

## Protected Invariant

Prior authorization does not guarantee present execution eligibility.
