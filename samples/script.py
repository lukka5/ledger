from datetime import date

from ledger import Ledger, Transaction

ledger = Ledger()
ledger.load_transactions("full.csv")
transactions = [
    Transaction(date="2015-01-18", sender="mary", recipient="john", amount="52.2"),
    Transaction(date="2015-01-18", sender="john", recipient="mary", amount="21"),
]
ledger.load_transactions(transactions)

print("Balance for Mary -->", ledger.get_balance("mary").total)
print("Balance for John -->", ledger.get_balance("john").total)
print("Balance for Supermarket -->", ledger.get_balance("supermarket").total)
print(
    "Balance for Mary at 2015-01-16 -->",
    ledger.get_balance("mary", date(2015, 1, 16)).total,
)
