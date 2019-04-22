from pathlib import Path
from typing import List


# Todo: Readd possibility to parse ofx
#
# def parse_ofx(account: Account) -> List[Optional[Transaction]]:
#     with codecs.open("../data/creditcard.ofx", encoding="latin-1") as file:
#         ofx = OfxParser.parse(file)
#
#     transactions = _parse_transactions_from_statement(account, ofx.account.statement)
#
#     return transactions


def list_files(path: str) -> List[Path]:
    import_folder = Path(path)
    assert import_folder.is_dir(), "Must be a folder."
    return [file for file in import_folder.glob("*.csv")]


#
# def _parse_transactions_from_statement(
#     account: Account, statement: ofxparse.Statement
# ) -> List[Optional[Transaction]]:
#
#     _transactions = []
#     for ofx_transaction in statement.transactions:
#         parsed_date = datetime.fromisoformat(str(ofx_transaction.date))
#
#         _transaction = Transaction(
#             parsed_date, account, ofx_transaction.amount, payee=ofx_transaction.payee
#         )
#
#         _transactions.append(_transaction)
#
#     return _transactions
