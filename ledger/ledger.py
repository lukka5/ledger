from datetime import date
from pathlib import PurePath
from typing import List, Optional, Union

from ledger.balance import Balance
from ledger.transaction import Transaction, get_transactions_from_file


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
        balance = Balance(entity=entity)
        for transaction in self.transactions:
            if transaction.involves(entity):
                balance.apply_transaction(transaction)
        return balance
