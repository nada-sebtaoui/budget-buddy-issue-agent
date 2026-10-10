Budget Buddy
Budget Buddy is a deliberately small Python transaction tracker. It reads transactions from CSV and prints a monthly summary of income, expenses, net cash flow, and expense totals by category.

This is a demo repository for testing an AI GitHub issue agent. It has a focused bug report supplied separately in DEMO_ISSUE.md at the ZIP's top level. Keep that file outside the GitHub repository when you upload the project, then create a GitHub issue from its contents.

Requirements
Python 3.10 or newer
pip
Docker is optional for local development, but useful if your issue agent executes tests in a container
Run locally
From the repository root:

python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Git Bash / macOS / Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m budget_buddy.cli --year 2026 --month 4
If running without installing the package, use PYTHONPATH=src (or set the equivalent environment variable in your shell):

PYTHONPATH=src python -m budget_buddy.cli --year 2026 --month 4
Run tests
python -m pip install -e ".[dev]"
python -m pytest -q
One reporting regression is intentionally present. The existing test suite includes a test that describes the expected behavior and should fail before the bug is fixed. This is useful for a bug-fixing agent: it can inspect the issue, identify the relevant implementation, propose a patch, and rerun the tests.

Run tests in Docker
Build and run the included image:

docker build -t budget-buddy-demo .
docker run --rm budget-buddy-demo
The image runs the test suite by default. It is suitable as a basic demo environment, not as a hardened security boundary for untrusted code.

Project layout
src/budget_buddy/
  models.py   # Transaction model and input validation
  storage.py  # CSV loading
  reports.py  # Monthly aggregation logic
  cli.py      # Command-line report
 tests/
  test_models.py
  test_storage.py
  test_reports.py
 data/
  sample_transactions.csv
Important demo note
The bug is intentionally seeded in reports.py. Do not fix it before running the agent if you want to record the agent discovering and resolving it. After the demo, keep the fix if you want to reuse this as a normal project.
