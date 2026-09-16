# AOMS Applied: Civic Systems

## Status

Batch 06 domain profile. This profile maps civic systems execution boundaries to the canonical AOMS runtime and proof obligations.

## Governing problem

A technically available action is not necessarily eligible at effect time. Every proposed effect requires reconstructed authority, continuity, boundary, dependency, evidence, and policy state.

## Consequential effects

- Registration update.
- Ballot workflow.
- Tabulation action.
- Certification step.
- Public-record release.

## Mandatory controls

- Official authority.
- Constitutional scope.
- Chain continuity.
- Source integrity.
- Finality evidence.

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
