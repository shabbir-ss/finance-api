from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.income import Income
from app.models.account import Account
from app.models.user import User
from app.schemas.income import IncomeCreate, IncomeUpdate, IncomeResponse

router = APIRouter(prefix="/income", tags=["Income"])


# 🔐 GET all income (current user only)
@router.get("/", response_model=list[IncomeResponse])
def get_income(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Income)
        .filter(Income.user_id == current_user.id)
        .order_by(Income.received_date.desc())
        .all()
    )


# ➕ ADD income
@router.post("/", response_model=IncomeResponse)
def add_income(
    payload: IncomeCreate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user),
):
    account = (
        db.query(Account)
        .filter(
            Account.id == payload.account_id,
            # Account.user_id == current_user.id,
        )
        .first()
    )
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    income = Income(
        **payload.dict(),
        # user_id=current_user.id,
    )
    db.add(income)

    # 💰 Update account balance
    account.balance += payload.amount

    db.commit()
    db.refresh(income)
    return income


# ✏️ UPDATE income
@router.put("/{income_id}", response_model=IncomeResponse)
def update_income(
    income_id: int,
    payload: IncomeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    income = (
        db.query(Income)
        .filter(
            Income.id == income_id,
            Income.user_id == current_user.id,
        )
        .first()
    )
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")

    # rollback old account balance
    old_account = (
        db.query(Account)
        .filter(
            Account.id == income.account_id,
            Account.user_id == current_user.id,
        )
        .first()
    )
    if old_account:
        old_account.balance -= income.amount

    # apply new account
    new_account = (
        db.query(Account)
        .filter(
            Account.id == payload.account_id,
            Account.user_id == current_user.id,
        )
        .first()
    )
    if not new_account:
        raise HTTPException(status_code=404, detail="Account not found")

    for key, value in payload.dict().items():
        setattr(income, key, value)

    new_account.balance += payload.amount

    db.commit()
    db.refresh(income)
    return income


# 🗑️ DELETE income
@router.delete("/{income_id}")
def delete_income(
    income_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    income = (
        db.query(Income)
        .filter(
            Income.id == income_id,
            Income.user_id == current_user.id,
        )
        .first()
    )
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")

    account = (
        db.query(Account)
        .filter(
            Account.id == income.account_id,
            Account.user_id == current_user.id,
        )
        .first()
    )
    if account:
        account.balance -= income.amount

    db.delete(income)
    db.commit()

    return {"success": True}
