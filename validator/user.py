# validator/user.py
import re


def validate_email(value: str) -> str:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.fullmatch(regex, value):
        raise ValueError("Invalid email format")
    return value


def validate_nickname(value: str) -> str:
    # Implement nickname validation logic (e.g., length, allowed characters)
    if not (3 <= len(value) <= 30):
        raise ValueError("Nickname must be between 3 and 30 characters")
    return value
