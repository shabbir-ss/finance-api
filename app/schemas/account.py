from pydantic import BaseModel

class AccountBase(BaseModel):
    name: str
    type: str
    balance: float

class AccountCreate(AccountBase):
    pass

class AccountUpdate(AccountBase):
    pass

class AccountResponse(AccountBase):
    id: int

    class Config:
        from_attributes = True
