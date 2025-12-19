from sqlalchemy import Column, BigInteger, String, Numeric, Date, ForeignKey
from app.core.database import Base

class Bill(Base):
    __tablename__ = "bills"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    title = Column(String(150), nullable=False)
    amount = Column(Numeric(12,2), nullable=False)
    frequency = Column(String(20), nullable=False)
    due_date = Column(Date, nullable=False)
