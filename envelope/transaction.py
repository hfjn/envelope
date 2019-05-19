from typing import Any, Dict

import pendulum
from sqlalchemy import Column, Integer, String, DateTime, Float, TIMESTAMP

from envelope.backend import BaseModel, session


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
    import_timestamp = Column(TIMESTAMP)
    row_hash = Column(String)

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
        import_timestamp: pendulum.DateTime = None,
        row_hash: str = None,
    ):
        self.date: pendulum.DateTime = date
        self.amount: float = amount
        self.purpose: str = purpose
        self.payee: str = payee
        self.account: str = account
        self.category: str = category
        self.value_date: pendulum.DateTime = value_date
        self.currency: str = currency
        self.import_timestamp: pendulum.DateTime = import_timestamp
        self.row_hash: str = row_hash

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
        return self.date.date.isoformat()

    @property
    def iso_value_date(self) -> Any:
        return self.value_date.date.isoformat()

    def as_dict(self) -> Dict[str, Any]:
        return {
            "amount": self.amount,
            "purpose": self.purpose,
            "payee": self.payee,
            "account": self.account,
            "category": self.account,
            "value_date": self.value_date.isoformat(),
            "date": self.date.isoformat(),
        }
