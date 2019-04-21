import csv
import pytest

@pytest.fixture(scope="session")
def test_data():
    return {"date": "2019-04-17T00:00:00+00:00", "amount": -39.95, "purpose": "Mobilfunk Kundenkonto 0060259776 Rg 25116694000731/05.04.2019, Transaction type: Folgelastschrift, Reference: Zahlbeleg 390789093522, Mandate: DE000205000600000000000000011969993, Creditor ID: DE93ZZZ00000078611", "payee": "Telekom Deutschland GmbH Landgrabenweg 151", "account": "DKB", "category": "", "value_date": "2019-04-17T00:00:00+00:00", "currency": "\u20ac"}


@pytest.fixture(scope="session")
def money_money_data():
