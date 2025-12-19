from sqlalchemy import Column, BigInteger, Numeric, Date, ForeignKey
from app.core.database import Base

class BillPayment(Base):
    __tablename__ = "bill_payments"

    id = Column(BigInteger, primary_key=True)
    bill_id = Column(BigInteger, ForeignKey("bills.id"))
    paid_on = Column(Date, nullable=False)
    amount = Column(Numeric(12,2), nullable=False)
