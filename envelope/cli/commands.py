import pprint
from typing import Union

import click
import pendulum
from envelope import ledger
from envelope.tools import list_files


@click.group()
def envelope() -> None:
    pass


@envelope.command()
def list() -> None:
    raise NotImplementedError


@envelope.command()
def get() -> None:
    raise NotImplementedError


@envelope.command()
@click.option("--start-date", default=ledger.start_date)
@click.option("--end-date", default=ledger.end_date)
def income(
    start_date: Union[str, pendulum.DateTime], end_date: Union[str, pendulum.DateTime]
) -> None:
    if isinstance(start_date, str):
        start_date = pendulum.parse(start_date)
    if isinstance(end_date, str):
        end_date = pendulum.parse(end_date)
    for income, value in ledger.income_statement(start_date, end_date).items():
        click.echo(f"{income}: {value:0.2f}€")


# TODO: Enable possibility to set configs
@envelope.command()
def config() -> None:
    pprint.pprint(ledger.config.config)


@envelope.command()
@click.option("--group", default="account", required=False)
def balance(group: str) -> None:
    for balance, value in ledger.balance(group=group).items():
        click.echo(f"{balance}: {value:0.2f}€")


@envelope.command()
def stats() -> None:
    click.echo(f"Start Date: {ledger.start_date.to_date_string()}")
    click.echo(f"End Date: {ledger.end_date.to_date_string()}")
    click.echo(f"Payees: {len(ledger.payees)}")
    click.echo(f"Accounts: {len(ledger.accounts)}")
    click.echo(f"Transactions: {len(ledger.transactions)}")


@envelope.command()
def import_files() -> None:
    files = list_files("/Users/hfjn/code/envelope/data")
    for file in files:
        choices = [
            account["friendly_name"] for _, account in ledger.config.accounts.items()
        ]
        account_name = click.prompt(
            f"Account name of {file.stem}:", default=None, type=click.Choice(choices)
        )
        number_of_new_transactions = ledger.import_transactions_from_file(
            file, account_name=account_name
        )
        click.echo(f"Added {number_of_new_transactions} new transactions.")


@envelope.command("net-worth")
def networth() -> None:
    raise NotImplementedError
