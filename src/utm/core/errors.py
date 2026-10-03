"""Custom exceptions used in the project"""


class UTMError(Exception):
    """Base error for the whole package."""


class MachineDefinitionError(UTMError):
    """Raised when the Turing Machine is defined incorrectly."""


class InvalidTransitionError(MachineDefinitionError):
    """Raised when a transition is invalid."""


class TapeError(UTMError):
    """Raised on an invalid tape operation."""


class EncodingError(UTMError):
    """Raised when a machine can't be encoded."""


class DecodingError(EncodingError):
    """Raised when a string is not a valid machine encoding."""

    def __init__(self, message: str, position: int | None = None) -> None:
        self.position = position
        if position is not None:
            message = f"{message} (at position {position})"
        super().__init__(message)


class MachineLoadError(UTMError):
    """Raised when a machine file can't be loaded."""
