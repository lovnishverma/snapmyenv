"""Custom exceptions for Snapmyenv."""


class SnapmyenvError(Exception):
    """Base exception for all Snapmyenv errors."""
    pass


class CaptureError(SnapmyenvError):
    """Raised when environment capture fails."""
    pass


class RestoreError(SnapmyenvError):
    """Raised when environment restoration fails."""
    pass


class NotebookError(SnapmyenvError):
    """Raised when notebook operations fail."""
    pass


class ValidationError(SnapmyenvError):
    """Raised when snapshot validation fails."""
    pass