from pydantic import BaseModel
from datetime import date

class IncomeCreate(BaseModel):
    title: str
    amount: float
    account_id: int
    received_date: date


class IncomeUpdate(BaseModel):
    title: str
    amount: float
    account_id: int
    received_date: date

class IncomeResponse(BaseModel):
    id: int
    title: str
    amount: float
    account_id: int
    received_date: date

    class Config:
        from_attributes = True
