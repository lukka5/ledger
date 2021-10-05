from datetime import date
from pathlib import PurePath
from typing import List, Union

from ledger.balance import Balance
from ledger.transaction import Transaction, get_transactions_from_file


class Ledger:
    transactions: List[Transaction]

    def __init__(self):
        self.transactions = []

    def load_from_file(self, path: Union[str, PurePath]) -> None:
        self.transactions += get_transactions_from_file(path)

    def get_balance(self, entity: str, at: date = date.max) -> Balance:
        balance = Balance(entity=entity)
        for transaction in self.transactions:
            if transaction.involves(entity) and transaction.date <= at:
                balance.apply_transaction(transaction)
        return balance
