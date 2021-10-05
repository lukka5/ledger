import csv
from datetime import date
from dataclasses import dataclass
from decimal import Decimal
from pathlib import PurePath
from typing import List, Optional, Union

from pydantic import BaseModel


def get_transactions_from_file(path: Union[str, PurePath]) -> List["Transaction"]:
    with open(path, encoding="UTF-8") as csvfile:
        reader = csv.reader(csvfile)
        return [Transaction.from_row(row) for row in reader]


class IrrelevantTransactionError(Exception):
    def __init__(self, balance: "Balance", transaction: "Transaction"):
        super().__init__(
            f"{balance.entity} is not involved on transaction {repr(transaction)}"
        )


class Transaction(BaseModel):
    date: date
    sender: str
    recipient: str
    amount: Decimal

    @classmethod
    def from_row(cls, row: List[str]) -> "Transaction":
        return cls(date=row[0], sender=row[1], recipient=row[2], amount=row[3])

    def involves(self, entity: str) -> bool:
        return entity in [self.sender, self.recipient]


@dataclass
class Balance:
    entity: str
    total: Decimal = Decimal(0)

    def apply_transaction(self, transaction: Transaction) -> None:
        if self.entity == transaction.sender:
            self.total -= transaction.amount
        elif self.entity == transaction.recipient:
            self.total += transaction.amount
        else:
            raise IrrelevantTransactionError(self, transaction)


class Ledger:
    transactions: List[Transaction]

    def __init__(self):
        self.transactions = []

    def load_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    def load_transactions(
        self, source: Union[str, PurePath, List[Transaction]]
    ) -> None:
        transactions = (
            get_transactions_from_file(source)
            if isinstance(source, (str, PurePath))
            else source
        )
        for transaction in transactions:
            self.load_transaction(transaction)

    def get_balance(self, entity: str, at: Optional[date] = None) -> Balance:
        balance = Balance(entity)
        for transaction in self.transactions:
            if transaction.involves(entity):
                balance.apply_transaction(transaction)
        return balance


ledger = Ledger()
ledger.load_transactions("samples/minimal.csv")
print("Balance for Mary -->", ledger.get_balance("mary").total)
print("Balance for John -->", ledger.get_balance("john").total)
print("Balance for Supermarket -->", ledger.get_balance("supermarket").total)
