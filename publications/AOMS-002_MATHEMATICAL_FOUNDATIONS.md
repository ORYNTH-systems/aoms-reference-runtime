# AOMS-002: Mathematical Foundations of Reconstruction-Governed Execution

## Status

Phase II working manuscript. This document formalizes the AOMS execution-eligibility model implemented by the canonical reference runtime.

## Abstract

A capable system may possess the technical means to cause an effect while lacking current authority to do so. AOMS resolves this gap by reconstructing the governing execution state at the moment of proposed effect. The runtime evaluates authority, continuity, boundaries, dependencies, and evidence before issuing one of four terminal decisions: `ALLOW`, `DENY`, `ESCALATE`, or `REAUTHORIZE`. This paper defines the state space, reconstruction operator, admissibility relation, decision function, invariants, and proof obligations needed to make that process deterministic and auditable.

## 1. Execution state

Let a proposed execution be represented by

\[
x=(a,c,b,d,e,p)
\]

where `a` is the authority artifact, `c` the current execution context, `b` the boundary assessment, `d` the dependency state, `e` the evidence state, and `p` the governing policy state.

The authorized state is not presumed to remain valid merely because it was valid when first issued. AOMS therefore evaluates the reconstructed state

\[
R_t(x)=\langle A_t,C_t,B_t,D_t,E_t,P_t\rangle
\]

at effect time `t`.

## 2. Reconstruction operator

The reconstruction operator is deterministic over a fixed input record and policy version:

\[
R_t:X\times P\rightarrow S
\]

It must preserve provenance, expose unknown values, and never convert missing evidence into affirmative authority. Reconstruction is complete only when every decision-relevant dimension is represented or explicitly marked unresolved.

## 3. Eligibility predicates

Define the predicates:

- `Auth(s)`: authority is valid, scoped, unrevoked, and unexpired.
- `Cont(s)`: actor, principal, action, and relevant state remain continuous.
- `Bound(s)`: no protected boundary requires human or higher-order review.
- `Dep(s)`: required dependencies remain available and conformant.
- `Evid(s)`: required evidence is present, attributable, and current.

The admissibility predicate is

\[
Adm(s)=Auth(s)\land Cont(s)\land Bound(s)\land Dep(s)\land Evid(s).
\]

An `ALLOW` decision requires `Adm(s)=true`. The converse is intentionally not generalized to all non-allow outcomes because distinct failed predicates carry distinct governance consequences.

## 4. Terminal decision function

Let

\[
\delta:S\rightarrow\{ALLOW,DENY,ESCALATE,REAUTHORIZE\}.
\]

Precedence is safety preserving:

1. Invalid action, dependency failure, or nonrecoverable evidence failure yields `DENY`.
2. Expired, revoked, or materially changed authority yields `REAUTHORIZE`.
3. A protected, ambiguous, personal, psychological, therapeutic, or unknown boundary yields `ESCALATE`.
4. Only a fully satisfied state yields `ALLOW`.

Every result is terminal for the evaluated execution identity. A retry is a new proposed execution and receives a fresh identity and evaluation.

## 5. Core invariants

- Capability is not authority.
- Access is not execution eligibility.
- Prior admissibility is not present admissibility.
- Evidence is not self-executing authority.
- Unknown state cannot satisfy an affirmative predicate.
- Delegation cannot expand the authority received.
- Every execution attempt has a unique evaluation identity.
- Every terminal decision retains complete provenance.
- Runtime failure fails closed.

## 6. Monotonicity and non-monotonic authority

Evidence accumulation may be monotone, but authority validity is not. New evidence can improve knowledge while expiry, revocation, policy change, or principal change can invalidate execution eligibility. Therefore AOMS does not infer current permission from a previously successful decision.

## 7. Proof obligations

A conformant implementation must demonstrate deterministic reconstruction, terminal decision completeness, fail-closed behavior, provenance completeness, fresh execution identity, bounded delegation, explicit unknown-state handling, and equivalence with declared legacy outcomes.

## 8. Runtime correspondence

The canonical objects and engines are implemented in `src/canonical/`. Conformance requirements are operationalized by `src/conformance.py`, while the canonical proof corpus occupies `cases/canonical/AOMS-101.json` through `AOMS-350.json`.

## 9. Limits

This formalization establishes execution-governance semantics. It does not assert that a policy is lawful, morally sufficient, or institutionally legitimate merely because it is machine-readable. Those questions remain external proof obligations that must be bound into the authority and evidence layers.
