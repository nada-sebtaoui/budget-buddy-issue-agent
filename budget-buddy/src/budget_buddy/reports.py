"""Reporting and aggregation logic."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

from .models import Transaction, TransactionType

ZERO = Decimal("0.00")


@dataclass(frozen=True, slots=True)
class MonthlySummary:
    year: int
    month: int
    income: Decimal
    expenses: Decimal
    net: Decimal
    transaction_count: int
    expense_by_category: dict[str, Decimal]


def monthly_summary(
    transactions: Iterable[Transaction], year: int, month: int
) -> MonthlySummary:
    """Aggregate income and expenses for the requested calendar month."""
    if not 1 <= month <= 12:
        raise ValueError("month must be between 1 and 12")

    # BUG (intentionally seeded for the demo): this selects a calendar month
    # but forgets to check the requested year as well.
    selected = [transaction for transaction in transactions if transaction.date.month == month]

    income = sum(
        (transaction.amount for transaction in selected if transaction.type is TransactionType.INCOME),
        ZERO,
    )
    expenses = sum(
        (transaction.amount for transaction in selected if transaction.type is TransactionType.EXPENSE),
        ZERO,
    )

    category_totals: dict[str, Decimal] = {}
    for transaction in selected:
        if transaction.type is TransactionType.EXPENSE:
            category_totals[transaction.category] = (
                category_totals.get(transaction.category, ZERO) + transaction.amount
            )

    return MonthlySummary(
        year=year,
        month=month,
        income=income.quantize(Decimal("0.01")),
        expenses=expenses.quantize(Decimal("0.01")),
        net=(income - expenses).quantize(Decimal("0.01")),
        transaction_count=len(selected),
        expense_by_category={key: value.quantize(Decimal("0.01")) for key, value in sorted(category_totals.items())},
    )
