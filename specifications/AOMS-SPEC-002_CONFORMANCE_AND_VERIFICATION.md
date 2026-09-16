# AOMS-SPEC-002: Conformance and Verification Profile

Status: Phase II normative profile

An implementation conforms only when it preserves the ordered reconstruction pipeline, emits terminal decisions solely through the decision engine, fails closed, generates fresh execution identity, carries complete provenance, recognizes registered and unknown boundary signals, preserves declared compatibility, and passes the canonical proof corpus.

## Required evidence

Conformance requires machine-readable requirements, discharged proof obligations, full corpus results, fault-injection results, and a reproducible report. A passing test count alone is insufficient without traceability from each requirement to its evidence.

## Decision coverage

The reference profile requires evidence for `ALLOW`, `DENY`, `ESCALATE`, and `REAUTHORIZE`. Absence of any decision family is incomplete coverage.

## Boundary coverage

Personal, psychological, therapeutic, safety, operational, authority, identity, and unknown boundary classes must remain agent-readable. Boundary labels are governance signals, not diagnoses.
