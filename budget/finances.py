from datetime import datetime
from typing import Dict


class Budget:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Account:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Transaction:
    def __init__(
        self,
        date: datetime,
        account: Account,
        amount: float,
        *,
        payee: str = None,
        budget: Budget = None,
        currency="€",
        description="",
    ):
        self._date: datetime = date
        self.currency: str = currency
        self.amount: float = amount
        self.description: str = description
        self.payee: str = payee
        self.account: Account = account
        self.budget: Budget = budget

    def __str__(self):
        return f"{self._date.date()}: {self.account} - {self.payee} {self.amount}{self.currency} [{self.budget}]"

    @property
    def date(self):
        return self._date.date().isoformat()


class SplitTransaction(Transaction):
    def __init__(
        self,
        date: datetime,
        account: Account,
        amount: float,
        subactions: Dict[Budget, float],
        *,
        payee: str = None,
        currency="Euro",
        description=None,
    ):
        super().__init__(
            date,
            account,
            amount,
            payee=payee,
            currency=currency,
            description=description,
        )
        self.subactions: Dict[Budget, float] = subactions

        assert self.amount + self._sum_subactions() == 0

    def _sum_subactions(self):
        subaction_sum = 0
        for _, value in self.subactions.items():
            subaction_sum += value
        return subaction_sum
