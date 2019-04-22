import functools
import json
from itertools import groupby
from pathlib import Path
from typing import List, Dict, Callable, Set, Any

import pendulum

from envelope import parser, config
from envelope.transaction import Transaction

Snapshot: Path = Path(config["settings"]["folder"]) / "snapshot.json"  # type: ignore


class Ledger:
    def __init__(self, *, ledger_file: str = None) -> None:
        self.transactions: List[Transaction] = []
        if ledger_file:
            try:
                self.load_from_json(ledger_file)
            except FileNotFoundError:
                print(f"File {ledger_file} does not exist. Loaded empty ledger.")

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

    @property
    def json(self) -> str:
        return json.dumps(self.transactions, default=lambda x: x.as_dict())

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

    def write_to_json(self) -> None:
        file = Path("output.json")
        file.write_text(self.json)

    def load_from_json(self, file_path: str) -> None:
        with Path(file_path).open() as f:
            transactions = json.load(f)
            self.transactions = [
                Transaction(**parser.parse_json_row(transaction))
                for transaction in transactions
            ]

    def _persist(func: Callable) -> Any:  # type: ignore
        @functools.wraps(func)
        def wrapper(self, *args: Any, **kwargs: Any) -> Any:  # type: ignore
            result = func(self, *args, **kwargs)
            self.write_to_json()
            return result

        return wrapper

    @_persist
    def import_transactions_from_file(
        self, file_path: Path, *, account_name: str = None
    ) -> int:
        old_length = len(self.transactions)
        new_transactions = parser.parse_file(file_path, account_name)
        self.add_transactions(new_transactions)
        return len(self.transactions) - old_length

    def add_transactions(
        self, new_transactions: List[Transaction], *, validation: bool = True
    ) -> None:
        if validation and len(self.transactions) != 0:
            self.transactions += [
                transaction
                for transaction in new_transactions
                if transaction not in self.transactions
            ]
        else:
            self.transactions += [transaction for transaction in new_transactions]
