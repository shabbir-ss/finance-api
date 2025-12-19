from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class IncomeCreate(BaseModel):
    title: str
    amount: Decimal
    account_id: int
    received_date: date   # 🔥 REQUIRED

class IncomeUpdate(IncomeCreate):
    pass

class IncomeResponse(BaseModel):
    id: int
    title: str
    amount: Decimal
    account_id: int
    received_date: date

    class Config:
        from_attributes = True
