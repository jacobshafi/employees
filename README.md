# 🧱 HR Dashboard – Architectural Overview

This project is structured with a clean separation of concerns and just enough abstraction for maintainability and extensibility—without overengineering.

---

## ✅ Employee Handling

The `EmployeeDatabase` class serves as a **Data Access Object (DAO)** for managing employee records.

A separate service layer was **not introduced** for employee logic because:

- The logic is limited to basic CRUD operations.
- There are no domain-specific business rules (e.g., validations, cross-entity dependencies).
- Adding another layer would introduce unnecessary complexity.

> This decision keeps the system clean, focused, and testable while remaining extensible should business logic grow in the future.

---

## ✅ Time Off Handling

This part of the domain uses a layered design with:

- `TimeOffDao` – handles all raw SQL/database interactions.
- `TimeOffService` – encapsulates all business rules and validation logic.

### 📌 Why this structure?

Time off management includes domain logic like:

- Preventing overlapping requests unless one is **"Work Remotely"**.
- Potential for rules such as:
  - Holiday calendars
  - Approval workflows
  - Maximum time-off limits

> By separating concerns, this part of the system is highly testable, reusable, and future-proof.

---

## 🧪 Running Tests

You can run the full test suite using the following methods from the root of the project:

### ▶️ With `pytest` (Recommended)

```bash
PYTHONPATH=. pytest
