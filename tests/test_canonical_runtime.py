import glob
import os
import sys
import unittest
from dataclasses import replace

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from canonical.adapter import adapt_v1, evaluate_v1, legacy_execution_result
from canonical.models import Decision
from canonical.pipeline import CanonicalPipeline
from case_loader import load_case
from execution import execute
from models import CurrentState


class CanonicalRuntimeTests(unittest.TestCase):
    def load_synthetic_allow(self):
        """Build a positive control from the v1 schema; the v1 corpus is adversarial-only."""
        path = sorted(glob.glob(os.path.join(ROOT, "cases", "AOMS-*.json")))[0]
        _, _, authorized, _ = load_case(path)
        authorized = replace(authorized, authority_valid=True)
        current = CurrentState(
            actor_id=authorized.actor_id,
            current_action=authorized.authorized_action,
            execution_attempted_at=authorized.authorized_at,
            authority_valid=True,
            identity_state=authorized.identity_state,
            policy_version=authorized.policy_version,
            dependency_state=authorized.dependency_state,
            resource_state=authorized.resource_state,
            environment_state=authorized.environment_state,
            evidence_state=authorized.evidence_state,
        )
        self.assertEqual("APPROVED", execute(authorized, current))
        return authorized, current

    def test_all_v1_cases_preserve_binary_outcome(self):
        paths = sorted(glob.glob(os.path.join(ROOT, "cases", "AOMS-*.json")))
        self.assertEqual(100, len(paths))
        approved = 0
        declined = 0
        for path in paths:
            _, _, authorized, current = load_case(path)
            legacy = execute(authorized, current)
            canonical = legacy_execution_result(evaluate_v1(authorized, current))
            self.assertEqual(legacy, canonical, path)
            approved += legacy == "APPROVED"
            declined += legacy == "DECLINED"
        self.assertEqual(0, approved)
        self.assertEqual(100, declined)

    def test_synthetic_positive_control_allows_terminally(self):
        authorized, current = self.load_synthetic_allow()
        result = evaluate_v1(authorized, current)
        self.assertEqual(Decision.ALLOW, result.decision)
        self.assertTrue(result.terminal)

    def test_each_evaluation_has_fresh_identity(self):
        authorized, current = self.load_synthetic_allow()
        first = evaluate_v1(authorized, current)
        second = evaluate_v1(authorized, current)
        self.assertNotEqual(first.execution_id, second.execution_id)

    def assert_boundary_escalates(self, boundary):
        authorized, current = self.load_synthetic_allow()
        artifact, context = adapt_v1(authorized, current)
        result = CanonicalPipeline().evaluate(artifact, replace(context, boundary_signals=[boundary]))
        self.assertEqual(Decision.ESCALATE, result.decision)
        self.assertTrue(result.governance.boundary.crossed)

    def test_personal_boundary_escalates(self):
        self.assert_boundary_escalates("PERSONAL")

    def test_psychological_boundary_escalates(self):
        self.assert_boundary_escalates("PSYCHOLOGICAL")

    def test_therapeutic_boundary_escalates(self):
        self.assert_boundary_escalates("THERAPEUTIC")

    def test_unknown_boundary_escalates(self):
        self.assert_boundary_escalates("UNREGISTERED-BOUNDARY")

    def test_expired_authority_requires_reauthorization(self):
        authorized, current = self.load_synthetic_allow()
        artifact, context = adapt_v1(authorized, current)
        result = CanonicalPipeline().evaluate(artifact, replace(context, attempted_at="9999-12-31T23:59:59Z"))
        self.assertEqual(Decision.REAUTHORIZE, result.decision)

    def test_dependency_failure_denies(self):
        authorized, current = self.load_synthetic_allow()
        artifact, context = adapt_v1(authorized, current)
        result = CanonicalPipeline().evaluate(artifact, replace(context, dependency_state="FAILED"))
        self.assertEqual(Decision.DENY, result.decision)

    def test_provenance_is_complete(self):
        authorized, current = self.load_synthetic_allow()
        result = evaluate_v1(authorized, current)
        self.assertIn("authority_artifact", result.provenance)
        self.assertIn("decision_engine", result.provenance)
        self.assertIn(result.execution_id, result.provenance)


if __name__ == "__main__":
    unittest.main()
