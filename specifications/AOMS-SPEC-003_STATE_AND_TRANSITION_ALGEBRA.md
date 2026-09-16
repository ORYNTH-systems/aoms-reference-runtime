# AOMS-SPEC-003: State and Transition Algebra

## 1. Scope

This specification defines canonical state categories, transition semantics, outcome precedence, and invariants for reconstruction-governed execution.

## 2. Normative terms

`MUST`, `MUST NOT`, `SHALL`, `SHALL NOT`, `SHOULD`, and `MAY` are normative.

## 3. State tuple

An evaluation state SHALL contain authority, context, continuity, boundary, dependency, evidence, policy, and provenance dimensions. Missing mandatory dimensions MUST be represented as unresolved and MUST NOT be treated as satisfied.

## 4. Transition sequence

The canonical sequence is `PROPOSED -> RECONSTRUCTED -> RECONCILED -> ELIGIBILITY-DETERMINED -> TERMINAL`.

An implementation MUST NOT enter `TERMINAL:ALLOW` before completing all mandatory engines. A terminal record MUST be immutable. A retry MUST create a new execution identity.

## 5. Decision algebra

Let `F` denote a nonrecoverable validity failure, `R` an authority condition requiring renewed authorization, `E` a protected or unresolved boundary, and `V` complete validity.

| Condition | Decision |
|---|---|
| `F` | `DENY` |
| `not F and R` | `REAUTHORIZE` |
| `not F and not R and E` | `ESCALATE` |
| `V` | `ALLOW` |

`ALLOW` MUST be issued only when every required affirmative predicate is true.

## 6. Invariants

- Terminal decisions MUST be one of the four canonical values.
- Unknown mandatory state MUST NOT yield `ALLOW`.
- Delegated authority MUST NOT exceed its parent scope.
- Changed principals MUST trigger renewed evaluation.
- Expired or revoked authority MUST NOT be reused.
- Internal evaluation failure MUST fail closed.
- Provenance MUST identify the policy and execution identity.

## 7. Conformance

Conformance requires the proof obligations in `conformance/AOMS-PROOF-OBLIGATIONS.csv` and the verification methodology in `publications/AOMS-003_VERIFICATION_METHODOLOGY.md`.
