import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TOOLS = os.path.join(ROOT, "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

from validate_claim_proof_closure import validate


class ClaimProofClosureTests(unittest.TestCase):
    def test_all_twenty_claims_are_closed(self):
        result = validate(write_outputs=False)
        self.assertTrue(result["passed"], result["errors"])
        self.assertEqual(20, result["claim_count"])
        self.assertEqual(3, result["closure_count"])
        self.assertEqual({"AOMS-002": 8, "AOMS-003": 6, "AOMS-004": 6}, result["publication_counts"])


if __name__ == "__main__":
    unittest.main()
