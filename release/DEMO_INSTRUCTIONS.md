AOMS v1 Demonstration Instructions
Requirements
Python 3.10 or later
No external Python dependencies
Run One Case
python .\src\main.py --case .\cases\AOMS-001.json
Run the Complete Corpus
python .\src\main.py --all
Expected Corpus Result
Total cases: 100
Approved executions: 0
Declined executions: 100
Admissible cases: 0
Inadmissible cases: 100
Evidence Output

Execution artifacts are written under:

reports/json/
Interpretation

The v1 corpus contains deliberately inadmissible test cases. It demonstrates detection of execution-condition drift. It is not yet a balanced performance benchmark and must not be interpreted as evidence of false-positive or overblocking performance.

Phase II Notice

Phase II will add positive controls, graduated outcomes, canonical engine separation, provenance verification, and failure-injection testing.
