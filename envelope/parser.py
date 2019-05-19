import csv
import hashlib as hash
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, Iterable, List

import pendulum
from envelope.transaction import Transaction

BLOCKSIZE = 65536
MONEY_MONEY_MAPPING: Dict[str, Any] = {
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


def hash_file(file_path: Path) -> str:
    sha = hash.sha256()
    with file_path.open(mode="rb") as file:
        file_buffer = file.read(BLOCKSIZE)
        while len(file_buffer) > 0:
            sha.update(file_buffer)
            file_buffer = file.read(BLOCKSIZE)
    return sha.hexdigest()


def parse_file(file_path: Path, account_name: str, max_account_date) -> Any:
    import_timestamp: pendulum.DateTime = pendulum.now()

    with file_path.open() as file:
        file_type: str = file_path.suffix.replace(".", "")
        if file_type not in FILE_TYPE_MAPPING.keys():
            raise NotImplementedError()
        return FILE_TYPE_MAPPING[file_type](
            file, account_name, import_timestamp, max_account_date
        )


def parse_csv(
    file: Iterable,
    account_name: str,
    import_timestamp: pendulum.DateTime,
    max_account_date: pendulum.DateTime,
) -> List[Transaction]:
    csv_reader = csv.DictReader(file, delimiter=";")

    if max_account_date:
        rows = [
            _parse_csv_row(row, MONEY_MONEY_MAPPING, account_name, import_timestamp)
            for row in csv_reader
            if pendulum.from_format(
                row[MONEY_MONEY_MAPPING["fields"]["date"]],
                MONEY_MONEY_MAPPING["date_layout"],
            )
            >= max_account_date
        ]
    else:
        rows = [
            _parse_csv_row(row, MONEY_MONEY_MAPPING, account_name, import_timestamp)
            for row in csv_reader
        ]
    return rows


def parse_json_row(transaction: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(transaction["date"], pendulum.DateTime):
        transaction["date"] = pendulum.parse(transaction["date"])
    if not isinstance(transaction["value_date"], pendulum.DateTime):
        transaction["value_date"] = pendulum.parse(transaction["value_date"])
    return transaction


def _parse_csv_row(
    row: OrderedDict,
    mapping: Dict[str, Any],
    account_name: str,
    import_timestamp: pendulum.DateTime,
) -> Transaction:
    """
    Parses csv row and sets all fields according to given mapping.
    Account name will be overwritten if given in the csv.
    """

    transaction: Dict[str, Any] = {"account": account_name}
    for field, mapped_field in mapping["fields"].items():
        if field == "date" or field == "value_date":
            transaction[field] = pendulum.from_format(
                row[mapped_field], mapping["date_layout"]
            )
        elif field == "amount":
            transaction[field] = _parse_csv_amount(
                row[mapped_field], mapping["decimal_separator"]
            )
        else:
            transaction[field] = row[mapped_field]
    transaction["import_timestamp"] = import_timestamp

    return Transaction.get_or_create(**transaction)


def _parse_csv_amount(amount: str, separator: str) -> float:
    return float(amount.replace(separator, "."))


FILE_TYPE_MAPPING: Dict[str, Any] = {"csv": parse_csv}
