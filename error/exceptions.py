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


class WrongFileTypeError(Exception):
    """Raised when a file is of the wrong type."""
    pass


class WavFileNotFoundError(Exception):
    """Raised when a wav file is not found."""
    pass


class WrongCryOfSpeciesError(Exception):
    """Raised when a cry of a wrong species is found."""
    pass


class CryNotFoundError(Exception):
    """Raised when a cry is not found."""
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
