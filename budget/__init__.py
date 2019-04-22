from pathlib import Path

import toml

from budget.ledger import Ledger

_CONFIG = Path("/Users/hfjn/code/budget/config/config.toml")

with _CONFIG.open() as c:
    config = toml.load(c)

ledger = Ledger(ledger_file="output.json")