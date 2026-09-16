import glob
import json
import os
import sys
import unittest
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from canonical_cases import load_canonical_case, run_all, run_case
from canonical.pipeline import CanonicalPipeline

class CanonicalCaseSuiteTests(unittest.TestCase):
    @classmethod
    def paths(cls):
        return sorted(glob.glob(os.path.join(ROOT, "cases", "canonical", "AOMS-*.json")))

    def test_exact_case_identity_range(self):
        names = [os.path.splitext(os.path.basename(path))[0] for path in self.paths()]
        self.assertEqual(["AOMS-%03d" % number for number in range(101, 351)], names)

    def test_exact_decision_distribution(self):
        distribution = Counter()
        for path in self.paths():
            with open(path, "r", encoding="utf-8") as handle:
                distribution[json.load(handle)["expected"]["decision"]] += 1
        self.assertEqual(Counter({"ALLOW": 25, "DENY": 75, "ESCALATE": 75, "REAUTHORIZE": 75}), distribution)

    def test_all_250_proofs_pass(self):
        report = run_all()
        self.assertEqual(250, report["case_count"])
        self.assertEqual(250, report["passed"])
        self.assertEqual(0, report["failed"])

    def test_every_decision_is_terminal_and_provenanced(self):
        for path in self.paths():
            _, artifact, context = load_canonical_case(path)
            result = CanonicalPipeline().evaluate(artifact, context)
            self.assertTrue(result.terminal, path)
            self.assertIn("decision_engine", result.provenance, path)
            self.assertIn(result.execution_id, result.provenance, path)

    def test_decisions_are_fresh_not_cached(self):
        path = self.paths()[0]
        _, artifact, context = load_canonical_case(path)
        first = CanonicalPipeline().evaluate(artifact, context)
        second = CanonicalPipeline().evaluate(artifact, context)
        self.assertNotEqual(first.execution_id, second.execution_id)

    def test_agent_readable_boundary_families_are_present(self):
        variants = set()
        for path in self.paths():
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            variants.add(data["variant"])
        required = {"personal-boundary", "psychological-boundary", "therapeutic-boundary", "safety-boundary", "unknown-boundary"}
        self.assertTrue(required.issubset(variants))

if __name__ == "__main__":
    unittest.main()
