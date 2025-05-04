class EmployeeNotFoundError(Exception):
    """Raised when an employee is not found in the database."""
    pass

class DuplicateEmployeeError(Exception):
    """Raised when an employee is already in the database."""
    pass

class InvalidEmployeeDataError(Exception):
    """Raised when employee data is invalid."""
    pass

class TimeOffOverlapError(Exception):
    """Raised when a time off request overlaps in a disallowed way."""
    pass