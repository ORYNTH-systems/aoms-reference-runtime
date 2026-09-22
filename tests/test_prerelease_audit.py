import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TOOLS = os.path.join(ROOT, "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

from validate_prerelease_audit import validate

class PrereleaseAuditTests(unittest.TestCase):
    def test_phase_ii_prerelease_surface_is_complete(self):
        result = validate(write_outputs=False)
        self.assertTrue(result["passed"], result["errors"])
        self.assertEqual(410, result["counts"]["total_cases"])
        self.assertEqual(20, result["closed_claims"])
        self.assertFalse(result["release_action_performed"])

if __name__ == "__main__":
    unittest.main()
