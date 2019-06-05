import sys
from pathlib import Path
from typing import Union, Any

import click
import pendulum
from PyInquirer import prompt
from tabulate import tabulate
from yaspin import yaspin

from envelope import ledger
from envelope.cli.output import pretty_dict
from envelope.parser import hash_file
from envelope.tools import list_files
from envelope.transaction import Transaction


@click.group()
def envelope() -> None:
    pass


@envelope.command()
@click.argument("account", type=click.Choice(ledger.config.accounts_names))
@click.option("--n", default=100, help="Number of rows")
def list(account, n) -> None:
    transactions = [
        [
            transaction.id,
            transaction.date,
            transaction.payee,
            transaction.category,
            transaction.amount,
            transaction.currency,
        ]
        for transaction in ledger.filter_transactions(
            "account", account, number_of_rows=n
        )
    ]
    click.echo(
        tabulate(
            transactions,
            headers=("id", "date", "payee", "category", "amount", "currency"),
        )
    )


@envelope.command()
@click.argument("id")
def edit(id):
    transaction: Transaction = ledger.filter_transactions("id", id)[0]
    edited = click.edit(transaction.to_yaml())
    if not edited:
        click.echo("Editing was cancelled.")
        sys.exit(1)
    transaction.from_yaml(edited)


@envelope.command()
def get() -> None:
    raise NotImplementedError


@envelope.command()
def add() -> None:
    raise NotImplementedError


@envelope.command()
@click.option("--start-date")
@click.option("--end-date")
def income(
    start_date: Union[str, pendulum.DateTime], end_date: Union[str, pendulum.DateTime]
) -> None:
    if not start_date:
        start_date = ledger.start_date
    if not end_date:
        end_date = ledger.end_date

    if isinstance(start_date, str):
        start_date = pendulum.parse(start_date)
    if isinstance(end_date, str):
        end_date = pendulum.parse(end_date)

    pretty_dict(ledger.income_statement(start_date, end_date))


# TODO: Enable possibility to set configs
@envelope.command()
def config() -> None:
    pretty_dict(ledger.config.config, break_after_key=True)


@envelope.command()
@click.option("--group", default="account", required=False)
def balance(group: str) -> None:
    pretty_dict(ledger.balance(group=group))


@envelope.command()
def stats() -> None:
    click.echo(f"Start Date: {ledger.start_date.to_date_string()}")
    click.echo(f"End Date: {ledger.end_date.to_date_string()}")
    click.echo(f"Last Import: {ledger.last_import.to_date_string()}")
    click.echo(f"Payees: {len(ledger.payees)}")
    click.echo(f"Accounts: {len(ledger.accounts)}")
    click.echo(f"Transactions: {ledger.num_transactions}")


@envelope.command()
def import_files() -> None:
    path = Path.cwd() / "data"
    files = list_files(path)
    for file in files:
        if _file_load_necessary(file):
            account_name = _get_account_name(file)
            _load_transactions_from_file(file, account_name)
        else:
            click.echo(f"No new transactions found in {file.stem}{file.suffix}")


def _load_transactions_from_file(file: Path, account_name: str) -> None:
    with yaspin(text=f"Importing {file.stem + file.suffix}...") as spinner:
        number_of_new_transactions = ledger.import_transactions_from_file(
            file, account_name=account_name
        )
        spinner.text = ""
        spinner.ok(f"✅ Added {number_of_new_transactions} new transactions.")


def _get_account_name(file: Path) -> Any:
    file_name = f"{file.stem}{file.suffix}"
    if file_name in ledger.file_state.keys():
        return ledger.file_state[file_name]["account_name"]
    click.echo()
    questions = [
        {
            "type": "list",
            "name": "account_name",
            "message": f"Account name of {file.stem+file.suffix}:",
            "choices": ledger.config.accounts_names,
        }
    ]

    answers = prompt(questions)
    return answers["account_name"]


def _file_load_necessary(file: Path) -> bool:
    file_name = f"{file.stem}{file.suffix}"
    if file_name not in ledger.file_state:
        return True
    if ledger.file_state[file_name]["hash"] != hash_file(file):
        return True
    return False


@envelope.command("net-worth")
def networth() -> None:
    raise NotImplementedError
