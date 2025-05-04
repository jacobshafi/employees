from typing import Final
from uuid import UUID, uuid4
from datetime import datetime
from utils.exceptions import InvalidEmployeeDataError
from utils.timezone import to_local_time
class Employee:
    """
    Represents an employee with immutable attributes.
    """

    def __init__(
        self,
        *,
        employee_id: Final[UUID],
        name: Final[str],
        position: Final[str],
        email: Final[str],
        salary: Final[float],
        created_at: Final[datetime],
        modified_at: Final[datetime]
    ) -> None:
        if not name:
            raise InvalidEmployeeDataError("Name cannot be empty")
        if salary <= 0:
            raise InvalidEmployeeDataError("Salary must be positive")
        self._employee_id: Final[UUID] = employee_id
        self._name: Final[str] = name
        self._position: Final[str] = position
        self._email: Final[str] = email
        self._salary: Final[float] = salary
        self._created_at: Final[datetime] = created_at
        self._modified_at: Final[datetime] = modified_at

    @property
    def employee_id(self) -> UUID:
        return self._employee_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def position(self) -> str:
        return self._position

    @property
    def email(self) -> str:
        return self._email

    @property
    def salary(self) -> float:
        return self._salary

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def modified_at(self) -> datetime:
        return self._modified_at

    def __str__(self) -> str:
        return (
            f"Employee:\n"
            f"  ID:        {self.employee_id}\n"
            f"  Name:      {self.name}\n"
            f"  Position:  {self.position}\n"
            f"  Email:     {self.email}\n"
            f"  Salary:    ${self.salary:,.2f}\n"
            f"  Created:   {to_local_time(self.created_at)}\n"
            f"  Modified:  {to_local_time(self.modified_at)}"
        )