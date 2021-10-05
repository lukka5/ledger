from decimal import Decimal

from pydantic import BaseModel

from ledger.transaction import IrrelevantTransactionError, Transaction


class Balance(BaseModel):
    entity: str
    total: Decimal = Decimal(0)

    def apply_transaction(self, transaction: Transaction) -> None:
        if not transaction.involves(self.entity):
            raise IrrelevantTransactionError(self.entity, transaction)
        if self.entity == transaction.sender:
            self.total -= transaction.amount
        if self.entity == transaction.recipient:
            self.total += transaction.amount
