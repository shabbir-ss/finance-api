from sqlalchemy import Column, BigInteger, Integer, Numeric, ForeignKey
from app.core.database import Base

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    amount = Column(Numeric(12,2), nullable=False)
