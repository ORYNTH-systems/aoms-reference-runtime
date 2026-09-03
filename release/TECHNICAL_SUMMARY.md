AOMS Technical Summary

AOMS determines whether historical authorization remains execution-eligible under conditions current at effectuation time.

The v1 runtime compares authorized and current state across authority, policy, time, identity, dependency, resource, environment, action, and evidence dimensions. Material divergence produces deterministic decline.

The complete architecture requires an ordered six-engine composition:

authority-state reconstruction;
continuity verification;
boundary evaluation;
reconciliation;
execution-eligibility determination;
execution decision.

Phase II will expose each engine and canonical state object separately, preserve provenance between stages, and implement ALLOW, DENY, ESCALATE, and REAUTHORIZE.

The protected invariant is:

A valid historical authority artifact does not independently establish present execution permission.
