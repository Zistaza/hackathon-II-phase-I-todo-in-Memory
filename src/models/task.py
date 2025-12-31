from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """
    Represents a single todo task with validation and status management.

    Attributes:
        id (int): Sequential numeric ID starting from 1
        title (str): Task title (max 100 chars)
        description (Optional[str]): Optional task description (max 500 chars)
        completed (bool): Completion status (default: False)
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __post_init__(self):
        """Validate task attributes after initialization."""
        self._validate_title()
        self._validate_description()

    def _validate_title(self):
        """Validate title requirements: not empty, max 100 chars."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
        if len(self.title) > 100:
            raise ValueError(f"Task title exceeds 100 character limit: {len(self.title)} chars")

    def _validate_description(self):
        """Validate description if provided: max 500 chars."""
        if self.description and len(self.description) > 500:
            raise ValueError(f"Task description exceeds 500 character limit: {len(self.description)} chars")

    def mark_complete(self):
        """Mark the task as complete."""
        self.completed = True

    def mark_incomplete(self):
        """Mark the task as incomplete."""
        self.completed = False

    def update_title(self, new_title: str):
        """Update the task title with validation."""
        if not new_title or not new_title.strip():
            raise ValueError("Task title cannot be empty")
        if len(new_title) > 100:
            raise ValueError(f"Task title exceeds 100 character limit: {len(new_title)} chars")
        self.title = new_title

    def update_description(self, new_description: Optional[str]):
        """Update the task description with validation."""
        if new_description and len(new_description) > 500:
            raise ValueError(f"Task description exceeds 500 character limit: {len(new_description)} chars")
        self.description = new_description