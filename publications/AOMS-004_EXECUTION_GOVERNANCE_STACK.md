# AOMS-004: The ORYNTH Execution Governance Stack

## Status

Phase II systems-paper working manuscript.

## Abstract

Execution governance requires several separable questions: who or what possesses authority, whether an action remains eligible at effect time, how consequences are contained, and what evidence survives the decision. This paper positions AOMS as the reconstruction and execution-eligibility layer within the broader ORYNTH architecture. It describes interfaces to authority, integrity, proof, audit, and domain-specific systems without collapsing those layers into one mechanism.

## 1. Architectural problem

Authentication establishes identity, access control grants entry, and orchestration coordinates capability. None independently proves that a specific effect remains authorized under current conditions. AOMS occupies that missing effect-time boundary.

## 2. Layer separation

| Layer | Governing question | AOMS relationship |
|---|---|---|
| Authority | Who may authorize what, for whom, and within which scope? | Consumes bounded authority artifacts. |
| Reconstruction | What is the governing state now? | Reconstructs current decision-relevant state. |
| Eligibility | May this proposed execution proceed now? | Produces a terminal execution decision. |
| Integrity | Did the action remain inside its authorized transition? | Supplies continuity and post-effect evidence. |
| Proof | Can the decision and transition be independently checked? | Emits attributable provenance and obligations. |
| Audit | Can the full chain be reviewed and reproduced? | Exposes records, reasons, policies, and identities. |

## 3. AOMS role

AOMS does not manufacture authority, infer legitimacy from capability, or treat evidence as permission. It reconstructs the execution state, tests canonical predicates, identifies boundary conditions, and issues a decision that is terminal for one execution identity.

## 4. Interfaces

Upstream systems provide principal identity, delegation scope, authority artifacts, policy versions, and evidence references. Downstream systems receive the terminal decision, reason codes, reconciliation record, eligibility record, execution identity, and provenance bundle.

## 5. Composition rule

No adjacent layer may silently override an AOMS denial, escalation, or reauthorization requirement. An `ALLOW` decision is necessary but remains bounded to the evaluated proposal; it is not a durable grant for later or downstream actions.

## 6. Domain portability

The same structure applies to autonomous agents, financial infrastructure, healthcare workflows, civic systems, robotics, cloud automation, emergency response, and other consequential systems because the governed object is the state transition rather than a particular industry interface.

## 7. Research program

The AOMS research series separates mathematical foundations, runtime specification, verification methodology, domain applications, benchmarks, and formal proofs. Each descendant work maps claims to executable artifacts and proof obligations.
