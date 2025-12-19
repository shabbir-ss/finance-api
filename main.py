from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import accounts, income, expenses, bills, dashboard, notifications, budgets,deps,auth

app = FastAPI(title=settings.APP_NAME)

# CORS
origins = settings.CORS_ORIGINS.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "API running 🚀"}

app.include_router(auth.router, prefix=settings.API_PREFIX, tags=["Auth"])
app.include_router(accounts.router, prefix=settings.API_PREFIX, tags=["Accounts"])
app.include_router(income.router, prefix=settings.API_PREFIX, tags=["Income"])
app.include_router(expenses.router, prefix=settings.API_PREFIX, tags=["Expenses"])
app.include_router(bills.router, prefix=settings.API_PREFIX, tags=["Bills"])
app.include_router(notifications.router, prefix=settings.API_PREFIX, tags=["Notifications"])
app.include_router(budgets.router, prefix=settings.API_PREFIX, tags=["Budgets"])

# app.include_router(dashboard.router) # TODO: Add this back in when we have a frontend ready
# # app.include_router(deps.router) # TODO: Add this back in when we have a frontend ready
