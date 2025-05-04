🧱 Architectural Decisions
This project follows clean separation of concerns, with just enough abstraction for maintainability and extensibility — but without overengineering.

✅ Employee Handling
EmployeeDatabase serves as a simple data access object (DAO).

A separate service layer is not introduced for employees because:

The logic is limited to basic CRUD (create, read, update).

There are no domain-specific business rules (e.g., validations, cross-entity dependencies).

Adding another layer would create unnecessary complexity.

This design keeps the system clean, focused, and testable while still being extensible if business logic grows in the future.

✅ Time Off Handling
A full TimeOffService + TimeOffDao pattern is used.

Reasoning:

This part of the domain has explicit business rules, such as:

Overlapping requests are only allowed if one is "Work Remotely"

More complex rules could be added in the future (e.g., holiday calendars, maximum days off, approval workflows).

Separating concerns makes the logic testable, reusable, and independent of database access details.

TimeOffDao handles all SQL/database logic, while TimeOffService focuses purely on business decisions.

## 🧪 Running Tests

To run all tests in this project, use one of the following methods from the project root directory:

**With `pytest` (recommended):**
```bash
PYTHONPATH=. pytest
```
- This will discover and run all tests in the `tests/` directory.
- Make sure you have `pytest` installed:
  ```bash
  pip install pytest
  ```

**With `unittest` (built-in):**
```bash
python -m unittest discover
```
- This will also discover and run all tests, but `pytest` is recommended for better output and flexibility.

**Note:**  
If you add new modules or packages, ensure each directory contains an empty `__init__.py` file so Python recognizes them as packages.