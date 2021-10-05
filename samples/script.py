from ledger import Ledger, Transaction

ledger = Ledger()
ledger.load_transactions("full.csv")
transactions = [
    Transaction(date="2020-01-01", sender="mary", recipient="john", amount="52.2"),
    Transaction(date="2020-01-02", sender="john", recipient="mary", amount="21"),
    Transaction(date="2020-01-03", sender="mike", recipient="susan", amount="142.1"),
    Transaction(date="2020-01-04", sender="mary", recipient="mike", amount="0.1"),
]
ledger.load_transactions(transactions)

print("Balance for Mary -->", ledger.get_balance("mary").total)
print("Balance for John -->", ledger.get_balance("john").total)
print("Balance for Mike -->", ledger.get_balance("mike").total)
print("Balance for Susan -->", ledger.get_balance("susan").total)
print("Balance for Supermarket -->", ledger.get_balance("supermarket").total)
