# AOMS-SPEC-004: Evidence and Provenance

## 1. Scope

This specification defines the minimum evidence and provenance requirements for an AOMS terminal decision.

## 2. Evidence principles

Evidence MUST be attributable, relevant to a declared predicate, bound to a version or observation time, and distinguishable from authority. Evidence MAY support an authority claim but MUST NOT create authority by itself.

## 3. Required terminal record

Each terminal record MUST contain:

- A unique execution identity.
- The proposed action and principal.
- Authority-artifact identity and status.
- Policy identity and version.
- Reconstructed-state identity or digest.
- Engine results and reason codes.
- Terminal decision.
- Evaluation time.
- Evidence references.
- Implementation/profile identity.

## 4. Completeness

Provenance is complete only when an independent evaluator can determine which proposal was evaluated, under which authority and policy, using which evidence, through which engine results, and why the terminal decision followed.

## 5. Unknown and conflicting evidence

Unknown mandatory evidence MUST remain unknown. Conflicting evidence MUST be surfaced and resolved by declared policy. Neither condition may be silently normalized into satisfaction.

## 6. Retention and redaction

Implementations MAY redact protected payload data, but MUST retain stable references, digests, classifications, and decision-relevant metadata sufficient to verify the decision without exposing the protected content.

## 7. Replay resistance

A prior terminal record MAY be used as evidence of a historical decision. It MUST NOT be accepted as present execution authority. Every new proposed effect requires a new execution identity and current-state evaluation.

## 8. Conformance

The conformance report MUST identify the evaluated profile, corpus size, checks performed, and aggregate pass state. A missing or failed mandatory check makes the profile nonconformant.
