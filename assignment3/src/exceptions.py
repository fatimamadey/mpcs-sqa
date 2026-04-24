"""Custom exceptions for the To-Do List application."""


class TaskNotFoundError(Exception):
    """Raised when a task does not exist."""
    pass


class UnauthorizedError(Exception):
    """Raised when a user attempts to access a task they do not own."""
    pass


class UserNotFoundError(Exception):
    """Raised when a user does not exist."""
    pass


class DuplicateUserError(Exception):
    """Raised when attempting to register a username that already exists."""
    pass


class InvalidTaskError(Exception):
    """Raised when task data fails validation (e.g. blank title, bad priority)."""
    pass
