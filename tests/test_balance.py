from decimal import Decimal

import pytest

from ledger.balance import Balance
from ledger.transaction import IrrelevantTransactionError


class TestBalance:
    def test_init(self):
        balance = Balance(entity="mike", total="1.123")
        assert balance.entity == "mike"
        assert balance.total == Decimal("1.123")

    def test_init_defaults(self):
        balance = Balance(entity="mike")
        assert balance.entity == "mike"
        assert balance.total == Decimal(0)

    def test_apply_transaction_sending(self, mocker):
        balance = Balance(entity="mike", total="1.123")
        transaction_mock = mocker.Mock(sender="mike", amount=Decimal("0.122"))

        balance.apply_transaction(transaction_mock)

        assert balance.total == Decimal("1.001")

    def test_apply_transaction_recipient(self, mocker):
        balance = Balance(entity="mike", total="1.123")
        transaction_mock = mocker.Mock(recipient="mike", amount=Decimal("10.001"))

        balance.apply_transaction(transaction_mock)

        assert balance.total == Decimal("11.124")

    def test_apply_transaction_irrelevant(self, mocker):
        balance = Balance(entity="mike", total="1.123")
        transaction_mock = mocker.Mock(sender="other", recipient="other")

        with pytest.raises(IrrelevantTransactionError):
            balance.apply_transaction(transaction_mock)
