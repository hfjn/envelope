import json
from itertools import groupby
from pathlib import Path
from typing import List, Dict

import pendulum

from budget.transaction import Transaction
from budget import parser

Snapshot = Path("/Users/hfjn/code/budget/output.json")

Giro = Path("/Users/hfjn/code/budget/data/Giro.csv")
Kreditkarte = Path("/Users/hfjn/code/budget/data/Kreditkarte.csv")


class Ledger:
    def __init__(self):
        self.transactions: List[Transaction] = []
        self.load_from_json("output.json")

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

    def running_balance(
        self, start: pendulum.DateTime, end: pendulum.DateTime
    ) -> Dict[str, float]:
        balance_range = pendulum.period(start, end)
        for day in balance_range.range("days"):
            print(f"{day.isoformat()}: {self.balance(date=day)}")

    def balance(
        self, *, date: pendulum.DateTime = pendulum.now(), group: str = "account"
    ):
        balances = {}
        for grouped, transactions in groupby(
            self.transactions, key=lambda t: getattr(t, group)
        ):
            balances[grouped] = sum(
                transaction.amount
                for transaction in transactions
                if transaction.date < date
            )
        return balances

    def write_to_json(self):
        file = Path("output.json")
        file.write_text(self.json)

    def load_from_json(self, file_path: str):
        with Path(file_path).open() as f:
            transactions = json.load(f)
            self.transactions = [
                Transaction(**transaction) for transaction in transactions
            ]

    def load_from_file(self, file_path: Path, *, account_name=None) -> int:
        old_length = len(self.transactions)
        with file_path.open() as f:
            new_transactions = parser.parse_csv(f, account_name)
            self.add_to_transactions(new_transactions)
        return len(self.transactions) - old_length

    def add_to_transactions(self, new_transactions: List[Transaction]):
        self.transactions += [
            transaction
            for transaction in new_transactions
            if transaction not in set(self.transactions)
        ]
