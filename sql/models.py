# Code generated by sqlc. DO NOT EDIT.
# versions:
#   sqlc v1.27.0
import dataclasses
import decimal
from typing import Optional
import uuid


@dataclasses.dataclass()
class Transaction:
    id: uuid.UUID
    remarks: str
    amount: decimal.Decimal
    category: Optional[str]
