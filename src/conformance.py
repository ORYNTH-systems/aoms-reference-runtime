import json, os, sys
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if os.path.join(ROOT, "src") not in sys.path:
    sys.path.insert(0, os.path.join(ROOT, "src"))
from canonical_cases import run_all, load_canonical_case
from canonical.pipeline import CanonicalPipeline

def evaluate():
    report = run_all()
    paths = [os.path.join(ROOT, "cases", "canonical", "AOMS-%03d.json" % n) for n in range(101, 351)]
    fresh = True; terminal = True; provenance = True; proof = True
    for path in paths:
        _, artifact, context = load_canonical_case(path)
        a = CanonicalPipeline().evaluate(artifact, context)
        b = CanonicalPipeline().evaluate(artifact, context)
        fresh &= a.execution_id != b.execution_id
        terminal &= a.terminal
        provenance &= "decision_engine" in a.provenance and a.execution_id in a.provenance
        proof &= a.governance.eligibility.proof_complete
    checks = {
        "case_count_250": report["case_count"] == 250,
        "all_cases_pass": report["failed"] == 0,
        "decision_distribution": report["decision_counts"] == {"ALLOW":25,"DENY":75,"ESCALATE":75,"REAUTHORIZE":75},
        "fresh_execution_identity": fresh,
        "terminal_decisions": terminal,
        "complete_provenance": provenance,
        "eligibility_proof_complete": proof,
    }
    return {"profile":"AOMS-CONF-001","case_count":250,"checks":checks,"passed":all(checks.values())}

if __name__ == "__main__":
    result=evaluate()
    out=os.path.join(ROOT,"reports","conformance","BATCH_04_CONFORMANCE.json")
    os.makedirs(os.path.dirname(out),exist_ok=True)
    with open(out,"w",encoding="utf-8",newline="\n") as f:
        json.dump(result,f,indent=2,sort_keys=True); f.write("\n")
    print(json.dumps(result,indent=2,sort_keys=True))
    raise SystemExit(0 if result["passed"] else 1)
