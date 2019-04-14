from itertools import groupby
from pathlib import Path
from typing import List, Dict
import json

import pendulum

from budget.parser import parse_csv
from budget.transaction import Transaction

Giro = Path("/Users/hfjn/code/budget/data/Giro.csv")
Kreditkarte = Path("/Users/hfjn/code/budget/data/Kreditkarte.csv")


class Ledger:
    def __init__(self):
        self.transactions: List[Transaction] = []

    @property
    def payees(self):
        return set(t.payee for t in self.transactions)

    @property
    def currencies(self):
        return set(t.currency for t in self.transactions)

    @property
    def accounts(self):
        return set(t.account for t in self.transactions)

    @property
    def start_date(self):
        return min(set(t.date for t in self.transactions))

    @property
    def json(self):
        return json.dumps(self.transactions, default=lambda x: x.as_dict())

    def add_transactions_from_file(self):
        self.transactions += parse_csv(Giro, "DKB")
        self.transactions += parse_csv(Kreditkarte, "Kreditkarte")

    def running_balance(
        self, start: pendulum.DateTime, end: pendulum.DateTime
    ) -> Dict[str, float]:
        balance_range = pendulum.period(start, end)
        for day in balance_range.range("days"):
            print(f"{day.isoformat()}: {self.balance(date=day)}")

    # TODO: Make group key dynamic
    def balance(self, *, date: pendulum.DateTime = pendulum.now()):
        balances = {}
        for account, transactions in groupby(
            self.transactions, key=lambda t: t.account
        ):
            balances[account] = sum(
                transaction.amount
                for transaction in transactions
                if transaction.date < date
            )
        return balances

    def write_to_file(self):
        file = Path("output.json")
        file.write_text(self.json)

    def load_from_file(self, file_path: str):
        with Path(file_path).open() as f:
            transactions = json.load(f)
            self.transactions = [Transaction(**transaction) for transaction in transactions]


if __name__ == "__main__":
    ledger.load_from_file("output.json")
    print(ledger.balance())
