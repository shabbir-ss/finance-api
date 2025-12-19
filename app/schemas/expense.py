from pydantic import BaseModel
from datetime import date
from typing import List

class ExpensePaymentCreate(BaseModel):
    account_id: int
    amount: float

class ExpenseCreate(BaseModel):
    title: str
    category: str
    total_amount: float
    expense_date: date
    notes: str | None = None
    payments: List[ExpensePaymentCreate]

class ExpenseResponse(BaseModel):
    id: int
    title: str
    category: str
    total_amount: float
    expense_date: date
    payments: list

    class Config:
        orm_mode = True
