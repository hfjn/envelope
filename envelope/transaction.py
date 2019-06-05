import datetime
from typing import Any, Dict

import pendulum
import yaml
from sqlalchemy import Column, Integer, String, DateTime, Float, TIMESTAMP
from sqlalchemy.exc import DatabaseError

from envelope.backend import BaseModel, session, commit


class Transaction(BaseModel):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    account = Column(String)
    amount = Column(Float)
    payee = Column(String)
    currency = Column(String)
    purpose = Column(String, nullable=True)
    value_date = Column(DateTime, nullable=True)
    category = Column(String, nullable=True)
    added_timestamp = Column(TIMESTAMP)
    meta = Column(String)

    def __init__(
        self,
        date: pendulum.DateTime = None,
        account: str = None,
        amount: float = None,
        payee: str = None,
        currency: str = "€",
        purpose: str = "",
        value_date: pendulum.DateTime = None,
        category: str = None,
        added_timestamp: pendulum.DateTime = None,
        meta: str = None,
    ):
        self.date: pendulum.DateTime = date
        self.amount: float = amount
        self.purpose: str = purpose
        self.payee: str = payee
        self.account: str = account
        self.category: str = category
        self.value_date: pendulum.DateTime = value_date
        self.currency: str = currency
        self.added_timestamp: pendulum.DateTime = added_timestamp
        self.meta: str = meta

    def __str__(self) -> str:
        return f"{self.date.isoformat()}: {self.account} - {self.payee} {self.amount}{self.currency}"

    def __repr__(self) -> str:
        return f"{self.date},{self.value_date},{self.purpose},{self.account},{self.amount},{self.payee},{self.currency}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Transaction):
            return False
        return other.as_dict() == self.as_dict()

    @classmethod
    def get_or_create(cls, **kwargs):
        kwargs.pop(
            "import_timestamp"
        )  # Import Date should not be used to identify uniqueness
        exists = session.query(Transaction.id).filter_by(**kwargs).scalar() is not None
        if exists:
            return session.query(Transaction).filter_by(**kwargs).first()
        return Transaction(**kwargs)

    @property
    def iso_date(self) -> Any:
        return self.date.isoformat()

    @property
    def iso_value_date(self) -> Any:
        return self.value_date.isoformat()

    def as_dict(self) -> Dict[str, Any]:
        return {
            "amount": self.amount,
            "purpose": self.purpose,
            "account": self.account,
            "value_date": self.value_date.isoformat(),
            "date": self.date.isoformat(),
            "payee": self.payee,
            "category": self.category,
        }

    def to_yaml(self) -> str:
        return yaml.dump(self.as_dict())

    def _pendulum_to_datetime(self, parsed: pendulum.DateTime):
        return datetime.datetime(
            parsed.year,
            parsed.month,
            parsed.day,
            parsed.hour,
            parsed.minute,
            parsed.second,
            parsed.microsecond,
            tzinfo=parsed.tz,
        )

    @commit
    def from_yaml(self, data) -> None:
        new_values = yaml.safe_load(data)
        for attr, value in new_values.items():
            if attr == "date" or attr == "value_date":
                value = self._pendulum_to_datetime(pendulum.parse(value))
            setattr(self, attr, value)
        self.save()

    def save(self):
        session.add(self)
        self._flush()
        return self

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save()

    def delete(self):
        session.delete(self)
        self._flush()

    def _flush(self):
        try:
            session.flush()
        except DatabaseError:
            session.rollback()
            raise
