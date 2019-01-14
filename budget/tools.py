import ofxparse
from ofxparse import OfxParser
import codecs

from typing import List, Optional

from .finances import Transaction


def parse_ofx() -> List[Optional[Transaction]]:
    with codecs.open("../data/creditcard.ofx", encoding="latin-1") as file:
        ofx = OfxParser.parse(file)

    print(ofx.account.type)
    transactions = _parse_transactions_from_statement(ofx.account.statement)

    return transactions


def _parse_transactions_from_statement(
    statement: ofxparse.Statement
) -> List[Optional[Transaction]]:

    _transactions = []
    for ofx_transaction in statement.transactions:
        _transaction = Transaction(
            ofx_transaction.date,
            ofx_transaction.amount,
            "CreditCard",
            ofx_transaction.payee,
            "Unbudgeted",
            currency=statement.currency,
            description=ofx_transaction.memo
        )

        _transactions.append(_transaction)

    return _transactions

