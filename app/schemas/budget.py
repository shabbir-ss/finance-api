from pydantic import BaseModel

class BudgetCreate(BaseModel):
    year: int
    month: int
    amount: float

class CategoryBudgetCreate(BaseModel):
    category: str
    year: int
    month: int
    amount: float
