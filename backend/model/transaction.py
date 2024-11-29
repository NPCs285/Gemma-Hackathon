from pydantic import BaseModel, Field
from typing import Dict, Any

from langchain.output_parsers import PydanticOutputParser


class Transaction(BaseModel):
    remarks: str = Field(description="description of transaction")
    amount: float = Field(description="amount present in the transaction")
    category: str = Field(description="category of the transaction")

    def to_dict(self) -> Dict[str, Any]:
        return {"remarks": self.description,
                "amount": self.amount,
                "category": self.category
                }


transaction_parser = PydanticOutputParser(pydantic_object=Transaction)
