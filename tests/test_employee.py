import unittest
from uuid import uuid4
from datetime import datetime
from models.employee import Employee
from db.database import EmployeeDatabase
from utils.timezone import get_server_now
from utils.validators import InvalidEmailError
from utils.db_utils import create_all_tables

class TestEmployeeDatabase(unittest.TestCase):
    def setUp(self):
        self.db = EmployeeDatabase(db_path=":memory:")
        create_all_tables(self.db._conn, db_name="employees")  # <--- Add this

    def test_create_employee_and_retrieve(self):
        employee = Employee(
            employee_id=uuid4(),
            name="John Doe",
            position="Developer",
            email="john@example.com",
            salary=90000.0,
            created_at=get_server_now(),
            modified_at=get_server_now()
        )
        self.db.add_employee(employee=employee)
        retrieved = self.db.get_employee(employee_id=employee.employee_id)
        self.assertEqual(retrieved.name, "John Doe")
        self.assertEqual(retrieved.email, "john@example.com")

    def test_invalid_email(self):
        employee = Employee(
            employee_id=uuid4(),
            name="Invalid Email",
            position="Engineer",
            email="not-an-email",
            salary=75000.0,
            created_at=get_server_now(),
            modified_at=get_server_now()
        )

        with self.assertRaises(InvalidEmailError):
            self.db.add_employee(employee=employee)