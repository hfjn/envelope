import csv
from collections import OrderedDict
from pathlib import Path
from typing import List, Dict
import pprint

import pendulum

from budget.transaction import Transaction


BUDGET_REGEX = "#\s([0-9]{4}\-[0-9]{2})"

MONEY_MONEY_MAPPING: Dict[str, str] = {
    "fields": {
        "date": "Date",
        "value_date": "Value date",
        "category": "Category",
        "payee": "Name",
        "purpose": "Purpose",
        "amount": "Amount",
        "currency": "Currency",
    },
    "date_layout": "DD.MM.YY",
    "decimal_separator": ",",
}



def parse_csv(file_path: Path, account_name: str):
    with file_path.open() as f:
        csv_reader = csv.DictReader(f, delimiter=";")
        return [
            _parse_row(row, MONEY_MONEY_MAPPING, account_name) for row in csv_reader
        ]


def _parse_row(
    row: OrderedDict, mapping: Dict[str, str], account_name: str
) -> Transaction:
    transaction = {"account": account_name}
    for field, mapped_field in mapping["fields"].items():
        if field == "date" or field == "value_date":
            transaction[field] = pendulum.from_format(
                row[mapped_field], mapping["date_layout"]
            )
        elif field == "amount":
            transaction[field] = _parse_amount(
                row[mapped_field], mapping["decimal_separator"]
            )
        else:
            transaction[field] = row[mapped_field]
    return Transaction(**transaction)


def _parse_amount(amount: str, separator: str):
    return float(amount.replace(separator, "."))


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


if __name__ == "__main__":
    parse_csv()
