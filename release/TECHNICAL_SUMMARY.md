# AOMS Technical Summary

AOMS determines whether historical authorization remains execution-eligible under conditions current at effectuation time.

The v1 runtime compares authorized and current state across authority, policy, time, identity, dependency, resource, environment, action, and evidence dimensions. Material divergence produces deterministic decline.

## Canonical Engine Sequence
1. Authority-state reconstruction
2. Continuity verification
3. Boundary evaluation
4. Reconciliation
5. Execution-eligibility determination
6. Execution decision

Phase II exposes each engine and canonical state object separately, preserves provenance between stages, and implements ALLOW, DENY, ESCALATE, and REAUTHORIZE.

## Protected Invariant
A valid historical authority artifact does not independently establish present execution permission.
