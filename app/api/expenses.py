from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.expense import Expense
from app.models.expense_payment import ExpensePayment
from app.models.account import Account
from app.schemas.expense import ExpenseCreate

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.get("/")
def list_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).order_by(Expense.expense_date.desc()).all()

@router.post("/")
def add_expense(payload: ExpenseCreate, db: Session = Depends(get_db)):
    paid_total = sum(p.amount for p in payload.payments)

    if paid_total != payload.total_amount:
        raise HTTPException(
            status_code=400,
            detail="Payment split total must match expense amount"
        )

    expense = Expense(
        title=payload.title,
        category=payload.category,
        total_amount=payload.total_amount,
        expense_date=payload.expense_date,
        notes=payload.notes
    )
    db.add(expense)
    db.flush()  # get expense.id

    for p in payload.payments:
        account = db.query(Account).filter(Account.id == p.account_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        if account.balance < p.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        account.balance -= p.amount

        db.add(ExpensePayment(
            expense_id=expense.id,
            account_id=p.account_id,
            amount=p.amount
        ))

    db.commit()
    return {"message": "Expense added successfully", "id": expense.id}

@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    payments = db.query(ExpensePayment).filter(
        ExpensePayment.expense_id == expense_id
    ).all()

    for p in payments:
        account = db.query(Account).filter(Account.id == p.account_id).first()
        if account:
            account.balance += p.amount

    db.query(ExpensePayment).filter(
        ExpensePayment.expense_id == expense_id
    ).delete()

    db.delete(expense)
    db.commit()

    return {"message": "Expense deleted"}
