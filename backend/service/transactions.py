from db.db import create_db_conn
from sql.transaction import Querier as TransactionQuerier
from sql.transaction import InsertTransactionParams
from sql.models import Transaction
from typing import List

from helper_utils import generate_uuid


def get_transaction_limit(limit: int) -> List[Transaction]:
    conn = create_db_conn()
    transaction_querier = TransactionQuerier(conn=conn)
    values = transaction_querier.get_transaction_limit(limit=0)
    return values


def get_all_transactions() -> List[Transaction]:
    conn = create_db_conn()
    transaction_querier = TransactionQuerier(conn=conn)
    values = transaction_querier.get_all_transaction()
    return values


def get_category_transactions():
    conn = create_db_conn()
    transaction_querier = TransactionQuerier(conn=conn)
    values = transaction_querier.get_by_category()
    return values


def insert_txn(remarks: str, amount: float, category: str):
    print("===Entering Insert Txn===")
    conn = create_db_conn()
    transaction_querier = TransactionQuerier(conn=conn)
    id = generate_uuid()
    arg = {"id": id, "amount": amount, "remarks": remarks,
           "transaction_date": None, "category": category}
    param = InsertTransactionParams(**arg)
    print(param)

    transaction_querier.insert_transaction(arg=param)
    conn.commit()
    print("===Exiting Insert Txn===")
