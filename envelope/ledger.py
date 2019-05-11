import json
from itertools import groupby
from pathlib import Path
from typing import Any, Dict, Set

import pendulum

from envelope import parser
from envelope.backend import session, BaseModel, engine, commit
from envelope.config import Config
from envelope.transaction import Transaction


class Ledger:
    def __init__(self) -> None:
        self.config: Config = Config()
        self._snapshot: Path = Path(self.config.folder) / self.config.snapshot_name
        self.file_state: Dict[str, Any] = {}

        BaseModel.metadata.drop_all(bind=engine)
        BaseModel.metadata.create_all(bind=engine)

    @property
    def transactions(self):
        return session.query(Transaction).count()

    @property
    def payees(self) -> Set:
        return set(t.payee for t in self.transactions)

    @property
    def currencies(self) -> Set:
        return set(t.currency for t in self.transactions)

    @property
    def accounts(self) -> Set:
        return set(t.account for t in self.transactions)

    @property
    def start_date(self) -> pendulum.DateTime:
        return min(set(t.date for t in self.transactions))

    @property
    def end_date(self) -> pendulum.DateTime:
        return max(set(t.date for t in self.transactions))

    def as_dict(self) -> Dict[str, Any]:
        return {
            "file_state": self.file_state,
            "transactions": [
                transaction.as_dict() for transaction in self.transactions
            ],
        }

    @property
    def json(self) -> str:
        return json.dumps(self.as_dict())

    def running_balance(
        self, start: pendulum.DateTime, end: pendulum.DateTime
    ) -> Dict[Any, float]:
        balance_range: pendulum.Period = pendulum.period(start, end)
        return {day: self.balance(date=day)[day] for day in balance_range.range("days")}

    def balance(
        self, *, date: pendulum.DateTime = pendulum.now(), group: str = "account"
    ) -> Dict[pendulum.DateTime, float]:
        balances = {}
        for grouped, transactions in groupby(
            self.transactions, key=lambda t: getattr(t, group)  # type: ignore
        ):
            balances[grouped] = sum(
                transaction.amount
                for transaction in transactions
                if transaction.date < date
            )
        return balances

    def income_statement(
        self, start_date: pendulum.DateTime, end_date: pendulum.DateTime
    ) -> Dict[str, float]:
        statement: Dict[str, float] = {}
        for transaction in self.transactions:
            if transaction.amount > 0 and start_date <= transaction.date <= end_date:
                if transaction.payee in statement:
                    statement[transaction.payee] += transaction.amount
                else:
                    statement[transaction.payee] = transaction.amount
        return statement

    def write_to_json(self) -> None:
        file = Path(self._snapshot)
        file.write_text(self.json)

    @commit
    def load_from_json(self, file_path: Path) -> None:
        with file_path.open() as f:
            json_dump = json.load(f)
            transactions = [
                Transaction(**parser.parse_json_row(transaction))
                for transaction in json_dump["transactions"]
            ]
            self.file_state = json_dump["file_state"]

        for transaction in transactions:
            transaction.save()

    @commit
    def import_transactions_from_file(
        self, file_path: Path, *, account_name: str = None
    ):
        self.file_state[f"{file_path.stem}{file_path.suffix}"] = {
            "hash": parser.hash_file(file_path),
            "account_name": account_name,
        }
        old_number = self.transactions
        new_transactions = parser.parse_file(file_path, account_name)

        for transaction in new_transactions:
            transaction.save()

        return self.transactions - old_number
