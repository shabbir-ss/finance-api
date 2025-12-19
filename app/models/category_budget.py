from sqlalchemy import Column, BigInteger, Integer, Numeric, String, ForeignKey
from app.core.database import Base

class CategoryBudget(Base):
    __tablename__ = "category_budgets"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    category = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    amount = Column(Numeric(12,2), nullable=False)
