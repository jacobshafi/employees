import unittest
import sqlite3
from datetime import date
from dao.time_off_dao import TimeOffDao

class TestTimeOffDao(unittest.TestCase):
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

            INSERT INTO request_category (id, name) VALUES (1, 'Annual Leave'), (2, 'Work Remotely');
        """)
        self.dao = TimeOffDao(self.conn)

    def test_get_category_name(self):
        category = self.dao.get_category(category_id=1)
        self.assertEqual(category.name, "Annual Leave")

    def test_insert_and_retrieve_overlap(self):
        self.dao.insert_time_off_request(
            employee_id="emp1",
            category_id=1,
            start=date(2025, 5, 1),
            end=date(2025, 5, 3)
        )
        overlaps = self.dao.get_overlapping_requests(
            employee_id="emp1",
            start=date(2025, 5, 2),
            end=date(2025, 5, 4)
        )
        self.assertEqual(len(overlaps), 1)