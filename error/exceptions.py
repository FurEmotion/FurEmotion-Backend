# error/exceptions.py
class ValidationError(Exception):
    """General validation error."""
    pass


class NegativeAgeError(ValidationError):
    """Raised when the age is negative."""
    pass


class InvalidSpeciesError(ValidationError):
    """Raised when the species is invalid."""
    pass


class PetNotFoundError(Exception):
    """Raised when a pet is not found."""
    pass


class UserNotFoundError(Exception):
    """Raised when a user is not found."""
    pass


class UnauthorizedError(Exception):
    """Raised when a user is not authorized to perform an action."""
    pass


class DuplicateEmailError(Exception):
    """Raised when attempting to create a user with an email that already exists."""
    pass


class DuplicateUidError(Exception):
    """Raised when attempting to create a user with an uid that already exists."""
    pass
