from typing import List

from .models import (
    AuthorityArtifact,
    AuthorityState,
    BoundaryAssessment,
    BoundaryClass,
    ContinuityVector,
    Decision,
    EligibilityRecord,
    ExecutionContext,
    ExecutionDecision,
    GovernanceState,
    ReconciliationRecord,
)


class AuthorityStateEngine:
    def reconstruct(self, artifact: AuthorityArtifact, context: ExecutionContext) -> AuthorityState:
        reasons: List[str] = []
        if not artifact.authorization_id or not artifact.issuer_id:
            reasons.append("authority_artifact_incomplete")
        if not artifact.authority_valid or not context.authority_valid:
            reasons.append("authority_invalid")
        if context.attempted_at < artifact.authorized_at:
            reasons.append("execution_too_early")
        if context.attempted_at > artifact.expires_at:
            reasons.append("authorization_expired")
        return AuthorityState(
            reconstructed=len(reasons) == 0,
            effective=len(reasons) == 0,
            reasons=reasons,
            provenance=["authority_artifact", artifact.authorization_id, artifact.issuer_id],
        )


class ContinuityVerificationEngine:
    def verify(self, artifact: AuthorityArtifact, context: ExecutionContext) -> ContinuityVector:
        dimensions = {
            "actor": context.actor_id == artifact.actor_id,
            "action": context.requested_action == artifact.authorized_action,
            "identity": context.identity_state == artifact.identity_state,
            "policy": context.policy_version == artifact.policy_version,
            "dependency": context.dependency_state == artifact.dependency_state,
            "resource": context.resource_state == artifact.resource_state,
            "environment": context.environment_state == artifact.environment_state,
            "evidence": context.evidence_state == artifact.evidence_state,
        }
        names = {
            "actor": "actor_mismatch",
            "action": "action_drift_detected",
            "identity": "identity_continuity_failed",
            "policy": "policy_changed",
            "dependency": "dependency_state_changed",
            "resource": "resource_unavailable",
            "environment": "environment_invalid",
            "evidence": "evidence_insufficient",
        }
        violations = [names[name] for name, matched in dimensions.items() if not matched]
        return ContinuityVector(dimensions, violations, all(dimensions.values()), ["authority_state", "execution_context"])


class BoundaryEvaluationEngine:
    _classes = {item.value for item in BoundaryClass}
    _escalation = {
        BoundaryClass.PERSONAL.value,
        BoundaryClass.PSYCHOLOGICAL.value,
        BoundaryClass.THERAPEUTIC.value,
        BoundaryClass.SAFETY.value,
    }

    def evaluate(self, context: ExecutionContext) -> BoundaryAssessment:
        normalized = sorted({signal.strip().upper() for signal in context.boundary_signals if signal.strip()})
        known = [signal for signal in normalized if signal in self._classes]
        unknown = [signal for signal in normalized if signal not in self._classes]
        classes = known + (["UNKNOWN"] if unknown else [])
        return BoundaryAssessment(
            crossed=bool(normalized),
            classes=classes,
            signals=normalized,
            requires_escalation=bool(set(known) & self._escalation) or bool(unknown),
            provenance=["execution_context.boundary_signals"],
        )


class ReconciliationEngine:
    def reconcile(self, authority: AuthorityState, continuity: ContinuityVector, boundary: BoundaryAssessment) -> ReconciliationRecord:
        violations = list(dict.fromkeys(authority.reasons + continuity.violations))
        if boundary.crossed:
            violations.extend("boundary_crossed:" + item.lower() for item in boundary.classes)
        required = bool(violations)
        return ReconciliationRecord(
            required=required,
            resolved=not required,
            violations=violations,
            disposition="UNCHANGED" if not required else "UNRESOLVED",
            provenance=authority.provenance + continuity.provenance + boundary.provenance,
        )


class EligibilityEngine:
    def determine(self, authority: AuthorityState, reconciliation: ReconciliationRecord) -> EligibilityRecord:
        complete = bool(authority.provenance and reconciliation.provenance)
        eligible = authority.effective and reconciliation.resolved and complete
        reasons = [] if eligible else list(reconciliation.violations or authority.reasons or ["eligibility_proof_incomplete"])
        return EligibilityRecord(eligible, reasons, complete, reconciliation.provenance + ["eligibility_engine"])


class DecisionEngine:
    _reauthorize = {
        "authority_artifact_incomplete", "authority_invalid", "authorization_expired",
        "execution_too_early", "actor_mismatch", "action_drift_detected",
        "identity_continuity_failed", "policy_changed",
    }

    def decide(self, execution_id: str, state: GovernanceState) -> ExecutionDecision:
        reasons = list(state.eligibility.reasons)
        if state.eligibility.eligible:
            decision = Decision.ALLOW
        elif state.boundary.requires_escalation:
            decision = Decision.ESCALATE
        elif any(reason in self._reauthorize for reason in reasons):
            decision = Decision.REAUTHORIZE
        else:
            decision = Decision.DENY
        return ExecutionDecision(
            execution_id=execution_id,
            decision=decision,
            terminal=True,
            reasons=reasons,
            governance=state,
            provenance=state.eligibility.provenance + ["decision_engine", execution_id],
        )
