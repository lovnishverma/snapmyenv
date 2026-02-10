"""Custom exceptions for snapenv."""


class SnapenvError(Exception):
    """Base exception for all snapenv errors."""
    pass


class CaptureError(SnapenvError):
    """Raised when environment capture fails."""
    pass


class RestoreError(SnapenvError):
    """Raised when environment restoration fails."""
    pass


class NotebookError(SnapenvError):
    """Raised when notebook operations fail."""
    pass


class ValidationError(SnapenvError):
    """Raised when snapshot validation fails."""
    pass