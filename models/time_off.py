from dataclasses import dataclass
from datetime import date


@dataclass
class TimeOffCategory:
    id: int
    name: str


@dataclass
class TimeOffRequest:
    id: int
    request_category_id: int
    employee_id: str
    start_date: date
    end_date: date