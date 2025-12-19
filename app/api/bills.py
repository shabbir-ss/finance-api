from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.api.deps import get_db, get_current_user
from app.models.bill import Bill
from app.models.bill_payment import BillPayment
from app.schemas.bill import BillCreate

router = APIRouter(prefix="/bills", tags=["Bills"])

@router.get("/")
def get_bills(db: Session = Depends(get_db),
              user=Depends(get_current_user)):

    bills = db.query(Bill).filter(Bill.user_id == user.id).all()

    result = []
    for b in bills:
        payments = db.query(BillPayment).filter(
            BillPayment.bill_id == b.id
        ).all()

        result.append({
            "id": b.id,
            "title": b.title,
            "amount": float(b.amount),
            "frequency": b.frequency,
            "due_date": b.due_date,
            "history": [
                {
                    "id": p.id,
                    "paid_on": p.paid_on,
                    "amount": float(p.amount)
                } for p in payments
            ]
        })

    return result

@router.get("/")
def get_bills(db: Session = Depends(get_db),
              user=Depends(get_current_user)):

    bills = db.query(Bill).filter(Bill.user_id == user.id).all()

    result = []
    for b in bills:
        payments = db.query(BillPayment).filter(
            BillPayment.bill_id == b.id
        ).all()

        result.append({
            "id": b.id,
            "title": b.title,
            "amount": float(b.amount),
            "frequency": b.frequency,
            "due_date": b.due_date,
            "history": [
                {
                    "id": p.id,
                    "paid_on": p.paid_on,
                    "amount": float(p.amount)
                } for p in payments
            ]
        })

    return result

@router.post("/")
def create_bill(payload: BillCreate,
                db: Session = Depends(get_db),
                user=Depends(get_current_user)):

    bill = Bill(
        user_id=user.id,
        title=payload.title,
        amount=payload.amount,
        frequency=payload.frequency,
        due_date=payload.due_date
    )

    db.add(bill)
    db.commit()
    return {"message": "Bill created"}

@router.post("/{bill_id}/pay")
def mark_bill_paid(bill_id: int,
                   db: Session = Depends(get_db),
                   user=Depends(get_current_user)):

    bill = db.query(Bill).filter_by(
        id=bill_id,
        user_id=user.id
    ).first()

    if not bill:
        return {"error": "Bill not found"}

    payment = BillPayment(
        bill_id=bill.id,
        paid_on=date.today(),
        amount=bill.amount
    )

    db.add(payment)
    db.commit()

    return {"message": "Bill marked as paid"}


@router.delete("/{bill_id}")
def delete_bill(bill_id: int,
                db: Session = Depends(get_db),
                user=Depends(get_current_user)):

    db.query(Bill).filter_by(
        id=bill_id,
        user_id=user.id
    ).delete()

    db.commit()
    return {"message": "Bill deleted"}
