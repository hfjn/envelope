from budget.tools import parse_ofx
from budget.database import Database

if __name__ == "__main__":
    transactions = parse_ofx()
    for transaction in transactions:
        print(transaction)

    db = Database()
    db.write_transactions(transactions)


