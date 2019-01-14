# import apsw
from datetime import datetime
from hashlib import sha1
from peewee import BaseModel


class Transaction(BaseModel):
    def __init__(
        self,
        date: datetime,
        amount: float,
        account: str,
        payee: str,
        budget: str,
        *,
        key=None,
        currency="Euro",
        description=None,
    ):
        self._date: datetime = date
        self._amount: float = amount
        self._currency: str = currency
        self._description: str = description
        self._payee: str = payee
        self._account: str = account
        self._budget: str = budget

    def __str__(self):
        return f"{self._date.date()}: {self._account} - {self._payee} {self._amount}{self._currency} {self._description}"

    def prepare_insert_query(self, table_name: str) -> str:
        return f"""INSERT INTO {table_name} (date, amount, account, payee, 
        budget, currency, description) 
        VALUES ('{self._date.date()}', {self._amount}, '{self._account}', '{self._payee}', '{self._budget}','{self._currency}', '{self._description}')"""
