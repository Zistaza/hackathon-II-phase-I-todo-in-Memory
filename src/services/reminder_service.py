"""
Reminder service for the advanced todo CLI application.

This module provides functionality for checking and triggering reminders.
"""

from datetime import datetime
from typing import List
from ..models.task import Task
from ..models.reminder import Reminder
from .task_storage import tasks, reminders
from .task_service import TaskService


class ReminderService:
    """Service class for managing task reminders."""

    @staticmethod
    def check_and_trigger_reminders() -> List[Reminder]:
        """
        Check for reminders that should be triggered.

        Returns:
            List[Reminder]: List of triggered reminders
        """
        triggered_reminders = []
        current_time = datetime.now()

        # Iterate through all reminders
        for task_id, reminder in list(reminders.items()):
            # Check if the reminder time has passed and it hasn't been triggered yet
            if not reminder.triggered and reminder.reminder_time <= current_time:
                # Trigger the reminder
                reminder.trigger()
                triggered_reminders.append(reminder)

        return triggered_reminders

    @staticmethod
    def add_reminder_for_task(task_id: int, reminder_time: datetime) -> bool:
        """
        Add a reminder for a specific task.

        Args:
            task_id: ID of the task to add reminder for
            reminder_time: When the reminder should trigger

        Returns:
            bool: True if reminder was added, False if task not found
        """
        if task_id not in tasks:
            return False

        # Create a new reminder
        reminder = Reminder(
            task_id=str(task_id),
            reminder_time=reminder_time
        )

        # Add to global reminders storage
        reminders[str(task_id)] = reminder
        return True

    @staticmethod
    def remove_reminder_for_task(task_id: int) -> bool:
        """
        Remove a reminder for a specific task.

        Args:
            task_id: ID of the task to remove reminder for

        Returns:
            bool: True if reminder was removed, False if not found
        """
        if str(task_id) in reminders:
            del reminders[str(task_id)]
            return True
        return False

    @staticmethod
    def get_upcoming_reminders() -> List[Reminder]:
        """
        Get all upcoming (not yet triggered) reminders.

        Returns:
            List[Reminder]: List of upcoming reminders
        """
        current_time = datetime.now()
        upcoming_reminders = []

        for reminder in reminders.values():
            if not reminder.triggered and reminder.reminder_time > current_time:
                upcoming_reminders.append(reminder)

        return upcoming_reminders

    @staticmethod
    def get_triggered_reminders() -> List[Reminder]:
        """
        Get all triggered reminders.

        Returns:
            List[Reminder]: List of triggered reminders
        """
        triggered_reminders = []

        for reminder in reminders.values():
            if reminder.triggered:
                triggered_reminders.append(reminder)

        return triggered_reminders