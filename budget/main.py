from budget.tools import parse_ofx, daily_balance, running_balance
from budget.parser import write_transactions
from budget import ledger
from datetime import datetime


if __name__ == "__main__":
    accounts = {"Kreditkarte": ledger.Account("Kreditkarte")}
    budget = {"Lebensmittel": ledger.Budget("Lebensmittel")}
    transactions = parse_ofx(accounts["Kreditkarte"])

    print(daily_balance(transactions))
    print(running_balance(transactions))
