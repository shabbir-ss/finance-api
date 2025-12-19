from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.notification import Notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/")
def get_notifications(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    return notifications

@router.get("/unread-count")
def unread_count(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    count = (
        db.query(Notification)
        .filter(
            Notification.user_id == user.id,
            Notification.is_read == False
        )
        .count()
    )

    return count

@router.patch("/mark-read/{id}")
def mark_read(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    notif = (
        db.query(Notification)
        .filter(
            Notification.id == id,
            Notification.user_id == user.id
        )
        .first()
    )

    if notif:
        notif.is_read = True
        db.commit()

    return {"message": "Notification marked as read"}

def create_bill_notification(db, user_id, bill):
    notif = Notification(
        user_id=user_id,
        title="Bill Due Reminder",
        message=f"{bill.title} is due on {bill.due_date}",
        type="bill"
    )
    db.add(notif)
    db.commit()
    
def create_budget_alert(db, user_id, category, spent, limit):
    notif = Notification(
        user_id=user_id,
        title="Budget Alert",
        message=f"{category} budget exceeded (₹{spent} / ₹{limit})",
        type="budget"
    )
    db.add(notif)
    db.commit()

