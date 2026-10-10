"""Command-line interface for Budget Buddy."""

import argparse
from pathlib import Path

from .reports import monthly_summary
from .storage import load_transactions


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize income and expenses for a month.")
    parser.add_argument("--year", type=int, required=True, help="Report year, for example 2026")
    parser.add_argument("--month", type=int, required=True, help="Report month (1-12)")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("data/sample_transactions.csv"),
        help="Path to a transaction CSV (default: data/sample_transactions.csv)",
    )
    args = parser.parse_args()

    try:
        transactions = load_transactions(args.csv)
        report = monthly_summary(transactions, args.year, args.month)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    print(f"Budget Buddy — {report.year:04d}-{report.month:02d}")
    print("-" * 34)
    print(f"Transactions: {report.transaction_count}")
    print(f"Income:       {report.income:.2f}")
    print(f"Expenses:     {report.expenses:.2f}")
    print(f"Net:          {report.net:.2f}")
    print("Expense categories:")
    if report.expense_by_category:
        for category, total in report.expense_by_category.items():
            print(f"  {category:<16} {total:.2f}")
    else:
        print("  (none)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
