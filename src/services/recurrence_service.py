"""
Recurrence service for the advanced todo CLI application.

This module provides functionality for creating recurrence patterns and calculating next occurrences.
"""

from datetime import datetime, timedelta
from typing import Optional
from ..models.task import Task, RecurrencePattern
from .datetime_utils import get_next_occurrence, get_next_weekday, add_days, add_weeks

# Import storage to ensure consistent access
import src.services.task_storage


class RecurrenceService:
    """Service class for managing recurring tasks."""

    @staticmethod
    def create_recurrence_pattern(
        pattern_type: str,
        interval: Optional[int] = None,
        days_of_week: Optional[list] = None
    ) -> RecurrencePattern:
        """
        Create a recurrence pattern object.

        Args:
            pattern_type: Type of recurrence ('daily', 'weekly', 'custom')
            interval: For custom patterns, interval in days/weeks
            days_of_week: For weekly patterns, list of days [0=Monday, 6=Sunday]

        Returns:
            RecurrencePattern: Created recurrence pattern object
        """
        pattern = RecurrencePattern(
            type=pattern_type,
            interval=interval,
            days_of_week=days_of_week
        )
        return pattern

    @staticmethod
    def calculate_next_occurrence(
        pattern: RecurrencePattern,
        last_occurrence: datetime
    ) -> datetime:
        """
        Calculate the next occurrence based on pattern.

        Args:
            pattern: Recurrence pattern to use
            last_occurrence: When the task last occurred

        Returns:
            datetime: When the next occurrence should happen
        """
        if pattern.type == "daily":
            return add_days(last_occurrence, 1)
        elif pattern.type == "weekly":
            if pattern.days_of_week:
                # If specific days of week are specified, find the next one
                return get_next_occurrence(last_occurrence, pattern.days_of_week)
            else:
                # Otherwise, just add a week
                return add_weeks(last_occurrence, 1)
        elif pattern.type == "custom":
            if pattern.interval:
                # For custom patterns, add the specified interval in days
                return add_days(last_occurrence, pattern.interval)
            else:
                # Default to daily if no interval specified
                return add_days(last_occurrence, 1)
        else:
            # Default to daily if unknown type
            return add_days(last_occurrence, 1)

    @staticmethod
    def generate_recurring_tasks() -> list:
        """
        Generate new task instances based on recurrence patterns.

        Returns:
            list: List of newly created Task objects
        """
        new_tasks = []
        current_time = datetime.now()

        # Iterate through all recurrence templates
        for task_id, template_task in list(src.services.task_storage.recurrence_templates.items()):
            if template_task.recurrence_pattern:
                pattern = template_task.recurrence_pattern

                # Check if it's time to create a new occurrence
                if pattern.next_occurrence and current_time >= pattern.next_occurrence:
                    # Create a new task instance based on the template
                    new_task = Task(
                        id=len(src.services.task_storage.tasks) + 1,  # Generate new ID
                        title=template_task.title,
                        description=template_task.description,
                        completed=False,  # New tasks start as incomplete
                        priority=template_task.priority,
                        tags=template_task.tags.copy() if template_task.tags else [],
                        due_date=template_task.due_date,
                        reminder_time=template_task.reminder_time,
                        parent_task_id=str(task_id)  # Link to the original recurring task
                    )

                    # Add to global tasks
                    src.services.task_storage.tasks[new_task.id] = new_task

                    # Calculate when the next occurrence should happen
                    pattern.next_occurrence = RecurrenceService.calculate_next_occurrence(
                        pattern, pattern.next_occurrence
                    )

                    # Update the pattern in the template task
                    template_task.recurrence_pattern = pattern

                    # Add to list of new tasks
                    new_tasks.append(new_task)

        return new_tasks

    @staticmethod
    def update_recurrence_pattern(task_id: int, new_pattern: RecurrencePattern) -> bool:
        """
        Update the recurrence pattern for a task.

        Args:
            task_id: ID of the task to update
            new_pattern: New recurrence pattern

        Returns:
            bool: True if updated, False if task not found
        """
        task_id_str = str(task_id)
        if task_id_str in src.services.task_storage.recurrence_templates:
            template_task = src.services.task_storage.recurrence_templates[task_id_str]
            template_task.recurrence_pattern = new_pattern
            return True
        return False

    @staticmethod
    def cancel_recurrence_pattern(task_id: int) -> bool:
        """
        Cancel the recurrence pattern for a task.

        Args:
            task_id: ID of the task to cancel recurrence for

        Returns:
            bool: True if canceled, False if task not found
        """
        task_id_str = str(task_id)
        if task_id_str in src.services.task_storage.recurrence_templates:
            # Remove from recurrence templates but keep the task itself
            del src.services.task_storage.recurrence_templates[task_id_str]
            # Update the task to mark it as not a recurring template anymore
            if task_id in src.services.task_storage.tasks:
                src.services.task_storage.tasks[task_id].is_recurring_template = False
                src.services.task_storage.tasks[task_id].recurrence_pattern = None
            return True
        return False