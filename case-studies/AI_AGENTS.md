# AOMS Applied: AI Agents

## Status

Batch 06 domain profile. This profile maps ai agents execution boundaries to the canonical AOMS runtime and proof obligations.

## Governing problem

A technically available action is not necessarily eligible at effect time. Every proposed effect requires reconstructed authority, continuity, boundary, dependency, evidence, and policy state.

## Consequential effects

- Tool invocation.
- Credential use.
- Delegated action.
- External communication.
- Memory mutation.

## Mandatory controls

- Principal continuity.
- Delegation scope.
- Tool authority.
- Boundary identity.
- Effect-time policy.

## Decision mapping

- `ALLOW`: every required predicate is affirmatively satisfied.
- `DENY`: a nonrecoverable validity, dependency, or evidence failure exists.
- `ESCALATE`: a protected, ambiguous, or unknown boundary requires review.
- `REAUTHORIZE`: authority expired, changed, was revoked, or no longer covers the proposal.

## Proof obligations

The profile inherits fresh execution identity, terminality, complete provenance, fail-closed evaluation, non-expanding delegation, explicit unknown-state handling, and replay resistance.

## Benchmark linkage

Ten scenarios are registered in `benchmarks/AOMS-BENCH-001_DOMAIN_MATRIX.csv`. Scenario validation establishes profile completeness and decision coverage; runtime conformance remains governed by the canonical case suite and `AOMS-CONF-001`.

## Boundary

This profile is an architectural reference and does not substitute for domain law, professional judgment, institutional authorization, or operational certification.
