from envelope.ledger import Ledger
from envelope.config import get_config

config = get_config()

ledger = Ledger(ledger_file="output.json")
