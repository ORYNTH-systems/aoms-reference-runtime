# AOMS Identity State Category Report

## Scope

This report covers AOMS-031 through AOMS-040.

The Identity State category tests whether execution is declined when the identity continuity supporting authorization no longer remains valid at execution time.

## Cases

AOMS-031 Actor Identity Changed
AOMS-032 Account Ownership Changed
AOMS-033 Identity Verification Failed
AOMS-034 Credential Subject Mismatch
AOMS-035 Delegated Actor Mismatch
AOMS-036 Human Operator Reassigned
AOMS-037 Agent Instance Changed
AOMS-038 Session Identity Lost
AOMS-039 Counterparty Identity Changed
AOMS-040 Identity Continuity Failure

## Expected Violation

identity_continuity_failed

## Expected Result

All executions declined.

## Architectural Finding

Authorization remains bound to identity continuity. Identity state drift invalidates execution eligibility even when authority, policy, dependency, resource, and environmental conditions remain unchanged.

## Protected Invariant

Authorization does not survive identity discontinuity.
