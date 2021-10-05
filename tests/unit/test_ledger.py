from datetime import date

from ledger.ledger import Ledger


class TestLedger:
    def test_init(self):
        ledger = Ledger()
        assert ledger.transactions == []

    def test_load_from_file(self, mocker):
        mock_transactions = [mocker.Mock(), mocker.Mock()]
        get_transactions_from_file_mock = mocker.patch(
            "ledger.ledger.get_transactions_from_file", return_value=mock_transactions
        )
        ledger = Ledger()

        ledger.load_from_file("foo.csv")

        get_transactions_from_file_mock.assert_called_once_with("foo.csv")
        assert ledger.transactions == mock_transactions

    def test_get_balance_with_at_date(self, mocker):
        balance_mock = mocker.patch("ledger.ledger.Balance")
        transaction1 = mocker.Mock(involves=lambda entity: False, date=date(1, 1, 1))
        transaction2 = mocker.Mock(involves=lambda entity: True, date=date(1, 1, 1))
        transaction3 = mocker.Mock(involves=lambda entity: True, date=date(2, 2, 2))
        transaction4 = mocker.Mock(involves=lambda entity: True, date=date(3, 3, 3))
        ledger = Ledger()
        ledger.transactions = [transaction1, transaction2, transaction3, transaction4]

        result = ledger.get_balance("mike", date(2, 2, 2))

        balance_mock.assert_called_once_with(entity="mike")
        assert balance_mock.return_value.apply_transaction.call_args_list == [
            mocker.call(transaction2),
            mocker.call(transaction3),
        ]
        assert result is balance_mock.return_value

    def test_get_balance_without_at_date(self, mocker):
        balance_mock = mocker.patch("ledger.ledger.Balance")
        transaction1 = mocker.Mock(involves=lambda entity: False, date=date(1, 1, 1))
        transaction2 = mocker.Mock(involves=lambda entity: True, date=date(1, 1, 1))
        ledger = Ledger()
        ledger.transactions = [transaction1, transaction2]

        result = ledger.get_balance("mike")

        balance_mock.assert_called_once_with(entity="mike")
        balance_mock.return_value.apply_transaction.assert_called_once_with(
            transaction2
        )
        assert result is balance_mock.return_value

    def test_get_balance_without_transactions(self, mocker):
        balance_mock = mocker.patch("ledger.ledger.Balance")
        ledger = Ledger()
        ledger.transactions = []

        result = ledger.get_balance("mike")

        balance_mock.assert_called_once_with(entity="mike")
        balance_mock.return_value.apply_transaction.assert_not_called()
        assert result is balance_mock.return_value
