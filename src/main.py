from case_loader import load_case
from reconciliation import reconcile
from execution import execute
from evidence import write_evidence


case_id, description, authorized, current = load_case(
    "cases/AOMS-001.json"
)

reconciliation = reconcile(
    authorized,
    current
)

execution_result = execute(
    authorized,
    current
)

result = {
    "case_id": case_id,
    "description": description,
    "violations": reconciliation.violations,
    "admissibility": reconciliation.admissibility,
    "execution_result": execution_result
}

artifact = write_evidence(result)

print(f"Case: {case_id}")
print(f"Description: {description}")
print(f"Violations: {reconciliation.violations}")
print(f"Admissibility: {reconciliation.admissibility}")
print(f"Execution Result: {execution_result}")
print(f"Evidence Artifact: {artifact}")
