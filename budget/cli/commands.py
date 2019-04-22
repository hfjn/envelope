import click

from budget import ledger, config
from budget.tools import list_files


@click.group()
def budget():
    pass


@budget.command()
def list():
    raise NotImplementedError


@budget.command()
def get():
    raise NotImplementedError


@budget.command()
@click.option("--group", default="account", required=False)
def balance(group):
    for balance, value in ledger.balance(group=group).items():
        click.echo(f"{balance}: {value:0.2f}€")

@budget.command()
def stats():
    click.echo(f"Start Date: {ledger.start_date.to_date_string()}")
    click.echo(f"End Date: {ledger.end_date.to_date_string()}")
    click.echo(f"Payees: {len(ledger.payees)}")
    click.echo(f"Accounts: {len(ledger.accounts)}")
    click.echo(f"Transactions: {len(ledger.transactions)}")


@budget.command()
def import_files():
    files = list_files("/Users/hfjn/code/budget/data")
    for file in files:
        choices = [account["friendly_name"] for _, account in config["accounts"].items()]
        account_name = click.prompt(
            f"Account name of {file.stem}:", default=None, type=click.Choice(choices)
        )
        number_of_new_transactions = ledger.import_transactions_from_file(
            file, account_name=account_name
        )
        click.echo(f"Added {number_of_new_transactions} new transactions.")


@budget.command("net-worth")
def networth():
    raise NotImplementedError
