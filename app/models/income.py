from sqlalchemy import Column, BigInteger, String, Numeric, Date, ForeignKey
from app.core.database import Base

class Income(Base):
    __tablename__ = "income"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    account_id = Column(BigInteger, ForeignKey("accounts.id"))
    title = Column(String(150), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    received_date = Column(Date, nullable=False)
