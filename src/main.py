from case_loader import load_case
from reconciliation import reconcile
from execution import execute


case_id, description, authorized, current = load_case(
    "cases/AOMS-001.json"
)

reconciliation = reconcile(
    authorized,
    current
)

result = execute(
    authorized,
    current
)

print(f"Case: {case_id}")
print(f"Description: {description}")
print(f"Violations: {reconciliation.violations}")
print(f"Admissibility: {reconciliation.admissibility}")
print(f"Execution Result: {result}")
