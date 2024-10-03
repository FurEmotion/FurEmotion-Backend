class ValidationError(Exception):
    """Base class for validation errors."""
    pass


class InvalidSpeciesError(ValidationError):
    """Raised when the species is invalid."""
    pass


class NegativeAgeError(ValidationError):
    """Raised when the age is negative."""
    pass
