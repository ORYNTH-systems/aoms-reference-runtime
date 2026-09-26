from uuid import uuid4

from .collective_engines import (
    AccountabilityAttributionEngine,
    CollectiveAdmissibilityEngine,
    DelegationChainEngine,
    QuorumEvaluationEngine,
    ScopeCompositionEngine,
    SeparationOfDutiesEngine,
    participant_evaluation,
)
from .collective_models import CollectiveDecision, CollectiveExecutionRequest
from .models import Decision
from .pipeline import CanonicalPipeline


class CollectiveAuthorityPipeline:
    """Composes independently reconstructed participant decisions without manufacturing authority."""

    def __init__(self) -> None:
        self.participant_pipeline = CanonicalPipeline()
        self.delegation = DelegationChainEngine()
        self.scope = ScopeCompositionEngine()
        self.quorum = QuorumEvaluationEngine()
        self.separation = SeparationOfDutiesEngine()
        self.admissibility = CollectiveAdmissibilityEngine()
        self.accountability = AccountabilityAttributionEngine()

    def evaluate(self, request: CollectiveExecutionRequest) -> CollectiveDecision:
        execution_id = "AOMS-COL-EXE-" + uuid4().hex
        try:
            identities = [item.participant_id for item in request.participants]
            collective_reasons = []
            if len(identities) != len(set(identities)):
                collective_reasons.append("duplicate_participant_identity")

            results = []
            for participant in request.participants:
                decision = self.participant_pipeline.evaluate(participant.artifact, participant.context)
                delegation_valid, delegation_reasons = self.delegation.evaluate(participant, request.requested_action)
                scope_valid, scope_reasons = self.scope.evaluate(participant, request.requested_action)
                results.append(participant_evaluation(
                    participant,
                    decision,
                    delegation_valid,
                    delegation_reasons,
                    scope_valid,
                    scope_reasons,
                ))

            quorum_valid, quorum_reasons = self.quorum.evaluate(request, results)
            separation_valid, separation_reasons = self.separation.evaluate(request)
            collective_reasons.extend(quorum_reasons)
            collective_reasons.extend(separation_reasons)
            decision, reasons = self.admissibility.determine(
                request,
                results,
                quorum_valid,
                separation_valid,
                collective_reasons,
            )
            provenance = self.accountability.attribute(request, results)
            provenance.extend(["collective_admissibility_engine", execution_id])
            return CollectiveDecision(execution_id, request.request_id, decision, True, reasons, results, provenance)
        except Exception as error:
            reason = "collective_runtime_failure:" + error.__class__.__name__
            return CollectiveDecision(
                execution_id,
                request.request_id,
                Decision.DENY,
                True,
                [reason],
                [],
                ["fail_closed", "collective_pipeline", execution_id],
            )
