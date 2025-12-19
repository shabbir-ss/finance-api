# 📊 Personal Finance Management System
## Full PostgreSQL Database Builder Script

> This script creates a **production-ready schema** for:
- Authentication & Users
- Accounts
- Income
- Expenses (multi-account ready)
- Budgets (global & category)
- Bills & Reminders
- Notifications
- Savings
- Assets

---

## 🔹 EXTENSIONS
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

---

## 🔹 USERS & AUTH
```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔹 ACCOUNTS
```sql
CREATE TABLE accounts (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL, -- bank, wallet, cash, credit
    balance NUMERIC(12,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔹 INCOME
```sql
CREATE TABLE income (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    account_id BIGINT REFERENCES accounts(id),
    title VARCHAR(150),
    amount NUMERIC(12,2) NOT NULL,
    received_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔹 EXPENSES
```sql
CREATE TABLE expenses (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(150),
    category VARCHAR(100),
    total_amount NUMERIC(12,2) NOT NULL,
    expense_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 🔹 Expense Payments (Multi-Account Split)
```sql
CREATE TABLE expense_payments (
    id BIGSERIAL PRIMARY KEY,
    expense_id BIGINT REFERENCES expenses(id) ON DELETE CASCADE,
    account_id BIGINT REFERENCES accounts(id),
    amount NUMERIC(12,2) NOT NULL
);
```

---

## 🔹 BUDGETS

### Global Monthly Budgets
```sql
CREATE TABLE budgets_global (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    year INT NOT NULL,
    month INT NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    UNIQUE(user_id, year, month)
);
```

### Category Budgets
```sql
CREATE TABLE budgets_category (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    category VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    amount NUMERIC(12,2) NOT NULL
);
```

---

## 🔹 BILLS & REMINDERS
```sql
CREATE TABLE bills (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(150) NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    due_date DATE NOT NULL,
    frequency VARCHAR(20), -- monthly, yearly
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Bill Payment History
```sql
CREATE TABLE bill_payments (
    id BIGSERIAL PRIMARY KEY,
    bill_id BIGINT REFERENCES bills(id) ON DELETE CASCADE,
    paid_on DATE NOT NULL,
    amount NUMERIC(12,2) NOT NULL
);
```

---

## 🔹 SAVINGS
```sql
CREATE TABLE savings (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(150),
    amount NUMERIC(12,2),
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔹 ASSETS
```sql
CREATE TABLE assets (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(150),
    value NUMERIC(14,2),
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔹 NOTIFICATIONS
```sql
CREATE TABLE notifications (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50), -- bill, budget, expense, system
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔹 INDEXES (Performance)
```sql
CREATE INDEX idx_expenses_user_date ON expenses(user_id, expense_date);
CREATE INDEX idx_income_user_date ON income(user_id, received_date);
CREATE INDEX idx_notifications_user_read ON notifications(user_id, is_read);
```

---

## ✅ WHAT THIS DESIGN SUPPORTS
✔ Multi-account expense payments
✔ Budget vs actual analytics
✔ Bill reminders & alerts
✔ Notification system
✔ Clean dashboard aggregations
✔ Scales to mobile & web

---

## 🔜 NEXT STEPS
- Generate **FastAPI CRUD APIs** for all modules
- Add **database views** for dashboard analytics
- Add **triggers** for auto notifications

---

If you want next:
- **G → Full FastAPI CRUD APIs**
- **H → Analytics SQL Views**
- **I → Auth + JWT + RBAC**

