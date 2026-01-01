"""
Tests for recurring task functionality in the advanced todo CLI application.
"""
import pytest
from datetime import datetime, timedelta
from src.models.task import Task, RecurrencePattern
from src.services.task_service import TaskService
from src.services.recurrence_service import RecurrenceService


class TestRecurrenceFunctionality:
    """Test class for recurring task functionality."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Reset global task storage for clean tests
        from src.services.task_storage import initialize_storage
        initialize_storage()
        self.task_service = TaskService()
        self.recurrence_service = RecurrenceService()

    def test_daily_recurring_task_functionality(self):
        """Test creating and generating daily recurring tasks."""
        # Create a daily recurrence pattern
        pattern = self.recurrence_service.create_recurrence_pattern("daily")

        # Add a recurring task
        task = self.task_service.add_task(
            title="Daily exercise",
            recurrence_pattern=pattern
        )

        # Verify the task was created with recurrence
        assert task.recurrence_pattern is not None
        assert task.recurrence_pattern.type == "daily"
        assert task.is_recurring_template == True

        # Generate recurring tasks (though they won't generate until next occurrence)
        new_tasks = self.recurrence_service.generate_recurring_tasks()
        assert len(new_tasks) == 0  # No tasks generated yet as next occurrence is in the future

    def test_weekly_recurring_task_functionality(self):
        """Test creating and generating weekly recurring tasks."""
        # Create a weekly recurrence pattern
        pattern = self.recurrence_service.create_recurrence_pattern("weekly")

        # Add a recurring task
        task = self.task_service.add_task(
            title="Weekly meeting",
            recurrence_pattern=pattern
        )

        # Verify the task was created with recurrence
        assert task.recurrence_pattern is not None
        assert task.recurrence_pattern.type == "weekly"

    def test_custom_recurring_task_functionality(self):
        """Test creating and generating custom recurring tasks."""
        # Create a custom recurrence pattern (every 3 days)
        pattern = self.recurrence_service.create_recurrence_pattern("custom", interval=3)

        # Add a recurring task
        task = self.task_service.add_task(
            title="Water plants",
            recurrence_pattern=pattern
        )

        # Verify the task was created with recurrence
        assert task.recurrence_pattern is not None
        assert task.recurrence_pattern.type == "custom"
        assert task.recurrence_pattern.interval == 3

    def test_cancel_recurring_pattern(self):
        """Test canceling a recurring pattern."""
        # Create and add a recurring task
        pattern = self.recurrence_service.create_recurrence_pattern("daily")
        task = self.task_service.add_task(
            title="Cancel test task",
            recurrence_pattern=pattern
        )

        # Verify it's a recurring template initially
        assert task in self.task_service.get_all_tasks()

        # Cancel the recurrence
        success = self.task_service.cancel_recurrence_for_task(task.id)
        assert success is True

        # Verify the recurrence was canceled
        from src.services.task_storage import recurrence_templates
        assert task.id not in recurrence_templates

    def test_update_recurring_pattern(self):
        """Test updating a recurring pattern."""
        # Create and add a recurring task with daily pattern
        pattern = self.recurrence_service.create_recurrence_pattern("daily")
        task = self.task_service.add_task(
            title="Update test task",
            recurrence_pattern=pattern
        )

        # Verify initial pattern
        assert task.recurrence_pattern.type == "daily"

        # Update to weekly pattern
        new_pattern = self.recurrence_service.create_recurrence_pattern("weekly")
        success = self.task_service.update_recurrence_for_task(task.id, new_pattern)
        assert success is True