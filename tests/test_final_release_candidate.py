import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TOOLS = os.path.join(ROOT, "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

from validate_final_release_candidate import validate

class FinalReleaseCandidateTests(unittest.TestCase):
    def test_candidate_is_complete_but_not_released(self):
        result = validate(write_outputs=False)
        self.assertTrue(result["passed"], result["errors"])
        self.assertEqual("2.0.0-rc.1", result["version"])
        self.assertEqual(410, result["counts"]["total_cases"])
        self.assertEqual(20, result["closed_claims"])
        self.assertFalse(result["release_authorized"])
        self.assertFalse(result["tag_created"])
        self.assertFalse(result["github_release_created"])

if __name__ == "__main__":
    unittest.main()
