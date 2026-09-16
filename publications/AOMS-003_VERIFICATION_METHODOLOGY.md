# AOMS-003: Verification Methodology for Reconstruction-Governed Systems

## Status

Phase II working manuscript defining reproducible verification of AOMS implementations.

## Abstract

Verification of an execution-governance runtime requires more than checking whether expected examples pass. It must establish that the implementation preserves decision semantics under adversarial state changes, produces attributable evidence, distinguishes governance outcomes, and fails closed when evaluation cannot complete. This methodology defines unit, corpus, metamorphic, fault-injection, provenance, equivalence, and release-level verification.

## 1. Verification target

The target is the complete path from proposed execution through reconstruction, reconciliation, eligibility determination, governance classification, and terminal decision. Tests must verify both the outcome and the evidence explaining the outcome.

## 2. Verification layers

### 2.1 Object validation

Verify required fields, enumerated states, timestamps, stable identifiers, and rejection of malformed objects.

### 2.2 Engine isolation

Exercise authority, continuity, boundary, dependency, evidence, and decision engines independently before pipeline composition.

### 2.3 Canonical corpus

Run the declared case range without omission or duplication. Verify exact decision distribution and required reason codes.

### 2.4 Metamorphic testing

Starting from an admissible control, mutate one decision-relevant dimension at a time. The result must move to the outcome required by the governing rule while unrelated provenance remains stable.

### 2.5 Fault injection

Interrupt evaluation, remove required evidence, corrupt a dependency, introduce an unknown boundary, expire authority, and simulate internal exceptions. No failure may produce `ALLOW`.

### 2.6 Replay testing

Repeat equivalent inputs and verify deterministic semantics but fresh evaluation identity. A prior decision must not become reusable execution authority.

### 2.7 Legacy equivalence

Where a legacy corpus is retained, verify declared outcome equivalence without silently rewriting the historical artifacts.

## 3. Required metrics

- Total cases evaluated.
- Exact case identity coverage.
- Decision distribution.
- Expected-versus-actual agreement.
- Reason-code agreement.
- Provenance completeness.
- Fresh-identity rate.
- Fail-closed fault outcomes.
- Unresolved proof obligations.

## 4. Admission rule

A release is admissible only if all mandatory tests pass, no case is silently skipped, all terminal decisions contain required provenance, every injected evaluator failure fails closed, and the generated report is bound to the evaluated profile and corpus.

## 5. Reproducibility

Verification commands, schemas, case registries, requirements, proof obligations, and machine-readable results must be versioned with the runtime. A narrative assertion of conformance is insufficient without a reproducible evidence path.

## 6. Current reference baseline

The reference baseline contains 100 preserved v1 adversarial cases and 250 canonical cases. The canonical wave includes all four terminal decisions and agent-readable boundary classes. `AOMS-CONF-001` evaluates the canonical suite and records its result under `reports/conformance/`.

## 7. Extension protocol

New domains may add policies, evidence types, or boundary classes, but must not weaken the core invariants. Extensions must declare their objects, decisions, proof obligations, test vectors, and mapping to canonical semantics.
