from .finances import Transaction
from typing import List

FILE_PATH = "/Users/hfjn/code/budget/ledger.ldg"

BUDGET_REGEX = "#\s([0-9]{4}\-[0-9]{2})"

#
# def parse_file():
#     for line in _iterate_on_lines(FILE_PATH):
#         if line.startswith("#"):
#             _parse_budget_line(line)
#         elif line.startswith("*"):
#             _parse_transaction_line(line)
#         else:
#             _parse_line(line)
#
#
# def _parse_budget_line(line: str):
#     "#"


# def _iterate_on_lines(file_name):
#     with open(FILE_PATH) as f:
#         for line in f:
#             yield line.rstrip("\n")


def write_transactions(transactions: List[Transaction]):
    with open(FILE_PATH, "w") as ledger:
        for transaction in transactions:
            ledger.writelines(_prepare_transaction(transaction))
            ledger.write("\n")


def _prepare_transaction(transaction: Transaction) -> List[str]:
    prepared_list: List[str] = []
    prepared_list.append(f"{transaction.date} - {transaction.description}\n")
    prepared_list.append(
        f'    "{transaction.payee}" {transaction.amount} {transaction.currency}\n'
    )
    for budget, value in transaction.subactions.items():
        prepared_list.append(f'    "{budget}", {value} {transaction.currency}\n')
    return prepared_list
