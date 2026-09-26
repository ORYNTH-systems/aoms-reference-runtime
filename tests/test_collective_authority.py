import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from canonical.collective_pipeline import CollectiveAuthorityPipeline
from collective_cases import load_collective_case


class CollectiveAuthorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paths = sorted((ROOT / "cases" / "collective").glob("AOMS-COL-*.json"))

    def test_exact_case_range(self):
        self.assertEqual([f"AOMS-COL-{n:03d}.json" for n in range(1, 13)], [item.name for item in self.paths])

    def test_all_cases_match_declared_outcomes(self):
        for path in self.paths:
            case_id, request, expected = load_collective_case(path)
            result = CollectiveAuthorityPipeline().evaluate(request)
            self.assertEqual(expected["decision"], result.decision.value, case_id)
            for reason in expected.get("required_reasons", []):
                combined = result.reasons + [reason for item in result.participants for reason in item.reasons]
                self.assertIn(reason, combined, case_id)

    def test_collective_decisions_are_fresh_terminal_and_attributable(self):
        for path in self.paths:
            _, request, _ = load_collective_case(path)
            first = CollectiveAuthorityPipeline().evaluate(request)
            second = CollectiveAuthorityPipeline().evaluate(request)
            self.assertNotEqual(first.execution_id, second.execution_id)
            self.assertTrue(first.terminal)
            self.assertIn(first.execution_id, first.provenance)
            self.assertTrue(any(item.startswith("coordinator:") for item in first.provenance))

    def test_each_participant_runs_canonical_pipeline(self):
        _, request, _ = load_collective_case(self.paths[0])
        result = CollectiveAuthorityPipeline().evaluate(request)
        self.assertTrue(result.participants)
        for participant in result.participants:
            self.assertIn("decision_engine", participant.provenance)


if __name__ == "__main__":
    unittest.main()
