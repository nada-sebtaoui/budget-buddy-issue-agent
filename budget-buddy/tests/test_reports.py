from datetime import date
from decimal import Decimal

import pytest

from budget_buddy.models import Transaction, TransactionType
from budget_buddy.reports import monthly_summary


def tx(transaction_id, when, amount, kind, category="general", description="test"):
    return Transaction(
        transaction_id=transaction_id,
        date=date.fromisoformat(when),
        description=description,
        category=category,
        amount=Decimal(amount),
        type=TransactionType(kind),
    )


@pytest.fixture
def transactions():
    return [
        tx("T-1", "2026-04-03", "3000.00", "income", "salary"),
        tx("T-2", "2026-04-05", "900.00", "expense", "housing"),
        tx("T-3", "2026-04-10", "120.00", "expense", "food"),
        tx("T-4", "2026-03-18", "76.40", "expense", "utilities"),
        tx("T-5", "2025-04-15", "850.00", "expense", "housing"),
        tx("T-6", "2025-04-20", "250.00", "income", "freelance"),
        tx("T-7", "2026-05-02", "44.50", "expense", "travel"),
        tx("T-8", "2026-04-26", "180.00", "income", "freelance"),
    ]


def test_monthly_summary_totals_for_requested_year_and_month(transactions):
    summary = monthly_summary(transactions, 2026, 4)

    assert summary.income == Decimal("3180.00")
    assert summary.expenses == Decimal("1020.00")
    assert summary.net == Decimal("2160.00")
    assert summary.transaction_count == 4
    assert summary.expense_by_category == {
        "food": Decimal("120.00"),
        "housing": Decimal("900.00"),
    }


def test_month_with_no_transactions_returns_zero_totals():
    summary = monthly_summary([], 2026, 2)

    assert summary.income == Decimal("0.00")
    assert summary.expenses == Decimal("0.00")
    assert summary.net == Decimal("0.00")
    assert summary.transaction_count == 0
    assert summary.expense_by_category == {}


@pytest.mark.parametrize("month", [0, 13, -1])
def test_invalid_month_is_rejected(month):
    with pytest.raises(ValueError, match="month must be between 1 and 12"):
        monthly_summary([], 2026, month)
