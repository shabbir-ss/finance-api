from pydantic import BaseModel
from datetime import date

class BillCreate(BaseModel):
    title: str
    amount: float
    frequency: str
    due_date: date

class BillPaymentCreate(BaseModel):
    amount: float
    paid_on: date
