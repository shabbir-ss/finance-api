from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.budget import Budget
from app.models.category_budget import CategoryBudget
from app.schemas.budget import BudgetCreate, CategoryBudgetCreate

router = APIRouter(prefix="/budgets", tags=["Budgets"])

@router.get("/")
def get_budgets(db: Session = Depends(get_db),
                user=Depends(get_current_user)):

    global_budgets = db.query(Budget).filter(
        Budget.user_id == user.id
    ).all()

    category_budgets = db.query(CategoryBudget).filter(
        CategoryBudget.user_id == user.id
    ).all()

    return {
        "globalBudgets": [
            {
                "year": b.year,
                "month": str(b.month).zfill(2),
                "amount": float(b.amount)
            } for b in global_budgets
        ],
        "categoryBudgets": [
            {
                "id": c.id,
                "category": c.category,
                "year": c.year,
                "month": str(c.month).zfill(2),
                "amount": float(c.amount)
            } for c in category_budgets
        ]
    }


@router.post("/global")
def set_global_budget(payload: BudgetCreate,
                      db: Session = Depends(get_db),
                      user=Depends(get_current_user)):

    budget = db.query(Budget).filter_by(
        user_id=user.id,
        year=payload.year,
        month=payload.month
    ).first()

    if budget:
        budget.amount = payload.amount
    else:
        budget = Budget(
            user_id=user.id,
            year=payload.year,
            month=payload.month,
            amount=payload.amount
        )
        db.add(budget)

    db.commit()
    return {"message": "Global budget saved"}

@router.post("/category")
def set_category_budget(payload: CategoryBudgetCreate,
                        db: Session = Depends(get_db),
                        user=Depends(get_current_user)):

    budget = db.query(CategoryBudget).filter_by(
        user_id=user.id,
        category=payload.category,
        year=payload.year,
        month=payload.month
    ).first()

    if budget:
        budget.amount = payload.amount
    else:
        budget = CategoryBudget(
            user_id=user.id,
            category=payload.category,
            year=payload.year,
            month=payload.month,
            amount=payload.amount
        )
        db.add(budget)

    db.commit()
    return {"message": "Category budget saved"}

@router.post("/category")
def set_category_budget(payload: CategoryBudgetCreate,
                        db: Session = Depends(get_db),
                        user=Depends(get_current_user)):

    budget = db.query(CategoryBudget).filter_by(
        user_id=user.id,
        category=payload.category,
        year=payload.year,
        month=payload.month
    ).first()

    if budget:
        budget.amount = payload.amount
    else:
        budget = CategoryBudget(
            user_id=user.id,
            category=payload.category,
            year=payload.year,
            month=payload.month,
            amount=payload.amount
        )
        db.add(budget)

    db.commit()
    return {"message": "Category budget saved"}

@router.delete("/global/{year}/{month}")
def delete_global_budget(year: int, month: int,
                         db: Session = Depends(get_db),
                         user=Depends(get_current_user)):

    db.query(Budget).filter_by(
        user_id=user.id,
        year=year,
        month=month
    ).delete()

    db.commit()
    return {"message": "Global budget removed"}

