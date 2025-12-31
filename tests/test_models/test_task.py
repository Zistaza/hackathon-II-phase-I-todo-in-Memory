import pytest
from src.models.task import Task
from src.exceptions import TaskValidationError


class TestTask:
    """Unit tests for the Task model."""

    def test_task_creation_with_valid_data(self):
        """Test creating a task with valid data."""
        task = Task(id=1, title="Test Task", description="Test Description", completed=False)
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False

    def test_task_creation_with_defaults(self):
        """Test creating a task with default values."""
        task = Task(id=1, title="Test Task")
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description is None
        assert task.completed is False

    def test_task_creation_fails_with_empty_title(self):
        """Test that creating a task with empty title raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            Task(id=1, title="")
        assert "Task title cannot be empty" in str(exc_info.value)

    def test_task_creation_fails_with_whitespace_only_title(self):
        """Test that creating a task with whitespace-only title raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            Task(id=1, title="   ")
        assert "Task title cannot be empty" in str(exc_info.value)

    def test_task_creation_fails_with_long_title(self):
        """Test that creating a task with title exceeding 100 chars raises ValueError."""
        long_title = "A" * 101
        with pytest.raises(ValueError) as exc_info:
            Task(id=1, title=long_title)
        assert "exceeds 100 character limit" in str(exc_info.value)

    def test_task_creation_fails_with_long_description(self):
        """Test that creating a task with description exceeding 500 chars raises ValueError."""
        long_description = "A" * 501
        with pytest.raises(ValueError) as exc_info:
            Task(id=1, title="Test Task", description=long_description)
        assert "exceeds 500 character limit" in str(exc_info.value)

    def test_mark_complete_method(self):
        """Test the mark_complete method."""
        task = Task(id=1, title="Test Task", completed=False)
        task.mark_complete()
        assert task.completed is True

    def test_mark_incomplete_method(self):
        """Test the mark_incomplete method."""
        task = Task(id=1, title="Test Task", completed=True)
        task.mark_incomplete()
        assert task.completed is False

    def test_update_title_with_valid_data(self):
        """Test updating task title with valid data."""
        task = Task(id=1, title="Old Title")
        task.update_title("New Title")
        assert task.title == "New Title"

    def test_update_title_fails_with_empty_title(self):
        """Test that updating task title with empty title raises ValueError."""
        task = Task(id=1, title="Old Title")
        with pytest.raises(ValueError) as exc_info:
            task.update_title("")
        assert "Task title cannot be empty" in str(exc_info.value)

    def test_update_title_fails_with_long_title(self):
        """Test that updating task title with title exceeding 100 chars raises ValueError."""
        task = Task(id=1, title="Old Title")
        long_title = "A" * 101
        with pytest.raises(ValueError) as exc_info:
            task.update_title(long_title)
        assert "exceeds 100 character limit" in str(exc_info.value)

    def test_update_description_with_valid_data(self):
        """Test updating task description with valid data."""
        task = Task(id=1, title="Test Task", description="Old Description")
        task.update_description("New Description")
        assert task.description == "New Description"

    def test_update_description_fails_with_long_description(self):
        """Test that updating task description with description exceeding 500 chars raises ValueError."""
        task = Task(id=1, title="Test Task")
        long_description = "A" * 501
        with pytest.raises(ValueError) as exc_info:
            task.update_description(long_description)
        assert "exceeds 500 character limit" in str(exc_info.value)