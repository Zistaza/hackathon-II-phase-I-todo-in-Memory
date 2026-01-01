"""
Reminder model for the advanced todo CLI application.

This module defines the Reminder class for managing task reminders.
"""

from datetime import datetime
from typing import Optional
from dataclasses import dataclass


@dataclass
class Reminder:
    """Time-based notification associated with a task."""
    task_id: str  # Reference to the task
    reminder_time: datetime  # When to trigger the reminder
    triggered: bool = False  # Whether the reminder has been shown
    triggered_at: Optional[datetime] = None  # When the reminder was shown (optional)

    def __post_init__(self):
        """Validate reminder after initialization."""
        self._validate_task_id()
        self._validate_reminder_time()

    def _validate_task_id(self):
        """Validate task_id: must not be empty."""
        if not self.task_id or not self.task_id.strip():
            raise ValueError(f"Task ID cannot be empty, got: {self.task_id}")

    def _validate_reminder_time(self):
        """Validate reminder_time: must be in the future."""
        if self.reminder_time and self.reminder_time < datetime.now():
            raise ValueError(f"Reminder time must be in the future, got: {self.reminder_time}")

    def trigger(self):
        """Mark the reminder as triggered."""
        self.triggered = True
        self.triggered_at = datetime.now()