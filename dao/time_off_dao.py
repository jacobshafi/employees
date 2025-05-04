import sqlite3
from datetime import date
from typing import Any
from models.time_off import TimeOffRequest, TimeOffCategory
from datetime import datetime


class TimeOffDao:
    """
    Data Access Object for interacting with time_off_request and request_category tables.
    Handles raw SQL operations only. Business logic lives in TimeOffService.
    """

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def get_category(self, *, category_id: int) -> TimeOffCategory:
        result = self._conn.execute(
            "SELECT id, name FROM request_category WHERE id = ?",
            (category_id,)
        ).fetchone()

        if result is None:
            raise ValueError(f"No category found with id {category_id}")

        return TimeOffCategory(id=result["id"], name=result["name"])     

    def get_overlapping_requests(
        self,
        *,
        employee_id: str,
        start: date,
        end: date
    ) -> list[TimeOffRequest]:
        rows = self._conn.execute("""
            SELECT r.id, r.request_category_id, r.employee_id, r.start_date, r.end_date
            FROM time_off_request r
            WHERE r.employee_id = ?
            AND NOT (r.end_date < ? OR r.start_date > ?)
        """, (
            employee_id,
            start.isoformat(),
            end.isoformat()
        )).fetchall()

        return [
            TimeOffRequest(
                id=row["id"],
                request_category_id=row["request_category_id"],
                employee_id=row["employee_id"],
                start_date=datetime.strptime(row["start_date"], "%Y-%m-%d").date(),
                end_date=datetime.strptime(row["end_date"], "%Y-%m-%d").date(),
            )
            for row in rows
        ]
    def insert_time_off_request(
        self,
        *,
        employee_id: str,
        category_id: int,
        start: date,
        end: date
    ) -> None:
        self._conn.execute("""
            INSERT INTO time_off_request (
                request_category_id, employee_id, start_date, end_date
            ) VALUES (?, ?, ?, ?)
        """, (
            category_id,
            employee_id,
            start.isoformat(),
            end.isoformat()
        ))
        self._conn.commit()