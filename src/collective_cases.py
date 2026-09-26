import json
from pathlib import Path

from canonical.collective_models import CollectiveExecutionRequest, CollectiveParticipant, DelegationLink
from canonical.models import AuthorityArtifact, ExecutionContext


def load_collective_case(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    participants = []
    for item in data["request"]["participants"]:
        participant = dict(item)
        participant["artifact"] = AuthorityArtifact(**participant["artifact"])
        participant["context"] = ExecutionContext(**participant["context"])
        participant["delegation_chain"] = [DelegationLink(**link) for link in participant.get("delegation_chain", [])]
        participants.append(CollectiveParticipant(**participant))
    request = dict(data["request"])
    request["participants"] = participants
    return data["case_id"], CollectiveExecutionRequest(**request), data["expected"]
