from datetime import date
from decimal import Decimal

import pytest

from budget_buddy.models import Transaction, TransactionType


def make_transaction(**overrides):
    values = {
        "transaction_id": "T-1",
        "date": date(2026, 4, 3),
        "description": "Coffee",
        "category": "food",
        "amount": Decimal("3.456"),
        "type": TransactionType.EXPENSE,
    }
    values.update(overrides)
    return Transaction(**values)


def test_amount_is_normalized_to_two_decimal_places():
    assert make_transaction().amount == Decimal("3.46")


@pytest.mark.parametrize("bad_amount", [0, -1, "NaN", "Infinity"])
def test_amount_must_be_positive_and_finite(bad_amount):
    with pytest.raises(ValueError, match="positive finite"):
        make_transaction(amount=bad_amount)


def test_string_transaction_type_is_normalized():
    transaction = make_transaction(type="income")
    assert transaction.type is TransactionType.INCOME
