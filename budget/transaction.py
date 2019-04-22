from typing import Any, Dict

import pendulum


class Transaction:
    def __init__(
        self,
        date: Any = None,
        account: str = None,
        amount: float = None,
        payee: str = None,
        currency="€",
        purpose="",
        value_date: Any = None,
        category=None,
    ):
        self.date: pendulum.Date = date
        self.amount: float = amount
        self.purpose: str = purpose
        self.payee: str = payee
        self.account: str = account
        self.category: str = category
        self.value_date: pendulum.Date = value_date

        if not isinstance(self.date, pendulum.DateTime):
            raise ValueError(f"Date {self.date} not pendulum.DateTime")
        if not isinstance(self.value_date, pendulum.DateTime):
            raise ValueError(f"Date {self.value_date} not pendulum.DateTime")

        if currency == "EUR":
            self.currency: str = "€"

        else:
            self.currency = currency

    def __str__(self):
        return f"{self.date.isoformat()}: {self.account} - {self.payee} {self.amount}{self.currency}"

    def __repr__(self):
        return f"{self.date},{self.value_date},{self.purpose},{self.account},{self.amount},{self.payee},{self.currency}"

    # TODO: Only use imported & fields for comparison
    def __eq__(self, other):
        if not isinstance(other, Transaction):
            return False
        return other.as_dict() == self.as_dict()

    def __hash__(self):
        return hash(self.__repr__())

    @property
    def iso_date(self):
        return self.date.isoformat()

    @property
    def iso_value_date(self):
        return self.value_date.isoformat()

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

    @property
    def formatted_date(self):
        return self.date.date().isoformat()
