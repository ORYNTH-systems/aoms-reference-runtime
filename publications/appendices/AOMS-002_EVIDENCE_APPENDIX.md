# AOMS-002 Evidence Appendix

## Purpose

This appendix binds the principal mathematical claims in AOMS-002 to normative specifications, canonical runtime components, executable fixtures, and machine-generated proof reports.

## Closure set

Claims `AOMS-CP-001` through `AOMS-CP-008` cover the separation of capability and authority, effect-time reconstruction, unknown-state treatment, fresh identity, terminal decision completeness, expiration, dependency failure, and protected-boundary escalation.

## Evidence path

Each claim is resolved through `crosswalks/AOMS_CLAIM_TO_PROOF_MATRIX.csv`. The referenced fixtures were executed by `CanonicalPipeline`; expected decision, required reason, terminality, proof completeness, and provenance were verified. Batch 07 proof records are frozen by `reports/domain-execution/SHA256SUMS.txt`.

## Interpretation

Closure establishes correspondence between stated architecture and the reference implementation. It does not assert mathematical completeness beyond the declared model or external certification.
