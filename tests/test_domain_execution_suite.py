import glob
import os
import sys
import unittest
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from domain_execution import load_case, run_all
from canonical.pipeline import CanonicalPipeline


class DomainExecutionSuiteTests(unittest.TestCase):
    @classmethod
    def paths(cls):
        return sorted(glob.glob(os.path.join(ROOT, "cases", "domains", "AOMS-B06-*.json")))

    def test_exact_fixture_range(self):
        names = [os.path.splitext(os.path.basename(path))[0] for path in self.paths()]
        self.assertEqual(["AOMS-B06-%03d" % number for number in range(1, 61)], names)

    def test_all_domain_fixtures_execute(self):
        report = run_all(write_reports=False)
        self.assertEqual(60, report["case_count"])
        self.assertEqual(60, report["passed"])
        self.assertEqual(0, report["failed"])
        self.assertEqual("EXECUTION-VERIFIED", report["status"])

    def test_exact_domain_and_decision_distribution(self):
        report = run_all(write_reports=False)
        self.assertEqual(Counter({
            "AI_AGENTS": 10, "CIVIC_SYSTEMS": 10, "EMERGENCY_RESPONSE": 10,
            "FINANCE": 10, "HEALTHCARE": 10, "ROBOTICS": 10,
        }), Counter(report["domain_counts"]))
        self.assertEqual(Counter({"ALLOW": 15, "DENY": 15, "ESCALATE": 15, "REAUTHORIZE": 15}), Counter(report["decision_counts"]))

    def test_replay_creates_fresh_execution_identity(self):
        _, artifact, context = load_case(self.paths()[0])
        first = CanonicalPipeline().evaluate(artifact, context)
        second = CanonicalPipeline().evaluate(artifact, context)
        self.assertNotEqual(first.execution_id, second.execution_id)


if __name__ == "__main__":
    unittest.main()
