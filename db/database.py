import sqlite3
from uuid import UUID
from datetime import datetime
from typing import Optional
from models.employee import Employee
from utils.validators import validate_email
from utils.timezone import to_local_time
from utils.db_utils import create_all_tables


class EmployeeDatabase:
    # When we call Employee Database, we want to create a new database
    def __init__(self, *, db_path: str = "employees.db") -> None:
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
     

    def add_employee(self, *, employee: Employee) -> None:
        validate_email(email=employee.email) # First we want to validate the email before we add the employee
        with self._conn:
            try:
                self._conn.execute("""
                    INSERT INTO employees (
                        employee_id, name, position, email, salary, created_at, modified_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                str(employee.employee_id),
                employee.name,
                employee.position,
                employee.email,
                employee.salary,
                employee.created_at.isoformat(),
                employee.modified_at.isoformat()
            ))
            except sqlite3.IntegrityError:
                raise DuplicateEmployeeError("Employee already exists")

    def update_employee(self, *, employee: Employee) -> None:
        validate_email(email=employee.email)
        with self._conn:
            cur = self._conn.execute("""
                UPDATE employees
                SET name = ?, position = ?, email = ?, salary = ?, modified_at = ?
                WHERE employee_id = ?
            """, (
                employee.name,
                employee.position,
                employee.email,
                employee.salary,
                employee.modified_at.isoformat(),
                str(employee.employee_id)
            ))
            if cur.rowcount == 0:
                raise EmployeeNotFoundError("Employee not found")

    def get_employee(self, *, employee_id: UUID) -> Employee:
        cur = self._conn.execute("SELECT * FROM employees WHERE employee_id = ?", (str(employee_id),))
        row = cur.fetchone()
        if row is None:
            raise EmployeeNotFoundError("Employee not found")
        return self._row_to_employee(row)

    def get_all(self) -> list[Employee]:
        cur = self._conn.execute("SELECT * FROM employees")
        return [self._row_to_employee(row) for row in cur.fetchall()]

    def __str__(self) -> str:
        return "\n".join(str(emp) for emp in self.get_all())

    def _row_to_employee(self, row: sqlite3.Row) -> Employee:
        return Employee(
            employee_id=UUID(row["employee_id"]),
            name=row["name"],
            position=row["position"],
            email=row["email"],
            salary=row["salary"],
            created_at=to_local_time(dt=datetime.fromisoformat(row["created_at"])),
            modified_at=to_local_time(dt=datetime.fromisoformat(row["modified_at"])),
        )
