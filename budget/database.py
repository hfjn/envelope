import apsw

from typing import List

from .finances import Transaction


class Database:
    def __init__(self):
        self._connection_string = "/Users/hfjn/.pybudget"
        self._table_name = "transactions"
        if not self._table_exists():
            self._create_transaction_table()

    def _table_exists(self):
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self._table_name}';"
        with apsw.Connection(self._connection_string) as conn:
            cursor = conn.cursor()
            result = [row for row in cursor.execute(query)]
            print(result)
        return len(result) > 0

    def _create_transaction_table(self):
        create_query = f"""CREATE TABLE {self._table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        date DATE NOT NULL, 
        amount DECIMAL(10,2) NOT NULL, 
        account VARCHAR(255) NOT NULL, 
        payee VARCHAR(255) NOT NULL, 
        budget VARCHAR(255), 
        currency CHAR(10) NOT NULL, 
        description TEXT);
        """

        with apsw.Connection(self._connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute(create_query)

    def write_transactions(self, transactions: List[Transaction]):
        queries = [
            transaction.prepare_insert_query(self._table_name)
            for transaction in transactions
        ]

        print(queries)

        with apsw.Connection(self._connection_string) as conn:
            cursor = conn.cursor()
            for query in queries:
                cursor.execute(query)
