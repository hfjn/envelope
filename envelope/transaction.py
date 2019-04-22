from typing import Any, Dict

import pendulum


class Transaction:
    def __init__(
        self,
        date: pendulum.Datetime = None,
        account: str = None,
        amount: float = None,
        payee: str = None,
        currency: str = "€",
        purpose: str = "",
        value_date: pendulum.Datetime = None,
        category: str = None,
    ):
        self.date: pendulum.Datetime = date
        self.amount: float = amount
        self.purpose: str = purpose
        self.payee: str = payee
        self.account: str = account
        self.category: str = category
        self.value_date: pendulum.Datetime = value_date

        if not isinstance(self.date, pendulum.DateTime):
            raise ValueError(f"Date {self.date} not pendulum.DateTime")
        if not isinstance(self.value_date, pendulum.DateTime):
            raise ValueError(f"Date {self.value_date} not pendulum.DateTime")

        if currency == "EUR":
            self.currency: str = "€"

        else:
            self.currency: str = currency

    def __str__(self) -> str:
        return f"{self.date.isoformat()}: {self.account} - {self.payee} {self.amount}{self.currency}"

    def __repr__(self) -> str:
        return f"{self.date},{self.value_date},{self.purpose},{self.account},{self.amount},{self.payee},{self.currency}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Transaction):
            return False
        return other.as_dict() == self.as_dict()

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
