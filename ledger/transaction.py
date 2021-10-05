import csv
from datetime import date
from decimal import Decimal
from pathlib import PurePath
from typing import List, Union

from pydantic import BaseModel


def get_transactions_from_file(path: Union[str, PurePath]) -> List["Transaction"]:
    with open(path, encoding="UTF-8") as csvfile:
        reader = csv.reader(csvfile)
        return [Transaction.from_row(row) for row in reader]


class IrrelevantTransactionError(Exception):
    def __init__(self, entity: str, transaction: "Transaction"):
        super().__init__(f"{entity} is not involved on transaction {repr(transaction)}")


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
