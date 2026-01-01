"""
Tests for reminder functionality in the advanced todo CLI application.
"""
import pytest
from datetime import datetime, timedelta
from src.models.task import Task
from src.services.task_service import TaskService
from src.services.reminder_service import ReminderService


class TestReminderFunctionality:
    """Test class for reminder functionality."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Reset global task storage for clean tests
        from src.services.task_storage import initialize_storage
        initialize_storage()
        self.task_service = TaskService()
        self.reminder_service = ReminderService()

    def test_due_date_functionality(self):
        """Test setting due dates for tasks."""
        future_date = datetime.now() + timedelta(days=1)

        # Add a task with a due date
        task = self.task_service.add_task(
            title="Test due date",
            due_date=future_date
        )

        # Verify the due date was set
        assert task.due_date == future_date

        # Test updating due date
        new_future_date = datetime.now() + timedelta(days=2)
        updated_task = self.task_service.update_task(
            task_id=task.id,
            due_date=new_future_date
        )
        assert updated_task.due_date == new_future_date

    def test_reminder_functionality(self):
        """Test setting reminders for tasks."""
        future_date = datetime.now() + timedelta(days=1)
        future_reminder = datetime.now() + timedelta(hours=1)

        # Add a task with a due date and reminder
        task = self.task_service.add_task(
            title="Test reminder",
            due_date=future_date,
            reminder_time=future_reminder
        )

        # Verify the reminder was set
        assert task.reminder_time == future_reminder

        # Test updating reminder
        new_reminder = datetime.now() + timedelta(hours=2)
        updated_task = self.task_service.update_task(
            task_id=task.id,
            reminder_time=new_reminder
        )
        assert updated_task.reminder_time == new_reminder

    def test_upcoming_tasks_view(self):
        """Test getting upcoming tasks sorted by due date."""
        # Create tasks with different due dates
        future_date1 = datetime.now() + timedelta(days=2)
        future_date2 = datetime.now() + timedelta(days=1)
        future_date3 = datetime.now() + timedelta(days=3)

        task1 = self.task_service.add_task(title="Task 1", due_date=future_date1)
        task2 = self.task_service.add_task(title="Task 2", due_date=future_date2)
        task3 = self.task_service.add_task(title="Task 3", due_date=future_date3)

        # Get upcoming tasks
        upcoming_tasks = self.task_service.get_upcoming_tasks()

        # Verify we have 3 tasks
        assert len(upcoming_tasks) == 3

        # Verify they are sorted by due date (earliest first)
        assert upcoming_tasks[0].id == task2.id  # 1 day
        assert upcoming_tasks[1].id == task1.id  # 2 days
        assert upcoming_tasks[2].id == task3.id  # 3 days

    def test_overdue_task_detection(self):
        """Test detecting overdue tasks."""
        past_date = datetime.now() - timedelta(days=1)
        future_date = datetime.now() + timedelta(days=1)

        # Add an overdue task
        overdue_task = self.task_service.add_task(
            title="Overdue task",
            due_date=past_date
        )

        # Add a future task
        future_task = self.task_service.add_task(
            title="Future task",
            due_date=future_date
        )

        # Get overdue tasks
        overdue_tasks = self.task_service.get_overdue_tasks()

        # Verify only the past-dated task is considered overdue
        assert len(overdue_tasks) == 1
        assert overdue_tasks[0].id == overdue_task.id

        # Verify the future task is not in the overdue list
        assert future_task.id not in [t.id for t in overdue_tasks]