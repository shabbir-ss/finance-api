from sqlalchemy import Column, BigInteger, String, Numeric, Date, Text, ForeignKey
from app.core.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    category = Column(String(100), nullable=False)
    title = Column(String(150))
    total_amount = Column(Numeric(12,2), nullable=False)
    expense_date = Column(Date, nullable=False)
    notes = Column(Text)
