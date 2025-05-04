import re

class InvalidEmailError(Exception):
    """Raised when an email is not valid."""
    pass

def validate_email(*, email: str) -> None:
    """
    Validates email format using a simple regex.
    """
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        raise InvalidEmailError(f"Invalid email: {email}")