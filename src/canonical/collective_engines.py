from typing import List, Sequence, Tuple

from .collective_models import (
    CollectiveExecutionRequest,
    CollectiveParticipant,
    ParticipantEvaluation,
)
from .models import Decision, ExecutionDecision


class DelegationChainEngine:
    def evaluate(self, participant: CollectiveParticipant, action: str) -> Tuple[bool, List[str]]:
        reasons: List[str] = []
        seen = set()
        expected_delegate = participant.artifact.actor_id
        for index, link in enumerate(participant.delegation_chain):
            edge = (link.delegator_id, link.delegate_id)
            if edge in seen or link.delegator_id == link.delegate_id:
                reasons.append("delegation_cycle")
            seen.add(edge)
            if not link.active or link.revoked:
                reasons.append("delegation_inactive")
            if action not in link.scope:
                reasons.append("delegation_scope_exceeded")
            if index == len(participant.delegation_chain) - 1 and link.delegate_id != expected_delegate:
                reasons.append("delegation_terminal_identity_mismatch")
            if index > 0:
                previous = participant.delegation_chain[index - 1]
                if link.delegator_id != previous.delegate_id:
                    reasons.append("delegation_chain_disconnected")
                if not set(link.scope).issubset(set(previous.scope)):
                    reasons.append("delegation_scope_enlarged")
        return not reasons, list(dict.fromkeys(reasons))


class ScopeCompositionEngine:
    def evaluate(self, participant: CollectiveParticipant, action: str) -> Tuple[bool, List[str]]:
        reasons = []
        if action != participant.artifact.authorized_action:
            reasons.append("collective_action_not_authorized")
        if action not in participant.delegated_scope:
            reasons.append("participant_scope_insufficient")
        return not reasons, reasons


class QuorumEvaluationEngine:
    def evaluate(self, request: CollectiveExecutionRequest, results: Sequence[ParticipantEvaluation]) -> Tuple[bool, List[str]]:
        unique_admissible = {item.participant_id for item in results if item.admissible}
        if request.quorum_required < 1:
            return False, ["invalid_quorum_rule"]
        if len(unique_admissible) < request.quorum_required:
            return False, ["quorum_not_satisfied"]
        return True, []


class SeparationOfDutiesEngine:
    def evaluate(self, request: CollectiveExecutionRequest) -> Tuple[bool, List[str]]:
        bindings = {}
        for participant in request.participants:
            bindings.setdefault(participant.role, set()).add(participant.participant_id)
        reasons = []
        for pair in request.separation_of_duties:
            if len(pair) != 2:
                reasons.append("invalid_separation_rule")
                continue
            left, right = pair
            if bindings.get(left, set()) & bindings.get(right, set()):
                reasons.append("separation_of_duties_violated")
        return not reasons, list(dict.fromkeys(reasons))


class CollectiveAdmissibilityEngine:
    def determine(
        self,
        request: CollectiveExecutionRequest,
        results: Sequence[ParticipantEvaluation],
        quorum_valid: bool,
        separation_valid: bool,
        collective_reasons: Sequence[str],
    ) -> Tuple[Decision, List[str]]:
        reasons = list(collective_reasons)
        if not request.coordinator_authorized:
            reasons.append("coordinator_unauthorized")

        present_roles = {item.role for item in request.participants}
        missing_roles = sorted(set(request.required_roles) - present_roles)
        reasons.extend("required_role_missing:" + role for role in missing_roles)

        required = [item for item in results if item.required or item.role in request.required_roles]
        unresolved = [item for item in required if not item.admissible]
        for item in unresolved:
            reasons.append("required_participant_inadmissible:" + item.participant_id)

        reasons = list(dict.fromkeys(reasons))
        if not reasons and quorum_valid and separation_valid:
            return Decision.ALLOW, []

        required_decisions = {item.decision for item in unresolved}
        if Decision.ESCALATE in required_decisions:
            return Decision.ESCALATE, reasons
        if Decision.REAUTHORIZE in required_decisions or not request.coordinator_authorized:
            return Decision.REAUTHORIZE, reasons
        return Decision.DENY, reasons


class AccountabilityAttributionEngine:
    def attribute(self, request: CollectiveExecutionRequest, results: Sequence[ParticipantEvaluation]) -> List[str]:
        provenance = ["collective_request:" + request.request_id, "coordinator:" + request.coordinator_id]
        provenance.extend("participant:" + item.participant_id + ":" + item.role for item in results)
        return provenance + ["collective_accountability_engine"]


def participant_evaluation(
    participant: CollectiveParticipant,
    decision: ExecutionDecision,
    delegation_valid: bool,
    delegation_reasons: Sequence[str],
    scope_valid: bool,
    scope_reasons: Sequence[str],
) -> ParticipantEvaluation:
    reasons = list(dict.fromkeys(list(decision.reasons) + list(delegation_reasons) + list(scope_reasons)))
    admissible = decision.decision == Decision.ALLOW and delegation_valid and scope_valid
    return ParticipantEvaluation(
        participant_id=participant.participant_id,
        role=participant.role,
        required=participant.required,
        decision=decision.decision,
        admissible=admissible,
        delegation_valid=delegation_valid,
        scope_valid=scope_valid,
        reasons=reasons,
        provenance=decision.provenance + ["delegation_engine", "scope_engine"],
    )
