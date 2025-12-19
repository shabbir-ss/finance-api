from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate, AccountResponse
from app.models.user import User

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.get("/", response_model=list[AccountResponse])
def get_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Account).filter(Account.user_id == current_user.id).all()


@router.post("/", response_model=AccountResponse)
def create_account(
    payload: AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    acc = Account(
        **payload.dict(),
        user_id=current_user.id,
    )
    db.add(acc)
    db.commit()
    db.refresh(acc)
    return acc


@router.put("/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: int,
    payload: AccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    acc = (
        db.query(Account)
        .filter(
            Account.id == account_id,
            Account.user_id == current_user.id,
        )
        .first()
    )

    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")

    for key, value in payload.dict().items():
        setattr(acc, key, value)

    db.commit()
    db.refresh(acc)
    return acc


@router.delete("/{account_id}")
def delete_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    acc = (
        db.query(Account)
        .filter(
            Account.id == account_id,
            Account.user_id == current_user.id,
        )
        .first()
    )

    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")

    db.delete(acc)
    db.commit()
    return {"success": True}


@router.post("/transfer")
def transfer_money(
    from_id: int,
    to_id: int,
    amount: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from_acc = (
        db.query(Account)
        .filter(
            Account.id == from_id,
            Account.user_id == current_user.id,
        )
        .first()
    )

    to_acc = (
        db.query(Account)
        .filter(
            Account.id == to_id,
            Account.user_id == current_user.id,
        )
        .first()
    )

    if not from_acc or not to_acc:
        raise HTTPException(status_code=404, detail="Account not found")

    if from_acc.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    from_acc.balance -= amount
    to_acc.balance += amount

    db.commit()
    return {"success": True}
