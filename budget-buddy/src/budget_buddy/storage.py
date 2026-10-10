"""CSV loading utilities."""

import csv
from datetime import date
from decimal import Decimal
from pathlib import Path

from .models import Transaction, TransactionType


def load_transactions(path: str | Path) -> list[Transaction]:
    """Load transactions from a UTF-8 CSV file.

    Required columns: id,date,description,category,amount,type.
    Dates use ISO format (YYYY-MM-DD); type is income or expense.
    """
    csv_path = Path(path)
    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required = {"id", "date", "description", "category", "amount", "type"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")

        transactions: list[Transaction] = []
        for line_number, row in enumerate(reader, start=2):
            try:
                transactions.append(
                    Transaction(
                        transaction_id=row["id"],
                        date=date.fromisoformat(row["date"]),
                        description=row["description"],
                        category=row["category"],
                        amount=Decimal(row["amount"]),
                        type=TransactionType(row["type"].strip().lower()),
                    )
                )
            except (ValueError, ArithmeticError) as exc:
                raise ValueError(f"Invalid transaction on CSV line {line_number}: {exc}") from exc
    return transactions
