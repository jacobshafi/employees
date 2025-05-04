import unittest
import sqlite3
from datetime import date
from dao.time_off_dao import TimeOffDao
from services.time_off_service import TimeOffService
from utils.exceptions import TimeOffOverlapError

class TestTimeOffService(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript("""
            CREATE TABLE request_category (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            );

            CREATE TABLE time_off_request (
                id INTEGER PRIMARY KEY,
                request_category_id INTEGER,
                employee_id TEXT,
                start_date TEXT,
                end_date TEXT,
                FOREIGN KEY (request_category_id) REFERENCES request_category(id)
            );

            INSERT INTO request_category (id, name) VALUES
            (1, 'Annual Leave'),
            (2, 'Work Remotely');
        """)
        self.dao = TimeOffDao(self.conn)
        self.service = TimeOffService(self.dao)

    def test_valid_non_overlapping_request(self):
        self.service.create_time_off_request(
            employee_id="emp123",
            category_id=1,
            start_date=date(2025, 6, 1),
            end_date=date(2025, 6, 3)
        )

    def test_invalid_overlap_both_non_remote(self):
        self.service.create_time_off_request(
            employee_id="emp456",
            category_id=1,
            start_date=date(2025, 6, 1),
            end_date=date(2025, 6, 3)
        )
        with self.assertRaises(TimeOffOverlapError):
            self.service.create_time_off_request(
                employee_id="emp456",
                category_id=1,
                start_date=date(2025, 6, 2),
                end_date=date(2025, 6, 4)
            )

    def test_valid_overlap_with_remote(self):
        self.service.create_time_off_request(
            employee_id="emp789",
            category_id=2,
            start_date=date(2025, 6, 10),
            end_date=date(2025, 6, 12)
        )
        self.service.create_time_off_request(
            employee_id="emp789",
            category_id=1,
            start_date=date(2025, 6, 10),
            end_date=date(2025, 6, 12)
        )