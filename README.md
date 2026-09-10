# Adaptive Orchestration Management System

## Reconstruction-Governed Execution at Effectuation Time

The Adaptive Orchestration Management System (AOMS) is an execution-governance architecture for determining whether a previously authorized action remains eligible when execution is actually attempted.

AOMS separates two conditions that conventional systems frequently collapse:

```text
Historical authorization != present execution permission
```

Historical authorization is evidence. Execution permission is a current determination reconstructed from authority-relevant conditions at or near effectuation time.

## Governing Pipeline

```text
AuthorityArtifact
    -> AuthorityState
    -> ContinuityVector
    -> BoundaryAssessment
    -> ReconciliationRecord
    -> EligibilityRecord
    -> ExecutionDecision
```

The canonical decision space is:

- `ALLOW`
- `DENY`
- `ESCALATE`
- `REAUTHORIZE`

An affirmative decision is unavailable unless the complete ordered pipeline positively establishes present execution eligibility.

## Current Repository Baseline

Version 1 contains:

- 100 deterministic execution cases;
- 100 corresponding evidence artifacts;
- 10 state-family reports;
- a replayable Python runtime;
- doctrine and execution-specification documents;
- authority, policy, temporal, identity, dependency, resource, environmental, agentic, evidence, and compound-state coverage.

All 100 v1 cases are deliberately inadmissible controls. They demonstrate that changed execution conditions defeat automatic execution despite prior authorization.

Version 1 is retained as a historical baseline. Phase II will implement the complete canonical pipeline and a balanced four-decision verification corpus.

## Existing State Families

| Range | State family |
|---|---|
| AOMS-001 - AOMS-010 | Authority |
| AOMS-011 - AOMS-020 | Policy |
| AOMS-021 - AOMS-030 | Temporal |
| AOMS-031 - AOMS-040 | Identity |
| AOMS-041 - AOMS-050 | Dependency |
| AOMS-051 - AOMS-060 | Resource |
| AOMS-061 - AOMS-070 | Environment |
| AOMS-071 - AOMS-080 | Agentic |
| AOMS-081 - AOMS-090 | Evidence |
| AOMS-091 - AOMS-100 | Compound |

## Run the Existing Demonstration

From the repository root:

```powershell
python .\src\main.py --case .\cases\AOMS-001.json
python .\src\main.py --all
```

The v1 runtime produces deterministic violation findings and writes evidence artifacts under `reports/json`.

## Phase II

Phase II will add:

- separate reconstruction, continuity, boundary, reconciliation, eligibility, and decision engines;
- canonical immutable state objects;
- explicit governance and execution contexts;
- authority and delegation reconstruction;
- agent-readable boundary evaluation;
- complete provenance chains;
- four-outcome decision semantics;
- failure-injection and bypass testing;
- balanced positive and negative controls;
- multi-agent and cross-boundary execution cases;
- conformance specifications and formal proof obligations.

See `architecture/PHASE_II_ARCHITECTURE_MANIFEST.md` and `ROADMAP.md`.

## Foundational Publication

Ashley S. Harris, "Adaptive Orchestration Management System (AOMS): Reconstruction-Governed Execution Eligibility Determination for Autonomous and Distributed Systems," 2026.

DOI: https://doi.org/10.5281/zenodo.20673754

## Software Record

DOI: https://doi.org/10.5281/zenodo.20819505

## Author

Ashley S. Harris
Independent Researcher
ORYNTH Systems

## Status

- v1 corpus: complete historical baseline
- Phase II canonicalization: active
- Phase II runtime: pending Batch 02
- Phase II verification corpus: pending Batch 03
- specifications and manuals: pending Batch 04
- publication extensions: pending Batch 05
