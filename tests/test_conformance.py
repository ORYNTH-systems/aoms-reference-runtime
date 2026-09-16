import os, sys, unittest
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"..")); sys.path.insert(0,os.path.join(ROOT,"src"))
from conformance import evaluate
from canonical.pipeline import CanonicalPipeline
from canonical.models import AuthorityArtifact, ExecutionContext, Decision

class ConformanceTests(unittest.TestCase):
    def test_profile_passes(self): self.assertTrue(evaluate()["passed"])
    def test_runtime_exception_fails_closed(self):
        class Broken:
            def reconstruct(self,*args): raise RuntimeError("fault")
        a=AuthorityArtifact("a","x","y","2026","2027",True,"i","p","d","r","e","v")
        c=ExecutionContext("x","y","2026",True,"i","p","d","r","e","v")
        p=CanonicalPipeline(); p.authority=Broken(); result=p.evaluate(a,c)
        self.assertEqual(Decision.DENY,result.decision); self.assertIn("runtime_failure:RuntimeError",result.reasons)
    def test_fault_denial_is_terminal(self):
        class Broken:
            def reconstruct(self,*args): raise ValueError("fault")
        a=AuthorityArtifact("a","x","y","2026","2027",True,"i","p","d","r","e","v")
        c=ExecutionContext("x","y","2026",True,"i","p","d","r","e","v")
        p=CanonicalPipeline(); p.authority=Broken(); self.assertTrue(p.evaluate(a,c).terminal)

if __name__=="__main__": unittest.main()
