from db.db import create_db_conn
from sql.transaction import Querier as TransactionQuerier
from sql.models import Transaction
from typing import List

conn = create_db_conn()
transaction_querier = TransactionQuerier(conn=conn)


def get_transactions(limit: int) -> List[Transaction]:
    values = transaction_querier.get_transaction()
    return values
