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


class UnauthorizedError(Exception):
    """Raised when a user is unauthorized to perform an action."""
    pass
