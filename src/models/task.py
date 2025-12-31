from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class Task:
    """
    Represents a single todo task with validation and status management.

    Attributes:
        id (int): Sequential numeric ID starting from 1
        title (str): Task title (max 100 chars)
        description (Optional[str]): Optional task description (max 500 chars)
        completed (bool): Completion status (default: False)
        priority (str): Task priority level ('high', 'medium', 'low') (default: 'medium')
        tags (List[str]): List of tags/categories for the task (default: empty list)
        created_at (datetime): Timestamp of when task was created (immutable)
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"
    tags: List[str] = None
    created_at: datetime = None

    def __post_init__(self):
        """Validate task attributes after initialization."""
        # Initialize mutable defaults
        if self.tags is None:
            self.tags = []
        if self.created_at is None:
            self.created_at = datetime.now()

        self._validate_title()
        self._validate_description()
        self._validate_priority()
        self._validate_tags()

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

    def _validate_priority(self):
        """Validate priority requirements: must be one of 'high', 'medium', 'low'."""
        valid_priorities = ['high', 'medium', 'low']
        if self.priority not in valid_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}, got: {self.priority}")

    def _validate_tags(self):
        """Validate tags requirements: each tag must be non-empty and contain no spaces."""
        for tag in self.tags:
            if not tag or not tag.strip():
                raise ValueError(f"Tag cannot be empty: '{tag}'")
            if ' ' in tag:
                raise ValueError(f"Tag cannot contain spaces: '{tag}'")

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

    def update_priority(self, new_priority: str):
        """Update the task priority with validation."""
        valid_priorities = ['high', 'medium', 'low']
        if new_priority not in valid_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}, got: {new_priority}")
        self.priority = new_priority

    def update_tags(self, new_tags: List[str]):
        """Update the task tags with validation."""
        for tag in new_tags:
            if not tag or not tag.strip():
                raise ValueError(f"Tag cannot be empty: '{tag}'")
            if ' ' in tag:
                raise ValueError(f"Tag cannot contain spaces: '{tag}'")
        self.tags = new_tags

    def add_tag(self, tag: str):
        """Add a single tag to the task."""
        if not tag or not tag.strip():
            raise ValueError(f"Tag cannot be empty: '{tag}'")
        if ' ' in tag:
            raise ValueError(f"Tag cannot contain spaces: '{tag}'")
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str):
        """Remove a single tag from the task."""
        if tag in self.tags:
            self.tags.remove(tag)