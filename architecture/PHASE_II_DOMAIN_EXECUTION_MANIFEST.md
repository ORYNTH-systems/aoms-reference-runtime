# AOMS Phase II Domain Execution Manifest

## Wave

Batch 07 converts the 60 Batch 06 design-validated scenarios into executable canonical fixtures and evaluates every fixture through `CanonicalPipeline`.

## Required outputs

- 60 JSON fixtures under `cases/domains/`.
- One execution registry.
- Six domain proof reports.
- One aggregate proof report.
- One SHA-256 freeze manifest.
- One executable runner and one regression test module.
- One domain-case schema.

## Admission requirements

- Exactly 60 unique case identities.
- Exactly ten cases per domain.
- Exactly fifteen results per terminal decision.
- Expected and actual decisions agree for every case.
- Every result is terminal and proof-complete.
- Every decision contains its fresh execution identity in provenance.
- Replay creates a new execution identity.
- All pre-existing runtime, canonical-corpus, conformance, and publication tests remain green.
- The freeze manifest contains every fixture, proof report, and the execution registry.

## Status semantics

`EXECUTION-VERIFIED` means the fixture was evaluated by the canonical reference runtime and its required outcome, reason, terminality, proof completeness, and provenance checks passed. It does not claim external certification or domain-law approval.
