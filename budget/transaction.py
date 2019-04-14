from typing import Any, Dict, Optional

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
        if isinstance(date, str):
            date = pendulum.parse(date)

        if isinstance(value_date, str):
            value_date = pendulum.parse(value_date)

        self.date: pendulum.Date = date
        self.amount: float = amount
        self.purpose: str = purpose
        self.payee: str = payee
        self.account: str = account
        self.category: str = category
        self.value_date: pendulum.Date = value_date

        if currency == "EUR":
            self.currency: str = "€"

    def __str__(self):
        return f"{self.date.date()}: {self.account} - {self.payee} {self.amount}{self.currency}"

    def __repr__(self):
        return f"{self.date.date()}: {self.account} - {self.payee} {self.amount}{self.currency}"

    def as_dict(self) -> Dict[str, Any]:
        formatted_transaction = self.__dict__
        formatted_transaction["date"] = self.date.isoformat()
        if self.value_date:
            formatted_transaction["value_date"] = self.value_date.isoformat()
        else:
            formatted_transaction["value_date"] = None
        return formatted_transaction

    @property
    def formatted_date(self):
        return self.date.date().isoformat()
