import ofxparse
from ofxparse import OfxParser
import codecs

from datetime import datetime, date

from typing import List, Optional, Dict

from .finances import Account, Transaction


def parse_ofx(account: Account) -> List[Optional[Transaction]]:
    with codecs.open("../data/creditcard.ofx", encoding="latin-1") as file:
        ofx = OfxParser.parse(file)

    transactions = _parse_transactions_from_statement(
        account, ofx.account.statement
    )

    return transactions


def _parse_transactions_from_statement(
    account: Account, statement: ofxparse.Statement
) -> List[Optional[Transaction]]:

    _transactions = []
    for ofx_transaction in statement.transactions:
        parsed_date = datetime.fromisoformat(str(ofx_transaction.date))

        _transaction = Transaction(
            parsed_date,
            account,
            ofx_transaction.amount,
            payee=ofx_transaction.payee
        )

        _transactions.append(_transaction)

    return _transactions




