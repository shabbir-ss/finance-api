from sqlalchemy import Column, BigInteger, String, Numeric, ForeignKey
from app.core.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    name = Column(String(100))
    type = Column(String(50))
    balance = Column(Numeric(12, 2), default=0)
