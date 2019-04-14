import pendulum


class Transaction:
    def __init__(
        self,
        date: pendulum.datetime = None,
        account: str = None,
        amount: float = None,
        payee: str = None,
        currency="€",
        purpose="",
        value_date: pendulum.datetime = None,
        category=None,
    ):
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

    @property
    def formatted_date(self):
        return self.date.date().isoformat()
