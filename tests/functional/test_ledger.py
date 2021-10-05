from datetime import date
from decimal import Decimal

from ledger import Ledger, Transaction


class TestLedger:
    def test_load_from_file(self, tmp_csv_factory):
        csvfile = tmp_csv_factory(
            "2015-01-16,john,mary,125.00",
            "2015-01-17,john,supermarket,20.00",
            "2015-01-17,mary,insurance,100.00",
        )
        ledger = Ledger()
        ledger.load_from_file(csvfile)

        assert ledger.transactions == [
            Transaction(
                date=date(2015, 1, 16),
                sender="john",
                recipient="mary",
                amount=Decimal("125.00"),
            ),
            Transaction(
                date=date(2015, 1, 17),
                sender="john",
                recipient="supermarket",
                amount=Decimal("20.00"),
            ),
            Transaction(
                date=date(2015, 1, 17),
                sender="mary",
                recipient="insurance",
                amount=Decimal("100.00"),
            ),
        ]

    def test_load_from_file_empty(self, tmp_csv_factory):
        csvfile = tmp_csv_factory()
        ledger = Ledger()
        ledger.load_from_file(csvfile)

        assert ledger.transactions == []

    def test_get_balance(self):
        ledger = Ledger()
        ledger.transactions.append(
            Transaction(date="2015-1-2", sender="mary", recipient="john", amount="1.2"),
        )
        balance = ledger.get_balance("mary")
        assert balance.entity == "mary"
        assert balance.total == Decimal("-1.2")

        ledger.transactions.append(
            Transaction(date="2015-1-2", sender="john", recipient="mary", amount="100"),
        )
        balance = ledger.get_balance("mary")
        assert balance.entity == "mary"
        assert balance.total == Decimal("98.8")

    def test_get_balance_empty_ledger(self):
        ledger = Ledger()

        balance = ledger.get_balance("mike")

        assert balance.entity == "mike"
        assert balance.total == Decimal(0)

    def test_get_balance_entity_not_present(self):
        ledger = Ledger()
        ledger.transactions += [
            Transaction(date="2015-01-18", sender="mary", recipient="john", amount="1"),
            Transaction(date="2015-01-18", sender="john", recipient="mary", amount="1"),
        ]

        balance = ledger.get_balance("mike")

        assert balance.entity == "mike"
        assert balance.total == Decimal(0)

    def test_get_balance_requesting_old_date(self):
        ledger = Ledger()
        ledger.transactions += [
            Transaction(date="2015-01-18", sender="mary", recipient="john", amount="1"),
            Transaction(date="2015-01-18", sender="john", recipient="mary", amount="1"),
        ]

        balance = ledger.get_balance("mary", date(2010, 1, 2))

        assert balance.entity == "mary"
        assert balance.total == Decimal(0)

    def test_get_balance_cancel_itself_transactions(self):
        ledger = Ledger()
        ledger.transactions += [
            Transaction(date="2015-1-2", sender="mary", recipient="john", amount="1.2"),
            Transaction(date="2015-1-3", sender="john", recipient="mary", amount="1.2"),
        ]

        balance = ledger.get_balance("mary")

        assert balance.entity == "mary"
        assert balance.total == Decimal(0)

    def test_get_balance_same_sender_and_recipient(self):
        ledger = Ledger()
        ledger.transactions.append(
            Transaction(date="2015-1-2", sender="mary", recipient="mary", amount="1.2"),
        )

        balance = ledger.get_balance("mary")

        assert balance.entity == "mary"
        assert balance.total == Decimal(0)

    def test_get_balance_requesting_equal_and_newer_dates(self):
        ledger = Ledger()
        ledger.transactions += [
            Transaction(date="2015-1-2", sender="mary", recipient="john", amount="1.2"),
            Transaction(date="2015-1-3", sender="john", recipient="mary", amount="1.2"),
            Transaction(date="2020-1-2", sender="mike", recipient="mary", amount="1.4"),
        ]
        balance = ledger.get_balance("mary", date(2020, 1, 2))
        assert balance.entity == "mary"
        assert balance.total == Decimal("1.4")
