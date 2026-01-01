"""
Recurrence pattern model for the advanced todo CLI application.

This module defines the RecurrencePattern class for managing recurring tasks.
"""

from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class RecurrencePattern:
    """Defines the schedule for task repetition."""
    type: str  # "daily", "weekly", "custom"
    interval: Optional[int] = None  # For custom: every N days/weeks
    days_of_week: Optional[List[int]] = None  # For weekly: [0,1,2,3,4] for Mon-Fri
    end_date: Optional[datetime] = None  # Optional end date for recurrence
    max_occurrences: Optional[int] = None  # Optional limit on number of occurrences
    next_occurrence: Optional[datetime] = None  # When the next instance should be created

    def __post_init__(self):
        """Validate recurrence pattern after initialization."""
        self._validate_type()
        self._validate_interval()
        self._validate_days_of_week()
        self._validate_end_date()
        self._validate_max_occurrences()

    def _validate_type(self):
        """Validate recurrence type: must be one of allowed values."""
        valid_types = ["daily", "weekly", "custom"]
        if self.type not in valid_types:
            raise ValueError(f"Recurrence type must be one of: {', '.join(valid_types)}, got: {self.type}")

    def _validate_interval(self):
        """Validate interval: must be positive if type is 'custom'."""
        if self.type == "custom" and (self.interval is None or self.interval <= 0):
            raise ValueError(f"Custom recurrence requires positive interval, got: {self.interval}")

    def _validate_days_of_week(self):
        """Validate days_of_week: values must be 0-6 if type is 'weekly'."""
        if self.type == "weekly" and self.days_of_week:
            for day in self.days_of_week:
                if not 0 <= day <= 6:
                    raise ValueError(f"Day of week must be 0-6 (Monday=0, Sunday=6), got: {day}")

    def _validate_end_date(self):
        """Validate end_date: must be in the future (if specified)."""
        if self.end_date and self.end_date < datetime.now():
            raise ValueError(f"End date must be in the future, got: {self.end_date}")

    def _validate_max_occurrences(self):
        """Validate max_occurrences: must be positive (if specified)."""
        if self.max_occurrences and self.max_occurrences <= 0:
            raise ValueError(f"Max occurrences must be positive, got: {self.max_occurrences}")