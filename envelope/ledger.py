import json
from pathlib import Path
from typing import Any, Dict, Set, Optional

import pendulum
from sqlalchemy import func

from envelope import parser
from envelope.backend import session, BaseModel, engine, commit
from envelope.config import Config
from envelope.transaction import Transaction


class Ledger:
    def __init__(self) -> None:
        self.config: Config = Config()
        self._snapshot: Path = Path(self.config.folder) / self.config.snapshot_name
        self.file_state: Dict[str, Any] = {}

        BaseModel.metadata.create_all(bind=engine)

    @property
    def num_transactions(self):
        return session.query(Transaction).count()

    @property
    def payees(self) -> Set:
        return session.query(Transaction.payee).distinct().all()

    @property
    def currencies(self) -> Set:
        return session.query(Transaction.currency).distinct().all()

    @property
    def accounts(self) -> Set:
        return session.query(Transaction.account).distinct().all()

    @property
    def start_date(self) -> Optional[pendulum.DateTime]:
        result = session.query(func.min(Transaction.date)).first()
        if len(result) == 1:
            return pendulum.instance(result[0])
        return None

    @property
    def last_import(self) -> Optional[pendulum.DateTime]:
        result = session.query(func.max(Transaction.import_timestamp)).first()
        if len(result) == 1:
            return pendulum.instance(result[0])
        return None

    @property
    def end_date(self) -> Optional[pendulum.DateTime]:
        result = session.query(func.max(Transaction.date)).first()
        if len(result) == 1:
            return pendulum.instance(result[0])
        return None

    def running_balance(
        self, start: pendulum.DateTime, end: pendulum.DateTime
    ) -> Dict[Any, float]:
        balance_range: pendulum.Period = pendulum.period(start, end)
        return {day: self.balance(date=day)[day] for day in balance_range.range("days")}

    def balance(
        self, *, date: pendulum.DateTime = pendulum.now(), group: str = "account"
    ) -> Dict[pendulum.DateTime, float]:
        balance_rows = (
            session.query(getattr(Transaction, group), func.sum(Transaction.amount))
            .filter(Transaction.date <= date)
            .group_by(group)
            .all()
        )

        return dict(balance_rows)

    def income_statement(
        self, start_date: pendulum.DateTime, end_date: pendulum.DateTime
    ) -> Dict[str, float]:
        balance_rows = (
            session.query(Transaction.payee, func.sum(Transaction.amount))
            .filter(Transaction.date <= end_date)
            .filter(Transaction.date >= start_date)
            .filter(Transaction.amount >= 0)
            .group_by(Transaction.payee)
            .all()
        )
        return dict(balance_rows)

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
        old_number = self.num_transactions

        max_account_date = (
            session.query(func.max(Transaction.date))
            .filter(Transaction.account == account_name)
            .first()
        )
        if max_account_date[0] is not None:
            max_account_date = pendulum.instance(max_account_date[0])
        else:
            max_account_date = None

        # Make Optional

        new_transactions = parser.parse_file(
            file_path, account_name, max_account_date=max_account_date
        )

        for transaction in new_transactions:
            transaction.save()

        return self.num_transactions - old_number
