from decimal import Decimal

import pytest

from budget_buddy.storage import load_transactions


def test_load_transactions_reads_csv(tmp_path):
    path = tmp_path / "transactions.csv"
    path.write_text(
        "id,date,description,category,amount,type\n"
        "T-1,2026-04-03,Salary,salary,1200.00,income\n",
        encoding="utf-8",
    )

    transactions = load_transactions(path)

    assert len(transactions) == 1
    assert transactions[0].amount == Decimal("1200.00")
    assert transactions[0].type.value == "income"


def test_missing_columns_produce_a_clear_error(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("id,date,amount\nT-1,2026-04-03,12.00\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing required columns"):
        load_transactions(path)
