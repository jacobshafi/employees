from setup_db import setup_database
import sqlite3
from dao.time_off_dao import TimeOffDao
from services.time_off_service import TimeOffService
from datetime import date
from uuid import uuid4
from utils.timezone import get_server_now, to_local_time
from models.employee import Employee
from db.database import EmployeeDatabase

def main() -> None:
    # Ensure DB is set up (creates tables and inserts initial data)
    setup_database(db_name="employees")
    setup_database(db_name="time_off_requests")

    # Employee DB logic
    emp_db = EmployeeDatabase(db_path="employees.db")

    emp = Employee(
        employee_id=uuid4(),
        name="Alice Johnson",
        position="Software Engineer",
        email="alice.johnson@example.com",
        salary=85000.00,
        created_at=get_server_now(),
        modified_at=get_server_now(),
    )
    emp_db.add_employee(employee=emp)

    # Display all
    print("\n📋 All Employees:")
    print(emp_db)

    print("\n👤 Retrieved Employee:")
    print(emp_db.get_employee(employee_id=emp.employee_id))

    # Time Off Request Logic
    conn = sqlite3.connect("time_off_requests.db")
    conn.row_factory = sqlite3.Row
    dao = TimeOffDao(conn)
    service = TimeOffService(dao)

    print("\n🏖️ Creating initial Annual Leave request...")
    service.create_time_off_request(
        employee_id=str(emp.employee_id),
        category_id=1,  # Annual Leave
        start_date=date(2025, 5, 10),
        end_date=date(2025, 5, 15)
    )

    print("✅ Annual Leave request created.")

    print("\n🏠 Attempting overlapping Work Remotely request...")
    service.create_time_off_request(
        employee_id=str(emp.employee_id),
        category_id=3,  # Work Remotely
        start_date=date(2025, 5, 12),
        end_date=date(2025, 5, 14)
    )

    print("✅ Work Remotely request created (overlap allowed).")

    print("\n❌ Attempting invalid overlapping Sick Leave request...")
    try:
        service.create_time_off_request(
            employee_id=str(emp.employee_id),
            category_id=2,  # Sick Leave
            start_date=date(2025, 5, 13),
            end_date=date(2025, 5, 16)
        )
    except Exception as e:
        print(f"❗ Error: {e}")

if __name__ == "__main__":
    main()
