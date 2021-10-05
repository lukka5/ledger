from datetime import date
from decimal import Decimal

import pytest

from ledger.transaction import (
    IrrelevantTransactionError,
    Transaction,
    get_transactions_from_file,
)


def test_get_transactions_from_file(mocker, tmp_csv_factory):
    from_row_mock = mocker.patch.object(
        Transaction, "from_row", side_effect=["T-1", "T-2", "T-3"]
    )
    csvfile = tmp_csv_factory(
        "2015-01-16,john,mary,125.00",
        "2015-01-17,john,supermarket,20.00",
        "2015-01-17,mary,insurance,100.00",
    )

    transactions = get_transactions_from_file(csvfile)

    assert from_row_mock.call_args_list == [
        mocker.call(["2015-01-16", "john", "mary", "125.00"]),
        mocker.call(["2015-01-17", "john", "supermarket", "20.00"]),
        mocker.call(["2015-01-17", "mary", "insurance", "100.00"]),
    ]
    assert transactions == ["T-1", "T-2", "T-3"]


class TestIrrelevantTransactionError:
    def test_init(self, mocker):
        transaction = mocker.MagicMock()

        error = IrrelevantTransactionError("mike", transaction)

        expected = f"mike is not involved on transaction {repr(transaction)}"
        assert error.args[0] == expected


class TestTransaction:
    def test_init(self):
        balance = Transaction(
            date="2020-01-02", sender="mike", recipient="susan", amount="1.234"
        )
        assert balance.date == date(2020, 1, 2)
        assert balance.sender == "mike"
        assert balance.recipient == "susan"
        assert balance.amount == Decimal("1.234")

    def test_from_row(self):
        balance = Transaction.from_row(["2020-01-02", "mike", "susan", "1.234"])
        assert balance.date == date(2020, 1, 2)
        assert balance.sender == "mike"
        assert balance.recipient == "susan"
        assert balance.amount == Decimal("1.234")

    @pytest.mark.parametrize(
        "entity, expected", [("paul", False), ("mike", True), ("susan", True)]
    )
    def test_involves(self, entity, expected):
        balance = Transaction(
            date="2020-01-02", sender="mike", recipient="susan", amount="1.234"
        )

        assert balance.involves(entity) is expected
