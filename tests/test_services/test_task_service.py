import pytest
from src.services.task_service import TaskService
from src.models.task import Task
from src.exceptions import TaskNotFoundError, TaskValidationError


class TestTaskService:
    """Unit tests for the TaskService."""

    def test_initialization(self):
        """Test that TaskService initializes with empty task list and ID counter."""
        service = TaskService()
        assert len(service.get_all_tasks()) == 0
        assert service._next_id == 1

    def test_add_task_with_title_only(self):
        """Test adding a task with title only."""
        service = TaskService()
        task = service.add_task("Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description is None
        assert task.completed is False
        assert task.priority == "medium"  # Default priority
        assert task.tags == []  # Default tags
        assert len(service.get_all_tasks()) == 1

    def test_add_task_with_title_and_description(self):
        """Test adding a task with title and description."""
        service = TaskService()
        task = service.add_task("Test Task", "Test Description")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False
        assert task.priority == "medium"  # Default priority
        assert task.tags == []  # Default tags
        assert len(service.get_all_tasks()) == 1

    def test_add_task_with_priority_and_tags(self):
        """Test adding a task with priority and tags."""
        service = TaskService()
        task = service.add_task("Test Task", "Test Description", "high", ["work", "urgent"])

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False
        assert task.priority == "high"
        assert set(task.tags) == {"work", "urgent"}
        assert len(service.get_all_tasks()) == 1

    def test_add_task_generates_sequential_ids(self):
        """Test that TaskService generates sequential IDs."""
        service = TaskService()
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_fails_with_empty_title(self):
        """Test that adding a task with empty title raises TaskValidationError."""
        service = TaskService()
        with pytest.raises(TaskValidationError) as exc_info:
            service.add_task("")
        assert "Task title cannot be empty" in str(exc_info.value)

    def test_add_task_fails_with_long_title(self):
        """Test that adding a task with title exceeding 100 chars raises TaskValidationError."""
        service = TaskService()
        long_title = "A" * 101
        with pytest.raises(TaskValidationError) as exc_info:
            service.add_task(long_title)
        assert "exceeds 100 character limit" in str(exc_info.value)

    def test_add_task_fails_with_long_description(self):
        """Test that adding a task with description exceeding 500 chars raises TaskValidationError."""
        service = TaskService()
        long_description = "A" * 501
        with pytest.raises(TaskValidationError) as exc_info:
            service.add_task("Test Task", long_description)
        assert "exceeds 500 character limit" in str(exc_info.value)

    def test_add_task_fails_with_invalid_priority(self):
        """Test that adding a task with invalid priority raises TaskValidationError."""
        service = TaskService()
        with pytest.raises(TaskValidationError) as exc_info:
            service.add_task("Test Task", priority="invalid")
        assert "Priority must be one of: high, medium, low" in str(exc_info.value)

    def test_add_task_fails_with_invalid_tags(self):
        """Test that adding a task with invalid tags raises TaskValidationError."""
        service = TaskService()

        # Test empty tag
        with pytest.raises(TaskValidationError) as exc_info:
            service.add_task("Test Task", tags=["", "valid"])
        assert "Tag cannot be empty" in str(exc_info.value)

        # Test tag with spaces
        with pytest.raises(TaskValidationError) as exc_info:
            service.add_task("Test Task", tags=["valid", "with spaces"])
        assert "Tag cannot contain spaces" in str(exc_info.value)

    def test_get_all_tasks_returns_all_tasks(self):
        """Test that get_all_tasks returns all tasks."""
        service = TaskService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")

        tasks = service.get_all_tasks()
        assert len(tasks) == 3
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"
        assert tasks[2].title == "Task 3"

    def test_get_all_tasks_returns_copy_of_list(self):
        """Test that get_all_tasks returns a copy of the internal list."""
        service = TaskService()
        service.add_task("Task 1")

        tasks = service.get_all_tasks()
        tasks.append("fake_task")

        # Original list should not be affected
        assert len(service.get_all_tasks()) == 1

    def test_get_task_by_id_returns_correct_task(self):
        """Test that get_task_by_id returns the correct task."""
        service = TaskService()
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")

        retrieved_task = service.get_task_by_id(1)
        assert retrieved_task.id == task1.id
        assert retrieved_task.title == task1.title

        retrieved_task = service.get_task_by_id(2)
        assert retrieved_task.id == task2.id
        assert retrieved_task.title == task2.title

    def test_get_task_by_id_raises_error_for_nonexistent_task(self):
        """Test that get_task_by_id raises TaskNotFoundError for non-existent task."""
        service = TaskService()
        service.add_task("Task 1")

        with pytest.raises(TaskNotFoundError) as exc_info:
            service.get_task_by_id(999)
        assert "Task with ID 999 not found" in str(exc_info.value)

    def test_update_task_updates_title(self):
        """Test updating task title."""
        service = TaskService()
        original_task = service.add_task("Original Title")

        updated_task = service.update_task(1, title="New Title")

        assert updated_task.id == 1
        assert updated_task.title == "New Title"
        assert updated_task.description is None
        assert updated_task.priority == "medium"  # Should keep default priority
        assert updated_task.tags == []  # Should keep default tags

    def test_update_task_updates_description(self):
        """Test updating task description."""
        service = TaskService()
        original_task = service.add_task("Title", "Original Description")

        updated_task = service.update_task(1, description="New Description")

        assert updated_task.id == 1
        assert updated_task.title == "Title"
        assert updated_task.description == "New Description"

    def test_update_task_updates_priority(self):
        """Test updating task priority."""
        service = TaskService()
        original_task = service.add_task("Title", priority="low")

        updated_task = service.update_task(1, priority="high")

        assert updated_task.id == 1
        assert updated_task.title == "Title"
        assert updated_task.priority == "high"

    def test_update_task_updates_tags(self):
        """Test updating task tags."""
        service = TaskService()
        original_task = service.add_task("Title", tags=["old"])

        updated_task = service.update_task(1, tags=["new", "tags"])

        assert updated_task.id == 1
        assert updated_task.title == "Title"
        assert set(updated_task.tags) == {"new", "tags"}

    def test_update_task_updates_all_fields(self):
        """Test updating all task fields at once."""
        service = TaskService()
        original_task = service.add_task("Old Title", "Old Description", "low", ["old", "tags"])

        updated_task = service.update_task(
            1,
            title="New Title",
            description="New Description",
            priority="high",
            tags=["new", "tags"]
        )

        assert updated_task.id == 1
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"
        assert updated_task.priority == "high"
        assert set(updated_task.tags) == {"new", "tags"}

    def test_update_task_fails_with_invalid_id(self):
        """Test that updating task with invalid ID raises TaskNotFoundError."""
        service = TaskService()
        service.add_task("Task 1")

        with pytest.raises(TaskNotFoundError) as exc_info:
            service.update_task(999, title="New Title")
        assert "Task with ID 999 not found" in str(exc_info.value)

    def test_update_task_fails_with_empty_title(self):
        """Test that updating task with empty title raises TaskValidationError."""
        service = TaskService()
        service.add_task("Task 1")

        with pytest.raises(TaskValidationError) as exc_info:
            service.update_task(1, title="")
        assert "Task title cannot be empty" in str(exc_info.value)

    def test_update_task_fails_with_long_title(self):
        """Test that updating task with long title raises TaskValidationError."""
        service = TaskService()
        service.add_task("Task 1")

        long_title = "A" * 101
        with pytest.raises(TaskValidationError) as exc_info:
            service.update_task(1, title=long_title)
        assert "exceeds 100 character limit" in str(exc_info.value)

    def test_update_task_fails_with_invalid_priority(self):
        """Test that updating task with invalid priority raises TaskValidationError."""
        service = TaskService()
        service.add_task("Task 1")

        with pytest.raises(TaskValidationError) as exc_info:
            service.update_task(1, priority="invalid")
        assert "Priority must be one of: high, medium, low" in str(exc_info.value)

    def test_update_task_fails_with_invalid_tags(self):
        """Test that updating task with invalid tags raises TaskValidationError."""
        service = TaskService()
        service.add_task("Task 1")

        # Test empty tag
        with pytest.raises(TaskValidationError) as exc_info:
            service.update_task(1, tags=["", "valid"])
        assert "Tag cannot be empty" in str(exc_info.value)

        # Test tag with spaces
        with pytest.raises(TaskValidationError) as exc_info:
            service.update_task(1, tags=["valid", "with spaces"])
        assert "Tag cannot contain spaces" in str(exc_info.value)

    def test_delete_task_removes_task(self):
        """Test that delete_task removes the task."""
        service = TaskService()
        service.add_task("Task 1")
        service.add_task("Task 2")

        result = service.delete_task(1)

        assert result is True
        remaining_tasks = service.get_all_tasks()
        assert len(remaining_tasks) == 1
        assert remaining_tasks[0].title == "Task 2"

    def test_delete_task_fails_with_invalid_id(self):
        """Test that delete_task raises TaskNotFoundError for non-existent task."""
        service = TaskService()
        service.add_task("Task 1")

        with pytest.raises(TaskNotFoundError) as exc_info:
            service.delete_task(999)
        assert "Task with ID 999 not found" in str(exc_info.value)

    def test_update_task_status_marks_complete(self):
        """Test updating task status to complete."""
        service = TaskService()
        task = service.add_task("Task 1")
        assert task.completed is False

        updated_task = service.update_task_status(1, True)
        assert updated_task.completed is True

    def test_update_task_status_marks_incomplete(self):
        """Test updating task status to incomplete."""
        service = TaskService()
        task = service.add_task("Task 1")
        # First mark as complete
        service.update_task_status(1, True)
        assert task.completed is True

        updated_task = service.update_task_status(1, False)
        assert updated_task.completed is False

    def test_update_task_status_fails_with_invalid_id(self):
        """Test that update_task_status raises TaskNotFoundError for non-existent task."""
        service = TaskService()
        service.add_task("Task 1")

        with pytest.raises(TaskNotFoundError) as exc_info:
            service.update_task_status(999, True)
        assert "Task with ID 999 not found" in str(exc_info.value)