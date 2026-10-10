"""Domain models for Budget Buddy."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from enum import Enum


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


@dataclass(frozen=True, slots=True)
class Transaction:
    """A single income or expense transaction.

    Amounts are always stored as positive Decimal values. The transaction type
    determines whether an amount increases or decreases the account balance.
    """

    transaction_id: str
    date: date
    description: str
    category: str
    amount: Decimal
    type: TransactionType

    def __post_init__(self) -> None:
        if not self.transaction_id.strip():
            raise ValueError("transaction_id must not be empty")
        if not self.description.strip():
            raise ValueError("description must not be empty")
        if not self.category.strip():
            raise ValueError("category must not be empty")

        try:
            normalized_amount = Decimal(str(self.amount))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("amount must be a valid decimal number") from exc

        if not normalized_amount.is_finite() or normalized_amount <= 0:
            raise ValueError("amount must be a positive finite number")
        object.__setattr__(self, "amount", normalized_amount.quantize(Decimal("0.01")))

        if not isinstance(self.date, date):
            raise ValueError("date must be a datetime.date instance")
        if not isinstance(self.type, TransactionType):
            try:
                object.__setattr__(self, "type", TransactionType(self.type))
            except ValueError as exc:
                raise ValueError("type must be 'income' or 'expense'") from exc
