from uuid import uuid4

from .engines import (
    AuthorityStateEngine,
    BoundaryEvaluationEngine,
    ContinuityVerificationEngine,
    DecisionEngine,
    EligibilityEngine,
    ReconciliationEngine,
)
from .models import AuthorityArtifact, Decision, ExecutionContext, ExecutionDecision, GovernanceState


class CanonicalPipeline:
    """Runs every request from fresh source state; terminal decisions are never reused."""

    def __init__(self) -> None:
        self.authority = AuthorityStateEngine()
        self.continuity = ContinuityVerificationEngine()
        self.boundary = BoundaryEvaluationEngine()
        self.reconciliation = ReconciliationEngine()
        self.eligibility = EligibilityEngine()
        self.decision = DecisionEngine()

    def evaluate(self, artifact: AuthorityArtifact, context: ExecutionContext) -> ExecutionDecision:
        execution_id = "AOMS-EXE-" + uuid4().hex
        try:
            authority = self.authority.reconstruct(artifact, context)
            continuity = self.continuity.verify(artifact, context)
            boundary = self.boundary.evaluate(context)
            reconciliation = self.reconciliation.reconcile(authority, continuity, boundary)
            eligibility = self.eligibility.determine(authority, reconciliation)
            state = GovernanceState(authority, continuity, boundary, reconciliation, eligibility)
            return self.decision.decide(execution_id, state)
        except Exception as error:
            # The runtime fails closed and emits a terminal, attributable denial.
            from .models import AuthorityState, BoundaryAssessment, ContinuityVector, EligibilityRecord, ReconciliationRecord
            reason = "runtime_failure:" + error.__class__.__name__
            state = GovernanceState(
                AuthorityState(False, False, [reason], ["fail_closed"]),
                ContinuityVector({}, [reason], False, ["fail_closed"]),
                BoundaryAssessment(False, [], [], False, ["fail_closed"]),
                ReconciliationRecord(True, False, [reason], "UNRESOLVED", ["fail_closed"]),
                EligibilityRecord(False, [reason], False, ["fail_closed"]),
            )
            return ExecutionDecision(execution_id, Decision.DENY, True, [reason], state, ["fail_closed", execution_id])
