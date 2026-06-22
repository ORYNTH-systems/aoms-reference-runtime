from case_loader import load_case
from execution import execute


case_id, description, authorized, current = load_case(
    "cases/AOMS-001.json"
)

result = execute(
    authorized,
    current
)

print(f"Case: {case_id}")
print(f"Description: {description}")
print(f"Execution Result: {result}")
