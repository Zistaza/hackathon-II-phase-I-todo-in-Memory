class TaskNotFoundError(Exception):
    """Raised when a task with a given ID is not found."""
    pass


class TaskValidationError(Exception):
    """Raised when task validation fails."""
    pass