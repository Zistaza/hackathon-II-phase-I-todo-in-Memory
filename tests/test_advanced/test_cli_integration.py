"""
Integration tests for CLI functionality in the advanced todo CLI application.
"""
import pytest
from datetime import datetime, timedelta
from src.cli.cli_interface import CLIInterface
from src.services.task_service import TaskService
from src.services.recurrence_service import RecurrenceService


class TestCLIIntegration:
    """Test class for CLI integration with advanced features."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Reset global task storage for clean tests
        from src.services.task_storage import initialize_storage
        initialize_storage()
        self.task_service = TaskService()
        self.cli_interface = CLIInterface(self.task_service)

    def test_upcoming_task_view(self):
        """Test viewing upcoming tasks with CLI."""
        # Create tasks with different due dates
        future_date1 = datetime.now() + timedelta(days=1)
        future_date2 = datetime.now() + timedelta(days=2)

        task1 = self.task_service.add_task(title="Task 1", due_date=future_date1)
        task2 = self.task_service.add_task(title="Task 2", due_date=future_date2)

        # Test the get_upcoming_tasks method
        upcoming_tasks = self.task_service.get_upcoming_tasks()
        assert len(upcoming_tasks) == 2

        # Verify they are sorted by due date
        assert upcoming_tasks[0].id == task1.id
        assert upcoming_tasks[1].id == task2.id

    def test_overdue_task_view(self):
        """Test viewing overdue tasks with CLI."""
        # Create an overdue task
        past_date = datetime.now() - timedelta(days=1)
        overdue_task = self.task_service.add_task(
            title="Overdue task",
            due_date=past_date
        )

        # Create a future task
        future_date = datetime.now() + timedelta(days=1)
        future_task = self.task_service.add_task(
            title="Future task",
            due_date=future_date
        )

        # Test the get_overdue_tasks method
        overdue_tasks = self.task_service.get_overdue_tasks()
        assert len(overdue_tasks) == 1
        assert overdue_tasks[0].id == overdue_task.id

    def test_recurring_task_view(self):
        """Test viewing recurring tasks with CLI."""
        # Create a recurring task
        pattern = RecurrenceService.create_recurrence_pattern("daily")
        recurring_task = self.task_service.add_task(
            title="Daily task",
            recurrence_pattern=pattern
        )

        # Create a non-recurring task
        non_recurring_task = self.task_service.add_task(title="One-time task")

        # Test that recurring tasks can be retrieved
        from src.services.task_storage import recurrence_templates
        assert len(recurrence_templates) == 1
        assert str(recurring_task.id) in recurrence_templates
        assert str(non_recurring_task.id) not in recurrence_templates

    def test_task_with_all_advanced_features(self):
        """Test creating a task with all advanced features."""
        from datetime import datetime, timedelta
        from src.services.recurrence_service import RecurrenceService

        future_date = datetime.now() + timedelta(days=1)
        future_reminder = datetime.now() + timedelta(hours=1)
        pattern = RecurrenceService.create_recurrence_pattern("weekly")

        # Create a task with all advanced features
        task = self.task_service.add_task(
            title="Complete advanced task",
            description="A task with all advanced features",
            priority="high",
            tags=["important", "advanced"],
            due_date=future_date,
            reminder_time=future_reminder,
            recurrence_pattern=pattern
        )

        # Verify all features are set
        assert task.title == "Complete advanced task"
        assert task.description == "A task with all advanced features"
        assert task.priority == "high"
        assert "important" in task.tags
        assert "advanced" in task.tags
        assert task.due_date == future_date
        assert task.reminder_time == future_reminder
        assert task.recurrence_pattern is not None
        assert task.recurrence_pattern.type == "weekly"