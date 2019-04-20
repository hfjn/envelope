import click

from budget import ledger
from budget.tools import list_files


@click.group()
def budget():
    pass


@budget.command()
def balance():
    for balance, value in ledger.balance().items():
        click.echo(f"{balance}: {value:0.2f}€")


@budget.command()
def import_files():
    files = list_files("/Users/hfjn/code/budget/data")
    for file in files:
        account_name = click.prompt(f"Account name for {file.stem}:", type=str, default=None)
        number_of_new_transactions = ledger.load_from_file(file, account_name=account_name)
        click.echo(f"Added {number_of_new_transactions} new transactions.")

