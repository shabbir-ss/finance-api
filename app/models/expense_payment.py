from sqlalchemy import Column, BigInteger, Numeric, ForeignKey
from app.core.database import Base

class ExpensePayment(Base):
    __tablename__ = "expense_payments"

    id = Column(BigInteger, primary_key=True)
    expense_id = Column(BigInteger, ForeignKey("expenses.id"))
    account_id = Column(BigInteger, ForeignKey("accounts.id"))
    amount = Column(Numeric(12,2), nullable=False)
